import tkinter as tk
from tkinter import ttk

def DEBUG(text):
    if DEBUGON == True:
        print("Playlists:\n",text)

DEBUGON = True

class Playlists(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_propagate(False)
        self.config(width=1000,height=600)
        DEBUG("Loading Widgets")
        #add widgets to the frame
        self.searchBar = tk.Entry(self,font=controller.title_font)
        self.searchBar.place(x=137,y=25)
        self.searchBar.insert(0, 'Search Playlist Files')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<FocusOut>", lambda args: self.searchBar.insert(0, 'Search Playlist Files') if len(self.searchBar.get()) < 1 else 1+1)
        self.searchBar.bind("<KeyRelease>", lambda args: self.filter_table(self.searchBar.get()))
   
        #dedicated variable for label text
        self.labelText = tk.StringVar()
        self.label_playlistNameTxt = tk.Label(self, text="Playlist Name: ", font=controller.title_font).place(x=15,y=80)
        self.label_playlistName = tk.Label(self, textvariable=self.labelText, font=controller.title_font).place(x=200,y=80)
        button_rename_playlist = tk.Button(self,text="Rename Playlist",command=self.popup_renamePlaylist).place(x=550,y=100) # PLACE LABEL
        button_delete_playlist = tk.Button(self,text="  Delete Playlist ",command=self.delete_playlist).place(x=550,y=130) # PLACE LABEL

        #style and pack table
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Treeview",
        background="#D3D3D3",
        foreground="black",
        rowheight=30,
        fieldbackground="#D3D3D3",
        height=800)
        style.map("Treeview", background=[("selected","#347083")])
        tree_frame= tk.Frame(self)
        tree_frame.place(x=0,y=120)
        tree_scroll = tk.Scrollbar(tree_frame)
        tree_scroll.pack(side="right", fill="y")
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)
        self.tree.pack()
        tree_scroll.config(command=self.tree.yview)
        self.tree["columns"] = ("PlaylistNumber", "FileName")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("PlaylistNumber", anchor="center", width=100)
        self.tree.column("FileName", anchor="center", width=400)
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("PlaylistNumber", text="Playlist Number", anchor="center")
        self.tree.heading("FileName", text="File Name", anchor="center")
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")

        #side control buttons
        button_moveUp_playlist = tk.Button(self,text="    Move Up   ",command=lambda:self.move_playlistFile("up")).place(x=550,y=300) 
        button_removeFile_playlist = tk.Button(self,text=" Remove File ",command=self.delete_playlistFile).place(x=550,y=330) 
        button_moveDown_playlist = tk.Button(self,text=" Move Down ",command=lambda:self.move_playlistFile("down")).place(x=550,y=360)

        #helper variables during runtime
        self.playlistCount = 1
        self.top_exists = False
        #load sidemenu items
        self.load_playlistMenu()

##### FRAME METHODS BELOW ############################################################    
    def rename_playlist(self,name)-> None:
        """Method for renaming a playlist in playlisy library and gui"""
        self.controller.playlistLibrary.rename_playlist(self.labelText.get(), name)
        DEBUG(f"rename_playlist - \nold name: {self.labelText.get()}\nnew name: {name}")
        self.labelText.set(name)
        self.close_win(self.top)
        self.load_playlistMenu()

    def move_playlistFile(self,direction)-> None:
        """Method for moving a playlist item up or down within the playlist"""
        try:
            curItem = self.tree.focus()
            DEBUG(f"move_playlistFile - Current ITEM: {curItem}")
            selectedPlaylistID = self.tree.item(curItem)["values"][0]
            selectedPlaylistFileName = self.tree.item(curItem)["values"][1]
            DEBUG(f"move_playlistFile - selectedPlaylistID: {selectedPlaylistID}")
            DEBUG(f"move_playlistFile - selectedPlaylistFileName: {selectedPlaylistFileName}")
            self.controller.playlistLibrary.move_playlistFile(self.labelText.get(),selectedPlaylistID,direction)
            self.load_playlist(self.labelText.get())
        except IndexError as e:
            DEBUG(f"move_playlistFile - {e}")

    def delete_playlistFile(self)-> None:
        """Method for deleting a file from a playlist"""
        try:
            curItem = self.tree.focus()
            DEBUG(f"delete_playlistFile - Current ITEM: {curItem}")
            selectedPlaylistID = self.tree.item(curItem)["values"][0]
            selectedPlaylistFileName = self.tree.item(curItem)["values"][1]
            DEBUG(f"delete_playlistFile - selectedPlaylistID: {selectedPlaylistID}")
            DEBUG(f"delete_playlistFile - selectedPlaylistFileName: {selectedPlaylistFileName}")
            self.controller.playlistLibrary.delete_file_from_playist(self.labelText.get(),selectedPlaylistID)
            self.tree.delete(curItem)
            self.load_playlist(self.labelText.get())
        except IndexError as e:
            DEBUG(f"delete_playlistFile - {e}")

    def create_playlist(self,name)-> None:
        """Method creates a playlist in both library and gui"""
        if name.isalnum():
            self.controller.playlistLibrary.add_playlist(name)
            DEBUG(f"create_playlist - creating : {name}")
            tk.Button(self.controller.playlist_frame.inner_frame, text=name,
                            command=lambda: self.show_load(name), bg=self.controller.colourPalette["darkblue"], 
                            fg="White").grid(row=self.playlistCount, column=0,columnspan=2,sticky='ew')
            self.close_win(self.top)
            self.playlistCount +=1

    def delete_playlist(self)-> None:
        """Method deletes a playlist"""
        name = self.labelText.get()
        DEBUG(f"delete_playlist - deleteing : {name}")
        self.controller.playlistLibrary.delete_playlist(name)
        self.labelText.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_playlistMenu()

    def load_playlist(self,name)-> None:
        """Method loads a playlist into the table"""
        self.labelText.set(name)
        DEBUG(f"load_playlist - loading playlist : {name}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        count = 0
        if self.controller.playlistLibrary.getSize() > 0:
            for key,record in self.controller.playlistLibrary.playlists.items():
                if name == key:
                    for mediaFile in self.controller.playlistLibrary.playlists[name]:
                        if count %2 ==0:
                            self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1].file_name),tags=('evenrow',""))
                        else:
                            self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1].file_name),tags=('oddrow',""))
                        count +=1 
        
    def filter_table(self,search=""):
        """Method filters playlist files based in searchbar criteria"""
        DEBUG(f"filter_table - filtering playlist : {search}")
        if search == "Search Playlist Files":
            search = ""
        for item in self.tree.get_children():
            self.tree.delete(item)
        playlistName = self.labelText.get()
        count = 0
        if self.controller.playlistLibrary.getSize() > 0:
            for key,record in self.controller.playlistLibrary.playlists.items():
                if playlistName == key:
                    for mediaFile in self.controller.playlistLibrary.playlists[playlistName]:
                        if search.lower() in mediaFile[1].file_name.lower():
                            if count %2 ==0:
                                self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1].file_name),tags=('evenrow',""))
                            else:
                                self.tree.insert(parent="",index="end", iid= count, text="", values=(mediaFile[0],mediaFile[1].file_name),tags=('oddrow',""))
                            count +=1 

    def show_load(self,key)-> None:
        """Helper Method, calls load playlist and ensures the playlists frame is showing"""
        self.load_playlist(key)
        self.controller.show_frame("Playlists")

    def load_playlistMenu(self)-> None:
        """Loads all of the available playlist items in to the left hand side menu"""
        for widgets in self.controller.playlist_frame.inner_frame.winfo_children():
            widgets.destroy()
        tk.Button(self.controller.playlist_frame.inner_frame, text="Add New Playlist",
                           command=self.popup_createPlaylist).grid(row=0, column=0,columnspan=2,sticky='ew')
        for key,record in self.controller.playlistLibrary.playlists.items():
            tk.Button(self.controller.playlist_frame.inner_frame, text=key,
                            command=lambda x=key: self.show_load(x), bg=self.controller.colourPalette["darkblue"], fg="White").grid(row=self.playlistCount, column=0,columnspan=2,sticky='ew')
            self.playlistCount +=1

    def popup_createPlaylist(self)-> None:
        """Method - Pop up window for entering the name of a new playlist"""
        if self.top_exists == False:
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            label = tk.Label(self.top,text="Enter A Playlist Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()
            tk.Button(self.top,text= "Create Playlist", 
            command= lambda:self.create_playlist(entry.get())).pack(pady= 5,in_=self.top, side="top")
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True

    def popup_renamePlaylist(self)-> None:
        """Method - Pop up window for renaming a playlist"""
        if self.labelText.get() != "":
            if self.top_exists == False:
                self.top= tk.Toplevel(self)
                self.top.geometry("400x150")
                label = tk.Label(self.top,text="Enter A New Playlist Name:")
                label.pack(pady=10)
                entry= tk.Entry(self.top, width= 25)
                entry.pack()
                tk.Button(self.top,text= "Rename Playlist", 
                command= lambda:self.rename_playlist(entry.get())).pack(pady= 5,in_=self.top, side="top")
                tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
                self.top_exists = True
        else:
            DEBUG(f"popup_renamePlaylist - wont load pop up, no playlist selected :  {self.labelText.get()}")

    def close_win(self,top):
        """closes the pop up window"""
        top.destroy()
        self.top_exists = False