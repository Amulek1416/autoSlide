import os
import sys

if __name__ == "__main__":
    NAME = " --name \"Auto Slide\""
    MAIN_FILE = " main.py"
    WINDOWS_ICON = " --icon=\"icons/camera-icon.ico\""
    APPLE_ICON = " --icon=\"icons/camera-icon.icns\""

    GENERAL_COMMAND = "pyinstaller --onefile --windowed"

    WINDOWS_COMMAND = GENERAL_COMMAND + WINDOWS_ICON + NAME + MAIN_FILE
    APPLE_COMMAND = GENERAL_COMMAND + APPLE_ICON + NAME + MAIN_FILE

    if sys.platform.startswith('win'):
        print(os.system(WINDOWS_COMMAND))
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        print(os.system(APPLE_COMMAND))
    elif sys.platform.startswith('darwin'):
        print(os.system(APPLE_COMMAND))
    else:
        raise EnvironmentError('Unsupported platform')

