# 第 1 步：遍历文件夹
import pathlib

folder = pathlib.Path("test_files")

for file in folder.rglob("*"):
    if file.is_file():
        print(f"名字：{file.name} | 后缀：{file.suffix} | 父文件夹:{file.parent}")
        