from fastapi import FastAPI, File, UploadFile, HTTPException
from moviepy.editor import VideoFileClip
import io
from google.cloud import speech_v1p1beta1 as speech
import speech_recognition as sr

# Create FastAPI application instance with increased max request size
app = FastAPI(max_request_size=500 * 1024 * 1024)  # Set max request size to 500MB

# Function to convert video file to audio and perform speech recognition
def process_video_and_get_transcription(video_path):
    try:
        # Load the video clip
        video = VideoFileClip(video_path)

        # Extract audio
        audio = video.audio

        # Save the audio file
        audio.write_audiofile("uploaded_audio.wav")

        # Close the video clip
        video.close()

        # Initialize the recognizer
        recognizer = sr.Recognizer()

        # Load the audio file
        audio_file = "uploaded_audio.wav"

        # Use the recognizer to open the audio file
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        # Perform speech recognition
        text = recognizer.recognize_google(audio_data)

        return text
    except Exception as e:
        # Log the exception details
        print(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Failed to process the audio.")

# Define the upload endpoint
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded video file
        with open("uploaded_video.mp4", "wb") as buffer:
            buffer.write(await file.read())

        # Convert video to audio and perform speech recognition
        transcript = process_video_and_get_transcription("uploaded_video.mp4")

        # Return the text transcription
        return {"transcription": transcript.strip()}
    except Exception as e:
        # Log the exception details
        print(f"An error occurred: {str(e)}")
        # Raise HTTP exception with a more informative error message
        raise HTTPException(status_code=500, detail="Internal Server Error: Failed to process the audio.")
