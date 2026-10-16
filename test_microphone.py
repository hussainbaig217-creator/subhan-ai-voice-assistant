import speech_recognition as sr

recognizer = sr.Recognizer()

try:
    with sr.Microphone() as source:
        print("Listening for up to 5 seconds. Say a short sentence...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    print("Recognizing speech...")
    text = recognizer.recognize_google(audio)
    print("You said:", text)

except sr.WaitTimeoutError:
    print("I didn't hear speech in time. Please try again.")
except sr.UnknownValueError:
    print("I heard audio, but couldn't understand the words.")
except sr.RequestError as error:
    print("Speech recognition service error:", error)
except OSError as error:
    print("Microphone error:", error);
