import os
import subprocess
import platform
import webbrowser
import time
import requests

os.chdir("./app")

os_commands = {
    "Windows": ["python3", "-m", "uvicorn", "main:app"],
    "Linux": ["uvicorn", "main:app", "--reload"],
    # aqui para adicionar otros SO
}

os_name = platform.system()
subprocess.Popen(os_commands[os_name])

url = "http://127.0.0.1:8000"
while True:
    try:
        requests.get(url)
        break
    except requests.exceptions.ConnectionError:
        time.sleep(0.5)


webbrowser.open(url)