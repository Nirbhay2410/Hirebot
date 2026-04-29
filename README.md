# 🤖 HireBot: Intelligent Candidate Screening Assistant

> A conversational AI interview agent that automates early-stage recruitment — built for speed, accuracy, and a great candidate experience.

## 📖 What is HireBot?

**HireBot** is an AI-driven screening assistant designed for tech recruitment. Instead of manually scheduling and conducting initial interviews, HireBot handles the entire first-round screening automatically — collecting candidate details, understanding their tech background, and asking relevant technical questions on the spot.

It understands natural language, adapts questions based on the candidate's role and experience level, and wraps up with a downloadable interview summary ready for the recruiter to review.

Powered by **Meta's LLaMA 3.3 70B** model running on **Groq's LPU inference engine**, responses feel instant and natural — not like talking to a form.

---

## ✨ Features

| | |
|---|---|
| ⚡ **Instant Responses** | Groq's LPU hardware makes LLM responses feel real-time |
| 🗺️ **Guided Interview Flow** | A strict state machine ensures no step is skipped |
| 🌐 **Multilingual** | Responds in the candidate's language automatically |
| 🎯 **Role-Aware Questions** | Questions adapt to the job title and years of experience |
| 💬 **Empathy Detection** | Picks up on frustration and responds with encouragement |
| 🔒 **Privacy First** | GDPR-aligned data handling with PII masking built in |
| 📄 **Interview Export** | Candidates can download a full transcript at the end |
| 🎨 **Themed UI** | Three color themes (Midnight, Dark, Light) with one-click switching |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.10+ |
| UI Framework | Streamlit |
| LLM Provider | Groq Cloud |
| Model | LLaMA 3.3 70B Versatile |
| Storage | Local JSON |
| Config | python-dotenv |

---

## 📁 Project Structure

```
hirebot/
├── app.py              # UI, theming, session management
├── chatbot.py          # Interview logic and state machine
├── config.py           # Constants and stage definitions
├── prompts.py          # LLM prompt templates
├── utils.py            # Validators, sentiment detection, formatting
├── data_handler.py     # Data storage and privacy utilities
├── requirements.txt    # Dependencies
├── .env.example        # API key template
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com)

### 1. Clone the repo

```bash
git clone https://github.com/Nirbhay2410/Talentscout.git
cd HireBot
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key

```bash
cp .env.example .env
```

Open `.env` and set:

```
GROQ_API_KEY=your_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Opens at `http://localhost:8501`.

---

## 🧭 How to Use

1. Open the app — HireBot greets you and explains the process
2. Answer each question as prompted (name, email, phone, experience, role, location)
3. List your tech stack in plain language — e.g. *"I work with Python, FastAPI, and PostgreSQL"*
4. HireBot generates 3 technical questions per technology based on your role and experience
5. Answer the questions — HireBot moves through each technology automatically
6. At the end, download your full interview summary from the sidebar
7. Use the theme button (top right) to switch between Midnight / Dark / Light

---

## 🧠 How It Works

### Interview State Machine

The conversation is controlled entirely by Python logic, not the LLM. The LLM only generates text — it never decides what happens next. This prevents hallucinations from derailing the flow.

```
COLLECT_NAME → COLLECT_EMAIL → COLLECT_PHONE → COLLECT_EXPERIENCE
    → COLLECT_POSITION → COLLECT_LOCATION → COLLECT_TECH_STACK
        → TECHNICAL_QUESTIONS → FAREWELL
```

### Tech Stack Extraction

When a candidate writes something like *"mostly Python, some React, and a bit of AWS"*, a dedicated LLM call with a strict extraction prompt converts that into a clean list: `["Python", "React", "AWS"]`. No regex hacks needed.

### Question Personalization

The job title and years of experience are injected directly into the question generation prompt. A junior candidate applying for an internship gets different questions than a senior engineer — same technology, different depth.

### Fallback Handling

Off-topic messages or unclear inputs trigger a fallback prompt that acknowledges the message and redirects the candidate back to the current stage without breaking the flow.

### Sentiment Detection

A keyword-based engine scans each message for frustration signals. When detected, the bot adds an encouraging prefix before continuing — small touch, big difference in candidate experience.

---

## 🔐 Privacy & Data Handling

- A GDPR-aligned privacy notice is shown at the start of every session
- Email and phone are validated before being stored
- All data is saved locally to `candidates_data.json` — nothing is sent to third parties except the Groq API for inference
- A built-in anonymization utility masks PII when sharing or exporting logs
- A `data_consent` flag is recorded with every candidate entry

---

## 🚧 Challenges I Ran Into

**Free-form tech stack input** — Candidates don't write "Python, React, SQL" in a neat list. They write paragraphs. Solved by using a separate LLM call with a strict extraction-only prompt that returns nothing but a comma-separated list.

**Keeping the LLM on topic** — Without guardrails, LLMs will happily answer coding questions or go off on tangents. A strict system prompt acts as a firewall, and all routing logic lives in Python so the model never controls what stage comes next.

**UI theming across Streamlit's fixed containers** — Streamlit renders the chat input in a separate fixed DOM container that ignores most CSS overrides. Solved by hiding that container entirely and building a custom inline input using `st.text_input` inside the main content area.

**Clearing the input after submit** — Streamlit doesn't natively clear `st.text_input` on rerun. Fixed by using a key counter that increments on each submission, forcing Streamlit to mount a fresh widget.

---

## 🔭 What's Next

- Cloud deployment on Streamlit Community Cloud or GCP
- PostgreSQL backend for multi-user support
- Recruiter dashboard to review and filter submissions
- Resume upload with auto-population of candidate fields
- Email notifications on interview completion

---

## 👤 Author

**Nirbhay**
[GitHub](https://github.com/Nirbhay2410)

---

*Built for the AI/ML Intern Assignment — HireBot, screening smarter.*
