from datetime import datetime
import utils.base.configpath as cfgp

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(cfgp.log_path, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {message}\n")