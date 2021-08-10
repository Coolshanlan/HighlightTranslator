from requests import get
from time import sleep
from urllib.parse import quote
from json import loads
import tk as tk
import pyuseragents
tk = tk.Token()
class GoogleTranslator():

    def __init__(self,name,base_url,general_params):
        """Google Translator can support multiple source."""
        self.name=name
        self.url = base_url
        self.base_parames=general_params
        self.client_list={'nottk':['gtx','at'],'ttk':['webapp'],'clients5':['dict-chrome-ex']}
        self.client_list_state=self.client_list.copy()

    @staticmethod
    def convert_qtext(text):
        return quote(text)

    @staticmethod
    def calculate_tkid(text):
        return tk.calculate_token(text)

    def __call__(self,input_text, sourcelanguage='auto',targetlanguage='tr',ttk_enable=False):
        HEADERS = {
            "User-Agent": pyuseragents.random(),
            "Accept": "*/*",
            "Accept-Language": "en-US,en-GB; q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; application/json; charset=UTF-8",
            "Connection": "keep-alive"
        }
        #text = self.convert_qtext(input_text)
        self.parames=general_params
        self.parames['sl']=sourcelanguage
        self.parames['tl']=targetlanguage
        self.parames['hl']=targetlanguage
        self.parames['q']=input_text
        self.parames['ie']='UTF-8'
        self.parames['oe']='UTF-8'
        mode=''
        if self.name == 'clients5' and not ttk_enable:
            mode='clients5'
        elif ttk_enable:
            mode = 'ttk'
            tkid = self.calculate_tkid(input_text)
            self.parames['tk']=tkid
        else:
            mode='nottk'
        #print(mode,self.client_list[mode])
        self.parames['client']=self.client_list[mode][0]

        try:
            req = get(self.url,params=self.parames,headers=HEADERS)
            status_code = req.status_code
        except Exception :
            return 400,(None,None,None,None)

        if status_code == 400:
            return status_code,(None,None,None,None)

        while  status_code != 200:
            self.client_list[mode].pop(0)
            if self.client_list[mode] == []:
                return False,(None,None,None,None)
            self.parames['client']=self.client_list[mode][0]
            req = get(self.url,params=self.parames,headers=HEADERS)
            status_code = req.status_code

        return status_code,self.parser(req.text)


    def parser(self,request_text):
        req = loads(request_text)

        detect_language = req['ld_result']['extended_srclangs'][0]#req['src']
        if self.name  == 'clients5':
            req['sentences']=req['sentences'][:-1]
        result = [ trans['trans'] for trans in req['sentences']]
        if 'spell' in req and 'spell_res' in req['spell']:
            revise=req['spell']['spell_res']
        else:
            revise=None

        if 'dict' in req:
            dict_list = req['dict']
            allresult = [{'pos': dic['pos'],'terms':dic['terms'] } for dic in dict_list]
        else:
            allresult=[]

        return result, allresult,detect_language,revise

#service
service_dict={
    'com_apis':'https://translate.googleapis.com/translate_a/single',
    'clients5':'https://clients5.google.com/translate_a/t',
    'com':'https://translate.google.com/translate_a/single',
    'tw':'https://translate.google.com.tw/translate_a/single',
    'cn':'https://translate.google.cn/translate_a/single',
}

#params = {"dt": ["t", "bd", "ex", "ld", "md", "qca", "rw", "rm", "ss", "t", "at"], "client": "gtx", "q": text, "hl": destination_language, "sl": source_language, "tl": destination_language, "dj": "1", "source": "bubble"}
general_params = {"dt": ["t", "bd", "qca","t", "at"],"dj": "1"}
translator_list = [GoogleTranslator(name,url,general_params) for name,url in service_dict.items()]

translator_idx=0
ttk_enable=False

RETRY_TIME=60*5

def get_translate(inputtext, sourcelanguage='auto',targetlanguage='zh-TW'):
    global ttk_enable,translator_idx,RETRY_TIME

    status,(result, allresult,detect_language,revise)=translator_list[translator_idx](inputtext, sourcelanguage,targetlanguage,ttk_enable)

    if status == 200:
        return result, allresult,detect_language,revise
    elif status == 400:
        return None, None,None,None
    else:
        translator_idx +=1
        if translator_idx < len(translator_list):
            return get_translate(inputtext, sourcelanguage,targetlanguage)
        elif not ttk_enable:
            translator_idx=0
            ttk_enable=True
            return get_translate(inputtext, sourcelanguage,targetlanguage)
        else:
            sleep(RETRY_TIME)
            translator_idx=0
            ttk_enable=False
            return get_translate(inputtext, sourcelanguage,targetlanguage)

if __name__ == '__main__':
    #print(get_translate("And say mean things", "en","zh-TW"))
    print(get_translate("And say mean things", "en","zh-TW"))



# 目前了解：
# client: gtx, at 都不需要 ttk (容易被檔)
# client: webapp, t 需要 ttk (目前沒被檔過)
# t, webapp 翻譯類似
# gtx, at 翻譯類似
# 目前對於整句翻譯結果 webapp, t  與 網頁上不同步，我比較喜歡 gtx, at 翻譯版本感覺比較精確
# dt: 決定回傳結果的種類 t 單一翻譯 等等
# hl: 目前看起來沒用

# dt parameter:

# t - translation of source text
# at - alternate translations
# rm - transcription / transliteration of source and translated texts
# bd - dictionary, in case source text is one word (you get translations with articles, reverse translations, etc.)
# md - definitions of source text, if it's one word
# ss - synonyms of source text, if it's one word
# ex - examples
# rw - See also list.
# dj - Json response with names. (dj=1)
