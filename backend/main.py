# ============================================================
# NOVA — main.py  (V2)
# This is Nova's main loop. It's intentionally short: all the
# real work happens in the other files.
#
#   voice.py    -> turns speech into text
#   commands.py -> turns text into a {"intent", "target", "query"} dict
#   router.py   -> turns that dict into an actual action
#   tts.py      -> speaks Nova's responses out loud
#
# main.py's only job is to connect these four steps in a loop.
# ============================================================

from voice import listen_for_command
from commands import clean_command
from router import route_command
from tts import speak

# Step 1: Greet the user when the program starts.
print("Hello, I am Nova. How can I help you today?")
speak("Hello, I am Nova. How can I help you today?")

# Step 2: Keep listening, understanding, and acting on commands
# until route_command() tells us to stop.
while True:
    # Step 3: Listen for speech. This returns the recognized
    # text, or None if nothing understandable was heard.
    raw_text = listen_for_command()

    # Step 4: If speech wasn't understood, skip everything below
    # and go back to listening again.
    if raw_text is None:
        continue

    # Step 5: Turn the raw text into a command dictionary, e.g.
    # {"intent": "open_application", "target": "chrome", "query": None}
    command = clean_command(raw_text)

    # Step 6: Hand that dictionary to the router, which figures
    # out which actions.py function to call and runs it. The
    # router already prints its own status messages (what it's
    # doing, errors, "I don't know that command yet.", etc.), so
    # main.py doesn't need to repeat any of that here.
    keep_running = route_command(command)

    # Step 7: route_command() only returns False for the "exit"
    # intent. When that happens, speak a goodbye — the router
    # already PRINTED "Nova: Goodbye!", but it doesn't speak
    # anything itself, so this adds the audio side without
    # duplicating any printed text — and then stop the loop.
    if not keep_running:
        speak("Goodbye!")
        break