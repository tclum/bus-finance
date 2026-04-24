# Timothy Lum

## About Me
Aloha! My name is Timothy Lum and I am a Computer Science student at the University of Hawai‘i at Mānoa. I was born and raised in Kāneʻohe on the windward side of Oʻahu. My academic work focuses on technology, entrepreneurship, and the intersection of computing and business. Alongside my studies in computer science, I am also preparing to pursue a master’s degree in finance with interests in fintech and emerging technologies.

I enjoy working on projects that combine technology with real-world applications, especially those involving artificial intelligence, game development, and innovative digital systems.

## Academic & Professional Interests
- Artificial Intelligence and Agentic Systems  
- Game Development (Unity)  
- Financial Technology  
- Entrepreneurship and Startup Development  
- Data Analysis and Applied Computing  

## Skills

### Programming Languages
- Python  
- JavaScript  
- C#  
- Java  
- SQL  

### Tools & Technologies
- Unity Game Engine  
- Git & GitHub  
- Node.js  
- React / MERN Stack  
- Discord API & automation tools  
- Data analysis tools (NumPy, Pandas, Jupyter)

## Current Projects
- **AinaQuest** – A card game and digital game project focused on educating players about native, canoe, and invasive plants in Hawai‘i.
- **Unity Agent** – An AI-assisted development system designed to help developers build and debug Unity projects more efficiently.
- **Agentic AI Systems** – Experimenting with multi-agent AI environments in simulations and games.

## Fun Facts
- I enjoy dancing, including ballroom.
- I am currently training for the Honolulu Marathon.
- I like cooking, photography, and exploring new technology projects.

## Career Goals
My long-term goal is to work at the intersection of **technology, finance, and entrepreneurship**, building innovative systems that leverage artificial intelligence and software development to solve real-world problems.

---

## Daily Market Hypothesis Generator

This repository hosts an automated system that scans U.S. equity market data and business-news RSS feeds twice per trading day and generates 3–5 analytical hypotheses formatted as a CFO briefing memo. Full design in [`docs/hypothesis-generator-spec.md`](docs/hypothesis-generator-spec.md).

### How this runs

A GitHub Actions workflow at [`.github/workflows/daily-evaluation.yml`](.github/workflows/daily-evaluation.yml) runs on two cron schedules (UTC):

- **Pre-market** — `0 12 * * 1-5` (8:00 AM ET during DST)
- **Close** — `30 20 * * 1-5` (4:30 PM ET during DST)

Each run pulls current market data via `yfinance`, the last 12 hours of business headlines from Reuters, Yahoo Finance, and MarketWatch, assembles a prompt from the three files in `prompts/`, and calls the Anthropic API. The resulting memo is committed back to `main` at `evaluations/YYYY/MM/YYYY-MM-DD-HHMM.md`, with a sidecar `.meta.json` capturing inputs and token usage. A rolling `evaluations/_metrics.csv` file appends one row per run (timestamp, session, tokens, cost, hypothesis count, stop reason) for later calibration against outcomes.

To trigger a run manually:

```bash
gh workflow run daily-evaluation.yml
```

Or in the UI: **Actions → Daily Evaluation → Run workflow**. The `ANTHROPIC_API_KEY` must be configured as a repo secret.
