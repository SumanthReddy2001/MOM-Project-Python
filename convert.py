from google.cloud import speech_v1p1beta1 as speech

# Initialize SpeechClient
client = speech.SpeechClient()

# Specify recognition config
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)

# Open audio file and stream data in chunks
with open("uploaded_audio.mp3", "rb") as audio_file:
    content = audio_file.read()

    # Process audio in chunks
    chunk_size = 1024 * 1024  # 1MB
    offset = 0
    while offset < len(content):
        chunk = content[offset:offset + chunk_size]
        
        # Perform streaming speech recognition
        response = client.streaming_recognize(
            config=config,
            audio_config={"content": chunk}
        )

        for result in response.results:
            for alternative in result.alternatives:
                print("Transcript: {}".format(alternative.transcript))

        offset += chunk_size
