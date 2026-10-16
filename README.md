<<<<<<< HEAD

# Subhan AI — Voice Assistant

A Python-based AI voice assistant that can listen to voice input,
generate responses using a locally running language model through
Ollama, speak responses aloud, and handle supported computer commands.

This project was built as a learning project for the Subhan Developer
YouTube channel.

## Features

- Voice input through a microphone
- AI-generated responses using Ollama and Qwen 2.5 3B
- Spoken responses using Edge TTS
- English and Urdu language options
- Support for specific, allowlisted application and website commands

Features depend on the version of the code you download and your
computer configuration.

## How It Works

1. The microphone captures your request.
2. Speech recognition converts your speech into text.
3. The Python program checks for supported commands.
4. Normal questions are sent to the Ollama language model.
5. The response is converted into speech.
6. Aira speaks the answer.

## Requirements

- Windows 10 or Windows 11
- Python 3.13, for the version tested in this project
- Visual Studio Code (recommended)
- Ollama
- An internet connection for the current speech recognition
  and Edge TTS setup
- A working microphone and audio output

## Step 1 — Install the Tools

Install Python:
https://www.python.org/downloads/

Install Visual Studio Code:
https://code.visualstudio.com/

Install Ollama:
https://ollama.com/download

## Step 2 — Download the Project

Clone the repository, or download it as a ZIP from GitHub.

Open the project folder in Visual Studio Code.

## Step 3 — Download the AI Model

Open the VS Code terminal and run:

    ollama pull qwen2.5:3b

Wait for the download to finish.

## Step 4 — Create a Virtual Environment

In the terminal, run:

    py -3.13 -m venv .venv

Activate it in Windows PowerShell:

    .\.venv\Scripts\Activate.ps1

If activation is blocked by your PowerShell policy, use the
project's Python executable directly instead of changing security
settings unnecessarily.

## Step 5 — Install Python Packages

With the virtual environment active, run:

    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

If microphone or audio installation fails, check the troubleshooting
section and the official package documentation.

## Step 6 — Run the Assistant

Run:

    python main.py

Follow the startup instructions and select your language.

## Example Commands

Try asking a question, then test the supported commands shown in
the project documentation, such as opening Calculator or Notepad.

The exact commands depend on the current implementation.

## Troubleshooting

### Ollama is not responding
Make sure Ollama is installed and running. Confirm the model exists:

    ollama list

If needed, download it again:

    ollama pull qwen2.5:3b

### Python cannot find a package
Make sure you are using the Python interpreter from your project's
virtual environment, then reinstall the requirements.

### The microphone does not work
Check Windows microphone permissions, select the correct input
device, and test your microphone in another application.

### Voice recognition or speech output fails
The current setup uses online services for speech recognition
and Edge TTS, so check your internet connection.

### An application does not open
Use a command supported by the current code and check that the
application is installed.

## Limitations

- The language model runs locally through Ollama.
- The current speech recognition and Edge TTS features need internet.
- Speech recognition can make mistakes.
- Available computer commands are limited to those implemented
  in the program.

## Learning and Contributions

This project is intended for learning Python and AI application
development. You can fork the repository, experiment with the code,
and suggest improvements.

## Credits

Built by Subhan Developer.

YouTube: [Add your YouTube channel URL]
GitHub: [Add your GitHub profile URL]
=======
# subhan-ai-voice-assistant
A Python AI voice assistant using Ollama, speech recognition, and text-to-speech.
>>>>>>> 6737c5b9577fc46915937944921b770261220475
