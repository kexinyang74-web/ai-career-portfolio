# 1. 这个函数接收两个输入 tid 和 body 
# 2. 成功后返回 topic
# 3. 选题不存在则返回 404
# 4. 它最终要把修改保存到数据库中。还有本地内存中。
@app.patch("/api/topics/{tid}")
def patch_topic(tid: str, body: TopicPatch):
    with writing():
        topic = topic_or_404(tid)
        updates = body.model_dump(exclude_none=True)
        if updates.get("favorite") and not topic["favorite"]:
            topic["status"] = "待创作"
        topic.update(updates)
        return db.save_topic(topic)


# ===== 差异记录（2026-10-08 本人版 vs 原版）=====
# 【语法错】跑一次 py_compile 就报，不涉及理解：
#   - @app.PATCH  → @app.patch（方法名小写）
#   - "api/topic/{tid})  → "/api/topics/{tid}"（缺开头 /、少 s、引号括号没闭合）
#   - with writing()  → with writing():（缺冒号）
# 【记岔了 / 忘了】记忆缺口，需多默写：
#   - updates = body.???  → body.model_dump(exclude_none=True)（记得意思，忘了 API）
#   - if (...)  → if updates.get("favorite") and not topic["favorite"]:（骨架对，细节忘）
# 【漏了】原版有、本人版没有：
#   - topic["status"] = "待创作"（复述时说对，默写时整行没写出来）
# 【写对了】：
#   - def patch_topic(tid: str, body: TopicPatch):
#   - topic = topic_or_404(tid)
#   - topic.update(updates)
#   - return db.save_topic(topic)
# 【下一步】合上全部，再默写一次，专盯 model_dump(exclude_none=True) 和 status 那行。
