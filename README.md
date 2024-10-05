# 実行ファイル作成手順と使用方法

このリポジトリには、`ui.py` および `drive_main.py` の2つのPythonスクリプトをEXE形式に変換するための手順を記載しています。Windows環境でのみEXEファイルを作成することが可能です。`PyInstaller` を使用して実行ファイルを作成します。

## 必要なツール
- **Windows OS**（EXEファイル作成はWindowsでのみサポートされています）
- Python 3.x
- `PyInstaller` ライブラリ
- 依存関係のインストール（`requirements.txt` を使用）

### 依存関係のインストール
リポジトリ内にある `requirements.txt` を使用して、必要なパッケージをインストールしてください。

```bash
pip install -r requirements.txt
```

これで、`altgraph`, `selenium`, `PyInstaller` などの必要なパッケージがインストールされます。

## 実行ファイルの作成方法

### 1. `.spec` ファイルの準備
それぞれのスクリプトに対して、`spec` ファイルを編集して、依存関係を追加します。`hiddenimports` に必要なモジュールを追加することで、PyInstaller が依存関係を正しく認識できるようにします。

#### 1.1 `drive_main.spec` の編集
`drive_main.py` に関連する `spec` ファイルを編集します。`hiddenimports` に依存するモジュールを指定します。

```
# drive_main.spec

# PyInstallerの設定
hiddenimports = ['src.database.db']

# 他のオプションも含む spec ファイルの内容
```

#### 1.2 `ui.spec` の編集
同様に、ui.py に関連する spec ファイルも編集します。

```
# ui.spec

# PyInstallerの設定
hiddenimports = ['src.database.db', 'tkcalendar','babel.numbers', 'babel.dates']

# 他のオプションも含む spec ファイルの内容
```
### 2. 実行ファイルの作成
各 `.spec` ファイルを使って、EXE ファイルを生成します。以下のコマンドを使って、PyInstaller が `.spec` ファイルを基に EXE を作成します。

#### 2.1 drive_main.py の実行ファイルを作成
```
pyinstaller drive_main.spec
```
このコマンドにより、drive_main.py の実行ファイルが dist/drive_main/ フォルダに生成されます。

#### 2.2 ui.py の実行ファイルを作成
```
pyinstaller ui.spec
```
このコマンドにより、`ui.py` の実行ファイルが `dist/ui/` フォルダに生成されます。

### 3. 実行ファイルの確認
生成された EXE ファイルは、それぞれ以下のパスに配置されています。

- `dist/drive_main/drive_main.exe`
- `dist/ui/ui.exe`

### 4. EXE ファイルの実行方法
生成された EXE ファイルは、Windows 環境でダブルクリックすることで実行可能です。コマンドラインから実行する場合は、以下のコマンドを使います。

```bash
./dist/drive_main/drive_main.exe
./dist/ui/ui.exe

```
./dist/drive_main/drive_main.exe
./dist/ui/ui.exe

```
### 注意点
- EXEファイルの作成はWindowsでのみサポートされています。 他のOS（Linux, macOSなど）では、この方法でEXEファイルを作成することはできません。
- `hiddenimports` の部分に必要なモジュールをすべて追加しないと、実行ファイル作成時にエラーが発生する可能性があります。
- EXE 化に必要な他の設定項目があれば、`spec` ファイルをさらにカスタマイズしてください。
- EXEファイルの操作方法については、`explanation.md`を参照してください。