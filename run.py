import os
import subprocess
import platform
import webbrowser
import time
import requests
from pathlib import Path


absolute_path = Path("app/db").resolve()
docker_compose_command = "docker-compose up -d"

try:
    result = subprocess.run(docker_compose_command, shell=True, cwd=absolute_path, check=True, capture_output=True)
    standard_output = result.stdout.decode("utf-8")
    error_output = result.stderr.decode("utf-8")

    print("Standard:")
    print(standard_output)

    if error_output:
        print("Error output:")
        print(error_output)

except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")



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