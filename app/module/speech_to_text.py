import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()


def run():
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic)
        audio2 = r.listen(mic)
                
    # Using google to recognize audio
    try:
        MyText = r.recognize_google(audio2, language="vi")
        return MyText
    except Exception:
        return "Vui lòng đọc lại"
    # SpeakText(MyText)
