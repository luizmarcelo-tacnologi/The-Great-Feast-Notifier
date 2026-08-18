import winsound
from win11toast import toast
import utils.base.configpath as cfgp

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
        image=cfgp.resource_path(image)
    )