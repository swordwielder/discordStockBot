import speech_recognition as sr

if __name__ == "__main__":
    r = sr.Recognizer()
    r.energy_threshold = 4000 

    keyWord = 'listen bot'

    with sr.Microphone() as source:
        print('start speaking..\n')
        while True: 
            r.adjust_for_ambient_noise(source)  
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio)
                if keyWord.lower() in text.lower():
                    print('Keyword found.',text.lower())
            except Exception as e:
                print('Come again?.')  
