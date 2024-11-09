import tkinter
import tkinter.filedialog
from discorddms import file_writer, har_to_arr


class MainWindow:
    def open_file(self):
        file = tkinter.filedialog.askopenfilename(initialdir='/', filetypes=[("HAR file", "*.har"), ("All files", "*.*")])
        if file:
            self.file_entry.delete(0,tkinter.END)
            self.file_entry.insert(0,file)

    def parse(self):
        file_writer(har_to_arr(self.file_entry.get()), self.text_check_bool.get(), self.json_check_bool.get(), self.parse_prefix.get())

    def button_inactive(self, *args):
        self.parse_button["state"] = tkinter.NORMAL if (self.json_check_bool.get() or self.text_check_bool.get()) and self.file_entry.get() else tkinter.DISABLED

    def __init__(self, top_lvl):
        self.top_lvl = top_lvl
        #self.top_lvl.geometry("700x700")
        self.top_lvl.resizable(width=False, height=False)
        self.top_lvl.grid_columnconfigure(1, weight=1)

        self.file_label = tkinter.Label(self.top_lvl, text="HAR File to parse: ", justify=tkinter.LEFT)
        self.file_label.grid(row=0, column=0, sticky=tkinter.W)

        self.file_entry_string = tkinter.StringVar()
        self.file_entry_string.trace_add("write", self.button_inactive)
        self.file_entry = tkinter.Entry(self.top_lvl, width=50, textvariable=self.file_entry_string)
        self.file_entry.grid(row=0, column=1, sticky=tkinter.E)

        self.file_button = tkinter.Button(self.top_lvl, width=1, text=u"\U0001F5C0", command=self.open_file)
        self.file_button.grid(row=0, column=2, sticky=tkinter.E)

        self.text_label = tkinter.Label(self.top_lvl, text="Store as text: ", justify=tkinter.LEFT)
        self.text_label.grid(row=1, column=0, sticky=tkinter.W)

        self.text_check_bool = tkinter.BooleanVar()
        self.text_check = tkinter.Checkbutton(self.top_lvl, variable=self.text_check_bool, command=self.button_inactive)
        self.text_check.grid(row=1, column=1, columnspan=2)

        self.json_label = tkinter.Label(self.top_lvl, text="Store as JSON: ", justify=tkinter.LEFT)
        self.json_label.grid(row=2, column=0, sticky=tkinter.W)

        self.json_check_bool = tkinter.BooleanVar()
        self.json_check = tkinter.Checkbutton(self.top_lvl, variable=self.json_check_bool, command=self.button_inactive)
        self.json_check.grid(row=2, column=1, columnspan=2)

        self.prefix_label = tkinter.Label(self.top_lvl, text="Optional Prefix: ", justify=tkinter.LEFT)
        self.prefix_label.grid(row=3, column=0, sticky=tkinter.W)

        self.parse_prefix = tkinter.Entry(self.top_lvl, width=53)
        self.parse_prefix.grid(row=3, column=1, columnspan=2, sticky=tkinter.E)

        self.parse_button = tkinter.Button(self.top_lvl, text="Begin", width=10,
                                             command=self.parse)
        self.parse_button.grid(row=4, column=0, columnspan=2)

        self.top_lvl.title("Discord DMs Parser")



if __name__ == '__main__':
    top = tkinter.Tk()
    MainWindow(top)
    top.mainloop()
