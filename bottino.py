import time
import socket
import random
import threading
from playsound import playsound
from gtts import gTTS
import os
from tkinter import *
from PIL import ImageTk,Image
from os import walk

def get_filenames_in_list(dir):
    _, _, filenames = next(walk(dir))
    return filenames

# ("abcdc1defgc1adasc2...",[c1,c2,...]) ---> [[[abcd],[defg],...]...]
def string_to_list_r(string,c_list=[' ','\n'],k=-1):
  result=[]
  if k+len(c_list)+1==0:return string
  for element in string.split(c_list[k]):
    result.append(string_to_list_r(element,c_list,k-1))
  return result

f = open("config.txt", "r")
f_content = f.read()
list = string_to_list_r(f_content,['>','\n'])

#carico la configurazione dal file
NICK = list[0][1]
PASS = list[1][1]
start_message = list[2][1]
stop_message = list[3][1]
meme_sound = list[4][1]
badwords_sound = list[5][1]
memedir_path = list[6][1]
badwords = string_to_list_r(list[7][1],[','])
tts = list[8][1]
show_time = int(list[9][1])

def send_message(message):
    global s
    try:
        s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))
    except Exception as e:
        erfile = open("errorlog.txt", "w")
        erfile.write("errore nella funzione \"send_message\"")
        erfile.close()
        exit()

occupato2 = False
def onMeme():
    global show_time
    global occupato2
    global label
    if not occupato2:
        occupato2 = True
        files = get_filenames_in_list(memedir_path)
        n = random.randint(0,count_files(memedir_path)-1)
        path = '{}\\{}'.format(memedir_path,files[n])
        #img = ImageTk.PhotoImage(Image.open(path))
        img = ridimensiona(path)
        playsound(meme_sound)
        label['image'] = img
        time.sleep(show_time)
        label['image'] = ''
        occupato2 = False

occupato = False
def onTTS(message):
    global occupato
    if message == "-tts":
        send_message("/me devi aggiungere il messaggio da leggere dopo il comando")
    else:
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
    return len([1 for x in os.scandir(dir) if x.is_file()])

def ridimensiona(path):
    img = Image.open(path)
    formato = img.height/img.width
    img = img.resize((round(1 / formato * 600), round(600)))
    if img.width>800:
        img = img.resize((round(800),round(formato*800)))
    return ImageTk.PhotoImage(img)

def init():
    global s
    HOST = "irc.twitch.tv"
    PORT = 6667
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
    s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
    s.send(bytes("JOIN #" + NICK + " \r\n", "UTF-8"))

try:
    init()
except:
    print("ERRORE INIT")
    exit()

try:
    send_message("/me {}".format(start_message))
except:
    print("ERRORE SEND START")
    exit()

last_sender = NICK
spam_time = 900 #15 minuti
last_spam = time.time()
last_ping = time.time()
spam = True
def spam_and_keep():
    global last_spam
    global last_sender
    def delta_data(t):
        return time.time()-t
    def spammino(t):
        global last_spam
        global  last_sender
        if delta_data(t)>=spam_time and last_sender != NICK:
            send_message("/me HEY! questo bot è stato fatto da s4m4s[https://twitch.tv/s4m4s], clicca sul link per più info")
            last_sender = NICK
            last_spam=time.time()
    def keepalive(t):
        global last_ping
        if delta_data(t) >= 60:  # manda una stringa vuota ogni minuto per mantenere il collegamento attivo, non viene visualizzata in da chat
            send_message("")
            last_ping= time.time()

    while True:
        try:
            if spam:
                spammino(last_spam)
            keepalive(last_ping)
        except Exception as e:
            erfile = open("errorlog.txt", "w")
            print(repr(e))
            stringa = "errore nella funzione \"spam\" tipo dell'errore: "
            erfile.write(stringa + repr(e))
            erfile.close()
            on_closing()
            return

def bot():
    global last_sender
    global root
    try:
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
                last_sender = username

                print(username + ": " + message)
                if message == "-s4m4s":
                    send_message('/me caro '+ username +' questo bot è stato fatto da s4m4s![https://twitch.tv/s4m4s]')
                if message == "-meme":
                    onMeme()
                if message.__contains__("-tts"):
                    if len(message)<204 and tts == "true":
                        onTTS(message)
                    else: send_message(username + ' contieniti bro')

    except Exception as e:
        erfile = open("errorlog.txt", "w")
        stringa = "errore nella funzione \"bot\" tipo dell'errore: "+repr(e)
        print(stringa)
        erfile.write(stringa + repr(e))
        erfile.close()
        root.destroy()
        exit()

def on_closing():
    send_message("/me {}".format(stop_message))
    root.destroy()

root = Tk()
root.title('il bottino twitch di samas 1.0')
root.geometry("800x600")
root.config(bg="green")

label = Label(bg="green")
label.pack(fill=BOTH, expand=True)

t1 = threading.Thread(target=bot)
t1.setDaemon(True)
t1.start()

t2 = threading.Thread(target=spam_and_keep)
t2.setDaemon(True)
t2.start()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

#exit()

# l'authcode https://twitchapps.com/tmi/
# per l'eseguibile con pyinstaller "pyinstaller --onefile -w bottino.py" nel cmd con il virtualenv attivo