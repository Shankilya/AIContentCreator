# ABTalks Autonomous AI Creator

An autonomous AI technology persona built for the ABTalks hackathon. 

## Features
- **Autonomy**: Starts after initialization and runs a background loop to discover, evaluate, and publish content.
- **Editorial Judgment**: Rejects topics based on relevance, novelty, and quality.
- **Memory**: Remembers past topics to avoid repetition using SQLite persistent storage.
- **Resilience**: Gracefully handles network errors, LLM validation failures, and process restarts.

## Setup and Run
1. Ensure Python 3.10+ is installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your API keys.
   ```bash
   cp .env.example .env
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Architecture
- `app/api/`: Public API routes (`/init`, `/feed`).
- `app/engine/`: The core autonomous logic (discovery, memory, editorial, publisher).
- `app/llm/`: Abstraction over LLM providers (LiteLLM).
- `app/db/`: SQLAlchemy definitions and database logic.
