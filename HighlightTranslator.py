# import pyautogui
# -*- coding: utf-8 -*-
from tokenize import Ignore
from gtts import gTTS
from pygame import error, mixer
from os import system,path,mkdir
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener, Button
import datetime
import win32con
import win32api
import CambridgeTranslate as ct
#import TranslatecomTranslate as tt
import GoogleTranslate as gt
import pytesseract
from PIL import Image, ImageOps,ImageGrab
import traceback
from time import sleep
import threading
from win32con import CF_TEXT
import win32clipboard
from tkinter import TclError, ttk, font,messagebox
import tkinter as tk
import re
import json
import sys
import pandas as pd
# root = tk.Tk()
# print(font.families())
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
VDA_DLL_VERSION = 'VirtualDesktopAccessor11.dll' if sys.getwindowsversion().build>20000 else 'VirtualDesktopAccessor.dll'

#Load all language from language.txt
source_languages={}
target_languages={}
with open("language.txt") as f:
    languagelist = json.loads(f.read())
for i in range(len(languagelist[0])):
    source_languages[languagelist[0][i][1]] = languagelist[0][i][0]
for i in range(len(languagelist[1])):
    target_languages[languagelist[1][i][1]] = languagelist[1][i][0]

Translators={'Google':gt,
             'Cambridge':ct,
             #'Transcom':tt,
             }


def load_vocabulary()->None:
    global vocabulary_df,vocabulary_path
    vocabulary_df = pd.read_pickle(vocabulary_path)

def add_to_vocabulary(word,content)->bool:
    global vocabulary_df,vocabulary_path
    word=word.lower().strip()
    word_exist= word in vocabulary_df.index
    if not word_exist:
        new_row = pd.DataFrame(index=[word],data={'content':[content],'wrong':[0]})
        vocabulary_df=pd.concat([vocabulary_df,new_row])

    vocabulary_df.loc[word,'wrong']+=1
    vocabulary_df.to_pickle(vocabulary_path)
    return word_exist

def remove_word(word)->None:
    if not word in vocabulary_df.word:
        vocabulary_df.drop(word)
    vocabulary_df.to_pickle(vocabulary_path)

def edit_word(word,content)->None:
    vocabulary_df.loc[word,'content']=content

    vocabulary_df.to_pickle(vocabulary_path)


vocabulary_path=r'C:\UserD\Program\Project_Python\Copy_Translator\vocabulary\vocabulary.pkl'
if not path.exists(vocabulary_path):
    new_row = pd.DataFrame({'word':['initial'],'content':['最初的'],'wrong':[1]})
    new_row=new_row.set_index('word')
    new_row=new_row.drop('initial')
    new_row.to_pickle(vocabulary_path)

vocabulary_df=None
load_vocabulary()

# Automatic change virtual desktop
import ctypes
import os
from ctypes.wintypes import *
from ctypes import windll, byref

def get_windows(pid):
    current_window = 0
    pid_local = DWORD()
    while True:
        current_window = windll.User32.FindWindowExA(0, current_window, 0, 0)
        windll.user32.GetWindowThreadProcessId(current_window, byref(pid_local))
        if pid == pid_local.value:
            yield current_window

        if current_window == 0:
            return

def Move_window_to_current_desktop():
    virtual_desktop_accessor = ctypes.WinDLL(VDA_DLL_VERSION)
    pid = os.getpid()
    current_number = virtual_desktop_accessor.GetCurrentDesktopNumber()
    for window in get_windows(pid):
        window = HWND(window)
        virtual_desktop_accessor.MoveWindowToDesktopNumber(window, current_number)
class MainWindow():

    def __init__(self):
        """The Main Window."""
        self.root = tk.Tk()
        self.set_WindowsSize()# Auto resizing
        self.keyboard = Controller()# keyboard hook

        self.button_size_scale=config['button_font_size_scale']
        self.font_config=("{} {}".format(str('Arial'), str(int(self.font_size*self.button_size_scale))))

        self.translate_result=''
        self.result_dict=None

        # Top of feature checkboxes
        self.checkbox_frame =tk.Frame(self.root)

        # Menu
        self.menubar =tk.Menu(self.root,font=self.font_config)
        self.menubar.add_cascade(label="Setting",command=self.open_setting,font=self.font_config)
        self.menubar.add_cascade(label="How to use",command=self.open_website,font=self.font_config)
        self.root.config(menu=self.menubar)

        self.top_value = tk.BooleanVar()
        self.top_value.set(False)
        self.top_checkbox = tk.Checkbutton((self.checkbox_frame), text='top', var=(self.top_value),command=(self.checkchange),font=self.font_config)

        self.select_value = tk.BooleanVar()
        self.select_value.set(True)
        self.select_checkbox = tk.Checkbutton((self.checkbox_frame), text='select', var=(self.select_value),command=(self.changehighlightclick),font=self.font_config)

        self.display_inputbox_value = tk.BooleanVar()
        self.display_inputbox_value.set(False)
        self.display_inputbox_checkbox = tk.Checkbutton((self.checkbox_frame), text='input', var=(self.display_inputbox_value),command=self.displayinputbox,font=self.font_config)

        self.screenshot_value = tk.BooleanVar()
        self.screenshot_value.set(True)
        self.screenshot_checkbox = tk.Checkbutton((self.checkbox_frame), text='shot', var=(self.screenshot_value),font=self.font_config)

        # Dictionary combobox
        self.dictionary_combobox = ttk.Combobox(self.root, state="readonly",font=self.font_config)
        self.dictionary_combobox["values"] = list(Translators.keys())
        self.dictionary_combobox.current(0)
        self.dictionary_combobox.bind("<<ComboboxSelected>>", self.dictionary_change_event)

        # Language region
        self.language_frame =tk.Frame(self.root)
        self.source_combobox = ttk.Combobox(self.language_frame, state="readonly", width=10, font=self.font_config)
        self.target_combobox = ttk.Combobox(self.language_frame, state="readonly", width=10, font=self.font_config)
        self.target_combobox.bind("<<ComboboxSelected>>", self.target_combobox_change)
        self.source_combobox.bind("<<ComboboxSelected>>", self.target_combobox_change)
        self.exchange_button = tk.Button((self.language_frame), text='⇄',command=(self.exchange_language),font=self.font_config)
        self.setup_language_item()

        # Button
        self.bottom_button_frame =tk.Frame(self.root)
        self.translate_button = tk.Button((self.root), text='Translate',command=(self.changeText),font=self.font_config)
        self.clear_button = tk.Button((self.bottom_button_frame), text='Clear',command=(self.ClearText),font=self.font_config)
        self.Add_to_book_button = tk.Button((self.bottom_button_frame), text='Add',command=(self.AddToBook),font=self.font_config)

        # Speak button region
        self.speak_frame =tk.Frame(self.root)
        self.speak_target_button = tk.Button((self.speak_frame), text='Speak T',command=(self.speak_t),font=self.font_config)
        self.speak_source_button = tk.Button((self.speak_frame), text='Speak S',command=(self.speak),font=self.font_config)

        self.auto_speak_value = tk.BooleanVar()
        self.auto_speak_value.set(False)
        self.auto_speak_checkbox = tk.Checkbutton((self.speak_frame), text='auto', var=(self.auto_speak_value),command=(self.speak_change),font=self.font_config)

        #scrollbar
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))
        # Inputbox
        self.inputbox = tk.Text(height=3, font=("{} {}".format(str(self.font_), str(self.font_size))),fg=config['inputbox_font_color'])
        self.inputbox.insert(tk.END, 'Try to copy/highlight/select/screenshot contents that you want to translate')
        self.inputbox.configure(bg=config["inputbox_color"])
        self.inputbox.bind('<Return>', self.input_press)
        #resultbox
        self.resultbox = tk.Text((self.root),yscrollcommand=(self.scrollbar.set), height=100, font=("{} {}".format(str(self.font_), str(self.font_size))),fg=config['resultbox_font_color'])
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
        self.bottom_button_frame.pack(fill=(tk.BOTH))
        self.clear_button.pack(fill=(tk.BOTH),expand=True,side=tk.LEFT)
        self.Add_to_book_button.pack(fill=(tk.BOTH),expand=True,side=tk.RIGHT)

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
        self.translate_result = ''
        self.previous_copy = ''

        # not translate the word already in clipboard when open the application
        # self.get_clipboard()
        # self.previous_copy = self.now_copy

        #close threads when window closed
        self.closed = False
        self.changed_language=False

        # # get current desktop number
        # self.vd_number = Move_window_to_current_desktop()

        self.root.bind('<Motion>', self.motion)
        self.root.title('Highlight Translator')
        self.root.protocol('WM_DELETE_WINDOW', self.closewindows)
        self.scrollbar.pack_forget()
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
        text = self.inputbox.get(1.0, tk.END)
        while text[-1] == ' ' or text[-1]=='\n':
            text = text[:-1]
        while text[0] == ' ' or text[0]=='\n':
            text = text[1:]
        self.inputbox.delete(1.0, tk.END)
        self.inputbox.insert(1.0, text)
        self.movein=True
        self.changeText(True)

    def exchange_language(self):
        can_change=True
        tmp_source = self.source_combobox.get()
        tmp_target = self.target_combobox.get()
        if self.source_combobox.get() in target_languages.keys():
            tmp_target = self.source_combobox.get()
        elif self.source_combobox.get() == 'Chinese':
            tmp_target = 'Chinese (Traditional)'
        else:
            can_change=False

        if self.target_combobox.get() in source_languages.keys():
            tmp_source = self.target_combobox.get()
        elif 'Chinese' in self.target_combobox.get():
            tmp_source='Chinese'
        else:
            can_change=False
        if can_change:
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
        font_family=list(font.families())
        font_family = [f.lower() for f in font_family]
        self.font_ = ''.join(config["font"].split(' ')).lower() if config["font"].lower() in font_family else 'Arial'
        self.font_size=int(config["font_size"]*scaleX)
        self.root.geometry('{}x{}+{}+{}'.format((int)(190*scaleX),(int)(320*scaleY),0,100))


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
        if self.dictionary_combobox.get() != "Cambridge":
            self.setup_language_item()
        else:
            self.source_combobox["values"] = ["English"]
            self.target_combobox["values"] = ["Chinese (Traditional)"]
            self.source_combobox.current(0)
            self.target_combobox.current(0)

        self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-16)/2))+"Change Dictionary" +
                ("*"*int((self.linelength-16)/2)+"\n"))
        self.resultbox.insert(tk.END, "="*self.linelength+"\n")




    def dictionary_change_event(self,event):
        self.dictionary_change()
        self.changeText(True)

    def target_combobox_change(self, event):
        self.changeText(True)

    def speak_t(self):
        text = self.translate_result
        language = target_languages[self.target_combobox.get()]
        speak_thread = threading.Thread(target = self.speak_func,args=(language,text))
        speak_thread.start()

    def speak_change(self):
        if self.auto_speak_value.get() == True:
            self.speak()

    def speak_func(self,language,text):
            if language == 'auto':
                language = detect_language.lower()
            try:
                myobj = gTTS(text=text, lang=language.lower(), slow=False)
            except Exception:
                return

            mixer.init()
            mixer.music.unload()
            myobj.save(MP3FILEPATH)
            self.run_speak_file()

    def speak(self):
        text = self.inputbox.get(1.0, tk.END)
        language = source_languages[self.source_combobox.get()]
        speak_thread = threading.Thread(target = self.speak_func,args=(language,text))
        speak_thread.start()

    @staticmethod
    def run_speak_file():
        try:
            mixer.music.set_volume(config['audio_volume'])
            mixer.music.load(MP3FILEPATH)
            mixer.music.play()
        except error:
            return
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
        os.kill(os.getpid(), -9)
        # self.check_clipboard_thread.join()
        # self.root.destroy()

    def printerror(self,error_class):
        self.resultbox.insert(tk.END, ("*"*3)+error_class +("*"*3+"\n"))
        self.resultbox.insert(tk.END, "="*self.linelength+"\n")
        self.resultbox.see(tk.END)

    def reset_clip_event(self):
        self.root.clipboard_append('')
        self.previous_copy=''
        self.now_copy=''

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
                                                            lang='eng+osd+equ').strip()
            elif self.source_combobox.get() == "Chinese":
                self.now_copy = pytesseract.image_to_string(im,
                                                            lang='chi_tra+eng+osd+equ').replace(" ", "").strip()
            else:
                tk.messagebox.showinfo(title=f"Not Support {self.source_combobox.get()}", message="Screenshot Translate only support English, Chinese")
        except Exception as e:
            self.printerror(self.record_error(e))
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-18)/2))+"OCR Error" +
                ("*"*int((self.linelength-18)/2)+"\n"))
            self.resultbox.insert(
                tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            self.root.clipboard_append('')
            return False
        #self.root.clipboard_append('')
        return True

    def get_clipboard(self):
        if win32clipboard.IsClipboardFormatAvailable(CF_TEXT):
            try:
                self.now_copy = self.root.clipboard_get().strip('-= \n')#self.root.selection_get(selection="CLIPBOARD")
            except TclError:
                # self.printerror(self.record_error(te))
                return False
            except Exception as e:
                self.printerror(self.record_error(e))
                self.root.clipboard_append('')
                self.reset_clip_event()
                return False

        elif self.root.state() != 'iconic' and self.screenshot_value.get():
            try:
                im = ImageGrab.grabclipboard()
            except OSError:
                return False
            except Exception as e:
                self.printerror(self.record_error(e))
                self.reset_clip_event()
                return False
            if isinstance(im, Image.Image):
                return self.image_OCR(im)
        return True


    def CheckCopy(self):
        if not self.get_clipboard(): return False
        if self.now_copy == self.previous_copy:
            return False
        if self.now_copy == self.translate_result.strip():
            return False
        if self.now_copy == '':
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

        while True:
            text = self.inputbox.get(1.0, tk.END)
            sleeptime = config["appear_time"]+int((len(text.split(' '))//3)*config['dynamic_adjust_appear_time'])
            self.topagain = False
            for _ in range(sleeptime):
                sleep(1)
                if self.movein:
                    break
            if not self.topagain:
                break

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
        while text[-1] == "@" or text[-1] == ' ' or text[-1]=='\n':
            text = text[:-1]
        while text[0] == "@" or text[0] == ' ' or text[0]=='\n':
            text = text[1:]
        if config["restructure_sentences"]:
            text = self.restructure_sentences(text)
        else:
            text = text.replace("@", "\n")
        return text.rstrip().lstrip()


    def get_translation(self,text):
        try:
            # Google Translate
            result_dict = Translators[self.dictionary_combobox.get()].get_translate(
                    inputtext=text, sourcelanguage=source_languages[self.source_combobox.get()],targetlanguage=target_languages[self.target_combobox.get()])


            if result_dict == None and self.dictionary_combobox.get() != 'Google' :
                self.dictionary_combobox.current(0)
                self.dictionary_change()
                return self.get_translation(text)
            elif result_dict == None:
                return False,None
            return True,result_dict

        except Exception as e:
            self.printerror(self.record_error(e))
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-21)/2))+"Checking WIFI and try again" +
                ("*"*int((self.linelength-21)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            self.top = threading.Thread(target=self.changetop)
            self.top.start()
            self.reset_clip_event()
            return False,None


    def autochange_dictionary(self,text):
        # if not a word change to google because Cambridge can only translate a word
        if len(text.split(' ')) > 1  and self.dictionary_combobox.get() != "Google":
            self.dictionary_combobox.current(0)
            self.dictionary_change()

        # automatic change to google dictionary if input is a word
        elif config["auto_change_dictionary"]  and self.dictionary_combobox.get() == "Google" and len(text.split(' ')) == 1:
            self.dictionary_combobox.current(1)
            self.dictionary_change()


    def get_output_string(self,input_string,result_dict,number_of_terms=config['number_of_terms'],num_sentence_example=config['sentence_example'],definition=config['definition']):
        output_string=[]
        output_string.append('\n※'+'='*(self.linelength-2)+'\n')

        output_string.append(input_string)
        if result_dict['revise']:
            output_string.append('({})\n'.format(result_dict['revise']))
            #self.resultbox.insert(tk.END, '({})\n'.format(result_dict['revise']))

        output_string.append("—"*((int)((self.linelength*1.8)//3))+"\n")

        # print result
        self.translate_result=''
        for iter_result in result_dict['result']:
            output_string.append(iter_result)
            self.translate_result += iter_result+'\n'

            if result_dict['all_result'] != []:
                output_string.append('\n')

        if  result_dict['all_result'] != None and len(result_dict['all_result']) > 0:
            output_string.append('\n')
            # print all result
            for r_idx,iter_result in enumerate(result_dict['all_result']):
                output_string.append('【'+iter_result['pos'].capitalize()+"】:"+"\n")

                terms = iter_result['terms'][:number_of_terms]
                for t_idx,iter_terms in enumerate(terms):
                    output_string.append(iter_terms)
                    if t_idx != len(terms)-1:
                        output_string.append(',')

                if definition and 'definition' in result_dict.keys() and result_dict['definition'] != None and iter_result['pos'] in result_dict['definition'].keys():
                    if result_dict['definition'][iter_result['pos']][0]['detail'] != None:
                        output_string.append('\n●definition\n'+result_dict['definition'][iter_result['pos']][0]['detail'])

                if num_sentence_example and 'definition' in result_dict.keys() and result_dict['definition'] != None and iter_result['pos'] in result_dict['definition'].keys():
                    if result_dict['definition'][iter_result['pos']][0]['example'] != None:
                        output_string.append('\n●example\n'+result_dict['definition'][iter_result['pos']][0]['example'])

                if r_idx != len(result_dict['all_result'])-1:
                    output_string.append('\n\n')

            if num_sentence_example and 'example' in result_dict.keys() and result_dict['example']!= None :
                output_string.append('\n')
                result_dict['example'] = result_dict['example'][:num_sentence_example]
                output_string.append('\n【Examples】')
                for idx,ex in enumerate(result_dict['example']):
                    output_string.append(f'\n{idx+1}.'+ex+'\n')
        output_string.append('\n')
        return output_string

    def changeText(self, click=True):
        global detect_language
        move_virtual_desktop_thread = threading.Thread(target=(Move_window_to_current_desktop()))
        move_virtual_desktop_thread.start()

        self.linelength = int((self.resultbox.winfo_width()/(self.font_size)*1.2))
        output_string=[]
        output_string.append('\n※'+'='*(self.linelength-2)+'\n')

        if not click:
            self.movein = False


        text = self.inputbox.get(1.0, tk.END)

        if not click and not self.changed_language:
            self.autochange_dictionary(text)

        status,result_dict = self.get_translation(text)

        if not status:
            self.clear_button.configure(text = 'Clear')
            return False
        detect_language = result_dict['detect_language']
        # modify text, if the final letter is 's' or 'es', it will be remove, this feature can get more result
        if (detect_language == 'en' or source_languages[self.source_combobox.get()] == 'en') and not click:
            if len(text.split(' ')) == 1 and (result_dict['all_result'] == None or result_dict['all_result']==[]) and text[-2] == 's':
                if text[-3] == 'e' and text[-4] in ['s','o','x','z'] or text[-5:-3] in ['sh','ch']:
                    revise_text = text[:-3]+'\n'
                elif text[-4:-1] == 'ies':
                    revise_text = text[:-4]+'y\n'
                else:
                    revise_text=text[:-2]+'\n'
                _status,_result_dict = self.get_translation(revise_text)
                if (_result_dict['revise'] == None or _result_dict['revise'] =='') and( _result_dict['all_result']  != [] and _result_dict['all_result'] != None):
                    status,result_dict = _status,_result_dict

        self.result_dict=result_dict

        output_string = self.get_output_string(text,result_dict)

        self.resultbox.insert(tk.END,''.join(output_string))
        self.resultbox.see(tk.END)
        self.clear_button.configure(text = 'Clear')

        # Let window top
        if not click and not self.top_value.get():
            self.top = threading.Thread(target=self.changetop)
            self.top.start()

        # auto speak
        if self.auto_speak_value.get() == True:
            audio_text = text.replace('\n',' ')
            if len(audio_text.split(' ')) <= config["auto_speak_length_limit"]:
                text_max_length = max([len(str(t)) for t in audio_text.split(' ')])
                if text_max_length <= config['auto_speak_length_limit']*1.5:
                    self.speak()

        #auto exchange dictionary
        if config['auto_switch_language']:
            if not self.changed_language and detect_language.replace('zh-CN','zh-TW') == target_languages[self.target_combobox.get()] and source_languages[self.source_combobox.get()] != 'auto':
                self.changed_language=True
                self.resultbox.insert(
                        tk.END, ("*"*int((self.linelength-15)/2))+"Exchange Language" +
                        ("*"*int((self.linelength-15)/2)+"\n"))
                self.resultbox.insert(tk.END,"="*self.linelength+"\n")
                self.exchange_language()
                self.changeText(click)

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

    def AddToBook(self):
        input_text=self.inputbox.get(1.0, tk.END).rstrip().lstrip()
        output_string = self.get_output_string(input_text,self.result_dict,number_of_terms=10,num_sentence_example=2,definition=0)[3:]
        output_string=''.join(output_string)
        word_exist=add_to_vocabulary(input_text,output_string)
        if word_exist:
            edit_state=messagebox.askquestion('this word already exists',f'{input_text} already exists, edit or not')
            if edit_state=='yes':
                edit_word(input_text,output_string)

class SettingWindow():

    def __init__(self):
        """Setting Interface."""
        self.root = tk.Tk()
        self.root.wm_attributes('-topmost', 1)
        self.root.title('Setting')
        self.textlist = []
        self.maxlen = max([len(str(v)) for v in config.values()])
        tk.Label(self.root,text='Some setting need to reload the application', justify=tk.LEFT, font=("{} {}".format('Arial', str(config['font_size']))), fg='#FF0000').pack()

        language_frame = tk.Frame(self.root)
        language_frame.pack(fill=(tk.BOTH))
        tk.Label(language_frame,text='Default Source Language', justify=tk.LEFT, font=("{} {}".format('Arial', str(config['font_size'])))).pack( side=tk.LEFT)
        self.source_combobox = ttk.Combobox(language_frame, state="readonly",font=("{} {}".format('Arial', str(config['font_size']))),width=self.maxlen-2)
        self.source_combobox.pack(side=tk.RIGHT)

        language_frame = tk.Frame(self.root)
        language_frame.pack(fill=(tk.BOTH))
        tk.Label(language_frame,text='Default Target Language', justify=tk.LEFT, font=("{} {}".format('Arial', str(config['font_size'])))).pack( side=tk.LEFT)
        self.target_combobox = ttk.Combobox(language_frame, state="readonly",font=("{} {}".format('Arial', str(config['font_size']))), width=self.maxlen-2)
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

        tk.Label(frame,text=key.replace('_',' '), justify=tk.LEFT, font=("{} {}".format('Arial', str(config["font_size"])))).pack( side=tk.LEFT)
        textbox=tk.Text(frame,height=1,width=self.maxlen, font=("{} {}".format('Arial', str(config["font_size"]))))
        textbox.insert(tk.END, str(value))
        textbox.pack( side=tk.RIGHT)

        return textbox



app = MainWindow()
app.closed =True
