# 第 2 步：按后缀分类归档
import pathlib

folder = pathlib.Path("test_files")
# 分类规则：后缀 → 目标文件夹名（这就是"规则"，你想怎么定就怎么定）
RULES = {
    ".jpg": "图片",
    ".png": "图片",
    ".txt": "文档",
    ".pdf": "文档",
    ".docx": "文档",
    ".zip": "压缩包",
    ".mp4": "视频",
}

for file in folder.rglob("*"):
    if not file.is_file():
        continue
    
    target_dir = RULES.get(file.suffix, "其他")
    dest = folder / target_dir / file.name
    dest.parent.mkdir(exist_ok=True)

    file.rename(dest)
    print(f"移动文件：{file.name} 到 {target_dir}")