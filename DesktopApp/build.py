import subprocess

print(subprocess.run("pyinstaller --onefile --windowed --icon=\"icons/camera-icon.ico\" --name \"Auto Slide\" main.py"))