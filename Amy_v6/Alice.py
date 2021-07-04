import speech_recognition as sr 
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes


listener = sr.Recognizer()

engine = pyttsx3.init()
engine.setProperty("rate", 110) # word per minute
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

talk("i am your Alice")
talk("What can i help you")

def take_command():
    try:
        # Open microphone as source, listen this sBource
        with sr.Microphone() as source:

            print("Alice's listening,...")
            voice = listener.listen(source)
            listener.adjust_for_ambient_noise(source)         # listen for 1 second to calibrate the energy threshold for ambient noise levels
            command = listener.recognize_google(voice)
            command = command.lower()
            print("original sound: " + command)
            
            if "alice" in command:
                command = command.replace("alice",'')
                return command

            else:
                talk("please try again")
                command = ""
                return command
    except:
        pass

    # if nothing detected on microphone return command es empty string
    command = "" 
    return command

def run_alice():
    command = take_command()
    print("return command: " + command)

    if "play" in command:
        song_name = command.replace("play","")
        print("song:" + song_name)
        talk("Alice is playing " + song_name + "song")
        pywhatkit.playonyt(song_name)
    
    elif "time" in command:
        #time = datetime.datetime.now().strftime('%H:%M')
        time = datetime.datetime.now().strftime('%I:%M %p')
        print("Current time: " + time)
        talk("Current time: " + time)
    
    elif "wikipedia" in command:
        thing = command.replace("wikipedia","")
        info = wikipedia.summary(thing,1)
        print(info)
        talk(info)

    elif "joke" in command:
        print("Telling a jokes")
        talk(pyjokes.get_joke())
    
    elif "fun" in command:
        print("I am a Ai, not Rowan Atkinson")
        talk("I am a Ai, not Rowan Atkinson")
    
while True:
    run_alice()