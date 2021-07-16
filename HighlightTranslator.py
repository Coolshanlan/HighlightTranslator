# import pyautogui
# -*- coding: utf-8 -*-
from gtts import gTTS
from pygame import mixer
from os import system
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener, Button
import datetime
import win32con
import win32api
import CambridgeTranslate as ct
import pytesseract
from PIL import Image, ImageOps,ImageGrab
import traceback
import GoogleTranslate as gt
from time import sleep
import threading
from win32con import CF_TEXT
import win32clipboard
from tkinter import ttk
import tkinter as tk
import re
import json
import sys

# tesseract setting
# OCR only support these four languages now, you can add another language from tesseract and put it file in tesseract/tessdata
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
tesseract_languages=["eng","chi_tra","kor","jpn"]

# load config (detail in readme)
config={}
def load_config():
    global config
    with open("config.json") as f:
        config = json.loads(f.read())
load_config()
detect_language=None
MP3FILEPATH='speech_file/output.mp3'

#Load all language from language.txt
source_languages={}
target_languages={}
with open("language.txt") as f:
    languagelist = json.loads(f.read())
for i in range(len(languagelist[0])):
    source_languages[languagelist[0][i][1]] = languagelist[0][i][0]
for i in range(len(languagelist[1])):
    target_languages[languagelist[1][i][1]] = languagelist[1][i][0]

# add language exchange function
class MainWindow():

    def __init__(self):
        """The Main Window."""
        self.root = tk.Tk()
        self.set_WindowsSize()# Auto resizing
        self.keyboard = Controller()# keyboard hook

        self.translate_result=''

        # Top of feature checkboxes
        self.checkbox_frame =tk.Frame(self.root)

        # Menu
        self.menubar =tk.Menu(self.root)
        self.menubar.add_cascade(label="Setting",command=self.open_setting)
        self.menubar.add_cascade(label="How to use",command=self.open_website)
        self.root.config(menu=self.menubar)

        self.top_value = tk.BooleanVar()
        self.top_value.set(False)
        self.top_checkbox = tk.Checkbutton((self.checkbox_frame), text='top', var=(self.top_value),command=(self.checkchange))

        self.select_value = tk.BooleanVar()
        self.select_value.set(True)
        self.select_checkbox = tk.Checkbutton((self.checkbox_frame), text='select', var=(self.select_value),command=(self.changehighlightclick))

        self.display_inputbox_value = tk.BooleanVar()
        self.display_inputbox_value.set(False)
        self.display_inputbox_checkbox = tk.Checkbutton((self.checkbox_frame), text='input', var=(self.display_inputbox_value),command=self.displayinputbox)

        self.screenshot_value = tk.BooleanVar()
        self.screenshot_value.set(True)
        self.screenshot_checkbox = tk.Checkbutton((self.checkbox_frame), text='screen', var=(self.screenshot_value))

        # Dictionary combobox
        self.dictionary_combobox = ttk.Combobox(self.root, state="readonly")
        self.dictionary_combobox["values"] = ["Google", "Cambridge"]
        self.dictionary_combobox.current(0)
        self.dictionary_combobox.bind("<<ComboboxSelected>>", self.dictionary_change_event)

        # Language region
        self.language_frame =tk.Frame(self.root)
        self.source_combobox = ttk.Combobox(self.language_frame, state="readonly", width=10)
        self.target_combobox = ttk.Combobox(self.language_frame, state="readonly", width=10)
        self.target_combobox.bind("<<ComboboxSelected>>", self.target_combobox_change)
        self.source_combobox.bind("<<ComboboxSelected>>", self.target_combobox_change)
        self.exchange_button = tk.Button((self.language_frame), text='⇄',command=(self.exchange_language))
        self.setup_language_item()

        # Button
        self.translate_button = tk.Button((self.root), text='Translate',command=(self.changeText))
        self.clear_button = tk.Button((self.root), text='Clear',command=(self.ClearText))

        # Speak button region
        self.speak_frame =tk.Frame(self.root)
        self.speak_target_button = tk.Button((self.speak_frame), text='Speak T',command=(self.speak_t))
        self.speak_source_button = tk.Button((self.speak_frame), text='Speak S',command=(self.speak))

        self.auto_speak_value = tk.BooleanVar()
        self.auto_speak_value.set(False)
        self.auto_speak_checkbox = tk.Checkbutton((self.speak_frame), text='auto', var=(self.auto_speak_value),command=(self.speak_change))

        #scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))
        # Inputbox
        self.inputbox = tk.Text(height=3, font=("{} {}".format(str(config["font"]), str(self.font_size))))
        self.inputbox.insert(tk.END, 'Try to copy/highlight/select/screenshot contents that you want to translate')
        self.inputbox.configure(bg=config["inputbox_color"])
        self.inputbox.bind('<Return>', self.input_press)
        #resultbox
        self.resultbox = tk.Text((self.root),yscrollcommand=(self.scrollbar.set), height=100, font=("{} {}".format(str(config["font"]), str(self.font_size))))
        self.resultbox.configure(bg=config["resultbox_color"])

        self.checkbox_frame.pack()
        self.top_checkbox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.select_checkbox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.screenshot_checkbox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.display_inputbox_checkbox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)

        self.dictionary_combobox.pack(fill=(tk.BOTH))
        self.source_combobox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.target_combobox.pack( fill=(tk.BOTH),expand=True,side=tk.RIGHT)
        self.language_frame.pack(fill=(tk.BOTH))

        self.speak_frame.pack(fill=(tk.BOTH))
        self.speak_source_button.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.speak_target_button.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.exchange_button.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.auto_speak_checkbox.pack( fill=(tk.BOTH),expand=True,side=tk.RIGHT)

        self.translate_button.pack(fill=(tk.BOTH))
        self.clear_button.pack(fill=(tk.BOTH))

        self.inputbox.pack(fill=(tk.BOTH))
        self.resultbox.pack(fill=(tk.BOTH))
        self.scrollbar.config(command=(self.resultbox.yview))

        self.inputbox.pack_forget()
        self.translate_button.pack_forget()

        # if your mouse move into windowns, it will not hide it-self
        self.movein = False
        self.checktop = False
        self.topagain = False

        self.linelength = int((self.resultbox.winfo_width()/(self.font_size-4*(self.font_size/11))-1))
        self.now_copy = ''
        self.previous_copy = ''

        # not translate the word already in clipboard when open the application
        # self.get_clipboard()
        # self.previous_copy = self.now_copy

        #close threads when window closed
        self.closed = False
        self.changed_language=False

        self.root.bind('<Motion>', self.motion)
        self.root.title('Highlight Translator')
        self.root.protocol('WM_DELETE_WINDOW', self.closewindows)

        #check is it double click or not
        self.clickstarttime = datetime.datetime.now()
        self.clickendtime = datetime.datetime.now()
        self.clickstarttime_tmp = datetime.datetime.now()
        self.clickendtime_tmp = datetime.datetime.now()
        # check finction
        self.mouse_listener = Listener(on_click=self.mouseclick)
        self.mouse_listener.start()

        # check clipboard change or not
        self.check_clipboard_thread = threading.Thread(target=(self.CheckCopyWhile))
        self.check_clipboard_thread.start()

        self.root.mainloop()

    def input_press(self,event):
        self.changeText(True)

    def exchange_language(self):
        tmp_source = self.source_combobox.get()
        tmp_target = self.target_combobox.get()
        if self.source_combobox.get() in target_languages.keys():
            tmp_target = self.source_combobox.get()
        elif self.source_combobox.get() == 'Chinese':
            tmp_target = 'Chinese (Traditional)'
        if self.target_combobox.get() in source_languages.keys():
            tmp_source = self.target_combobox.get()
        elif 'Chinese' in self.target_combobox.get():
            tmp_source='Chinese'

        self.source_combobox.current(self.source_combobox['values'].index(tmp_source))
        self.target_combobox.current(self.target_combobox['values'].index(tmp_target))

    def open_setting(self):
        self.setting_windows=SettingWindow()

    @staticmethod
    def open_website():
        system('start {}'.format('https://github.com/Coolshanlan/HighlightTranslator'))

    def set_WindowsSize(self):
        originX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        originY =win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        scaleX = originX/1280
        scaleY = originY/720
        self.font_size=int(config["font_size"]*scaleX)
        self.root.geometry('{}x{}'.format((int)(210*scaleX),(int)(320*scaleY)))


    def setup_language_item(self):
         self.source_combobox["values"] = sorted(source_languages.keys())
         self.target_combobox["values"] = sorted(target_languages.keys())
         self.source_combobox.current(self.source_combobox["values"].index(config["source_language"]))
         self.target_combobox.current(self.target_combobox["values"].index(config["target_language"]))


    def displayinputbox(self):
        if self.display_inputbox_value.get() == True:
            self.resultbox.pack_forget()
            self.translate_button.pack(fill=(tk.BOTH))
            self.inputbox.pack(fill=(tk.BOTH))
            self.resultbox.pack(fill=(tk.BOTH))
        else:
            self.inputbox.pack_forget()
            self.translate_button.pack_forget()


    def dictionary_change(self):
        if self.dictionary_combobox.get() == "Google":
            self.setup_language_item()
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                ("*"*int((self.linelength-16)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")

        else:
            self.source_combobox["values"] = ["English"]
            self.target_combobox["values"] = ["Chinese (Traditional)"]
            self.source_combobox.current(0)
            self.target_combobox.current(0)
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-18)/2))+"Change to cambridge" +
                ("*"*int((self.linelength-18)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")



    def dictionary_change_event(self,event):
        self.dictionary_change()
        self.changeText(True)

    def target_combobox_change(self, event):
        self.changeText(True)

    def speak_t(self):
        # remove(MP3FILEPATH)
        text = self.translate_result

        language = target_languages[self.target_combobox.get()]

        myobj = gTTS(text=text, lang=language.lower(), slow=False)
        mixer.init()
        mixer.music.unload()
        myobj.save(MP3FILEPATH)
        self.run_speak_file()

    def speak_change(self):
        if self.auto_speak_value.get() == True:
            self.speak()

    def speak(self):
        def speak_func():
            text = self.inputbox.get(1.0, tk.END)
            language = source_languages[self.source_combobox.get()]
            if language == 'auto':
                language = detect_language.lower()

            myobj = gTTS(text=text, lang=language.lower(), slow=False)
            mixer.init()
            mixer.music.unload()
            myobj.save(MP3FILEPATH)
            self.run_speak_file()
        speak_thread = threading.Thread(target = speak_func)
        speak_thread.start()

    @staticmethod
    def run_speak_file():
        try:
            mixer.music.set_volume(config['audio_volume'])
            mixer.music.load(MP3FILEPATH)
            mixer.music.play()
        except Exception as e:
            MainWindow.record_error(e)


    def changehighlightclick(self):
        if self.select_value.get() == True:
            self.mouse_listener = Listener(on_click=self.mouseclick)
            self.mouse_listener.start()
        else:
            self.mouse_listener.stop()


    def checkchange(self):
        if self.top_value.get() == True:
            self.root.wm_attributes('-topmost', 1)
        else:
            self.root.wm_attributes('-topmost', 0)


    def closewindows(self):
        self.closed = True
        if self.select_value.get() == True:
            self.mouse_listener.stop()
        self.check_clipboard_thread.join()
        self.root.destroy()

    def printerror(self,error_class):
        self.resultbox.insert(tk.END, ("*"*3)+error_class +("*"*3+"\n"))
        self.resultbox.insert(tk.END, "="*self.linelength+"\n")
        self.resultbox.see(tk.END)

    @staticmethod
    def record_error(e):
        with open("log.txt","a") as f:
            now = datetime.date.today()
            current_time = now.strftime("%m/%d/%Y")
            now = datetime.datetime.now()
            current_time += " "+ now.strftime("%H:%M:%S")
            print(current_time)
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            _, _, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}:\n [{}]\n{}".format(fileName, lineNum, funcName, error_class, detail)
            f.writelines(str(current_time)+"\n")
            f.writelines(errMsg+"\n")
            f.writelines("-------------------------"+"\n")
            return error_class


    def image_OCR(self,im):
        try:
            im = ImageOps.grayscale(im)
            if self.source_combobox.get() == "English" or self.source_combobox.get() =="Detect language":
                self.now_copy = pytesseract.image_to_string(im,
                                                            lang='eng')
            elif self.source_combobox.get() == "Chinese":
                self.now_copy = pytesseract.image_to_string(im,
                                                            lang='chi_tra').replace(" ", "")
            elif self.source_combobox.get() == "Korean":
                self.now_copy = pytesseract.image_to_string(im,
                                                            lang='kor+kor_vert').replace(" ", "")
            elif self.source_combobox.get() == "Japanese":
                self.now_copy = pytesseract.image_to_string(im,
                                                            lang='jpn').replace(" ", "")
            else:
                tk.messagebox.showinfo(title=f"Not Support {self.source_combobox.get()}", message="Screenshot Translate only support English, Chinese, Korean and Japanese")
        except Exception as e:
            self.printerror(self.record_error(e))
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-18)/2))+"OCR Error" +
                ("*"*int((self.linelength-18)/2)+"\n"))
            self.resultbox.insert(
                tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            #self.root.clipboard_append('')
            return False
        #self.root.clipboard_append('')
        return True

    def get_clipboard(self):
        if win32clipboard.IsClipboardFormatAvailable(CF_TEXT):
            try:
                self.now_copy = self.root.clipboard_get()#self.root.selection_get(selection="CLIPBOARD")
            except Exception as e:
                self.printerror(self.record_error(e))
                self.root.clipboard_append('')
                # self.now_copy = self.previous_copy
                return False
        elif self.root.state() != 'iconic' and self.screenshot_value.get():
            try:
                im = ImageGrab.grabclipboard()
            except OSError:
                return False
            except Exception as e:
                self.printerror(self.record_error(e))
                self.root.clipboard_append('')
                # self.now_copy = self.previous_copy
                return False
            if isinstance(im, Image.Image):
                return self.image_OCR(im)
        return True


    def CheckCopy(self):
        if not self.get_clipboard(): return False
        if self.now_copy == self.previous_copy:
            return False
        if self.now_copy.strip() == '':
            return False
        self.previous_copy = self.now_copy
        self.inputbox.delete(1.0, tk.END)
        self.inputbox.insert(1.0, self.textprocessing(self.now_copy))
        return True


    def changetop(self):
        if self.checktop:
            self.topagain = True
            return
        self.checktop = True
        self.root.wm_attributes('-topmost', 1)
        l = True
        while l:
            l = False
            sleep(config["hide"])
            if self.topagain:
                l = True
            self.topagain = False
        self.checktop = False
        if self.top_value.get() == False:
            self.root.wm_attributes('-topmost', 0)
            if self.movein == False:
                self.root.lower()
            else:
                self.movein = False


    def CheckCopyWhile(self):
        while not self.closed:
            if self.CheckCopy():
                self.clear_button.configure(text = 'Translating...')
                self.changet = threading.Thread(
                    target=(self.changeText(False)))
                self.changet.start()
            sleep(config["copycheck"])


    def restructure_sentences(self, text):
        textlist = text.split('@')
        newsentence = []
        # clear space
        i = 0
        while i < len(textlist):
            textlist[i] = textlist[i].strip()
            if textlist[i] == "":
                del textlist[i]
                i -= 1
            i += 1
        textlist[0] = textlist[0].strip()
        tmpsentence = textlist[0]

        for i in range(1, len(textlist)):
            textlist[i] = textlist[i].strip()
            if len(textlist[i]) == 0:
                continue
            if textlist[i][-1] == "-":
                textlist[i] = textlist[i][:-1]
            if tmpsentence[-1] == '.' or textlist[i][0] == "•" or textlist[i][0] == "" or re.search("[0-9]+\.?:", textlist[i]) != None or tmpsentence[-1] == ":"or tmpsentence[-1] == "：":
                newsentence.append(tmpsentence)
                tmpsentence = textlist[i]
                continue
            tmpsentence += " "+textlist[i]
        newsentence.append(tmpsentence)

        if len(newsentence) > 50:
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-25)/2)) + "The number of sentences exceeds the limit(50)" +
                ("*"*int((self.linelength-25)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")

        newsentence = newsentence[:50]
        resultsentence = "\n".join(newsentence)

        return resultsentence


    def textprocessing(self, inptext):
        text = inptext.replace(
            '\r', '').replace('¡', '').replace('\uf0a7', '').replace('¦', '').replace("\n", "@").replace("\t", "").replace("\x00", "").replace(' – ', '-').replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("  ", " ")
        while text[-1] == "@" or text[-1] == ' ':
            text = text[:-1]
        while text[0] == "@" or text[0] == ' ':
            text = text[1:]

        if config["restructure_sentences"]:
            text = self.restructure_sentences(text)
        else:
            text = text.replace("@", "\n")
        return text

    def get_translation(self,text):
        try:
            # Google Translate
            if self.dictionary_combobox.get() == "Google":
                result, allresult, detect_language, revise = gt.get_translate(
                    text, source_languages[self.source_combobox.get()],target_languages[self.target_combobox.get()])
            # Cambridge Translate
            else:
                result, allresult = ct.get_translate(text)
                revise=None
                detect_language='en'
                if result == "":
                    self.dictionary_combobox.current(0)
                    self.dictionary_change()
                    result, allresult, detect_language, revise = gt.get_translate(text, source_languages[self.source_combobox.get()],target_languages[self.target_combobox.get()])

            return True,(result,allresult,revise,detect_language)
        except Exception as e:
            self.printerror(self.record_error(e))
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-21)/2))+"Check WIFI and try again" +
                ("*"*int((self.linelength-21)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            self.top = threading.Thread(target=self.changetop)
            self.top.start()
            return False,(None,None,None,None)


    def autochange_dictionary(self,text):
        # if not a word change to google because Cambridge can only translate a word
        if len(text.split(' ')) > 1  and self.dictionary_combobox.get() != "Google":
            self.dictionary_combobox.current(0)
            self.dictionary_change()

        # automatic change to google dictionary if input is a word
        elif config["auto_change_dictionary"]  and self.dictionary_combobox.get() == "Google" and len(text.split(' ')) == 1:
            self.dictionary_combobox.current(1)
            self.dictionary_change()




    def changeText(self, click=True):
        global detect_language
        self.movein = False
        self.linelength = int((self.resultbox.winfo_width()/(self.font_size)*1.2))
        text = self.inputbox.get(1.0, tk.END)

        if not click:
            self.autochange_dictionary(text)

        status,(result,allresult,revise,detect_language) = self.get_translation(text)

        if not status:
            return False

        # print input
        self.resultbox.insert(tk.END, text)
        if revise:
            self.resultbox.insert(tk.END, '({})\n'.format(revise))

        self.resultbox.insert(
            tk.END, "-"*((int)(self.linelength*1.8))+"\n")

        # print result
        self.translate_result=''
        for iter_result in result:
            self.resultbox.insert(tk.END, iter_result)
            self.translate_result += iter_result+'\n'
            if allresult != []:
                self.resultbox.insert(tk.END, "\n")
        if len(allresult) > 0:
            self.resultbox.insert(tk.END, "\n")

        # print all result
        for r_idx,iter_result in enumerate(allresult):
            self.translate_result += iter_result['pos'].capitalize()+":"+"\n"
            self.resultbox.insert(tk.END, iter_result['pos'].capitalize()+":"+"\n")
            terms = iter_result['terms'][:config['number_of_terms']]
            for t_idx,iter_terms in enumerate(terms):
                self.resultbox.insert(tk.END, iter_terms)
                self.translate_result+=iter_terms
                if t_idx != len(terms)-1:
                    self.translate_result += ","
                    self.resultbox.insert(tk.END, ",")
            if r_idx != len(allresult)-1:
                self.resultbox.insert(tk.END, "\n\n")
                self.translate_result+="\n\n"

        self.resultbox.insert(tk.END, "\n"+"="*self.linelength+"\n")
        self.resultbox.see(tk.END)
        self.clear_button.configure(text = 'Clear')

        # Let window top
        if not self.top_value.get():
            self.top = threading.Thread(target=self.changetop)
            self.top.start()

        # auto speak
        if self.auto_speak_value.get() == True:
            if len(text.split(' ')) <= config["auto_speak_length_limit"]:
                text_max_length = max([len(str(t)) for t in text.split(' ')])
                if text_max_length <= config['auto_speak_length_limit']*1.5:
                    self.speak()

        #auto exchange dictionary
        if not self.changed_language and detect_language.replace('zh-CN','zh-TW') == target_languages[self.target_combobox.get()] and source_languages[self.source_combobox.get()] != 'auto':
            self.changed_language=True
            self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-15)/2))+"Exchange Language" +
                    ("*"*int((self.linelength-15)/2)+"\n"))
            self.resultbox.insert(tk.END,"="*self.linelength+"\n")
            self.exchange_language()
            self.changeText(False)

        self.changed_language=False


    def motion(self, event):
        self.movein = True


    def copyclick(self):
        # pyautogui.hotkey('ctrl', 'c')
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')


    def mouseclick(self, x, y, button, pressed):
        if button == Button.left and pressed == True:
            self.clickstarttime = datetime.datetime.now()
        if button == Button.left and pressed == False:
            self.clickendtime_tmp = datetime.datetime.now()
            if (self.clickendtime_tmp - self.clickendtime).total_seconds() < config["doubleclickcheck"]:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            elif (self.clickendtime_tmp - self.clickstarttime).total_seconds() > config["selectcheck"]:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            else:
                self.clickendtime = self.clickendtime_tmp

        if self.closed:
            return False


    def ClearText(self):
        self.resultbox.delete(0.0, tk.END)

class SettingWindow():

    def __init__(self):
        """Setting Interface."""
        self.root = tk.Tk()
        self.root.wm_attributes('-topmost', 1)
        self.root.title('Setting')
        self.textlist = []
        self.maxlen = max([len(str(v)) for v in config.values()])
        tk.Label(self.root,text='Some setting need to reload the application', justify=tk.LEFT, font=("{} {}".format(str(config["font"]), str(config['font_size']))), fg='#FF0000').pack()

        language_frame = tk.Frame(self.root)
        language_frame.pack(fill=(tk.BOTH))
        tk.Label(language_frame,text='Source Language', justify=tk.LEFT, font=("{} {}".format(str(config["font"]), str(config['font_size'])))).pack( side=tk.LEFT)
        self.source_combobox = ttk.Combobox(language_frame, state="readonly",font=("{} {}".format(str(config["font"]), str(config['font_size']))),width=self.maxlen-2)
        self.source_combobox.pack(side=tk.RIGHT)

        language_frame = tk.Frame(self.root)
        language_frame.pack(fill=(tk.BOTH))
        tk.Label(language_frame,text='Target Language', justify=tk.LEFT, font=("{} {}".format(str(config["font"]), str(config['font_size'])))).pack( side=tk.LEFT)
        self.target_combobox = ttk.Combobox(language_frame, state="readonly",font=("{} {}".format(str(config["font"]), str(config['font_size']))), width=self.maxlen-2)
        self.target_combobox.pack(side=tk.RIGHT)

        self.setup_language_item()

        for k,v in config.items():
            if k in ['source_language','target_language']:
                continue
            self.textlist.append(self.create_line(k,v))
        self.root.protocol('WM_DELETE_WINDOW', self.close_windows)

    def close_windows(self):
        self.save_config()
        self.root.destroy()

    def setup_language_item(self):
         self.source_combobox["values"] = sorted(source_languages.keys())
         self.target_combobox["values"] = sorted(target_languages.keys())
         self.source_combobox.current(self.source_combobox["values"].index(config["source_language"]))
         self.target_combobox.current(self.target_combobox["values"].index(config["target_language"]))


    def save_config(self):
        new_config={}
        new_config['source_language']=self.source_combobox.get().replace('\n','')
        new_config['target_language']=self.target_combobox.get().replace('\n','')
        reduce=0
        for idx,key in enumerate(config.keys()):
            if key in ['source_language','target_language']:
                reduce+=1
                continue
            tmp_value = self.textlist[idx-reduce].get(1.0, tk.END)
            try:
                tmp_value = float(tmp_value)
                if tmp_value - tmp_value//1 == 0:
                    tmp_value = int(tmp_value)
            except:
                tmp_value = str(tmp_value).replace('\n','').strip()
            new_config[key]=tmp_value

        with open('config.json', 'w') as fp:
            json.dump(new_config, fp)
        load_config()

    def create_line(self,key,value):
        frame = tk.Frame(self.root)
        frame.pack(fill=(tk.BOTH))

        tk.Label(frame,text=key.replace('_',' '), justify=tk.LEFT, font=("{} {}".format(str(config["font"]), str(config["font_size"])))).pack( side=tk.LEFT)
        textbox=tk.Text(frame,height=1,width=self.maxlen, font=("{} {}".format(str(config["font"]), str(config["font_size"]))))
        textbox.insert(tk.END, str(value))
        textbox.pack( side=tk.RIGHT)

        return textbox



app = MainWindow()
app.closed =True
