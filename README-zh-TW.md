# Anti-Droid Screenshot CLI

一個利用 `adb exec-out` 將 Android 螢幕截圖直接儲存到 macOS 的 Python CLI 工具，無須汙染 Android 裝置儲存空間（不會儲存到 SD 卡等）。

相較於傳統的 `adb shell screencap -p`，此工具傳輸速度更快，且拍攝後無需刪除裝置內的臨時檔案。此外，執行結果會透過音效回饋通知。

[ English ](./README.md) | [ 日本語 (Japanese) ](./README-ja.md)

## 主要功能

  * **高速傳輸**: 透過管線處理直接傳輸，實現低延遲拍攝。
  * **無須儲存空間**: 不會在 Android 裝置端產生臨時檔案。
  * **音效回饋**: 成功/失敗時播放不同提示音（使用 macOS `afplay`）。
  * **可自訂**: 透過 TOML 檔案管理儲存路徑、檔名前綴、音效設定等。

-----

## 更新履歷

  * **0.0.1** (2025-12-09): 首次發布。實作包含音效回饋的基本螢幕截圖功能。

-----

## 系統需求

  * **OS**: macOS
      * *※ 音效通知功能使用 macOS 標準 `afplay` 指令。*
  * **Python**: 3.x
  * **ADB**: [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)
  * **Android**: 已啟用 USB 偵錯的裝置

-----

## 安裝與設定

### 1. 安裝 ADB

如果 `adb` 已經安裝，請跳過此步驟。

```bash
brew install android-platform-tools
```

### 2. 複製儲存庫與安裝依賴

```bash
git clone <repository-url>
cd anti-droid-screenshot-cli

# 安裝讀取設定檔所需的函式庫
pip install toml
```

### 3. 準備 Android 裝置

1.  開啟 Android 裝置的 **「設定」 > 「關於手機」**，連續點擊 **「版本號碼」** 7 次以啟用「開發人員選項」。
2.  進入 **「系統」 > 「開發人員選項」**，將 **「USB 偵錯」開啟**。
3.  使用 USB 傳輸線連接 Mac，並在裝置上出現的「允許 USB 偵錯嗎？」對話框中選擇 **「允許」**。

-----

## 設定

編輯 `_setting/setting.toml` 進行設定。
首次使用請複製範例檔案來建立。

```bash
cp _setting/example.setting.toml _setting/setting.toml
```

### 設定檔 (`setting.toml`) 結構

在 `[constract]` 表格內設定以下參數。

```toml
[constract]
# 必須設定
TARGET_DEVICE = "emulator-5554"        # 請使用 adb devices 確認 ID (序號或 IP:Port)
SAVE_DIRECTORY = "/Users/hoge/Desktop" # 儲存目的地的絕對路徑
ADB_PATH = "/opt/homebrew/bin/adb"     # adb 的絕對路徑 (使用 which adb 確認)

# 選項設定
PREFIX = "screenshot_"                 # 檔名前綴
SUCCESS_SOUND = "_assets/shutter.mp3"  # 成功時的音效檔案路徑
ERROR_SOUND = "_assets/error.mp3"      # 失敗時的音效檔案路徑
```

### 參數詳細

| 鍵值 | 必須 | 說明 | 備註 |
| :--- | :---: | :--- | :--- |
| `TARGET_DEVICE` | ✅ | 目標 Android 裝置 ID | `adb devices` 顯示的字串 |
| `SAVE_DIRECTORY` | ✅ | 螢幕截圖儲存路徑 | 建議使用 Mac 上的絕對路徑 |
| `ADB_PATH` | ✅ | ADB 執行檔路徑 | 可用 `which adb` 確認 |
| `PREFIX` | - | 檔名開頭添加的字串 | 例: `screenshot_20251209...` |
| `SUCCESS_SOUND` | - | 成功時的通知音效 | wav, mp3 等 |
| `ERROR_SOUND` | - | 錯誤時的通知音效 | wav, mp3 等 |

-----

## 使用方法

### 1. 使用 Shell Script（推薦）

如果沒有執行權限，請執行以下指令賦予（僅需一次）：

```bash
chmod +x screenshot.sh
```

執行以下指令：

```bash
./screenshot.sh
```

### 2. 直接使用 Python

```bash
python3 main.py
```

-----

## 疑難排解

### 出現 "Device not found" 錯誤

  * 確認 USB 傳輸線是否正確連接。
  * 在終端機執行 `adb devices` 確認裝置是否顯示。
  * 如果狀態為 `unauthorized`，請在 Android 裝置端同意 USB 偵錯授權對話框。

### 沒有聲音

  * 確認 Mac 系統音量（是否靜音）。
  * 確認 `setting.toml` 內的音效檔案路徑是否正確。
  * 在終端機執行 `afplay <音效檔案路徑>` 測試是否能播放聲音。

-----

## 致謝

  * **音效素材**: [OtoLogic](https://otologic.jp)

-----

## 免責聲明

對於因使用本軟體而造成的任何損害（包括資料遺失、裝置故障等），開發者概不負責。請自行承擔風險。
