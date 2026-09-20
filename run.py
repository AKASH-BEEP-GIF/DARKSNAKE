import platform
import subprocess
import sys
import os


def main():
    system = platform.system()

    print("""
==============================
       NGROK AUTO RUNNER
==============================
""")

    print(f"[+] Detected OS: {system}")

    if system == "Windows":
        runner = os.path.join("windows", "runner.py")

    elif system == "Linux":
        runner = os.path.join("linux", "runner.py")

    else:
        print(f"[-] Unsupported operating system: {system}")
        sys.exit(1)

    print(f"[+] Loading: {runner}")

    subprocess.run([sys.executable, runner])


if __name__ == "__main__":
    main()