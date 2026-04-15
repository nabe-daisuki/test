# ==================================================
# WebCapture.ps1
# Webサイトのスクリーンショット自動取得スクリプト
#
# 使用方法:
#   powershell.exe -File "WebCapture.ps1" -url "https://example.com" -outputPath "C:\temp\shot.png"
#
# 引数:
#   -url        : 対象URL（必須）
#   -outputPath : 画像保存先フルパス（必須）
#   -waitSec    : ページ読み込み待機秒数（デフォルト: 5）
#   -browser    : 使用ブラウザ "edge" or "chrome"（デフォルト: "edge"）
#   -width      : ブラウザウィンドウ幅（デフォルト: 1280）
#   -height     : ブラウザウィンドウ高さ（デフォルト: 800）
# ==================================================

param(
    [Parameter(Mandatory=$true)]
    [string]$url,
    
    [Parameter(Mandatory=$true)]
    [string]$outputPath,
    
    [int]$waitSec = 5,
    [string]$browser = "edge",
    [int]$width = 1280,
    [int]$height = 800
)

# 必要なアセンブリを読み込み
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ログ出力用関数
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message"
}

try {
    Write-Log "スクリーンショット取得開始: $url"
    
    # ブラウザ実行ファイル決定
    if ($browser.ToLower() -eq "chrome") {
        $browserExe = "chrome.exe"
        $processName = "chrome"
    } else {
        $browserExe = "msedge.exe"
        $processName = "msedge"
    }
    
    # 出力フォルダが存在しない場合は作成
    $outputDir = Split-Path $outputPath -Parent
    if (-not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        Write-Log "出力フォルダを作成: $outputDir"
    }
    
    # ブラウザ起動（安全なプロセス管理）
    Write-Log "ブラウザ起動中..."
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $browserExe
    $startInfo.Arguments = "--new-window --window-size=$width,$height --disable-extensions --disable-notifications --no-first-run `"$url`""
    $startInfo.UseShellExecute = $true
    
    $process = [System.Diagnostics.Process]::Start($startInfo)
    
    if ($process -eq $null) {
        throw "ブラウザの起動に失敗しました: $browserExe"
    }
    
    Write-Log "プロセスID $($process.Id) でブラウザを起動"
    
    # ページ読み込み待機
    Write-Log "${waitSec}秒間待機中..."
    Start-Sleep -Seconds $waitSec
    
    # スクリーンショット取得
    Write-Log "スクリーンショット取得中..."
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    
    $graphics.CopyFromScreen(
        [System.Drawing.Point]::Empty,
        [System.Drawing.Point]::Empty,
        $screen.Size
    )
    
    # PNG形式で保存
    $bitmap.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Log "画像保存完了: $outputPath"
    
    # リソース解放
    $graphics.Dispose()
    $bitmap.Dispose()
    
    # 起動したブラウザプロセスのみを安全に終了
    try {
        if ($process -and -not $process.HasExited) {
            Write-Log "ブラウザプロセス終了中..."
            $process.Kill()
            $process.WaitForExit(3000)  # 3秒でタイムアウト
        }
    } catch {
        Write-Log "警告: ブラウザプロセスの終了に失敗 (影響なし)"
    }
    
    Write-Log "処理完了"
    exit 0
    
} catch {
    Write-Log "エラー: $($_.Exception.Message)"
    
    # エラー時もプロセス終了を試行
    try {
        if ($process -and -not $process.HasExited) {
            $process.Kill()
        }
    } catch {
        # 無視
    }
    
    exit 1
}
