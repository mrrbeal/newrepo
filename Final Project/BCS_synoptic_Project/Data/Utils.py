import sys,os,json
from tkinter.messagebox import showerror
import tkinter.simpledialog
import tkinter as tk

class Utilities:
    if getattr(sys, 'frozen', False):
        dname = os.path.dirname(sys.executable)
    elif __file__:
        dname = os.path.dirname(__file__)

    def load_system_config():
        with open(f'{Utilities.dname}/config.json') as json_file:
            data = json.load(json_file)
            for d in data["configuration"]:
                print(d)
                print(d["LAST_LOAD_FILE"] )
        return d["LAST_LOAD_FILE"]
    
    def load_state_file(file):
        try:
            with open(rf'{file}') as json_file:
                data = json.load(json_file)
                print(data)
                for d in data["configuration"]:
                    print(d)
                    print("STATE ID : ",d["state_ID"])
            return d["state_ID"]
        except Exception as e:
            print("An error occurred:", e.args[0])
            showerror(title='Error', message='Error loading selected file.')
            return None
    
    def save_state(state_id, path):
        dicto = {"configuration" : {"state_ID": state_id}}
        with open(path, 'w') as outfile:
            json.dump(dicto, outfile)


class MyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.dicto = {}
        super().__init__(parent, title)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
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

    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())



