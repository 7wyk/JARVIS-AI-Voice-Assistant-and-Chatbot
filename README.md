# 🔊 Jarvis - AI-Powered Voice Assistant

> An intelligent desktop assistant built with Python, Gemini AI, and real-time voice command capabilities.

![Jarvis Voice Assistant](https://img.shields.io/badge/Powered%20By-Gemini%20AI-blueviolet?style=for-the-badge&logo=google)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Speech Recognition](https://img.shields.io/badge/Speech--Recognition-Enabled-success?style=for-the-badge)

---

## 🧠 Features

- 🗣️ **Wake Word Detection** – Activate with "Jarvis"
- 🌐 **Web Browsing** – Opens Google, YouTube, LinkedIn, etc.
- 🎵 **Play Songs** – Stream YouTube music using voice
- 📰 **News Headlines** – Get top headlines from NewsAPI
- 🌤️ **Weather Report** – Live weather updates via OpenWeather API
- 🤖 **AI Chat** – Ask anything to Google Gemini 2.5 Pro model
- 🔉 **Text-to-Speech** – Voice responses using gTTS and Pygame
- 🧩 **Modular Design** – Clean and scalable Python codebase

---

## 📁 Project Structure

```
jarvis-voice-assistant/
│
├── main.py                # Main assistant logic
├── requirements.txt       # All required Python packages
├── README.md              # You're here!

```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/jarvis-voice-assistant.git
cd jarvis-voice-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Your API Keys

Open `main.py` and replace the placeholders:

```python
NEWS_API_KEY = "your_news_api_key"
WEATHER_API_KEY = "your_openweather_api_key"
GEMINI_API_KEY = "your_google_gemini_api_key"
```

> 📌 Sign up for free API keys at:
> - [NewsAPI](https://newsapi.org)
> - [OpenWeather](https://openweathermap.org)
> - [Google AI Studio (Gemini)](https://makersuite.google.com/app)

---

## 🚀 Running the Assistant

```bash
python main.py
```

Say **“Jarvis”** to activate the assistant and start giving voice commands.

---

## 🛠 Dependencies

- `speechrecognition`
- `gtts`
- `pygame`
- `pyttsx3`
- `pywhatkit`
- `requests`
- `google-generativeai`

Install all using:

```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Google Gemini Pro](https://ai.google.dev/)
- [News API](https://newsapi.org)
- [OpenWeather](https://openweathermap.org)
- [pywhatkit](https://pypi.org/project/pywhatkit/)

---

## 💡 Future Improvements

- Add GUI using Tkinter or PyQt
- Integrate chatbot memory for contextual conversations
- Add email/schedule/calendar support

---
