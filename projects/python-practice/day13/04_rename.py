# 第 3 步：给分类后的文件加序号重命名
import pathlib

folder = pathlib.Path("test_files")

for sub in folder.iterdir():
    if not sub.is_dir():
        continue
    for i, file in enumerate(sub.iterdir(),start=1):
        new_name = f"{i:02d}_{file.name}{file.suffix}"
        new_path = file.with_name(new_name)
        file.rename(new_path)
        print(f"改名：{file.name} → {new_name}")