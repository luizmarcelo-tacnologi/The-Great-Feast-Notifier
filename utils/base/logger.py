from datetime import datetime
import utils.base.configpath as cfgp

#Just a logger function
def log(message):
    #Get the time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Writes the log
    with open(cfgp.log_path, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")