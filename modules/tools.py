import os
import platform
import shutil
import subprocess

from modules.config import AppConfig


def detect_platform(config: AppConfig) -> None:
    config.operating_system = platform.system()
    if config.operating_system == "Windows":
        config.clear_cmd = "cls"
        config.opener = "start"
    elif config.operating_system == "Darwin":
        config.opener = "open"


def resolve_external_tools(config: AppConfig) -> None:
    config.adb_path = shutil.which("adb") or ""
    config.nmap_path = shutil.which("nmap") or ""


def check_packages(config: AppConfig) -> bool:
    missing = []
    if not config.adb_path:
        missing.append("ADB (platform-tools)")
    if not config.nmap_path:
        missing.append("Nmap")

    if not missing:
        return True

    print(f"{'='*60}")
    print(f"  Missing required tools:")
    for m in missing:
        print(f"    - {m}")
    print()
    print(f"  Install ADB:  sudo apt install adb  (or platform-tools)")
    print(f"  Install Nmap: sudo apt install nmap")
    print(f"{'='*60}")
    return False
