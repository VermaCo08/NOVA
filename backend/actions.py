# ============================================================
# NOVA — backend prototype
# This is the very first version of Nova's "brain".
# It does not understand commands yet — it just listens,
# and repeats back what you typed, until you say "exit".
# ============================================================

# Step 1: Greet the user when the program starts.
print("Hello, I am Nova. How can I help you today?")

# Step 2: Keep asking for commands forever, until we choose to stop.
while True:
    # input() pauses the program and waits for the user to type
    # something and press Enter. Whatever they type is returned
    # as text (a string), and we store it in the variable "command".
    command = input("You: ")

    # Step 3: Check if the user wants to quit.
    if command == "exit":
        print("Nova: Goodbye!")
        break  # break stops the while loop immediately

    # Step 4: If it wasn't "exit", just show what Nova received.
    # (Later, this is where real command handling will go.)
    print(f"Nova: I received your command -> {command}")