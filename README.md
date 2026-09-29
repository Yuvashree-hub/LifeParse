# LifeParse – Natural Language to Structured Life Data

> **Tagline:** Speak Naturally. Let AI Organize It.

---

## 📌 Project Overview
**LifeParse** is a lightweight Natural Language Processing (NLP) web application built using **Python, Flask, and spaCy**. It accepts unstructured text describing daily thoughts, plans, tasks, or events, and automatically extracts structured data including:
- 📋 Tasks
- 📅 Events
- ⏰ Dates & Times
- 👤 People
- 📍 Locations
- 🏷️ Categories (Academic, Career, Personal, General)

---

## 🎯 Objective
To demonstrate how core NLP techniques (Named Entity Recognition, Dependency Parsing, and Rule-based Keyword Matching) can transform informal human speech/text into organized, actionable structured JSON data.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.x, Flask
- **NLP Library:** spaCy (`en_core_web_sm` model)
- **Frontend:** HTML5, CSS3 (Modern Dark Navy Theme), Vanilla JavaScript (`fetch API`)

### Workflow:
```text
User Input Text
      ↓
JavaScript Fetch API
      ↓
Flask API POST (/analyze)
      ↓
spaCy NER + Rule Extraction
      ↓
Structured JSON Response
      ↓
UI Dynamic Render