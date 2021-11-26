import tkinter as tk
from tkinter import ttk

def DEBUG(text):
    if DEBUGON == True:
        print("Categories:\n",text)

DEBUGON = True

class Categories(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid_propagate(False)
        self.config(width=1000,height=600)
        DEBUG("Loading Widgets")
        #add widgets to the frame
        self.searchBar = tk.Entry(self,font=controller.title_font)
        self.searchBar.place(x=137,y=25)
        self.searchBar.insert(0, 'Search Categories')
        self.searchBar.bind("<FocusIn>", lambda args: self.searchBar.delete('0', 'end'))
        self.searchBar.bind("<FocusOut>", lambda args: self.searchBar.insert(0, 'Search Categories') if len(self.searchBar.get()) < 1 else 1+1)
        self.searchBar.bind("<KeyRelease>", lambda args: self.populateTable(self.searchBar.get()))
        button_addFiles = tk.Button(self, text="Add A Category", command= self.popupwinCreate).place(x=2,y=80)
        button_view_editFiles = tk.Button(self, text="Rename Category", command= self.popupwinUpdate).place(x=425,y=80)
        button_deleteFiles = tk.Button(self, text="  Delete Category ", command=self.delete_Category).place(x=425,y=110)
        
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
        self.tree["columns"] = ("CategoryName")
        self.tree.column("#0", width=0, stretch="no")
        self.tree.column("CategoryName", anchor="center", width=400)
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("CategoryName", text="Category Name", anchor="center")
        self.tree.tag_configure('oddrow', background="white")
        self.tree.tag_configure('evenrow', background="lightblue")
    
        #helper variables during runtime
        self.top_exists = False
        #populate table with blank search
        self.populateTable()

##### FRAME METHODS BELOW ############################################################    
    def populateTable(self,search="")-> None:
        """Method for populating the table with the available categories"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        if search == "Search Categories":
            search = ""
        DEBUG(f"populateTable - filtering categories : {search}")
        count = 0
        if self.controller.categoryList.getSize() > 0:
            for record in self.controller.categoryList.categories:
                if search.lower() in record.lower():
                    if count %2 ==0:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(record),tags=('evenrow',""))
                    else:
                        self.tree.insert(parent="",index="end", iid= count, text="", values=(record),tags=('oddrow',""))
                    count +=1 

    def delete_Category(self)-> None:
        """Method for deleting a category"""
        try:
            curItem = self.tree.focus()
            DEBUG(f"delete_Category - Current ITEM: {curItem}")
            categoryName = self.tree.item(curItem)["values"][0]
            DEBUG(f"delete_Category - categoryName: {categoryName}")
            self.controller.categoryList.removeCategory(categoryName)
            self.tree.delete(curItem)
        except IndexError as e:
            DEBUG(f"delete_Category - {e}")

    def create_category(self,e)-> None:
        """Method for creating a category"""
        if e.isdigit() or e.isalpha():
            DEBUG(f"create_category - Creating: {e}")
            if e not in self.controller.categoryList.categories:
                self.controller.categoryList.createCategory(e.strip())
                self.populateTable()
                self.close_win(self.top)
        #deselect a file here s the categories update
        page = self.controller.get_page("Files")
        page.unselectTable()

    def update_category(self,e)-> None:
        """Method for updating a category"""
        try:
            curItem = self.tree.focus()
            DEBUG(f"update_category - Current ITEM: {curItem}")
            categoryName = self.tree.item(curItem)["values"][0]
            DEBUG(f"update_category - old categoryName: {categoryName}")
            DEBUG(f"update_category - new categoryName: {e}")
            self.controller.categoryList.updateCategory(categoryName,e)
            self.populateTable()
            self.close_win(self.top)
            #deselect a file here s the categories update
            page = self.controller.get_page("Files")
            page.unselectTable()
        except IndexError as e:
            DEBUG(f"update_category - {e}")

    def popupwinCreate(self):
        """Pop up window method for entering a new category name"""
        if self.top_exists == False:
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            label = tk.Label(self.top,text="Enter A New Category Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()
            tk.Button(self.top,text= "Create Category",
             command= lambda:self.create_category(entry.get())).pack(pady= 5,in_=self.top, side="top")
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True

    def popupwinUpdate(self)-> None:
        """Pop up window method for entering a new name for a category category name"""
        if self.top_exists == False:
            self.top= tk.Toplevel(self)
            self.top.geometry("400x150")
            label = tk.Label(self.top,text="Enter A New Category Name:")
            label.pack(pady=10)
            entry= tk.Entry(self.top, width= 25)
            entry.pack()
            tk.Button(self.top,text= "Update Category Name",
             command= lambda:self.update_category(entry.get())).pack(pady= 5,in_=self.top, side="top")
            tk.Button(self.top, text="Cancel", command=lambda:self.close_win(self.top)).pack(pady=5, in_=self.top, side="top")
            self.top_exists = True

    def close_win(self,top)-> None:
        """Method closes open popups"""
        top.destroy()
        self.top_exists = False
        
