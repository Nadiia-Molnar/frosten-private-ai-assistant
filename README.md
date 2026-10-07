# Frosten Private Service-Call Assistant

A small local assistant for organizing fictional home-service technician notes into clear, reviewable next steps.

It can produce responses in English or Russian and uses a local Ollama model.

## Important review notice

The assistant's output is a draft only. A person must review the original technician note before contacting a customer, scheduling service, giving a price, or taking other action.

## Requirements

- Python 3
- [Ollama](https://ollama.com/)
- The local model `qwen2.5:3b-instruct`

## Set up the local model

After Ollama is installed, download the model once:

```bash
ollama pull qwen2.5:3b-instruct
```

## Run the assistant

From the project folder, run:

```bash
python3 app_multilingual.py
```
## Privacy and safe use

- Use fictional technician notes or notes approved for this purpose.
- Do not enter real customer names, addresses, phone numbers, payment details, or other private information without explicit permission.
- Review every response against the original technician note before taking action.

## Limitations

The model may occasionally omit, misunderstand, or format information imperfectly. Its suggestions are not confirmed diagnoses, prices, repairs, or appointments.
