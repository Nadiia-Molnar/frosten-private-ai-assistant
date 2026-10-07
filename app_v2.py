import json
import urllib.request
import urllib.error


def ask_local_model(technician_note):
    prompt = f"""
You are a private internal assistant for a home-service business.

Analyze the technician note using this exact format:

1. Confirmed facts
- Include only information explicitly stated in the note.

2. Suggested customer follow-up
- Give useful possible next steps for the customer.
- Do not say that an action, diagnosis, price, time, or appointment is confirmed.

3. Suggested internal next actions
- Give useful possible next steps for the office or technician.
- Include a short “Reason:” for each suggestion.

4. Information still needed
- List questions that should be answered before the business acts.

Use cautious language such as “may,” “could,” and “consider.”
Never invent facts. Clearly separate confirmed facts from your suggestions.

Technician note:
{technician_note}
"""

    payload = {
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    }

    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]


note = input("Paste a technician note: ")

try:
    answer = ask_local_model(note)
    print("\n--- Frosten Private Service-Call Assistant ---\n")
    print(answer)
except urllib.error.URLError:
    print("\nCould not reach Ollama. Make sure Ollama is open, then try again.")
