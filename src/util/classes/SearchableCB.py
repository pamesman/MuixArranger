import tkinter as tk
from PIL import Image, ImageTk

class SearchableComboBox():
    def __init__(self, options) -> None:
        self.dropdown_id = None
        self.options = options

        # Create a Text widget for the entry field
        wrapper = tk.Frame(root)
        wrapper.pack()

        self.entry = tk.Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.pack(side=tk.LEFT)

        # Dropdown icon/button
        #self.icon = ImageTk.PhotoImage(Image.open("dropdown_arrow.png").resize((16,16)))
        tk.Button(wrapper, command=self.show_dropdown).pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(root, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        pass

    def on_select(self, event):
        pass

    def show_dropdown(self, event=None):
        pass

    def hide_dropdown(self):
        pass

# Create the main window
root = tk.Tk()
root.title("Searchable Dropdown")

options = ["Apple", "Banana", "Cherry", "Date", "Grapes", "Kiwi", "Mango", "Orange", "Peach", "Pear"]
SearchableComboBox(options)

# Run the Tkinter event loop
root.geometry('220x150')
root.mainloop()