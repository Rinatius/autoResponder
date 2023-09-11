import os
import openai
import json

openai.api_key = "your_key"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/journal.json"
from google.cloud import translate_v2 as translate

UNIVERSAL_LANGUAGES = ["ar", "zh", "en", "fr", "de", "it", "ja", "ko", "da", "pl", "pt", "es", "th", "tr", "ru"]


def translate_text(text, target_language="en"):
    translate_client = translate.Client()
    detected_language = translate_client.detect_language(text)
    if detected_language in UNIVERSAL_LANGUAGES:
        return text
    translation = translate_client.translate(text, target_language=target_language)
    return translation["translatedText"]


# TODO rewrite code for question and answers
def get_gpt_response(comment):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content":
            f'''
    Output 3 answers in descending order that answer the question the best.  Question: Which country traditionally dominated the sport of snooker? Answer_1: Two professional Chinese snooker players have been banned for life and eight others suspended after being found guilty of match-fixing and other charges, the sport's governing body has announced., Answer_2: The punishment is the latest crisis to engulf professional sports in China which has seen a host of match-fixing scandals across multiple disciplines in recent years., Answer_3: Traditionally snooker was dominated by players from the United Kingdom, but in recent years has seen an influx of Chinese talent, with the sport soaring in popularity there.
  Input:
  {{
      "text":"Some example text"
  }}

  Output:
  {{
      Traditionally snooker was dominated by players from the United Kingdom, but in recent years has seen an influx of Chinese talent, with the sport soaring in popularity there.
      Two professional Chinese snooker players have been banned for life and eight others suspended after being found guilty of match-fixing and other charges, the sport's governing body has announced.
      The punishment is the latest crisis to engulf professional sports in China which has seen a host of match-fixing scandals across multiple disciplines in recent years.
  }}

  Input:
  {{
      "text": {comment}
  }}

  Output:
      Text: {comment}
  '''
                   }])
    response_json = json.dumps(completion)
    response_json = json.loads(response_json)
    return response_json