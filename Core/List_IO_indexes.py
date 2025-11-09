import sounddevice as sd
from Config_Manager import Config_Manager



devices = sd.query_devices()
for device in devices:
    print(f"{device['index']} : {device['name']}")
        
