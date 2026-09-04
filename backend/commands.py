# ============================================================
# NOVA — commands.py
# This file's only job: take the raw text that voice.py heard,
# and clean it up into a simple, predictable command string.
# It does not decide what the command DOES — that comes later.
# ============================================================

import string


def clean_command(text):
    """
    Takes raw recognized speech (or typed text) and returns a
    clean, lowercase command with the wake word and extra
    punctuation/spacing removed.

    Example:
        "Nova, open Chrome"  -> "open chrome"
        "NOVA open Chrome"   -> "open chrome"
        "open Chrome"        -> "open chrome"
    """

    # Step 1: Make everything lowercase so "Nova", "NOVA", and
    # "nova" are all treated the same way.
    cleaned = text.lower()

    # Step 2: Remove punctuation (commas, periods, etc).
    # str.maketrans("", "", string.punctuation) builds a
    # translation table that maps every punctuation character
    # to nothing, and translate() applies it.
    cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))

    # Step 3: Split the text into individual words. This also
    # gets rid of extra/duplicate spaces automatically, since
    # split() with no arguments splits on any amount of whitespace.
    words = cleaned.split()

    # Step 4: Remove the wake word "nova" if it's the first word.
    # We only check the first word so that a command like
    # "turn on nova mode" (if that ever existed) wouldn't have
    # its meaning changed by accident.
    if words and words[0] == "nova":
        words = words[1:]  # keep every word except the first

    # Step 5: Join the remaining words back into one string,
    # separated by single spaces.
    command = " ".join(words)

    return command