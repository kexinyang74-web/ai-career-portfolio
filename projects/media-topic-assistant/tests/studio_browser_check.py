"""Studio real-browser manual workflow; always uses an isolated temporary database."""
import sys
import base64
import tempfile
import threading
import time
from pathlib import Path

import uvicorn
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import create_app
from test_studio import StudioFake


def main():
    output = ROOT / "test-results"
    output.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        provider = StudioFake()
        server = uvicorn.Server(uvicorn.Config(create_app(Path(tmp) / "studio.db", provider), host="127.0.0.1", port=18766, log_level="error"))
        thread = threading.Thread(target=server.run, daemon=True)
        thread.start()
        for _ in range(100):
            if server.started:
                break
            time.sleep(.05)
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch()
                page = browser.new_page(viewport={"width":1440,"height":1000})
                errors = []
                page.on("pageerror", lambda e: errors.append(str(e)))
                page.goto("http://127.0.0.1:18766")
                expect(page.locator('[data-view="home"]')).to_be_visible(timeout=5000)
                expect(page.locator("#studio-busy")).to_be_hidden()
                page.screenshot(path=str(output / "studio-home.png"), full_page=True)
                page.locator('[data-view="materials"]').click()
                page.get_by_label("素材标题", exact=True).fill("周报亲测记录")
                page.get_by_label("素材正文", exact=True).fill("今天亲测整理周报花了 20 分钟。<script>alert(1)</script>")
                page.get_by_label("附加图片（可多选）").set_input_files({"name":"example.png", "mimeType":"image/png", "buffer":base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=")})
                page.get_by_role("button", name="保存素材", exact=True).click()
                expect(page.locator("#material-list")).to_contain_text("周报亲测记录")
                expect(page.locator("#material-list img")).to_have_count(1)
                assert page.locator("#material-list script").count() == 0
                page.locator('[data-view="works"]').click()
                page.get_by_label("作品标题", exact=True).fill("第一次周报实践")
                lost_response = {"done": False}
                def drop_saved_response(route):
                    if route.request.method == "POST" and not lost_response["done"]:
                        route.fetch()
                        lost_response["done"] = True
                        route.abort("failed")
                    else:
                        route.continue_()
                page.route("**/api/studio/works", drop_saved_response)
                page.get_by_role("button", name="创建作品", exact=True).click()
                expect(page.locator("#studio-error")).to_contain_text("无法连接")
                expect(page.get_by_label("作品标题", exact=True)).to_have_value("第一次周报实践")
                page.get_by_role("button", name="创建作品", exact=True).click()
                expect(page.locator("#work-detail")).to_contain_text("第一次周报实践")
                assert len(page.request.get("http://127.0.0.1:18766/api/studio/works").json()) == 1, "lost response retry duplicated work"
                page.unroute("**/api/studio/works", drop_saved_response)
                page.locator("#work-materials input").check()
                page.get_by_role("button", name="保存作品信息", exact=True).click()
                expect(page.locator("#studio-busy")).to_be_hidden()
                page.get_by_role("button", name="添加内容形式", exact=True).click()
                expect(page.locator("#variant-picker option")).to_have_count(1)
                page.get_by_label("人工稿件正文", exact=True).fill("# 周报\n真实记录，不编造数字。")
                page.get_by_role("button", name="保存人工版本", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("真实记录，不编造数字。")
                page.locator("#artifact-list").get_by_role("button", name="确认此版本", exact=True).first.click()
                expect(page.locator("#artifact-list")).to_contain_text("已确认")
                page.get_by_role("button", name="生成制作清单", exact=True).click()
                expect(page.locator("#task-list input[type=checkbox]").first).to_be_visible()
                page.get_by_label("发布链接", exact=True).fill("https://example.com/post/1")
                page.get_by_label("播放 / 阅读量", exact=True).fill("100")
                page.get_by_role("button", name="保存发布记录", exact=True).click()
                expect(page.locator("#publication-list")).to_contain_text("100")
                assert not provider.calls, "manual workflow unexpectedly called model"
                task = page.locator("#task-list .task").first
                task.locator('input[type="checkbox"]').check()
                task.get_by_label("实际小时", exact=True).fill("0.5")
                task.get_by_role("button", name="保存任务", exact=True).click()
                expect(page.locator("#task-list .task").first).to_have_class("task done")
                page.locator("#publication-list").get_by_role("button", name="编辑发布记录").click()
                page.get_by_label("播放 / 阅读量", exact=True).fill("150")
                page.get_by_role("button", name="保存发布记录", exact=True).click()
                expect(page.locator("#publication-list")).to_contain_text("150")
                # A publication being edited must never carry its id into work B.
                page.get_by_label("作品标题", exact=True).fill("独立的第二篇作品")
                page.get_by_role("button", name="创建作品", exact=True).click()
                expect(page.locator("#work-title")).to_have_text("独立的第二篇作品")
                page.locator('#variant-form [name="platform"]').fill("B站")
                page.get_by_role("button", name="添加内容形式", exact=True).click()
                expect(page.locator("#studio-busy")).to_be_hidden()
                page.locator("#work-list").get_by_role("button", name="第一次周报实践").click()
                expect(page.locator("#work-title")).to_have_text("第一次周报实践")
                page.locator("#publication-list").get_by_role("button", name="编辑发布记录").click()
                original_publication = page.locator('#publication-form [name="id"]').input_value()
                assert original_publication
                page.locator("#work-list").get_by_role("button", name="独立的第二篇作品").click()
                expect(page.locator("#work-title")).to_have_text("独立的第二篇作品")
                expect(page.locator('#publication-form [name="id"]')).to_have_value("")
                expect(page.locator('#publication-form [name="platform"]')).to_have_value("B站")
                page.get_by_label("播放 / 阅读量", exact=True).fill("200")
                page.get_by_role("button", name="保存发布记录", exact=True).click()
                expect(page.locator("#publication-list")).to_contain_text("200")
                records = page.request.get("http://127.0.0.1:18766/api/studio/works").json()
                first = next(w for w in records if w["title"] == "第一次周报实践")
                second_work = next(w for w in records if w["title"] == "独立的第二篇作品")
                assert first["variants"][0]["publications"][0]["metrics"]["views"] == 150
                assert second_work["variants"][0]["publications"][0]["id"] != original_publication
                page.locator("#work-list").get_by_role("button", name="第一次周报实践").click()
                expect(page.locator("#work-title")).to_have_text("第一次周报实践")

                # All eight helpers, including structured local editing and cross-form adaptation.
                page.locator('[data-view="profile"]').click()
                page.get_by_label("我的定位访谈", exact=True).fill("我是刚入职的初学者，每周记录一次真实实践。")
                page.get_by_role("button", name="生成三个定位候选", exact=True).click()
                expect(page.locator("#positioning-candidates .panel")).to_have_count(3)
                for iteration in range(3):
                    page.get_by_label("我的定位访谈", exact=True).fill(f"补充第 {iteration + 2} 次访谈：每周记录真实实践。")
                    page.get_by_role("button", name="生成三个定位候选", exact=True).click()
                    expect(page.locator("#studio-busy")).to_be_hidden()
                latest_positioning = page.request.get("http://127.0.0.1:18766/api/studio/positioning").json()[-1]["id"]
                page.locator('[data-view="materials"]').click()
                expect(page.locator("#view-materials")).to_be_visible()
                page.locator('[data-view="profile"]').click()
                expect(page.locator(f'[data-positioning-id="{latest_positioning}"]')).to_have_count(3)
                page.get_by_role("button", name="采用并填写定位", exact=True).first.click()
                page.locator('[data-direction]').first.fill("职场实践")
                page.get_by_role("button", name="保存定位新版本", exact=True).click()
                expect(page.locator("#profile-versions")).to_contain_text("v2")
                legacy = browser.new_page()
                legacy.goto("http://127.0.0.1:18766/topics")
                legacy.locator("#busy").wait_for(state="hidden")
                legacy.locator('.nav[data-view="profile"]').click()
                expect(legacy.locator("#custom-weight-note")).to_be_visible()
                legacy.get_by_role("button", name="保存定位", exact=True).click()
                legacy.locator("#busy").wait_for(state="hidden")
                assert "职场实践" in legacy.request.get("http://127.0.0.1:18766/api/profile").json()["weights"]
                legacy.close()
                page.locator('[data-view="materials"]').click()
                page.get_by_role("button", name="06 · 案例拆解", exact=True).click()
                expect(page.locator("#material-list details")).to_have_count(1)
                page.locator('[data-view="works"]').click()
                lost_response["done"] = False
                page.route("**/api/studio/works/*/generate", drop_saved_response)
                page.get_by_role("button", name="生成策划单", exact=True).click()
                expect(page.locator("#studio-error")).to_contain_text("无法连接")
                page.get_by_role("button", name="生成策划单", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("策划单")
                saved_work = next(w for w in page.request.get("http://127.0.0.1:18766/api/studio/works").json() if w["title"] == "第一次周报实践")
                assert len([a for a in saved_work["artifacts"] if a["kind"] == "brief"]) == 1, "lost generation response duplicated artifact"
                page.unroute("**/api/studio/works/*/generate", drop_saved_response)
                page.get_by_role("button", name="生成当前形式稿件", exact=True).click()
                expect(page.locator("#artifact-list .section-editor")).to_have_count(6)
                page.locator('[data-view="home"]').click()
                expect(page.locator("#view-home")).to_be_visible()
                expect(page.locator("#recent-works")).to_contain_text("准备标题、封面与发布包装")
                page.locator('[data-view="works"]').click()
                expect(page.locator("#view-works")).to_be_visible()
                original_id = page.locator("#artifact-list .artifact").first.get_attribute("data-artifact-id")
                second = page.locator("#artifact-list .section-editor").nth(1)
                second.locator("summary").click()
                second.get_by_label("正文 / 口播", exact=True).fill("第二段还没有保存的独立编辑")
                section = page.locator("#artifact-list .section-editor").first
                section.locator("summary").click()
                section.get_by_label("正文 / 口播", exact=True).fill("人工修订这一段")
                section.get_by_role("button", name="保存本段人工修改", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("人工修订这一段")
                kept = page.locator(f'[data-artifact-id="{original_id}"] [data-section-index="1"]')
                expect(kept.get_by_label("正文 / 口播", exact=True)).to_have_value("第二段还没有保存的独立编辑")
                expect(kept).to_be_visible()
                kept.get_by_role("button", name="放弃本段未保存修改", exact=True).click()
                section = page.locator("#artifact-list .section-editor").first
                section.locator("summary").click()
                section.get_by_label("这一段想怎么改？", exact=True).fill("说明具体观察，不编造结果")
                section.get_by_role("button", name="让助手修改本段", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("修改后的这一段")
                page.locator("#source-picker").select_option(index=1)
                page.get_by_role("button", name="生成标题封面与发布包装", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("发布包装")
                page.get_by_role("button", name="生成单篇复盘", exact=True).click()
                expect(page.locator("#artifact-list")).to_contain_text("单篇复盘")
                # Failure retains existing text and autosaves a newly typed manual draft first.
                provider.fail = True
                page.get_by_label("人工稿件正文", exact=True).fill("失败前新写的人工内容必须保留")
                page.get_by_role("button", name="生成当前形式稿件", exact=True).click()
                expect(page.locator("#studio-error")).to_contain_text("超时")
                expect(page.get_by_label("人工稿件正文", exact=True)).to_have_value("失败前新写的人工内容必须保留")
                provider.fail = False
                page.get_by_role("button", name="清空编辑器", exact=True).click()
                expect(page.get_by_label("人工稿件正文", exact=True)).to_have_value("")
                for form in ["口播", "录屏教程", "生活记录", "混合视频"]:
                    page.locator("#new-form").select_option(form)
                    page.get_by_role("button", name="添加内容形式", exact=True).click()
                    expect(page.locator("#studio-busy")).to_be_hidden()
                    page.locator("#source-picker").select_option(index=1)
                    page.get_by_role("button", name="生成当前形式稿件", exact=True).click()
                    expect(page.locator("#artifact-list .section-editor")).to_have_count(3)
                assert {c[1]['variant']['form'] for c in provider.calls if c[0] == 'studio.draft'} == {'图文','口播','录屏教程','生活记录','混合视频'}
                expect(page.locator("#view-works")).to_be_visible()
                expect(page.locator("#studio-busy")).to_be_hidden()
                expect(page.locator("#studio-toast")).to_be_hidden(timeout=5000)
                page.screenshot(path=str(output / "studio-ai-work.png"), full_page=True)
                page.locator('[data-view="home"]').click()
                page.get_by_role("button", name="按时间预算排期", exact=True).click()
                expect(page.locator("#weekly-tasks .task").first).to_be_visible()
                page.locator('[data-view="reviews"]').click()
                page.get_by_role("button", name="生成周期复盘", exact=True).click()
                expect(page.locator("#review-list")).to_contain_text("周期复盘")
                page.get_by_label("从这次复盘想到的待验证选题", exact=True).first.fill("下一次比较整理周报的两种方法")
                page.get_by_role("button", name="采纳为待验证选题", exact=True).first.click()
                expect(page.locator("#studio-toast")).to_contain_text("回流")
                page.locator('[data-view="topics"]').click()
                expect(page.locator("#favorite-list")).to_contain_text("下一次比较整理周报的两种方法")
                page.locator('[data-view="works"]').click()
                expect(page.locator("#view-works")).to_be_visible()
                expect(page.locator("#work-detail")).to_be_visible()
                expect(page.locator("#studio-busy")).to_be_hidden()
                expect(page.locator("#studio-toast")).to_be_hidden(timeout=5000)
                page.evaluate("window.scrollTo(0, 0)")
                page.screenshot(path=str(output / "studio-work.png"), full_page=True)
                page.screenshot(path=str(output / "studio-work-viewport.png"))
                page.set_viewport_size({"width":390,"height":844})
                expect(page.locator("#view-works")).to_be_visible()
                page.evaluate("window.scrollTo(0, 0)")
                page.screenshot(path=str(output / "studio-mobile.png"), full_page=True)
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "horizontal overflow"
                page.reload()
                expect(page.locator("#studio-busy")).to_be_hidden()
                expect(page.locator("#work-detail")).to_be_visible()
                expect(page.locator("#work-detail")).to_contain_text("第一次周报实践")
                assert not errors, errors
                browser.close()
                print("Studio browser workflow passed; screenshots in test-results/studio-*.png")
        finally:
            server.should_exit = True
            thread.join(timeout=5)


if __name__ == "__main__":
    main()
