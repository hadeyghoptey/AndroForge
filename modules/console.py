import os
import subprocess
from pathlib import Path
from modules.config import AppConfig


def print_banner(text: str, color: str = "") -> None:
    print(f"{color}{text}\033[0m")


def print_info(text: str) -> None:
    print(f"\033[96m{text}\033[0m")


def print_success(text: str) -> None:
    print(f"\033[92m{text}\033[0m")


def print_warning(text: str) -> None:
    print(f"\033[93m{text}\033[0m")


def print_error(text: str) -> None:
    print(f"\033[91m{text}\033[0m")


def print_dim(text: str) -> None:
    print(f"\033[2m{text}\033[0m")


def prompt(text: str) -> str:
    return input(f"\033[97m{text}\033[0m").strip()


def confirm(text: str = "Continue?") -> bool:
    choice = input(f"\n\033[93m{text}\033[0m  \033[97mY / N\033[0m > ").strip().lower()
    while choice not in ("y", "n", ""):
        choice = input("\033[91mInvalid! Y or N >\033[0m ").strip().lower()
    return choice in ("y", "")


def submenu_row(*labels: str) -> None:
    parts = [f"\033[2m{i}\033[0m {l}" for i, l in enumerate(labels, 1)]
    print("  " + "   ".join(parts))


def ensure_output_dir(config: AppConfig, setting: str, default: str = "Downloaded-Files") -> Path:
    val = getattr(config, setting, "")
    if not val:
        val = input(f"\033[93mOutput folder\033[0m \033[2m(Enter={default})\033[0m > ").strip() or default
        setattr(config, setting, val)
    p = Path(val)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_adb_exe(config: AppConfig) -> str:
    return config.adb_path or "adb"


def adb(config: AppConfig, args: list[str], capture: bool = True) -> subprocess.CompletedProcess:
    exe = get_adb_exe(config)
    cmd = [exe] + args
    try:
        if capture:
            return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        return subprocess.run(cmd)
    except FileNotFoundError:
        return subprocess.CompletedProcess(args=cmd, returncode=127, stdout="", stderr="adb not found")


def adb_output(config: AppConfig, args: list[str]) -> str:
    return adb(config, args).stdout.strip()


def require_device(config: AppConfig) -> bool:
    out = adb_output(config, ["devices"])
    lines = [l for l in out.splitlines() if l.strip() and "\tdevice" in l]
    if not lines:
        print_error("No device connected.")
        return False
    return True
