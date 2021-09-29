import tkinter as Chat

# defining fonts
LARGE_FONT = ("Minion Pro Med", 24)
NORMAL_FONT = ("Minion Pro Med", 18)
SMALL_FONT = ("Minion Pro Med", 12)


class StartFrame(Chat.Tk):

    def __init__(self, *args, **kwargs):
        Chat.Tk.__init__(self, *args, **kwargs)
        container = Chat.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # frame loop
        for F in (HostInput, UsernameInput):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HostInput)


    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()


class HostInput(Chat.Frame):
    def __init__(self, parent, controller):
        Chat.Frame.__init__(self, parent)
        label = Chat.Label(self, text="Please input Server IP", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        hostbox = Chat.Entry(self, text="")
        hostbox.pack(side=Chat.TOP)

        def setHost():
            global host
            host = hostbox.get()
            label = Chat.Label(self, text="Server IP set as: " + host + "\nPress Next to continue...", font=SMALL_FONT)
            label.pack(pady=10, padx=10)
            return host

        button = Chat.Button(self, text="Submit",
                           command=setHost)
        button.pack(side=Chat.TOP)
        button = Chat.Button(self, text="Next",
                             command=lambda: controller.show_frame(UsernameInput))
        button.pack(side=Chat.BOTTOM)

class UsernameInput(Chat.Frame):
    def __init__(self, parent, controller):
        Chat.Frame.__init__(self, parent)
        label = Chat.Label(self, text="Please input Username", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        namebox = Chat.Entry(self, text="")
        namebox.pack(side=Chat.TOP)

        def setUsername():
            global username
            username = namebox.get()
            label = Chat.Label(self, text="Username set as: " + username + "\nPress next to continue...", font=SMALL_FONT)
            label.pack(pady=10, padx=10)
            return username

        button = Chat.Button(self, text="Submit",
                           command=setUsername)
        button.pack(side=Chat.TOP)
        button = Chat.Button(self, text="Next",
                             command=lambda: app.destroy())
        button.pack(side=Chat.BOTTOM)


host = ''
username = ''
app = StartFrame()
app.title("Server IP Input")
app.geometry("350x200")
app.resizable(width=False, height=False)
app.mainloop()

