from gtts import gTTS
import playsound
import speech_recognition as sr


def speak(text):
    tts = gTTS(text=text , lang='en')
    filename= 'voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)


def repeat():
    r = sr.Recognizer()
    r.energy_threshold = 4000

    with sr.Microphone() as source:
        print('start speaking..\n')
        while True:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                speak(text)
                print('voice recognized!',text.lower())
                return text.capitalize()
            except Exception as e:
                return 'Come again?'
