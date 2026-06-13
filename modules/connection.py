import os
import socket
import subprocess
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, get_adb_exe
)


def get_ip_address() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3.0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return ""


def is_valid_ipv4(address: str) -> bool:
    parts = address.strip().split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(p) <= 255 for p in parts)
    except ValueError:
        return False


def list_ready_devices(config: AppConfig) -> list[str]:
    result = adb(config, ["devices"])
    serials = []
    for line in result.stdout.splitlines()[1:]:
        line = line.strip()
        if not line or "\t" not in line:
            continue
        serial, _, rest = line.partition("\t")
        state = rest.split()[0] if rest.split() else ""
        if state == "device":
            serials.append(serial.strip())
    return serials


def select_device(config: AppConfig) -> None:
    serials = list_ready_devices(config)
    if not serials:
        config.device_serial = ""
        os.environ.pop("ANDROID_SERIAL", None)
        return
    if len(serials) == 1:
        config.device_serial = serials[0]
        os.environ["ANDROID_SERIAL"] = serials[0]
        return
    print_info("Multiple devices detected:")
    for i, s in enumerate(serials, 1):
        print(f"  {i}. {s}")
    choice = prompt(f"Select device (1-{len(serials)}): ")
    idx = 0
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(serials):
            idx = n - 1
    config.device_serial = serials[idx]
    os.environ["ANDROID_SERIAL"] = serials[idx]
    print_success(f"Using device: {serials[idx]}")


def connect(config: AppConfig) -> None:
    ip = prompt("Target phone IP (e.g. 192.168.1.23): ")
    if not ip:
        print_error("No IP entered.")
        return
    if not is_valid_ipv4(ip):
        print_error("Invalid IPv4 address.")
        return
    if not confirm("Connect to this device? ADB server will restart."):
        return
    exe = get_adb_exe(config)
    print_info("Restarting ADB server...")
    subprocess.run([exe, "kill-server"], capture_output=True)
    subprocess.run([exe, "start-server"], capture_output=True)
    print_info(f"Connecting to {ip}:5555...")
    result = adb(config, ["connect", f"{ip}:5555"])
    out = result.stdout.strip()
    if "connected" in out.lower():
        print_success(out)
        select_device(config)
    else:
        print_error(out or result.stderr.strip())


def list_devices(config: AppConfig) -> None:
    result = adb(config, ["devices", "-l"])
    lines = result.stdout.strip().splitlines()
    if len(lines) <= 1:
        print_warning("No devices connected.")
        return
    print()
    for line in lines:
        print(f"  {line}")
    print()


def disconnect(config: AppConfig) -> None:
    if not confirm("Disconnect all ADB devices?"):
        return
    result = adb(config, ["disconnect"])
    os.environ.pop("ANDROID_SERIAL", None)
    config.device_serial = ""
    print_success(result.stdout.strip() or "Disconnected.")


def stop_adb_server(config: AppConfig) -> None:
    if not confirm("Stop ADB server? All connections will be lost."):
        return
    exe = get_adb_exe(config)
    subprocess.run([exe, "kill-server"])
    os.environ.pop("ANDROID_SERIAL", None)
    config.device_serial = ""
    print_success("ADB server stopped.")


def scan_network(config: AppConfig) -> None:
    ip = get_ip_address()
    if not ip:
        print_error("Could not detect local IP. Check network connection.")
        return
    subnet = ip.rsplit(".", 1)[0] + ".0/24"
    print_info(f"Scanning {subnet} for ADB ports 5555/5554...")
    try:
        import nmap
        nm = nmap.PortScanner()
        nm.scan(
            hosts=subnet,
            arguments="-Pn -sS -p 5555,5554 -sV -O --osscan-guess -T5 "
                      "--min-rate 10000 --max-retries 1 "
                      "--max-scan-delay 0 --open --version-intensity 9"
        )
        hosts = []
        for h in sorted(nm.all_hosts(), key=lambda x: tuple(int(p) for p in x.split("."))):
            tcp = nm[h].get("tcp", {})
            adb_info = ""
            status = ""
            for port in (5555, 5554):
                pinfo = tcp.get(port, {})
                if pinfo.get("state") == "open":
                    adb_info += f"{port}/tcp open "
                    if not status:
                        product = pinfo.get("product", "")
                        extrainfo = pinfo.get("extrainfo", "")
                        if "android" in (product + extrainfo).lower():
                            status = "Android Device"
                        elif "adb" in product.lower():
                            status = "ADB Enabled"
                        else:
                            status = "Unknown Device"
            if adb_info:
                hosts.append((h, adb_info, status))
        if not hosts:
            print_warning("No devices found with ADB ports open.")
            return
        print_info(f"Found {len(hosts)} device(s) with ADB ports open.")
        print()
        print(f"  {'IP Address':<20} {'ADB Ports':<30} {'Status':<20}")
        print(f"  {'-'*20} {'-'*30} {'-'*20}")
        for h, adb_info, status in hosts:
            print(f"  {h:<20} {adb_info:<30} {status:<20}")
        print()
    except ImportError:
        print_error("nmap module not installed. Run: pip install python-nmap")
    except Exception as e:
        print_error(f"Scan failed: {e}")
