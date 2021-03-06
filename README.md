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
If your **language of input text** as same as target language, source language and target language will be automatically switched to each other.
> 2021/07/17 update
### Exchange Language Button
It can exchange source and target language
> 2021/07/15 update
### Setting Interface
You can set the config on the menu
> 2021/07/10 update
### Text to Speech
It can speak the input sentence or the result of translating
> 2021/07/04 update

## :dart: Features
### :key: Translation Method
- **Screenshot** (Only support English and Chinese, you can add new language by your self)
- **Copy**
- **Highlight/Selected** (Not support PowerPoint and Word)
### :key: Text to Speech
It can speak the input sentence or the result of translating
### :pushpin: Auto resizing
Under different resolutions, automatically adjust the window size and font size
### :pushpin: Top Checkbox
If not checked, window will automatically hide after a few seconds.
> default 6 sec, you can modify hide variable in config.json
### :pushpin: Highlight Checkbox
Enable automatic translation when you highlight some content
### :pushpin: Result Box Checkbox
Display InputBox and Translate Button
### :pushpin: Change Dictionary
Only support Google and Cambridge Dictionary
### :pushpin: Change Language
You can change default language in config.json

Cambridge Dictionary only support English to Chinese


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
  "number_of_terms":4,
  "auto_switch_language":1,
  "auto_change_dictionary":0,
  "restructure_sentences":1,
  "inputbox_color":"#F2D8B3",
  "resultbox_color":"#FDF0C4",
  "copycheck":0.3,
  "doubleclickcheck":0.3,
  "selectcheck":0.3
}
```
- **source_language**: Default source language
  > defalut Detect language
- **sourcelanguage**: Default target language
  > defalut Chinese (Traditional)
- **hide**: The window will automatically hide after few seconds
  > default 6 sec
- **auto_speak_length_limit**: When the input length is less than the limit, the automatic speaking function will be triggered
  > default 10
- **font**
  > default Calibri
- **font_size**
  > default 11
- **audio_volume**: Speaking volume (0~1)
  > default 0.95
- **auto_switch_language**: Enable automatically switch language
- **number_or_terms**: Control the number of display translation result terms (>0)
  > default 0.95
- **auto_change_dictionary**: When the input is a word, automaticlly change to cambridge dictionary (0 or 1)
  > default 0
- **restructure_sentences**: It will restructure your input sentence (0 or 1)
  > default 1
- **inputbox_color**: The background color of input box
  > defult #F2D8B3
- **resultbox_color**: The background color of result box
  > defult #FDF0C4
- **copycheck**: Check clipboard frequency
  > default 0.3 sec
- **doubleclick**: 判斷是否為雙擊的時間間隔(幾秒內點兩下算是雙擊)
  > default 0.3 sec
- **select**: 長壓幾秒判斷為選取
  > default 0.3 sec


## How To Install
```
pip install -r requirements.txt
python Highlight_Translator.py
```
