import json
import urllib.request
import urllib.error

def ask_local_model(technician_note):
	prompt = f"""
You are a private internal assistant for a home-service business.

Read the techinican note below. Return these three sections:
1. Job summary
2. Customer-facing next steps
3. Internal office follow-up

Use concise bullet points. Do not invent facts, diagnoses prices, or appointments.

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
