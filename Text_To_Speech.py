from piper import PiperVoice, SynthesisConfig
import sounddevice as sd
import numpy as np


class TTS():
    def __init__ (self):
        
        self.voice = PiperVoice.load("Models//glados_piper_medium.onnx")
        self.test_message = """Based on the error message, it seems like you're having trouble with the CUDA Execution Provider for ONNX Runtime, which is used by Piper. Here's how you can address the issue:"""

        self.syn_config = SynthesisConfig(
            volume=1,  # half as loud
            length_scale=1,  
            noise_scale=0,  # more audio variation
            noise_w_scale=0,  # more speaking variation
            normalize_audio=False, # use raw audio from voice
            
        )

    def readAloud(self, message):
        stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16')
        stream.start()

        for chunk in self.voice.synthesize(message):
            int_data = np.frombuffer(chunk.audio_int16_bytes, dtype=np.int16)
            stream.write(int_data)

        stream.stop()
        stream.close()
        return