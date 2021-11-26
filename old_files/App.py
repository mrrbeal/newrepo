import os,sys
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno, askquestion
#from tkinter.ttk import *
from tkscrolledframe import ScrolledFrame
#from typing import Container, Counter, Text
from PIL import Image, ImageTk
from Data.Frame_Categories import Categories as Categories
from Data.Frame_Playlists import Playlists as Playlists
from Data.Frame_Files import Files as Files
import Data.Database as Database
from Data.Utils import Utilities as Utilities




#import Data.MediaDataBase as Database, Data.Frame_Playlists as Playlists, Data.Frame_Categories as Categories, Data.Frame_Files as Files
import win32api


class MediaOrganiser(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Whizzy Media Organiser")
        self.geometry("1400x750+10+10")
        self.minsize(400,600)
        self.colourPalette = {"nero": "#252726",
                            "orange": "#FF8700",
                            "lightgrey": "#e0e0e0", 
                            "lightblue" : '#36c3d9',
                            "darkblue" : "#42618a"}
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # determine if application is a script file or frozen exe
        if getattr(sys, 'frozen', False):
            self.dname = os.path.dirname(sys.executable)
        elif __file__:
            self.dname = os.path.dirname(__file__)

        self.last_file = Utilities.load_system_config()
        if self.last_file != "None":
            self.current_session_state = Utilities.load_save_file(self.last_file)
        else: 
            self.current_session_state = None
            answer = askyesno("Load a State", "There isnt a State loaded \n Do you want to load one ?")
            if answer != "" or answer != None:
                self.last_file = select_file()
                print(self.last_file)
                self.current_session_state = Utilities.load_state_file(self.last_file)


        self.database = Database.MediaDataBase("cheese1.db",self.current_session_state)
        #self.database = Database.MediaDataBase(self.dname + r"\Data\system_database.db")
            
  
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others

        headerFrame = tk.Frame(self, bg=self.colourPalette["darkblue"], height=50, width=1400, highlightbackground="black",highlightthickness=1)
        headerFrame.place(x=0, y=0)
        #self.logoImage = ImageTk.PhotoImage(Image.open('logo.png').resize((110,110),Image.ANTIALIAS))
        logoLabel = tk.Label(headerFrame, text="MEDIA ORGANISER", bg=self.colourPalette["darkblue"])
        logoLabel.config(font=("stencil", 30),fg="white")
        logoLabel.place(x=0, y=-1)
        headerLabel = tk.Label(headerFrame, text="HEADERLABEL", bg=self.colourPalette["darkblue"],font=self.title_font)
        headerLabel.place(x=700, y=75)


        sideMenu = tk.Frame(self, bg=self.colourPalette["darkblue"], height=700, width=150, highlightbackground="black",highlightthickness=1)
        sideMenu.place(x=0, y=50)
        #sideMenu.grid_propagate(0)
        #options = ["Files", "playlists", "settings", "Help", "About"]
        # Navbar Option Buttons:
        #y = 40
        #for i in range(5):
         #   action = lambda x = options[i]: self.show_frame(x)
          #  tk.Button(sideMenu, text=options[i],command=action, font="BahnschriftLight 15", bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).place(x=25, y=y)
          #  y += 60

        #action = lambda x = options[i]: self.show_frame(x)

### Set up side menu buttons start ################################
        tk.Button(sideMenu, text="Files",command=lambda x = "Files": self.show_frame(x), font="BahnschriftLight 15", 
                    bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=0, columnspan=2)
        self.playlist_frame = ToggledFrame(sideMenu, self, text='playlists')
        self.playlist_frame.mainLabel.config(font="BahnschriftLight 15", bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0)
        self.playlist_frame.grid(column=0,row=1, columnspan=2)
        tk.Button(sideMenu, text="Categories",command=lambda x = "Categories": self.show_frame(x), font="BahnschriftLight 15",
                     bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=2, columnspan=2)
        tk.Button(sideMenu, text="Help",command=lambda x = "Files": self.show_frame(x), font="BahnschriftLight 15", 
                    bg=self.colourPalette["darkblue"], fg="white", activebackground=self.colourPalette["darkblue"], activeforeground="black", bd=0).grid(column=0,row=3, columnspan=2)
### Set up side menu buttons end ##################################

        row = 4
        for i in range(27):
            tk.Label(sideMenu, text="this is nonsence text",bg=self.colourPalette["darkblue"],fg=self.colourPalette["darkblue"]).grid(column=1,row=row)
            row +=1

        container = tk.Frame(self)
        container.place(x=150, y=50)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Categories, Playlists, Files):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame("Files")

    # def show_frame(self, page_name):
    #     '''Show a frame for the given page name'''
    #     frame = self.frames[page_name]
    #     frame.tkraise()

    def show_frame(self, page_name):
        for frame in self.frames.values():
            frame.grid_remove()
        frame = self.frames[page_name]
        frame.grid()
    
    def get_page(self, page_class):
        return self.frames[page_class]

def select_file(tupletypes= None):
    
    if tupletypes == None:
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )
    else:
        filetypes = tupletypes

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    return filename



class ToggledFrame(tk.Frame):

    def __init__(self, parent, controller, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.controller = controller
        self.title_frame = tk.Frame(self,background=controller.colourPalette["darkblue"])
        self.title_frame.pack(fill="x", expand=1)

        self.mainLabel = tk.Button(self.title_frame, text=text,command=self.changeFrame)
        self.mainLabel.pack(side="left", fill="x", expand=1)
        self.frame_State = 0
        #self.toggle_button = ttk.Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
        #                                     variable=self.show, style='Toolbutton')
        self.toggle_button = tk.Button(self.title_frame, text="+",height=1,width=1,bd=0, command=self.toggle)
        self.toggle_button.pack(side="left")

        self.sub_frame = ScrolledFrame(self, relief="sunken", borderwidth=1,background=controller.colourPalette["darkblue"],width=97, height=150)
        self.inner_frame = self.sub_frame.display_widget(tk.Frame)


    def changeFrame(self):
        self.controller.show_frame("Playlists")
        if self.frame_State == 0:
            self.toggle()


    def toggle(self):
        self.frame_State = not self.frame_State
        if bool(self.frame_State):
            self.sub_frame.pack(side="top",fill="both", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')






if __name__ == "__main__":
    app = MediaOrganiser()
    app.mainloop()