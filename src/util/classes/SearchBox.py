import customtkinter
from time import sleep

class SearchBox(customtkinter.CTkComboBox):
    def __init__(self, parent,values, border_color = None, button_color = None, button_hover_color = None ,text_color = None, command = None, fg_color = None, placeholder = None):
        self.values = values
        self.border_color = border_color
        self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.text_color = text_color
        self.command = command
        self.fg_color = fg_color
        self.placeholder = placeholder
        self.pair = [placeholder, "N.A."]
        super().__init__(master= parent, values = self.values,
                         border_color = self.border_color,
                         button_color = self.button_color,
                         button_hover_color = self.button_hover_color,
                         text_color = self.text_color,
                         fg_color = self.fg_color,
                         command = self.command,
                         )

        self._entry.bind("<KeyRelease>",self.search_items)
        #self._entry.insert(0,str(self.placeholder))
        self._entry.bind("<Button-1>", self.click)
        self._entry.bind("<FocusOut>", self.salir)
        #self._entry.bind("<space>",print("x"))

        #self._dropdown_menu.bind("<Button-1>", self.select(self._entry.get()))



    def comando(self,value):
        self.placeholder = value
        self.pair[1] = value

    def reset_placeholder(self,value):
        self.placeholder = value

    def search_items(self, event):
        search_value = self._entry.get()
        self._clicked()
        self.focus_force()
        if search_value == "" or search_value == " ":
            self.configure(values=self.values)
        else:
            value_to_display = []
            for value in self.values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            self.configure(values=value_to_display)


    def click(self,*args):
        self._entry.delete(0, 'end')

    def salir(self,*args):
        if self._entry == self.focus_get() or self._dropdown_menu == self.focus_get():
            pass
        else:
            self._entry.delete(0, 'end')
            self._entry.insert(0, str(self.placeholder))
