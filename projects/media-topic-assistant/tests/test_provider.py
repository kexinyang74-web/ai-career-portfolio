import json

import httpx
import pytest

from provider import DeepSeekProvider, ProviderError


def response(text, annotations=None, searched=False):
    output = [{"type": "message", "content": [{"type": "output_text", "text": text, "annotations": annotations or []}]}]
    if searched:
        output.insert(0, {"type": "web_search_call", "status": "completed"})
    return {"status": "completed", "output": output}


def provider(handler):
    return DeepSeekProvider(api_key="test-secret-must-not-leak", transport=httpx.MockTransport(handler))


def test_missing_key_does_not_attempt_network():
    p = DeepSeekProvider(api_key="", transport=httpx.MockTransport(lambda _: pytest.fail("network must not be called")))
    with pytest.raises(ProviderError) as exc:
        p.generate("question", {}, {})
    assert exc.value.code == "missing_key"


@pytest.mark.parametrize("status,code", [(401,"invalid_key"), (402,"insufficient_balance"), (429,"rate_limit"), (500,"upstream_error")])
def test_upstream_error_is_sanitized(status, code):
    p = provider(lambda _: httpx.Response(status, text="test-secret-must-not-leak"))
    with pytest.raises(ProviderError) as exc:
        p.generate("question", {}, {})
    assert exc.value.code == code
    assert "test-secret" not in str(exc.value)


def test_timeout_is_sanitized():
    def handler(request):
        raise httpx.ReadTimeout("test-secret-must-not-leak", request=request)
    with pytest.raises(ProviderError) as exc:
        provider(handler).generate("question", {}, {})
    assert exc.value.status == 504
    assert "test-secret" not in str(exc.value)


@pytest.mark.parametrize("payload", [response("not-json"), {"status":"incomplete","output":[]}, []])
def test_invalid_output_is_rejected(payload):
    with pytest.raises(ProviderError):
        provider(lambda _: httpx.Response(200, json=payload)).generate("topics", {}, {})


def test_generate_uses_official_endpoint_and_json_format():
    def handler(request):
        assert str(request.url) == "https://api.deepseek.com/responses"
        body = json.loads(request.content)
        assert body["text"]["format"]["type"] == "json_object"
        assert "只返回JSON" in body["instructions"]
        return httpx.Response(200, json=response('{"question":"尝试了什么？"}'))
    assert provider(handler).generate("question", {}, {})["question"] == "尝试了什么？"


def test_ignored_search_is_not_evidence_and_is_cached():
    calls = []
    def handler(request):
        calls.append(request)
        return httpx.Response(200, json=response('{"references":[{"topic_id":"t1","url":"https://fake.example"}]}'))
    p = provider(handler)
    topics = [{"id":"t1", "external_claims":["export available"]}]
    assert p.research(topics)[0] == {}
    assert p.research(topics)[0] == {}
    assert len(calls) == 1
    assert p.search_status == "unavailable"


def test_only_completed_search_citations_can_be_linked_to_topics():
    refs = {"references":[{"topic_id":"t1","url":"https://docs.example/feature", "claim":"export"},
                          {"topic_id":"t1","url":"https://invented.example", "claim":"fake"},
                          {"topic_id":"wrong-id","url":"https://docs.example/feature"}]}
    annotations = [{"type":"url_citation","url":"https://docs.example/feature","title":"Official docs"}]
    p = provider(lambda _: httpx.Response(200, json=response(json.dumps(refs), annotations, True)))
    results, _ = p.research([{"id":"t1","external_claims":["export"]}])
    assert list(results) == ["t1"]
    assert len(results["t1"]) == 1
    assert results["t1"][0]["url"] == "https://docs.example/feature"


def test_search_failure_is_nonfatal():
    p = provider(lambda _: httpx.Response(400))
    refs, notice = p.research([{"id":"t1","external_claims":["export"]}])
    assert not refs and "未核实" in notice


def test_no_external_claims_no_search_call():
    p = provider(lambda _: pytest.fail("unnecessary search"))
    assert p.research([{"id":"t1", "external_claims":[]}]) == ({}, "")
