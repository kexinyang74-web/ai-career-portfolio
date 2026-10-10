# 素材数据清洗与汇总
"""可以将不干净的数据进行简单清洗，并统计清洗前后的数据量"""

import json
from pathlib import Path


def load_materials(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def clean_materials(materials: list[str]) -> list[str]:
    cleaned_materials: list[str] = []

    for material in materials:
        cleaned = material.strip()  # 去除材料两端的空白字符

        if (
            cleaned != "" and cleaned not in cleaned_materials
        ):  # 如果材料不为空且不在清洗后的材料列表中
            cleaned_materials.append(cleaned)  # 将清洗后的材料添加到列表中

    return cleaned_materials  # 返回清洗后的材料列表


def summarize_materials(materials: list[str]) -> dict[str, int]:
    cleaned_materials = clean_materials(materials)
    original_count = len(materials)
    cleaned_count = len(cleaned_materials)
    removed_count = original_count - cleaned_count
    return {
        "original_count": original_count,
        "cleaned_count": cleaned_count,
        "removed_count": removed_count,
    }


day3_folder = Path(__file__).resolve().parent
materials_file = day3_folder / "materials.json"


try:
    test_materials = load_materials(materials_file)
except FileNotFoundError:
    print(f"文件 {materials_file} 不存在")
except json.JSONDecodeError:
    print(f"文件 {materials_file} 格式损坏")
else:
    cleaned_result = clean_materials(test_materials)
    print(cleaned_result)
    summary_result = summarize_materials(test_materials)
    print(summary_result)
