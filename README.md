# AndroForge

Android Debug Forge Toolkit — a modular ADB toolkit for Android device management over USB or Wi-Fi.

## Features

### Page 1 — Connection and Device Management

| # | Feature | Description |
|---|---------|-------------|
| 1 | Connect a Device | Wi-Fi ADB connection (IP:5555) |
| 2 | List Connected Devices | Display connected devices with transport info |
| 3 | Disconnect All Devices | Terminate all ADB sessions |
| 4 | Scan Network for Devices | Nmap-based LAN scan probing ADB ports 5555 and 5554 |
| 5 | Access Device Shell | Interactive ADB shell session |
| 6 | Get Device Information | Model, manufacturer, Android version, security patch |
| 7 | Battery Information | Level, status, health, temperature, technology |
| 8 | List Installed Apps | Display third-party or all packages |
| 9 | Run an App | Launch app by list selection or package name |
| 10 | Install an APK | Install package from local file path |
| 11 | Uninstall an App | Remove app by list selection or package name |
| 12 | Get Screenshot | Capture screen with optional auto-delete mode |
| 13 | Screen Record | Record screen with configurable duration |
| 14 | Download File or Folder | Pull files from device storage |
| 15 | Send File or Folder | Push files to device storage |
| 16 | Copy WhatsApp Data | Pull WhatsApp data directory (legacy and scoped storage paths) |
| 17 | Copy Camera Photos | Pull all photos from DCIM/Camera |

### Page 2 — Tools and Utilities

| # | Feature | Description |
|---|---------|-------------|
| 18 | Send SMS | Send SMS via ADB service call (Android 12+) |
| 19 | Open Link on Device | Open URL through ACTION_VIEW intent |
| 20 | Advanced Reboot | Reboot to system, recovery, bootloader, or fastboot |
| 21 | Port Forwarding | Configure and list forward and reverse TCP rules |
| 22 | Logcat Viewer | Live logcat stream with optional filter |
| 23 | Logcat Export | Save last N log lines to a timestamped file |
| 24 | APK Extractor | Pull installed APK from device to computer |
| 25 | Device Backup | Full device backup via adb backup |
| 26 | Device Restore | Restore device from a backup file |
| 27 | Notification Listener | Dump active notifications via dumpsys |
| 28 | WiFi Management | List saved networks, toggle, view IP, ping, dump status |
| 29 | Screen Mirror (scrcpy) | Mirror and control the device screen via scrcpy |
| 30 | Use Keycodes | Interactive keycode sender with 17 actions |
| 31 | Dump SMS | Export SMS messages to file |
| 32 | Dump Contacts | Export contact list to file |
| 33 | Dump Call Logs | Export call history to file |
| 34 | Stop ADB Server | Kill the ADB server process |
| 35 | Power Off Device | Shut down device |

## Requirements

- Python 3.8 or newer
- ADB (Android Debug Bridge) — install via `sudo apt install adb` or [platform-tools](https://developer.android.com/studio/releases/platform-tools)
- Nmap — install via `sudo apt install nmap`
- Python package: `python-nmap`

## Installation

```bash
git clone https://github.com/hadeyghoptey/AndroForge.git
cd AndroForge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Tutorial

### Setting Up Android Phone for the First Time

#### Enabling Developer Options

1. Open **Settings**.
2. Go to **About Phone**.
3. Find **Build Number**.
4. Tap on **Build Number** 7 times.
5. Enter your pattern, PIN or password to enable the Developer options menu.
6. The **Developer options** menu will now appear in your Settings menu.

#### Enabling USB Debugging

1. Open **Settings**.
2. Go to **System > Developer options**.
3. Scroll down and enable **USB debugging**.

#### Connecting with Computer

1. Connect your Android device and ADB host computer to a common Wi-Fi network.
2. Connect the device to the host computer with a USB cable.
3. Open a terminal on the computer and enter:

   ```bash
   adb devices
   ```

4. A pop-up will appear on the Android phone when connecting to a new PC for the first time: **Allow USB debugging?**.
5. Check **Always allow from this computer** and click **Allow**.
6. In the terminal, enter:

   ```bash
   adb tcpip 5555
   ```

7. Now you can connect the Android phone with the computer over Wi-Fi using ADB.
8. Disconnect the USB cable.
9. Go to **Settings > About Phone > Status > IP address** and note the phone's IP address.
10. Run AndroForge, select **Connect a device**, and enter the phone's IP address to connect over Wi-Fi.

#### Connecting the Android Phone for Subsequent Sessions

1. Connect your Android device and host computer to a common Wi-Fi network.
2. Run AndroForge, select **Connect a device**, and enter the phone's IP address to connect over Wi-Fi.

### Verify Dependencies

```bash
python3 --version
pip3 --version
adb version
scrcpy --version
nmap --version
```

## Project Structure

```
AndroForge/
  main.py                  Entry point
  modules/
    config.py              Application configuration
    console.py             ADB wrapper and output helpers
    tools.py               Platform detection and tool resolution
    color.py               ANSI color constants
    banner.py              ASCII banner and menu layout
    connection.py          Device connection, discovery, and server control
    device.py              Shell, device info, battery, reboot, lock, power
    media.py               Screenshot and screen recording
    file_manager.py        File transfer, WhatsApp and camera data copy
    app_manager.py         App listing, launch, install, uninstall, APK extraction
    communication.py       SMS sending and URL opening
    port_forward.py        TCP port forwarding and reverse forwarding
    data_extraction.py     SMS, contact, and call log export
    input_control.py       Keycode injection and device unlocking
    extras.py              Logcat, backup and restore, notifications, WiFi
  requirements.txt         Python dependencies
  Downloaded-Files/        Default output directory for pulled data
```

## Acknowledgements

AndroForge incorporates concepts and patterns from the following open-source projects:

- **[PhoneSploit-Pro](https://github.com/AzeemIdrisi/PhoneSploit-Pro)** by Azeem Idrisi — primary architectural reference for modular design, console helpers, port forwarding, data extraction, and WiFi utilities.
- **[Ghost Framework](https://github.com/entynetproject/ghost)** by Entynetproject — keycode injection and device control patterns.
- **[ADB-Toolkit](https://github.com/ASHWIN990/ADB-Toolkit)** by ASHWINI SAHU — reference for multi-device ADB management workflows.
- **[AndroRAT](https://github.com/karma9874/AndroRAT)** by karma9874 — insights on device information gathering.
- **[Android-RAT](https://github.com/sa-fw-an/Android-RAT)** by Safwan Sayeed — APK handling and signing reference.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is provided for educational purposes and authorized security testing only. Unauthorized access to computer systems is illegal. The developers assume no liability for misuse or damage caused by this program.
