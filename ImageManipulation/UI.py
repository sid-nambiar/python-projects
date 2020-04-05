from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image,ImageTk

window = Tk()
window.title("image manipulator")
window.geometry("720x460")

def buttonClicked():
    print("the button was clicked!")
btn = Button(window, text="Click Me",command=buttonClicked)
btn.grid(column=1, row=0)

combo = Combobox(window)
combo['values']= ('blured', 'inverted', 'flipped', 'greyscale', "Text")
combo.current(0)
combo.grid(column=0, row=0)
combo.get()

def wrongButtonClicked():
    messagebox.showinfo('warning!', 'you have entered an invalid value')

alertBtn = Button(window, text="Dont click me!",command=wrongButtonClicked)
alertBtn.grid(column=3, row= 2)

lbl = Label(window, text="Hello, welcome to the image manipulator", font=("Arial Bold", 24))
lbl.grid(column=100, row=100)
window.mainloop()

def createImage(filename):
    load = Image.open(filename)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    return img
dogImage = createImage('dog.png')
dogImage.grid(column=20, row=50)

#file = filedialog.askopenfilename()