from requests import get
import json
from urllib.parse import quote
import tk as tk
tk = tk.Token()


def get_translate_nottk(inputtext, sourcelanguage='auto',targetlanguage='tr'):
    # tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    sl = sourcelanguage
    tl = targetlanguage

    r = get(
        f"http://translate.google.cn/translate_a/single?client=gtx&dt=t&ie=UTF-8&oe=UTF-8&sl={sl}&tl={tl}&q={urltext}")
    a = r.text
    a = eval(a.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    if len(a[0]) > 1:
        b = a[0]
    else:
        b = a[0]
    result = [i[0] for i in b]
    allresult = [{'name': i[0], 'value':i[1]} for i in a[1]]
    return result, []


def get_translate(inputtext, sourcelanguage='auto',targetlanguage='zh-TW'):
    tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    sl = sourcelanguage
    tl = targetlanguage
    req = get(
        f"https://translate.google.com/translate_a/single?client=webapp&sl={sl}&tl={tl}&hl={tl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=1791807&kc=1&tk={tkid}&q={urltext}")
    req = req.text
    req = eval(req.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    if len(req[0]) > 1:
        b = req[0][:-1]
    else:
        b = req[0]

    result = [i[0] for i in b]
    allresult = [{'type': i[0], 'words':i[1]} for i in req[1]]

    detect_language= req[2] if sl == 'auto' else None
    return result, allresult,detect_language


if __name__ == '__main__':
    # print(get_translate("工具", "zh-TW","en"))
    print(get_translate("工具", "auto","en"))
