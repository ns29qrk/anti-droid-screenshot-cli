# Anti-Droid Screenshot CLI

`adb exec-out` を活用し、Android 端末のストレージを汚さずに（SDカード等への保存を行わずに）直接 macOS へスクリーンショットを保存する Python CLI ツールです。

従来の `adb shell screencap -p` よりも転送速度が速く、撮影後に端末内の不要なファイルを削除する手間もありません。また、実行結果を音声フィードバックでお知らせします。

[ English ](https://www.google.com/search?q=./README.md) | [ 繁體中文 (Traditional Chinese) ](https://www.google.com/search?q=./README-zh-TW.md)

## 主な機能

  * **高速転送**: パイプライン処理による直接転送で、ラグの少ない撮影が可能。
  * **ストレージフリー**: Android 端末側に一時ファイルを生成しません。
  * **音声フィードバック**: 成功時・失敗時にそれぞれ異なる通知音を再生（macOS `afplay` 利用）。
  * **カスタマイズ可能**: 保存先、ファイル名プレフィックス、サウンド設定などを TOML ファイルで管理。

-----

## 更新履歴

  * **0.0.1** (2025-12-09): 初回リリース。音声フィードバック付きの基本スクリーンショット機能を実装。

-----

## 必要要件

  * **OS**: macOS
      * ※ 音声通知機能に macOS 標準の `afplay` コマンドを使用しているため。
  * **Python**: 3.x
  * **ADB**: [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)
  * **Android**: USBデバッグが有効になっている端末

-----

## インストールとセットアップ

### 1\. ADB のインストール

すでに `adb` がインストールされている場合はスキップしてください。

```bash
brew install android-platform-tools
```

### 2\. リポジトリのクローンと依存関係のインストール

```bash
git clone <repository-url>
cd anti-droid-screenshot-cli

# 設定ファイルの読み込みに必要なライブラリをインストール
pip install toml
```

### 3\. Android 端末の準備

1.  Android 端末の **「設定」 \> 「デバイス情報」** を開き、 **「ビルド番号」** を7回タップして「開発者向けオプション」を有効にします。
2.  **「システム」 \> 「開発者向けオプション」** へ進み、 **「USBデバッグ」をON** にします。
3.  Mac と USB ケーブルで接続し、端末側に表示される「USBデバッグを許可しますか？」というダイアログで **「許可」** を選択してください。

-----

## 設定

`_setting/setting.toml` を編集して動作設定を行います。
初回はサンプルファイルをコピーして作成してください。

```bash
cp _setting/example.setting.toml _setting/setting.toml
```

### 設定ファイル (`setting.toml`) の構成

`[constract]` テーブル内に以下のパラメータを設定します。

```toml
[constract]
# 必須設定
TARGET_DEVICE = "emulator-5554"        # adb devices で確認できる ID (シリアル または IP:Port)
SAVE_DIRECTORY = "/Users/hoge/Desktop" # 保存先の絶対パス
ADB_PATH = "/opt/homebrew/bin/adb"     # adb の絶対パス (which adb で確認)

# オプション設定
PREFIX = "screenshot_"                 # ファイル名の接頭辞
SUCCESS_SOUND = "_assets/shutter.mp3"  # 成功時のサウンドファイルパス
ERROR_SOUND = "_assets/error.mp3"      # 失敗時のサウンドファイルパス
```

### パラメータ詳細

| キー | 必須 | 説明 | 補足 |
| :--- | :---: | :--- | :--- |
| `TARGET_DEVICE` | ✅ | 対象 Android デバイスの ID | `adb devices` で表示される文字列 |
| `SAVE_DIRECTORY` | ✅ | スクリーンショット保存先のパス | Mac 上の絶対パスを推奨 |
| `ADB_PATH` | ✅ | ADB 実行ファイルのパス | `which adb` で確認可能 |
| `PREFIX` | - | ファイル名の先頭に付く文字列 | 例: `screenshot_20251209...` |
| `SUCCESS_SOUND` | - | 成功時の通知音 | wav, mp3 等 |
| `ERROR_SOUND` | - | エラー時の通知音 | wav, mp3 等 |

-----

## 使用方法

### 1\. シェルスクリプトを使用する場合（推奨）

実行権限がない場合は、初回のみ付与してください：

```bash
chmod +x screenshot.sh
```

以下のコマンドで実行します：

```bash
./screenshot.sh
```

### 2\. Python を直接使用する場合

```bash
python3 main.py
```

-----

## トラブルシューティング

### "Device not found" エラーが出る

  * USBケーブルが正しく接続されているか確認してください。
  * ターミナルで `adb devices` を実行し、端末が表示されるか確認してください。
  * ステータスが `unauthorized` の場合は、Android 端末側で USB デバッグの許可ダイアログを承認してください。

### 音が鳴らない

  * Mac のシステム音量（ミュートになっていないか）を確認してください。
  * `setting.toml` 内のサウンドファイルパスが正しいか確認してください。
  * ターミナルで `afplay <サウンドファイルパス>` を実行して、音が再生できるかテストしてください。

-----

## クレジット

  * **サウンド素材**: [OtoLogic](https://otologic.jp)

-----

## 免責事項

本ソフトウェアの使用により生じたいかなる損害（データ損失、機器の不具合等を含む）についても、開発者は責任を負いかねます。自己責任においてご利用ください。