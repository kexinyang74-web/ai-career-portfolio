# Day 23 终端与 shell 基础（PowerShell）

> 第 4 周第 2 天。核心：命令全家桶 + 管道/重定向 + 批量脚本。配套练习：projects/python-practice/day23/（03_batch_rename.ps1）。

## 一、为什么学终端

- GUI 一次点一个，终端一次管一批（1000 个文件改名 = 一条命令）
- 命令可以存成脚本自动跑（shell 脚本 = 把命令写进文件）
- 教程/文档/AI 对话里的操作全是命令

**心智模型：命令 = 动词 + 宾语**。`Copy-Item report1.txt backup.txt` = 复制 report1.txt 到 backup.txt。

## 二、命令全家桶（Windows PowerShell）

| 操作 | 命令 | 别名 | 说明 |
|---|---|---|---|
| 我在哪 | `Get-Location` | pwd | 打印当前目录 |
| 换目录 | `Set-Location` | cd | 相对/绝对路径都行 |
| 列出 | `Get-ChildItem` | ls / dir | 目录和文件都列 |
| 复制 | `Copy-Item` | cp | 留原件 |
| 移动 | `Move-Item` | mv | 搬走不留 |
| 改名 | `Rename-Item` | ren | 换名字 |
| 新建 | `New-Item -ItemType Directory` | mkdir | 目录/文件都能建（一次多个） |
| 写内容 | `Set-Content` | - | 写文件（覆盖） |
| 读内容 | `Get-Content` | cat / type | 读文件 |

**三兄弟对比**：Copy 留原件 / Move 不留 / Rename 换名牌。路径末尾 `\` 表示"这是个文件夹"。

## 三、管道 | 与重定向 > / >>

| 符号 | 名字 | 作用 | 例子 |
|---|---|---|---|
| `\|` | 管道 | 前一个命令的输出 → 后一个命令的输入 | `Get-ChildItem \| Where-Object { $_.Name -like "*.txt" }` |
| `>` | 重定向 | 输出写进文件（**覆盖**） | `pip freeze > requirements.txt` |
| `>>` | 重定向 | 输出写进文件（**追加**） | `"一行" >> 文件.txt` |

过滤常用：
- `Where-Object { $_.Name -like "*.txt" }`——`$_` = 当前项，`-like` 模糊匹配，`*` 通配符
- `Where-Object { $_.Length -gt 0 }`——大于 0 字节（非空）
- `Sort-Object Length`——按大小排序
- 可三连：`Get-ChildItem | Where-Object … | Sort-Object …`

**小坑**：命令生成的输出文件名，会被同类过滤条件命中（生成 `文件清单.txt` 后，过滤 `*.txt` 会把自己算进去）。正式脚本里输出文件别起会被自己处理的扩展名。

## 四、批量脚本 .ps1（今日产出物）

```powershell
param([switch]$真干)          # 参数开关：加 -真干 才真执行（默认预览）
$序号 = 1
Get-ChildItem -Filter "*.txt" | ForEach-Object {
    $新名 = "{0:D2}-{1}" -f $序号, $_.Name   # D2 = 两位编号：1 → 01
    if ($真干) { Rename-Item $_.FullName $新名 } else { Write-Host "预览: $新名" }
    $序号++
}
```

**与 Python 对照**（脚本语言都是相通的）：

| PowerShell | Python 对应 |
|---|---|
| `param([switch]$真干)` | 函数默认参数（开关） |
| `Get-ChildItem -Filter` | `glob.glob()` |
| `ForEach-Object { }` | for 循环 |
| `$_` | 循环变量 |
| `"{0:D2}" -f $序号` | `f"{序号:02d}"` |
| `Write-Host` | `print` |
| `if ($真干) { } else { }` | if/else |

**核心设计：dry-run 安全开关**。批量操作 = 高风险操作（错一个条件错 1000 次），永远先"演习模式"给人眼看，确认后才 `-真干`。以后写任何批量脚本都带这个开关。

## 五、编码坑（今天实测，重要）

**现象**：运行含中文的 .ps1 报错，`真干` 变成乱码 `鐪熷共`。

**原因**：PowerShell 5.1 读脚本**默认按系统 ANSI（GBK）解码**，不认裸 UTF-8 → 字节错位乱码。

**修复**：把文件转成**带 BOM 的 UTF-8**：

```powershell
$内容 = Get-Content -Raw -Encoding UTF8 脚本.ps1
Set-Content -Path 脚本.ps1 -Value $内容 -Encoding UTF8   # 5.1 的 -Encoding UTF8 = 带 BOM
```

**记忆钩子**：和 Day 20 CSV 的 `encoding="utf-8-sig"` 是同一个问题——**微软生态不认裸 UTF-8**，要 BOM 标记（文件开头特殊字节告诉解码器"我是 UTF-8"）。PowerShell 7 才原生支持无 BOM。脚本乱码 → 第一反应查编码。

## 六、速查卡

```powershell
Get-Location                      # 我在哪
cd 路径                           # 换目录
Get-ChildItem                     # 列出
Copy-Item 源 目标                 # 复制
Move-Item 源 目标                 # 移动
Rename-Item 旧 新                 # 改名
New-Item -ItemType Directory 名   # 建目录
Get-Content 文件                  # 读文件
Set-Content 文件 "内容"           # 写文件（覆盖）
命令 | Where-Object { 条件 }      # 过滤
命令 > 文件                       # 输出覆盖写进文件
命令 >> 文件                      # 输出追加写进文件
.\脚本.ps1 -真干                  # 运行脚本（带参数）
```
