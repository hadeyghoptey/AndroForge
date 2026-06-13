import os
import subprocess
from datetime import datetime
from pathlib import Path
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, get_adb_exe, ensure_output_dir, submenu_row
)


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def get_screenshot(config: AppConfig) -> None:
    submenu_row("Normal (keep on device)", "Anonymous (delete from device)")
    choice = prompt("Mode: ")
    anonymous = choice == "2"

    file_name = f"screenshot-{_timestamp()}.png"
    remote = f"/sdcard/{file_name}"
    out_dir = ensure_output_dir(config, "screenshot_location")

    print_info("Capturing screenshot...")
    adb(config, ["shell", "screencap", "-p", remote])
    print_info("Pulling screenshot...")
    result = adb(config, ["pull", remote, str(out_dir)])

    if anonymous:
        adb(config, ["shell", "rm", remote])

    local_path = out_dir / file_name
    if result.returncode == 0:
        print_success(f"Saved to: {local_path}")
    else:
        print_error((result.stdout + result.stderr).strip())
        return

    if confirm("Open the screenshot?"):
        if config.operating_system == "Windows":
            os.startfile(str(local_path))
        else:
            subprocess.run([config.opener, str(local_path)])


def screenrecord(config: AppConfig) -> None:
    submenu_row("Normal (keep on device)", "Anonymous (delete from device)")
    mode = prompt("Mode: ")
    anonymous = mode == "2"

    duration_raw = prompt("Duration (seconds): ")
    if not duration_raw.isdigit() or int(duration_raw) < 1:
        print_error("Enter a positive integer.")
        return
    duration = int(duration_raw)

    file_name = f"recording-{_timestamp()}.mp4"
    remote = f"/sdcard/{file_name}"
    out_dir = ensure_output_dir(config, "screenrecord_location")

    exe = get_adb_exe(config)
    print_info(f"Recording {duration}s...")
    rec = subprocess.run(
        [exe, "shell", "screenrecord", "--time-limit", str(duration), remote],
        capture_output=True, text=True,
    )
    if rec.returncode != 0:
        print_error((rec.stdout + rec.stderr).strip() or "screenrecord failed")
        return

    print_info("Pulling video...")
    result = adb(config, ["pull", remote, str(out_dir)])

    if anonymous:
        adb(config, ["shell", "rm", remote])

    local_path = out_dir / file_name
    if result.returncode == 0:
        print_success(f"Saved to: {local_path}")
    else:
        print_error((result.stdout + result.stderr).strip())
        return

    if confirm("Open the recording?"):
        if config.operating_system == "Windows":
            os.startfile(str(local_path))
        else:
            subprocess.run([config.opener, str(local_path)])
