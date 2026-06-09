# Email Tone Transformer

Email Tone Transformer is a small AI-powered Python tool that rewrites emails into different tones using the Gemini API.

The project takes a user's original email and selected tone, then returns a rewritten version of the email together with key changes made by the model.

It supports both a terminal-based interface and a simple Gradio web interface.

## Features

- Rewrite emails into different tones
- Supported tones:
  - professional
  - polite
  - concise
  - friendly
- Preserve the original meaning of the email
- Avoid inventing new facts
- Return both the rewritten email and key changes
- Run from the terminal with `app.py`
- Run as a simple web app with `app_gradio.py`
- Store API keys securely with `.env`
- Keep the project structure simple and beginner-friendly

## Tech Stack

- Python
- Google Gemini API
- google-genai
- Gradio
- python-dotenv
- JSON parsing
- Git/GitHub

## Project Structure

```text
email-tone-transformer/
├── app.py
├── app_gradio.py
├── prompts.py
├── llm_client.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_NOTES.md
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
→ Output parsing
→ Display rewritten email and key changes
```

The project is split into four main Python files:

- `app.py` handles the command-line user flow.
- `app_gradio.py` provides the Gradio web interface.
- `prompts.py` builds the prompt sent to Gemini.
- `llm_client.py` handles the Gemini API call and response parsing.

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/leo8796/email-tone-transformer.git
cd email-tone-transformer
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Install dependencies

```bash
./.venv/bin/python -m pip install -r requirements.txt
```

If you are not using the local virtual environment, you can also install dependencies with:

```bash
pip install -r requirements.txt
```

or:

```bash
python3 -m pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit your real `.env` file to GitHub.

This project includes `.env.example` as a safe template.

## Running the App

### Option 1: Run the terminal version

```bash
./.venv/bin/python app.py
```

If you are not using the local virtual environment:

```bash
python3 app.py
```

### Option 2: Run the Gradio web version

```bash
./.venv/bin/python app_gradio.py
```

Then open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

The Gradio interface lets users paste an email, select a target tone, and view both the rewritten email and the key changes.

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

Example input and output are included in the `examples/` folder:

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
- Parsing model responses in a Python app
- Handling cases where the model response is not perfectly formatted
- Building both terminal and web-based interfaces
- Organizing a small AI project into multiple files
- Using Git and GitHub for project version control

## Limitations

- The app currently supports a small fixed set of tones.
- The model output may occasionally need additional formatting cleanup.
- The Gradio interface is currently designed for local demo use.
- The app depends on Gemini API availability and supported user location.

## Future Improvements

- Deploy the Gradio app online
- Add more tone options
- Improve structured JSON reliability
- Add before-and-after comparison
- Support multiple LLM providers such as OpenAI or Claude
- Add automated tests
- Add demo video and slides links
- Add project screenshots to the README

## Security Note

This project uses a `.env` file to store the Gemini API key locally.

The `.gitignore` file is configured to prevent `.env` from being uploaded to GitHub.

Only `.env.example` should be committed.