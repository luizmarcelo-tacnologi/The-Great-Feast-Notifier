import winsound
from win11toast import toast
import utils.base.configpath as cfgp

def notification(header, message, image, sound):
    winsound.PlaySound(
        cfgp.resource_path(sound),
        winsound.SND_FILENAME | winsound.SND_ASYNC
    )

    toast(
        header,
        message,
        image=cfgp.resource_path(image)
    )