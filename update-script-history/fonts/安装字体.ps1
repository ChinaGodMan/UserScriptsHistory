# 确保以管理员身份运行此脚本

# 定义字体文件路径
$fontValue = "HYWenHei.ttf"
$fontName = "HY Wen Hei"
$fontFilePath = "C:\GitHub\UserScriptsHistory\update-script-history\fonts\$fontValue"
$fontDestinationPath = "$env:SystemRoot\Fonts\$fontValue"

# 复制字体文件到系统字体目录
Copy-Item -Path $fontFilePath -Destination $fontDestinationPath

# 注册字体到系统注册表
$fontsRegistryPath = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
New-ItemProperty -Path $fontsRegistryPath -Name $fontName -Value $fontValue -PropertyType String

# 刷新字体缓存
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class FontCache {
    [DllImport("gdi32.dll")]
    public static extern int AddFontResource(string lpFileName);
    [DllImport("gdi32.dll")]
    public static extern int RemoveFontResource(string lpFileName);
}
"@
[FontCache]::AddFontResource($fontDestinationPath)
