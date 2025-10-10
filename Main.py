import callLLM as LLM
from RealtimeSTT import AudioToTextRecorder
from Text_To_Speech import TTS
import onnxruntime as ort


def run(text):
    
    print(text)
    if "exit chat" in text.lower():
        goal = [{"role": "system", "content": "you are GlaD0s from the video game Portal"}]
        ai__response = LLM.call(goal, max_tokens=1000)
        speech = ai__response[0]
        print(speech)
        GLAD0S.readAloud(speech)
        quit()

    messages.append({"role": "user",
                     "content": text})
    
    ai__response = LLM.call(messages)
    messages.append(ai__response[1])
    
    speech = ai__response[0]
    print(speech)
    GLAD0S.readAloud(speech)


if __name__ == '__main__':
    
    messages = [{"role": "system",
                 "content": "you are glados"}]
    GLAD0S = TTS()
    recorder = AudioToTextRecorder()
    while True:
        input("press any key to start talking")
        run(recorder.text())
        