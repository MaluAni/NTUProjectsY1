import tkinter as tk
import random
import sys


#defining fonts
LARGE_FONT= ("Minion Pro Med", 24)
NORMAL_FONT= ("Minion Pro Med", 18)
SMALL_FONT= ("Minion Pro Med", 12)

#initialising frames
class StartFrame(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        # frame loop
        for F in (StartPage, PageOne):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        #frame startin with PageOne
        self.show_frame(StartPage)
    #using tkraise() to show the frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Welcome to Trivia Game", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Enter Name", font=SMALL_FONT)
        label.pack(pady=10,padx=10)
        textbox = tk.Entry(self, text="")
        textbox.pack(side=tk.TOP)
        #start message and textbox
        def printName(): #function for printing user input and start message
          textInput = textbox.get()
          label = tk.Label(self, text="Hello "+textInput+"!", font=SMALL_FONT)
          label.pack(side=tk.TOP)
          label = tk.Label(self, text="Press Begin to start the game or Exit to quit", font=SMALL_FONT)
          label.pack(side=tk.TOP)
          label = tk.Label(self, text="The goal of the game is to answer all 15 questions", font=SMALL_FONT)
          label.pack(side=tk.TOP)
          label = tk.Label(self, text="Good luck!", font=SMALL_FONT)
          label.pack(side=tk.TOP)

        button = tk.Button(self, text="Submit",
                           command=printName)
        button.pack(side=tk.TOP) #submit button calls the above function
        
        button = tk.Button(self, text="Begin",
                            command=lambda: controller.show_frame(PageOne))
        button.pack(pady=10,padx=10)
        button.place(x=250, y=300) #Begin button calls PageOne class
        button = tk.Button(self, text="Exit",
                            command=lambda: exit())
        button.pack(pady=10,padx=10,side=tk.BOTTOM)
        button.place(x=300, y=300)
          

class StartFrameGame(tk.Tk):
    #needed for looping when destroying then rebuilding PageOne
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (PageFinal, PageOne, PageOneSix):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageOne)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class PageOne(tk.Frame):
      #main Trivia frame
      def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global corrCount #adding correct answer counter to the frame
        corrCountStr = "You have answered " + str(corrCount) + " questions"
        label = tk.Label(self, text=corrCountStr, font=SMALL_FONT)
        label.pack(pady=10,padx=10)
        random.shuffle(triviaList) #shuffling list and question order
        for triviaItem in triviaList: 
          possible = triviaItem.otherAnsw + [triviaItem.corrAnsw]
          random.shuffle(possible)
        triviaList.remove(triviaItem) #remove the item from the list so no repeated questions
        v = tk.IntVar()
        v.set(None) #initialising variable for user input
        label = tk.Label(self, text=triviaItem.question, font=SMALL_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Possible answers are:", font=SMALL_FONT)
        label.pack(pady=10,padx=10)
        label.place(x=50, y=180)
               
        label = tk.Label(self, text="A", font=NORMAL_FONT)
        label.pack(pady=10,padx=10)
        label.place(x=25, y=200)
        button = tk.Radiobutton(self, text=possible[0], indicatoron = 0, variable = v,
                            value=1)
        button.pack()
        button.place(x=50, y=200)
        label = tk.Label(self, text="B", font=NORMAL_FONT)
        label.pack(pady=10,padx=10)
        label.place(x=325, y=200)
        button = tk.Radiobutton(self, text=possible[1], indicatoron = 0, variable = v,
                            value=2)
        button.pack()
        button.place(x=350, y=200)
        label = tk.Label(self, text="C", font=NORMAL_FONT)
        label.pack(pady=10,padx=10)
        label.place(x=25, y=300)
        button = tk.Radiobutton(self, text=possible[2], indicatoron = 0, variable = v,
                            value=3)
        button.pack()
        button.place(x=50, y=300)
        label = tk.Label(self, text="D", font=NORMAL_FONT)
        label.pack(pady=10,padx=10)
        label.place(x=325, y=300)
        button = tk.Radiobutton(self, text=possible[3], indicatoron = 0, variable = v,
                            value=4)
        
              
        button.pack()
        button.place(x=350, y=300) #questions and answers interface with radiobuttons assigned to the variable v

        def wrongAnswer(): #function for destroying and rebuilding in care of wrong answer
          global app
          app.destroy()
          app = EndFrameGame()
          app.geometry("600x400")
          app.resizable(width=False, height=False)
          app.mainloop()
          
        
        def check_fun(): #function for checking user answer with correct answer
          userAnsw = v.get()
          global app
          global corrCount
          while corrCount < 14: #while loop until 15 correct answers
              if possible[userAnsw - 1] == triviaItem.corrAnsw:
                corrCount += 1
                
                app.destroy() #destroy and rebuild if correct answer
                app = StartFrameGame()
                app.geometry("600x400")
                app.resizable(width=False, height=False)
                app.mainloop()
              else:
                wrongAnswer()
          else:
             controller.show_frame(PageFinal) #calls in case of 15 correct answers
          
        button = tk.Button(self, text = "Submit",
                      command = check_fun)
        button.pack(side=tk.BOTTOM) #button calls the check_fun function   
        
class EndFrameGame(tk.Tk): #called by wrongAnswer function with PageOneSix as starting frame

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (PageFinal, PageOneSix):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(PageOneSix)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class PageFinal(tk.Frame):

    def __init__(self, parent, controller):
      tk.Frame.__init__(self, parent)
      def restartGame(): #function to enable Play Again option
          global app
          global corrCount
          corrCount = 0
          app.destroy() #destroy and build with StartFrame
          app = StartFrame()
          app.geometry("600x400")
          app.resizable(width=False, height=False)
          app.mainloop()
      label = tk.Label(self, text="Correct!!!", font=SMALL_FONT)
      label.pack(pady=10,padx=10)
      label = tk.Label(self, text="You answered ALL 15 questions", font=SMALL_FONT)
      label.pack(pady=10,padx=10)
      label = tk.Label(self, text="Congratulations! You would have won £1 million!", font=SMALL_FONT)
      label.pack(pady=10,padx=10)
      button = tk.Button(self, text="Play Again?",
                          command=restartGame) #button calls restartGame function
      button.pack()
      button = tk.Button(self, text = "Exit",
                      command = lambda: exit())
      button.pack(side=tk.BOTTOM)

class PageOneSix(tk.Frame): #wrong answer frame

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        def restartGame():
          global app
          global corrCount
          corrCount = 0
          app.destroy()
          app = StartFrame()
          app.geometry("600x400")
          app.resizable(width=False, height=False)
          app.mainloop()
        label = tk.Label(self, text="Wrong!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="You answered "+str(corrCount)+" questions", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="You would have won "+str(corrCount*1000)+" £", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        button = tk.Button(self, text="Play Again?",
                            command=restartGame)
        button.pack()
        button = tk.Button(self, text="Quit?",
                            command=lambda: exit())
        button.pack()
        
#questions database
#adding methods to the class  
class Trivia:
  def __init__(self, question, correctAnswer, otherAnswers):
    self.question = question
    self.corrAnsw = correctAnswer
    self.otherAnsw = otherAnswers
#correct answer outside of list, is added in for loop inside PageOne class
triviaList = [Trivia("Where is Gdansk?", "in Poland", ["in Russia", "in Estonia", "in Latvia"]),
Trivia("What does BBC stand for?", "British Broadcasting Corporation", ["British Broadcasting Company", "British Baking Company", "Belgium Broadcasting Corporation"]),
Trivia("What nut is used to make marzipan?", "Almonds", ["Walnut", "Hazelnut", "Peanut"]),
Trivia("What element does 'O' represent on the periodic table?", "Oxygen", ["Ozone", "Osmium", "Oleum"]),
Trivia("Who was British Prime Minister before Theresa May?", "David Cameron", ["Gordon Brown", "Boris Johnson", "Jeremy Corbyn"]),
Trivia("Which of the following is not an African country?", "Malaysia", ["Madagascar", "Djibouti", "South Africa"]),
Trivia("What's the name of the river that runs through Egypt?", "Nile", ["Nigel", "Niger", "Norway"]),
Trivia("In meters, how long is an Olympic swimming pool?", "50", ["70", "90", "100"]),
Trivia("What's the name of the Royal family's castle in Scotland?", "Balmoral", ["Richmond", "Buckingham", "Durotan"]),
Trivia("Who did Orlando Bloom play in Pirates Of The Caribbean?", "Will Turner", ["Black Beard", "Red Beard", "Blue Beard"]),
Trivia("Which English town has football teams called United and Wednesday?", "Sheffield", ["Manchester", "Liverpool", "York"]),
Trivia("How many people are there on an English jury?", "12", ["10", "8", "15"]),
Trivia("What's the highest mountain in the world?", "Mount Everest", ["Montblanc", "K2", "Mount Fuji"]),
Trivia("How many wives did Henry VIII have?", "Six", ["Five", "Seven", "Eight"]),
Trivia("What's the name of Andy Murray's tennis playing brother?", "Jamie", ["John", "Jerry", "Jack"]),
Trivia("Where would you find the Golden Gate bridge?", "San Francisco", ["Los Angeles", "Sacramento", "Las Vegas"]),
Trivia("What year did World War II end?", "1945", ["1944", "1946", "1939"]),
Trivia("Who is Ashton Kutcher married to?", "Mila Kunis", ["Katy Perry", "Rihanna", "Beyonce"]),
Trivia("What's the capital of Spain?", "Madrid", ["Barcelona", "Oviedo", "Andorra"]),
Trivia("How many makes up a baker's dozen?", "13", ["12", "10", "11"]),
Trivia("Who was the president of the United States of America before Donald Trump?", "Barack Obama", ["Bill Clinton", "George Bush Jr.", "George Bush"]),
Trivia("What breed of dog does Queen Elizabeth II famously own?", "Corgis", ["Bulldogs", "Yorkshire Terriers", "Pugs"]),
Trivia("What is the capital of Australia?", "Canberra", ["Sydney", "Melbourne", "Wellington"]),
Trivia("How many letters in the word hippopotamus?", "12", ["11", "13", "10"]),
Trivia("What is the largest muscle in the body?", "The gluteus maximus or Buttocks", ["Biceps", "Triceps", "Hamstring"]),
Trivia("What famous battle happened in 1066?", "The Battle Of Hastings", ["The Battle Of Agincourt", "The Battle Of Trafalgar", "The Battle Of Termopile"]),
Trivia("What is Sweden's capital city?", "Stockholm", ["Uppsala", "Malmo", "Norrkoping"]),
Trivia("Which African country was formerly known as Abyssinia?", "Ethiopia", ["Somalia", "Nigeria", "Egypt"]),
Trivia("In which European city would you find Orly airport?", "Paris", ["Nice", "Monaco", "Lille"]),
Trivia("Which singer’s real name is Stefani Joanne Angelina Germanotta?", "Lady Gaga", ["Maddonna", "Gwen Stefani", "Katy Perry"]),
Trivia("Which country consumes the most chocolate per capita?", "Switzerland", ["Belgium", "United Kingdom", "USA"]),
Trivia("In the United Kingdom, what is the day after Christmas known as?", "Boxing Day", ["Unboxing Day", "Good Friday", "Black Friday"]),
Trivia("What is the tallest breed of dog in the world?", "The Great Dane", ["Husky", "TerraNova", "Caucasian Shepherd"]),
Trivia("What is the world’s biggest island?", "Greenland", ["Britain", "Madagascar", "Australia"]),
Trivia("What is the smallest ocean in the world?", "The Arctic", ["Atlantic", "Pacific", "Antarctic"]),
Trivia("What color eyes do most humans have?", "Brown", ["Blue", "Green", "Gray"])]


corrCount = 0
userAnsw = 0
app = StartFrame() #assigning first frame to StartFrame
app.geometry("600x400")
app.resizable(width=False, height=False)
app.mainloop()



