from pathlib import Path
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, ensure_output_dir
)


def pull_file(config: AppConfig) -> None:
    location = prompt("Path under /sdcard/ (e.g. Download/file.txt): ")
    if not location:
        print_error("No path entered.")
        return
    full_path = f"/sdcard/{location}"
    check = adb(config, ["shell", "test", "-e", full_path])
    if check.returncode != 0:
        print_error(f"Path does not exist: {full_path}")
        return
    out_dir = ensure_output_dir(config, "pull_location")
    print_info(f"Pulling {full_path}...")
    result = adb(config, ["pull", full_path, str(out_dir)])
    if result.returncode == 0:
        print_success(f"Saved to: {out_dir}")
    else:
        print_error((result.stdout + result.stderr).strip())


def push_file(config: AppConfig) -> None:
    location = prompt("File path on computer: ")
    if not location:
        print_error("No path entered.")
        return
    location = location.strip("'\"")
    file_path = Path(location)
    if not file_path.exists():
        print_error("File does not exist.")
        return
    dest = prompt("Destination under /sdcard/ (e.g. Documents): ")
    print_info(f"Pushing {file_path.name}...")
    result = adb(config, ["push", str(file_path), f"/sdcard/{dest}"])
    if result.returncode == 0:
        print_success(f"Pushed to /sdcard/{dest}")
    else:
        print_error((result.stdout + result.stderr).strip())


def _pull_dir(config: AppConfig, remote: str, label: str) -> None:
    out_dir = ensure_output_dir(config, "pull_location")
    print_info(f"Pulling {label}...")
    result = adb(config, ["pull", remote, str(out_dir)])
    if result.returncode == 0:
        print_success(f"{label} saved to: {out_dir}")
    else:
        print_error((result.stdout + result.stderr).strip())


def copy_whatsapp(config: AppConfig) -> None:
    new = adb(config, ["shell", "test", "-d", "/sdcard/Android/media/com.whatsapp/WhatsApp"])
    old = adb(config, ["shell", "test", "-d", "/sdcard/WhatsApp"])
    if new.returncode == 0:
        loc = "/sdcard/Android/media/com.whatsapp/WhatsApp"
    elif old.returncode == 0:
        loc = "/sdcard/WhatsApp"
    else:
        print_error("WhatsApp folder not found on device.")
        return
    if not confirm("Copy WhatsApp data? This may transfer large files."):
        return
    _pull_dir(config, loc, "WhatsApp Data")


def copy_camera(config: AppConfig) -> None:
    check = adb(config, ["shell", "test", "-d", "/sdcard/DCIM/Camera"])
    if check.returncode != 0:
        print_error("Camera folder not found on device.")
        return
    if not confirm("Copy all camera photos? This may transfer large files."):
        return
    _pull_dir(config, "/sdcard/DCIM/Camera", "Camera Photos")
