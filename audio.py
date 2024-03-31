import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Load the audio file
audio_file = "audio.wav"

# Use the recognizer to open the audio file
recognizer = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)  # Google Speech Recognition
        # Or use a different engine, e.g., recognize_ibm(), recognize_sphinx(), etc.
        print("Text:", text)
    except sr.UnknownValueError:
        print("Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print("Could not request results from the service; {0}".format(e))
