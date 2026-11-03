from openai import OpenAI
import os

# ==============================
# JARVIS AI ASSISTANT
# ==============================

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set."
    )

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are JARVIS, a highly intelligent personal AI assistant.

Your personality:
- Smart
- Polite
- Friendly
- Concise
- Natural
- Helpful

Always answer the user's question clearly.
"""

def ask_jarvis(question):

    response = client.responses.create(
        model="gpt-5-mini",
        instructions=SYSTEM_PROMPT,
        input=question
    )

    return response.output_text


# ==============================
# MAIN PROGRAM
# ==============================

print("================================")
print("        J.A.R.V.I.S")
print("================================")
print("Jarvis is online.")
print("Type 'exit' to close.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Jarvis: Goodbye, sir.")
        break

    try:
        answer = ask_jarvis(question)
        print("Jarvis:", answer)
        print()

    except Exception as error:
        print("Jarvis: I encountered an error.")
        print(error)