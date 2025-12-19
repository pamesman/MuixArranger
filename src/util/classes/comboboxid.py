from tkinter import *


root = Tk()
root.geometry("1280x720")
board = Frame(root)
board.pack()

square = "Chat"
cost = 2000

class buyPrompt:

         def __init__(self):
            pop = Toplevel()
            self.pop = Toplevel()
            pop.title("Purchase Square")

            Msg = Message(pop, text = "Would you like to purchase %s for %d" %                         (square, cost))
            Msg.pack()


            self.yes = Button(pop, text = "Yes", command = self.yesButton)
            self.yes.pack(side = LEFT)
            self.no = Button(pop, text = "No", command = self.noButton)
            self.no.pack(side = RIGHT)

            pop.mainloop()
         def yesButton(self):
                        self.pop.destroy()
                        return True

         def noButton(self):
                        return False
buyprompt = buyPrompt().pack
root.mainloop()
