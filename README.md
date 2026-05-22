# Nebula — Full Laptop Assistant v2.0

A Python-powered virtual desktop assistant with a retro-terminal GUI built using PyQt5. Nebula understands text and voice commands, responds with text and speech, and can perform a wide range of laptop operations.

## Features

### System Controls
- **Volume** — increase, decrease, mute, unmute, or set to a specific level
- **Brightness** — increase, decrease, or set screen brightness
- **System Stats** — live CPU, RAM, disk usage, and battery status

### File & Process Management
- **File operations** — create folders, search for files, open files/folders by path, delete files
- **Process management** — list running apps, kill a process by name, open Task Manager
- **App launcher** — Chrome, Notepad, VLC, Calculator, CMD, PowerShell, File Explorer, Settings, Spotify, and common folders (Desktop, Downloads, Documents, Pictures)

### Productivity
- **Timers** — set multiple simultaneous countdown timers
- **Reminders** — timed reminders with a custom message
- **Calculator** — evaluate any math expression safely (`2^8`, `25 * 4 + 10`)
- **Clipboard** — read clipboard contents or copy text to clipboard
- **Type text** — type any text into a focused window via automation

### Information & Web
- **Weather** — live forecast via OpenWeatherMap
- **Wikipedia** — instant summaries
- **Location** — approximate location via IP
- **Network info** — local IP, WiFi name, and signal strength

### Music (Spotify)
- Play, pause, resume, skip, previous track
- Search and play any song by name
- Show currently playing track

### Power & Security
- **Lock screen**, **sleep**, **restart**, **log off**, **shutdown**

### AI Conversation
- Claude AI (Haiku) handles any query that doesn't match a built-in command
- Remembers the full conversation session (multi-turn context)
- Falls back to a Google search if the API key is not set

### Voice I/O
- Microphone input via SpeechRecognition
- Text-to-speech responses via pyttsx3

## Requirements

- Windows 10/11
- Python 3.10+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Lalith1018/Nebula-Virtual-Assistant.git
   cd Nebula-Virtual-Assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Open `Virtualgui.py` and fill in your API keys at the top of the file:
   ```python
   WEATHER_API_KEY       = 'your_openweathermap_key'
   SPOTIFY_CLIENT_ID     = 'your_spotify_client_id'
   SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
   ANTHROPIC_API_KEY     = 'your_anthropic_key'
   ```

4. Run the assistant:
   ```bash
   python Virtualgui.py
   ```

## Example Commands

| Command | Action |
|---|---|
| `volume up` / `set volume to 60` | Adjust system volume |
| `brightness down` / `set brightness to 40` | Adjust screen brightness |
| `battery` | Show battery percentage and status |
| `system stats` | CPU, RAM, disk, and battery overview |
| `cpu usage` / `ram usage` / `disk usage` | Individual stats |
| `show running apps` | List top processes by resource use |
| `kill chrome` | Terminate a process by name |
| `create folder Reports` | Create a folder on the Desktop |
| `search for resume.pdf` | Search Desktop, Documents, Downloads |
| `open downloads` | Open the Downloads folder |
| `open settings` | Open Windows Settings |
| `set timer for 5 minutes` | Countdown timer with alert |
| `remind me in 10 minutes to call mom` | Timed reminder |
| `calculate 2^10 + 5` | Safe math evaluation |
| `what is in my clipboard` | Read clipboard contents |
| `copy Hello World` | Write text to clipboard |
| `type Hello World` | Type text into the focused window |
| `my ip` / `wifi info` | Network information |
| `weather in Mumbai` | Live weather forecast |
| `wikipedia Python` | Wikipedia summary |
| `play Blinding Lights` | Search and play on Spotify |
| `lock screen` | Lock the PC |
| `sleep` / `restart` | Power actions |
| `clear chat` | Reset AI conversation history |
| `exit` | Close the assistant |

## Dependencies

| Package | Purpose |
|---|---|
| `PyQt5` | GUI framework |
| `pyttsx3` | Text-to-speech |
| `SpeechRecognition` + `pyaudio` | Microphone voice input |
| `anthropic` | Claude AI fallback responses |
| `psutil` | CPU, RAM, disk, battery, process info |
| `pycaw` + `comtypes` | Windows volume control |
| `screen-brightness-control` | Screen brightness control |
| `pyperclip` | Clipboard read/write |
| `pyautogui` | Keyboard automation (type text) |
| `spotipy` | Spotify playback control |
| `wikipedia` | Wikipedia search |
| `requests` | Weather API and location |

## API Keys

| Service | Where to get it |
|---|---|
| OpenWeatherMap | [openweathermap.org/api](https://openweathermap.org/api) |
| Spotify | [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) |
| Anthropic (Claude) | [console.anthropic.com](https://console.anthropic.com) |

## License

MIT License — see [LICENSE](LICENSE) for details.

## Author

Made by **Aditya**
