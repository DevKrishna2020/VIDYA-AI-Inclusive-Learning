# VIDYA – AI-Powered Inclusive Learning and Educational Accessibility Platform

> **Aligned with SDG 4: Quality Education** — making learning accessible, understandable, and personalised for every student.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📖 **My Learning** | Browse and complete a structured lesson catalogue across Science, Mathematics, Computer Science, and Languages |
| 🤖 **AI Tutor** | Ask academic questions or discuss uploaded PDF documents with an AI assistant |
| 📄 **Accessible Reader** | Upload PDFs, extract text, simplify language, translate, and listen with text-to-speech |
| 🧠 **Quiz Center** | Take sample quizzes or generate AI-powered quizzes; scores are stored persistently |
| 📊 **Progress Analytics** | Interactive Plotly charts for quiz trends, weekly study time, and subject-wise completion |
| ⚙️ **Settings** | Font size, high-contrast mode, language selection, TTS configuration, and AI API setup |

---

## 🚀 Quick Start (Windows)

### Prerequisites

- Python 3.10 or later  
- pip

### 1 — Clone or download the project

```powershell
git clone https://github.com/<your-username>/vidya.git
cd vidya
```

### 2 — Create and activate a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If you see a policy error, run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 3 — Install dependencies

```powershell
pip install -r requirements.txt
```

### 4 — (Optional) Configure the AI assistant

VIDYA uses the OpenAI API. Features work without it, but AI responses require a key.

**Option A — environment variable (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-..."
```

**Option B — Streamlit secrets file:**

Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk-..."
```

### 5 — Run the application

```powershell
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## ☁️ Streamlit Community Cloud Deployment

1. Push the `vidya/` directory (or the whole repo) to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New app**.
3. Select your repository, set **Main file path** to `vidya/app.py`.
4. In **Advanced settings → Secrets**, add:
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. Click **Deploy**.

---

## 🗂 Project Structure

```
vidya/
├── app.py                    # Main Streamlit entry point (Dashboard)
├── requirements.txt
├── README.md
├── .gitignore
├── vidya_data.db             # SQLite database (auto-created on first run)
│
├── modules/
│   ├── __init__.py
│   ├── database.py           # SQLite persistence layer
│   ├── pdf_reader.py         # PDF text extraction (pypdf)
│   ├── ai_assistant.py       # OpenAI API wrapper
│   ├── translation.py        # deep-translator wrapper
│   ├── speech.py             # gTTS text-to-speech
│   ├── quiz_engine.py        # Quiz bank and AI quiz parser
│   └── progress_tracker.py  # Rule-based recommendation engine
│
├── pages/
│   ├── page_my_learning.py
│   ├── page_ai_tutor.py
│   ├── page_accessible_reader.py
│   ├── page_quiz_center.py
│   ├── page_progress.py
│   └── page_settings.py
│
├── assets/
│   └── logo.svg
│
└── tests/
    ├── test_pdf_reader.py
    ├── test_quiz_engine.py
    └── test_progress_tracker.py
```

---

## 🧪 Running Tests

```powershell
cd vidya
pytest tests/ -v
```

---

## ♿ Accessibility

VIDYA is built with accessibility as a first-class concern:

- Adjustable font size (12 – 24 px)
- High-contrast dark mode
- Text-to-speech for all content
- Translation into 10 languages
- Text simplification (AI-powered)
- Keyboard-accessible controls throughout
- WCAG AA colour contrast in default theme
- All status information uses both colour and icons/text

---

## 🛡 Security

- API keys are **never** hardcoded. Use environment variables or `.streamlit/secrets.toml`.
- The secrets file is listed in `.gitignore`.
- No personally identifiable information is collected or stored.

---

## 📜 License

MIT License — see `LICENSE` for details.

---

## 🤝 SDG 4 Alignment

VIDYA directly addresses **UN Sustainable Development Goal 4: Quality Education** by:

- Removing language barriers through translation and multilingual TTS
- Making dense academic text accessible via AI-powered simplification
- Supporting students with varied learning paces and styles through personalised recommendations
- Providing offline-capable core features for low-connectivity environments
- Delivering a free, open-source platform for educational institutions
