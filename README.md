# :books: Highlight Translator :books:
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/895ab53151cc4734ab63da3abaf25b82)](https://www.codacy.com/gh/Coolshanlan/HighlightTranslator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Coolshanlan/HighlightTranslator&amp;utm_campaign=Badge_Grade)

Highlight Translator can help you quickly translate, just highlight, copy or screenshot the content you want to translate anywhere on your computer (ex. pdf, ppt, etc.), and it will automatically display the translation results to you

:warning: **Only support in Windows, might add linux version in the future.** :warning:


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Highlight Translate Github](https://github.com/Coolshanlan/Copy-Translator)

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo.gif)
## :small_red_triangle_down: How To Use :small_red_triangle_down:
### Step 1. Download Executable File
[Download Zip File](https://rebrand.ly/HighlightTranslator)
### Step 2. Execute
Find the `HighlightTranslator.exe` in the folder and then double click

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/executablefile.png)
## Requirement
python 3.6
``` python
pyinstaller == 4.1
Pillow == 8.2.0
pynput == 1.6
pyautogui == 0.9
pytesseract == 0.3
pywin32 == 227
requests >= 2.24.0
beautifulsoup4 >= 4.9.3
numpy
pygame
gTTS
```
## :loudspeaker: New Feature
### Automatically Switch Language
> 2021/07/17 update
### Exchange Language Button
> 2021/07/15 update
### Setting Interface
> 2021/07/10 update
### Text to Speech
> 2021/07/04 update

## :dart: Features
### :key: Translation Method
- **Screenshot** (Only support English and Chinese, you can add new language by your self)
- **Copy**
- **Highlight/Selected** (Not support PowerPoint and Word)
### :key: Text to Speech
It can speak the input sentence or the result of translating
### :pushpin: Setting Interface
You can set the config on the menu
### :pushpin: Automatically Switch Language
If your **language of input text** as same as target language, source language and target language will be automatically switched to each other.
### :pushpin: Exchange Language Button
It can exchange source and target language
### :pushpin: Change Dictionary
Only support Google and Cambridge Dictionary, Cambridge only support English to Chinese
### :pushpin: Checkbox of top
If not checked, window will automatically hide after a few seconds.
> default 6 sec, you can modify hide variable in config.json
### :pushpin: Checkbox of select
Enable automatic translation when you highlight some content
### :pushpin: Checkbox of input
Display InputBox and Translate Button

## :notebook_with_decorative_cover: Google Translate API
This API can get the translation result from google translate
### How to use
```python
import GoogleTranslate as gt
print(get_translate("good", "en","zh-TW"))
```
### Parameters
1. inputtext: The text that you want to translate
2. sourcelanguage: Input text language
3. targetlanguage: Output result language
> You can see all of the supportive languages in language.txt
### Return
1. result: The most common result
2. allresult: All of the results
3. detect_language: Detecting language of the input text
4. revise: Revising suggest of the input text that is misspelled

## :bookmark_tabs: Config.json
``` python
{
  "source_language":"Detect language",
  "target_language":"Chinese (Traditional)",
  "hide":6,
  "auto_speak_length_limit":15,
  "font":"Arial",
  "font_size":11,
  "audio_volume":0.95,
  "number_of_terms":5,
  "auto_switch_language":1,
  "auto_change_dictionary":0,
  "restructure_sentences":1,
  "inputbox_color":"#F2D8B3",
  "resultbox_color":"#FDF0C4",
  "copycheck":0.3,
  "doubleclickcheck":0.5,
  "selectcheck":0.3
}
```
- **source_language**:

  Default source language

- **sourcelanguage**:

  Default target language

- **hide**: The window will automatically hide after few seconds
- **auto_speak_length_limit**: When the input length is less than the limit, the automatic speaking function will be triggered
- **font**
- **font_size**
- **audio_volume**: Speaking volume (0~1)
- **auto_switch_language**: Enable automatically switch language
- **number_or_terms**: Control the number of display translation result terms (>0)
- **auto_change_dictionary**: When the input is a word, automaticlly change to cambridge dictionary (0 or 1)
- **restructure_sentences**: It will restructure your input sentence (0 or 1)
- **inputbox_color**: The background color of input box
- **resultbox_color**: The background color of result box
- **copycheck**: Check clipboard frequency
- **doubleclick**: 判斷是否為雙擊的時間間隔(幾秒內點兩下算是雙擊)
- **select**: 長壓幾秒判斷為選取


## How To Install
```
pip install -r requirements.txt
python Highlight_Translator.py
```
