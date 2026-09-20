import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

NGROK_URL = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
NGROK_DIR = os.path.join(os.getcwd(), "ngrok")
NGROK_EXE = os.path.join(NGROK_DIR, "ngrok.exe")


def install_ngrok():
    if os.path.exists(NGROK_EXE):
        print("[+] ngrok already installed")
        return

    print("[+] Downloading ngrok...")

    zip_path = os.path.join(os.getcwd(), "ngrok.zip")

    urllib.request.urlretrieve(NGROK_URL, zip_path)

    print("[+] Extracting ngrok...")

    os.makedirs(NGROK_DIR, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_file:
        zip_file.extractall(NGROK_DIR)

    os.remove(zip_path)

    print("[+] ngrok installed successfully!")


def start_flask():
    print("[+] Starting Flask server...")

    subprocess.Popen(
        [sys.executable, "locationinsta.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


def start_ngrok():
    print("[+] Starting ngrok tunnel...")

    subprocess.Popen(
        [NGROK_EXE, "http", "5000"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )


if __name__ == "__main__":

    print("""
==============================
       NGROK AUTO RUNNER
==============================
""")

    install_ngrok()

    start_flask()

    start_ngrok()

    print("\n[+] Flask running on port 5000")
    print("[+] ngrok tunnel started")
    print("[+] Check the ngrok window for your public HTTPS URL")