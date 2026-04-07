# Nebula - Virtual GUI Assistant

A Python-based virtual desktop assistant with a graphical interface built using Tkinter. Nebula can understand text commands, respond with text and voice, and perform various tasks on your Windows PC.

## Features

- **Voice responses** using text-to-speech (pyttsx3)
- **Wikipedia search** — just say "wikipedia \<topic\>"
- **Weather forecast** — ask "what's the weather in \<city\>"
- **Open applications** — Google Chrome, VLC, Notepad, VS Code, Paint, Calculator, and more
- **Web browsing** — open Google, YouTube, or search anything
- **System commands** — get current time, location, take a screenshot, shutdown
- **Music & Movies** — play random music or movies from local folders
- **Conversational responses** — greetings, small talk, about info

## Requirements

- Windows OS
- Python 3.x
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/virtualgui.git
   cd virtualgui
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the assistant:
   ```bash
   python Virtualgui.py
   ```

## Usage

Type your command in the input box and press **Send** or hit **Enter**.

### Example Commands

| Command | Response |
|---|---|
| `hello` / `hi` | Greeting |
| `who are you` | Introduces itself |
| `what time is it` | Current time |
| `weather in Delhi` | Weather forecast |
| `open youtube` | Opens YouTube in browser |
| `open chrome` | Launches Chrome |
| `wikipedia Python` | Wikipedia summary |
| `play music` | Plays random music |
| `shutdown` | Shuts down the system |
| `exit` | Closes the assistant |

## Dependencies

| Package | Purpose |
|---|---|
| `pyttsx3` | Text-to-speech engine |
| `wikipedia` | Wikipedia search |
| `requests` | Weather API & location |
| `tkinter` | GUI (built into Python) |

## Weather API

Weather data is fetched from [OpenWeatherMap](https://openweathermap.org/). The default city is set to **Ludhiana**. You can change the default city in `Virtualgui.py`.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Author

Made by **Aditya**
