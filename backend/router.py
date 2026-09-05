# ============================================================
# NOVA — router.py  (V2)
# This file's only job: take the dictionary returned by
# commands.clean_command() and call the matching function in
# actions.py.
#
# commands.py decides WHAT the user wants (the intent).
# router.py decides WHICH FUNCTION that maps to.
# actions.py actually DOES it.
#
# Keeping this as its own file (instead of putting all of this
# logic into main.py) means main.py can stay a short, simple
# loop, and all the "which intent goes to which function"
# decisions live in exactly one place.
# ============================================================

import actions


# ------------------------------------------------------------
# "open_application" needs to call one of FOUR separate
# functions in actions.py — there's no single generic
# "open_application(name)" function there, so this dictionary
# maps each known target to the actual function that handles it.
#
# Note: "brave" is a target commands.py can recognize, but
# actions.py doesn't have an open_brave() function yet, so it's
# deliberately left out of this dictionary. See the
# open_application handling below for how that's dealt with
# safely, without inventing a function that doesn't exist.
# ------------------------------------------------------------
OPEN_APPLICATION_ACTIONS = {
    "chrome": actions.open_chrome,
    "brave": actions.open_brave,
    "notepad": actions.open_notepad,
    "calculator": actions.open_calculator,
    "file_explorer": actions.open_file_explorer,
}

# ------------------------------------------------------------
# "open_website" gives us a short target name like "youtube",
# but actions.open_website() needs a full URL. This dictionary
# is what turns one into the other.
# ------------------------------------------------------------
WEBSITE_URLS = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://www.github.com",
}


def route_command(command):
    """
    Takes the dictionary produced by clean_command(), e.g.:
        {"intent": "open_application", "target": "chrome", "query": None}

    ...and calls whichever actions.py function matches its
    "intent". Some intents also need "target" or "query" to
    know exactly what to do.

    Returns True if Nova should keep running, or False if Nova
    should stop (this only happens for the "exit" intent).
    main.py can use this later like:
        keep_running = route_command(command)
        if not keep_running:
            break
    """

    intent = command["intent"]
    target = command["target"]
    query = command["query"]

    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------
    if intent == "exit":
        print("Nova: Goodbye!")
        return False  # tells main.py to stop the loop

    # --------------------------------------------------------
    # Open an application
    # --------------------------------------------------------
    if intent == "open_application":
        open_function = OPEN_APPLICATION_ACTIONS.get(target)

        if open_function is None:
            # This is where "brave" ends up for now — a target
            # commands.py understands, but actions.py doesn't
            # have a matching function for yet.
            print(f"Nova: I understand 'open {target}', but I don't have a way to do that yet.")
        else:
            open_function()

        return True

    # --------------------------------------------------------
    # Close an application
    # --------------------------------------------------------
    if intent == "close_application":
        # actions.close_application() already accepts any app
        # name and safely handles ones it doesn't recognize, so
        # we can just pass the target straight through.
        actions.close_application(target)
        return True

    # --------------------------------------------------------
    # Open a folder
    # --------------------------------------------------------
    if intent == "open_folder":
        # Same idea as close_application() — actions.open_folder()
        # already handles an unrecognized folder name safely.
        actions.open_folder(target)
        return True

    # --------------------------------------------------------
    # Open a website
    # --------------------------------------------------------
    if intent == "open_website":
        url = WEBSITE_URLS.get(target)

        if url is None:
            print(f"Nova: I don't have a website saved for '{target}'.")
        else:
            actions.open_website(url)

        return True

    # --------------------------------------------------------
    # Search Google / YouTube
    # --------------------------------------------------------
    if intent == "search_google":
        actions.search_google(query)
        return True

    if intent == "search_youtube":
        actions.search_youtube(query)
        return True

    if intent == "search_brave":
        actions.search_brave(query)
        return True
    # --------------------------------------------------------
    # Volume control
    # --------------------------------------------------------
    if intent == "increase_volume":
        actions.increase_volume()
        return True

    if intent == "decrease_volume":
        actions.decrease_volume()
        return True

    if intent == "mute_volume":
        actions.mute_volume()
        return True

    # --------------------------------------------------------
    # Screenshot
    # --------------------------------------------------------
    if intent == "take_screenshot":
        # actions.take_screenshot() already prints its own
        # success/failure message, so there's nothing extra to
        # do here besides calling it.
        actions.take_screenshot()
        return True

    # --------------------------------------------------------
    # System information
    # --------------------------------------------------------
    if intent == "get_time":
        current_time = actions.get_current_time()
        print(f"Nova: It's {current_time}.")
        return True

    if intent == "get_battery":
        battery_percent = actions.get_battery_level()

        if battery_percent is None:
            print("Nova: I couldn't detect a battery on this device.")
        else:
            print(f"Nova: Battery is at {battery_percent} percent.")

        return True

    # --------------------------------------------------------
    # Lock computer
    # --------------------------------------------------------
    if intent == "lock_computer":
        actions.lock_computer()
        return True

    # --------------------------------------------------------
    # Unknown command — commands.py already puts the cleaned
    # text into "query" for us in this case, but we don't need
    # to show it back to the user; a clear, simple message is
    # enough.
    # --------------------------------------------------------
    print("Nova: I don't know that command yet.")
    return True


# ============================================================
# Optional: a small manual test you can run directly with
#     python router.py
# This does NOT use the microphone — it just feeds a few typed
# example commands through clean_command() and route_command()
# so you can check the routing works before wiring it into
# main.py.
# ============================================================
if __name__ == "__main__":
    from commands import clean_command

    test_phrases = [
        "Nova, open Chrome",
        "Nova, open Brave",
        "Nova, close Chrome",
        "Nova, open Downloads",
        "Nova, search Google for python tutorials",
        "Nova, what's the time",
        "Nova, exit",
    ]

    for phrase in test_phrases:
        print(f"\n> {phrase}")
        parsed_command = clean_command(phrase)
        route_command(parsed_command)