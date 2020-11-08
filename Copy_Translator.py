# import pyautogui
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener, Button
from numpy import array
import datetime
import CambridgeTranslate as ct
import pytesseract
from PIL import ImageWin
from PIL import ImageGrab
from PIL import Image
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
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
with open("config.json") as f:
    config = json.loads(f.read())
fontt = config["font"]
fontsize = config["font-size"]
copychecktime = config["copycheck"]
hidetime = config["hide"]
doubleclicktime = config["doubleclick"]
selecttime = config["select"]
googlenotttk = config["googlenotttk"]
automaticchange = config["automaticchange"]
longttk = config["longttk"]
restructureSentences = config["restructureSentences"]


class Test():

    def __init__(self):
        self.root = tk.Tk()
        self.keyboard = Controller()
        self.inputbox = tk.Text(height=3, font=(
            "{} {}".format(str(fontt), str(fontsize))))
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))
        self.resultbox = tk.Text((self.root),
                                 yscrollcommand=(self.scrollbar.set), height=100, font=("{} {}".format(str(fontt), str(fontsize))))
        self.button = tk.Button((self.root), text='Translate',
                                command=(self.changeText))
        self.clearbutton = tk.Button((self.root), text='Clear',
                                     command=(self.ClearText))
        self.inputbox.insert(
            tk.END, 'Try to Copy some Text or take the screenshot for text')
        self.checkvalue = tk.BooleanVar()
        self.checkvalue.set(False)
        self.checktop = tk.Checkbutton((self.root), text='Top', var=(self.checkvalue),
                                       command=(self.checkcange))
        self.checkvalueclick = tk.BooleanVar()
        self.checkvalueclick.set(True)
        self.checkclick = tk.Checkbutton((self.root), text='selected', var=(self.checkvalueclick),
                                         command=(self.checkchangeclick))
        self.combobox = ttk.Combobox(self.root, state="readonly")
        self.combobox["values"] = ["To Chinese", "To English"]
        self.combobox.current(0)
        self.selectcombobox = ttk.Combobox(self.root, state="readonly")
        self.selectcombobox["values"] = ["Google", "Cambridge"]
        self.selectcombobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.combochange)
        self.selectcombobox.bind("<<ComboboxSelected>>", self.combochangedic)
        self.checktop.pack(fill=(tk.BOTH))
        self.checkclick.pack(fill=(tk.BOTH))
        self.combobox.pack(fill=(tk.BOTH))
        self.selectcombobox.pack(fill=(tk.BOTH))
        self.button.pack(fill=(tk.BOTH))
        self.clearbutton.pack(fill=(tk.BOTH))
        self.inputbox.pack(fill=(tk.BOTH))
        self.resultbox.pack(fill=(tk.BOTH))
        self.scrollbar.config(command=(self.resultbox.yview))
        self.nowcopy = ''
        self.movein = False
        self.get_clipboard()
        self.tmpcopy = self.nowcopy
        self.closed = False
        self.dotop = False
        self.topagain = False
        self.root.bind('<Motion>', self.motion)
        self.root.title('Copy Translator')
        self.root.geometry('200x350')
        self.root.protocol('WM_DELETE_WINDOW', self.closewindows)
        self.t = threading.Thread(target=(self.CheckWhile))
        self.clickstarttime = datetime.datetime.now()
        self.clickendtime = datetime.datetime.now()
        self.clickstarttime_tmp = datetime.datetime.now()
        self.clickendtime_tmp = datetime.datetime.now()
        self.muls = Listener(on_click=self.on_click)
        self.muls.start()
        self.t.start()

        self.root.mainloop()

    def combochange(self, event):
        if self.combobox.get() == "To Chinese":
            self.selectcombobox["values"] = ["Google", "Cambridge"]
            self.selectcombobox.current(0)
        else:
            self.selectcombobox.current(0)
            self.selectcombobox["values"] = ["Google"]

    def combochangedic(self, event):
        if self.selectcombobox.get() == "Cambridge":
            self.combobox["values"] = ["English to Chinese"]
            self.combobox.current(0)
        else:
            self.combobox["values"] = ["To Chinese", "To English"]
            self.combobox.current(0)

    def checkchangeclick(self):
        if self.checkvalueclick.get() == True:
            self.muls = Listener(on_click=self.on_click)
            self.muls.start()
        else:
            self.muls.stop()

    def checkcange(self):
        if self.checkvalue.get() == True:
            self.root.wm_attributes('-topmost', 1)
        else:
            self.root.wm_attributes('-topmost', 0)

    def closewindows(self):

        self.closed = True
        if self.checkvalueclick.get() == True:
            self.muls.stop()
        self.t.join()
        self.root.destroy()

    def get_clipboard(self):
        if win32clipboard.IsClipboardFormatAvailable(CF_TEXT):
            try:
                self.nowcopy = self.root.clipboard_get()
            except:
                self.nowcopy = self.tmpcopy
                return False
        else:
            im = ImageGrab.grabclipboard()

            if isinstance(im, Image.Image):
                try:
                    if self.combobox.get() == "English to Chinese" or self.combobox.get() == "To Chinese":
                        self.nowcopy = pytesseract.image_to_string(array(im),
                                                                   lang='eng')
                    else:
                        self.nowcopy = pytesseract.image_to_string((array(im)),
                                                                   lang='chi_tra').replace(" ", "")
                except:
                    # self.resultbox.insert(tk.END, "Psytesseract Error")
                    # self.resultbox.insert(
                    #     tk.END, "\n=========================\n")
                    self.resultbox.insert(
                        tk.END, ("*"*int((self.linelength-18)/2))+"Psytesseract Error" +
                        ("*"*int((self.linelength-18)/2)+"\n"))
                    self.resultbox.insert(
                        tk.END, "="*self.linelength+"\n")
                    self.resultbox.see(tk.END)
                self.root.clipboard_clear()
                self.root.clipboard_append('')

    def CheckCopy(self):
        self.get_clipboard()
        if self.nowcopy == self.tmpcopy:
            return False
        if self.nowcopy.replace(' ', '') == '':
            return False
        self.tmpcopy = self.nowcopy
        self.inputbox.delete(1.0, tk.END)
        self.inputbox.insert(1.0, self.textprocessing(self.nowcopy))
        return True

    def changetop(self):
        if self.dotop:
            self.topagain = True
            return
        self.dotop = True
        self.root.wm_attributes('-topmost', 1)
        l = True
        while l:
            l = False
            sleep(hidetime)
            if self.topagain:
                l = True
            self.topagain = False
        self.dotop = False
        if self.checkvalue.get() == False:
            self.root.wm_attributes('-topmost', 0)
            if self.movein == False:
                self.root.lower()
            else:
                self.movein == False

    def CheckWhile(self):
        while not self.closed:
            if self.CheckCopy():
                self.changet = threading.Thread(
                    target=(self.changeText(False)))
                self.changet.start()
            sleep(copychecktime)

    def restructure_sentences(self, text):
        textlist = text.split('@')
        newsentence = []
        i = 0
        while i < len(textlist):
            textlist[i] = textlist[i].strip()
            if textlist[i] == "":
                del textlist[i]
                i -= 1
            i += 1
        tmpsentence = textlist[0].strip()
        for i in range(1, len(textlist)):
            textlist[i] = textlist[i].strip()
            if textlist[i][-1] == "-":
                textlist[i] = textlist[i][:-1]
            if tmpsentence[-1] == '.' or textlist[i][0] == "•" or textlist[i][0] == "" or re.search('[0-9]:', textlist[i]) != None or tmpsentence[-1] == ":":
                newsentence.append(tmpsentence)
                tmpsentence = textlist[i]
                continue
            tmpsentence += " "+textlist[i]
        newsentence.append(tmpsentence)
        # print(len(newsentence))
        # for i in newsentence:
        #     print("------------"+i+"--------------")
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
        for i in range(len(text)):
            if text[-1] == "@" or text[-1] == ' ':
                text = text[:-1]
            else:
                break
        for i in range(len(text)):
            if text[0] == "@" or text[0] == ' ':
                text = text[1:]
            else:
                break
        if restructureSentences:
            text = self.restructure_sentences(text)
        else:
            text = text.replace("@", "\n")
        return text

    def changeText(self, click=True):
        self.movein = False
        self.linelength = int(self.resultbox.winfo_width()/(fontsize-4)-1)
        text = self.inputbox.get(1.0, tk.END)
        # text = text.replace("@", "\n")
        try:
            if len(text.split(' ')) > 1 and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                self.combochangedic(None)
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")

            # and self.selectcombobox.get() != "Cambridge"
            if automaticchange and not click and self.combobox.get() == "To Chinese" and len(text.split(' ')) == 1:
                self.selectcombobox.current(1)
                self.combochangedic(None)
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-18)/2))+"Change to cambridge" +
                    ("*"*int((self.linelength-18)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")

            if self.selectcombobox.get() == "Google":
                if googlenotttk:
                    result, allresult = gt.get_translate_nottk(
                        text, self.combobox.get())
                else:
                    if longttk and len(text.split(' ')) > 1:
                        result, allresult = gt.get_translate_nottk(
                            text, self.combobox.get())
                    else:
                        result, allresult = gt.get_translate(
                            text, self.combobox.get())
            else:
                result, allresult = ct.get_translate(text)
            if result == "" and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                self.combochangedic(None)
                result, allresult = gt.get_translate(text, self.combobox.get())
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")

        except:
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-21)/2))+"Check WIFI and try again" +
                ("*"*int((self.linelength-21)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            self.top = threading.Thread(target=self.changetop)
            self.top.start()
            return False
        if not self.checkvalue.get():
            self.top = threading.Thread(target=self.changetop)
            self.top.start()
        self.resultbox.insert(tk.END, text)
        self.resultbox.insert(
            tk.END, "-"*self.linelength+"\n")
        for i in result:
            self.resultbox.insert(tk.END, i)
            if allresult != []:
                self.resultbox.insert(tk.END, "\n")
        if len(allresult) > 0:
            self.resultbox.insert(tk.END, "\n")
        for i in range(len(allresult)):
            allresult[i]['name'] = allresult[i]['name'].replace(
                '動詞', '動  詞').replace('名詞', '名  詞').replace('代名  詞', '代名詞').replace('副詞', '副  詞')
            self.resultbox.insert(tk.END, allresult[i]['name']+":")
            v = allresult[i]['value'][:4]
            for j in range(len(v)):
                self.resultbox.insert(tk.END, v[j])
                if j != len(v)-1:
                    self.resultbox.insert(tk.END, ",")
            if i != len(allresult)-1:
                self.resultbox.insert(tk.END, "\n")
            if self.selectcombobox.get() != "Google":
                self.resultbox.insert(tk.END, "\n")
        self.resultbox.insert(tk.END, "\n"+"="*self.linelength+"\n")
        self.resultbox.see(tk.END)

    def motion(self, event):
        self.movein = True

    def copyclick(self):
        # pyautogui.hotkey('ctrl', 'c')
        with self.keyboard.pressed(Key.ctrl):
            self.keyboard.press('c')
            self.keyboard.release('c')

    def on_click(self, x, y, button, pressed):
        if button == Button.left and pressed == True:
            self.clickstarttime = datetime.datetime.now()
        if button == Button.left and pressed == False:
            self.clickendtime_tmp = datetime.datetime.now()
            # print((self.clickendtime_tmp - self.clickendtime).total_seconds())
            if (self.clickendtime_tmp - self.clickendtime).total_seconds() < doubleclicktime:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            elif (self.clickendtime_tmp - self.clickstarttime).total_seconds() > selecttime:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            else:
                self.clickendtime = self.clickendtime_tmp

        if self.closed:
            return False

    def ClearText(self):
        self.resultbox.delete(0.0, tk.END)


app = Test()
