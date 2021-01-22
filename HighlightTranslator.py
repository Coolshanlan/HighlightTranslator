# import pyautogui
# -*- coding: utf-8 -*-
from pynput.keyboard import Key, Controller
from pynput.mouse import Listener, Button
from datetime import date
from datetime import datetime
import win32con
import win32api
import datetime
import traceback
import CambridgeTranslate as ct
import pytesseract
from PIL import ImageWin
from PIL import ImageGrab
from PIL import Image, ImageOps
import sys
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
# import pyautogui
# program setting
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
with open("config.json") as f:
    config = json.loads(f.read())
# Now, OCR only support these four languages, you can add another language from tesseract
tesseract_languages=["eng","chi_tra","kor","jpn"]
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
inputboxcolor = config["inputboxcolor"]
resultboxcolor = config["resultboxcolor"]
defaultsourcelanguage = config["sourcelanguage"]
defaulttargetlanguage = config["targetlanguage"]

#Read language from language.txt
sourcelanguagelist={}
targetlanguagelist={}
with open("language.txt") as f:
    languagelist = eval(f.read())
for i in range(len(languagelist[0])):
    sourcelanguagelist[languagelist[0][i][1]] = languagelist[0][i][0]
for i in range(len(languagelist[1])):
    targetlanguagelist[languagelist[1][i][1]] = languagelist[1][i][0]
class MainWindow():

    def __init__(self):
        self.root = tk.Tk()
        self.fontsize =fontsize
        self.setWindowsSize()# Auto resizing
        self.keyboard = Controller()# keyboard hook

        self.inputbox = tk.Text(height=3, font=("{} {}".format(str(fontt), str(self.fontsize))))
        self.inputbox.insert(tk.END, 'Try to copy/highlight some Text or take the screenshot for text')
        self.inputbox.configure(bg=inputboxcolor)#82A0C2#FDF0C4

        self.displayinputboxvalue = tk.BooleanVar()
        self.displayinputboxvalue.set(False)
        self.displayinputbox = tk.Checkbutton((self.root), text='Input Box', var=(self.displayinputboxvalue),command=self.displayinputbox)

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))

        self.resultbox = tk.Text((self.root),yscrollcommand=(self.scrollbar.set), height=100, font=("{} {}".format(str(fontt), str(self.fontsize))))
        self.resultbox.configure(bg=resultboxcolor)#82A0C2#FDF0C4

        self.translatebutton = tk.Button((self.root), text='Translate',command=(self.changeText))

        self.clearbutton = tk.Button((self.root), text='Clear',command=(self.ClearText))

        self.comboboxframe =tk.Frame(self.root)
        self.sourcecombobox = ttk.Combobox(self.comboboxframe, state="readonly", width=10)
        self.targetcombobox = ttk.Combobox(self.comboboxframe, state="readonly", width=10)

        self.checkvalue = tk.BooleanVar()
        self.checkvalue.set(False)
        self.checktop = tk.Checkbutton((self.root), text='Top', var=(self.checkvalue),command=(self.checkchange))

        self.highlightcheckvalue = tk.BooleanVar()
        self.highlightcheckvalue.set(True)
        self.highlightcheckbox = tk.Checkbutton((self.root), text='highlight', var=(self.highlightcheckvalue),command=(self.changehighlightclick))

        self.selectcombobox = ttk.Combobox(self.root, state="readonly")
        self.setuplanguageitem()
        self.selectcombobox["values"] = ["Google", "Cambridge"]
        self.selectcombobox.current(0)
        self.selectcombobox.bind("<<ComboboxSelected>>", self.combochangedict)

        self.checktop.pack()
        self.highlightcheckbox.pack()
        self.displayinputbox.pack()
        self.selectcombobox.pack(fill=(tk.BOTH))
        self.sourcecombobox.pack(fill=(tk.BOTH),expand=True, side=tk.LEFT)
        self.targetcombobox.pack( fill=(tk.BOTH),expand=True,side=tk.RIGHT)
        self.comboboxframe.pack(fill=(tk.BOTH))
        self.translatebutton.pack(fill=(tk.BOTH))
        self.clearbutton.pack(fill=(tk.BOTH))
        self.inputbox.pack(fill=(tk.BOTH))
        self.resultbox.pack(fill=(tk.BOTH))
        self.scrollbar.config(command=(self.resultbox.yview))

        self.inputbox.pack_forget()
        self.translatebutton.pack_forget()
        # if mouse move in windowns, cancel auto hide windows function
        self.movein = False
        self.dotop = False
        self.topagain = False

        self.linelength = int((self.resultbox.winfo_width()/(self.fontsize-4*(self.fontsize/11))-1))
        self.nowcopy = ''
        self.tmpcopy = ''
        # self.check_clipboard()
        # self.tmpcopy = self.nowcopy

        #close threads when window closed
        self.closed = False

        self.root.bind('<Motion>', self.motion)
        self.root.title('Highlight Translator')
        self.root.protocol('WM_DELETE_WINDOW', self.closewindows)


        #check is it double click or not
        self.clickstarttime = datetime.datetime.now()
        self.clickendtime = datetime.datetime.now()
        self.clickstarttime_tmp = datetime.datetime.now()
        self.clickendtime_tmp = datetime.datetime.now()
        # check finction
        self.muls = Listener(on_click=self.mouseclick)
        self.muls.start()

        # check clipboard change or not
        self.t = threading.Thread(target=(self.CheckCopyWhile))
        self.t.start()



        self.root.mainloop()


    def setWindowsSize(self):
        originX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        originY =win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        scaleX = originX/1280
        scaleY = originY/720
        self.fontsize = int(self.fontsize*scaleX)
        self.root.geometry('{}x{}'.format((int)(200*scaleX),(int)(320*scaleY)))


    def setuplanguageitem(self):
         self.sourcecombobox["values"] = sorted(sourcelanguagelist.keys())
         self.targetcombobox["values"] = sorted(targetlanguagelist.keys())
         self.sourcecombobox.current(self.sourcecombobox["values"].index(defaultsourcelanguage))
         self.targetcombobox.current(self.targetcombobox["values"].index(defaulttargetlanguage))


    def displayinputbox(self):
        if self.displayinputboxvalue.get() == True:
            self.resultbox.pack_forget()
            self.translatebutton.pack(fill=(tk.BOTH))
            self.inputbox.pack(fill=(tk.BOTH))
            self.resultbox.pack(fill=(tk.BOTH))
        else:
            self.inputbox.pack_forget()
            self.translatebutton.pack_forget()


    def combochangedict(self, event):
        if self.selectcombobox.get() == "Cambridge":
            self.sourcecombobox["values"] = ["English"]
            self.targetcombobox["values"] = ["Chinese (Traditional)"]
            self.sourcecombobox.current(0)
            self.targetcombobox.current(0)
        else:
            self.setuplanguageitem()
        self.changeText(False)


    def changehighlightclick(self):
        if self.highlightcheckvalue.get() == True:
            self.muls = Listener(on_click=self.mouseclick)
            self.muls.start()
        else:
            self.muls.stop()


    def checkchange(self):
        if self.checkvalue.get() == True:
            self.root.wm_attributes('-topmost', 1)
        else:
            self.root.wm_attributes('-topmost', 0)


    def closewindows(self):

        self.closed = True
        if self.highlightcheckvalue.get() == True:
            self.muls.stop()
        self.t.join()
        self.root.destroy()

    def printerror(self,e):
        with open("log.txt","a") as f:
            now = date.today()
            current_time = now.strftime("%m/%d/%Y")
            now = datetime.datetime.now()
            current_time += " "+ now.strftime("%H:%M:%S")
            print(current_time)
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}:\n [{}]\n{}".format(fileName, lineNum, funcName, error_class, detail)
            f.writelines(str(current_time)+"\n")
            f.writelines(errMsg+"\n")
            f.writelines("-------------------------"+"\n")
            self.resultbox.insert(tk.END, ("*"*3)+error_class +("*"*3+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            return error_class


    def binarization(self, image,threshold = 200):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return image.point(table, '1')
        # print(errMsg)


    def check_clipboard(self):
        if win32clipboard.IsClipboardFormatAvailable(CF_TEXT):
            try:
                self.nowcopy = self.root.selection_get(selection="CLIPBOARD")#clipboard_get()
            except Exception as e:
                self.printerror(e)
                self.root.clipboard_append('')
                self.nowcopy = self.tmpcopy
                return False
        elif self.root.state() != 'iconic':
            try:
                im = ImageGrab.grabclipboard()
            except OSError:
                return False
            except Exception as e:
                print(e)
                self.printerror(e)
                self.root.clipboard_clear()
                self.root.clipboard_append('')
                return False
            if isinstance(im, Image.Image):
                try:
                    im = ImageOps.grayscale(im)
                    # im = self.binarization(im,225)
                    # im.save('tmp.png')
                    if self.sourcecombobox.get() =="Detect language":
                        self.nowcopy = pytesseract.image_to_string(im,
                                                                   lang='eng')
                    elif self.sourcecombobox.get() == "English" or self.sourcecombobox.get() =="Detect language":
                        self.nowcopy = pytesseract.image_to_string(im,
                                                                   lang='eng')
                    elif self.sourcecombobox.get() == "Chinese":
                        self.nowcopy = pytesseract.image_to_string(im,
                                                                   lang='chi_tra').replace(" ", "")
                    elif self.sourcecombobox.get() == "Korean":
                        self.nowcopy = pytesseract.image_to_string(im,
                                                                   lang='kor+kor_vert').replace(" ", "")
                    elif self.sourcecombobox.get() == "Japanese":
                        self.nowcopy = pytesseract.image_to_string(im,
                                                                   lang='jpn').replace(" ", "")

                    else:
                        tk.messagebox.showinfo(title=f"Not Support {self.sourcecombobox.get()}", message="Screenshot Translate only support English and Chinese")
                except Exception as e:
                    self.printerror(e)
                    self.resultbox.insert(
                        tk.END, ("*"*int((self.linelength-18)/2))+"Psytesseract Error" +
                        ("*"*int((self.linelength-18)/2)+"\n"))
                    self.resultbox.insert(
                        tk.END, "="*self.linelength+"\n")
                    self.resultbox.see(tk.END)
                    return False
                self.root.clipboard_clear()
                self.root.clipboard_append('')

        return True

    def CheckCopy(self):
        if not self.check_clipboard(): return False
        if self.nowcopy == self.tmpcopy:
            return False
        if self.nowcopy.strip() == '':
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


    def CheckCopyWhile(self):
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
        self.linelength = int((self.resultbox.winfo_width()/(self.fontsize)*1.2))
        text = self.inputbox.get(1.0, tk.END)
        try:
            # if not a word change to google because Cambridge can only translate a word
            if len(text.split(' ')) > 1 and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                self.combochangedict(None)
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            # automatic change to google dictionary if input is a word
            if automaticchange and not click and self.selectcombobox.get() != "Google" and len(text.split(' ')) == 1:
                self.selectcombobox.current(1)
                self.combochangedict(None)
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-18)/2))+"Change to cambridge" +
                    ("*"*int((self.linelength-18)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")

            # Google Translate
            if self.selectcombobox.get() == "Google":
                if googlenotttk:
                    result, allresult = gt.get_translate_nottk(
                        text, sourcelanguagelist[self.sourcecombobox.get()],targetlanguagelist[self.targetcombobox.get()])
                else:
                    if longttk and len(text.split(' ')) > 1:
                        result, allresult = gt.get_translate_nottk(
                            text, sourcelanguagelist[self.sourcecombobox.get()],targetlanguagelist[self.targetcombobox.get()])
                    else:
                        result, allresult = gt.get_translate(
                            text, sourcelanguagelist[self.sourcecombobox.get()],targetlanguagelist[self.targetcombobox.get()])
            else:
                result, allresult = ct.get_translate(text)
            if result == "" and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                self.combochangedict(None)
                result, allresult = gt.get_translate(text, sourcelanguagelist[self.sourcecombobox.get()],targetlanguagelist[self.targetcombobox.get()])
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")
        except Exception as e:
            self.printerror(e)
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
            tk.END, "-"*((int)(self.linelength*1.8))+"\n")
        for i in result:
            self.resultbox.insert(tk.END, i)
            if allresult != []:
                self.resultbox.insert(tk.END, "\n")
        if len(allresult) > 0:
            self.resultbox.insert(tk.END, "\n")
        for i in range(len(allresult)):
            allresult[i]['name'] = allresult[i]['name'].replace(
                '動詞', '動  詞').replace('名詞', '名  詞').replace('代名  詞', '代名詞').replace('副詞', '副  詞')
            self.resultbox.insert(tk.END, allresult[i]['name'].capitalize()+":"+"\n")
            v = allresult[i]['value'][:4]
            for j in range(len(v)):
                self.resultbox.insert(tk.END, v[j])
                if j != len(v)-1:
                    self.resultbox.insert(tk.END, ",")
            if i != len(allresult)-1:
                self.resultbox.insert(tk.END, "\n")
                self.resultbox.insert(tk.END, "\n")
            # if self.selectcombobox.get() != "Google":
            #     self.resultbox.insert(tk.END, "\n")
        self.resultbox.insert(tk.END, "\n"+"="*self.linelength+"\n")
        self.resultbox.see(tk.END)


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

app = MainWindow()
app.closed =True
