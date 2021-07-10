import re
from requests import get
import json
from urllib.parse import quote
import tk as tk
tk = tk.Token()

nottk=True

def get_translate_nottk(inputtext, sourcelanguage='auto',targetlanguage='tr'):
    global nottk
    #tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    sl = sourcelanguage
    tl = targetlanguage

    if not nottk:
        return get_translate(inputtext, sourcelanguage,targetlanguage)

    req = get(
        f"https://translate.google.com.tw/translate_a/single?&client=gtx&dt=t&sl={sl}&tl={tl}&hl={tl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=1791807&kc=1&q={urltext}")

    if req.status_code != 200:
        nottk=False
        return get_translate(inputtext, sourcelanguage,targetlanguage)

    req = req.text
    req = eval(req.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    if len(req[0]) > 1:
        translate_content = req[0][:-1]
    else:
        translate_content = req[0]

    result = [i[0] for i in translate_content]
    allresult = [{'type': i[0], 'words':i[1]} for i in req[1]]
    revise = req[7][1] if req[7] != [] else None
    detect_language= req[2]
    return result, allresult,detect_language,revise


def get_translate(inputtext, sourcelanguage='auto',targetlanguage='zh-TW'):
    tkid = tk.calculate_token(inputtext)
    urltext = quote(inputtext)
    sl = sourcelanguage
    tl = targetlanguage
    req = get(
        f"https://translate.google.com/translate_a/single?&client=webapp&dt=t&sl={sl}&tl={tl}&hl={tl}&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=1791807&kc=1&tk={tkid}&q={urltext}")
    req = req.text
    req = eval(req.replace('null', '""').replace('"""', '"').replace(
        'true', "True").replace('false', "False"))
    if len(req[0]) > 1:
        translate_content = req[0][:-1]
    else:
        translate_content = req[0]

    result = [i[0] for i in translate_content]
    allresult = [{'type': i[0], 'words':i[1]} for i in req[1]]
    revise = req[7][1] if req[7] != [] else None
    detect_language= req[2]
    return result, allresult,detect_language,revise


if __name__ == '__main__':
    #print(get_translate("And say mean things", "en","zh-TW"))
    print(get_translate_nottk("And say mean things", "en","zh-TW"))

# 目前了解：
# client: gtx, at 都不需要 ttk (容易被檔)
# client: webapp, t 需要 ttk (目前沒被檔過)
# t, webapp 翻譯類似
# gtx, at 翻譯類似
# 目前對於整句翻譯結果 webapp, t  與 網頁上不同步，我比較喜歡 gtx, at 翻譯版本感覺比較精確
# dt: 決定回傳結果的種類 t 單一翻譯 等等
# hl: 目前看起來沒用