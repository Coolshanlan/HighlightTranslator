# :books: Highlight Translator :books:
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/895ab53151cc4734ab63da3abaf25b82)](https://www.codacy.com/gh/Coolshanlan/HighlightTranslator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Coolshanlan/HighlightTranslator&amp;utm_campaign=Badge_Grade)

Highlight Translator can help you **translate the words quickly and accurately**. By only `highlighting`, `copying`, or `screenshoting` the content you want to translate anywhere on your computer (ex. `PDF`, `PPT`, `WORD` etc.), the translated results will then be automatically displayed before you.

:warning: **The software is only supported in Windows. Mac OS version might be added in the future.** :warning:


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

[Highlight Translate Github](https://github.com/Coolshanlan/Copy-Translator)

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo.gif)
## :small_red_triangle_down: How To Use :small_red_triangle_down:
### Step 1. Download the software in the Executable File
[Download Zip File](https://coolshan.pse.is/3jrczc)
### Step 2. Decompress the Zip file and Execute the file
Find the `HighlightTranslator.exe` in the folder and then double click

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/executablefile.png)
## :loudspeaker: Highlight Features
### [Methods of getting source texts](#GettingMethods)
- Highlight/Selected
- Screenshot
- Copy
### [Automatically Appear Window](#AutomaticallyAppearWindow)
The window will be automatically appear **when you `copy`/`highlight`/`screenshot` some content** and then automatically be hidden after a few seconds if you don't use it.
### [Automatically Switch between Languages](#AutomaticallySwitchbetweenLanguages)
When the **language of input texts** is the same as the target language, source language and target language will be automatically switched to each other.
### [Text to Speak](#Speak)
It can speak the input sentences or the translated results, and also can be automatic.

**It will be helpful to learning languages**
## :dart: Features
### :key: Methods of getting your source texts<a name="GettingMethods"></a>
- **Highlight/Selected** (This method does not support Microsoft Office, but you can copy the words/sentences instead)
- **Screenshot** (Only English and Chinese supported currently, but feel free to add new languages by yourself)
- **Copy**
### :key: Text to Speech<a name="Speak"></a>
It can speak the input sentences or the translated results, and also can be automatic.
### :key: Automatically Appear Window<a name="AutomaticallyAppearWindow"></a>
The window will be automatically appear **when you copy/highlight/screenshot some content** and then automatically be hidden after a few seconds if you don't use it.

If you don't want the window to automatically disappear, you can stop it by moving your mouse on the window or just clicking the checkbox on the top

<img src="https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo_automaticlly_hide.gif" width="700">

### :key: Automatically Switch between Languages<a name="AutomaticallySwitchbetweenLanguages"></a>
If **the language of input texts** is the same as the target language, source language and target language will be automatically switched to each other.

<img src="https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo_switch_language.gif" width="700">

### :pushpin: Switch Language Button
It can switch between source and target languages
### :pushpin: Setting Interface
You can set the config on the menu
### :pushpin: Change Dictionary
Only Google and Cambridge Dictionary supported for now. For Cambridge Dictionary, only "English to Chinese" supported
### :pushpin: Checkbox "top"
If the checkbox is checked, the window will always be kept on top.
### :pushpin: Checkbox "select"
When you highlight some content, the translation will be automatically displayed.
### :pushpin: Checkbox "input"
Display InputBox and Translate Button

## :notebook_with_decorative_cover: Google Translate API
This API can get the translation result from Google Translate
### How to use
```python
import GoogleTranslate as gt
print(gt.get_translate("good", "en","zh-TW"))
```
### Parameters
1. inputtext: The text that you want to translate
2. sourcelanguage: The language of the input text language
3. targetlanguage: The language of the output result language
> You can refer to `language.txt` for all the languages supported.
### Return
1. result: The most common result
2. allresult: All of the results
3. detect_language: Detecting the language of the input text
4. revise: Suggestion when the text is seemingly misspelled

## :bookmark_tabs: Config.json
``` python
{
  "source_language":"Detect language",
  "target_language":"Chinese (Traditional)",
  "appear_time":6,
  "dynamic_adjust_appear_time":1,
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
- **source_language**: Default source language
- **target_language**: Default target language
- **appear_time**: The window will be automatically appear when you copy/highlight/screenshot some content and then automatically be hidden after a few seconds.
- **dynamic_adjust_appear_time**: The time of Window automatic appearance will be extended according to the length of input text(0 will close this feature, if >=1, every three words will extend  `dynamic_adjust_appear_time` seconds)
- **auto_speak_length_limit**: When the input length is less than the limit, the automatic speaking function will be triggered
- **font**
- **font_size**
- **audio_volume**: Speaking volume (0~1)
- **auto_switch_language**: Enable the source and target languages to be swtiched automatically (0 or 1)
- **number_of_terms**: Control the number of displayed translation results (terms) (>0)
- **auto_change_dictionary**: When the input is a word, the dictionary will be automaticlly switched to cambridge dictionary (0 or 1)
- **restructure_sentences**: It will restructure your input sentences (0 or 1)
- **inputbox_color**: The background color of input box
- **resultbox_color**: The background color of result box
- **copycheck**: Check clipboard frequency (sec)
- **doubleclick**: the time between the two clicks that will make them viewed as a "doublecklick" (sec)
- **select**: The time of the press to make the press viewed as a "long press" (sec)


## How To Install
```
pip install -r requirements.txt
python Highlight_Translator.py
```
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
