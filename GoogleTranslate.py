import requests
import json
import urllib
import tk as tk

import os
tk = tk.Token()


def get_translate(inputtext, language):
    tkid = tk.calculate_token(inputtext)
    urltext = urllib.parse.quote(inputtext)
    if language == "English to Chinese":
        tl = "zh-TW"
        sl = "en"
    else:
        sl = "zh-TW"
        tl = "en"
    r = requests.get(
        f"https://translate.google.com.tw/translate_a/single?client=webapp&sl={sl}&tl={tl}&hl=zh-TW&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=1791807&kc=1&tk={tkid}&q={urltext}")
    a = r.text
    a = eval(a.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    b = a[0][:-1]
    result = [i[0] for i in b]
    allresult = [{'name': i[0], 'value':i[1]} for i in a[1]]
    return result, allresult
