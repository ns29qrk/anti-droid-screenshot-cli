
# Version: 0.0.1
import os
import sys
import toml
import subprocess
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

# Define constants
SETTING_FILE_PATH = os.path.join(os.path.dirname(__file__), '_setting', 'setting.toml')
EXAMPLE_SETTING_FILE_PATH = os.path.join(os.path.dirname(__file__), '_setting', 'exsample.setting.toml')
LOG_DIR = os.path.join(os.path.dirname(__file__), '_log')
LOG_FILE = os.path.join(LOG_DIR, 'log.txt')

def setup_logging():
    """Sets up logging with 1 week retention."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    logger = logging.getLogger('anti_droid_screenshot')
    logger.setLevel(logging.INFO)
    
    # Create handler that rotates logs every day, keeps 7 days worth
    handler = TimedRotatingFileHandler(LOG_FILE, when='D', interval=1, backupCount=7)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

logger = setup_logging()

def load_settings():
    """Loads settings from setting.toml, falling back to exsample.setting.toml."""
    settings = {}
    try:
        if os.path.exists(SETTING_FILE_PATH):
            logger.info(f"Loading settings from {SETTING_FILE_PATH}")
            with open(SETTING_FILE_PATH, 'r') as f:
                settings = toml.load(f)
        elif os.path.exists(EXAMPLE_SETTING_FILE_PATH):
            logger.info(f"Loading settings from {EXAMPLE_SETTING_FILE_PATH}")
            with open(EXAMPLE_SETTING_FILE_PATH, 'r') as f:
                settings = toml.load(f)
        else:
            raise FileNotFoundError("No setting file found.")
            
        return settings.get('constract', {})
    except Exception as e:
        logger.error(f"Failed to load settings: {e}")
        print(f"Error loading settings: {e}")
        sys.exit(1)

def play_sound(sound_path):
    """Plays a sound file using afplay on macOS."""
    if not sound_path:
        return
    
    # If the path is relative, resolve it relative to the script directory
    # But first expand user (~) just in case
    expanded_path = os.path.expanduser(sound_path)
    if not os.path.isabs(expanded_path):
        # Join with script directory
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), expanded_path))
    else:
        abs_path = os.path.abspath(expanded_path)

    if not os.path.exists(abs_path):
        logger.warning(f"Sound file not found: {abs_path}")
        return

    try:
        subprocess.Popen(['/usr/bin/afplay', abs_path])
    except Exception as e:
        logger.error(f"Failed to play sound: {e}")

def check_device(adb_path, target_device):
    """Checks if the target device is connected."""
    try:
        result = subprocess.run([adb_path, 'devices'], capture_output=True, text=True, check=True)
        # Parse output to check for device. Simple check if string exists in output.
        # adb devices output format:
        # List of devices attached
        # <serial>    device
        if target_device in result.stdout:
            lines = result.stdout.splitlines()
            for line in lines:
                if target_device in line and 'device' in line:
                    return True
        return False
    except Exception as e:
        logger.error(f"Error checking device: {e}")
        return False

def take_screenshot(adb_path, target_device):
    """Takes a screenshot using adb exec-out."""
    try:
        command = [adb_path, '-s', target_device, 'exec-out', 'screencap', '-p']
        result = subprocess.run(command, capture_output=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"ADB command failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise

def save_screenshot(data, save_directory, prefix):
    """Saves the screenshot data to a file."""
    try:
        # Expand user path (~) if present
        save_dir_expanded = os.path.expanduser(save_directory)
        
        if not os.path.exists(save_dir_expanded):
            os.makedirs(save_dir_expanded)
            
        timestamp = datetime.datetime.now().strftime('%y%m%d-%H%M%S#%f')[:-3] # Truncate microseconds to milliseconds
        filename = f"{prefix}{timestamp}.png"
        filepath = os.path.join(save_dir_expanded, filename)
        
        with open(filepath, 'wb') as f:
            f.write(data)
            
        return filepath
    except Exception as e:
        logger.error(f"Error saving file: {e}")
        raise

def main():
    settings = load_settings()
    
    # Required parameters
    target_device = settings.get('TARGET_DEVICE')
    save_directory = settings.get('SAVE_DIRECTORY')
    adb_path = settings.get('ADB_PATH')
    
    # Optional parameters
    prefix = settings.get('PREFIX', '')
    success_sound = settings.get('SUCCESS_SOUND')
    error_sound = settings.get('ERROR_SOUND')
    
    if not all([target_device, save_directory, adb_path]):
        logger.error("Missing required settings.")
        play_sound(error_sound)
        sys.exit(1)
        
    try:
        if not check_device(adb_path, target_device):
            logger.error(f"Device {target_device} not found.")
            play_sound(error_sound)
            sys.exit(1)
            
        logger.info(f"Taking screenshot from {target_device}...")
        image_data = take_screenshot(adb_path, target_device)
        
        filepath = save_screenshot(image_data, save_directory, prefix)
        logger.info(f"Screenshot saved to {filepath}")
        
        play_sound(success_sound)
        
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        play_sound(error_sound)
        sys.exit(1)

if __name__ == "__main__":
    main()
