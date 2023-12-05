from google.cloud import translate_v2 as translate
from openai import OpenAI
from openai.types.chat import ChatCompletion

from autoResponder import settings


def detect_language(text: str) -> str:
    """Return language short name"""
    translate_client = translate.Client()
    return translate_client.detect_language(text)["language"]


def translate_text(text: str, target_language: str = "en") -> str:
    """Returns a translation of the input text into the specified
    target language using the Google Cloud Translation API"""
    translate_client = translate.Client()
    translation = translate_client.translate(text, target_language=target_language)
    return translation.get("translatedText")


def generate_best_response(question: str, answer_options: list[str, ...]) -> int:
    """Return index of best answer or -1 if best answer does not exist"""
    answers = "\n".join(
        [f"{i + 1}. {answer}" for i, answer in enumerate(answer_options)]
    )
    prompt = f"""
    Choose the number of the correct answer, if there is no answer to the question, send "0".
    For example:
    Answer: 1

    Question: {question}
    Options: 
    {answers}
    Answer:
    """

    model_reply = _ask_open_ai(prompt).choices[0].message.content

    try:
        best_answer = int(model_reply[0])
        if 0 <= best_answer <= 3:
            return best_answer - 1
    except ValueError:
        print(
            f"The Chat GPT answered incorrectly! (A number was expected, but it came: {model_reply})"
        )
    return 1


def is_question(text: str) -> bool:
    """Return True if text is question, else return False"""
    prompt = f"""
    Determine if it is a question, if it is a question, send 1, and if not, send 0.
    Text: {text}
    """

    model_reply = _ask_open_ai(prompt).choices[0].message.content

    try:
        return _to_bool(model_reply)
    except ValueError:
        print(
            f"The Chat GPT answered incorrectly! (A number [0 | 1] was expected, but it came: {model_reply})"
        )
    return False


def _ask_open_ai(prompt: str, max_tokens: int = 2) -> ChatCompletion:
    """Return OpenAI model reply"""
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL, messages=messages, max_tokens=max_tokens
    )
    return response


def _to_bool(val: str) -> bool:
    """Return True or False or exception"""
    if val.lower() in ["1", "ok", "yes", "y"]:
        return True
    if val.lower() in ["0", "nok", "no", "n"]:
        return False
    raise ValueError(f"Invalid given value '{val}' (expected a boolean)")
