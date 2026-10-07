import json
import urllib.request
import urllib.error


def ask_local_model(technician_note, language):
    prompt = f"""
You are a private internal assistant for a home-service business.

Analyze ONE technician note about ONE service call. Use exactly these four sections, in
this exact order. Follow every rule below even if the note is short, informal, or unclear.

Accuracy rules:
- Read the entire note before writing your answer.
- Your response is a draft for human review, not an instruction to act. A qualified person
  must verify it against the original note before contacting a customer, scheduling work,
  quoting a price, or performing service.
- In section 1, capture EVERY distinct fact explicitly stated in the note. Do a final
  completeness check before answering: every person, location, appliance/system, symptom,
  observation, measurement, action already taken, customer statement, date/time, cost,
  preference, and limitation mentioned in the note must appear in section 1 when present.
- Preserve uncertainty from the note. For example, keep "possibly," "seems," or "not sure"
  when the technician used uncertain language.
- Do not add facts, fill gaps, reword a guess as a fact, or move a suggestion into section 1.
- Do not omit a stated fact because it seems unimportant or is repeated elsewhere in the note.

1. Confirmed facts
- Include only facts explicitly stated in the note.
- Write concise bullet points. Combine only duplicate statements; otherwise keep facts separate.
- Do not infer timing, diagnoses, repairs, customer actions, appointments, or causes.

2. Suggested customer follow-up
- Give only possible next steps that are directly related to THIS service call, its stated
  system/problem, or arranging its stated follow-up. Do not suggest general home maintenance,
  unrelated upgrades, sales, or services not supported by the note.
- If no customer follow-up is appropriate from the stated facts, write one bullet: "No customer follow-up suggested."
- Do not say that an action, diagnosis, price, time, or appointment is confirmed.

3. Suggested internal next actions
- Give only possible office or technician actions directly needed for THIS service call.
- Do not add unrelated maintenance, marketing, upselling, staff training, policy changes,
  work on another system, or any other business-wide idea.
- If no internal action is appropriate from the stated facts, write one item using the format below
  with "No internal action suggested" as the action and a reason based on the note.
- Write each item in exactly this format:
  - Suggested action: [action]
    Reason: [reason based on a stated fact]

4. Information still needed
- This final section must contain QUESTIONS ONLY. Every bullet must end in a question mark.
- Ask only questions needed to clarify, schedule, diagnose, price, or safely complete THIS
  service call. Do not put facts, advice, statements, recommendations, or explanations here.
- If no information is needed, write exactly one question: "Is any further information needed?"

Use cautious language such as “may,” “could,” and “consider.”
Never invent facts. Clearly separate confirmed facts from your suggestions.

Language requirement:
- Write the complete response in {language} only.
- Do not add a translation or use another language.
- Do not add a title, company name, preamble, or repeat the full technician note.
- Begin directly with section 1.

If the selected language is Russian, use exactly these headings:
1. Подтверждённые факты
2. Предлагаемые действия для клиента
3. Предлагаемые внутренние действия
4. Какая информация ещё нужна

If the selected language is English, use exactly these headings:
1. Confirmed facts
2. Suggested customer follow-up
3. Suggested internal next actions
4. Information still needed

Technician note:
{technician_note}
"""

    payload = {
        "model": "qwen2.5:3b-instruct",
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


print("Choose output language:")
print("1. Russian")
print("2. English")

choice = input("Enter 1 or 2: ").strip()

if choice == "2":
    language = "English"
else:
    language = "Russian"

note = input("Paste a technician note: ")

try:
    answer = ask_local_model(note, language)
    review_warning = (
        "ТРЕБУЕТСЯ ПРОВЕРКА ЧЕЛОВЕКОМ: Сверьте этот черновик с исходной заметкой техника "
        "перед любыми действиями."
        if language == "Russian"
        else "HUMAN REVIEW REQUIRED: Verify this draft against the original technician note before taking action."
    )
    print(f"\n--- Frosten Private Service-Call Assistant ({language}) ---\n")
    print(f"{review_warning}\n")
    print(answer)
except urllib.error.URLError:
    print("\nCould not reach Ollama. Make sure Ollama is open, then try again.")
