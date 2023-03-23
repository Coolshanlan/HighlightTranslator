import requests
from time import sleep
from urllib.parse import quote
from json import loads
import tk as tk
import pyuseragents
import time

def get_translate(inputtext,sourcelanguage):
    result_dict = {}
    error_times=0
    while error_times<10:
      HEADERS = {
              "User-Agent": pyuseragents.random(),
              "Accept": "*/*",
              "Accept-Language": "en-US,en-GB; q=0.5",
              "Accept-Encoding": "gzip, deflate",
              "Content-Type": "application/json"
          }

      ChatGPT_api_URL = 'https://chatgpt-api.shn.hk/v1/'

      data={}
      data["model"] = "gpt-3.5-turbo"
      if sourcelanguage == 'en':
        pre_content = 'Be a translator.\ntranslate below content from English to Traditional\n\n'
      else:
        pre_content = 'Be a translator.\ntranslate below content from Traditional to English \n\n'

      data['messages'] = [{"role": "user", "content": f"{pre_content+inputtext}"}]
      try:
        session = requests.Session()
        req = requests.post(ChatGPT_api_URL,json=data,headers=HEADERS)
      except Exception:
        return None
      print(req.status_code == 200,req.status_code)
      if req.status_code == 200:
        answer = loads(req.text, strict=False)["choices"][0]["message"]["content"][2:]
        result_dict['result']=answer
        return result_dict
      else:
        error_times+=1
        time.sleep(0.5)
    return None

if __name__ == '__main__':
    #print(get_translate("And say mean things", "en","zh-TW"))
    print(get_translate("What is your mean active change over december for mar/apr/may?", sourcelanguage="en"))
