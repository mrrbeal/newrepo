import tkinter as tk
import PIL
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import filedialog as fd
import win32api
import tkinter.simpledialog

def DEBUG(text):
    if DEBUGON == True:
        print("Files:\n",text)

DEBUGON = True

class Files(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_propagate(False)
        self.config(width=1200,height=700)
        DEBUG("Loading Widgets")
        #add widgets to the frame
        self.searchBar = tk.Entry(self,font=controller.title_font)
        self.searchBar.grid(column=0,row=0,columnspan=3, pady=25,padx= 50)
        self.searchBar.insert(0, '--Search Files--')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<FocusOut>", lambda args: self.searchBar.insert(0, '--Search Files--') if len(self.searchBar.get()) < 1 else 1+1)
        self.searchBar.bind("<KeyRelease>", lambda args: self.populateTable(self.searchBar.get()))
        button_addFiles = tk.Button(self, text="Add Files", command=self.add_files).grid(column=0,row=1,sticky='W')
        button_deleteFiles = tk.Button(self, text="Delete File", command=lambda: self.delete_treeItem()).place(x=435,y=78)

        #add pop ups for right clicking table
        self.popup = tk.Menu(self, tearoff=0)
        self.popup.add_command(label="Add to Playlist",command=lambda: self.playlistPopup())
        self.popup.add_separator()
        self.popup.add_command(label="")
        self.popup.add_command(label="Exit", command=lambda: self.closeWindow())
        #secondary popup
        self.playpopup = tk.Menu(self, tearoff=0)

    
        #style for table
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=30,
        fieldbackground="#D3D3D3",
        height=800)
        style.map("Treeview", background=[("selected","#347083")])
        #set up table frame and pack table
        tree_frame= tk.Frame(self)
        tree_frame.grid(column=0, row=3, columnspan=3, pady=10)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()
        tree_scroll.config(command=self.tree.yview)
        #add columns
        self.tree["columns"] = ("FileID", "FileName", "FileType")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("FileID", anchor="center", width=40)
        self.tree.column("FileName", anchor="center", width=400)
        self.tree.column("FileType", anchor="center", width=60)
        #add column headers
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("FileID", text="File ID", anchor="center")
        self.tree.heading("FileName", text="File Name", anchor="center")
        self.tree.heading("FileType", text="File Type", anchor="center")
        #set up tags for table colour
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

        #bind right click to pop up menu, left click to populate right hand boxes
        self.tree.bind("<Button-3>", self.do_popup)
        self.tree.bind("<Button-1>", self.fill_view_edit)

        #frame for right hand boxes
        view_editFrame = tk.Frame(self,width=550,height=1000)
        view_editFrame.place(x=550,y=115)
        view_editFrame.grid_propagate(0)
        #set up all labels
        view_edit_label = tk.Label(view_editFrame,text="View or edit file details below:",font=controller.label_font).place(x=0,y=0)
        view_edit_label_fileName = tk.Label(view_editFrame,text="File Name:")
        view_edit_label_fileName.place(x=0,y=45)
        view_edit_label_fileType = tk.Label(view_editFrame,text="File Type:")
        view_edit_label_fileType.place(x=0,y=75)
        view_edit_label_filePath = tk.Label(view_editFrame,text="File Path:")
        view_edit_label_filePath.place(x=0,y=105)
        view_edit_label_commentBox = tk.Label(view_editFrame,text="Comment:")
        view_edit_label_commentBox.place(x=0,y=135)
        view_edit_label_category = tk.Label(view_editFrame,text="Category:")
        view_edit_label_category.place(x=0,y=260)
    
        #set up interactive widgets
        self.view_edit_entry_fileName = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileName.place(x=80,y=45,width=200)
        self.view_edit_entry_fileType = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_fileType.place(x=80,y=75,width=200)
        self.view_edit_entry_filePath = tk.Entry(view_editFrame,text="")
        self.view_edit_entry_filePath.place(x=80,y=105,width=200)
        view_edit_frame_commentBox = tk.Frame(view_editFrame, width=200, height=100)
        view_edit_frame_commentBox.place(x=80,y=135)
        view_edit_frame_commentBox.columnconfigure(0, weight=100)  
        view_edit_frame_commentBox.rowconfigure(0, weight=100)  
        view_edit_frame_commentBox.grid_propagate(0)
        self.view_edit_entry_commentBox = tk.Text(view_edit_frame_commentBox)
        self.view_edit_entry_commentBox.grid(sticky="NSEW")
        #list box for categories
        view_edit_frame_listbox = tk.Frame(view_editFrame)
        view_edit_frame_listbox.place(x=80,y=260)
        view_edit_frame_listbox.rowconfigure(0, weight=10) 
        view_edit_frame_listbox.columnconfigure(0, weight=10) 
        view_edit_frame_listbox.grid_propagate(0) 
        self.yscrollbar = tk.Scrollbar(view_edit_frame_listbox)
        self.yscrollbar.pack(side = "right", fill = "y")
        self.listBox = tk.Listbox(view_edit_frame_listbox, selectmode = "multiple",yscrollcommand = self.yscrollbar.set)
        self.listBox.pack(pady = 5,fill = "y",expand=1)
        view_edit_label_fileImage = tk.Label(view_editFrame,text="File image:",font=controller.label_font)
        view_edit_label_fileImage.place(x=300,y=0)
        self.view_edit_label_image = tk.Label(view_editFrame,text="",borderwidth=2, relief="ridge")
        self.view_edit_label_image.place(x=300,y=90,height=195, width=195)
        view_edit_button_selectImage = tk.Button(view_editFrame,text="Change image", command=self.update_image_file)
        view_edit_button_selectImage.place(x=350,y=45)
        self.view_edit_button_saveChanges = tk.Button(view_editFrame,text="Save changes", command= self.update_file)
        self.view_edit_button_saveChanges.place(x=100,y=450)
        #helper variables during runtime
        self.photoImg = None
        self.img = None
        self.tempImagePath = None
        self.selectedFileID=None
        self.selectedFile=None

##### FRAME METHODS BELOW ############################################################
    def unselectTable(self,deselect=False) -> None:
        """Method to deselect a table item and clear the right hand side widgets"""
        DEBUG("unselectTable - Clearing boxes")
        if deselect == True:
            self.tree.selection_clear()
        self.view_edit_entry_fileName.delete(0, 'end')
        self.view_edit_entry_filePath.delete(0, 'end')
        self.view_edit_entry_fileType.delete(0, 'end')
        self.view_edit_entry_commentBox.delete(1.0, 'end')
        self.listBox.delete(0,'end')
        self.view_edit_label_image.configure(image=None)
        if deselect == True:
            self.populateTable()
  
    def add_files(self) -> None:
        """Method asks for filetypes and whther the user wants to search for
           a single file or all files in selected directory"""
        diag = MyDialog(self,"Select file types")
        if diag.selectedTypes == False:
                DEBUG("add_files - MyDialog returned False")
                return False
        answer = askyesno("Add a file or a folder ", f"Click 'Yes' to add a file \n or \n click 'No' to add a folder ?")
        if answer:
            if len(diag.selectedTypes) < 1:
                DEBUG("add_files -no filetypes selected, setting all")
                filename = fd.askopenfilename(filetypes=[('Selected Files', '*.m4a '), ('Selected Files', '*.cflac '), 
                                                        ('Selected Files', '*.mp3 '), ('Selected Files', '*.mp4 '), 
                                                        ('Selected Files', '*.wav '), ('Selected Files', '*.wma '), 
                                                        ('Selected Files', '*.aac ')])
            else:
                filename = fd.askopenfilename(filetypes=diag.selectedTypes)
            if len(filename) < 1 :
                DEBUG("add_files - No file selected")
                return False
            DEBUG(f"add_files - {filename} ")
            self.controller.mediaLibrary.add_file(filename)
        else:
            directory = fd.askdirectory(parent=self,initialdir="/",title='Please select a directory')
            if len(directory) < 1 :
                DEBUG("add_files - No file selected")
                return False
            DEBUG(f"add_files - adding directory {directory}")
            fileTypes = []
            for x in diag.selectedTypes:
                fileTypes.append(x[1][2:].strip())
            self.controller.mediaLibrary.add_folder(directory,fileTypes)
        self.populateTable()

    def update_image_file(self) -> None:
        """Method loads dialog box and asks user to select an image,
           the temp image populates the image box"""
        if len(self.view_edit_entry_fileName.get()) > 1:
            filetypes = [('Select Image', '*.png '), ('Select Image', '*.bmp '), ('Select Image', '*.gif '), ('Select Image', '*.jpg ')]
            filename = fd.askopenfilename(
                title='Select an Image',
                initialdir='/',
                filetypes=filetypes)
            width = 195
            height = 195
            DEBUG(f"update_image_file - image selected {filename}")
            self.tempImagePath = filename
            self.img = PIL.Image.open(filename)
            self.img = self.img.resize((width,height), PIL.Image.ANTIALIAS)
            self.photoImg =  PIL.ImageTk.PhotoImage(self.img)
            self.view_edit_label_image.configure(image=self.photoImg)

 
    def listBox_set_selected_items(self,n) -> None:
        """Sets the selected listbox item as highlighed"""
        self.listBox.select_set(n)

    def update_file(self) -> None:
        """Method updates the mediafile from the input boxes"""
        if self.selectedFile != None:
            self.selectedFile.file_path = self.view_edit_entry_filePath.get()
            self.selectedFile.file_name = self.view_edit_entry_fileName.get()
            self.selectedFile.file_type = self.view_edit_entry_fileType.get()
            self.selectedFile.file_comment = self.view_edit_entry_commentBox.get("1.0","end")
            self.selectedFile.categories = []
            for i in self.listBox.curselection():
                self.selectedFile.categories.append(self.listBox.get(i))
            if self.tempImagePath != None:
                self.selectedFile.image_path = self.tempImagePath
            DEBUG(f"""update_file:
                        filename:{self.selectedFile.file_name}
                        filepath:{self.selectedFile.file_path}
                        filetype:{self.selectedFile.file_type}
                        filecomment:{self.selectedFile.file_comment}
                        filecategories:{self.selectedFile.categories}
                        fileimage:{self.selectedFile.image_path}""")
        self.tempImagePath = None

        self.populateTable(self.searchBar.get())
        
    def fill_view_edit(self, event) -> None:
        "method clears and then populates the right hand widgets"
        try:
            item = self.tree.identify("item", event.x, event.y)
            selectedFile =self.tree.item(item)["values"][0]
            self.selectedFile = self.controller.mediaLibrary.get_file(selectedFile)
            self.unselectTable(False)
            DEBUG(f"fill_view_edit - {self.selectedFile.file_name}")
            DEBUG(f"fill_view_edit - setting wigets with file info")
            self.view_edit_entry_fileName.insert(0,self.selectedFile.file_name)
            self.view_edit_entry_filePath.insert(0,self.selectedFile.file_path)
            self.view_edit_entry_fileType.insert(0,self.selectedFile.file_type)
            self.view_edit_entry_commentBox.insert(1.0,self.selectedFile.file_comment)
            if self.controller.categoryList.getSize() > 0:
                sortedList = sorted(self.controller.categoryList.categories)
                for i in sortedList:
                    self.listBox.insert('end',i)
                for x in self.selectedFile.categories:
                    if x in sortedList:
                        self.listBox_set_selected_items(sortedList.index(x))
            width = 195
            height = 195
            self.img = PIL.Image.open(self.selectedFile.image_path)
            self.img = self.img.resize((width,height), PIL.Image.ANTIALIAS)
            self.photoImg =  PIL.ImageTk.PhotoImage(self.img)
            self.view_edit_label_image.configure(image=self.photoImg)
        except IndexError as e:
            DEBUG(f"fill_view_edit - {e}")
    def do_popup(self, event) -> None:
        """Method shows the first pop up window to add file to playlist"""
        try:
            item = self.tree.identify("item", event.x, event.y)
            curItem = self.tree.focus()
            self.tree.selection_set(item)
            self.curitem = self.tree.item(item)["values"]
            DEBUG(f"do_popup - clicked on: {self.tree.item(item)['values']}")
            self.selectedFileID = self.tree.item(item)["values"][0]
            self.popup.tk_popup(event.x_root, event.y_root, 0,)
        except IndexError as e:
            DEBUG(f"do_popup - {e}")
        finally:
            self.popup.grab_release()

    def playlistPopup(self,*args) -> None:
        """Method shows secondary pop up with playlists to select"""
        last = self.playpopup.index(tk.END)
        if last != None:
            for i in range(last+1):
                self.playpopup.delete(0, "end")
        for l in range(len(self.controller.playlistLibrary.playlists)):
            keys_list = list(self.controller.playlistLibrary.playlists)
            self.playpopup.add_command(label=keys_list[l], command=lambda x=l: self.add_toPlaylist(x))
        x, y = win32api.GetCursorPos()
        try:
            DEBUG(f"playlistPopup - Popped up")
            self.playpopup.tk_popup(x+20, y, 0)
        except IndexError as e:
            DEBUG(f"playlistPopup - {e}")
        finally:
            self.playpopup.grab_release()
    
    def delete_treeItem(self) -> None:
        """Method deletes an item in table and also removes from class object"""
        try:
            curItem = self.tree.focus()
            DEBUG(f"Current ITEM: {curItem}")
            selectedFileID = self.tree.item(curItem)["values"][0]
            selectedFileName = self.tree.item(curItem)["values"][1]
            selectedFileType = self.tree.item(curItem)["values"][2]
            DEBUG(f"selectedFileID: {selectedFileID}")
            DEBUG(f"selectedFileName: {selectedFileName}")
            DEBUG(f"selectedFileName: {selectedFileType}")
            self.controller.mediaLibrary.removeFile(selectedFileID,selectedFileName,selectedFileType)
            self.tree.delete(curItem)
        except IndexError as e:
            DEBUG(f"delete_treeItem - {e}")

    def populateTable(self,search="") -> None:
        """Method populates table and also filters table from search input"""
        if search == "--Search Files--":
            search = ""
        DEBUG(f"populateTable - Called - search variable:{search}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        count = 0
        if self.controller.mediaLibrary.getSize() > 0:
            for key,record in self.controller.mediaLibrary.files.items():
                if search.lower() in record.file_name.lower():
                    if count %2 ==0:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(key,record.file_name,record.file_type),tags=('evenrow',""))

                    else:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(key,record.file_name,record.file_type),tags=('oddrow',""))
                    count +=1 

    def add_toPlaylist(self,playlistid) -> None:
        """Method adds a selected file to a selected playlist"""
        DEBUG(f"add_toPlaylist - PLAYLISTNAME: {list(self.controller.playlistLibrary.playlists)[playlistid]}")
        playlistName = list(self.controller.playlistLibrary.playlists)[playlistid]
        fileid,filename,filetype = self.curitem
        DEBUG(f"add_toPlaylist - filename: {filename}")
        for key, value in self.controller.mediaLibrary.files.items():
            if value.file_name == filename and value.file_type == filetype and key == fileid:
                self.controller.playlistLibrary.add_file_to_playlist(playlistName,value)
     

class MyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.dicto = {}
        super().__init__(parent, title)

    #add all the widgets to the body and assign variables to the check boxes
    def body(self, frame):
        self.label = tk.Label(frame, width=25, text="Select the file types to search for.")
        self.label.pack()
        self.cv = tk.IntVar()
        self.cv1 = tk.IntVar()
        self.cv2 = tk.IntVar()
        self.cv3 = tk.IntVar()
        self.cv4 = tk.IntVar()
        self.cv5 = tk.IntVar()
        self.cv6 = tk.IntVar()

        self.c = tk.Checkbutton(frame, text = "M4A",variable=self.cv)
        self.c.pack()
        self.c1 = tk.Checkbutton(frame, text = "CFLAC",variable=self.cv1)
        self.c1.pack()
        self.c2 = tk.Checkbutton(frame, text = "MP3",variable=self.cv2)
        self.c2.pack()
        self.c3 = tk.Checkbutton(frame, text = "MP4",variable=self.cv3)
        self.c3.pack()
        self.c4 = tk.Checkbutton(frame, text = "WAV",variable=self.cv4)
        self.c4.pack()
        self.c5 = tk.Checkbutton(frame, text = "WMA",variable=self.cv5)
        self.c5.pack()
        self.c6 = tk.Checkbutton(frame, text = "AAC",variable=self.cv6)
        self.c6.pack()
  
        return frame

    #Action for when OK is clicked, Method takes the values of the check boxes and assigns them to a class variable
    def ok_pressed(self):
        self.selectedTypes= []
        self.selected={
        self.c.cget("text") : self.cv.get(),
        self.c1.cget("text"): self.cv1.get(), 
        self.c2.cget("text"): self.cv2.get(), 
        self.c3.cget("text"): self.cv3.get(), 
        self.c4.cget("text"): self.cv4.get(), 
        self.c5.cget("text"): self.cv5.get(),
        self.c6.cget("text"): self.cv6.get()}
        ftypes = ""
        for key, value in self.selected.items():
            if value == 1:
                ftypes  = f"*.{key.lower()} "
                self.selectedTypes.append(tuple((f"Selected Files", ftypes)))
        print(self.selectedTypes)
        self.destroy()

    def cancel_pressed(self):
        self.selectedTypes = False
        self.destroy()

    #add buttons to widget
    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())

    

