# Copy Translator
You can copy or highlight/select sentence or word in anywhere or take screenshot for the text then this tool will automatic get Google Translate or Cambridge dictionary result and then display to you.
> Only support **Chinese to English** and **English to Chinese**

Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Copy Translator Github](https://github.com/Coolshanlan/Copy-Translator)

## 功能介紹
### Translation method
- Take screenshot for the text
- Copy
- Highlight/Select
### Top checkbox
如果有勾選，程式會置頂，不會被其他程式蓋住

如果沒有勾選，程式會在特訂時間後自動跑到最下層隱藏起來
> defult 5 sec, you can modify hide variable in config.json
### Select checkbox
勾選後開啟選取自動翻譯功能
### Change Language
Only support **Chinese to English** and **English to Chinese**
### Change dictionary
Only support **Google** and **Cambridge**

## Config.json
- hide -> 控制自動消失時間
- font-size -> 調整字體大小
- doubleclick -> 判斷是否為雙擊的時間間隔(幾秒內點兩下算是雙擊)
- select -> 長壓幾秒判斷為選取
