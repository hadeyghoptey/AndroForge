import subprocess
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, get_adb_exe, submenu_row
)


def get_shell(config: AppConfig) -> None:
    print_info("Opening interactive ADB shell (type 'exit' to return)...")
    exe = get_adb_exe(config)
    if not exe:
        print_error("ADB not available.")
        return
    print_warning("If shell is restricted, update device to latest firmware for full access.")
    subprocess.run([exe, "shell"])


def get_device_info(config: AppConfig) -> None:
    props = {
        "Model": ["shell", "getprop", "ro.product.model"],
        "Manufacturer": ["shell", "getprop", "ro.product.manufacturer"],
        "Chipset": ["shell", "getprop", "ro.product.board"],
        "Android Version": ["shell", "getprop", "ro.build.version.release"],
        "Security Patch": ["shell", "getprop", "ro.build.version.security_patch"],
        "Device": ["shell", "getprop", "ro.product.vendor.device"],
        "SIM Operator": ["shell", "getprop", "gsm.sim.operator.alpha"],
        "Encryption": ["shell", "getprop", "ro.crypto.state"],
        "Build Date": ["shell", "getprop", "ro.build.date"],
        "SDK Version": ["shell", "getprop", "ro.build.version.sdk"],
        "WiFi Interface": ["shell", "getprop", "wifi.interface"],
    }
    print_info("Fetching device information...")
    print()
    print(f"  {'Property':<25} {'Value':<40}")
    print(f"  {'-'*25} {'-'*40}")
    for label, cmd in props.items():
        val = adb_output(config, cmd)
        print(f"  {label:<25} {val or 'N/A':<40}")
    print()


def battery_info(config: AppConfig) -> None:
    raw = adb_output(config, ["shell", "dumpsys", "battery"])
    print_info("Battery Information:")
    print()
    print(f"  {'Property':<25} {'Value':<40}")
    print(f"  {'-'*25} {'-'*40}")
    for line in raw.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, value = line.partition(":")
            print(f"  {key.strip():<25} {value.strip():<40}")
    print()


def reboot(config: AppConfig, mode: str = "system") -> None:
    if mode == "system":
        if not confirm("Restart device? Connection will be lost."):
            return
        adb(config, ["reboot"])
        print_success("Rebooting...")
        return

    submenu_row("Recovery", "Bootloader", "Fastboot")
    choice = prompt("Mode: ")
    modes = {"1": "recovery", "2": "bootloader", "3": "fastboot"}
    if choice not in modes:
        print_error("Invalid selection.")
        return
    target = modes[choice]
    if not confirm(f"Reboot to {target}?"):
        return
    adb(config, ["reboot", target])
    print_success(f"Rebooting to {target}...")


def power_off(config: AppConfig) -> None:
    if not confirm("Power off device? Connection will be lost."):
        return
    adb(config, ["shell", "reboot", "-p"])
    print_success("Powering off...")





def lock_device(config: AppConfig) -> None:
    adb(config, ["shell", "input", "keyevent", "26"])
    print_success("Device locked.")
