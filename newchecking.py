import azure.cognitiveservices.speech as speechsdk

# Replace 'your_subscription_key' and 'your_service_region' with your actual subscription key and region
speech_key = "your_subscription_key"
service_region = "your_service_region"

# Create a speech config object
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Create a speech recognizer object
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

# Specify audio file path
audio_file = "audio.wav"

# Open the audio file and recognize speech
with open(audio_file, "rb") as audio_file:
    speech_config.audio_stream_format = speechsdk.AudioStreamFormat(wav_header=True)
    result = recognizer.recognize_once_async(audio_file).get()

    # Print recognized text
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
