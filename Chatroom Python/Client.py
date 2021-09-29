import socket
import threading
import tkinter as Chat
from datetime import datetime
import config

# TCP chat - NeuralNine https://www.youtube.com/watch?v=3UOyky9sEQY
# bubble from https://stackoverflow.com/questions/64736839/python-tkinter-chat-application-i-want-to-draw-bubbles-around-messages
# chat from https://stackoverflow.com/questions/42062391/how-to-create-a-chat-window-with-tkinter

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
        for F in (ConnectClient, ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(ConnectClient)

    # using tkraise() to show the frame
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

class ConnectClient(Chat.Frame):
    def __init__(self, parent, controller):
        Chat.Frame.__init__(self, parent)
        frame = Chat.Frame(self)
        messages = Chat.Text(self)
        messages.pack()
        typedmessage = Chat.StringVar()
        typebox = Chat.Entry(self, text=typedmessage, font=SMALL_FONT)
        typebox.pack(side=Chat.BOTTOM, fill=Chat.BOTH, ipady=15)
        button = Chat.Button(self, text="Exit", font=NORMAL_FONT,
                           command=lambda: app.destroy())
        button.pack(pady=10, padx=10, side=Chat.RIGHT)
        button.place(x=580, y=393)

        def receiveMessage():
            while True:
                try:
                    # If 'CODEWORD' Send Username
                    message = client.recv(1024).decode('ascii')
                    if message == 'CODEWORD':
                        client.send(username.encode('ascii'))
                    else:
                        print(message)
                        messages.window_create(Chat.INSERT, window=Chat.Label(messages, fg="#000000", text=format(message),
                                                                    wraplength=500, font=SMALL_FONT, bg="lightblue",
                                                                    bd=4, justify="left"))

                        messages.insert(Chat.INSERT, '\n')
                except:
                    print("There has been an error!")
                    client.close()
                    break

        # Sending Messages To Server
        def printMessage(event):
            now = datetime.now()
            current_time = now.strftime("%H:%M ")
            message = '{}- {}: {}'.format(current_time, username, typedmessage.get())
            client.send(message.encode('ascii'))
            typedmessage.set('')
            return "break"

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, 55555))
        except:
            print('Connection timed out! \nProbably wrong Server IP entered. \nPlease restart Client')

        receive_thread = threading.Thread(target=receiveMessage)
        receive_thread.start()
        typebox.bind("<Return>", printMessage)
        frame.pack()


host = config.host
username = config.username
app = StartFrame()
app.title("Chat")
app.geometry("650x440")
app.resizable(width=False, height=False)
app.mainloop()
