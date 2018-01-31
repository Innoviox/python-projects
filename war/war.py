#images taken from opensourcegaming.com and
#converted to gifs at http://image.online-convert.com/convert-to-gif
from tkinter import *
import random
import time
import pygame.mixer
import simpleaudio as sa
random.seed()
pygame.mixer.init()
root = Tk()
root.geometry("%dx%d%+d%+d"% (root.winfo_screenwidth(), root.winfo_screenheight(), 0, 20))
root.title("War!")
numbers = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'A', 'J', 'Q', 'K']
suits = ["clubs", "hearts", "spades", "diamonds"]
buttons = {}
deck1 = []
deck2 = []
center = {"d1":[], "d2":[]}
label1 = Label(root, width = 50, height = 3)
label2 = Label(root, width = 50, height = 3)
label1.place_configure(x=0, y=0)
label2.place_configure(x=0, y=350)
label1.pack()
label2.pack()
x=0
y=50
x2 = 0
y2 = 400

def popup(root, header, text, windowHeight=500, windowWidth=500, winx=0, winy=0):
    def closePopup():
        window.destroy()
    window = Toplevel(root, height=windowHeight, width=windowWidth)
    window.wm_title(header)
    label = Label(window, text=text, relief = SUNKEN)
    label.place(x=winx, y=winy, height = 500, width = 500)
    button = Button(window, text="Close")
    button.config(command=closePopup)
    button.place(x=300, y=300)

        
def get_posscards():
    global posscards
    posscards = []
    for i in numbers:
        for j in suits:
            posscards.append(i+"_of_"+j+".gif")
def play(audio_file_path):
    #pygame.mixer.Sound(audio_file_path).play()
    pass
def create_random_card(xpos, ypos, col=False):
    img = PhotoImage(file="resources/"+random.choice(numbers)+"_of_"+random.choice(suits)+".gif")
    button = Label(root, image=img)
    button.img = img
    if col:
        button.grid(row=xpos, column=ypos)
    else:
        button.place_configure(x=xpos, y=ypos)
    buttons.append(button) 
def create_card(name, undername, xpos, ypos, typ, col=False):
    img = PhotoImage(file="resources/"+name)
    button = Button(root, image=img)
    button.config(command=lambda undername=undername: flip(button, undername))
    button.img = img
    button.subimg = undername
    button.typ = typ
    button.name = name
    buttons[undername] = button
    if col:
        button.grid(row=xpos, column=ypos)
    else:
        button.place_configure(x=xpos, y=ypos)  
def create_deck():
    for i in deck1:
        deck1.remove(i)
    get_posscards()
    for i in range(30):
        random.shuffle(posscards)
        print("Shuffling...")
    subi = "back.gif"
    for i in range(0, len(posscards), 2):
        create_card(subi, posscards[i], x, y, "d1")
        create_card(subi, posscards[i+1], x2, y2, "d2")
        deck1.append(posscards[i])
        deck2.append(posscards[i+1])
    #deck1[-1] = "3_of_clubs.gif"
    #deck2[-1] = "3_of_hearts.gif"
    update()   
def flip(button, name):
    play("fanfare.flac")
    if button.typ == "d1":
        if center["d1"] == []:
            if deck1[0]=="redo.gif":
                for button in center:
                    button.destroy()
                
                create_deck()
            else:
                img = PhotoImage(file="resources/"+name)
                button.place_configure(x=button.winfo_x()+210)
                button.config(image=img, command=null)
                button.img = img
                button.lift()
                deck1.remove(name)
                center["d1"] = [button]
    else:
        if center["d2"] == []:
            if deck2[0]=="redo.gif":
                for button in center:
                    button.destroy()
                
                create_deck()
            else:
                img = PhotoImage(file="resources/"+name)
                button.place_configure(x=button.winfo_x()+210)
                button.config(image=img, command=null)
                button.img = img
                button.lift()
                deck2.remove(name)
                center["d2"] = [button]
    update()
    root.update_idletasks()
    root.update()
    time.sleep(0.5)
    compare()
    update()    
def compare():
    if len(center["d1"])>0 and len(center["d2"])>0:
        #print(numbers.index(center["d1"][0].subimg[0]))
        if numbers.index(center["d1"][0].subimg[0])>\
           numbers.index(center["d2"][0].subimg[0]):
            deck1.insert(0, center["d1"][0].subimg)
            deck1.insert(0, center["d2"][0].subimg)
            center["d1"][0].destroy()
            center["d2"][0].destroy()
            center["d1"] = []
            center["d2"] = []
            popup(root, "Deck 1 Won", "Deck 1 wins that battle!!!")
        elif numbers.index(center["d1"][0].subimg[0])<\
           numbers.index(center["d2"][0].subimg[0]):
            deck2.insert(0, center["d1"][0].subimg)
            deck2.insert(0, center["d2"][0].subimg)
            center["d1"][0].destroy()
            center["d2"][0].destroy()
            center["d1"] = []
            center["d2"] = []
            popup(root, "Deck 2 Won", "Deck 2 wins that battle!!!")
        else:
            war()
    update()    
def war():
    #Flip function, except will flip farther and ignores subcenter argubouncing
    for i in range(4):
        button = buttons[deck1[-1]]
        img = PhotoImage(file=button.subimg)
        button.place_configure(x=button.winfo_x()+210 * (i+2))
        button.config(image=img, command=null)
        button.img = img
        button.lift()
        deck1.remove(button.subimg)
        center["d1"].append(button)
        update()
    for i in range(4):
        button = buttons[deck2[-1]]
        img = PhotoImage(file=button.subimg)
        button.place_configure(x=button.winfo_x()+210 * (i+2))
        button.config(image=img, command=null)
        button.img = img
        button.lift()
        deck2.remove(button.subimg)
        center["d2"].append(button)
        update()
    directcompare(center["d1"][-1], center["d2"][-1])
def directcompare(c1, c2):
    time.sleep(0.5)
    #again ignores subcenter argubouncing and subaliasing; specified proarguments
    if numbers.index(c1.subimg[0])>\
       numbers.index(c2.subimg[0]):
        for i in center["d1"]:
            deck1.insert(0, i.subimg)
        for i in center["d2"]:
            deck1.insert(0, i.subimg)

        for i in center["d1"]:
            i.destroy()
        for i in center["d2"]:
            i.destroy()
        center["d1"] = []
        center["d2"] = []
        popup(root, "Deck 1 Won", "Deck 1 wins that war!!!")
        
    elif numbers.index(c1.subimg[0])<\
       numbers.index(c2.subimg[0]):
        for i in center["d1"]:
            deck2.insert(0, i.subimg)
        for i in center["d2"]:
            deck2.insert(0, i.subimg)

        for i in center["d1"]:
            i.destroy()
        for i in center["d2"]:
            i.destroy()
        center["d1"] = []
        center["d2"] = []
        popup(root, "Deck 2 Won", "Deck 2 wins that war!!!")
    else:
        war()
    update()
def update():
    label1.place_configure(x=0, y=0)
    label2.place_configure(x=0, y=350)
    label1.config(text = "Deck 1: " + str(len(deck1)) + " cards")
    label2.config(text = "Deck 2: " + str(len(deck2)) + " cards")
    label1.lift()
    label2.lift()
    root.update_idletasks()
    root.update()
    for i in buttons.values():
        if not (i in center["d1"]) and (not (i in center["d2"])):
            i.destroy()
    for i in range(0, len(deck1), 1):
        create_card("back.gif", deck1[i], x, y, "d1")
    for i in range(0, len(deck2), 1):
        create_card("back.gif", deck2[i], x2, y2, "d2")        
def null(): 
	pass

create_deck()
root.mainloop()
