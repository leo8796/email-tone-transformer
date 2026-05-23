from prompts import TONE_DESCRIPTIONS, build_email_prompt
from llm_client import rewrite_email_with_gemini


def choose_tone() -> str:
    tones = list(TONE_DESCRIPTIONS.keys())

    print("\nChoose a tone:")
    for index, tone in enumerate(tones, start=1):
        print(f"{index}. {tone}")

    choice = input("\nEnter a number: ").strip()

    if not choice.isdigit():
        print("Invalid choice. Defaulting to professional.")
        return "professional"

    choice_index = int(choice) - 1

    if choice_index < 0 or choice_index >= len(tones):
        print("Invalid choice. Defaulting to professional.")
        return "professional"

    return tones[choice_index]


def get_email_input() -> str:
    print("\nPaste your email below.")
    print("When finished, press Enter on an empty line:\n")

    lines = []

    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    return "\n".join(lines).strip()


def display_result(result: dict) -> None:
    print("\n" + "=" * 60)
    print("Rewritten Email")
    print("=" * 60)
    print(result.get("rewritten_email", "No rewritten email returned."))

    print("\n" + "=" * 60)
    print("Key Changes")
    print("=" * 60)

    key_changes = result.get("key_changes", [])

    if isinstance(key_changes, list):
        for change in key_changes:
            print(f"- {change}")
    else:
        print(key_changes)

    print("\n" + "=" * 60)


def main():
    print("Email Tone Transformer")

    email = get_email_input()

    if not email:
        print("No email entered. Please try again.")
        return

    tone = choose_tone()
    prompt = build_email_prompt(email=email, tone=tone)

    print("\nRewriting email with Gemini...\n")

    try:
        result = rewrite_email_with_gemini(prompt=prompt, tone=tone)
        display_result(result)
    except Exception as error:
        print(f"Something went wrong: {error}")


if __name__ == "__main__":
    main()