import requests
from libretranslatepy import LibreTranslateAPI

lt = LibreTranslateAPI("https://translate.terraprint.co/")

def translate_word(word):
    return lt.translate(word, "en", "ko")

def get_sentence_examples(word):
    url = f"https://api.sentencestack.com/v1/sentences"
    params = {"q": word}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        sentences = response.json().get("sentences", [])
        return [sentence["sentence"] for sentence in sentences]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
