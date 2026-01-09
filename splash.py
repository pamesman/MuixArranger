import tkinter
import os
from PIL import Image, ImageTk

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)




#splash screen
splash = tkinter.Toplevel()

# splash.overrideredirect(True)
splash.geometry('%dx%d+%d+%d' % (823,300,500,320))

pic = Image.open(resource_path("banner.png"))
pic = pic.resize((823,300))
pic = ImageTk.PhotoImage(pic)
banner = tkinter.Label(splash, text = "omg hii", image = pic)
banner.pack(fill = "both", expand = "yes")
splash.after(3000, splash.destroy)
# splash.destroy()
def splash_resize():
    splash.geometry('%dx%d+%d+%d' % (50,50,500,320))
splash.after(3000, splash_resize)
splash.mainloop()


