import customtkinter
import tkinter


def crear_searchbox(parent, values, dataframe,entry_width = 100, entry_height = 25, function = None, function_vars = None,croquis = None):
    entry = customtkinter.CTkEntry(parent, width = entry_width)
    textvar = tkinter.StringVar()
    entry.configure(textvariable=textvar)
    lb = tkinter.Listbox(parent.master, width=12, background="#2B2B2B", fg="#FFFFFF", bd=0, relief="flat",
                              activestyle="none", highlightthickness=0, justify="left")

    if function is None:
        def function():
            print("No function")

    def function2(value):
        textvar.set(lb.get(lb.nearest(value.y)))
        lb.place_forget()
        if function_vars is None:
            function()
        else:
            function(function_vars)

    def search_items(_event, entry):
        search_value = entry.get()
        entry.focus_force()
        working_values = list(set(values) ^ set([i.upper() for i in list(croquis.values())[2:]]))
        if search_value == "" or search_value == " ":
            lb.delete(0, "end")
            try:
                working_values.sort(key = lambda x: dataframe.loc[dataframe["Àlies"].str.upper() == x].iloc[0, 2], reverse=True)
            except:
                pass
            for i in working_values:
                lb.insert("end",i)
            lb.insert("end", textvar.get())
        else:
            value_to_display = []
            for value in working_values:
                if search_value.lower() in value.lower():
                    value_to_display.append(value)
            try:
                value_to_display.sort(key = lambda x: dataframe.loc[dataframe["Àlies"].str.upper() == x].iloc[0, 2], reverse=True)
            except:
                pass
            lb.delete(0, "end")
            for i in value_to_display:
                lb.insert("end",i)
            lb.insert("end", textvar.get())


    def on_click(_event):
        entry.delete(0, "end")
        working_values = list(set(values)^set([i.upper() for i in list(croquis.values())[2:]]))
        if "N. A." in list(working_values):
            working_values.remove("N. A.")

        try:
            working_values.sort(reverse=True,key = lambda x: dataframe.loc[dataframe["Àlies"].str.upper() == x].iloc[0, 2])
        except:
            pass
        #Configurar el dropdown:
        lb.place(relx= 0.98, rely = 0.7, anchor = "ne"
                      )
        sb = tkinter.Scrollbar(parent)
        lb.delete(0, "end")
        for i in working_values:
            lb.insert("end", i)
        lb.config(yscrollcommand=sb.set)
        sb.config(command=lb.yview)
        entry.focus_set()

    entry.bind("<KeyRelease>", lambda x = entry : search_items(entry, entry))
    entry.bind("<Button-1>", on_click)
    lb.bind("<Button-1>", function2)

    return entry

