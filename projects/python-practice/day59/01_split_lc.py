"""Day 59：LangChain Loader / TextSplitter，对照 day51/01_split.py。

不调 Embedding、不写 Chroma、不调 Chat。
"""

from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent / "day51" / "docs"


def split_by_paragraph(text: str) -> list[str]:
    parts = [p.strip() for p in text.split("\n\n")]
    return [p for p in parts if p]


def load_docs():
    loader = DirectoryLoader(
        str(DOCS),
        glob="*.md",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
        show_progress=False,
    )
    raw = loader.load()
    docs = [
        d
        for d in raw
        if not Path(d.metadata.get("source", "")).name.startswith("_")
    ]
    return docs


def main() -> None:
    files = sorted(p for p in DOCS.glob("*.md") if not p.name.startswith("_"))
    hand_chunks = []
    for path in files:
        hand_chunks.extend(split_by_paragraph(path.read_text(encoding="utf-8")))

    docs = load_docs()
    print("== 对照：Loader vs 手写读文件 ==")
    print(f"手写 glob：{len(files)} 篇")
    print(f"DirectoryLoader + TextLoader（跳过 _ 开头）：{len(docs)} 个 Document")
    if docs:
        src = Path(docs[0].metadata.get("source", "")).name
        print(f"第一个 Document.metadata 里有 source → {src}")
        print(f"metadata 键：{sorted(docs[0].metadata.keys())}")
    print()

    para = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=2000,
        chunk_overlap=0,
    ).split_documents(docs)

    fixed = RecursiveCharacterTextSplitter(
        chunk_size=80,
        chunk_overlap=20,
    ).split_documents(docs)

    print("== 对照：Splitter vs 手写按空行 ==")
    print(f"手写按空行：{len(hand_chunks)} 块")
    print(f"CharacterTextSplitter(separator=\\\\n\\\\n, chunk_size=2000)：{len(para)} 块")
    print(f"RecursiveCharacterTextSplitter(chunk_size=80, overlap=20)：{len(fixed)} 块")
    print()

    if fixed:
        sample = fixed[0].page_content.replace("\n", " ")
        print("定长切出来的第 1 块预览（可能从句子中间断）：")
        print(f"  [{Path(fixed[0].metadata.get('source', '')).name}] {sample}")
    print()
    print("四词对照（后两个明天）：")
    print("  Loader        ↔  Path.read_text / glob")
    print("  TextSplitter  ↔  split_by_paragraph / 定长切")
    print("  VectorStore   ↔  embeddings.json + Chroma query（Day 52–58）")
    print("  RetrievalQA   ↔  01_rag_chat.py（检索片段塞进 user 再 Chat）")
    print("语义切分今天不写代码：按句向量再合并，要调 Embedding。")


if __name__ == "__main__":
    main()
