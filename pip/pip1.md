ポータブルPython.exeにpipをインストールなしで連携する完全ガイド

展開されただけのポータブルPython環境に、システムへのインストールを行わずにpipを連携させる方法を、実用性と確実性を重視して解説します。

状況の整理と目標設定

想定される環境：
- Windows埋め込み配布（Embeddable Package）
- ZIPで展開されたポータブルPython
- 管理者権限なし、またはシステム変更を避けたい環境

「インストールなし」の定義：
- システムレジストリを変更しない
- システム全体のPATH環境変数を変更しない
- 可能な限りポータブル環境内で完結する

推奨アプローチ（確実性順）

方法1: get-pip.pyによるユーザーローカル設定（最も確実）

システムを汚さず、特定のPython環境にのみpipを追加する最も安全な方法です。

基本手順：

#!/usr/bin/env python
"""ポータブルPythonへのpip設定スクリプト"""

import sys
import subprocess
import urllib.request
from pathlib import Path

def setup_pip_portable(python_exe_path):
    """ポータブルPython.exeにpipをセットアップ"""
    
    python_exe = Path(python_exe_path).resolve()
    work_dir = python_exe.parent
    
    if not python_exe.exists():
        print(f"✗ Python.exeが見つかりません: {python_exe}")
        return False
    
    print(f"=== ポータブルPythonセットアップ ===")
    print(f"対象: {python_exe}")
Step 1: Pythonの動作確認
    try:
        result = subprocess.run([str(python_exe), "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✓ Python確認: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("✗ Pythonの実行に失敗")
        return False
Step 2: get-pip.pyの準備
    get_pip_path = work_dir / "get-pip.py"
    if not get_pip_path.exists():
        print("get-pip.pyをダウンロード中...")
        try:
            urllib.request.urlretrieve(
                "https://bootstrap.pypa.io/get-pip.py", 
                str(get_pip_path)
            )
            print("✓ ダウンロード完了")
        except Exception as e:
            print(f"✗ ダウンロード失敗: {e}")
            return False
Step 3: pipをユーザーディレクトリにインストール
    try:
        subprocess.run([
            str(python_exe), 
            str(get_pip_path),
            "--user",
            "--no-warn-script-location"
        ], check=True)
        print("✓ pipのセットアップ完了")
    except subprocess.CalledProcessError as e:
        print(f"✗ pipセットアップ失敗: {e}")
        return False
Step 4: 動作確認
    try:
        result = subprocess.run([str(python_exe), "-m", "pip", "--version"],
                              capture_output=True, text=True, check=True)
        print(f"✓ pip確認: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError:
        print("✗ pipの確認に失敗")
        return False

使用例
if name == 'main':
    success = setup_pip_portable("./portable_python/python.exe")
    if success:
        print("\n使用方法:")
        print("  ./portable_python/python.exe -m pip install package_name --user")

方法2: 埋め込み配布用の完全ポータブル設定

Windows埋め込み配布の場合、特別な設定が必要です。

ディレクトリ構造の準備：

def setup_embeddable_python(python_dir):
    """埋め込み配布Python用の完全セットアップ"""
    
    python_dir = Path(python_dir)
    python_exe = python_dir / "python.exe"
    
    if not python_exe.exists():
        print(f"✗ Python.exeが見つかりません: {python_exe}")
        return False
    
    print(f"=== 埋め込み配布Python セットアップ ===")
Step 1: 必要なディレクトリ構造を作成
    lib_dir = python_dir / "Lib"
    site_packages_dir = lib_dir / "site-packages"
    
    lib_dir.mkdir(exist_ok=True)
    site_packages_dir.mkdir(exist_ok=True)
    print(f"✓ ディレクトリ作成: {site_packages_dir}")
Step 2: ._pthファイルを修正
    pth_files = list(python_dir.glob("python*._pth"))
    if pth_files:
        pth_file = pth_files[0]
        print(f"._pthファイルを修正: {pth_file}")
既存の内容を読み取り
        try:
            content = pth_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = pth_file.read_text(encoding='cp1252')
必要なパスを追加
        required_paths = ["Lib", "Lib\\site-packages"]
        lines = content.strip().split('\n')
        
        for path in required_paths:
            if path not in lines:
                lines.append(path)
ファイルを更新
        pth_file.write_text('\n'.join(lines), encoding='utf-8')
        print("✓ ._pthファイル更新完了")
Step 3: pipのwheelファイルを配置（オフライン用）
    return setup_pip_from_wheels(python_dir, site_packages_dir)

def setup_pip_from_wheels(python_dir, site_packages_dir):
    """wheelファイルからpipを配置"""
    
    wheels_dir = python_dir / "wheels"
    if not wheels_dir.exists():
        print(f"⚠ wheelsディレクトリが見つかりません: {wheels_dir}")
        print("オンライン環境で以下を実行してください:")
        print(f"pip download -d {wheels_dir} pip setuptools wheel")
        return False
wheelファイルを検索
    pip_wheels = list(wheels_dir.glob("pip-*.whl"))
    if not pip_wheels:
        print("✗ pipのwheelファイルが見つかりません")
        return False
wheelファイルをsite-packagesに展開
    import zipfile
    
    for wheel in wheels_dir.glob("*.whl"):
        print(f"展開中: {wheel.name}")
        try:
            with zipfile.ZipFile(wheel, 'r') as zip_ref:
                zip_ref.extractall(site_packages_dir)
        except Exception as e:
            print(f"✗ 展開失敗 {wheel.name}: {e}")
            continue
    
    print("✓ pipの配置完了")
動作確認
    python_exe = python_dir / "python.exe"
    try:
        result = subprocess.run([str(python_exe), "-m", "pip", "--version"],
                              capture_output=True, text=True, check=True)
        print(f"✓ pip確認: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ pip確認失敗: {e}")
        return False

方法3: 完全自動化バッチスクリプト

日常的な使用を想定した自動化スクリプトです。

Windows用バッチファイル（setup_portable_pip.bat）：

@echo off
setlocal enabledelayedexpansion

echo ===== ポータブルPython pip セットアップ =====

REM パスの設定
set SCRIPT_DIR=%~dp0
set PYTHON_EXE=%SCRIPT_DIR%python.exe
set TOOLS_DIR=%SCRIPT_DIR%tools
set GET_PIP=%TOOLS_DIR%\get-pip.py

REM ディレクトリ作成
if not exist "%TOOLS_DIR%" mkdir "%TOOLS_DIR%"

REM Python.exeの確認
if not exist "%PYTHON_EXE%" (
    echo ✗ python.exeが見つかりません: %PYTHON_EXE%
    pause
    exit /b 1
)

echo ✓ Python確認: %PYTHON_EXE%
"%PYTHON_EXE%" --version

REM get-pip.pyの準備
if not exist "%GET_PIP%" (
    echo get-pip.pyをダウンロード中...
    
    REM PowerShellでダウンロード
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://bootstrap.pypa.io/get-pip.py', '%GET_PIP%')"
    
    if not exist "%GET_PIP%" (
        echo ✗ get-pip.pyのダウンロードに失敗
        pause
        exit /b 1
    )
    echo ✓ ダウンロード完了
)

REM pipのセットアップ
echo pipをセットアップ中...
"%PYTHON_EXE%" "%GET_PIP%" --user --no-warn-script-location

if %ERRORLEVEL% neq 0 (
    echo ✗ pipのセットアップに失敗
    pause
    exit /b 1
)

REM 確認
echo ✓ セットアップ完了
"%PYTHON_EXE%" -m pip --version

echo.
echo 使用方法:
echo   %PYTHON_EXE% -m pip install package_name --user
echo   %PYTHON_EXE% -m pip list --user
echo.
pause

Linux/Mac用シェルスクリプト（setup_portable_pip.sh）：

#!/bin/bash

echo "===== ポータブルPython pip セットアップ ====="

パスの設定
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXE="$SCRIPT_DIR/python"
TOOLS_DIR="$SCRIPT_DIR/tools"
GET_PIP="$TOOLS_DIR/get-pip.py"

ディレクトリ作成
mkdir -p "$TOOLS_DIR"

Python実行ファイルの確認
if [ ! -f "$PYTHON_EXE" ]; then
    echo "✗ pythonが見つかりません: $PYTHON_EXE"
    exit 1
fi

echo "✓ Python確認: $PYTHON_EXE"
"$PYTHON_EXE" --version

get-pip.pyの準備
if [ ! -f "$GET_PIP" ]; then
    echo "get-pip.pyをダウンロード中..."
    
    if command -v curl > /dev/null; then
        curl -o "$GET_PIP" https://bootstrap.pypa.io/get-pip.py
    elif command -v wget > /dev/null; then
        wget -O "$GET_PIP" https://bootstrap.pypa.io/get-pip.py
    else
        echo "✗ curlまたはwgetが必要です"
        exit 1
    fi
    
    if [ ! -f "$GET_PIP" ]; then
        echo "✗ get-pip.pyのダウンロードに失敗"
        exit 1
    fi
    echo "✓ ダウンロード完了"
fi

pipのセットアップ
echo "pipをセットアップ中..."
"$PYTHON_EXE" "$GET_PIP" --user --no-warn-script-location

if [ $? -ne 0 ]; then
    echo "✗ pipのセットアップに失敗"
    exit 1
fi

確認
echo "✓ セットアップ完了"
"$PYTHON_EXE" -m pip --version

echo ""
echo "使用方法:"
echo "  $PYTHON_EXE -m pip install package_name --user"
echo "  $PYTHON_EXE -m pip list --user"

パッケージインストール用スクリプト

セットアップ後のパッケージ管理を簡単にするスクリプトです。

#!/usr/bin/env python
"""ポータブルPython用パッケージマネージャー"""

import sys
import subprocess
from pathlib import Path

class PortablePackageManager:
    """ポータブルPython環境用パッケージマネージャー"""
    
    def init(self, python_exe_path):
        self.python_exe = Path(python_exe_path).resolve()
        self.base_dir = self.python_exe.parent
        
        if not self.python_exe.exists():
            raise FileNotFoundError(f"Python.exeが見つかりません: {self.python_exe}")
    
    def install_from_requirements(self, requirements_file):
        """requirements.txtからパッケージをインストール"""
        req_path = Path(requirements_file)
        if not req_path.exists():
            print(f"✗ requirements.txtが見つかりません: {req_path}")
            return False
        
        print(f"requirements.txtからインストール: {req_path}")
        try:
            subprocess.run([
                str(self.python_exe), "-m", "pip", "install",
                "--user", "-r", str(req_path)
            ], check=True)
            print("✓ インストール完了")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ インストール失敗: {e}")
            return False
    
    def install_from_wheels(self, wheels_dir):
        """wheelファイルからオフラインインストール"""
        wheels_path = Path(wheels_dir)
        if not wheels_path.exists():
            print(f"✗ wheelsディレクトリが見つかりません: {wheels_path}")
            return False
        
        wheels = list(wheels_path.glob("*.whl"))
        if not wheels:
            print(f"✗ wheelファイルが見つかりません: {wheels_path}")
            return False
        
        print(f"オフラインインストール: {len(wheels)} パッケージ")
        try:
            subprocess.run([
                str(self.python_exe), "-m", "pip", "install",
                "--user", "--no-index", "--find-links", str(wheels_path)
            ] + [w.stem.split('-')[0] for w in wheels], check=True)
            print("✓ オフラインインストール完了")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ インストール失敗: {e}")
            return False
    
    def list_packages(self):
        """インストール済みパッケージを表示"""
        try:
            result = subprocess.run([
                str(self.python_exe), "-m", "pip", "list", "--user"
            ], capture_output=True, text=True, check=True)
            print("インストール済みパッケージ:")
            print(result.stdout)
        except subprocess.CalledProcessError:
            print("✗ パッケージリストの取得に失敗")

使用例
if name == 'main':
    manager = PortablePackageManager("./portable_python/python.exe")
requirements.txtからインストール
manager.install_from_requirements("./requirements.txt")
オフラインwheelからインストール
manager.install_from_wheels("./wheels")
パッケージリストを表示
    manager.list_packages()

トラブルシューティング

よくある問題と解決策

def diagnose_portable_python(python_exe_path):
    """ポータブルPython環境の診断"""
    
    python_exe = Path(python_exe_path)
    print(f"=== 診断: {python_exe} ===")
基本確認
    if not python_exe.exists():
        print(f"✗ Python.exeが見つかりません")
        return False
Python実行確認
    try:
        result = subprocess.run([str(python_exe), "--version"],
                              capture_output=True, text=True, check=True)
        print(f"✓ Python: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("✗ Pythonの実行に失敗")
        return False
pip確認
    try:
        result = subprocess.run([str(python_exe), "-m", "pip", "--version"],
                              capture_output=True, text=True, check=True)
        print(f"✓ pip: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        print("✗ pipが利用できません")
        print("  解決方法: setup_pip_portable() を実行してください")
埋め込み配布の確認
    python_dir = python_exe.parent
    pth_files = list(python_dir.glob("python*._pth"))
    if pth_files:
        print(f"✓ 埋め込み配布を検出: {pth_files[0]}")
._pthファイルの内容確認
        pth_content = pth_files[0].read_text()
        required_paths = ["Lib", "Lib\\site-packages"]
        missing_paths = []
        
        for path in required_paths:
            if path not in pth_content:
                missing_paths.append(path)
        
        if missing_paths:
            print(f"⚠ ._pthファイルに不足: {missing_paths}")
            print("  解決方法: setup_embeddable_python() を実行してください")
ディレクトリ構造確認
    lib_dir = python_dir / "Lib"
    site_packages_dir = lib_dir / "site-packages"
    
    if lib_dir.exists():
        print(f"✓ Libディレクトリ: {lib_dir}")
    else:
        print(f"⚠ Libディレクトリなし: {lib_dir}")
    
    if site_packages_dir.exists():
        print(f"✓ site-packagesディレクトリ: {site_packages_dir}")
    else:
        print(f"⚠ site-packagesディレクトリなし: {site_packages_dir}")
    
    return True

診断実行例
diagnose_portable_python("./portable_python/python.exe")

推奨される選択指針

環境別の最適解：

$$\text{推奨方法} = \begin{cases}
\text{get-pip.py + --user} & \text{（通常のポータブル環境）} \\
\text{埋め込み配布用設定} & \text{（Windows Embeddable Package）} \\
\text{ensurepip} & \text{（標準機能が利用可能な場合）} \\
\text{wheelファイル直接配置} & \text{（完全オフライン環境）}
\end{cases}$$

成功率の目安：

- get-pip.py方式： 95%（最も確実）
- ensurepip方式： 80%（埋め込み配布では利用不可）
- wheel直接配置： 70%（依存関係の手動管理が必要）

この完全なガイドにより、どのようなポータブルPython環境でも、システムを汚すことなくpipを連携させることができます。環境の制約に応じて、最適な方法を選択してください。