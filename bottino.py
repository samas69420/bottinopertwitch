import time
from config import nick as NICK
from config import authcode as PASS
from config import banned_words as badwords
import socket
import random
import threading
from playsound import playsound
from gtts import gTTS
import os
from tkinter import *
from PIL import ImageTk,Image

def send_message(message):
    s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))

occupato2 = False
def onMeme():
    global occupato2
    global label
    if not occupato2:
        occupato2 = True
        n = random.randint(1,count_files("memes"))
        playsound('yeet.mp3')
        path = 'memes\\{}.png'.format(n)
        #img = ImageTk.PhotoImage(Image.open(path))
        img = ridimensiona(path)
        label['image'] = img
        time.sleep(8)
        label['image'] = ''
        occupato2 = False

occupato = False
def onTTS(message):
    global occupato
    def pulisci(messaggio):
        risultato = ""
        for i, element in enumerate(messaggio):
            if i > 3:
                risultato = risultato + element
        return risultato
    def containsBadWords(messaggio):
        for element in badwords:
            if messaggio.__contains__(element):
                return True
        return False
    if not occupato:
        if not containsBadWords(message):
            occupato = True
            gTTS(text=pulisci(message), lang='it', slow=False).save("ttsaudio.mp3")
            playsound("ttsaudio.mp3")
            os.remove("ttsaudio.mp3")
            occupato = False
        else:
            occupato = True
            playsound("noo.mp3")
            occupato = False

def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])

def ridimensiona(path):
    img = Image.open(path)
    formato = img.height/img.width
    img = img.resize((round(1 / formato * 600), round(600)))
    if img.width>800:
        img = img.resize((round(800),round(formato*800)))
    return ImageTk.PhotoImage(img)

#HOST = "irc.twitch.tv"
#PORT = 6667
#NICK = "bosdsd"
#PASS =

HOST = "irc.twitch.tv"
PORT = 6667

s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))

send_message('/me bot partito che worka incredibile WOOO s4m4sWeee s4m4sWeee')

def bot():
    global bcolor

    while True:
        line = str(s.recv(1024))
        if "End of /NAMES list" in line:
            break

    while True:
        for line in str(s.recv(1024)).split('\\r\\n'):
            parts = line.split(':')
            if len(parts) < 3:
                continue

            if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
                message = parts[2][:len(parts[2])]

            usernamesplit = parts[1].split("!")
            username = usernamesplit[0]

            print(username + ": " + message)
            if message == "-s4m4s":
                send_message('/me si sono proprio io ' + username)
            if message == "-meme":
                onMeme()
            if message.__contains__("-tts"):
                if len(message)<204:
                    onTTS(message)
                else: send_message(username + ' contieniti bro')


root = Tk()
root.title('dio bestia')
root.geometry("800x600")
root.config(bg="green")

label = Label(bg="green")
label.pack()

t1 = threading.Thread(target=bot)
t1.start()
root.mainloop()

# per l'authcode https://twitchapps.com/tmi/
# per l'eseguibile con pyinstaller "pyinstaller --onefile -w bottino.py" nel cmd con il virtualenv attivo
