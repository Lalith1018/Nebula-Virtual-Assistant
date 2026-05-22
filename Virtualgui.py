
# ─────────────────────────────────────────────────────────────────────────────
#  Nebula — Virtual Assistant  (PyQt5 UI) — v2.0 Full Laptop Assistant
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import ast
import re
import math
import random
import shutil
import socket
import subprocess
import threading
import webbrowser
import ctypes
from datetime import datetime

import requests
import wikipedia
import pyttsx3
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import psutil
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame,
    QDialog, QMessageBox, QSizePolicy, QCompleter, QScrollArea,
)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QStringListModel
from PyQt5.QtGui import QFont, QTextCursor, QColor

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    PYCAW_AVAILABLE = True
except Exception:
    PYCAW_AVAILABLE = False

try:
    import screen_brightness_control as sbc
    SBC_AVAILABLE = True
except ImportError:
    SBC_AVAILABLE = False

try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

# ── Config ────────────────────────────────────────────────────────────────────
WEATHER_API_KEY       = os.getenv('WEATHER_API_KEY', '')
DEFAULT_CITY          = 'Ludhiana'
MUSIC_DIR             = r'D:\Top 20 Kuldeep Manak'

SPOTIFY_CLIENT_ID     = os.getenv('SPOTIFY_CLIENT_ID', '')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '')
SPOTIFY_REDIRECT_URI  = 'http://127.0.0.1:8888/callback'

ANTHROPIC_API_KEY     = os.getenv('ANTHROPIC_API_KEY', '')

# ── Autocomplete commands ─────────────────────────────────────────────────────
COMMANDS = [
    'hello', 'hi', 'hey', 'howdy',
    'how are you',
    'who are you', 'what are you', 'your name',
    'who made you', 'who created you', 'who built you',
    'what can you do', 'capabilities',
    'thank you', 'thanks',
    'what time is it', "what's today's date", 'today',
    'good morning',
    'weather in ', f'weather in {DEFAULT_CITY}',
    'wikipedia ',
    # Apps
    'open google', 'open youtube', 'open chrome', 'open notepad',
    'open paint', 'open calculator', 'open cmd', 'open vlc', 'open wordpad',
    'open desktop', 'open downloads', 'open documents', 'open pictures',
    'open file explorer', 'open settings', 'open task manager', 'open spotify',
    # Music
    'play ', 'pause', 'resume', 'skip', 'next song', 'previous song',
    "what's playing", 'now playing', 'current song',
    # Volume
    'volume up', 'volume down', 'mute', 'unmute', 'set volume to ',
    'increase volume', 'decrease volume',
    # Brightness
    'brightness up', 'brightness down', 'set brightness to ',
    'increase brightness', 'decrease brightness',
    # System stats
    'system stats', 'cpu usage', 'ram usage', 'disk usage',
    'battery status', 'battery', 'memory usage', 'performance',
    # Process management
    'show running apps', 'list processes', 'kill ', 'terminate ', 'close ',
    'open task manager',
    # File operations
    'open file ', 'open folder ', 'create folder ', 'make folder ',
    'delete file ', 'delete folder ', 'search for ', 'find file ',
    # Clipboard
    'what is in my clipboard', 'copy ', 'paste clipboard',
    # Productivity
    'set timer for ', 'timer ', 'remind me ', 'reminder ',
    'calculate ', 'compute ', 'what is ',
    # Network
    'my ip', 'wifi info', 'network info', 'internet connection',
    # Power
    'lock screen', 'lock', 'sleep', 'restart', 'reboot', 'log off',
    # Misc
    'take a screenshot', 'where am i',
    'clear chat', 'clear history', 'new conversation',
    'type ', 'write ',
    'shutdown', 'exit', 'goodbye', 'bye', 'help', 'about you',
]

# ── Stylesheet — Retro Terminal ───────────────────────────────────────────────
QSS = """
QMainWindow, QWidget {
    background-color: #0c0c0c;
    color: #ccffcc;
    font-family: 'Consolas';
}
QTextEdit {
    background-color: #060606;
    color: #ccffcc;
    border: none;
    font-size: 10pt;
    font-family: 'Consolas';
    padding: 10px 12px;
    selection-background-color: #1a4a1a;
    selection-color: #00ff41;
}
QScrollBar:vertical {
    background: #060606;
    width: 6px;
    border-radius: 0;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #1a3a1a;
    min-height: 20px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical { height: 0; }
QLineEdit {
    background-color: #060606;
    color: #00ff41;
    border: 1px solid #1a3a1a;
    border-radius: 0;
    padding: 9px 14px;
    font-size: 11pt;
    font-family: 'Consolas';
    selection-background-color: #1a4a1a;
    selection-color: #00ff41;
}
QLineEdit:focus { border: 1px solid #00ff41; }
QPushButton#sendBtn {
    background-color: #001500;
    color: #00ff41;
    border: 1px solid #00aa33;
    border-radius: 0;
    padding: 9px 20px;
    font-size: 10pt;
    font-family: 'Consolas';
    font-weight: bold;
    letter-spacing: 1px;
}
QPushButton#sendBtn:hover   { background-color: #002800; border-color: #00ff41; }
QPushButton#sendBtn:pressed { background-color: #00ff41; color: #000000; }
QPushButton#micBtn {
    background-color: #0a0a0a;
    color: #99cc99;
    border: 1px solid #1a3a1a;
    border-radius: 0;
    padding: 9px 12px;
    font-size: 13pt;
}
QPushButton#micBtn:hover   { border-color: #00ff41; color: #00ff41; }
QPushButton#micListening {
    background-color: #1a0000;
    color: #ff4444;
    border: 1px solid #ff4444;
    border-radius: 0;
    padding: 9px 12px;
    font-size: 13pt;
    font-weight: bold;
}
QPushButton#headerBtn {
    background-color: transparent;
    color: #336633;
    border: 1px solid transparent;
    font-family: 'Consolas';
    font-size: 9pt;
    padding: 4px 10px;
    letter-spacing: 1px;
}
QPushButton#headerBtn:hover { color: #00ff41; border-color: #1a3a1a; }
QPushButton#toggleBtn {
    background-color: transparent;
    color: #336633;
    border: none;
    font-size: 14pt;
    padding: 4px 8px;
    font-family: 'Consolas';
}
QPushButton#toggleBtn:hover { color: #00ff41; }
QPushButton#quickBtn {
    background-color: #0a0a0a;
    color: #99cc99;
    border: 1px solid #1a2a1a;
    border-radius: 2px;
    padding: 6px 10px;
    font-size: 8pt;
    font-family: 'Consolas';
    text-align: left;
    min-height: 28px;
}
QPushButton#quickBtn:hover   { background-color: #0f1f0f; border-color: #336633; color: #ccffcc; }
QPushButton#quickBtn:pressed { background-color: #1a3a1a; color: #00ff41; border-color: #00ff41; }
QLabel#title {
    color: #00ff41;
    font-size: 14pt;
    font-weight: bold;
    font-family: 'Consolas';
    letter-spacing: 4px;
}
QLabel#subtitle { color: #336633; font-size: 8pt; font-family: 'Consolas'; letter-spacing: 2px; }
QLabel#dot      { color: #00ff41; font-size: 14pt; }
QLabel#status   { color: #336633; font-size: 9pt; font-family: 'Consolas'; padding: 2px 10px; }
QLabel#sidebarHdr { color: #336633; font-size: 7pt; font-family: 'Consolas'; letter-spacing: 2px; padding: 4px 8px; background: #0a0a0a; }
QLabel#secInfo    { color: #00aaff; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secMusic   { color: #00ff41; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secApps    { color: #ffaa00; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secSystem  { color: #ff5555; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secCtrl    { color: #cc88ff; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secStats   { color: #ffcc44; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QLabel#secPower   { color: #ff6644; font-size: 7pt; font-family: 'Consolas'; font-weight: bold; letter-spacing: 1px; padding: 8px 4px 3px 4px; }
QFrame#divider    { background-color: #1a3a1a; }
QFrame#sectionDiv { background-color: #141414; min-height: 1px; max-height: 1px; }
QFrame#sidebar {
    background-color: #080808;
    border-right: 1px solid #1a3a1a;
}
QFrame#typingBar {
    background-color: #060606;
    border-top: 1px solid #1a3a1a;
}
QScrollArea { background-color: #080808; border: none; }
QScrollBar:vertical {
    background: #080808;
    width: 4px;
    border-radius: 0;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #1a3a1a;
    min-height: 16px;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical { height: 0; }
QDialog { background-color: #0c0c0c; color: #ccffcc; font-family: 'Consolas'; }
QMessageBox { background-color: #0c0c0c; color: #ccffcc; font-family: 'Consolas'; }
QMessageBox QPushButton {
    background-color: #001500;
    color: #00ff41;
    border: 1px solid #00aa33;
    border-radius: 0;
    padding: 6px 16px;
    font-family: 'Consolas';
}
QMessageBox QPushButton:hover { background-color: #002800; border-color: #00ff41; }
"""
# ─────────────────────────────────────────────────────────────────────────────


# ── Voice worker ──────────────────────────────────────────────────────────────
class VoiceWorker(QThread):
    result = pyqtSignal(str)
    error  = pyqtSignal(str)

    def run(self):
        if not SR_AVAILABLE:
            self.error.emit(
                "SpeechRecognition is not installed.\n"
                "Run:  pip install SpeechRecognition pyaudio"
            )
            return
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.4)
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
            text = r.recognize_google(audio)
            self.result.emit(text)
        except sr.WaitTimeoutError:
            self.error.emit("No speech detected. Try again.")
        except sr.UnknownValueError:
            self.error.emit("Couldn't understand the audio. Try again.")
        except Exception as e:
            self.error.emit(f"Voice error: {e}")
# ─────────────────────────────────────────────────────────────────────────────


# ── AI worker (with multi-turn history) ──────────────────────────────────────
class AIWorker(QThread):
    result = pyqtSignal(str)
    error  = pyqtSignal(str)

    def __init__(self, query, history=None, parent=None):
        super().__init__(parent)
        self.query   = query
        self.history = history or []

    def run(self):
        try:
            import anthropic
            client   = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            messages = self.history + [{'role': 'user', 'content': self.query}]
            msg = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=500,
                system=(
                    'You are Nebula, a friendly virtual desktop assistant for Windows. '
                    'Reply in 1-3 concise sentences, plain text only, no markdown.'
                ),
                messages=messages,
            )
            self.result.emit(msg.content[0].text)
        except ImportError:
            self.error.emit('__no_anthropic__')
        except Exception as e:
            self.error.emit(f'AI error: {e}')
# ─────────────────────────────────────────────────────────────────────────────


# ── Typing indicator ──────────────────────────────────────────────────────────
class TypingIndicator(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('typingBar')
        self.setFixedHeight(26)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(5)

        lbl = QLabel('> NEBULA PROCESSING')
        lbl.setStyleSheet('color: #336633; font-size: 8pt; font-family: Consolas; background: transparent;')
        layout.addWidget(lbl)

        self.dots = []
        for _ in range(3):
            d = QLabel('█')
            d.setStyleSheet('color: #1a3a1a; font-size: 9pt; font-family: Consolas; background: transparent;')
            layout.addWidget(d)
            self.dots.append(d)

        layout.addStretch()

        self._step  = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self.hide()

    def _tick(self):
        for i, d in enumerate(self.dots):
            active = (i == self._step % 3)
            d.setStyleSheet(
                f'color: {"#00ff41" if active else "#1a3a1a"}; '
                'font-size: 9pt; font-family: Consolas; background: transparent;'
            )
        self._step += 1

    def start(self):
        self._step = 0
        self.show()
        self._timer.start(350)

    def stop(self):
        self._timer.stop()
        self.hide()
# ─────────────────────────────────────────────────────────────────────────────


class AboutDialog(QDialog):
    def __init__(self, parent, speak_fn):
        super().__init__(parent)
        self.setWindowTitle('About Nebula')
        self.setFixedSize(480, 320)
        self.setStyleSheet(QSS)

        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel('Nebula — Virtual Assistant v2.0')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('color: #a6e3a1; font-size: 14pt; font-weight: bold;')
        layout.addWidget(title)

        by = QLabel('by Aditya')
        by.setAlignment(Qt.AlignCenter)
        by.setStyleSheet('color: #6c7086; font-size: 10pt;')
        layout.addWidget(by)

        self.body = (
            'Nebula is a Python-powered virtual assistant built with PyQt5.\n'
            'She can control system volume and brightness, check battery and\n'
            'system stats, manage files and processes, set timers and reminders,\n'
            'control Spotify, check weather, search Wikipedia, and much more.\n\n'
            'Powered by Claude AI for natural conversation.'
        )
        body_lbl = QLabel(self.body)
        body_lbl.setAlignment(Qt.AlignCenter)
        body_lbl.setStyleSheet('color: #cdd6f4; font-size: 10pt;')
        body_lbl.setWordWrap(True)
        layout.addWidget(body_lbl)

        narrate_btn = QPushButton('▶  Narrate')
        narrate_btn.setStyleSheet(
            'background-color: #89b4fa; color: #11111b; border: none; '
            'border-radius: 6px; padding: 8px 18px; font-size: 10pt; font-weight: bold;'
        )
        narrate_btn.setCursor(Qt.PointingHandCursor)
        narrate_btn.clicked.connect(lambda: speak_fn(self.body))
        layout.addWidget(narrate_btn, alignment=Qt.AlignCenter)


class NebulaWindow(QMainWindow):

    # ── Response banks ────────────────────────────────────────────────────────
    greet    = ["Hey! What's up?", "Hello there!", "Hi, I'm Nebula — how can I help?", "Hello! Good to see you."]
    how      = ["I'm doing great, thanks!", "All systems running fine!", "Feeling fantastic — what about you?"]
    name     = ["You can call me Nebula.", "My name is Nebula.", "Nebula — your personal assistant!"]
    creator  = ["I was made by Aditya.", "Aditya built me with Python!", "Created by Aditya — one of his favourite projects."]
    can_do   = ["I can control volume, brightness, manage files, set timers, check system stats, control Spotify, and much more!",
                "Type 'help' for a full list of commands.", "Ask me anything — I've got a lot of tricks!"]
    confused = ["I didn't quite catch that.", "Could you rephrase that?", "Hmm, I'm not sure I understood."]
    thanks   = ["My pleasure!", "You're welcome!", "Happy to help!", "Anytime!"]
    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self):
        super().__init__()
        self._sidebar_visible = True
        self._voice_worker    = None
        self._ai_worker       = None
        self._chat_history    = []   # multi-turn AI memory
        self._timers          = {}   # id -> {'label': str, 'qtimer': QTimer}
        self._timer_id        = 0
        self._init_tts()
        self._init_spotify()
        self._build_ui()

        self.add_message('Nebula',
            "Hello! I'm Nebula v2.0, your full laptop assistant. "
            "I can control volume, brightness, manage files, set timers, check system stats, and much more. "
            "Type 'help' to see everything I can do.")

    # ── TTS ───────────────────────────────────────────────────────────────────
    def _init_tts(self):
        try:
            self.engine = pyttsx3.init('sapi5')
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[0].id)
            self.engine.setProperty('rate', 170)
            self.tts_ok = True
        except Exception:
            self.tts_ok = False

    def speak(self, text):
        if self.tts_ok:
            threading.Thread(target=self._tts_run, args=(text,), daemon=True).start()

    def _tts_run(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception:
            pass
    # ─────────────────────────────────────────────────────────────────────────

    # ── Spotify ───────────────────────────────────────────────────────────────
    def _init_spotify(self):
        if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
            self.sp = None
            return
        try:
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope='user-modify-playback-state user-read-playback-state user-read-currently-playing',
                open_browser=True,
                cache_path='.spotify_cache'
            ))
        except Exception:
            self.sp = None

    def _launch_spotify_app(self):
        paths = [
            r'C:\Users\{}\AppData\Roaming\Spotify\Spotify.exe'.format(os.getlogin()),
            r'C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.0.0.0_x86__zpdnekdrzrea0\Spotify.exe',
        ]
        for path in paths:
            try:
                os.startfile(path)
                return True
            except Exception:
                continue
        try:
            subprocess.Popen(['start', 'spotify:'], shell=True)
            return True
        except Exception:
            return False

    def _handle_spotify(self, ui, _retry=0):
        if not self.sp:
            self._respond(
                "Spotify isn't set up. Open Virtualgui.py, paste your "
                "Client ID and Secret at the top, then restart."
            )
            return
        try:
            if any(p in ui for p in ("what's playing", "now playing", "current song", "what song")):
                cur = self.sp.current_playback()
                if cur and cur.get('is_playing'):
                    self._respond(f"Now playing: {cur['item']['name']} by {cur['item']['artists'][0]['name']}.")
                else:
                    self._respond("Nothing is currently playing on Spotify.")
            elif 'pause' in ui:
                self.sp.pause_playback()
                self._respond("Music paused.")
            elif 'resume' in ui or 'unpause' in ui or 'continue' in ui:
                self.sp.start_playback()
                self._respond("Music resumed.")
            elif 'next' in ui or 'skip' in ui:
                self.sp.next_track()
                self._respond("Skipped to next track.")
            elif 'previous' in ui or ('back' in ui and 'song' in ui):
                self.sp.previous_track()
                self._respond("Going back to the previous track.")
            else:
                query = ui.replace('play', '').replace('on spotify', '').replace('spotify', '').replace('music', '').strip()
                if query:
                    results = self.sp.search(q=query, limit=1, type='track')
                    tracks  = results['tracks']['items']
                    if tracks:
                        self.sp.start_playback(uris=[tracks[0]['uri']])
                        self._respond(f"Playing {tracks[0]['name']} by {tracks[0]['artists'][0]['name']} on Spotify.")
                    else:
                        self._respond(f"Couldn't find '{query}' on Spotify.")
                else:
                    self.sp.start_playback()
                    self._respond("Resuming Spotify.")
        except spotipy.exceptions.SpotifyException as e:
            if 'No active device' in str(e):
                if _retry == 0:
                    launched = self._launch_spotify_app()
                    if launched:
                        self._respond("Spotify wasn't open — launching it. Retrying in 6 seconds…")
                        QTimer.singleShot(6000, lambda: self._handle_spotify(ui, _retry=1))
                    else:
                        self._respond("Couldn't launch Spotify automatically. Please open it manually.")
                elif _retry == 1:
                    self._respond("Still warming up… retrying in 4 more seconds.")
                    QTimer.singleShot(4000, lambda: self._handle_spotify(ui, _retry=2))
                else:
                    self._respond("Spotify is open but not ready. Click play on any track in Spotify first.")
            else:
                self._respond("Spotify error — make sure Spotify is open and try again.")
        except Exception:
            self._respond("Something went wrong with Spotify.")
    # ─────────────────────────────────────────────────────────────────────────

    # ── Chat helpers ──────────────────────────────────────────────────────────
    def add_message(self, sender, text):
        ts   = datetime.now().strftime('%H:%M:%S')
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', '<br>')

        if sender == 'You':
            html = (
                f'<div style="margin:2px 0 2px 0; font-family:Consolas; font-size:10pt; line-height:1.6;">'
                f'<span style="color:#1a4a1a;">[{ts}]</span>'
                f'<span style="color:#ffd700; font-weight:bold;"> YOU</span>'
                f'<span style="color:#1a4a1a;"> ──▶ </span>'
                f'<span style="color:#e8e8c8;">{text}</span>'
                f'</div>'
            )
        else:
            html = (
                f'<div style="margin:2px 0 6px 0; font-family:Consolas; font-size:10pt; line-height:1.6;">'
                f'<span style="color:#1a4a1a;">[{ts}]</span>'
                f'<span style="color:#00ff41; font-weight:bold;"> NEBULA</span>'
                f'<span style="color:#1a4a1a;"> ──▶ </span>'
                f'<span style="color:#ccffcc;">{text}</span>'
                f'</div>'
            )

        cursor = self.chat.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertHtml(html)
        self.chat.setTextCursor(cursor)
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())
        self.input_field.setFocus()

    def set_status(self, text='Ready'):
        self.status_label.setText(f'  {text}')

    def _respond(self, text):
        self.typing_indicator.stop()
        self.add_message('Nebula', text)
        self.set_status()
        self.speak(text)
    # ─────────────────────────────────────────────────────────────────────────

    # ── Send ──────────────────────────────────────────────────────────────────
    def send_func(self):
        raw = self.input_field.text().strip()
        if not raw:
            return
        self.input_field.clear()
        self.input_field.setFocus()
        self.add_message('You', raw)
        self.set_status('Nebula is thinking…')
        self.typing_indicator.start()
        QTimer.singleShot(50, lambda: self._process(raw.lower()))
    # ─────────────────────────────────────────────────────────────────────────

    # ── Voice input ───────────────────────────────────────────────────────────
    def _start_voice(self):
        if self._voice_worker and self._voice_worker.isRunning():
            return
        self.mic_btn.setObjectName('micListening')
        self.mic_btn.setStyleSheet(
            'background-color: #f38ba8; color: #11111b; border: none; '
            'border-radius: 6px; padding: 10px 12px; font-size: 14pt; font-weight: bold;'
        )
        self.mic_btn.setText('🔴')
        self.set_status('Listening…')

        self._voice_worker = VoiceWorker()
        self._voice_worker.result.connect(self._on_voice_result)
        self._voice_worker.error.connect(self._on_voice_error)
        self._voice_worker.start()

    def _reset_mic_btn(self):
        self.mic_btn.setObjectName('micBtn')
        self.mic_btn.setStyleSheet('')
        self.mic_btn.setText('🎤')
        self.mic_btn.setObjectName('micBtn')
        self.mic_btn.style().unpolish(self.mic_btn)
        self.mic_btn.style().polish(self.mic_btn)

    def _on_voice_result(self, text):
        self._reset_mic_btn()
        self.set_status('Ready')
        self.input_field.setText(text)
        self.send_func()

    def _on_voice_error(self, msg):
        self._reset_mic_btn()
        self._respond(msg)
    # ─────────────────────────────────────────────────────────────────────────

    # ── Sidebar toggle ────────────────────────────────────────────────────────
    def _toggle_sidebar(self):
        self._sidebar_visible = not self._sidebar_visible
        self.sidebar.setVisible(self._sidebar_visible)
        self.toggle_btn.setText('◀' if self._sidebar_visible else '▶')
    # ─────────────────────────────────────────────────────────────────────────

    # ── Quick command ─────────────────────────────────────────────────────────
    def _quick(self, cmd):
        self.add_message('You', cmd)
        self.set_status('Nebula is thinking…')
        self.typing_indicator.start()
        QTimer.singleShot(50, lambda: self._process(cmd.lower()))
    # ─────────────────────────────────────────────────────────────────────────

    # ═════════════════════════════════════════════════════════════════════════
    #  NEW FEATURE HANDLERS
    # ═════════════════════════════════════════════════════════════════════════

    # ── Volume ────────────────────────────────────────────────────────────────
    def _handle_volume(self, ui):
        if not PYCAW_AVAILABLE:
            self._respond("Volume control requires pycaw. Run: pip install pycaw comtypes")
            return
        try:
            devices   = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            vc        = cast(interface, POINTER(IAudioEndpointVolume))
            current   = round(vc.GetMasterVolumeLevelScalar() * 100)

            if 'unmute' in ui:
                vc.SetMute(0, None)
                self._respond(f"Unmuted. Volume is at {current}%.")
            elif 'mute' in ui:
                vc.SetMute(1, None)
                self._respond("Muted.")
            else:
                num = re.search(r'(\d+)', ui)
                step = int(num.group(1)) if num else 10

                if any(w in ui for w in ('up', 'increase', 'louder', 'raise', 'higher')):
                    new = min(100, current + step)
                    vc.SetMasterVolumeLevelScalar(new / 100, None)
                    self._respond(f"Volume increased to {new}%.")
                elif any(w in ui for w in ('down', 'decrease', 'lower', 'quieter', 'reduce', 'quiet')):
                    new = max(0, current - step)
                    vc.SetMasterVolumeLevelScalar(new / 100, None)
                    self._respond(f"Volume decreased to {new}%.")
                elif ('set' in ui or 'to' in ui) and num:
                    new = max(0, min(100, step))
                    vc.SetMasterVolumeLevelScalar(new / 100, None)
                    self._respond(f"Volume set to {new}%.")
                else:
                    self._respond(f"Current volume is {current}%.")
        except Exception as e:
            self._respond(f"Volume error: {e}")

    # ── Brightness ────────────────────────────────────────────────────────────
    def _handle_brightness(self, ui):
        if not SBC_AVAILABLE:
            self._respond("Brightness control requires screen-brightness-control. Run: pip install screen-brightness-control")
            return
        try:
            current = sbc.get_brightness(display=0)
            if isinstance(current, list):
                current = current[0]

            num  = re.search(r'(\d+)', ui)
            step = int(num.group(1)) if num else 10

            if any(w in ui for w in ('up', 'increase', 'brighter', 'raise', 'higher')):
                new = min(100, current + step)
                sbc.set_brightness(new, display=0)
                self._respond(f"Brightness increased to {new}%.")
            elif any(w in ui for w in ('down', 'decrease', 'dim', 'lower', 'reduce', 'darker')):
                new = max(10, current - step)
                sbc.set_brightness(new, display=0)
                self._respond(f"Brightness decreased to {new}%.")
            elif ('set' in ui or 'to' in ui) and num:
                new = max(10, min(100, step))
                sbc.set_brightness(new, display=0)
                self._respond(f"Brightness set to {new}%.")
            else:
                self._respond(f"Current brightness is {current}%.")
        except Exception as e:
            self._respond(f"Brightness error: {e}")

    # ── System stats ──────────────────────────────────────────────────────────
    def _handle_system_stats(self, ui):
        try:
            if 'battery' in ui:
                bat = psutil.sensors_battery()
                if bat:
                    plug  = 'Charging' if bat.power_plugged else 'Discharging'
                    extra = ''
                    if bat.secsleft > 0 and not bat.power_plugged:
                        h, m = divmod(bat.secsleft // 60, 60)
                        extra = f" (~{h}h {m}m remaining)"
                    self._respond(f"Battery: {round(bat.percent)}% — {plug}{extra}.")
                else:
                    self._respond("Battery info unavailable (desktop PC?).")

            elif 'cpu' in ui:
                pct   = psutil.cpu_percent(interval=1)
                cores = psutil.cpu_count(logical=False)
                freq  = psutil.cpu_freq()
                ghz   = f" @ {freq.current / 1000:.1f} GHz" if freq else ''
                self._respond(f"CPU: {pct}% usage, {cores} cores{ghz}.")

            elif any(w in ui for w in ('ram', 'memory')):
                vm   = psutil.virtual_memory()
                used = vm.used  // (1024 ** 3)
                tot  = vm.total // (1024 ** 3)
                self._respond(f"RAM: {used} GB used of {tot} GB ({vm.percent}% full).")

            elif any(w in ui for w in ('disk', 'storage', 'drive')):
                disk = psutil.disk_usage('C:\\')
                used = disk.used  // (1024 ** 3)
                free = disk.free  // (1024 ** 3)
                tot  = disk.total // (1024 ** 3)
                self._respond(f"Disk C:\\: {used} GB used, {free} GB free of {tot} GB ({disk.percent}% full).")

            else:
                cpu  = psutil.cpu_percent(interval=0.5)
                vm   = psutil.virtual_memory()
                disk = psutil.disk_usage('C:\\')
                bat  = psutil.sensors_battery()
                lines = [
                    f"CPU:  {cpu}%",
                    f"RAM:  {vm.percent}%  ({vm.used // (1024**3)} GB / {vm.total // (1024**3)} GB)",
                    f"Disk: {disk.percent}%  ({disk.free // (1024**3)} GB free)",
                ]
                if bat:
                    icon = '⚡' if bat.power_plugged else '🔋'
                    lines.append(f"Bat:  {icon} {round(bat.percent)}%")
                self._respond('\n'.join(lines))

        except Exception as e:
            self._respond(f"Stats error: {e}")

    # ── Process management ────────────────────────────────────────────────────
    def _handle_process_mgmt(self, ui):
        try:
            if any(w in ui for w in ('task manager', 'taskmgr')):
                subprocess.Popen(['taskmgr.exe'])
                self._respond("Opening Task Manager.")
                return

            if any(w in ui for w in ('list', 'show', 'running', 'what apps', 'what programs', 'what processes')):
                procs = []
                for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
                    try:
                        if p.info['name']:
                            procs.append(p.info)
                    except Exception:
                        pass
                procs.sort(key=lambda x: (x['cpu_percent'] or 0) + (x['memory_percent'] or 0), reverse=True)
                top = procs[:8]
                lines = ['Top running processes:']
                for p in top:
                    lines.append(f"  • {p['name']}  CPU:{p['cpu_percent']:.1f}%  MEM:{p['memory_percent']:.1f}%")
                self._respond('\n'.join(lines))
                return

            # Kill / close / terminate
            target = ui
            for w in ('kill', 'terminate', 'close', 'stop', 'end', 'the', 'process',
                      'application', 'program', 'app', 'task'):
                target = target.replace(w, ' ').strip()
            target = ' '.join(target.split()).strip()

            if not target:
                self._respond("Which process should I kill? (e.g. 'kill chrome')")
                return

            killed = []
            for proc in psutil.process_iter(['name', 'pid']):
                try:
                    if target.lower() in proc.info['name'].lower():
                        proc.kill()
                        killed.append(proc.info['name'])
                except Exception:
                    pass

            if killed:
                self._respond(f"Terminated: {', '.join(set(killed))}.")
            else:
                self._respond(f"No running process found matching '{target}'.")

        except Exception as e:
            self._respond(f"Process error: {e}")

    # ── File operations ───────────────────────────────────────────────────────
    def _handle_file_ops(self, ui):
        try:
            # Create folder
            if any(p in ui for p in ('create folder', 'make folder', 'new folder', 'mkdir',
                                     'create a folder', 'make a folder')):
                name = ui
                for w in ('create a folder called', 'make a folder called', 'create folder',
                          'make folder', 'new folder', 'mkdir', 'named', 'called'):
                    name = name.replace(w, ' ').strip()
                name = ' '.join(name.split()).strip('"\'').strip()
                if not name:
                    self._respond("What should I name the new folder?")
                    return
                if not os.path.isabs(name):
                    path = os.path.join(os.path.expanduser('~'), 'Desktop', name)
                else:
                    path = name
                os.makedirs(path, exist_ok=True)
                self._respond(f"Folder created: {path}")

            # Delete file/folder
            elif any(p in ui for p in ('delete file', 'delete folder', 'remove file', 'remove folder',
                                       'delete the', 'remove the')):
                target = ui
                for w in ('delete file', 'delete folder', 'remove file', 'remove folder',
                          'delete the', 'remove the', 'delete', 'remove'):
                    target = target.replace(w, ' ').strip()
                target = ' '.join(target.split()).strip('"\'').strip()
                if not target:
                    self._respond("Which file or folder should I delete?")
                    return
                if not os.path.exists(target):
                    self._respond(f"Not found: {target}")
                    return
                reply = QMessageBox.question(self, 'Confirm Delete',
                    f'Permanently delete:\n{target}?', QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    if os.path.isfile(target):
                        os.remove(target)
                    else:
                        shutil.rmtree(target)
                    self._respond(f"Deleted: {target}")
                else:
                    self._respond("Deletion cancelled.")

            # Search for file
            elif any(p in ui for p in ('search for', 'find file', 'find folder', 'search file',
                                       'look for file', 'locate')):
                query = ui
                for w in ('search for a file called', 'search for a folder called', 'search for',
                          'find file', 'find folder', 'search file', 'look for file', 'locate',
                          'find', 'called', 'named'):
                    query = query.replace(w, ' ').strip()
                query = ' '.join(query.split()).strip('"\'').strip()
                if not query:
                    self._respond("What should I search for?")
                    return

                search_dirs = [
                    os.path.expanduser('~\\Desktop'),
                    os.path.expanduser('~\\Documents'),
                    os.path.expanduser('~\\Downloads'),
                    os.path.expanduser('~\\Pictures'),
                    os.path.expanduser('~\\Music'),
                ]
                results = []
                for base in search_dirs:
                    if not os.path.exists(base):
                        continue
                    for root, dirs, files in os.walk(base):
                        for f in files + dirs:
                            if query.lower() in f.lower():
                                results.append(os.path.join(root, f))
                        if len(results) >= 6:
                            break
                    if len(results) >= 6:
                        break

                if results:
                    lines = [f"Found {len(results)} result(s):"] + [f"  • {r}" for r in results[:6]]
                    self._respond('\n'.join(lines))
                else:
                    self._respond(f"No files found matching '{query}' in common folders.")

            # Open file/folder by path
            elif any(p in ui for p in ('open file', 'open folder', 'open path')):
                target = ui
                for w in ('open file', 'open folder', 'open path', 'open the file', 'open the folder'):
                    target = target.replace(w, ' ').strip()
                target = ' '.join(target.split()).strip('"\'').strip()
                if not target:
                    self._respond("Which file or folder should I open?")
                    return
                if os.path.exists(target):
                    os.startfile(target)
                    self._respond(f"Opened: {target}")
                else:
                    self._respond(f"Path not found: {target}")

            else:
                self._respond(
                    "File commands:\n"
                    "• create folder [name]\n"
                    "• search for [filename]\n"
                    "• open file [path]\n"
                    "• delete file [path]"
                )

        except PermissionError:
            self._respond("Permission denied. Try running as administrator.")
        except Exception as e:
            self._respond(f"File error: {e}")

    # ── Clipboard ─────────────────────────────────────────────────────────────
    def _handle_clipboard(self, ui):
        if not PYPERCLIP_AVAILABLE:
            self._respond("Clipboard requires pyperclip. Run: pip install pyperclip")
            return
        try:
            if any(p in ui for p in ("what's in", 'what is in', 'show clipboard', 'read clipboard', 'paste')):
                content = pyperclip.paste()
                if content:
                    preview = content[:300]
                    suffix  = '…' if len(content) > 300 else ''
                    self._respond(f"Clipboard: {preview}{suffix}")
                else:
                    self._respond("The clipboard is empty.")
            elif ui.startswith('copy '):
                text = ui[5:].strip().strip('"\'')
                if text:
                    pyperclip.copy(text)
                    self._respond(f"Copied to clipboard.")
                else:
                    self._respond("What should I copy?")
            else:
                content = pyperclip.paste()
                self._respond(f"Clipboard: {content[:200]}" if content else "The clipboard is empty.")
        except Exception as e:
            self._respond(f"Clipboard error: {e}")

    # ── Timer ─────────────────────────────────────────────────────────────────
    def _handle_timer(self, ui):
        m = re.search(r'(\d+)\s*min', ui)
        s = re.search(r'(\d+)\s*sec', ui)
        minutes = int(m.group(1)) if m else 0
        seconds = int(s.group(1)) if s else 0
        total   = minutes * 60 + seconds

        if total == 0:
            # Check if asking about active timers
            if self._timers:
                lines = [f"Active timers ({len(self._timers)}):"]
                for tid, t in self._timers.items():
                    remaining = t['qtimer'].remainingTime() // 1000
                    h, rem = divmod(remaining, 3600)
                    mn, sc = divmod(rem, 60)
                    ts = f"{h}h {mn}m {sc}s" if h else (f"{mn}m {sc}s" if mn else f"{sc}s")
                    lines.append(f"  • {t['label']} — {ts} left")
                self._respond('\n'.join(lines))
            else:
                self._respond("No active timers. Try: 'set timer for 5 minutes'")
            return

        self._timer_id += 1
        tid   = self._timer_id
        label = f"Timer #{tid}"

        qt = QTimer(self)
        qt.setSingleShot(True)
        qt.timeout.connect(lambda: self._timer_done(tid, label))
        qt.start(total * 1000)
        self._timers[tid] = {'label': label, 'qtimer': qt}

        parts = []
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds:
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        self._respond(f"Timer set for {' '.join(parts)}.")

    def _timer_done(self, tid, label):
        self.add_message('Nebula', f"⏰ {label} is done!")
        self.speak(f"{label} done!")
        self._timers.pop(tid, None)

    # ── Reminder ──────────────────────────────────────────────────────────────
    def _handle_reminder(self, ui):
        m = re.search(r'(\d+)\s*min', ui)
        s = re.search(r'(\d+)\s*sec', ui)
        minutes = int(m.group(1)) if m else 0
        seconds = int(s.group(1)) if s else 0
        total   = minutes * 60 + seconds

        # Extract task text
        task = ''
        for pattern in [
            r'remind me (?:in .+? )?to (.+)',
            r'remind me to (.+?) in \d',
            r'reminder.*?to (.+)',
        ]:
            match = re.search(pattern, ui)
            if match:
                task = match.group(1).strip()
                task = re.sub(r'\s+in\s+\d+\s+\w+$', '', task).strip()
                break

        if total == 0:
            self._respond("When should I remind you? (e.g. 'remind me in 10 minutes to call mom')")
            return

        task_str = task if task else 'your reminder'
        self._timer_id += 1
        tid = self._timer_id

        qt = QTimer(self)
        qt.setSingleShot(True)
        qt.timeout.connect(lambda: self._reminder_done(tid, task_str))
        qt.start(total * 1000)
        self._timers[tid] = {'label': task_str, 'qtimer': qt}

        parts = []
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
        if seconds:
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
        self._respond(f"I'll remind you to '{task_str}' in {' '.join(parts)}.")

    def _reminder_done(self, tid, task):
        self.add_message('Nebula', f"⏰ Reminder: {task}")
        self.speak(f"Reminder: {task}")
        self._timers.pop(tid, None)

    # ── Calculator ────────────────────────────────────────────────────────────
    def _handle_calculator(self, ui):
        expr = ui
        for w in ('calculate', 'compute', 'what is', "what's", 'evaluate', 'solve',
                  'math', 'equals', '?'):
            expr = expr.replace(w, ' ')
        expr = expr.strip().replace('^', '**')
        expr = re.sub(r'(\d)\s*x\s*(\d)', r'\1*\2', expr)  # "3 x 4" -> "3*4"
        expr = ' '.join(expr.split())

        if not expr:
            self._respond("What should I calculate? (e.g. 'calculate 25 * 4')")
            return

        try:
            tree = ast.parse(expr, mode='eval')
            _safe = {ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
                     ast.FloorDiv, ast.USub, ast.UAdd}
            for node in ast.walk(tree):
                if type(node) not in _safe:
                    raise ValueError("unsafe")
            result = eval(compile(tree, '<string>', 'eval'))
            if isinstance(result, float) and result == int(result):
                result = int(result)
            self._respond(f"{expr} = {result}")
        except ZeroDivisionError:
            self._respond("Division by zero is undefined.")
        except Exception:
            self._respond(f"Couldn't calculate '{expr}'. Try: 'calculate 25 * 4 + 10'")

    # ── Network info ──────────────────────────────────────────────────────────
    def _handle_network(self, ui):
        try:
            hostname = socket.gethostname()
            ip       = socket.gethostbyname(hostname)

            if any(w in ui for w in ('ip', 'address', 'my ip', 'ip address')):
                self._respond(f"Local IP: {ip}  |  Hostname: {hostname}")
                return

            # WiFi SSID and signal
            try:
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'interfaces'],
                    capture_output=True, text=True, timeout=5
                )
                ssid_m   = re.search(r'^\s*SSID\s*:\s*(.+)$',   result.stdout, re.M)
                signal_m = re.search(r'Signal\s*:\s*(\d+)%',    result.stdout)
                speed_m  = re.search(r'Receive rate.*?:\s*([\d.]+)', result.stdout)

                lines = [f"IP: {ip}", f"Hostname: {hostname}"]
                if ssid_m:
                    lines.append(f"WiFi: {ssid_m.group(1).strip()}")
                if signal_m:
                    lines.append(f"Signal: {signal_m.group(1)}%")
                if speed_m:
                    lines.append(f"Rx speed: {speed_m.group(1)} Mbps")
                self._respond('\n'.join(lines))
            except Exception:
                self._respond(f"IP: {ip}  |  Hostname: {hostname}")

        except Exception as e:
            self._respond(f"Network error: {e}")

    # ── Power / system actions ────────────────────────────────────────────────
    def _handle_power(self, ui):
        if 'lock' in ui:
            self._respond("Locking the screen.")
            ctypes.windll.user32.LockWorkStation()

        elif any(w in ui for w in ('sleep', 'hibernate', 'suspend')):
            reply = QMessageBox.question(self, 'Confirm Sleep',
                'Put the system to sleep?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._respond("Going to sleep. Goodnight!")
                QTimer.singleShot(1500, lambda: subprocess.run(
                    ['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0']
                ))
            else:
                self._respond("Sleep cancelled.")

        elif any(w in ui for w in ('restart', 'reboot')):
            reply = QMessageBox.question(self, 'Confirm Restart',
                'Restart the system?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._respond("Restarting. See you on the other side!")
                os.system('shutdown -r -t 5')
            else:
                self._respond("Restart cancelled.")

        elif any(w in ui for w in ('log off', 'logoff', 'sign out')):
            reply = QMessageBox.question(self, 'Confirm Sign Out',
                'Sign out of Windows?', QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._respond("Signing out…")
                subprocess.run(['logoff'])
            else:
                self._respond("Sign-out cancelled.")

    # ── Type text ─────────────────────────────────────────────────────────────
    def _handle_type_text(self, ui):
        if not PYAUTOGUI_AVAILABLE:
            self._respond("Typing requires pyautogui. Run: pip install pyautogui")
            return
        text = ui
        for prefix in ('type out ', 'type in ', 'type ', 'write out ', 'write '):
            if ui.startswith(prefix):
                text = ui[len(prefix):].strip().strip('"\'')
                break
        if not text:
            self._respond("What should I type?")
            return
        self._respond("Typing in 2 seconds — click your target window!")
        QTimer.singleShot(2000, lambda: pyautogui.typewrite(text, interval=0.04))

    # ═════════════════════════════════════════════════════════════════════════
    #  INTENT DISPATCHER
    # ═════════════════════════════════════════════════════════════════════════

    def _process(self, ui):

        # ── Meta ──────────────────────────────────────────────────────────────
        if ui in ('help', 'commands', 'what can you do'):
            self._respond(
                'NEBULA v2.0 — Full Laptop Assistant\n'
                '\n'
                'INFO & WEB\n'
                '  what time is it / what\'s today\'s date / good morning\n'
                '  weather in [city]  |  wikipedia [topic]  |  where am i\n'
                '\n'
                'SYSTEM CONTROLS\n'
                '  volume up/down/mute/unmute / set volume to 70\n'
                '  brightness up/down / set brightness to 50\n'
                '  battery / cpu usage / ram usage / disk usage / system stats\n'
                '\n'
                'FILES\n'
                '  create folder [name]  |  search for [filename]\n'
                '  open file [path]      |  delete file [path]\n'
                '\n'
                'APPS & PROCESSES\n'
                '  open chrome/notepad/vlc/calculator/cmd/spotify/settings…\n'
                '  open desktop/downloads/documents/file explorer\n'
                '  show running apps  |  kill [process name]\n'
                '\n'
                'PRODUCTIVITY\n'
                '  set timer for 5 minutes  |  remind me in 10 minutes to [task]\n'
                '  calculate [expression]   |  type [text]\n'
                '  what is in my clipboard  |  copy [text]\n'
                '\n'
                'MUSIC (Spotify)\n'
                '  play [song]  |  pause / resume / skip / previous song\n'
                '  what\'s playing\n'
                '\n'
                'POWER\n'
                '  lock screen  |  sleep  |  restart  |  shutdown  |  log off\n'
                '\n'
                'OTHER\n'
                '  take a screenshot  |  network info  |  my ip\n'
                '  clear chat  |  about you  |  exit'
            )

        elif 'about' in ui and 'you' in ui:
            self._respond('Let me introduce myself.')
            AboutDialog(self, self.speak).exec_()

        # ── Greetings / small talk ─────────────────────────────────────────────
        elif any(w in ui for w in ('hello', 'hi', 'hey', 'howdy')):
            self._respond(random.choice(self.greet))

        elif 'how are you' in ui:
            self._respond(random.choice(self.how))

        elif 'who are you' in ui or 'your name' in ui or 'what are you' in ui:
            self._respond(random.choice(self.name))

        elif 'who made you' in ui or 'who created you' in ui or 'who built you' in ui:
            self._respond(random.choice(self.creator))

        elif 'what can you do' in ui or 'capabilities' in ui:
            self._respond(random.choice(self.can_do))

        elif 'thank' in ui:
            self._respond(random.choice(self.thanks))

        elif 'who am i' in ui or 'my name' in ui:
            self._respond("You told me your name is Aditya!")

        elif 'friend' in ui:
            self._respond(random.choice(["I'd love to be your friend!", "Of course, friends it is!"]))

        elif 'bored' in ui:
            self._respond("Shall I play something on Spotify or open YouTube?")

        # ── Date / Time ────────────────────────────────────────────────────────
        elif 'time' in ui and 'timer' not in ui:
            self._respond(f"The current time is {datetime.now().strftime('%I:%M %p')}.")

        elif 'date' in ui or ui.strip() == 'today':
            self._respond(f"Today is {datetime.now().strftime('%A, %B %d %Y')}.")

        elif 'good morning' in ui:
            t = datetime.now().strftime('%I:%M %p')
            self._respond(f"Good morning, Aditya! It's {t}. {self._fetch_weather(DEFAULT_CITY)} Have a great day!")

        # ── Weather ────────────────────────────────────────────────────────────
        elif 'weather' in ui:
            city = DEFAULT_CITY
            if ' in ' in ui:
                city = ui.split(' in ', 1)[-1].strip().title()
            self._respond(self._fetch_weather(city))

        # ── Location ───────────────────────────────────────────────────────────
        elif 'location' in ui or ('where' in ui and 'am i' in ui):
            try:
                d = requests.get('https://ipinfo.io/json', timeout=6).json()
                self._respond(f"Your approximate location is {d.get('city','?')}, {d.get('region','?')}.")
            except Exception:
                self._respond("I was unable to determine your location right now.")

        # ── Wikipedia ──────────────────────────────────────────────────────────
        elif 'wikipedia' in ui:
            query = ui.replace('wikipedia', '').strip()
            if not query:
                self._respond("What would you like me to look up on Wikipedia?")
            else:
                try:
                    self._respond('According to Wikipedia: ' + wikipedia.summary(query, sentences=2))
                except wikipedia.exceptions.DisambiguationError as e:
                    self._respond(f"That's ambiguous. Did you mean: {', '.join(e.options[:4])}?")
                except Exception:
                    self._respond(f"Sorry, I couldn't find '{query}' on Wikipedia.")

        # ── Volume ─────────────────────────────────────────────────────────────
        elif any(w in ui for w in ('volume', 'mute', 'unmute')) and \
             not any(w in ui for w in ('play', 'song', 'music', 'spotify')):
            self._handle_volume(ui)

        # ── Brightness ─────────────────────────────────────────────────────────
        elif any(w in ui for w in ('brightness', 'brighten', 'dim screen')):
            self._handle_brightness(ui)

        # ── System stats ───────────────────────────────────────────────────────
        elif any(w in ui for w in ('battery', 'cpu', 'ram', 'memory usage', 'disk usage',
                                   'storage', 'system stats', 'performance', 'system info')):
            self._handle_system_stats(ui)

        # ── Process management ─────────────────────────────────────────────────
        elif any(w in ui for w in ('running apps', 'running processes', 'running programs',
                                   'list processes', 'show processes', 'what apps',
                                   'what programs', 'task manager')) or \
             any(w in ui for w in ('kill ', 'terminate ')) or \
             ('close ' in ui and ui != 'close') or \
             ('stop ' in ui and len(ui.split()) > 1):
            self._handle_process_mgmt(ui)

        # ── File operations (before generic 'open') ────────────────────────────
        elif any(p in ui for p in ('open file', 'open folder', 'open path',
                                   'create folder', 'make folder', 'new folder',
                                   'delete file', 'delete folder', 'remove file',
                                   'search for', 'find file', 'find folder',
                                   'locate file', 'search file')):
            self._handle_file_ops(ui)

        # ── Open apps / folders ────────────────────────────────────────────────
        elif 'open' in ui:
            self._handle_open(ui)

        # ── Spotify / music ────────────────────────────────────────────────────
        elif any(w in ui for w in ('play', 'pause', 'resume', 'skip', 'next song',
                                   'previous song', "what's playing", 'now playing',
                                   'current song', 'spotify', 'music')):
            self._handle_spotify(ui)

        # ── Screenshot ─────────────────────────────────────────────────────────
        elif 'screenshot' in ui or 'snip' in ui:
            self._respond('Opening Snipping Tool.')
            try:
                subprocess.Popen(['explorer.exe', 'ms-screenclip:'])
            except Exception:
                os.system('start ms-screenclip:')

        # ── Clipboard ──────────────────────────────────────────────────────────
        elif any(w in ui for w in ('clipboard', "what's copied", "what is copied")) or \
             (ui.startswith('copy ') and len(ui) > 5):
            self._handle_clipboard(ui)

        # ── Timer ──────────────────────────────────────────────────────────────
        elif 'timer' in ui or \
             ('set' in ui and any(w in ui for w in ('minute', 'second', 'hour'))):
            self._handle_timer(ui)

        # ── Reminder ───────────────────────────────────────────────────────────
        elif 'remind' in ui or 'reminder' in ui:
            self._handle_reminder(ui)

        # ── Calculator ─────────────────────────────────────────────────────────
        elif any(w in ui for w in ('calculate', 'compute', 'solve')) or \
             (any(w in ui for w in ('what is', "what's")) and
              re.search(r'\d.*[+\-*/^%]|[+\-*/^%].*\d', ui)):
            self._handle_calculator(ui)

        # ── Network info ────────────────────────────────────────────────────────
        elif any(w in ui for w in ('wifi', 'network info', 'internet', 'my ip',
                                   'ip address', 'connection')):
            self._handle_network(ui)

        # ── Power ──────────────────────────────────────────────────────────────
        elif any(w in ui for w in ('lock screen', 'lock pc', 'lock computer')) or \
             ui == 'lock' or \
             any(w in ui for w in ('sleep', 'hibernate', 'restart', 'reboot',
                                   'log off', 'logoff', 'sign out')):
            self._handle_power(ui)

        # ── Type text ──────────────────────────────────────────────────────────
        elif ui.startswith('type ') or ui.startswith('write '):
            self._handle_type_text(ui)

        # ── Clear chat history ─────────────────────────────────────────────────
        elif any(p in ui for p in ('clear chat', 'clear history', 'new conversation',
                                   'reset chat', 'forget conversation')):
            self._chat_history = []
            self._respond("Conversation history cleared. Starting fresh!")

        # ── Simple affirmations ─────────────────────────────────────────────────
        elif ui in ('fine', 'good', 'great', 'nice', 'okay', 'ok'):
            self._respond("Great to hear!")

        elif 'nebula' in ui:
            self._respond("That's me! How can I help?")

        # ── Shutdown ───────────────────────────────────────────────────────────
        elif 'shutdown' in ui or 'shut down' in ui:
            reply = QMessageBox.question(self, 'Confirm Shutdown',
                'Are you sure you want to shut down?',
                QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self._respond('Shutting down. Goodbye, Aditya!')
                os.system('shutdown -s -t 5')
            else:
                self._respond('Shutdown cancelled.')

        # ── Exit ───────────────────────────────────────────────────────────────
        elif ui in ('exit', 'quit', 'goodbye', 'bye', 'close', 'get lost') or \
             ui.startswith('goodbye') or ui.startswith('bye '):
            self._respond('Goodbye! Have a great day, Aditya!')
            QTimer.singleShot(1800, self.close)

        # ── Empty ──────────────────────────────────────────────────────────────
        elif not ui.strip():
            self.typing_indicator.stop()
            self.set_status()

        # ── AI fallback ────────────────────────────────────────────────────────
        else:
            self._handle_ai(ui)

    # ── Weather fetch ─────────────────────────────────────────────────────────
    def _fetch_weather(self, city):
        try:
            url = (f'http://api.openweathermap.org/data/2.5/weather'
                   f'?appid={WEATHER_API_KEY}&q={city}&units=metric')
            d     = requests.get(url, timeout=6).json()
            temp  = round(d['main']['temp'])
            feels = round(d['main']['feels_like'])
            desc  = d['weather'][0]['description'].capitalize()
            return f'In {city}: {temp}°C (feels like {feels}°C), {desc}.'
        except Exception:
            return 'Weather forecast is currently unavailable.'

    # ── Open apps / folders ───────────────────────────────────────────────────
    def _handle_open(self, ui):
        home = os.path.expanduser('~')
        apps = {
            'google':         ('Opening Google.',          lambda: webbrowser.open('https://www.google.com')),
            'youtube':        ('Opening YouTube.',         lambda: webbrowser.open('https://www.youtube.com')),
            'github':         ('Opening GitHub.',          lambda: webbrowser.open('https://www.github.com')),
            'gmail':          ('Opening Gmail.',           lambda: webbrowser.open('https://mail.google.com')),
            'maps':           ('Opening Google Maps.',     lambda: webbrowser.open('https://maps.google.com')),
            'paint':          ('Opening Paint.',           lambda: os.startfile(r'C:\Windows\System32\mspaint.exe')),
            'notepad':        ('Opening Notepad.',         lambda: os.startfile(r'C:\Windows\System32\notepad.exe')),
            'calculator':     ('Opening Calculator.',      lambda: os.startfile(r'C:\Windows\System32\calc.exe')),
            'wordpad':        ('Opening WordPad.',         lambda: os.startfile(r'C:\Program Files\Windows NT\Accessories\wordpad.exe')),
            'chrome':         ('Opening Chrome.',          lambda: os.startfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe')),
            'browser':        ('Opening Chrome.',          lambda: os.startfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe')),
            'vlc':            ('Opening VLC.',             lambda: os.startfile(r'C:\Program Files\VideoLAN\VLC\vlc.exe')),
            'command prompt': ('Opening Command Prompt.',  lambda: os.startfile(r'C:\Windows\System32\cmd.exe')),
            'cmd':            ('Opening Command Prompt.',  lambda: os.startfile(r'C:\Windows\System32\cmd.exe')),
            'powershell':     ('Opening PowerShell.',      lambda: subprocess.Popen(['powershell.exe'])),
            'task manager':   ('Opening Task Manager.',    lambda: subprocess.Popen(['taskmgr.exe'])),
            'settings':       ('Opening Windows Settings.',lambda: os.startfile('ms-settings:')),
            'control panel':  ('Opening Control Panel.',   lambda: subprocess.Popen(['control.exe'])),
            'file explorer':  ('Opening File Explorer.',   lambda: os.startfile('explorer.exe')),
            'explorer':       ('Opening File Explorer.',   lambda: os.startfile('explorer.exe')),
            'spotify':        ('Opening Spotify.',         self._launch_spotify_app),
            'desktop':        ('Opening Desktop.',         lambda: os.startfile(os.path.join(home, 'Desktop'))),
            'downloads':      ('Opening Downloads.',       lambda: os.startfile(os.path.join(home, 'Downloads'))),
            'documents':      ('Opening Documents.',       lambda: os.startfile(os.path.join(home, 'Documents'))),
            'pictures':       ('Opening Pictures.',        lambda: os.startfile(os.path.join(home, 'Pictures'))),
            'music folder':   ('Opening Music folder.',    lambda: os.startfile(os.path.join(home, 'Music'))),
            'videos':         ('Opening Videos.',          lambda: os.startfile(os.path.join(home, 'Videos'))),
        }
        for keyword in sorted(apps, key=len, reverse=True):
            if keyword in ui:
                msg, action = apps[keyword]
                self._respond(msg)
                try:
                    action()
                except Exception:
                    self._respond("Sorry, I couldn't open that.")
                return
        self._respond(random.choice(self.confused))

    # ── AI response ───────────────────────────────────────────────────────────
    def _handle_ai(self, ui):
        if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == 'sk-ant-...':
            self.typing_indicator.stop()
            self._show_google_fallback(ui)
            return
        if self._ai_worker and self._ai_worker.isRunning():
            return
        self.set_status('Asking AI…')
        self._ai_worker = AIWorker(ui, history=self._chat_history)
        self._ai_worker.result.connect(self._on_ai_result)
        self._ai_worker.error.connect(lambda err: self._on_ai_error(err, ui))
        self._ai_worker.start()

    def _on_ai_result(self, text):
        if self._ai_worker:
            self._chat_history.append({'role': 'user',      'content': self._ai_worker.query})
            self._chat_history.append({'role': 'assistant', 'content': text})
            if len(self._chat_history) > 20:
                self._chat_history = self._chat_history[-20:]
        self._respond(text)

    def _on_ai_error(self, err, ui):
        self.typing_indicator.stop()
        self.set_status()
        if err == '__no_anthropic__':
            self._show_google_fallback(ui)
        else:
            self._respond(err)

    def _show_google_fallback(self, ui):
        reply = QMessageBox.question(self, 'Google Search',
            f'Should I search Google for:\n"{ui}"?',
            QMessageBox.Yes | QMessageBox.No)
        self.set_status()
        if reply == QMessageBox.Yes:
            self._respond('Searching Google…')
            webbrowser.open('https://www.google.com/search?q=' + ui)
        else:
            self._respond("Alright, let me know if I can help with something else.")

    # ── Sidebar builder ───────────────────────────────────────────────────────
    def _build_sidebar(self):
        outer = QFrame()
        outer.setObjectName('sidebar')
        outer.setFixedWidth(160)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        title_bar = QWidget()
        title_bar.setStyleSheet('background-color: #0a0a0a;')
        title_bar.setFixedHeight(32)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(10, 0, 10, 0)
        lbl = QLabel('QUICK ACCESS')
        lbl.setObjectName('sidebarHdr')
        lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        tb_layout.addWidget(lbl)
        outer_layout.addWidget(title_bar)

        accent = QFrame()
        accent.setObjectName('divider')
        accent.setFixedHeight(1)
        outer_layout.addWidget(accent)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet('background-color: #080808; border: none;')

        container = QWidget()
        container.setStyleSheet('background-color: #080808;')
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 6, 8, 8)
        layout.setSpacing(2)

        def div():
            d = QFrame()
            d.setObjectName('sectionDiv')
            layout.addSpacing(4)
            layout.addWidget(d)
            layout.addSpacing(2)

        def sec(name, obj):
            lb = QLabel(name)
            lb.setObjectName(obj)
            layout.addWidget(lb)

        def btn(icon, text, cmd, tip=''):
            b = QPushButton(f'{icon}  {text}')
            b.setObjectName('quickBtn')
            b.setCursor(Qt.PointingHandCursor)
            if tip:
                b.setToolTip(tip)
            b.clicked.connect(lambda checked, c=cmd: self._quick(c))
            layout.addWidget(b)

        # INFO
        sec('▸  INFO', 'secInfo')
        btn('🕐', 'Time',       'what time is it')
        btn('📅', 'Date',       "what's today's date")
        btn('☁️', 'Weather',    f'weather in {DEFAULT_CITY}')
        btn('📍', 'Location',   'where am i')

        div()

        # CONTROLS
        sec('▸  CONTROLS', 'secCtrl')
        btn('🔊', 'Vol Up',     'volume up')
        btn('🔉', 'Vol Down',   'volume down')
        btn('🔇', 'Mute',       'mute')
        btn('☀️', 'Bright +',   'brightness up')
        btn('🌙', 'Bright -',   'brightness down')

        div()

        # STATS
        sec('▸  STATS', 'secStats')
        btn('🖥️', 'System',     'system stats')
        btn('🔋', 'Battery',    'battery status')
        btn('⚙️', 'CPU',        'cpu usage')
        btn('💾', 'RAM',        'ram usage')
        btn('💿', 'Disk',       'disk usage')

        div()

        # MUSIC
        sec('▸  MUSIC', 'secMusic')
        btn('🎵', 'Playing',    "what's playing")
        btn('▶', 'Resume',      'resume')
        btn('⏸', 'Pause',       'pause')
        btn('⏭', 'Skip',        'skip')
        btn('⏮', 'Previous',    'previous song')

        div()

        # APPS
        sec('▸  APPS', 'secApps')
        btn('🌐', 'Google',     'open google')
        btn('📺', 'YouTube',    'open youtube')
        btn('📝', 'Notepad',    'open notepad')
        btn('🧮', 'Calculator', 'open calculator')
        btn('💻', 'CMD',        'open cmd')
        btn('📁', 'Explorer',   'open file explorer')
        btn('⚙️', 'Settings',   'open settings')

        div()

        # POWER
        sec('▸  POWER', 'secPower')
        btn('🔒', 'Lock',       'lock screen')
        btn('💤', 'Sleep',      'sleep')
        btn('🔄', 'Restart',    'restart')
        btn('📸', 'Screenshot', 'take a screenshot')
        btn('❓', 'Help',       'help')
        btn('ℹ️', 'About',      'about you')

        layout.addStretch()
        scroll.setWidget(container)
        outer_layout.addWidget(scroll)
        return outer

    # ── UI layout ─────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.setWindowTitle('Nebula — Virtual Assistant v2.0')
        self.setMinimumSize(650, 700)
        self.resize(860, 760)
        self.setStyleSheet(QSS)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(68)
        header.setStyleSheet('background-color: #11111b;')
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(8, 0, 12, 0)

        self.toggle_btn = QPushButton('◀')
        self.toggle_btn.setObjectName('toggleBtn')
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setToolTip('Toggle sidebar')
        self.toggle_btn.clicked.connect(self._toggle_sidebar)
        h_layout.addWidget(self.toggle_btn)

        dot = QLabel('●')
        dot.setObjectName('dot')
        h_layout.addWidget(dot)

        title_col = QWidget()
        title_col.setStyleSheet('background: transparent;')
        tc = QVBoxLayout(title_col)
        tc.setContentsMargins(6, 0, 0, 0)
        tc.setSpacing(1)
        title = QLabel('NEBULA')
        title.setObjectName('title')
        sub   = QLabel('Full Laptop Assistant v2.0')
        sub.setObjectName('subtitle')
        tc.addWidget(title)
        tc.addWidget(sub)
        h_layout.addWidget(title_col)
        h_layout.addStretch()

        for label, slot in (('Help', self._show_help), ('About', self._show_about)):
            b = QPushButton(label)
            b.setObjectName('headerBtn')
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(slot)
            h_layout.addWidget(b)

        root.addWidget(header)

        accent = QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet('background-color: #a6e3a1;')
        root.addWidget(accent)

        # Content row
        content = QWidget()
        content.setStyleSheet('background: transparent;')
        c_layout = QHBoxLayout(content)
        c_layout.setContentsMargins(0, 0, 0, 0)
        c_layout.setSpacing(0)

        self.sidebar = self._build_sidebar()
        c_layout.addWidget(self.sidebar)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)
        self.chat.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        c_layout.addWidget(self.chat, stretch=1)

        root.addWidget(content, stretch=1)

        self.typing_indicator = TypingIndicator()
        root.addWidget(self.typing_indicator)

        self.status_label = QLabel('  Ready')
        self.status_label.setObjectName('status')
        self.status_label.setFixedHeight(22)
        self.status_label.setStyleSheet('background-color: #11111b; color: #6c7086; font-size: 9pt;')
        root.addWidget(self.status_label)

        # Input row
        input_wrap = QWidget()
        input_wrap.setStyleSheet('background-color: #1e1e2e;')
        i_layout = QHBoxLayout(input_wrap)
        i_layout.setContentsMargins(10, 8, 10, 12)
        i_layout.setSpacing(8)

        self.mic_btn = QPushButton('🎤')
        self.mic_btn.setObjectName('micBtn')
        self.mic_btn.setCursor(Qt.PointingHandCursor)
        self.mic_btn.setToolTip('Voice input')
        self.mic_btn.setFixedWidth(46)
        self.mic_btn.clicked.connect(self._start_voice)
        i_layout.addWidget(self.mic_btn)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('Type a command or press 🎤 to speak…')
        self.input_field.returnPressed.connect(self.send_func)

        completer = QCompleter(COMMANDS, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setFilterMode(Qt.MatchContains)
        completer.popup().setStyleSheet(
            'background-color: #2a2a40; color: #cdd6f4; '
            'border: 1px solid #45475a; border-radius: 4px; '
            'selection-background-color: #89b4fa; selection-color: #11111b; '
            'font-size: 10pt; padding: 2px;'
        )
        self.input_field.setCompleter(completer)
        i_layout.addWidget(self.input_field)

        send_btn = QPushButton('Send  ➤')
        send_btn.setObjectName('sendBtn')
        send_btn.setCursor(Qt.PointingHandCursor)
        send_btn.clicked.connect(self.send_func)
        i_layout.addWidget(send_btn)

        root.addWidget(input_wrap)
        self.input_field.setFocus()

    def _show_about(self):
        AboutDialog(self, self.speak).exec_()

    def _show_help(self):
        self._process('help')
    # ─────────────────────────────────────────────────────────────────────────


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(QSS)
    window = NebulaWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
