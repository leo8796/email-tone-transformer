# Email Tone Transformer

Email Tone Transformer is a small AI-powered Python tool that rewrites emails into different tones using the Gemini API.

The project takes a user's original email and selected tone, then returns a rewritten version of the email together with key changes made by the model.

## Features

- Rewrite emails into different tones
- Supported tones:
  - professional
  - polite
  - concise
  - friendly
- Preserve the original meaning of the email
- Avoid inventing new facts
- Show key changes made by the model
- Store API keys securely with `.env`
- Keep the project structure simple and beginner-friendly

## Tech Stack

- Python
- Google Gemini API
- google-genai
- python-dotenv
- JSON

## Project Structure

```text
01-email-tone-transformer/
├── app.py
├── prompts.py
├── llm_client.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
└── examples/
    ├── input_example.txt
    └── output_example.txt
```

## How It Works

The app follows a simple LLM application workflow:

```text
User email
→ Tone selection
→ Prompt construction
→ Gemini API call
→ Model response
→ Display rewritten email and key changes
```

The project is split into three main Python files:

- `app.py` handles the command-line user flow.
- `prompts.py` builds the prompt sent to Gemini.
- `llm_client.py` handles the Gemini API call and response parsing.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/email-tone-transformer.git
cd email-tone-transformer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If your system uses `python3`:

```bash
python3 -m pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit your real `.env` file to GitHub.

### 4. Run the app

```bash
python app.py
```

If your system uses `python3`:

```bash
python3 app.py
```

If you are using the local virtual environment directly:

```bash
./.venv/bin/python app.py
```

## Example Input

```text
Tone: friendly

Original email:
hey professor,
i can't finish the assignment today.
can i get more time?
```

## Example Output

```text
Rewritten Email
============================================================
Dear Professor,

I hope you're having a good week.

I'm writing to politely request an extension for the assignment that's due today. Unfortunately, I won't be able to complete it by the current deadline.

Would it be possible to get a bit more time to finish it up? Please let me know if an extension is an option.

Thank you for your understanding.

Best regards,

============================================================
Key Changes
============================================================
- Changed the casual greeting to a more respectful and warm one.
- Rephrased the direct statement of inability to complete the assignment into a polite explanation.
- Transformed the direct question for more time into a polite and natural request.
- Added a polite closing and sign-off.
```

## Example Files

Example input and output are also included in the `examples/` folder:

```text
examples/input_example.txt
examples/output_example.txt
```

## What I Learned

Through this project, I practiced:

- Calling an LLM API from Python
- Managing API keys with environment variables
- Using a `.env` file safely
- Designing prompts for controlled rewriting
- Asking an LLM for structured output
- Handling model responses in a Python app
- Organizing a small AI project into multiple files
- Using Git and GitHub for project version control

## Limitations

- The app currently runs in the terminal only.
- The model output may occasionally need additional formatting cleanup.
- The app does not currently have a web interface.
- It supports a small fixed set of tones.

## Future Improvements

- Add a simple Gradio web interface
- Add more tone options
- Improve structured JSON reliability
- Add before-and-after comparison
- Support multiple LLM providers such as OpenAI or Claude
- Add automated tests
- Add deployment instructions

## Security Note

This project uses a `.env` file to store the Gemini API key locally.

The `.gitignore` file is configured to prevent `.env` from being uploaded to GitHub.

Only `.env.example` should be committed.