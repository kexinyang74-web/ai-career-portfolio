"""loader 测试:读 CSV 用现成的脏文件;读 Excel 用临时造的小文件

tmp_path 是 pytest 自带的"临时目录"——每次测试自动创建、测完自动清理,
不用往项目里丢垃圾文件。
"""
import openpyxl

from loader import 读csv, 读xlsx


def test_读csv_行数和内容():
    rows = 读csv("销售数据_脏.csv")
    assert len(rows) == 14            # 空行被 DictReader 自动跳过
    assert rows[0]["负责人"] == "张伟"
    assert rows[4]["日期"] == ""      # 第 5 行日期是空缺的


def test_读xlsx_临时造文件(tmp_path):
    # 现场造一个小 Excel:表头 + 1 行数据 + 1 行全空
    p = tmp_path / "小数据.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["日期", "区域", "金额"])
    ws.append(["2024/1/5", "华东", "100"])
    ws.append([None, None, None])
    wb.save(p)

    rows = 读xlsx(str(p))
    assert len(rows) == 1             # 空行被跳过
    assert rows[0]["区域"] == "华东"
    assert rows[0]["日期"] == "2024/1/5"
