# Highlight Translate
Highlight Translator can help you quickly translate, just highlight, copy or screenshot the content you want to translate anywhere on your computer (ex. pdf, ppt, etc.), and it will automatically display the translation results to you

**Only support in Windows, might add linux version in the future.**


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Highlight Translate Github](https://github.com/Coolshanlan/Copy-Translator)

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo.gif)
## Download
[Download Zip File](https://bit.ly/37QQvgN)

## Requirement
python 3.6
``` python
pyinstaller == 4.1
Pillow == 8.0.1
pynput == 1.6
pyautogui == 0.9
pytesseract == 0.3
pywin32 == 227
requests >= 2.24.0
beautifulsoup4 >= 4.9.3
numpy == 1.19.3
```

## Features
### Auto resizing
Under different resolutions, automatically adjust the window size and font size
### Translation Method
- Screenshot (Only support English, Chinese, Japanese and Korean, you can add new language by your self)
- Copy
- Highlight/Selected (Not support PowerPoint and Word)
### Top Checkbox
Window will be top
if not checked, it will automatically hide after a few seconds.
> default 6 sec, you can modify hide variable in config.json
### Highlight Checkbox
Enable automatic translation when you highlight some content
### Result Box Checkbox
Display InputBox and Translate Button
### Change Dictionary
Only support Google and Cambridge Dictionary
### Change Language
You can change default language in config.json

Cambridge Dictionary only support English to Chinese


## Config.json
``` json
{"hide":6,"font":"Arial","font-size":11,"sourcelanguage":"Detect language","targetlanguage":"Chinese (Traditional)","inputboxcolor":"#F2D8B3","resultboxcolor":"#FDF0C4","copycheck":0.3,"doubleclick":0.3,"select":0.3,"googlenotttk":0,"longttk":0,"automaticchange":0,"restructureSentences":1}
```
- hide: window automatically hide seconds
  > default 6 sec
- font
  > default Calibri
- font-size
  > default 11
- sourcelanguage: Default source language
  > defalut Detect language
- sourcelanguage -> Default target language
  > defalut Chinese (Traditional)
- inputboxcolor -> input box bg color
  > defult #F2D8B3
- resultboxcolor -> result box bg color
  > defult #FDF0C4
- copycheck -> Check clipboard frequency
  > default 0.3 sec
- doubleclick -> 判斷是否為雙擊的時間間隔(幾秒內點兩下算是雙擊)
  > default 0.3 sec
- select -> 長壓幾秒判斷為選取
  > default 0.3 sec
- googlenotttk -> google translate don't need ttk version
  > default 0
- longttk -> If sentence too long, use not ttk version
  > default 0
- automaticchange -> if want to translate a word, automatic change to cambridge
  > default 0
- restructureSentences
  > default 1

## How to use
```
pip install -r requirements.txt
python Highlight_Translator.py
```
