import tkinter as tk
from tkinter import ttk
import win32clipboard
import win32con
import threading
import time
import GoogleTranslate as gt
import os
from PIL import Image
from PIL import ImageGrab
import pytesseract
import numpy as np
pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'


class Test():

    def __init__(self):
        self.root = tk.Tk()
        self.inputbox = tk.Text(height=3)
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side=(tk.RIGHT), fill=(tk.Y))
        self.resultbox = tk.Text((self.root),
                                 yscrollcommand=(self.scrollbar.set))
        self.button = tk.Button((self.root), text='Click to Translate',
                                command=(self.changeText))
        self.clearbutton = tk.Button((self.root), text='Clear',
                                     command=(self.ClearText))
        self.inputbox.insert(
            tk.END, 'Result from google translator\nTry to Copy some Text')
        self
        self.checkvalue = tk.BooleanVar()
        self.checkvalue.set(False)
        self.checktop = tk.Checkbutton((self.root), text='Top', var=(self.checkvalue),
                                       command=(self.checkcange))
        self.combobox = ttk.Combobox(self.root)
        self.combobox["values"] = ["English to Chinese", "Chinese to English"]
        self.combobox.current(0)
        self.checktop.pack(side=(tk.TOP), fill=(tk.BOTH))
        self.combobox.pack(side=(tk.TOP), fill=(tk.BOTH))
        self.button.pack(side=(tk.TOP), fill=(tk.BOTH))
        self.clearbutton.pack(fill=(tk.BOTH))
        self.inputbox.pack()
        self.resultbox.pack(side=(tk.RIGHT), fill=(tk.BOTH))
        self.scrollbar.config(command=(self.resultbox.yview))
        self.nowcopy = ''
        self.get_clipboard()
        self.tmpcopy = self.nowcopy
        self.closed = False
        self.root.title('Copy Translator')
        self.root.geometry('200x350')
        self.root.protocol('WM_DELETE_WINDOW', self.closewindows)
        self.t = threading.Thread(target=(self.CheckWhile))
        self.t.start()
        self.root.mainloop()

    def checkcange(self):
        if self.checkvalue.get() == True:
            self.root.wm_attributes('-topmost', 1)
        else:
            self.root.wm_attributes('-topmost', 0)

    def closewindows(self):
        self.closed = True
        self.t.join()
        self.root.destroy()

    def get_clipboard(self):
        if win32clipboard.IsClipboardFormatAvailable(win32con.CF_TEXT):
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
                        self.nowcopy = pytesseract.image_to_string((np.array(im)),
                                                                   lang='eng')
                    else:
                        self.nowcopy = pytesseract.image_to_string((np.array(im)),
                                                                   lang='chi_tra').replace(" ", "")
                except:
                    self.resultbox.insert(tk.END, "Psytesseract Error")
                    self.resultbox.insert(
                        tk.END, "\n=========================\n")
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
        self.root.wm_attributes('-topmost', 1)
        time.sleep(1)
        self.root.wm_attributes('-topmost', 0)

    def CheckWhile(self):
        while not self.closed:
            if self.CheckCopy():
                self.changet = threading.Thread(target=(self.changeText()))
                self.changet.start()
            time.sleep(1)

    def changeText(self):
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
            result, allresult = gt.get_translate(text, self.combobox.get())
        except:
            self.resultbox.insert(tk.END, "Error")
            self.resultbox.insert(tk.END, "\n=========================\n")
            return False
        self.top = threading.Thread(target=self.changetop)
        self.top.start()
        self.resultbox.insert(tk.END, text+"\n")
        self.resultbox.insert(tk.END, "-------------------------\n")
        for i in result:
            self.resultbox.insert(tk.END, i)
            if allresult != []:
                self.resultbox.insert(tk.END, "\n")
        if len(allresult) > 0:
            self.resultbox.insert(tk.END, "\n")
        for i in range(len(allresult)):
            allresult[i]['name'] = allresult[i]['name'].replace(
                '動詞', '動  詞').replace('名詞', '名  詞').replace('副詞', '副  詞')
            self.resultbox.insert(tk.END, allresult[i]['name']+":")
            v = allresult[i]['value'][:4]
            for j in range(len(v)):
                self.resultbox.insert(tk.END, v[j])
                if j != len(v)-1:
                    self.resultbox.insert(tk.END, ",")
            if i != len(allresult)-1:
                self.resultbox.insert(tk.END, "\n")
        self.resultbox.insert(tk.END, "\n=========================\n")
        self.resultbox.see(tk.END)

    def ClearText(self):
        self.resultbox.delete(0.0, tk.END)


app = Test()
