from Tkinter import *
import Image
import ImageTk
import numpy as np
import tkFileDialog
import ttk

class DIP(Frame):
    def __init__(self):
        self.root = Tk()
        Frame.__init__(self, self.root)

        self.initUI()

    def initUI(self):

        self.pack(fill = tk.BOTH, expand = 1)

        menubar = Menu(self.root)


        self.label1 = ttk.Label(self, border = 25)
        self.label2 = ttk.Label(self, border = 25)
        print self.label1, self.label2
        self.label1.grid(row = 1, column = 1)
        self.label2.grid(row = 1, column = 2)

        #Open Image Menu
        fileMenu = Menu(menubar)
        fileMenu.add_command(label = "Open", command = self.onOpen)
        menubar.add_cascade(label = "File", menu = fileMenu)


    def setImage(self):
        self.img = Image.open(self.fn)
        self.I = np.asarray(self.img)
        l, h = self.img.size
        text = str(2*l+100)+"x"+str(h+50)+"+0+0"
        self.root.geometry(text)
        photo = ImageTk.PhotoImage(self.img)
        print self.label1
        self.label1.configure(image = photo)
        self.label1.image = photo # keep a reference!

    def onOpen(self):
        #Open Callback
        ftypes = [('Image Files', '*.tif *.jpg *.png')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        filename = dlg.show()
        self.fn = filename
        #print self.fn #prints filename with path here
        self.setImage()

def main():


    dip = DIP()
    dip.root.geometry("320x240")
    dip.root.mainloop()


if __name__ == '__main__':
    main()