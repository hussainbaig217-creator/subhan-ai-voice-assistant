
import asyncio
import itertools
import os
import shutil
import subprocess
import sys
import threading
import time
import uuid
import webbrowser

import edge_tts

# Pygame reads this during import; set it first to hide its support banner.
os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
import pygame
import requests
import speech_recognition as sr


# ==================================================
# SUBHAN AI — AIRA
# ==================================================

ASSISTANT_NAME = "Aira"
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_TAGS_URL = "http://localhost:11434/api/tags"
MODEL = "qwen2.5:3b"


LANGUAGES = {
    "english": {
        "recognition": "en-US",
        "voice": "en-US-AriaNeural",
        "system": (
            "You are Aira, the friendly female voice assistant "
            "of Subhan AI. Reply in natural, conversational English. "
            "Keep ordinary spoken answers concise, usually 1-4 sentences. "
            "Answer the exact question, avoid unnecessary introductions, "
            "and never pretend to perform actions you have not performed."
        ),
        "greeting": (
            "Hi! I'm Aira, your Subhan AI assistant. "
            "Take your time. What would you like to ask?"
        ),
        "goodbye": "Goodbye! Talk to you later.",
        "repeat": "Sorry, I didn't catch that. Please say it again.",
        "connection_error": (
            "Sorry, I couldn't connect to my AI model. "
            "Please check that Ollama is running."
        ),
    },
    "urdu": {
        "recognition": "ur-PK",
        "voice": "ur-PK-UzmaNeural",
        "system": (
            "You are Aira, the friendly female voice assistant "
            "of Subhan AI. Reply in natural Pakistani Urdu, using "
            "Urdu script. Keep ordinary spoken answers concise. "
            "Answer the exact question and avoid unnecessary introductions. "
            "If the user explicitly asks for English, reply in English."
        ),
        "greeting": (
            "السلام علیکم! میں ایرا ہوں، آپ کی سبھان اے آئی اسسٹنٹ۔ "
            "بتائیں، میں آپ کی کیا مدد کر سکتی ہوں؟"
        ),
        "goodbye": "اللہ حافظ! پھر بات ہوگی۔",
        "repeat": "معاف کیجیے، میں سمجھ نہیں سکی۔ دوبارہ بتائیں۔",
        "connection_error": (
            "معاف کیجیے، میں اپنے اے آئی ماڈل سے رابطہ نہیں کر سکی۔"
        ),
    },
}

current_language = "english"


# ==================================================
# SAFE COMPUTER CONTROL
# Only the websites and applications listed here
# can be opened through these voice commands.
# ==================================================

WEBSITES = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "chatgpt": "https://chatgpt.com",
}

APPS = {
    "notepad": ["notepad.exe"],
    "calculator": ["calc.exe"],
    "file explorer": ["explorer.exe"],
    "paint": ["mspaint.exe"],
}


def handle_computer_command(text):
    """Handle approved computer commands without using the AI to execute code."""

    command = text.lower().strip(" .!?")

    # Allow "Aira, open YouTube".
    if command.startswith("aira "):
        command = command[5:].strip()

    # Open only approved websites.
    for name, url in WEBSITES.items():
        if command in (
            f"open {name}",
            f"open {name} website",
        ):
            try:
                opened = webbrowser.open(url, new=2)

                if opened:
                    speak(f"Opening {name}.")
                else:
                    speak(
                        f"I tried to open {name}, "
                        "but the browser did not confirm the request."
                    )
            except Exception as error:
                print(f"Website error: {error}")
                speak(f"Sorry, I could not open {name}.")

            return True

    # Launch only the applications in the allowlist.
    for name, app_command in APPS.items():
        if command in (f"open {name}", f"launch {name}"):
            try:
                subprocess.Popen(app_command)
                speak(f"Opening {name}.")
            except OSError as error:
                print(f"Application error: {error}")
                speak(f"Sorry, I could not open {name}.")

            return True

    # Open VS Code only if its command is available.
    if command in (
        "open vs code",
        "launch vs code",
        "open visual studio code",
    ):
        code_path = shutil.which("code")

        if code_path:
            try:
                subprocess.Popen([code_path])
                speak("Opening Visual Studio Code.")
            except OSError as error:
                print(f"VS Code error: {error}")
                speak("Sorry, I could not open Visual Studio Code.")
        else:
            speak(
                "I could not find the VS Code command. "
                "Please check that VS Code is installed "
                "and available in your PATH."
            )

        return True

    return False


# ==================================================
# TEXT TO SPEECH
# ==================================================


def generate_speech(text, filename, voice):
    async def create_audio():
        communication = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="+0%",
            pitch="+0Hz",
        )
        await communication.save(filename)

    asyncio.run(create_audio())


def speak(text):
    """Speak a complete response using the selected female voice."""

    filename = os.path.join(
        os.environ.get("TEMP", "."),
        f"aira_{uuid.uuid4().hex}.mp3",
    )

    print(f"\n{ASSISTANT_NAME}: {text}\n")

    try:
        voice = LANGUAGES[current_language]["voice"]
        generate_speech(text, filename, voice)

        pygame.mixer.music.stop()

        try:
            pygame.mixer.music.unload()
        except pygame.error:
            pass

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as error:
        print(f"Voice error: {error}")
        print("Check your internet connection and audio output.")

    finally:
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except pygame.error:
            pass

        try:
            if os.path.exists(filename):
                os.remove(filename)
        except OSError:
            pass


# ==================================================
# MICROPHONE — LONGER QUESTIONS
# ==================================================

recognizer = sr.Recognizer()

recognizer.pause_threshold = 2.0
recognizer.non_speaking_duration = 0.5
recognizer.phrase_threshold = 0.3
recognizer.dynamic_energy_threshold = True


def listen():
    with sr.Microphone() as source:
        print(
            f"\nListening in {current_language.title()}... "
            "Speak your complete question."
        )

        audio = recognizer.listen(
            source,
            timeout=20,
            phrase_time_limit=60,
        )

    print("Recognizing speech...")

    return recognizer.recognize_google(
        audio,
        language=LANGUAGES[current_language]["recognition"],
    ).strip()


# ==================================================
# THINKING SPINNER
# ==================================================

thinking = threading.Event()


def show_spinner():
    frames = itertools.cycle(["◐", "◓", "◑", "◒"])

    while thinking.is_set():
        sys.stdout.write(
            "\rAira is thinking " + next(frames) + "   "
        )
        sys.stdout.flush()
        time.sleep(0.12)


# ==================================================
# LOCAL AI — OLLAMA
# ==================================================

messages = []


def reset_system_prompt():
    global messages

    messages = [
        {
            "role": "system",
            "content": LANGUAGES[current_language]["system"],
        }
    ]


def get_ai_answer(user_text):
    messages.append({
        "role": "user",
        "content": user_text,
    })

    # Keep recent conversation history for faster processing.
    if len(messages) > 13:
        del messages[1:3]

    thinking.set()

    animation = threading.Thread(
        target=show_spinner,
        daemon=True,
    )
    animation.start()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "messages": messages,
                "stream": False,
                "keep_alive": -1,
                "options": {
                    "num_predict": 120,
                    "temperature": 0.5,
                },
            },
            timeout=180,
        )

        response.raise_for_status()
        answer = response.json()["message"]["content"].strip()

        if not answer:
            answer = (
                "معاف کیجیے، میں جواب نہیں بنا سکی۔"
                if current_language == "urdu"
                else "Sorry, I couldn't create an answer."
            )

        messages.append({
            "role": "assistant",
            "content": answer,
        })

        return answer

    except Exception:
        if messages and messages[-1]["role"] == "user":
            messages.pop()
        raise

    finally:
        thinking.clear()
        animation.join()

        sys.stdout.write("\r" + " " * 45 + "\r")
        sys.stdout.flush()


# ==================================================
# LANGUAGE SWITCHING
# ==================================================

def switch_language(new_language):
    global current_language

    current_language = new_language
    reset_system_prompt()

    if new_language == "urdu":
        speak("اب میں اردو میں بات کروں گی۔")
    else:
        speak("I'll speak in English now.")


# ==================================================
# VOICE COMMAND HANDLER
# ==================================================

def handle_command(text):
    """Handle exit, language switching, and computer commands."""

    command = text.lower().strip(" .!?")

    english_exit = {
        "exit",
        "quit",
        "goodbye",
        "stop assistant",
        "close assistant",
    }

    english_to_urdu = {
        "switch to urdu",
        "speak urdu",
        "urdu mode",
    }

    english_to_english = {
        "switch to english",
        "speak english",
        "english mode",
    }

    urdu_to_urdu = {
        "اردو میں بات کرو",
        "اردو میں بات کریں",
    }

    urdu_to_english = {
        "انگریزی میں بات کرو",
        "انگریزی میں بات کریں",
    }

    if command in english_exit:
        speak(LANGUAGES[current_language]["goodbye"])
        return True

    if command in english_to_urdu or command in urdu_to_urdu:
        switch_language("urdu")
        return True

    if command in english_to_english or command in urdu_to_english:
        switch_language("english")
        return True

    # Try approved computer commands before sending text to Ollama.
    if handle_computer_command(text):
        return True

    return False


# ==================================================
# STARTUP AND CONVERSATION LOOP
# ==================================================

def main():
    global current_language

    try:
        pygame.mixer.init()
    except pygame.error as error:
        print('\nAudio initialization failed; Aira cannot start voice output.')
        print(f'Details: {error}')
        print('Check your speakers/headphones and Windows audio output, then try again.')
        return

    print("=" * 48)
    print("              SUBHAN AI")
    print("          Your assistant is Aira")
    print("=" * 48)

    print("\nChoose your conversation language:")
    print("1. English")
    print("2. Urdu")

    choice = input("Enter 1 or 2 (default English): ").strip()

    current_language = "urdu" if choice == "2" else "english"
    reset_system_prompt()

    # Check that Ollama is running.
    try:
        response = requests.get(
            OLLAMA_TAGS_URL,
            timeout=5,
        )
        response.raise_for_status()

        available_models = [
            item.get("name", "")
            for item in response.json().get("models", [])
        ]

        if not any(
            name == MODEL or name.startswith(MODEL + ":")
            for name in available_models
        ):
            print(f"\nModel {MODEL} was not found in Ollama.")
            print(f"Run this command in another terminal: ollama pull {MODEL}")
            return

    except requests.RequestException as error:
        print("\nOllama is not responding.")
        print("Make sure Ollama is running.")
        print(f"Details: {error}")
        return

    try:
        with sr.Microphone() as source:
            print("\nCalibrating microphone. Please stay quiet...")
            recognizer.adjust_for_ambient_noise(
                source,
                duration=1.0,
            )

        speak(LANGUAGES[current_language]["greeting"])

        while True:
            try:
                user_text = listen()

                if not user_text:
                    continue

                print(f"\nYou: {user_text}")

                # Process exit, language, and computer commands first.
                if handle_command(user_text):
                    if user_text.lower().strip(" .!?") in {
                        "exit",
                        "quit",
                        "goodbye",
                        "stop assistant",
                        "close assistant",
                    }:
                        break

                    continue

                # Ordinary questions go to the local Ollama model.
                try:
                    answer = get_ai_answer(user_text)
                    speak(answer)

                except requests.RequestException as error:
                    print(f"\nAI connection error: {error}")
                    speak(
                        LANGUAGES[current_language]["connection_error"]
                    )

                except (KeyError, ValueError) as error:
                    print(f"\nInvalid AI response: {error}")
                    speak(
                        "Sorry, I had trouble creating an answer."
                        if current_language == "english"
                        else "معاف کیجیے، جواب میں مسئلہ ہو گیا۔"
                    )

                except Exception as error:
                    print(f"\nUnexpected AI error: {error}")
                    speak(
                        "Sorry, something went wrong while answering."
                        if current_language == "english"
                        else "معاف کیجیے، جواب دیتے ہوئے مسئلہ ہو گیا۔"
                    )

            except sr.WaitTimeoutError:
                print("I didn't hear anything. I'll listen again.")
                time.sleep(0.5)

            except sr.UnknownValueError:
                print("I couldn't understand the recording.")
                speak(LANGUAGES[current_language]["repeat"])
                time.sleep(0.5)

            except sr.RequestError as error:
                print(f"Speech recognition error: {error}")
                speak(
                    "Speech recognition needs an internet connection."
                    if current_language == "english"
                    else "آواز پہچاننے کے لیے انٹرنیٹ درکار ہے۔"
                )
                time.sleep(1.5)

    except KeyboardInterrupt:
        print("\nStopping Aira...")

    except (OSError, AttributeError) as error:
        print(f"Microphone or audio error: {error}")

    finally:
        thinking.clear()
        pygame.mixer.quit()
        print("Subhan AI has closed.")


if __name__ == "__main__":
    main()
