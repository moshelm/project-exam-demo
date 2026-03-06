import speech_recognition as sr
from io import BytesIO


def stt_file(file:BytesIO, language : str = "en-US" ):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file) as af:
        file_data = recognizer.record(af)
        return recognizer.recognize_google(file_data,language=language)
