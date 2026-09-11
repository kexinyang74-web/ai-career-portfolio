"""Real browser smoke test with an isolated database and a fake model.

Run: python tests/browser_check.py
No real API keys, external model calls or personal records are used.
"""
import sys
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import create_app
from test_app import FakeProvider


def main():
    output = ROOT / "test-results"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        app = create_app(Path(temp) / "browser.db", FakeProvider())
        config = uvicorn.Config(app, host="127.0.0.1", port=18765, log_level="error")
        server = uvicorn.Server(config)
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        for _ in range(100):
            if server.started:
                break
            time.sleep(.05)
        assert server.started
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=1)
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto("http://127.0.0.1:18765/topics")
                page.locator("#busy").wait_for(state="hidden")
                page.screenshot(path=str(output / "desktop-empty.png"), full_page=True)
                page.locator("#message-input").fill("我刚入职，整理学习笔记很费时间，还没有试过 AI。")
                page.locator("#send").click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator(".message").count() == 3
                page.locator("#generate").click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator("#topics .topic-card").count() == 6
                assert page.locator("#research-notice").is_visible()
                page.locator("#topics .topic-card").first.get_by_role("button", name="♡ 收藏", exact=True).click()
                page.locator("#busy").wait_for(state="hidden")
                page.locator("#topics .topic-card").first.get_by_role("button", name="展开策划单 ↗").click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator("#plan-dialog").is_visible()
                assert "亲测步骤" in page.locator("#plan-content").inner_text()
                assert page.locator('#close-dialog').bounding_box()['y'] > 0
                page.screenshot(path=str(output / "brief.png"))
                page.locator("#close-dialog").click()
                page.locator('.nav[data-view="favorites"]').click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator("#favorites .topic-card").count() == 1
                page.locator("#favorites select").select_option("已发布")
                page.locator("#busy").wait_for(state="hidden")
                page.get_by_role("button", name="已发布", exact=True).click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator("#favorites .topic-card").count() == 1
                page.locator('.nav[data-view="profile"]').click()
                page.locator("#busy").wait_for(state="hidden")
                page.locator('[name="audience"]').fill("毕业一年，正在适应职场的年轻人")
                page.get_by_role("button", name="保存定位").click()
                page.locator("#busy").wait_for(state="hidden")
                page.reload()
                page.locator("#busy").wait_for(state="hidden")
                assert "毕业一年" in page.locator("#audience-summary").inner_text()
                assert page.locator("#topics .topic-card").count() == 6
                # Reject a topic, save rationale and regenerate through actual handlers.
                page.locator("#topics .topic-card").last.get_by_role("button", name="不适合", exact=True).click()
                page.locator("#busy").wait_for(state="hidden")
                page.locator("#topics .feedback-note input").fill("没有相关经验")
                page.locator("#topics .feedback-note").get_by_role("button", name="保存反馈").click()
                page.locator("#busy").wait_for(state="hidden")
                page.locator("#generate").click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator("#topics .topic-card").count() == 5
                page.screenshot(path=str(output / "desktop-topics.png"), full_page=True)
                page.set_viewport_size({"width":390,"height":844})
                page.screenshot(path=str(output / "mobile.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "horizontal overflow"
                page.locator('.nav[data-view="history"]').click()
                page.locator("#busy").wait_for(state="hidden")
                assert page.locator(".history-item").count() == 1
                assert not errors, errors
                assert page.locator("#error").is_hidden()
                browser.close()
        finally:
            server.should_exit = True
            thread.join(timeout=10)
    print("Browser PASS: chat, 6 cards, brief, favorite/status, profile persistence, feedback/regeneration, history, 390px layout; no JS errors; clean shutdown.")


if __name__ == "__main__":
    main()
