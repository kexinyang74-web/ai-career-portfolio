"""Day 65：按评测集逐条 RAG，写出运行记录。引用命中可自动猜；可接受仍要人看。"""

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from main import (  # noqa: E402
    CHAT_KEY,
    EMBED_BASE,
    EMBED_KEY,
    EMBED_MODEL,
    chat,
    retrieve,
    source_name,
)

EVAL_MD = HERE / "eval" / "评测集.md"
OUT_MD = HERE / "eval" / "运行记录.md"

# 跨篇题：命中其中任一文件名即可（见评测表备注）
ANY_OF = {
    24: ["02.md"],
    25: ["01.md", "05.md"],
    26: ["07.md", "08.md"],
}


def parse_table(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        if cells[0] in {"id", "---"} or cells[0].startswith("-"):
            continue
        if not cells[0].isdigit():
            continue
        rows.append(
            {
                "id": int(cells[0]),
                "query": cells[1],
                "expected": cells[2],
            }
        )
    return rows


def citation_guess(expected: str, answer: str, qid: int) -> str:
    files = re.findall(r"\d{2}\.md", answer, flags=re.I)
    files = [f.lower() for f in files]
    if expected == "无":
        return "否" if files else "是"
    need = [x.lower() for x in ANY_OF.get(qid, [expected])]
    return "是" if any(n in answer.lower() for n in need) else "否"


def ask(query: str, k: int) -> tuple[str, str]:
    hits = retrieve(query, k, "")
    if not hits:
        ans = chat("资料不足。问题：" + query)
        return "（无命中）", ans
    names = []
    parts = ["资料（检索得到，请优先依据这些内容，并在回答里写上来源文件名）："]
    for i, (doc, score) in enumerate(hits, start=1):
        name = source_name(doc.metadata)
        names.append(name)
        parts.append(f"\n[{i}] 来源 {name}  score {score:.4f}\n{doc.page_content}")
    parts.append(f"\n问题：{query}")
    ans = chat("\n".join(parts))
    return "、".join(dict.fromkeys(names)), ans


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=10, help="先跑前 N 条，默认 10")
    p.add_argument("--all", action="store_true", help="跑满表里所有问句")
    p.add_argument("-k", type=int, default=3)
    args = p.parse_args()

    if not CHAT_KEY or not EMBED_KEY or not EMBED_BASE or not EMBED_MODEL:
        print("缺少密钥或 Embedding 配置。")
        sys.exit(1)

    rows = parse_table(EVAL_MD.read_text(encoding="utf-8"))
    if not args.all:
        rows = rows[: args.limit]

    lines = [
        "# 评测运行记录",
        "",
        f"> 跑了 {len(rows)} 条，k={args.k}。引用命中是脚本按文件名猜的；**可接受请你看完回答后自己勾。**",
        "",
    ]
    hit = 0
    for i, row in enumerate(rows, start=1):
        print(f"== {i}/{len(rows)} id={row['id']} 预期 {row['expected']} ==")
        print(row["query"][:60])
        retrieved, answer = ask(row["query"], args.k)
        guess = citation_guess(row["expected"], answer, row["id"])
        if guess == "是":
            hit += 1
        print("检索:", retrieved)
        print("引用命中(自动):", guess)
        print(answer[:400])
        print()
        lines.append(f"## id {row['id']}  预期 {row['expected']}  引用命中(自动) {guess}")
        lines.append("")
        lines.append(f"- 问句：{row['query']}")
        lines.append(f"- 检索来源：{retrieved}")
        lines.append("")
        lines.append(answer)
        lines.append("")
        if i < len(rows):
            time.sleep(0.8)

    rate = hit / len(rows) if rows else 0
    lines.append("## 自动汇总（仅引用命中）")
    lines.append("")
    lines.append(f"- 条数：{len(rows)}")
    lines.append(f"- 引用命中(自动)：{hit}/{len(rows)} = {rate:.0%}")
    lines.append("- 可接受率：请打开本文件逐条勾到 `评测集.md`")
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"已写入 {OUT_MD}")
    print(f"引用命中(自动) {hit}/{len(rows)}")


if __name__ == "__main__":
    main()
