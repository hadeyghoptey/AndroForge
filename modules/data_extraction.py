from pathlib import Path
from datetime import datetime
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error,
    prompt, confirm, adb, adb_output, ensure_output_dir
)


def _timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def _write_dump(config: AppConfig, result, dest: Path) -> None:
    if result.returncode != 0:
        err = result.stderr.strip() or "(no stderr)"
        print_error(f"Dump failed: {err}")
        return
    try:
        dest.write_text(result.stdout, encoding="utf-8")
    except OSError as e:
        print_error(f"Could not write: {e}")
        return
    lines = [l for l in result.stdout.splitlines() if l.strip()]
    print_success(f"Saved {len(lines)} records to: {dest}")


def dump_sms(config: AppConfig) -> None:
    if not confirm("Export all SMS to a file?"):
        return
    save_dir = ensure_output_dir(config, "pull_location")
    dest = Path(save_dir) / f"sms_dump-{_timestamp()}.txt"
    print_info("Dumping SMS...")
    result = adb(config, [
        "shell", "content", "query",
        "--uri", "content://sms/",
        "--projection", "address:date:body",
    ])
    _write_dump(config, result, dest)


def dump_contacts(config: AppConfig) -> None:
    if not confirm("Export all contacts to a file?"):
        return
    save_dir = ensure_output_dir(config, "pull_location")
    dest = Path(save_dir) / f"contacts_dump-{_timestamp()}.txt"
    print_info("Dumping contacts...")
    result = adb(config, [
        "shell", "content", "query",
        "--uri", "content://contacts/phones/",
        "--projection", "display_name:number",
    ])
    _write_dump(config, result, dest)


def dump_call_logs(config: AppConfig) -> None:
    if not confirm("Export all call logs to a file?"):
        return
    save_dir = ensure_output_dir(config, "pull_location")
    dest = Path(save_dir) / f"call_logs_dump-{_timestamp()}.txt"
    print_info("Dumping call logs...")
    result = adb(config, [
        "shell", "content", "query",
        "--uri", "content://call_log/calls",
        "--projection", "name:number:duration:date",
    ])
    _write_dump(config, result, dest)
