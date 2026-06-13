import subprocess
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error,
    prompt, confirm, adb, get_adb_exe, submenu_row
)


def _run_host(config: AppConfig, args: list[str]) -> subprocess.CompletedProcess:
    exe = get_adb_exe(config)
    if not exe:
        return subprocess.CompletedProcess(args=[], returncode=127, stdout="", stderr="no adb")
    return subprocess.run([exe] + args, capture_output=True, text=True)


def port_forward_menu(config: AppConfig) -> None:
    submenu_row("Forward (PC→Device)", "Reverse (Device→PC)", "List rules", "Remove rule", "Remove all")
    choice = prompt("Option: ")

    if choice == "1":
        local = prompt("Local (PC) TCP port: ")
        remote = prompt("Remote (device) TCP port: ")
        if not local.isdigit() or not remote.isdigit():
            print_error("Port must be a number.")
            return
        r = _run_host(config, ["forward", f"tcp:{local}", f"tcp:{remote}"])
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            print_success(out or f"Forwarded tcp:{local} → device tcp:{remote}")
        else:
            print_error(out or "forward failed")

    elif choice == "2":
        remote = prompt("Device TCP port: ")
        local = prompt("Host TCP port: ")
        if not remote.isdigit() or not local.isdigit():
            print_error("Port must be a number.")
            return
        r = _run_host(config, ["reverse", f"tcp:{remote}", f"tcp:{local}"])
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            print_success(out or f"Reverse tcp:{remote} → host tcp:{local}")
        else:
            print_error(out or "reverse failed")

    elif choice == "3":
        r = _run_host(config, ["forward", "--list"])
        out = (r.stdout + r.stderr).strip()
        print(out or "No forwarding rules.")

    elif choice == "4":
        spec = prompt("Rule to remove (e.g. tcp:8080): ")
        if not spec:
            return
        r = _run_host(config, ["forward", "--remove", spec])
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            print_success(out or "Removed.")
        else:
            print_error(out or "remove failed")

    elif choice == "5":
        if not confirm("Remove all forwarding rules?"):
            return
        r = _run_host(config, ["forward", "--remove-all"])
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0:
            print_success(out or "All rules removed.")
        else:
            print_error(out or "failed")

    else:
        print_error("Invalid selection.")
