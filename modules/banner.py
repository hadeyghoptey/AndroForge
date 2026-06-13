from modules.color import RED, GREEN, CYAN, YELLOW, WHITE, RESET

version = "v2.0"

logo = f"""
{RED}        █████╗ ███╗   ██╗██████╗ ██████╗  ██████╗ ███████╗ ██████╗ ███████╗
{RED}       ██╔══██╗████╗  ██║██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔═══██╗██╔════╝
{RED}       ███████║██╔██╗ ██║██║  ██║██████╔╝██║   ██║█████╗  ██║   ██║█████╗
{RED}       ██╔══██║██║╚██╗██║██║  ██║██╔══██╗██║   ██║██╔══╝  ██║   ██║██╔══╝
{RED}       ██║  ██║██║ ╚████║██████╔╝██║  ██║╚██████╔╝██║     ╚██████╔╝███████╗
{RED}       ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝      ╚═════╝ ╚══════╝{RESET}
{GREEN}                        Android Debug Forge Toolkit{YELLOW}  {version}{RESET}
{CYAN}                     github.com/hadeyghoptey/AndroForge{RESET}
"""

menu1 = f"""
{WHITE} 1. {GREEN}Connect a Device          {WHITE}10. {GREEN}Install an APK
{WHITE} 2. {GREEN}List Connected Devices    {WHITE}11. {GREEN}Uninstall an App
{WHITE} 3. {GREEN}Disconnect All Devices    {WHITE}12. {GREEN}Get Screenshot
{WHITE} 4. {GREEN}Scan Network for Devices  {WHITE}13. {GREEN}Screen Record
{WHITE} 5. {GREEN}Access Device Shell       {WHITE}14. {GREEN}Download File/Folder
{WHITE} 6. {GREEN}Get Device Information    {WHITE}15. {GREEN}Send File/Folder
{WHITE} 7. {GREEN}Battery Information       {WHITE}16. {GREEN}Copy WhatsApp Data
{WHITE} 8. {GREEN}List Installed Apps       {WHITE}17. {GREEN}Copy Camera Photos
{WHITE} 9. {GREEN}Run an App                {WHITE}99. {CYAN}Clear Screen
{YELLOW}                               N: Next Page  (Page 1/2){RESET}
"""

menu2 = f"""
{WHITE}18. {GREEN}Send SMS                  {WHITE}28. {GREEN}WiFi Management
{WHITE}19. {GREEN}Open Link on Device       {WHITE}29. {GREEN}Unlock Device
{WHITE}20. {GREEN}Advanced Reboot Options   {WHITE}30. {GREEN}Lock Device
{WHITE}21. {GREEN}Port Forwarding           {WHITE}31. {GREEN}Use Keycodes
{WHITE}22. {GREEN}Logcat Viewer             {WHITE}32. {GREEN}Dump SMS
{WHITE}23. {GREEN}Logcat Export             {WHITE}33. {GREEN}Dump Contacts
{WHITE}24. {GREEN}APK Extractor             {WHITE}34. {GREEN}Dump Call Logs
{WHITE}25. {GREEN}Device Backup             {WHITE}35. {GREEN}Stop ADB Server
{WHITE}26. {GREEN}Device Restore            {WHITE}36. {GREEN}Power Off Device
{WHITE}27. {GREEN}Notification Listener     {WHITE}99. {CYAN}Clear Screen
{YELLOW}                               P: Previous Page  (Page 2/2){RESET}
"""

menu = [menu1, menu2]

keycode_menu = f"""
{WHITE} 1. {GREEN}Keyboard Text Input   {WHITE} 8. {GREEN}DPAD Left         {WHITE}14. {GREEN}Media Play
{WHITE} 2. {GREEN}Home                  {WHITE} 9. {GREEN}DPAD Right        {WHITE}15. {GREEN}Media Pause
{WHITE} 3. {GREEN}Back                  {WHITE}10. {GREEN}Delete/Backspace  {WHITE}16. {GREEN}Tab
{WHITE} 4. {GREEN}Recent Apps           {WHITE}11. {GREEN}Enter             {WHITE}17. {GREEN}Esc
{WHITE} 5. {GREEN}Power Button          {WHITE}12. {GREEN}Volume Up
{WHITE} 6. {GREEN}DPAD Up               {WHITE}13. {GREEN}Volume Down
{WHITE} 7. {GREEN}DPAD Down             {WHITE} 0. {WHITE}Back to Menu
"""
