# ============================================================
# NOVA — backend prototype
# This is the very first version of Nova's "brain".
# It listens to the microphone, cleans up what it heard, and
# prints the result — until you say "exit".
# ============================================================

from voice import listen_for_command
from commands import clean_command

# Step 1: Greet the user when the program starts.
print("Hello, I am Nova. How can I help you today?")

# Step 2: Keep asking for commands forever, until we choose to stop.
while True:
    # listen_for_command() uses the microphone and returns the
    # recognized speech as text — or None if nothing could be
    # understood.
    raw_command = listen_for_command()

    # Step 3: If speech wasn't understood, skip everything below
    # and go back to listening again.
    if raw_command is None:
        continue

    # Step 4: Clean up the raw text (lowercase, no punctuation,
    # wake word removed) before we do anything with it.
    command = clean_command(raw_command)

    # Step 5: Check if the user wants to quit.
    if command == "exit":
        print("Nova: Goodbye!")
        break  # break stops the while loop immediately

    # Step 6: If it wasn't "exit", just show the cleaned command.
    # (Later, this is where real command handling will go.)
    print(f"Nova: I received your command -> {command}")