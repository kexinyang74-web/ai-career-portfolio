# Day 66 调优 k（第 10 周第 3 天）

> 一次只拧 **k**。不重切、不重 embed、不改 prompt。基线是 k=3、第 24 条漏了 `02.md`。

## 今天目的

看把 k 从 3 加到 5 之后，第 24 条检索里**会不会出现 `02.md`**。其它 29 条今天不必全跑（全量对比留给 Day 67）。

加大 k 的代价你已经知道：更容易把 `03.md` 这类噪音塞进 `user`。今天要看的是：漏召回有没有换回来，噪音有没有变多。

## 你做

```powershell
cd C:\Users\Administrator\Desktop\学习安排\projects\project-2-rag
$env:HTTPS_PROXY = "http://127.0.0.1:7897"
python eval_run.py --ids 24 -k 5 --out eval/运行记录-k5-q24.md
```

对照 `eval/运行记录.md` 里第 24 条（k=3 时检索是 `10.md、05.md、01.md`）。把 k=5 的检索名单记进日志或评测表备注。

可选：再跑 1、28 当对照，看加大 k 有没有把本来对的题弄吵。

```powershell
python eval_run.py --ids 1,24,28 -k 5 --out eval/运行记录-k5-抽样.md
```

不要覆盖 `eval/运行记录.md`。

## 明确不做

- 不改切分、不改 Embedding、不改 system 文案
- 不把项目二默认 k 改掉，除非你看完 k=5 明确要改 `main.py`

## 做完

答 [[Day66-自测5题]]。说「收尾」再批。
