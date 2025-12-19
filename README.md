# Anti-Droid Screenshot CLI

A Python CLI tool that utilizes `adb exec-out` to save screenshots directly to macOS without "polluting" the Android device storage (no saving to SD card, etc.).

It offers faster transfer speeds than the traditional `adb shell screencap -p` and eliminates the need to delete unnecessary files from the device after capturing. It also provides audio feedback on execution results.

[ 日本語 (Japanese) ](./README-ja.md) | [ 繁體中文 (Traditional Chinese) ](./README-zh-TW.md)

## Key Features

  * **Fast Transfer**: Direct transfer via pipeline processing enables low-latency capture.
  * **Storage Free**: No temporary files are created on the Android device.
  * **Audio Feedback**: different sounds for success and failure (uses macOS `afplay`).
  * **Customizable**: Manage save destination, filename prefix, sound settings, etc., via a TOML file.

-----

## Update History

  * **0.0.1** (2025-12-09): Initial release. Implemented basic screenshot functionality with audio feedback.

-----

## Requirements

  * **OS**: macOS
      * *Note: The audio notification feature uses the macOS standard `afplay` command.*
  * **Python**: 3.x
  * **ADB**: [Android Debug Bridge](https://developer.android.com/studio/command-line/adb)
  * **Android**: Device with USB debugging enabled

-----

## Installation and Setup

### 1. Install ADB

Skip this step if `adb` is already installed.

```bash
brew install android-platform-tools
```

### 2. Clone Repository and Install Dependencies

```bash
git clone <repository-url>
cd anti-droid-screenshot-cli

# Install library required for loading configuration files
pip install toml
```

### 3. Prepare Android Device

1.  Open **Settings > About phone** on your Android device and tap **Build number** 7 times to enable "Developer options".
2.  Go to **System > Developer options** and turn **USB debugging ON**.
3.  Connect to Mac via USB cable and select **Allow** in the "Allow USB debugging?" dialog displayed on the device.

-----

## Configuration

Edit `_setting/setting.toml` to configure behavior.
For the first time, copy the sample file to create it.

```bash
cp _setting/example.setting.toml _setting/setting.toml
```

### Configuration File (`setting.toml`) Structure

Set the following parameters inside the `[constract]` table.

```toml
[constract]
# Required Settings
TARGET_DEVICE = "emulator-5554"        # ID confirming with adb devices (Serial or IP:Port)
SAVE_DIRECTORY = "/Users/hoge/Desktop" # Absolute path for save destination
ADB_PATH = "/opt/homebrew/bin/adb"     # Absolute path to adb (check with which adb)

# Optional Settings
PREFIX = "screenshot_"                 # Filename prefix
SUCCESS_SOUND = "_assets/shutter.mp3"  # Sound file path for success
ERROR_SOUND = "_assets/error.mp3"      # Sound file path for failure
```

### Parameter Details

| Key | Required | Description | Notes |
| :--- | :---: | :--- | :--- |
| `TARGET_DEVICE` | ✅ | Target Android Device ID | String displayed by `adb devices` |
| `SAVE_DIRECTORY` | ✅ | Screenshot save path | Absolute path on Mac recommended |
| `ADB_PATH` | ✅ | Path to ADB executable | Check with `which adb` |
| `PREFIX` | - | String added to the beginning of the filename | Ex: `screenshot_20251209...` |
| `SUCCESS_SOUND` | - | Notification sound for success | wav, mp3, etc. |
| `ERROR_SOUND` | - | Notification sound for error | wav, mp3, etc. |

-----

## Usage

### 1. Using Shell Script (Recommended)

If you don't have execution permissions, grant them only for the first time:

```bash
chmod +x screenshot.sh
```

Run with the following command:

```bash
./screenshot.sh
```

### 2. Using Python Directly

```bash
python3 main.py
```

-----

## Troubleshooting

### "Device not found" Error

  * Check if the USB cable is correctly connected.
  * Run `adb devices` in the terminal and check if the device is displayed.
  * If the status is `unauthorized`, approve the USB debugging permission dialog on the Android device side.

### No Sound

  * Check Mac system volume (ensure it's not muted).
  * Check if the sound file path in `setting.toml` is correct.
  * Run `afplay <sound_file_path>` in the terminal to test if the sound plays.

-----

## Credits

  * **Sound Materials**: [OtoLogic](https://otologic.jp)

-----

## Disclaimer

The developer is not responsible for any damages (including data loss, device malfunction, etc.) caused by the use of this software. Please use at your own risk.
