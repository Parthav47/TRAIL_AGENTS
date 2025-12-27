📰 Multi-Agent Article Writer (CrewAI)

A **multi-agent AI article generation system** built using **CrewAI**, designed to collaboratively plan, research, design, and write long-form articles using **multiple free-tier LLMs**.

This project is intentionally designed to **avoid reliance on a single free model**, reduce rate-limit failures, and provide **transparent proof-of-work** from each agent involved in the writing pipeline.

---

## ✨ What This Project Does

Given a single theme, the system:

1. Designs a **content strategy** (tone, framing, boundaries)
2. Creates a **section-wise article blueprint**
3. Performs **web research with citations**
4. Produces a **structured long-form article**

Each step is handled by a **specialized agent**, and **each agent’s output is saved to disk** for review and debugging.

---

## 🧠 Agent Architecture & LLM Usage

This project **intentionally uses multiple LLMs**.

> ⚠️ **Do NOT attempt to run the entire pipeline using only one free model.**
> Free tiers have strict rate limits and will fail mid-execution.

### Agents & Recommended Free Models
| Agent Role             | Core Responsibility                             | Best Free Model(s)                                                             | Why This Works Well                                                           | What to Avoid                                         |
| ---------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Content Strategist** | Story framing, tone, constraints, content rules | **Gemini 2.5 Flash**                                                           | Extremely strong at structured reasoning, instruction-following, and planning | Avoid creative-heavy models here — they over-generate |
| **Article Designer**   | Section breakdown, flow, word budgets           | **Gemini 2.5 Flash**                                                           | Deterministic, consistent formatting, low hallucination                       | Avoid small open models — structure suffers           |
| **Research Analyst**   | Fact finding, synthesis, citation-ready notes   | **Mistral-7B-Instruct (OpenRouter)**<br>**Nous Hermes 2 Mixtral (OpenRouter)** | Handles long context, reasoning, and tool-augmented tasks well                | Avoid Gemini here — quota dies quickly                |
| **Writer**             | Long-form narrative writing                     | **Mistral-7B-Instruct (OpenRouter)**<br>**OpenChat 3.5 (OpenRouter)**          | Good balance of creativity + coherence for articles                           | Avoid ultra-small models — prose quality drops        |
| **Backup / Overflow**  | Emergency fallback if quotas hit                | **Groq LLaMA-3-8B**                                                            | Very fast, generous free tier                                                 | Slightly less nuanced writing                         |


This split **dramatically reduces quota exhaustion** and improves output quality.

---

## 🔑 API Keys Required

You must obtain **separate API keys** for each provider.

### 1️⃣ Google Gemini API (Free Tier)

Used for **Content Strategist & Designer**

🔗 Get API key:
👉 [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

Free tier includes limited requests per minute.

---

### 2️⃣ OpenRouter API

Used for **Mistral-7B-Instruct**

🔗 Get API key:
👉 [https://openrouter.ai/keys](https://openrouter.ai/keys)

Recommended free models:

* `mistralai/mistral-7b-instruct`
* `nousresearch/nous-hermes-2-mixtral`

---

### 3️⃣ Serper API (Web Search Tool)

Used by **Research Analyst**

🔗 Get API key:
👉 [https://serper.dev/](https://serper.dev/)

---

## 📁 Project Structure

```
ARTICLE_WRITER/
├── article_agent/
│   ├── src/article_agent/
│   │   ├── crew.py          # Agents, tasks, LLM wiring
│   │   ├── main.py          # Entry point
│   ├── agents.yaml          # Agent configurations
│   ├── tasks.yaml           # Task definitions
│   ├── .env                 # API keys (NOT committed)
│   └── .venv/               # Virtual environment (ignored)
├── output/
│   ├── content_strategy.md
│   ├── design.md
│   ├── research.md
│   └── final_article.md
├── .gitignore
└── README.md
```

---

## 🚀 Running the Project

### 1️⃣ Create & Activate Virtual Environment

#### Windows (PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\Activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Windows users:**
> If you hit long-path errors during install, enable Windows Long Path support:
> [https://pip.pypa.io/warnings/enable-long-paths](https://pip.pypa.io/warnings/enable-long-paths)

---

### 3️⃣ Configure Environment Variables

Create `.env` inside `article_agent/`:

```env
GEMINI_API_KEY=your_google_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
SERPER_API_KEY=your_serper_api_key
```

❗ **Never commit `.env`**

---

### 4️⃣ Run the Pipeline

```bash
python -m article_agent.main
```

All agent outputs will be saved in the `output/` directory.

---

## 📄 Sample Output (Free-Tier Models)

Using **Gemini 2.5 Flash + Mistral-7B**, the system produces:

* Clear content strategy documents
* Structured article blueprints
* Citation-based research notes
* A readable, coherent long-form article

> Output quality improves significantly when prompts are refined and agent instructions are tightened.

---

## 🎯 Improving Output Quality (Strongly Recommended)

You are **encouraged to modify prompts** in:

* `agents.yaml`
* `tasks.yaml`

### Suggestions:

* Tighten research scope to reduce tool calls
* Add stronger style constraints to the Writer
* Reduce verbosity in planning agents
* Adjust `temperature` per agent:

  * Strategy/Design: `0.2 – 0.3`
  * Writing: `0.6 – 0.8`

Prompt tuning has **more impact than switching models**.

---

## ⚠️ Common Issues & Troubleshooting

### ❌ `Fallback to LiteLLM is not available`

**Why this happens**

* CrewAI routes OpenRouter models through **LiteLLM**
* `litellm` failed to install or install was incomplete

**Fix**

```bash
pip install litellm
```

If installation fails on Windows:

* Enable long path support
* Use a shorter Python install path

---

### ❌ Gemini `429 RESOURCE_EXHAUSTED`

**Cause**

* Free tier allows only ~5 requests/minute

**Solution**

* Do NOT use Gemini for all agents
* Mix models (as done in this project)
* Reduce retries and agent verbosity

---

### ❌ `.venv` accidentally pushed to GitHub

Add this to `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
```

Then remove cached files:

```bash
git rm -r --cached .venv
git commit -m "Remove virtual environment from repo"
```

---

## 🚨 Important Warnings

* ❌ Do not run all agents on one free LLM
* ❌ Do not ignore rate limits
* ❌ Do not hardcode API keys
* ✅ Always mix planning + writing models
* ✅ Save intermediate outputs for debugging

---

## 📌 Final Note

This project reflects **real-world multi-agent system challenges**:

* API quotas
* Model routing
* Tool failures
* Environment issues

If you can run this cleanly, you are already working at an **advanced AI engineering level**.

Happy building 🚀
