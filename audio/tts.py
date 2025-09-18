## : לומר למשתמש את התשובה בקול
import pyttsx3
# generates natural voice feedback to the user the after processing a question
class Speaker:
    def __init__(self, rate: int = 180, volume: float =2.0, voice: str | None = None):
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            self.engine.setProperty('volume', volume)
            if voice:
                self.engine.setProperty('voice', voice)
            self.available = True
        except Exception as e:
            print("TTS engine failed to initialize:", e)
            self.engine = None
            self.available = False

    def say(self, text: str, wait: bool = True):
        if not text:
            print("No text provided to speak.")
            return
        if not self.available:
            print("TTS engine not available. Cannot speak.")
            return
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
        except Exception as e:
            print("Error during TTS:", e)


    def close(self):
        if self .engine:
            self .engine .stop()
