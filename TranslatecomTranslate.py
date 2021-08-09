from requests import get,post
from time import sleep
from urllib.parse import quote
from json import loads
import pyuseragents
from requests.models import Response
HEADERS = {
            "User-Agent": pyuseragents.random(),
            "Accept": "*/*",
            "Accept-Language": "en-US,en-GB; q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
class Translatecom:
  def __init__(self):
    self.url="https://www.translate.com/translator/ajax_translate"
    self.url_language='https://www.translate.com/translator/ajax_lang_auto_detect'


  def __call__(self,input_text,sourcelanguage='auto',targetlanguage='en'):
    try:
      detect_language=self.detect_language(input_text)
      if sourcelanguage == 'auto':
        sourcelanguage = detect_language
      req = post(self.url,headers=HEADERS,data={"text_to_translate": input_text,"source_lang": sourcelanguage,'translated_lang': targetlanguage})
      req = req.json()
      results = req['translated_text']
      return results,results,detect_language,None
    except Exception:
      return None,None,None,None


  def detect_language(self,input_text):
    req=post(self.url_language, data={"text_to_translate": input_text})
    req.raise_for_status()
    detect_language = req.json()['language']
    return detect_language

def get_translate(inputtext, sourcelanguage='auto',targetlanguage='zh-TW'):
    results,_,detect_language,_=translator(inputtext,sourcelanguage,targetlanguage)
    return [results],[],detect_language,None


translator=Translatecom()
def detect_language_transcom(input_text):
    url_language='https://www.translate.com/translator/ajax_lang_auto_detect'
    req=post(url_language, data={"text_to_translate": input_text})
    req.raise_for_status()
    detect_language = req.json()['language']
    return detect_language

def detect_language_bing(input_text):
    request = post(
            "https://api.reverso.net/translate/v1/translation",
            json={
                "input": input_text,
                "from": "zh",
                "to": "fra",
                "format": "text",
                "options": {
                    "origin": "reversodesktop",
                    "sentenceSplitter": False,
                    "contextResults": False,
                    "languageDetection": True
                }
            },
            headers={"Content-Type": "application/json; charset=UTF-8"}
        )
    # response = request.json()
    print(request.text)
    if request.status_code < 400:
        return response["languageDetection"]["detectedLanguage"]

if __name__ == '__main__':
  translator=Translatecom()
  print(detect_language_transcom('大家好'))
  print(get_translate('apply','auto','en'))