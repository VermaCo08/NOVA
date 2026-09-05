from ollama import chat


conversation = [
    {
        "role": "system",
        "content": (
            "You are Nova, a helpful personal AI assistant. "
            "Respond naturally, clearly, and concisely. "
            "You are currently only a conversational assistant. "
            "Do not claim to have performed actions on the computer."
        ),
    }
]


def ask_brain(user_text):
    conversation.append(
        {
            "role": "user",
            "content": user_text,
        }
    )

    response = chat(
        model="qwen3:4b",
        messages=conversation,
    )

    reply = response.message.content

    conversation.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )

    return reply


if __name__ == "__main__":
    print("Nova: Conversation test started.")

    reply = ask_brain("My favorite programming language is Python.")
    print(f"Nova: {reply}")

    reply = ask_brain("What is my favorite programming language?")
    print(f"Nova: {reply}")