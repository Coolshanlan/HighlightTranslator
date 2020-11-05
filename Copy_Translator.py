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
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'


class Test():

    def __init__(self):
        self.root = tk.Tk()
        self.keyboard = Controller()
        self.inputbox = tk.Text(height=3)
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))
        self.resultbox = tk.Text((self.root),
                                 yscrollcommand=(self.scrollbar.set))
        self.button = tk.Button((self.root), text='Translate',
                                command=(self.changeText))
        self.clearbutton = tk.Button((self.root), text='Clear',
                                     command=(self.ClearText))
        self.inputbox.insert(
            tk.END, 'Try to Copy some Text or capture the screenshot')
        self.checkvalue = tk.BooleanVar()
        self.checkvalue.set(False)
        self.checktop = tk.Checkbutton((self.root), text='Top', var=(self.checkvalue),
                                       command=(self.checkcange))
        self.checkvalueclick = tk.BooleanVar()
        self.checkvalueclick.set(True)
        self.checkclick = tk.Checkbutton((self.root), text='selected', var=(self.checkvalueclick),
                                         command=(self.checkchangeclick))
        self.combobox = ttk.Combobox(self.root, state="readonly")
        self.combobox["values"] = ["English to Chinese", "Chinese to English"]
        self.combobox.current(0)
        self.selectcombobox = ttk.Combobox(self.root, state="readonly")
        self.selectcombobox["values"] = ["Google", "Cambridge"]
        self.selectcombobox.current(0)
        self.combobox.bind("<<ComboboxSelected>>", self.combochange)
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
        self.get_clipboard()
        self.tmpcopy = self.nowcopy
        self.closed = False
        self.dotop = False
        self.topagain = False
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
        if self.combobox.get() == "English to Chinese":
            self.selectcombobox["values"] = ["Google", "Cambridge"]
            self.selectcombobox.current(0)
        else:
            self.selectcombobox.current(0)
            self.selectcombobox["values"] = ["Google"]

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
        # self.muls.join()
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
                    if self.combobox.get() == "English to Chinese":
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
        self.inputbox.insert(1.0, self.nowcopy)
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
            sleep(3)
            if self.topagain:
                l = True
            self.topagain = False
        self.dotop = False
        if self.checkvalue.get() == False:
            self.root.wm_attributes('-topmost', 0)
            self.root.lower()

    def CheckWhile(self):
        while not self.closed:
            if self.CheckCopy():
                self.changet = threading.Thread(target=(self.changeText()))
                self.changet.start()
            sleep(0.3)

    def changeText(self):
        self.linelength = int(self.resultbox.winfo_width()/7-1)
        text = self.inputbox.get(1.0, tk.END).replace(
            '\r', '').replace('¡', '').replace('¦', '').replace("\n", "@").replace("\t", "").replace("\x00", "").replace(' – ', '-').replace("     ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("  ", " ")
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
        text = text.replace("@", "\n")
        try:
            if len(text.split(' ')) > 1 and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            if self.selectcombobox.get() == "Google":
                result, allresult = gt.get_translate(text, self.combobox.get())
            else:
                result, allresult = ct.get_translate(text)
            if result == "" and self.selectcombobox.get() != "Google":
                self.selectcombobox.current(0)
                result, allresult = gt.get_translate(text, self.combobox.get())
                self.resultbox.insert(
                    tk.END, ("*"*int((self.linelength-16)/2))+"Change to google" +
                    ("*"*int((self.linelength-16)/2)+"\n"))
                self.resultbox.insert(tk.END, "="*self.linelength+"\n")
        except:
            self.resultbox.insert(
                tk.END, ("*"*int((self.linelength-13)/2))+"Requert Error" +
                ("*"*int((self.linelength-13)/2)+"\n"))
            self.resultbox.insert(tk.END, "="*self.linelength+"\n")
            self.resultbox.see(tk.END)
            return False
        if not self.checkvalue.get():
            self.top = threading.Thread(target=self.changetop)
            self.top.start()
        self.resultbox.insert(tk.END, text+"\n")
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
            if (self.clickendtime_tmp - self.clickendtime).total_seconds() < 0.6:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            elif (self.clickendtime_tmp - self.clickstarttime).total_seconds() > 0.3:
                self.clickendtime = self.clickendtime_tmp
                self.copyclick()
            else:
                self.clickendtime = self.clickendtime_tmp

        if self.closed:
            return False

    def ClearText(self):
        self.resultbox.delete(0.0, tk.END)


app = Test()
