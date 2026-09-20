import os
import sys
import subprocess
import urllib.request
import tarfile
import platform


NGROK_URL = (
    "https://bin.equinox.io/c/bNyj1mQVY4c/"
    "ngrok-v3-stable-linux-amd64.tgz"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NGROK_DIR = os.path.join(BASE_DIR, "ngrok")
NGROK_BIN = os.path.join(NGROK_DIR, "ngrok")

FLASK_APP = os.path.join(BASE_DIR, "locationinsta.py")


def install_ngrok():

    if os.path.exists(NGROK_BIN):
        print("[+] ngrok already installed")
        return

    print("[+] Downloading ngrok for Linux...")

    archive_path = os.path.join(BASE_DIR, "ngrok.tgz")

    urllib.request.urlretrieve(NGROK_URL, archive_path)

    print("[+] Extracting ngrok...")

    os.makedirs(NGROK_DIR, exist_ok=True)

    with tarfile.open(archive_path, "r:gz") as archive:
        archive.extractall(NGROK_DIR)

    os.remove(archive_path)

    os.chmod(NGROK_BIN, 0o755)

    print("[+] ngrok installed successfully!")


def start_flask():

    print("[+] Starting Flask server...")

    subprocess.Popen(
        [sys.executable, FLASK_APP]
    )


def start_ngrok():

    print("[+] Starting ngrok tunnel...")

    subprocess.Popen(
        [NGROK_BIN, "http", "5000"]
    )


if __name__ == "__main__":

    print("[+] Linux runner started")

    install_ngrok()
    start_flask()
    start_ngrok()

    print("\n[+] Flask running on port 5000")
    print("[+] ngrok tunnel started")