import winsound
import winreg
from win11toast import toast
import utils.base.configpath as cfgp

#Sets the program's identity
def register_app_identity():
    icon_path = cfgp.resource_path("hypixel.png")
    key_path = fr"Software\Classes\AppUserModelId\{cfgp.APP_NAME}"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "The Great Feast Notifier")
        winreg.SetValueEx(key, "IconUri", 0, winreg.REG_SZ, icon_path)

#Just a windows notification function
def notification(header, message, image, sound):

    #Plays the notifications sound
    winsound.PlaySound(
        cfgp.resource_path(sound),
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

    #Sends the message
    toast(
        header,
        message,
        image=cfgp.resource_path(image),
        app_id=cfgp.APP_NAME
    )