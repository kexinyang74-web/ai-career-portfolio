# 03_batch_rename.ps1
# 批量改名脚本：给当前目录下所有 .txt 文件加上两位序号前缀
#
# 用法（在"素材目录"里运行，脚本会处理当前目录）：
#   .\day23\03_batch_rename.ps1            # 只预览，不改（安全模式）
#   .\day23\03_batch_rename.ps1 -真干      # 真正改名

param(
    [switch]$真干  # 带 -真干 参数 = 真正执行；不带 = 只打印预览
)

$序号 = 1
Get-ChildItem -Filter "*.txt" | ForEach-Object {
    # "{0:D2}" 是格式化：D2 = 两位数字（1 → 01）
    $新名 = "{0:D2}-{1}" -f $序号, $_.Name
    if ($真干) {
        Rename-Item $_.FullName $新名
        Write-Host "✅ 改名: $($_.Name) → $新名"
    } else {
        Write-Host "🔍 预览: $($_.Name) → $新名"
    }
    $序号++
}
Write-Host "（预览模式不会真的改，加 -真干 才执行）"

