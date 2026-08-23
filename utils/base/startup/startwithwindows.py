import sys
import winreg
import utils.base.configpath as cfgp

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

def set_startup(enabled):
    exe_path = sys.executable if getattr(sys, "frozen", False) else None
    if not exe_path:
        return  # running from source - nothing sensible to register
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
        if enabled:
            winreg.SetValueEx(key, cfgp.APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
        else:
            try:
                winreg.DeleteValue(key, cfgp.APP_NAME)
            except FileNotFoundError:
                pass