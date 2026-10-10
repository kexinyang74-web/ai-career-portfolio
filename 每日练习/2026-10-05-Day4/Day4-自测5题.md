# Day 4｜FastAPI 修改请求五层链路 · 自测 5 题

日期：2026-10-05

> 不看学习文档作答。答案写在每题下面；不知道可以直接写“不知道”。本文件不提供答案。

## 第 1 题

`@app.patch("/api/topics/{tid}")` 和下面的 `patch_topic()` 分别负责什么？浏览器发来请求后，哪一个决定请求交给这个函数？

你的答案：
1. @app.patch("/api/topics/{tid}")`负责路由装饰器的作用，把请求提交给patch_topic()`函数
2.`patch_topic()` 负责查体，修改字典，保存数据库和返回结果。它是真正执行请求里的工作
3. @app.patch("/api/topics/{tid}")决定请求交给函数
## 第 2 题

`tid: str` 和 `body: TopicPatch` 的数据分别来自哪里？为什么不能把它们当成同一种参数？

你的答案：
1. `tid: str`的数据来自网址中的topic-789，
2. `body: TopicPatch` 的数据来自请求携带的{"favorite":ture}
3. 原因是两者职能不同，一个负责该谁？一个负责该什么。
## 第 3 题

`topic_or_404(tid)` 为什么必须在 `topic.update(updates)` 之前？如果数据库中没有这个选题，程序应该停在哪一层？

你的答案：
1. 是为了避免对None字符修改，并给前端返回明确的404
2.如果数据库没有这个选题，程序会停在topic.update(updates)`这一层
## 第 4 题

`body.model_dump(exclude_none=True)` 在这条修改接口中解决什么问题？如果不排除 `None`，可能错误覆盖哪些已有数据？

你的答案：
1.body.model_dump(exclude_none=True)` 可以让updates只包含真正需要修改的字段，可以排除其他None字段
2. 如果不排除，可能将原有的status、feedback、feedback_note覆盖为None
## 第 5 题

从 `db.save_topic(topic)` 开始，一直讲到浏览器收到结果。至少说明：调用的方法、执行的 SQL 类型、数据库方法的返回值和 FastAPI 的最终响应格式。

你的答案：
调用的方法是save_topic()
SQL类型，UPDATE语句
python字典
JSON响应