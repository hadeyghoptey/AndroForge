import subprocess
from datetime import datetime
from pathlib import Path
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, get_adb_exe, ensure_output_dir,
    submenu_row
)


def save_logcat(config: AppConfig) -> None:
    n = prompt("Last N lines (default 500): ")
    lines = int(n) if n.isdigit() else 500
    out_dir = ensure_output_dir(config, "pull_location")
    name = f"logcat-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    path = out_dir / name
    print_info("Capturing logcat...")
    r = adb(config, ["logcat", "-d", "-t", str(lines)])
    text = r.stdout + r.stderr
    try:
        path.write_text(text, encoding="utf-8", errors="replace")
    except OSError as e:
        print_error(str(e))
        return
    print_success(f"Saved: {path}")


def live_logcat(config: AppConfig) -> None:
    filt = prompt("Optional filter (empty=all, *:W, or TAG:S): ")
    print_info("Streaming logcat (Ctrl+C to stop)...")
    exe = get_adb_exe(config)
    if not exe:
        print_error("ADB not available.")
        return
    args = [exe, "logcat", "-v", "time"]
    if filt:
        args.append(filt)
    try:
        subprocess.run(args)
    except KeyboardInterrupt:
        print("\nStopped.")


def device_backup(config: AppConfig) -> None:
    if not confirm("Create full device backup (-apk -shared -all -system)?"):
        return
    out = prompt("Output file (default backup.ab): ") or "backup.ab"
    print_info("Creating backup...")
    exe = get_adb_exe(config)
    subprocess.run([exe, "backup", "-apk", "-shared", "-all", "-system", "-f", out])
    print_success(f"Backup saved to: {out}")


def device_restore(config: AppConfig) -> None:
    src = prompt("Backup file path: ")
    if not src:
        return
    if not Path(src).is_file():
        print_error("File not found.")
        return
    if not confirm(f"Restore from {src}? This will overwrite device data."):
        return
    print_info("Restoring...")
    exe = get_adb_exe(config)
    subprocess.run([exe, "restore", src])
    print_success("Restore initiated.")


def notification_listener(config: AppConfig) -> None:
    print_info("Fetching active notifications...")
    raw = adb_output(config, ["shell", "dumpsys", "notification", "--noredact"])
    lines = [l.strip() for l in raw.splitlines()]
    shown = 0
    for line in lines:
        if any(k in line.lower() for k in ("tickertext", "title", "text", "key=", "package")):
            print(f"  {line}")
            shown += 1
    if shown == 0:
        print_warning("No notifications detected or device does not support --noredact.")
        print("Showing raw output:")
        for line in lines[:40]:
            print(f"  {line}")


def wifi_management(config: AppConfig) -> None:
    submenu_row("Saved networks", "WiFi toggle", "WLAN IP", "Ping", "Status dump")
    choice = prompt("Option: ")

    if choice == "1":
        print_info("Listing saved WiFi networks...")
        raw = adb_output(config, ["shell", "cmd", "wifi", "list-networks"])
        if "Unknown command" in raw or not raw.strip():
            raw = adb_output(config, ["shell", "dumpsys", "wifi"])
        print(raw[:2000] if raw else "No data.")

    elif choice == "2":
        mode = prompt("enable or disable: ").lower()
        if mode not in ("enable", "disable"):
            print_error("Enter 'enable' or 'disable'.")
            return
        adb(config, ["shell", "svc", "wifi", mode])
        print_success(f"WiFi {mode}d.")

    elif choice == "3":
        out = adb_output(config, ["shell", "ip", "addr", "show", "wlan0"])
        if "does not exist" in out.lower():
            out = adb_output(config, ["shell", "ip", "addr"])
        print(out or "No output.")

    elif choice == "4":
        host = prompt("Host to ping (default 8.8.8.8): ") or "8.8.8.8"
        r = adb(config, ["shell", "ping", "-c", "4", host])
        print((r.stdout + r.stderr).strip())

    elif choice == "5":
        raw = adb_output(config, ["shell", "dumpsys", "wifi"])
        for line in raw.splitlines():
            s = line.strip().lower()
            if any(k in s for k in ("ssid", "bssid", "ipaddress", "rssi", "frequency", "state:")):
                print(f"  {line.strip()}")
        if not any(k in raw.lower() for k in ("ssid", "bssid")):
            print(raw[:2000])

    else:
        print_error("Invalid selection.")
