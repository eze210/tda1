from tkinter import Tk, Button
from tkinter.filedialog import askopenfilename as choose_file


class GameWindow:
    def __init__(self, master):
        self.master = master
        master.title("Batalla Naval")

        for i in range(0, 10):
            for j in range(0, 5):
                button = Button(master, text="({}, {})".format(i, j), command=self.choose_file)
                button.grid(row=i, column=j)

    def choose_file(self):
        return choose_file()


root = Tk()
my_gui = GameWindow(root)
root.mainloop()
