# https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/good
from requests import get, post
from urllib.parse import quote
from bs4 import BeautifulSoup


def get_translate(inputtext):
    urltext = quote(inputtext.replace('\n',' '))
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    r = get(
        f"https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/{urltext}", headers=headers)
    a = BeautifulSoup(r.content,"html.parser")
    a = a.find_all("div", class_="pr entry-body__el")
    if len(a) == 0:
        return "", ""
    allresult = []

    for i in a:
        allresult.append({'pos': "", 'terms': []})
        name = i.find("div", class_="posgram dpos-g hdib lmr-5").text.replace('[CorU]', '').replace('[c]','').replace('[IorT]', '').replace('[ T ]', '').replace(' ', '').replace('adverb', '副詞').replace('verb', "動詞").replace('preposition', '介系詞').replace(
            'pronoun', '代名詞').replace('noun', "名詞").replace('adjective', '形容詞').replace('conjunction', "連接詞").replace('suffix', '字  尾').replace('determiner', '限定詞').replace('prefix', '字  首')
        allresult[len(allresult)-1]['pos'] = name
        for ii in i.find_all("span", class_="trans dtrans dtrans-se break-cj"):
            translist = ii.text.replace(
                ',', '；').replace('，', '；').split('；')[:2]
            for t in translist:
                allresult[len(allresult)-1]['terms'].append(t)
    result = allresult[0]["terms"][:1]
    return result, allresult

if __name__ == "__main__":
    print(get_translate("regret"))
