from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np
from Config_Manager import Config_Manager
from Convo_Manager import Convo_manager


class TTS():
    def __init__ (self):
        self.config = Config_Manager()
        self.voice = PiperVoice.load("Models//glados_piper_medium.onnx")
        self.test_message = """Based on the error message, it seems like you're having trouble with the CUDA Execution Provider for ONNX Runtime, which is used by Piper. Here's how you can address the issue:"""
        self.Cmanager = Convo_manager()

        self.syn_config = SynthesisConfig(
            volume=self.config.get('audio.volume'),  
            length_scale=self.config.get('audio.length_scale'),  
            noise_scale=self.config.get('audio.noise_scale'),  
            noise_w_scale=self.config.get('audio.noise_w_scale'),  
            normalize_audio=self.config.get('audio.normalize_audio'), 
        )

    def readAloud(self, message):
        stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16', device=self.config.get('audio.output_device'))
        stream.start()
        self.Cmanager.toggle_talking()

        for chunk in self.voice.synthesize(message):
            int_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            stream.write(int_data)

        stream.stop()
        self.Cmanager.toggle_talking()
        stream.close()
        return


    