# from tkinter import *
# from tkinter import filedialog

# win= Tk()
# win.geometry("750x250")

# menubar=Menu(win)
# win.config(menu=menubar)

# working_dir=StringVar()
# def select_file():
#     global DIR
#     open_file = filedialog.askdirectory()
#     print(open_file)
#     #Label(win, text=open_file, font=13).pack()s
#     DIR=open_file+'/Creo/img'
#     working_dir.set(DIR)

# file_menu=Menu(menubar)
# file_menu.add_command(label='Select working directory', command=select_file)
# menubar.add_cascade(label='File', menu=file_menu)

# Label(win, text='...', textvariable=working_dir, font=13).pack()
# print(working_dir)

# win.mainloop()

import os 

document_path=os.path.expanduser('~\Documents')
print(type(document_path))
print(document_path+'\ruqoyat_simulation')


