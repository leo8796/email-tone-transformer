import gradio as gr

from prompts import build_email_prompt
from llm_client import rewrite_email_with_gemini


def rewrite_email(email: str, tone: str):
    if not email.strip():
        return "Please enter an email.", ""

    prompt = build_email_prompt(email=email, tone=tone)
    result = rewrite_email_with_gemini(prompt=prompt, tone=tone)

    rewritten_email = result.get("rewritten_email", "")
    key_changes = result.get("key_changes", [])

    key_changes_text = "\n".join([f"- {change}" for change in key_changes])

    return rewritten_email, key_changes_text


demo = gr.Interface(
    fn=rewrite_email,
    inputs=[
        gr.Textbox(
            label="Original Email",
            lines=8,
            placeholder="Paste your email here..."
        ),
        gr.Dropdown(
            choices=["professional", "polite", "concise", "friendly"],
            value="professional",
            label="Target Tone"
        ),
    ],
    outputs=[
        gr.Textbox(label="Rewritten Email", lines=8),
        gr.Textbox(label="Key Changes", lines=6),
    ],
    title="Email Tone Transformer",
    description="Rewrite emails into different tones using Python and the Gemini API."
)


if __name__ == "__main__":
    demo.launch()