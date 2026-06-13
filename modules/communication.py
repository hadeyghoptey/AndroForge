from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb
)


def send_sms(config: AppConfig) -> None:
    print_warning("BETA — tested on Android 12+.")
    number = prompt("Phone number (with country code, e.g. +911234567890): ")
    if not number:
        print_error("No number entered.")
        return
    message = prompt("Message: ")
    if not confirm(f"Send SMS to {number}?"):
        return
    print_info("Sending SMS...")
    adb(config, [
        "shell", "service", "call", "isms", "5",
        "i32", "0",
        "s16", "com.android.mms.service",
        "s16", "null",
        "s16", number,
        "s16", "null",
        "s16", message,
        "s16", "null",
        "s16", "null",
        "s16", "null",
        "s16", "null",
    ])
    print_success(f"SMS sent to {number}.")


def open_link(config: AppConfig) -> None:
    url = prompt("URL (e.g. https://github.com): ")
    if not url:
        print_error("No URL entered.")
        return
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    if not confirm(f"Open {url} on device?"):
        return
    print_info("Opening URL...")
    adb(config, ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url])
    print_success(f"Opened: {url}")
