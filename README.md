# 🦎 Adaptive Support Agent (Chameleon)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![LangChain](https://img.shields.io/badge/Framework-LangChain-green)
![Gradio](https://img.shields.io/badge/UI-Gradio-orange)
![Ollama](https://img.shields.io/badge/LLM-Mistral%2FMinistral-purple)

## 📋 Overview

**Adaptive Support Agent** is an intelligent conversational system designed to **infer implicit user preferences** and adapt its communication style in real-time.

Unlike standard chatbots that provide a "one-size-fits-all" response, this agent acts as a **Chameleon**:
1.  It **observes** the user's input to detect technical proficiency (Novice vs. Expert).
2.  It **dynamically adjusts** its system prompt (persona, vocabulary, verbosity).
3.  It **generates** a tailored response (e.g., reassuring step-by-step guides for beginners vs. concise CLI commands for experts).

This project demonstrates proficiency in **LLM Orchestration**, **Contextual Prompt Tuning**, and **User Profiling**.

## 🧠 Architecture

The system relies on a two-step "Observer-Actor" pattern

1.  **Observer Node:** A lightweight LLM call analyzes the semantic complexity of the user's query (jargon, sentence structure, emotion).
2.  **Strategy Selector:** Maps the detected profile to a specific System Instruction (Prompt Engineering).
3.  **Actor Node:** Generates the final answer using the injected strategy.

## ✨ Key Features

* **Dynamic Profiling:** Automatically categorizes users (Novice, Expert, Neutral) without explicit surveys.
* **Adaptive Persona:** Switches between "Empathetic Guide" and "Senior Engineer" modes instantly.
* **Real-time Streaming:** Token-by-token streaming for a responsive UX using Python generators.
* **Explainability Dashboard:** A side-panel UI visualizing the internal decision-making process (Detected Level + Injected Prompt).

## 🛠️ Tech Stack

* **Language:** Python 3.13
* **Orchestration:** LangChain (Core & Community)
* **LLM Backend:** Ollama (running `ministral-3:3b`)
* **Interface:** Gradio 4.x (Web UI)

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.9+** and **Ollama** installed on your machine.

### 2. Clone the Repository
```bash
git clone https://github.com/quentinbch/adaptive-support-agent.git
cd adaptive-support-agent
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### Setup the Model
This project uses local LLMs via Ollama for privacy and performance. We recommend the 3B model for low latency.

```bash
# Pull the optimized 3B parameter model
ollama pull ministral-3:3b
```
Note: If you change the model, update src/config.py.

## 💻 Usage
Run the main application script:

```bash
python main.py
```
This will launch a Gradio web interface. Open your browser and navigate to `http://localhost:7860`.

### Test Scenarios to Try:

| User Input Example | Expected Profile | Agent Behavior |
| :--- | :--- | :--- |
| "The screen is black and I don't know what to do, I'm scared I broke it." | **NOVICE** | Reassuring, explains step-by-step, no jargon. |
| "I'm getting a 500 error on the /auth endpoint. Check the logs." | **EXPERT** | Concise, asks for logs, provides CLI commands. |
| "My internet is slow, can you help?" | **NEUTRAL** | Balanced tone, moderate detail. |

## 📂 Project Structure

```text
.
├── main.py             # Entry point (Gradio UI logic)
├── requirements.txt    # Project dependencies
└── src/
    ├── agent.py        # Core logic (Profile detection & Generation)
    ├── prompts.py      # System prompts & Adaptation strategies
    └── config.py       # Configuration (Model name, Temperature)
```

## 🔮 Future Improvements

* **Long-term Memory:** Integrate a Vector Database (Weaviate/Chroma) to persist user profiles across sessions.
* **Multi-Agent Routing:** Add specialized agents (e.g., Billing Agent vs. Tech Support Agent).
* **Feedback Loop:** Implement Reinforcement Learning from Human Feedback (RLHF) to refine strategies based on user satisfaction.
