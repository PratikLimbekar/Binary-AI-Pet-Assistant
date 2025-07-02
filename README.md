# 🦉 Binary — Your AI Owl Companion  
> A smart, voice-activated assistant that’s not just intelligent, but also wise.

Imagine a world where your desktop assistant doesn't just *respond* — it *understands*, learns, and speaks like a calm, poetic sage.  
Meet **Binary**, the owl-themed personal AI that combines **cutting-edge intelligence** with **gentle, grounded wisdom**.

---

## 🌟 Why Binary?

Unlike generic assistants, **Binary** is:
- 🔊 **Voice-triggered** (with a custom hotword!)
- 🧠 **Intent-aware** (understands *what* you want, not just *what* you say)
- 🧘 **Chill and charming** (responds like a wise owl mentor)
- 🎨 **Visual and dynamic** (can even generate AI images from imagination)

Whether you're taking notes, asking deep questions, controlling music, or just chatting — Binary feels like a real companion, not just a tool.

---

## ✨ What Can Binary Do?

### 🎤 Voice-First Assistant
- Just say **"Binary"** — and it wakes up.
- Uses **Porcupine hotword detection** + **Google STT** to listen and understand.
- Speaks responses aloud using TTS, with toggleable voice output.

### 💡 Natural Conversations (Powered by Gemini)
- Built-in Gemini 2.0 Flash for short, smart, poetic answers.
- Handles open-ended queries, trivia, questions, and more.

### 🧠 Smart Intent Recognition
- Classifies your input using **sentence-transformers**.
- Instantly detects what you want to do:
  - 🤖 Ask AI something
  - 📝 Create a note
  - 🎧 Control your media
  - 🔍 Wikipedia search
  - ⛅ Get the weather
  - 🖼️ Generate AI images
  - 📰 Fetch news
  - 📊 Get system stats
  - 📂 Launch apps

### 🖼️ Image Generation
- Describe anything, and Binary uses Gemini’s vision model to draw it.
- Opens the generated image instantly.

### 📖 Wikipedia + Web Info
- Gets precise 3-line summaries from Wikipedia.
- Handles disambiguation and unknowns gracefully.

### 🌦️ Real-Time Weather
- Uses OpenWeatherMap to fetch the latest weather by city.
- Simple, clear, and human-readable output.

### 🎵 Music & Media Controls
- Pause, resume, skip tracks, or go back — with your voice.
- Volume slider included in GUI.
- (Experimental YouTube Music support via Selenium in progress)

### 📊 System Monitoring
- Quickly get battery %, CPU, RAM, and disk stats.
- Useful for quick checks or scripting extensions.

### 💻 App Launcher
- Say “Open Chrome” or “Start VSCode” — Binary will do it for you.

---

## 🖥️ GUI Highlights

- 👁️‍🗨️ **Animated Eyes**: Watch Binary blink and stare as it listens.
- 🧪 **Tabbed Layout**: Chat tab, Music tab — expandable and collapsible UI.
- 📌 **Minimalist Always-On-Top**: Stays discreet when idle, expands on command.
- 📢 **TTS Toggle**: Turn voice responses on or off instantly.

---

## 🧩 Under the Hood

| Component | Tech |
|----------|------|
| Voice Recognition | `speech_recognition`, `Porcupine` |
| Intent Detection | `sentence-transformers` |
| AI Chat & Image | Google Gemini API |
| Weather | OpenWeatherMap API |
| UI | `Tkinter` |
| Music | `pygame` + system media controls |
| Notes & Logs | Custom note manager & logging |
| App Control | `os.system()` based launch map |

---
