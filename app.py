# DEVELOPED BY ONDREJ TOMASEK
# linkedin.com/in/ondrat

import speech_recognition as sr
import chatgpt_call
import pyttsx3
import pyautogui
from data import private_data
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()

def take_screenshot():
    # Create a directory if it doesn't exist
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Find the latest image number
    img_number = 1
    while os.path.exists(f"screenshots/img_{img_number}.jpg"):
        img_number += 1

    # Take screenshot
    screenshot = pyautogui.screenshot()

    # Save screenshot
    screenshot_path = f"screenshots/img_{img_number}.jpg"
    screenshot.save(screenshot_path)

    # Return the image name without extension
    return f"screenshots/img_{img_number}"

prompt_to_ask = "You are a PC technician and you assist people with their problems. Your responses are straightforward and you do not talk unnecessary stuff, you go right into the problem. The user knows where is the problem, you are here just to solve it and respond with the solution right away. You analyze image and respond to questions given with that screenshot. Your responses are short and well-structured, make it understandable for non-PC user and help the user solve the problem as quick and simple as possible. QUESTION:"

# Function to greet after recognizing "hey andrew"
def command_handler(command):
    screenshot = take_screenshot()
    chatgpt_response = chatgpt_call.analyze_image(image_name=screenshot, CHATGPT_API_KEY=private_data.CHATGPT_API_KEY, prompt_to_ask=prompt_to_ask + command)
    print(chatgpt_response)
    # READ OUT LOUD THE CHATGPT RESPONSE HERE
    engine.say(chatgpt_response)
    engine.runAndWait()

# Function to recognize voice
def recognize_voice():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Capture the audio input
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech Recognition
        text = recognizer.recognize_google(audio)

        # Check if "hey andrew" is in the recognized text
        if "hey andrew" in text.lower():
            # Get the command after "hey andrew"
            command = text.lower().replace("hey andrew", "").strip()
            command_handler(command)

    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

# Call the function to start voice recognition
recognize_voice()
