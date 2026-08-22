from utils.core.states import state
from utils.base.logger import log
from utils.base.notifier import notification

#Handles with the failed api requests
def failed_request(cause):

    #Sets the connection state to false
    state.api.connection = False

    #I don't want a jolly startup notification when there is an error ocuring
    if not state.init.startup_notification:
        state.init.startup_notification = True
        notification(
            "Not Initialized Correctly!!!",
            "Check the logs to see what is wrong!",
            "Error.png",
            "minecraft-level-up-sound.wav"
        )

    #Makes the failed requests conter go up by 1
    state.api.failed_requests += 1

    #Log about it
    log(cause)

    #If there are to many errors notifies about it
    if state.api.failed_requests == 10:
        log("[ERROR] Major Failed Request Streak!")
        notification(
            "Major Failed Request Streak!!!",
            "Check the logs to see what is wrong!",
            "Error.png",
            "minecraft-level-up-sound.wav"
        )

#Function to reset the failed requests counter
def reset_failed_Request():

    #Log about it
    log(f"[SUCCESS] API request successful after {state.api.failed_requests} failed requests")

    #If it was some major error notifies about if
    if state.api.failed_requests >= 10:
        log("[NOTIFICATION] Working fine notification sent!")
        notification(
            "Everything Working Just Fine!!!",
            "Don't matter the problem it's all right now!",
            "banner.png",
            "minecraft-level-up-sound.wav"
        )

    #And finnaly resets the counter
    state.api.failed_requests = 0