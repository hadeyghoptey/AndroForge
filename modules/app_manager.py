from pathlib import Path
from modules.config import AppConfig
from modules.console import (
    print_info, print_success, print_error, print_warning,
    prompt, confirm, adb, adb_output, ensure_output_dir, submenu_row
)


def _list_third_party(config: AppConfig) -> list[str]:
    raw = adb_output(config, ["shell", "pm", "list", "packages", "-3"])
    return [l.replace("package:", "").strip() for l in raw.splitlines() if l.strip()]


def _list_all_packages(config: AppConfig) -> list[str]:
    raw = adb_output(config, ["shell", "pm", "list", "packages"])
    return [l.replace("package:", "").strip() for l in raw.splitlines() if l.strip()]


def _select_package(config: AppConfig, title: str = "Installed Apps") -> str:
    submenu_row("Third-party only", "All packages")
    mode = prompt("List: ")
    if mode == "1":
        apps = _list_third_party(config)
    elif mode == "2":
        apps = _list_all_packages(config)
    else:
        print_error("Invalid selection.")
        return ""
    if not apps:
        print_warning("No apps found.")
        return ""
    print()
    for i, pkg in enumerate(apps, 1):
        print(f"  {i:>4}. {pkg}")
    print()
    choice = prompt(f"Select app (1-{len(apps)}): ")
    if choice.isdigit():
        n = int(choice)
        if 1 <= n <= len(apps):
            return apps[n - 1]
    print_error("Invalid selection.")
    return ""


def list_apps(config: AppConfig) -> None:
    submenu_row("Third-party only", "All packages")
    mode = prompt("List: ")
    if mode == "1":
        apps = _list_third_party(config)
        title = "Third-Party Apps"
    elif mode == "2":
        apps = _list_all_packages(config)
        title = "All Packages"
    else:
        print_error("Invalid selection.")
        return
    if not apps:
        print_warning("No apps found.")
        return
    print_info(f"{title} ({len(apps)}):")
    print()
    for i, pkg in enumerate(apps, 1):
        print(f"  {i:>4}. {pkg}")
    print()


def run_app(config: AppConfig) -> None:
    submenu_row("Select from list", "Enter package name manually")
    mode = prompt("Mode: ")
    pkg = ""
    if mode == "1":
        pkg = _select_package(config)
    elif mode == "2":
        pkg = prompt("Package name (e.g. com.example.app): ")
    else:
        print_error("Invalid selection.")
        return
    if not pkg:
        return
    print_info(f"Launching {pkg}...")
    adb(config, ["shell", "monkey", "-p", pkg, "1"])
    print_success(f"Launched: {pkg}")


def install_app(config: AppConfig) -> None:
    path = prompt("APK path on computer: ")
    if not path:
        print_error("No path entered.")
        return
    path = path.strip("'\"")
    apk = Path(path)
    if not apk.is_file():
        print_error("File not found.")
        return
    if not confirm(f"Install {apk.name}?"):
        return
    print_info(f"Installing {apk.name}...")
    result = adb(config, ["install", "-r", str(apk)])
    out = (result.stdout + result.stderr).strip()
    if "Success" in out:
        print_success(f"Installed: {apk.name}")
    else:
        print_error(f"Installation failed: {out}")


def uninstall_app(config: AppConfig) -> None:
    submenu_row("Select from list", "Enter package name manually")
    mode = prompt("Mode: ")
    pkg = ""
    if mode == "1":
        pkg = _select_package(config)
    elif mode == "2":
        pkg = prompt("Package name (e.g. com.example.app): ")
    else:
        print_error("Invalid selection.")
        return
    if not pkg:
        return
    if not confirm(f"Uninstall {pkg}?"):
        return
    print_info(f"Uninstalling {pkg}...")
    result = adb(config, ["uninstall", pkg])
    out = (result.stdout + result.stderr).strip()
    if "Success" in out:
        print_success(f"Uninstalled: {pkg}")
    else:
        print_error(f"Failed: {out}")


def extract_apk(config: AppConfig) -> None:
    submenu_row("Select from list", "Enter package name manually")
    mode = prompt("Mode: ")
    pkg = ""
    if mode == "1":
        pkg = _select_package(config)
    elif mode == "2":
        pkg = prompt("Package name (e.g. com.example.app): ")
    else:
        print_error("Invalid selection.")
        return
    if not pkg:
        return
    if not confirm(f"Extract APK for {pkg}?"):
        return

    save_dir = ensure_output_dir(config, "pull_location")
    out_name = pkg.replace(".", "_") + ".apk"
    dest = save_dir / out_name

    path_out = adb_output(config, ["shell", "pm", "path", pkg])
    lines = [l.strip() for l in path_out.splitlines() if l.strip().startswith("package:")]
    paths = [l.replace("package:", "").strip() for l in lines]
    if not paths:
        print_error(f"Package not found: {pkg}")
        return

    apk_path = paths[0]
    for p in paths:
        if p.endswith("base.apk"):
            apk_path = p
            break

    print_info(f"Pulling {Path(apk_path).name}...")
    result = adb(config, ["pull", apk_path])
    if result.returncode != 0:
        print_error((result.stdout + result.stderr).strip())
        return

    pulled = Path(apk_path).name
    src = Path(pulled)
    if not src.is_file() and Path("base.apk").is_file():
        src = Path("base.apk")
    if src.is_file():
        src.rename(dest)
        print_success(f"Saved to: {dest}")
    else:
        print_error("Could not locate pulled APK file.")
