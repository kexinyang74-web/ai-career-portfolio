# 第 4 步完整版 + 试跑开关：归档 + 日志 + 防错 + dry-run
import logging
import pathlib
import sys

DRY_RUN = "--dry-run" in sys.argv          # 命令行带 --dry-run 就是试跑模式

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="file_organize.log",
)

RULES = {".jpg": "图片", ".png": "图片", ".txt": "文档", ".pdf": "文档",
         ".docx": "文档", ".zip": "压缩包", ".mp4": "视频"}

folder = pathlib.Path("test_files")

def organize():
    logging.info(f"开始整理文件：{folder}")
    for file in folder.rglob("*"):
        if not file.is_file():
            continue
        target_dir = RULES.get(file.suffix, "其他")
        dest = folder / target_dir / file.name
        try:
            dest.parent.mkdir(exist_ok=True)
            if DRY_RUN:
                print(f"[试跑] 会把 {file.name} 移动到 {target_dir}/")   # 只演示，不动手
            else:
                file.rename(dest)                                        # 真移动
                logging.info(f"移动文件：{file.name} 到 {target_dir}/")
        except OSError as e:
            logging.error(f"移动文件失败：{file.name} - {e}")

if __name__ == "__main__":
    organize()
    logging.info("整理完成")
    print("整理完成，日志已保存到 file_organize.log")
