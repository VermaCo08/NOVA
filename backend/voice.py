# ============================================================
# NOVA — voice.py
# This file's only job: listen to the microphone, turn speech
# into text, and hand that text back to main.py.
# It does not decide what to DO with the text — that's main.py's job.
# ============================================================

import speech_recognition as sr


def listen_for_command():
    """
    Listens to the microphone, converts speech to text,
    and returns that text as a string.

    If the speech can't be understood, or something goes wrong,
    this returns None instead of crashing the program.
    """

    recognizer = sr.Recognizer()

    # "with" opens the microphone and guarantees it gets closed
    # properly afterward, even if something goes wrong.
    with sr.Microphone() as source:
        print("Nova: Listening...")

        # This briefly measures background noise so Nova can
        # tell the difference between silence and speech.
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            # Waits for you to start talking, then records until
            # you stop. timeout = how long to wait for speech to
            # start before giving up.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Nova: I didn't hear anything.")
            return None

    # At this point we have recorded audio — now we try to
    # convert it into text using Google's speech recognition API.
    try:
        text = recognizer.recognize_google(audio)
        print(f"Nova heard: {text}")
        return text

    except sr.UnknownValueError:
        # The audio was captured, but the speech wasn't clear
        # enough to turn into text.
        print("Nova: Sorry, I couldn't understand that.")
        return None

    except sr.RequestError:
        # This happens if there's no internet connection, since
        # recognize_google() needs to reach Google's servers.
        print("Nova: Speech service is unavailable right now.")
        return None