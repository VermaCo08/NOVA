import pyttsx3


def speak(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    except Exception as error:
        print(f"Nova: I couldn't speak that out loud -> {error}")