<div align="center">

# 🌌 ABTalks Autonomous AI Creator

<p align="center">
  <img src="https://img.shields.io/badge/Status-Autonomous-00ff00?style=for-the-badge&logo=statuspage&logoColor=white" alt="Status" />
  <img src="https://img.shields.io/badge/Brain-Meta%20Llama%203.1-blue?style=for-the-badge&logo=meta&logoColor=white" alt="LLM" />
  <img src="https://img.shields.io/badge/Engine-Python%203.14-yellow?style=for-the-badge&logo=python&logoColor=white" alt="Backend" />
  <img src="https://img.shields.io/badge/Frontend-React%20%2B%20Three.js-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="Frontend" />
</p>

> **An elite, persistent AI persona that no longer waits for instructions.** 
> Built for the *ABTalks Autonomous AI Creator Hackathon*.

</div>

---

## ⚡ System Overview

The ABTalks AI Creator is not a standard chatbot. It is a **persistent, autonomous entity** that actively surveys the digital landscape, curates high-signal technology news, and publishes original editorial content—all completely without human intervention.

Once initialized, the Neural Cortex takes over. It scrapes data, filters out noise, remembers past publications, and writes in a cohesive editorial voice.

### ✨ Core Capabilities

- 🔍 **Autonomous Discovery:** Continuously scrapes RSS feeds and live data sources (TechCrunch, MIT Tech Review, OpenAI, etc.).
- 🧠 **Editorial Judgment:** Uses Meta Llama 3.1 to strictly grade content. Rejects clickbait; accepts only groundbreaking industry shifts.
- ✍️ **Generative Publishing:** Synthesizes raw data into authoritative, punchy, and engaging 2-4 paragraph posts.
- 💾 **Persistent Memory:** SQLite-backed neural memory prevents duplicate posts and remembers past editorial decisions.
- 🌌 **Immersive Interface:** A production-grade Vite/React frontend featuring a fully interactive 3D Starfield and glassmorphism design.

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **LLM Provider** | **OpenRouter** | API gateway to premium LLM models. |
| **Neural Core** | **Meta Llama 3.1 8B** | The reasoning and generative brain behind the persona. |
| **Backend Engine** | **Python (Starlette/SQLite)** | Pure-Python asynchronous core for persistence and high-speed API routing. |
| **Frontend UI** | **React + Three.js** | Ultra-modern, responsive 3D dashboard built with TailwindCSS and Framer Motion. |

---

## 🚀 Initialization Sequence

### 1. Configure the Neural Cortex
Copy the environment variables and insert your OpenRouter API Key.
```bash
# In the root directory, create a .env file:
LLM_PROVIDER=openrouter
LLM_MODEL=meta-llama/llama-3.1-8b-instruct
OPENROUTER_API_KEY=your_api_key_here
```

### 2. Ignite the Backend Core
Spin up the persistent autonomous loop and API server.
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8080
```
*(The backend will automatically create the local SQLite memory banks on first boot).*

### 3. Launch the 3D Interface
Start the immersive React frontend to monitor your agent.
```bash
cd frontend
npm install
npm run dev
```

Navigate to `http://localhost:5173`. Initialize your agent persona, deploy it to the grid, and watch as it autonomously takes over the feed.

---

<div align="center">
  <i>"I no longer wait for instructions. I curate the future."</i>
  <br/><br/>
  <b>Built by Shankilya</b>
</div>
