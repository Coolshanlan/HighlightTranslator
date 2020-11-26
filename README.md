# Copy Translator
You can copy or highlight/select sentence or word in anywhere or take screenshot for the text then this tool will automatic get Google Translate or Cambridge dictionary result and then show to you.


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Copy Translator Github](https://github.com/Coolshanlan/Copy-Translator)

[Download Zip](https://drive.google.com/file/d/1CbpNgjE-orV_lMsCHhLgwArKOLc_ZSAt/view?usp=sharing)

![](https://github.com/Coolshanlan/Copy-Translator/blob/master/image/demo01.gif)
## Requirement
``` python
python == 3.6
pyinstaller == 4.1
tk == 8.6
pynput == 1.6
pyautogui == 0.9
pytesseract == 0.3
```

## Features
### Translation method
- Take screenshot for the text
- Copy
- Highlight/Select
### Top checkbox
如果有勾選，程式會置頂，不會被其他程式蓋住

如果沒有勾選，程式會在特訂時間後自動跑到最下層隱藏起來
> default 5 sec, you can modify hide variable in config.json
### Select checkbox
勾選後開啟選取自動翻譯功能
### Change Language
Only support Chinese to English and English to Chinese
### Change dictionary
Only support Google and Cambridge

## Config.json
- hide -> 控制自動消失時間
  > default 8 sec
- font -> 字體
  > default Calibri
- font-size -> 調整字體大小
  > default 11
- doubleclick -> 判斷是否為雙擊的時間間隔(幾秒內點兩下算是雙擊)
  > default 0.3 sec
- select -> 長壓幾秒判斷為選取
  > default 0.3 sec
- googlenotttk -> google translate don't need ttk version
  > default 0
- longttk -> 如果是翻譯整個句子使用非ttk版本
  > default 0
- automaticchange -> 如果是翻譯單字自動切換成劍橋字典
  > default 0
- restructureSentences -> 自動分辨上下句是否為同一句子
  > default 1

## How to use
```
pip install -r requirements.txt
python Copy_Translator.py
```