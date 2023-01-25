import speech_recognition as sr # recognise speech
import random, pyttsx3, time
from PIL import Image
import pyautogui #screenshot
import time, random, pyttsx3
import os # to remove created audio files
import datetime
from time import ctime # get time details
import webbrowser # open browser
import pyaudio, struct, pvporcupine 
import wikipedia, subprocess


class person:
    name = ''
    def setName(self, name):
        self.name = name

class asis:
    name = ''
    def setName(self, name):
        self.name = name

def there_exists(terms, voice_data):
    for term in terms:
        if term in voice_data:
            return True


# listen for audio and convert it to text:
def record_audio():
    # initialise a recogniser
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 100
    with sr.Microphone() as source: # microphone as source
        audio = recognizer.listen(source, 2, 5)  # listen for the audio via source
        print("Done Listening")
        voice_data = ''
        try:
            voice_data = recognizer.recognize_google(audio, language="en-IN")  # convert audio to text
            print(">>", voice_data.lower()) # print what user said
        except sr.UnknownValueError: # error: recognizer does not understand
            engine_speak('I did not get that')
            return "none"
        except sr.RequestError:
            engine_speak('Sorry, the service is down') # error: recognizer is not connected
        except Exception as e:
            engine_speak("Do you said something")
            return "none"
        # if(voice_data!=''):
        return voice_data.lower()

# get string and make a audio file to be played
def engine_speak(audio_string):
    audio_string = str(audio_string)
    print(asis_obj.name + ":", audio_string) # print what app said
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 180)
    engine.say(audio_string)
    engine.runAndWait()


# greets user first time depending on the time of device 
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        engine_speak(f"Good Morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        engine_speak(f"Good Afternoon, its {tt}")
    else:
        engine_speak(f"Good Evening, its {tt}")
    engine_speak("Do you need any helping hand boss")


# responds to your queries - (tasks)
def respond(voice_data):
    # 1: greeting
    if there_exists(["hey","hi","hello"], voice_data):
        greetings = ["hey, how can I help you", "hey, what's up?", "I'm listening", "may I help you with something?", "hello"]
        greet = random.choice(greetings)
        engine_speak(f"{greet} {person_obj.name}")
        engine_speak("What about you sir?")

    # 2: name
    if there_exists(["what is your name","tell me about yourself","tell me your name"], voice_data):
        if asis_obj.name:
            engine_speak("My name is " + asis_obj.name + " boss.")
            engine_speak(f"I am a virtual assistant made by {person_obj.name}. Just like any other assistants I can lend you my assistance in completing minimal tasks.")
        else:
            engine_speak("i dont know my name . what's your name?")

    if there_exists(["my name is", "I am"], voice_data):
        person_name = voice_data.split("is")[-1].strip()
        engine_speak("okay, i will remember that your name is " + person_name)
        person_obj.setName(person_name) # remember name in person object

    # 3: greeting
    if there_exists(["how are you","how are you doing"], voice_data):
        engine_speak("I'm very well, thanks for asking " + person_obj.name)
    
    if there_exists(["i am fine", "i am good", "very well"], voice_data):
        engine_speak("That's very good to hear sir. Hope you have a cheerful day.")

    # 4: time
    if there_exists(["what's the time","tell me the time","what time"], voice_data):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = "12"
        else:
            hours = time[0]
        minutes = time[1]
        time = hours + " hours and " + minutes + " minutes"
        engine_speak(time)

    #7: get stock price / item(object) price
    if  there_exists(["price of", "price for"], voice_data):
        search_term = voice_data.replace("of", "for").split("for ")[-1]
        url = "https://google.com/search?q=" + search_term
        webbrowser.get().open(url)
        engine_speak("Here is what I found for " + search_term + " on google")

    # 5: searching
    if there_exists(["search"], voice_data) and 'price' not in voice_data:
        search_term = str(voice_data.split("search ")[-1]).replace(" on youtube", "")
        print(search_term)
        if 'google' in voice_data and 'youtube' not in voice_data and 'amazon' not in voice_data:
            engine_speak("Searching results on google")
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            engine_speak("Here is what I found for" + search_term + " on google")
        elif there_exists(["youtube"], voice_data) and 'amazon' not in voice_data:
            engine_speak("Searching youtube for " + search_term)
            url = "https://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            engine_speak("This is what I found for " + search_term + " on youtube")
        elif there_exists(['amazon'], voice_data):
            engine_speak("searching" + search_term +  " on amazon.com for you boss")
            search_term = voice_data.split("search")[-1]
            url="https://www.amazon.in/s?k="+search_term
            webbrowser.get().open(url)
            engine_speak("here are the products you wanted on amazon.com")
        elif 'youtube' and 'amazon' not in voice_data:
            engine_speak("Searching google for " + search_term)
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            engine_speak("this is what I found for " + search_term + " on google")
    
    # search for music
    if there_exists(["play music", "play songs"], voice_data):
        url="https://open.spotify.com/search/"
        webbrowser.get().open(url)
        engine_speak("You are listening to spotify, enjoy sir")
         
    #make a note
    if there_exists(["make a note", "open notes"], voice_data):
        search_term=voice_data.split("for")[-1]
        url="https://keep.google.com/#home"
        webbrowser.get().open(url)
        subprocess.Popen(["StickyNotes.exe"])
        engine_speak("Here you can make notes")

    # opening websites and applications
    if "open" in voice_data:
        open(voice_data)
        
    #8 time table
    if there_exists(["show my time table"], voice_data):
        im = Image.open(r"C:\\Users\\MarvaL\\Pictures\\methodology.png")
        im.show()
    
    #9 weather
    if there_exists(["weather","tell me the weather report","whats the condition outside"], voice_data):
        search_term = voice_data.split("for")[-1]
        url = "https://www.google.com/search?sxsrf=ACYBGNSQwMLDByBwdVFIUCbQqya-ET7AAA%3A1578847393212&ei=oUwbXtbXDN-C4-EP-5u82AE&q=weather&oq=weather&gs_l=psy-ab.3..35i39i285i70i256j0i67l4j0i131i67j0i131j0i67l2j0.1630.4591..5475...1.2..2.322.1659.9j5j0j1......0....1..gws-wiz.....10..0i71j35i39j35i362i39._5eSPD47bv8&ved=0ahUKEwiWrJvwwP7mAhVfwTgGHfsNDxsQ4dUDCAs&uact=5"
        webbrowser.get().open(url)
        engine_speak("Here is what I found for on google")

    #10 stone paper scisorrs
    if there_exists(["game", "rock paper scissor"], voice_data):
        rps()
        
    #11 toss a coin
    if there_exists(["flip a coin","can I have a toss", "toss", "toss a coin"], voice_data):
        engine_speak("tossing a coin for you boss...")
        moves=["heads", "tails"]   
        cmove=random.choice(moves)
        engine_speak("I think I chose " + cmove + " " + person_obj.name)

    #12 calc
    if there_exists(["open calculator"], voice_data):
        os.startfile(r"C:\Windows\System32\calc.exe")
        engine_speak("calculator opened, this may help you boss...s")
        # if opr == '+' or 'add' or 'plus':
        #     engine_speak(int(voice_data.split()[0]) + int(voice_data.split()[2]))
        # elif opr == '-' or 'minus':
        #     engine_speak(int(voice_data.split()[0]) - int(voice_data.split()[2]))
        # elif opr == 'multiply':
        #     engine_speak(int(voice_data.split()[0]) * int(voice_data.split()[2]))
        # elif opr == 'divide':
        #     engine_speak(int(voice_data.split()[0]) / int(voice_data.split()[2]))
        # elif opr == 'power':
        #     engine_speak(int(voice_data.split()[0]) ** int(voice_data.split()[2]))
        # else:
        #     engine_speak("Wrong Operator")
        
    #13 screenshot
    if there_exists(["capture my screen","take a screenshot", "snap of my screen"], voice_data):
        myScreenshot = pyautogui.screenshot()
        ss = random.randint(1000000, 2000000)
        myScreenshot.save('C:\\Users\\MarvaL\\Documents\\ScreenShots\\ss.png') 
        engine_speak("Screenshot taken sir. you can view it by screenshots folder")

    elif there_exists(["open screenshots folder", "show screenshots"], voice_data):
        engine_speak("opening screenshots for you")
        os.startfile(r"C:/Users/MarvaL/Documents/ScreenShots")
        engine_speak("screenshots folder opened for you boss")

    # exit
    elif there_exists(["you can leave", "your time is over", "exit", "goodbye", "you need a break", "you can sleep", "take a sleep"], voice_data):
        engine_speak("we could continue more, but..........., you can call me anytime you want!")
        engine_speak("Have a good day boss..... Bye.....!")
        exit()


def open(voice_data):
    # search_term=voice_data.split("open")[-1]
    if there_exists(["whatsapp"], voice_data):
        url="https://web.whatsapp.com/"
        webbrowser.get().open(url)
        engine_speak("opening whatsapp for you boss")
    elif there_exists(["instagram"], voice_data):
        engine_speak("opening instagram for you boss")
        url="https://www.instagram.com/"
        webbrowser.get().open(url)
        engine_speak("instagram opened, enjoy " + person_obj.name)
    elif there_exists(["mails", "gmail"], voice_data):
        url="https://mail.google.com/mail/u/0/#inbox"
        webbrowser.get().open(url)
        engine_speak("here you can check your gmail")
    elif there_exists(["amazon.com", "amazon"], voice_data):
        engine_speak("opening amazon.com for you boss")
        url="https://www.amazon.in/"
        webbrowser.get().open(url)
        engine_speak("now you can search anything you want on amazon.com")
    elif  there_exists(["twitter"], voice_data):
        url="https://twitter.com/"
        webbrowser.get().open(url)
        engine_speak("opening twitter for you")
    elif  there_exists(["google"], voice_data):
        url="https://google.com/"
        webbrowser.get().open(url)
        engine_speak("opening google for you, here you can search anything...")
    elif  there_exists(["chrome", "google chrome"], voice_data):
        os.startfile(r"C:\Users\MarvaL\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        engine_speak("opening google chrome for you  boss")
    elif  there_exists(["chrome", "google chrome"], voice_data):
        os.startfile(r"C:\Users\MarvaL\AppData\Local\Programs\Microsoft VS Code\Code.exe")
        engine_speak("opening visual studio code for you, enjoy coding boss")
    

# rock paper scissor game code
def rps():
        engine_speak("choose among rock paper or scissor")
        voice_data = record_audio()
        moves=["rock", "paper", "scissor"]
    
        cmove=random.choice(moves)
        pmove=voice_data
        
        engine_speak("I chose " + cmove)
        engine_speak("You chose " + pmove)
        #engine_speak("hi")
        if pmove==cmove:
            engine_speak("the match is draw")
        elif pmove== "rock" and cmove== "scissor":
            engine_speak("You won boss")
        elif pmove== "rock" and cmove== "paper":
            engine_speak("I won sir")
        elif pmove== "paper" and cmove== "rock":
            engine_speak("You won boss")
        elif pmove== "paper" and cmove== "scissor":
            engine_speak("I won")
        elif pmove== "scissor" and cmove== "paper":
            engine_speak("You won boss")
        elif pmove== "scissor" and cmove== "rock":
            engine_speak("I won sir")

        engine_speak("do you wanna play again boss")
        voice_data = record_audio()
        if "yes" in voice_data:
            rps()
        else: 
            engine_speak("you can play again anytime")
            return

# wake word function - need to use wake word everytime for asking any queries
def engine_wake():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        access_key = "xdaz+lo9Vlxd79+zwXjkKFZAlgIcxPVCdxyxmGHXCUlCD7doYCnrpg=="
        porcupine = pvporcupine.create(access_key='xdaz+lo9Vlxd79+zwXjkKFZAlgIcxPVCdxyxmGHXCUlCD7doYCnrpg==',
        keyword_paths=['E:\\python\\basic virtual assistant\\wake_word\\justin_en_windows_v2_1_0.ppn'], keywords=['justin'])  # pvporcupine.KEYWORDS for all keywords
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(rate=porcupine.sample_rate, channels=1,format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h"*porcupine.frame_length, keyword)
            keyword_index = porcupine.process(keyword)
            if keyword_index >= 0:
                TaskExe()

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


# adds a pause to the program
time.sleep(2)

# we have assigned names to the assistant and person i.e. user, you can change person name
person_obj = person()
asis_obj = asis()
asis_obj.name = 'justin'

# this is task execution function where all the functions are called
def TaskExe():
    # while True:
    recording = ["What can I do", "How can I help you"]
    record = random.choice(recording)
    engine_speak(record)
    voice_data = record_audio() # get the voice input
    # print("Done")
    if(voice_data!=''):
        print("Q:", voice_data)
    respond(voice_data) # respond
    engine_speak("Awaiting your call boss.........")
    print(">>>> use keyword `justin` to activate the assistant <<<<")
    engine_wake()

if __name__ == "__main__":           
    wish() 
    TaskExe()