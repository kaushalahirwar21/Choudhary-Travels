import os
import sys
import time

import requests


USERNAME = os.environ.get("PYTHONANYWHERE_USERNAME", "your_pythonanywhere_username")
TOKEN = os.environ.get("PYTHONANYWHERE_API_TOKEN", "")
GITHUB_URL = os.environ.get(
    "PYTHONANYWHERE_GITHUB_URL",
    "https://github.com/kaushalahirwar21/timepass.git",
)
API_BASE = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}"

HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json",
}


def create_console():
    res = requests.post(
        f"{API_BASE}/consoles/",
        headers=HEADERS,
        json={"executable": "bash"},
    )
    if res.status_code == 201:
        return res.json()["id"]
    print("Failed to create console:", res.text)
    sys.exit(1)


def send_input(console_id, command):
    res = requests.post(
        f"{API_BASE}/consoles/{console_id}/send_input/",
        headers=HEADERS,
        json={"input": command + "\n"},
    )
    return res.status_code == 200


def get_output(console_id):
    res = requests.get(
        f"{API_BASE}/consoles/{console_id}/get_latest_output/",
        headers=HEADERS,
    )
    if res.status_code == 200:
        return res.json()["output"]
    return ""


def main():
    if USERNAME == "your_pythonanywhere_username" or not TOKEN:
        print("Set PYTHONANYWHERE_USERNAME and PYTHONANYWHERE_API_TOKEN first.")
        sys.exit(1)

    print("Starting deployment to PythonAnywhere...")
    print("Creating bash console...")
    console_id = create_console()
    print(f"Console ID: {console_id}")
    time.sleep(2)

    print("Sending installation command. This can take several minutes...")
    deploy_cmd = (
        "pip3.10 install --user pythonanywhere && "
        f"pa_autoconfigure_django.py --python=3.10 {GITHUB_URL}"
    )
    send_input(console_id, deploy_cmd)

    print("Waiting for deployment output:")
    last_output = ""
    while True:
        try:
            output = get_output(console_id)
            if output is not None and len(output) > len(last_output):
                print(output[len(last_output):], end="", flush=True)
                last_output = output
            if "All done!" in output or "Error:" in output or "Traceback" in output:
                break
            time.sleep(5)
        except KeyboardInterrupt:
            break

    print(f"\nDeployment finished! Check https://{USERNAME}.pythonanywhere.com")


if __name__ == "__main__":
    main()
