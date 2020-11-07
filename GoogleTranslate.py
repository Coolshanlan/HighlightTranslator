from requests import get
import json
from urllib.parse import quote
import tk as tk
tk = tk.Token()


def get_translate_nottk(inputtext, language):
    # tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    if language == "To Chinese":
        tl = "zh-TW"
        sl = "auto"  # "en"
    else:
        sl = "auto"  # "zh-TW"
        tl = "en"
    r = get(
        f"http://translate.google.cn/translate_a/single?client=gtx&dt=t&ie=UTF-8&oe=UTF-8&sl=auto&tl={tl}&q={urltext}")
    a = r.text
    a = eval(a.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    b = a[0][0]
    result = b[0]
    # allresult = [{'name': i[0], 'value':i[1]} for i in a[1]]
    return result, []


def get_translate(inputtext, language):
    tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    if language == "To Chinese":
        tl = "zh-TW"
        sl = "auto"  # "en"
    else:
        sl = "auto"  # "zh-TW"
        tl = "en"
    r = get(
        f"https://translate.google.com.tw/translate_a/single?client=webapp&sl={sl}&tl={tl}&hl=zh-TW&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=1791807&kc=1&tk={tkid}&q={urltext}")
    a = r.text
    a = eval(a.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    if len(a[0]) > 1:
        b = a[0][:-1]
    else:
        b = a[0]
    result = [i[0] for i in b]
    allresult = [{'name': i[0], 'value':i[1]} for i in a[1]]
    return result, allresult


if __name__ == '__main__':
    get_translate("看書", "To Chinese")
