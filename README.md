# 📁 Sortly – AI-Powered Local File Organizer

**Sortly** is an intelligent agent that uses an OpenAI-compatible LLM to analyze and reorganize your local files into meaningful folders. You provide a folder path and a list of file names, and the AI suggests and applies a logical folder structure based on file types, name patterns, and context.

---

## 🚀 Features

- 🔍 Analyzes filenames and groups them based on various criteria
- 📂 Physically reorganizes files on your local system
- 🧠 Uses a system prompt optimized for file organization
- ⚙️ Skips renaming or altering existing folders unless needed
- 🛠️ Falls back to a "Misc" folder only when no logical grouping is found

---

## 📦 Installation

Make sure you have Python 3.8+ installed. Then run:

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

## 📦 Alternatively you can Build the .exe and use it.

Ensure that you followed the above installation steps. 
Run
```bash
python setup.py build
```
This will generate a build folder inside navigate to:
📁 build/
    └── 📁 exe.win-amd64-3.11
        └── sortly.exe

You can double click and run it. Have fun cleaning your folders

## 📥 You can also directly download the installer (However this is experimental and your API key might fail)

➡️ [Download the latest Sortly.zip](https://github.com/bathonSpidey/Sortly/releases/latest

## 📘 System Behavior
Sortly instructs the AI agent to:

- Keep file names unchanged

- Use descriptive folder names (max 3 words)

- Avoid unnecessary changes to existing folders

- Prefer reusing existing folders when applicable

- Only use "Misc" if absolutely necessary

Sortly might create folders like:

📁 Invoices/
    └── invoice_2024_01.pdf
    └── invoice_2024_02.pdf

📁 Documents/
    └── resume.pdf
    └── notes.txt

📁 Photos/
    └── photo_beach.jpg

📁 Music/
    └── song.mp3



