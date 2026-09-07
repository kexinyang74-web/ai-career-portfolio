"""Day 51：读取 docs 下的 Markdown，按空行切成块并打印统计。

跳过文件名以下划线开头的文件（如 _template.md）。
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parent / "docs"


def split_by_paragraph(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if p]


def main() -> None:
    files = sorted(
        p for p in DOCS.glob("*.md") if not p.name.startswith("_")
    )
    if not files:
        print(f"没有文档。请在 {DOCS} 放入 01.md … 10.md（不要只用 _template.md）。")
        return

    total_chunks = 0
    for path in files:
        chunks = split_by_paragraph(path.read_text(encoding="utf-8"))
        total_chunks += len(chunks)
        print(f"{path.name}: {len(chunks)} 块")

    print(f"合计 {len(files)} 篇，{total_chunks} 块")


if __name__ == "__main__":
    main()
