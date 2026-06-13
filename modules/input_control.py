import os
from modules.config import AppConfig
from modules import banner
from modules.console import print_info, print_success, print_error, prompt, confirm, adb, get_adb_exe


def use_keycode(config: AppConfig) -> None:
    os.system(config.clear_cmd)
    print(banner.keycode_menu)

    while True:
        option = prompt("[KEYCODE] > ").strip().lower()

        if option == "0":
            return
        elif option == "99":
            os.system(config.clear_cmd)
            print(banner.keycode_menu)
        elif option == "1":
            text = prompt("Text: ")
            adb(config, ["shell", "input", "text", f'"{text}"'])
            print_success(f'Entered: "{text}"')
        elif option == "2":
            adb(config, ["shell", "input", "keyevent", "3"])
            print_success("Home")
        elif option == "3":
            adb(config, ["shell", "input", "keyevent", "4"])
            print_success("Back")
        elif option == "4":
            adb(config, ["shell", "input", "keyevent", "187"])
            print_success("Recent apps")
        elif option == "5":
            adb(config, ["shell", "input", "keyevent", "26"])
            print_success("Power")
        elif option == "6":
            adb(config, ["shell", "input", "keyevent", "19"])
            print_success("DPAD up")
        elif option == "7":
            adb(config, ["shell", "input", "keyevent", "20"])
            print_success("DPAD down")
        elif option == "8":
            adb(config, ["shell", "input", "keyevent", "21"])
            print_success("DPAD left")
        elif option == "9":
            adb(config, ["shell", "input", "keyevent", "22"])
            print_success("DPAD right")
        elif option == "10":
            adb(config, ["shell", "input", "keyevent", "67"])
            print_success("Delete")
        elif option == "11":
            adb(config, ["shell", "input", "keyevent", "66"])
            print_success("Enter")
        elif option == "12":
            adb(config, ["shell", "input", "keyevent", "24"])
            print_success("Volume up")
        elif option == "13":
            adb(config, ["shell", "input", "keyevent", "25"])
            print_success("Volume down")
        elif option == "14":
            adb(config, ["shell", "input", "keyevent", "126"])
            print_success("Media play")
        elif option == "15":
            adb(config, ["shell", "input", "keyevent", "127"])
            print_success("Media pause")
        elif option == "16":
            adb(config, ["shell", "input", "keyevent", "61"])
            print_success("Tab")
        elif option == "17":
            adb(config, ["shell", "input", "keyevent", "111"])
            print_success("Esc")
        else:
            print_error("Invalid.")
