import pyttsx3 as p
import speech_recognition as sr
import datetime
import os
import cv2
from bs4 import BeautifulSoup
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import sys
import time
import pyjokes
import requests
import pyautogui
import os.path

engine = p.init('sapi5')
voices = engine.getProperty('voices');
engine.setProperty('voices', voices[len(voices) - 1].id)

#text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


#To convert voice into text
def  takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source,timeout=5,phrase_time_limit=8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
    except Exception as e:
        return "null"
    return query

#to wish
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"good morning, its {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"good afternoon, its {tt}")
    else:
        speak(f"good evening, its {tt}")
    speak("i am pybot sir. please tell me how may i help you")
    print("Speak one of the following words to use specific feature:")
    print("open notepad: To open Notepad.\nVolume up or down or mute: For Volume Controls.")
    print("Day or Date: To get the current Day and Date.\nSearch File: To Search any file in system.")
    print("Open Chrome: To open the Chrome Browser. \nOpen Command Prompt: To open the command prompt.")
    print("Open Camera: To open laptops camera. \nTemperature: To get temperature of any city.")
    print("IP Address: To get the system's IP Address \n[Subject] Wikipedia: To about the subject on wikipedia.")
    print("Open Website: To open any website. \nClose or Kill current tab: To close the current tab of web browser.")
    print("Open Google: To open and search anything on google.\nVideo on Youtube: To play any video on Youtube.")
    print("Timer or Stopwatch: To set timer for minutes. \nWait: To activate Stand-by mode. \nJoke: To tell a joke. \nNews: To tell top 10 news-headlines.")
    print("Change Window: To switch applications. \nClose Application: To close any application.\nStop Listening: To Terminate program.")
    print("Shutdown or Restart or Sleep the system: To perform system functions.")

#Searching File
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name) 
 
#for news
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=d55e3e4edf81412c8944b9acb3c9223d'
    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page['articles']
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")

if __name__ == "__main__": #main program
    wish()
    while True:

        query = takecommand().lower()

        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
            speak("Sir do you want to dictate me to write?")
            c=takecommand()
            if "yes" in c:
                speak("Sir start Dictating...")
                while True:    
                    dn=takecommand().lower()
                    if 'exit dictation mode' in dn:
                        break
                    pyautogui.write(dn)
                    pyautogui.write('  ')
            elif "no" in c:
                speak("OK..")
            
        elif 'hi' in query or 'hello' in query:
            speak('Hello sir, how may I help you?')
            
        elif 'increase volume' in query or 'volume up' in query:
            pyautogui.press("volumeup")
        elif 'decrease volume' in query or 'volume down' in query:
            pyautogui.press("volumedown")
        elif 'volume mute' in query or 'mute' in query:
            pyautogui.press("volumemute")
            
        elif 'day' in query or 'date' in query:
            x=datetime.datetime.now()
            d=x.strftime("%A %d %B %Y ")
            speak("Today's day and date is "+d)
            
        elif 'search file' in query:
            p.speak("Sir please type your file name with extension")
            f=input("Enter your filename with extension:")
            p.speak("Please tell the drive to search in")
            d=input("Enter the Drive name to search in it:")
            s=":/"
            dr=d+s
            i=1
            se=find(f,dr)
            if se!=None :    
                fa="File found in "+se
                p.speak(fa)
                print(se)
                os.startfile(se)
            while se==None and i!=5:
                p.speak("File was not found in searched drive")
                p.speak("Please tell another drive to search in")
                d=input("Enter the Drive name to search in it:")
                dr=d+s
                i=i+1
                se=find(f,dr)
                if se==None:
                    print("File does not exist")
                    p.speak("File does not exist")
                else:
                    fa="File found in "+se
                    p.speak(fa)
                    print(se)
                    os.startfile(se)
        
        elif "open chrome" in query:
            apath = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            os.startfile(apath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k==27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "temperature" in query:
            speak("sir,temperature of which city?")
            t=takecommand()
            s="Temperature in "+t
            url="https://www.google.com/search?q="+s
            r=requests.get(url)
            data=BeautifulSoup(r.text,"html.parser")
            temp=data.find("div",class_="BNeawe").text
            speak("current "+s+" is "+temp)

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"your IP address is {ip}")

        elif "wikipedia" in query:
            speak("searching wikipedia....")
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=5)
            speak("according to wikipedia")
            speak(results)

        elif "open website" in query:
            speak("Which website do you want to open?")
            ws=takecommand().lower()
            webbrowser.open("www."+ws)

        elif "close application" in query:
            speak("Closing..")
            pyautogui.keyDown("alt")
            pyautogui.press("f4")
            pyautogui.keyUp("alt")

        elif "close current tab" in query or "kill current tab" in query:
            pyautogui.keyDown("ctrl")
            pyautogui.press("w")
            pyautogui.keyUp("ctrl")
        
        elif "open google" in query:
            speak("sir, what should i search on google")
            cm = takecommand().lower()
            kit.search(cm)

        elif "video on youtube" in query:
            speak("sir, which video would you like to play?")
            vc= takecommand().lower()
            kit.playonyt(vc)
            
        elif 'timer' in query or 'stopwatch' in query:
            speak("For how many minutes?")
            timing = takecommand()
            timing =timing.replace('minutes', '')
            timing = timing.replace('minute', '')
            timing = timing.replace('for', '')
            timing = float(timing)
            timing = timing * 60
            speak(f'I will remind you in {timing} seconds')
            time.sleep(timing)
            speak('Sir I am reminding you, your set time is finished')
            
        elif 'stop listening' in query:
            speak("okay sir, have a good day.")
            sys.exit()
        
        elif "wait" in query:
            while True:
                w= takecommand()
                if("ok listen" in w):
                    break

        elif "joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'change window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")
                   
        elif "news" in query:
            speak("please wait sir, fetching the latest news")
            news()
        speak("sir, do you have any other work for me?")    

