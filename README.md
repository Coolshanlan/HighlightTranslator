# Highlight Translator
You can highlight or copy sentence or word in anywhere or take a screenshot of the text then this tool will automatically get Google Translate or Cambridge dictionary result and display to you.

**Only support in Windows, might add linux version in the future.**


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Highlight Translator Github](https://github.com/Coolshanlan/Copy-Translator)

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo.gif)
## Download
[Download Zip File](https://bit.ly/2VNK7A7)

## Requirement
python == 3.6
``` python
pyinstaller == 4.1
Pillow == 8.0.1
pynput == 1.6
pyautogui == 0.9
pytesseract == 0.3
pywin32 == 227
requests >= 2.24.0
beautifulsoup4 >= 4.9.3
numpy
```

## Features
### Automatic Resize
在不同解析度下會自動調整視窗大小及字體大小
### Translation Method
- Take screenshot for the text (Only support English and Chinese)
- Copy
- Highlight/Select (Not support PowerPoint)
### Top Checkbox
如果有勾選，程式會置頂，不會被其他程式蓋住

如果沒有勾選，程式會在特訂時間後自動跑到最下層隱藏起來
> default 6 sec, you can modify hide variable in config.json
### Select Checkbox
勾選後開啟選取自動翻譯功能
### Search Box Checkbox
勾選後display InputBox and Translate Button
### Change Dictionary
Only support Google and Cambridge Dictionary
### Change Language
You can change default language in config.json

Cambridge Dictionary only support English to Chinese


## Config.json
``` json
{"hide":6,"font":"Calibri","font-size":11,"sourcelanguage":"Detect language","targetlanguage":"Chinese (Traditional)","inputboxcolor":"#F2D8B3","resultboxcolor":"#FDF0C4","copycheck":0.3,"doubleclick":0.3,"select":0.3,"googlenotttk":0,"longttk":0,"automaticchange":0,"restructureSentences":1}
```
- hide -> 控制自動消失時間
  > default 6 sec
- font -> 字體
  > default Calibri
- font-size -> 調整字體大小
  > default 11
- sourcelanguage -> Default of  source language
  > defalut Detect language
- sourcelanguage -> Default of  target language
  > defalut Chinese (Traditional)
- inputboxcolor -> 調整輸入框背景顏色
  > defult #F2D8B3
- resultboxcolor -> 調整輸出框背景顏色
  > defult #FDF0C4
- copycheck -> 查看剪貼簿頻率
  > default 0.3 sec
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
python Highlight_Translator.py
```
