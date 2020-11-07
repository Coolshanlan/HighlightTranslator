# https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/good
from requests import get, post
from urllib.parse import quote
from bs4 import BeautifulSoup


def get_translate(inputtext):
    urltext = quote(inputtext)
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = get(
        f"https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{urltext}", headers=headers)
    a = BeautifulSoup(r.content)
    a = a.find_all("div", class_="pr entry-body__el")
    if len(a) == 0:
        return "", ""
    allresult = []
    # allresult = [
    #     {'name': i.find("span", class_="pos dpos").text.replace('adverb', '副詞').replace('verb', "動詞").replace('preposition', '介系詞').replace('pronoun', '代名詞').replace('noun', "名詞").replace('adjective', '形容詞').replace('suffix', '字  尾').replace('determiner', '限定詞').replace('prefix', '字  首'), 'value': [(ii.find("span", class_="trans dtrans dtrans-se").text.replace(',', '；').split('；')[:1] for ii in i.find_all('div', 'pr dsense '))]} for i in a]
    for i in a:
        allresult.append({'name': "", 'value': []})
        name = i.find("div", class_="posgram dpos-g hdib lmr-5").text.replace('[CorU]', '').replace('[IorT]', '').replace('[ T ]', '').replace(' ', '').replace('adverb', '副詞').replace('verb', "動詞").replace('preposition', '介系詞').replace(
            'pronoun', '代名詞').replace('noun', "名詞").replace('adjective', '形容詞').replace('conjunction', "連接詞").replace('suffix', '字  尾').replace('determiner', '限定詞').replace('prefix', '字  首')
        allresult[len(allresult)-1]['name'] = name
        for ii in i.find_all("span", class_="trans dtrans dtrans-se"):
            translist = ii.text.replace(
                ',', '；').replace('，', '；').split('；')[:2]
            for t in translist:
                allresult[len(allresult)-1]['value'].append(t)
    result = allresult[0]["value"][:1]
    return result, allresult


# def get_mul_translate(inputtext):
#     urltext = quote(inputtext)
#     post_data = {'_csrf': '9c4c57e2-3e9c-41c9-aac1-362b6218d025', "languageFrom": "english", "txtTrans": urltext,
#                  "languageTo": "chinese-traditional", "g-recaptcha-response": "03AGdBq27KWqYb89NNhTbC075r8n7Iub0mHxbGWmuze-cuUoTqQTZf_CI3qKhbFcSd7PePE_ka9sGVuQzSS8DIIMRb7ZVOh_BJCZx-gGTCuBGgly1KYcEuPp0LXuOYehE1EtMaVGPLTpu0EQ_dn3QIicmv1IwSZfBhkApAgoLRxY3fhkPYZG5SgSrwzNpr1E_W-UkweNaV7fTljsn8hbTAmP01bzV854dZrYB9t-tvMKZx5SgmOrrWVX84rd-f4Zyr74viEpxFbPn9WybRZGFTHeWJzSxjfkfqPKObsppxc2lnwoMNKJJ0PGZnWgj_Q6HLMiN4syAHyKAqXxmT7lefrt-sK4B7B8M_wkPVTVJCe5T4gsg1jOeWr0CXGHt0vMAmRODczxl0gTtyQlOLh7L-NNo7rntus7UhnyZYiywnzUJ9eV6R-HcS1mcFVfbjhYNgfU9ujB212XDOGbmSCt8OLmnujMvCnCocTqvtFkN4X8gFhYqqsHbLgn4"}
#     header = {
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
#         'Cache-Control': 'max-age=0',
#         'Connection': 'keep-alive',
#         'Content-Length': '618',
#         'Content-Type': 'application/x-www-form-urlencoded',
#         'Cookie': 'XSRF-TOKEN=9c4c57e2-3e9c-41c9-aac1-362b6218d025; _ga=GA1.3.8195694.1588437991; _gid=GA1.3.158360984.1588437991; amp-access=amp-YIe1NeWcInsfc6yu764flQ; preferredDictionaries="english-chinese-traditional,english-chinese-simplified,english,british-grammar"; _fbp=fb.1.1588437992217.123996796; __gads=ID=a212a477dc3076c9:T=1588437992:S=ALNI_Ma9wrElFRZ73UtjsXY9_nR6znQsQQ; ssc=6; tc=38; _gat=1',
#         'Host': 'dictionary.cambridge.org',
#         'Origin': 'https: // dictionary.cambridge.org',
#         'Referer': 'https: // dictionary.cambridge.org/zht/translate /',
#         'Sec-Fetch-Dest': 'document',
#         'Sec-Fetch-Mode': 'navigate',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-User': '?1',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
#     }
#     r = post(
#         f"https://dictionary.cambridge.org/zht/translate", data=post_data, headers=header)

#     a = BeautifulSoup(r.content)
#     a = a.find_all(
#         "div", class_="tc-bb translate-tool__result translate-english-spanish js-translator-result")
#     if len(a) == 0:
#         return "", ""
#     allresult = [
#         {'name': i.find_all("span", class_="pos dpos")[0].text.replace('adverb', '副詞').replace('verb', "動詞").replace('preposition', '介系詞').replace('noun', "名詞").replace('adjective', '形容詞').replace('suffix', '詞  尾'), 'value': i.find("span", class_="trans dtrans dtrans-se").text.replace('，', '；').split('；')} for i in a]
#     result = allresult[0]["value"][: 1]
#     return result, allresult


# print(get_translate("good"))
