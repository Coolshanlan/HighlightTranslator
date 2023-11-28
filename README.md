# :books: Highlight Translator :books:
[![Visitors](https://api.visitorbadge.io/api/combined?path=https%3A%2F%2Fgithub.com%2FCoolshanlan%2FHighlightTranslator%2F&label=Visitors&countColor=%23379a6d&style=flat)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2FCoolshanlan%2FHighlightTranslator%2F)   
[:safety_pin: Download Zip File](https://coolshan.pse.is/3jrczc)
<!--
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/895ab53151cc4734ab63da3abaf25b82)](https://www.codacy.com/gh/Coolshanlan/HighlightTranslator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Coolshanlan/HighlightTranslator&amp;utm_campaign=Badge_Grade)
-->
Highlight Translator can help you to **translate the words quickly and accurately**. By only `highlighting`, `copying`, or `screenshoting` the content you want to translate anywhere on your computer (ex. `PDF`, `PPT`, `WORD` etc.), the translated results will then be automatically displayed before you.

:warning: **The software doesn’t support Linux and Mac OS. Mac OS might be supported in the future.** :warning:


Translation resource: [Google Translate](https://translate.google.com.tw) and [Cambridge dictionary](https://dictionary.cambridge.org)

OCR technology: [Tesseract](https://github.com/tesseract-ocr/tesseract)

Virtual Desktop Control DLL: [Ciantic/VirtualDesktopAccessor Github](https://github.com/Ciantic/VirtualDesktopAccessor)

[Highlight Translate Github](https://github.com/Coolshanlan/Copy-Translator)

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo.gif)
## :small_red_triangle_down: How To Use / Download :small_red_triangle_down:
### Step 1. Download the software in the Executable File
[:safety_pin: Download Zip File](https://coolshan.pse.is/3jrczc)
### Step 2. Decompress the Zip file and Execute the file
Find the `HighlightTranslator.exe` in the folder and then double click

![](https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/executablefile.png)
## :loudspeaker: Highlight Features
### [Methods of Getting Source Texts](#GettingMethods)
- Highlight/Selected
- Screenshot (keyboard shortcut: `Windows + Shift + S` )
- Copy

### [Automatically Appear Window](#AutomaticallyAppearWindow)
The window will be automatically appear **when you `copy`/`highlight`/`screenshot` some content** and then automatically be hidden after a few seconds if you don't use it.
### [Automatically Switch to Current Virtual Desktop](#AutomaticallySwitchtoCurrentVirtualDesktop)
You can use it on the different virtual desktops without manually switching by yourself, it will automatically switch to the current virtual desktop

### [Automatically Switch between Languages](#AutomaticallySwitchbetweenLanguages)
When the **language of input texts** is the same as the target language, the source language and target language will be automatically switched to each other.
### [Text to Speak](#Speak)
It can speak the input sentences or the translated results and also can be automatic.

**It will be helpful in learning languages**
## :dart: Features
### :key: Methods of getting your source texts<a name="GettingMethods"></a>
- **Highlight/Selected** (This method does not support Microsoft Office, but you can copy the words/sentences instead)
- **Screenshot** (Only English and Chinese supported currently, but feel free to add new languages by yourself)
  > Keyboard Shortcut: `Windows + Shift + S`
- **Copy**

### :key: Automatically Appear Window<a name="AutomaticallyAppearWindow"></a>
The window will automatically appear **when you copy/highlight/screenshot some content** and then automatically be hidden after a few seconds if you don't use it.
- Cancel disappearance

  If you don't want the window to automatically disappear, you can stop it by moving your mouse on the window or just clicking the checkbox on the top
- Early Disappear

  If you want the window to disappear early, you can move your mouse on the window first and then click anywhere out of the window
<img src="https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo_automaticlly_hide.gif" width="700">

### :key: Automatically Switch to Current Virtual Desktop<a name="AutomaticallySwitchtoCurrentVirtualDesktop"></a>
You can use it on different virtual desktops without manually switching by yourself, it will automatically switch to the current virtual desktop.

### :key: Automatically Switch between Languages<a name="AutomaticallySwitchbetweenLanguages"></a>
If **the language of input texts** is the same as the target language, the source language and target language will be automatically switched to each other.

<img src="https://github.com/Coolshanlan/Highlight-Translator/blob/master/image/demo_switch_language.gif" width="700">

### :key: Text to Speech<a name="Speak"></a>
It can speak the input sentences or the translated results, and also can be automatic.
### :pushpin: Checkbox "input"
Display InputBox and Translate Button.<br>
You can type the text in InputBox and then `press Enter` or `click the Translate Button` to get the translation result.
### :pushpin: Checkbox "top"
If the checkbox is checked, the window will always be kept on top.
### :pushpin: Checkbox "select"
When you highlight some content, the translation will be automatically displayed.
### :pushpin: Setting Interface
You can set the config on the menu
### :pushpin: Change Dictionary
Only Google and Cambridge Dictionary are supported for now. For Cambridge Dictionary, only "English to Chinese" supported
### :pushpin: Switch Language Button
It can switch between source and target languages

## :open_book: Google Translate API
This API can get the translation result from Google Translate
### How to use
```python
import GoogleTranslate as gt
print(gt.get_translate("good", "en","zh-TW"))
```
### Parameters
1. inputtext: The text that you want to translate
2. sourcelanguage: The language of the input text language
3. targetlanguage: The language of the output result in language
> You can refer to `language.txt` for all the languages supported.
### Return
1. result: The most common result
2. allresult: All of the results
3. detect_language: Detecting the language of the input text
4. revise: Suggestion when the text is seemingly misspelled

## :bookmark_tabs: Config.json
You can adjust these parameters in the Setting Interface.
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
- **appear_time**: The window will automatically appear when you copy/highlight/screenshot some content and then automatically be hidden after a few seconds.
- **dynamic_adjust_appear_time**: The time of Window automatic appearance will be extended according to the length of input text(0 will close this feature if >0, every three words will extend  `dynamic_adjust_appear_time` seconds)
- **auto_speak_length_limit**: When the input length is less than the limit, the automatic speaking function will be triggered
- **font**
- **font_size**
- **audio_volume**: Speaking volume (0~1)
- **auto_switch_language**: Enable the source and target languages to be switched automatically (0 or 1)
- **number_of_terms**: Control the number of displayed translation results (terms) (>0)
- **auto_change_dictionary**: When the input is a word, the dictionary will be automatically switched to Cambridge dictionary (0 or 1)
- **restructure_sentences**: It will restructure your input sentences (0 or 1)
- **inputbox_color**: The background color of the input box
- **resultbox_color**: The background color of the result box
- **copycheck**: Check clipboard frequency (sec)
- **doubleclick**: the time between the two clicks that will make them viewed as a "doublecklick" (sec)
- **select**: The time of the press to make the press viewed as a "long press" (sec)


## How To Install
```
pip install -r requirements.txt
python Highlight_Translator.py
```
## Requirement
python 3.7
``` python
python==3.7
pyinstaller==5.13.2
Pillow==9.5.0
pynput==1.6.0
PyAutoGUI==0.9.0
pytesseract==0.3.0
pywin32==306
requests>=2.24.0
beautifulsoup4>=4.9.3
numpy==1.21.6
pygame==2.5.2
gTTS==2.2.4
pyvda==0.3.1
```
