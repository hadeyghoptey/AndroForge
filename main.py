import os
import random
from modules.color import color_list, RESET
from modules.config import AppConfig
from modules import banner
from modules.tools import detect_platform, resolve_external_tools, check_packages
from modules.connection import connect, list_devices, disconnect, scan_network, select_device, stop_adb_server
from modules.device import get_shell, get_device_info, battery_info, reboot, power_off, unlock_device, lock_device
from modules.media import get_screenshot, screenrecord
from modules.file_manager import pull_file, push_file, copy_whatsapp, copy_camera
from modules.app_manager import list_apps, run_app, install_app, uninstall_app, extract_apk
from modules.communication import send_sms, open_link
from modules.port_forward import port_forward_menu
from modules.data_extraction import dump_sms, dump_contacts, dump_call_logs
from modules.input_control import use_keycode
from modules.extras import save_logcat, live_logcat, device_backup, device_restore, notification_listener, wifi_management


def clear_screen(config: AppConfig) -> None:
    os.system(config.clear_cmd)
    display_menu(config)


def change_page(config: AppConfig, direction: str) -> None:
    if direction == "p" and config.page_number > 0:
        config.page_number -= 1
    elif direction == "n" and config.page_number < 1:
        config.page_number += 1
    clear_screen(config)


def display_menu(config: AppConfig) -> None:
    color = random.choice(color_list)
    print(f"{color}{banner.logo}{RESET}")
    print(banner.menu[config.page_number])
    print("  0: Exit")


def start(config: AppConfig) -> None:
    os.makedirs("Downloaded-Files", exist_ok=True)
    detect_platform(config)
    resolve_external_tools(config)
    if not check_packages(config):
        config.run = False
    select_device(config)


def main(config: AppConfig) -> None:
    option = input("\n[AndroForge] > ").strip().lower()

    if option == "0":
        config.run = False
        print("\nExiting...\n")
    elif option in ("99", "clear"):
        clear_screen(config)
    elif option == "p":
        change_page(config, "p")
    elif option == "n":
        change_page(config, "n")
    elif option == "1":
        connect(config)
    elif option == "2":
        list_devices(config)
    elif option == "3":
        disconnect(config)
    elif option == "4":
        scan_network(config)
    elif option == "5":
        get_shell(config)
    elif option == "6":
        get_device_info(config)
    elif option == "7":
        battery_info(config)
    elif option == "8":
        list_apps(config)
    elif option == "9":
        run_app(config)
    elif option == "10":
        install_app(config)
    elif option == "11":
        uninstall_app(config)
    elif option == "12":
        get_screenshot(config)
    elif option == "13":
        screenrecord(config)
    elif option == "14":
        pull_file(config)
    elif option == "15":
        push_file(config)
    elif option == "16":
        copy_whatsapp(config)
    elif option == "17":
        copy_camera(config)
    elif option == "18":
        send_sms(config)
    elif option == "19":
        open_link(config)
    elif option == "20":
        reboot(config, "advanced")
    elif option == "21":
        port_forward_menu(config)
    elif option == "22":
        live_logcat(config)
    elif option == "23":
        save_logcat(config)
    elif option == "24":
        extract_apk(config)
    elif option == "25":
        device_backup(config)
    elif option == "26":
        device_restore(config)
    elif option == "27":
        notification_listener(config)
    elif option == "28":
        wifi_management(config)
    elif option == "29":
        unlock_device(config)
    elif option == "30":
        lock_device(config)
    elif option == "31":
        use_keycode(config)
    elif option == "32":
        dump_sms(config)
    elif option == "33":
        dump_contacts(config)
    elif option == "34":
        dump_call_logs(config)
    elif option == "35":
        stop_adb_server(config)
    elif option == "36":
        power_off(config)
    else:
        from modules.console import print_error
        print_error("Invalid selection!")


if __name__ == "__main__":
    config = AppConfig()
    start(config)
    clear_screen(config)

    while config.run:
        try:
            main(config)
        except KeyboardInterrupt:
            config.run = False
            print("\nExiting...\n")
