# 第 0 步：造测试文件（只运行一次）
import pathlib

folder = pathlib.Path('test_files')
folder.mkdir(exist_ok=True)


# 造 10 个乱七八糟的文件（图片、文档、压缩包、无后缀）
names =["风景照", "学习笔记", "报表", "照片备份", "临时文件",
         "项目文档", "桌面截图", "视频素材", "压缩包", "会议记录"]
suffixes = [".jpg", ".txt", ".pdf", ".png", "", ".docx", ".png", ".mp4", ".zip", ".pdf"]
for i,(name,suffix) in enumerate(zip(names,suffixes)):
    file = folder / f"{name}{suffix}"
    file.write_text(f"这是测试文件{i}, encoding='utf-8'")

print("测试文件已生成", len(list(folder.iterdir())),"个")
