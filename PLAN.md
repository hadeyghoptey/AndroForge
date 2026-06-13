# AndroForge — Complete Revamp Plan

> **Formerly:** BAU KO PHONE  
> **New Name:** AndroForge  
> **Goal:** A clean, modern, well-optimized ADB toolkit with only the best features — pulling from PhoneSploit-Pro, Ghost Framework, AndroRAT, Android-RAT, and ADB-Toolkit.

---

## Phase 0: Clean Slate — Strip Everything Non-Essential

### Features to KEEP (from your list)

| # | Feature | Source (current) | Notes |
|---|---------|-----------------|-------|
| 1 | Connect a Device | main.py:122 | Keep, improve UX |
| 2 | List Connected Devices | main.py:146 | Keep, add table format |
| 3 | Disconnect All Devices | main.py:152 | Keep |
| 4 | Scan Network for Devices | main.py:1398 | Keep, improve nmap scan (probe 5555/5554) |
| 5 | Get Screenshot | main.py:169 | Keep, add anonymous variant |
| 6 | Screen Record | main.py:208 | Keep, add anonymous variant |
| 7 | Download File/Folder | main.py:252 | Keep, improve path resolution |
| 8 | Send File/Folder | main.py:302 | Keep |
| 9 | Run an App | main.py:417 | Keep, add list-select + manual modes |
| 10 | List Installed Apps | main.py:470 | Keep, add third-party/all toggle |
| 11 | Access Shell | main.py:164 | Keep, add firmware-update note |
| 12 | Copy WhatsApp Data | main.py:658 | Keep, support new & old path |
| 13 | Copy Camera Photos | main.py:727 | Keep, confirm before large transfer |
| 14 | Send SMS | main.py:1123 | Keep, improve reliability |
| 15 | Open Link on Device | main.py:916 | Keep |
| 16 | Get Device Information | main.py:1083 | Keep, extend with more props |
| 17 | Advanced Reboot Options | main.py:505 | Keep (system/recovery/bootloader/fastboot/power-off) |

### Features to REMOVE (from current code & banner)

- Mirror & Control (scrcpy) — moved to P2
- Hack Device / Metasploit automation — removed (bloated, niche)
- Install APK / Uninstall App — moved to P1
- List All Folders/Files — redundant with file manager
- Copy All Screenshots — narrow use-case, remove
- Anonymous Screenshot — merged into base screenshot with --delete flag
- Anonymous Screen Record — merged into base screenrecord with --delete flag
- Display Photo / Audio / Video on Device — moved to P2
- Get Battery Information — moved to P1
- Restart Device (basic) — covered by Advanced Reboot
- Unlock / Lock Device — moved to P1
- Dump SMS / Contacts / Call Logs — moved to P1
- Extract APK — moved to P1 (essential toolkit)
- Stop ADB Server — moved to P1
- Use Keycodes — moved to P1
- Listen / Record Mic & Device Audio — moved to P2
- Update AndroForge — removed (manual git pull is fine)
- Visit GitHub — removed
- All Metasploit references (instructions banner, hack function)

---

## Phase 1: P0 — Core Feature Rebuild (17 features)

All P0 features get:
- Clean modular architecture (one file per domain)
- Rich console output (tables, spinners, colors)
- Consistent error handling & user confirmations
- Cross-platform support (Linux/macOS/Windows)

### Architecture (P0)

```
main.py                  → Entry point (thin, just starts CLI)
modules/
  __init__.py
  banner.py              → ASCII banners, menu strings
  color.py               → ANSI color constants
  config.py              → AppConfig dataclass
  console.py             → Rich console, adb() wrapper, helpers
  tools.py               → External tool resolution (adb, nmap)
  connection.py          → connect, list, disconnect, scan_network
  device.py              → get_shell, get_device_info, reboot, power_off
  media.py               → get_screenshot, screenrecord (with anonymous flags)
  file_manager.py        → pull_file, push_file, copy_whatsapp, copy_camera
  app_manager.py         → run_app, list_apps
  communication.py       → send_sms, open_link
```

---

## Phase 2: P1 — Essential Toolkit Additions

Must-have ADB toolkit features (your examples + my recommendations).

### P1 Feature List

| # | Feature | Source Inspiration | Implementation |
|---|---------|-------------------|----------------|
| 18 | Port Forwarding & Reverse Forwarding | PhoneSploit-Pro `port_forward.py` | `adb forward tcp:L tcp:R`, `adb reverse tcp:R tcp:L` + list/remove/remove-all |
| 19 | Logcat Viewer & Log Export | PhoneSploit-Pro `extras.py` (live_logcat, save_logcat_snippet) | Live streaming with filter support (`*:W`, `TAG:S`); save snippet with N-line cap |
| 20 | APK Extractor | PhoneSploit-Pro `app_manager.py:extract_apk` | `pm path <pkg>` → `adb pull` → rename to `pkg.apk` |
| 21 | Full Device Backup & Restore | ADB native (not in cloned repos directly) | `adb backup -apk -shared -all -system`, `adb restore backup.ab` |
| 22 | Notification Listener & Sender | Android `cmd notification` / `dumpsys notification` | List active notifications, post test notification via `am broadcast` |
| 23 | Battery Information | PhoneSploit-Pro `device.py:battery_info` | `dumpsys battery` in table format |
| 24 | Dump SMS / Contacts / Call Logs | PhoneSploit-Pro `data_extraction.py` | `content query` on `content://sms/`, `content://contacts/phones/`, `content://call_log/calls` → save to file |
| 25 | WiFi Management | PhoneSploit-Pro `wifi_utils.py` + Ghost option 17/22 | Saved networks list (`cmd wifi list-networks` / `dumpsys wifi`), toggle on/off (`svc wifi`), WLAN IP, ping, status dump |
| 26 | Unlock / Lock Device | PhoneSploit-Pro `device.py` | Wake (keyevent 26) + swipe + text password / keyevent 26 to lock |
| 27 | Use Keycodes | PhoneSploit-Pro `input_control.py` + Ghost option 24 | Interactive keycode sender (17+ options) |
| 28 | Install / Uninstall APK | PhoneSploit-Pro `app_manager.py` | `adb install -r`, `adb uninstall` with list-select or manual |
| 29 | Stop ADB Server / Power Off | PhoneSploit-Pro `connection.py:stop_adb`, `device.py:power_off` | With confirmation prompts |
| 30 | Multi-Device Support | PhoneSploit-Pro `connection.py:prompt_select_device_if_multiple` | `ANDROID_SERIAL` env var, auto-detect + prompt on multiple |

### Architecture Additions (P1)

```
modules/
  port_forward.py        → Forward/reverse/list/remove rules
  data_extraction.py     → dump_sms, dump_contacts, dump_call_logs
  wifi_utils.py          → saved_networks, toggle, wlan_ip, ping, status
  input_control.py       → use_keycode, unlock_device, lock_device
  extras.py              → logcat (live + snippet), backup/restore, notification, battery
```

---

## Phase 3: P2 — Advanced Features

Nice-to-have, add after P0/P1 are stable.

| # | Feature | Source | Priority |
|---|---------|--------|----------|
| 31 | Mirror & Control (scrcpy) | PhoneSploit-Pro `media.py:mirror` | Medium |
| 32 | Anonymous Screenshot / Record (auto-delete) | PhoneSploit-Pro `media.py` | Low |
| 33 | Open Photo / Audio / Video on Device | PhoneSploit-Pro `media.py` | Low |
| 34 | Force Stop / Clear Data / Grant-Revoke | PhoneSploit-Pro `extras.py` | Medium |
| 35 | Network Snapshot (ip, route, dns) | PhoneSploit-Pro `extras.py:network_snapshot` | Low |
| 36 | Camera Live Stream (Android 12+) | PhoneSploit-Pro `media.py:camera_live` | Low |
| 37 | Audio Streaming / Recording (Android 11+) | PhoneSploit-Pro `media.py` | Low |
| 38 | Saved WiFi Passwords (root) | Ghost option 17 | Low (root-only) |
| 39 | Root Heuristics Check | PhoneSploit-Pro `root_check.py` | Low |
| 40 | Read Locale / Screen Stay-On / Dev Settings | PhoneSploit-Pro `extras.py` | Low |
| 41 | Install Split APKs | PhoneSploit-Pro `extras.py:install_split_apks` | Low |

---

## Integration Insights from Cloned Repos

### PhoneSploit-Pro (Primary Reference)

The most mature codebase. Key patterns to adopt:

| Pattern | File | Why |
|---------|------|-----|
| `AppConfig` dataclass | `config.py` | Clean config management |
| Rich `Console` with custom theme | `console.py` | Beautiful terminal output |
| `adb()` / `adb_output()` wrappers | `console.py` | Consistent subprocess handling |
| `task_status()` context manager | `console.py` | Spinner during operations |
| `confirm()` helper | `console.py` | Safe Y/N prompts everywhere |
| Module-per-domain | all module files | Clean separation of concerns |
| `submenu_row()` for sub-menus | `console.py` | Compact inline menus |
| `ensure_config_dir()` for output | `console.py` | User-configurable save paths |
| Multi-device via `ANDROID_SERIAL` | `connection.py` | Elegant multi-device support |
| Nmap ADB-specific port probing | `connection.py:scan_network` | Only scans 5555/5554, not all ports |
| WhatsApp path detection | `file_manager.py:copy_whatsapp` | Handles legacy + scoped storage |
| `_timestamp()` naming for files | `media.py`, `data_extraction.py` | Unique filenames |
| Logcat live streaming + snippet save | `extras.py` | Both modes covered |
| WPA supplicant parsing fallback chain | `wifi_utils.py` | Works across ROM variants |

### Ghost Framework

| Feature | Takeaway |
|---------|----------|
| Auto `adb tcpip 5555` on launch | Helpful init step |
| `adb -s <serial>` for multi-device | Serial-specific commands |
| Simple `os.system()` calls | **Don't copy** — use subprocess properly |
| WPA supplicant grab (`su -c cp ...`) | Root-based wifi password extraction |

### ADB-Toolkit (Bash)

| Feature | Takeaway |
|---------|----------|
| Multi-device up to 3 | Limit is arbitrary, use PhoneSploit's approach |
| Copy all device storage | Useful but dangerous — skip |
| Check rooted status | Already covered by root heuristics |

### AndroRAT / Android-RAT

These are RAT builders, not relevant for ADB toolkit. Skip their features — they focus on:
- APK payload generation with msfvenom
- APK patching for invisible icon / persistence
- Ngrok tunneling
- Camera / SMS / GPS exfiltration via custom APK

**Not needed** — AndroForge is an ADB toolkit, not a RAT builder.

---

## Menu & Banner Redesign

### Menu Layout (2 pages)

**Page 1 — Connection & Media (P0 + P1 essentials)**
```
 1. Connect a Device              9.  Install an APK
 2. List Connected Devices        10. Uninstall an App
 3. Disconnect All Devices        11. Get Screenshot
 4. Scan Network for Devices      12. Screen Record
 5. Access Device Shell           13. Download File/Folder
 6. Get Device Info               14. Send File/Folder
 7. Battery Information           15. Copy WhatsApp Data
 8. List Installed Apps           16. Copy Camera Photos
                                   17. Run an App

   N: Next Page  (Page 1/2)
```

**Page 2 — Tools & Utilities (P1 essentials)**
```
 18. Send SMS                     27. Port Forwarding
 19. Open Link on Device          28. Logcat Viewer
 20. Advanced Reboot Options      29. Logcat Export (Snippet)
 21. Unlock Device                30. APK Extractor
 22. Lock Device                  31. Device Backup
 23. Use Keycodes                 32. Device Restore
 24. Dump SMS                     33. Notification Listener
 25. Dump Contacts                34. WiFi Management
 26. Dump Call Logs               35. Stop ADB Server

   P: Previous Page  (Page 2/2)
```

### Banner

- Single clean AndroForge ASCII banner (replace all multi-banner randomization)
- Version number only
- Remove Metasploit / hack references entirely
- Clean top-level menu copyright line

---

## Implementation Order

### Step 1 — Skeleton
- Create new `modules/` package with config.py, console.py, tools.py, color.py
- New main.py with AppConfig, startup, menu loop
- New banner.py with clean AndroForge banner + 2-page menu

### Step 2 — P0 Connection Module
- `connection.py`: connect, list, disconnect, scan_network
- Multi-device support

### Step 3 — P0 Device Module
- `device.py`: get_shell, get_device_info, reboot (advanced), power_off

### Step 4 — P0 Media Module
- `media.py`: get_screenshot, screenrecord
- Support anonymous variant via `--no-trace` flag instead of separate option

### Step 5 — P0 File Manager Module
- `file_manager.py`: pull, push, copy_whatsapp, copy_camera

### Step 6 — P0 App Manager Module
- `app_manager.py`: run_app, list_apps, install_app, uninstall_app

### Step 7 — P0 Communication Module
- `communication.py`: send_sms, open_link

### Step 8 — P1 Port Forwarding
- `port_forward.py`: full forward/reverse management

### Step 9 — P1 Logcat
- `extras.py`: live_logcat (stream with filter), save_logcat_snippet

### Step 10 — P1 Data Extraction
- `data_extraction.py`: dump_sms, dump_contacts, dump_call_logs

### Step 11 — P1 APK Extractor
- Integrated into `app_manager.py`

### Step 12 — P1 WiFi Management
- `wifi_utils.py`: saved networks, toggle, wlan_ip, ping, status dump

### Step 13 — P1 Device Control
- `input_control.py`: use_keycode, unlock, lock

### Step 14 — P1 Battery & Backup
- Battery in `device.py`, backup/restore in `extras.py`

### Step 15 — Notification Listener
- `extras.py`: `dumpsys notification`, `cmd notification list`

### Step 16 — P2 Features
- Mirror (scrcpy), camera, audio, etc.
- Only after P0 + P1 are polished

---

## Verification & Quality

- Every operation must confirm before side effects
- Every `adb` call must handle no-device gracefully
- `requirements.txt`: only `python-nmap`, `rich`
- Drop `rich` from requirements if minimalism desired (use raw ANSI)
- Test on: Linux, macOS, Windows
- Test with: 0 devices, 1 device, 2+ devices

---

## Summary

| Phase | Features | Scope |
|-------|----------|-------|
| P0 | 17 core features | Rewrite from current main.py |
| P1 | 17 essential toolkit features | Integrate from PhoneSploit-Pro |
| P2 | ~10 advanced features | Optional, add later |

**Total target: ~34 well-crafted features** instead of the current 45 bloated ones + 63 from PhoneSploit-Pro. Quality over quantity.
