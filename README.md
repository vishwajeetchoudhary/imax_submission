# Automated Cold-Calling & Interview Chatbot

## Overview
This project is an **AI-powered chatbot** designed for **automated cold-calling, demo scheduling, interview screening, and payment follow-ups**. It uses **LangChain** and **OpenAI's LLM** to generate dynamic, context-aware responses in **Hinglish (a mix of Hindi & English)**.

## Features
- **Automated Cold-Calling**: Engages with clients and schedules product demos.
- **Interview Screening**: Conducts AI-driven preliminary job interviews.
- **Payment Follow-Ups**: Sends polite reminders for pending invoices.
- **Conversational AI**: Uses **LLM (OpenAI's GPT model)** for intelligent responses.
- **Session Management**: Tracks user interactions and maintains context.
- **CRM Integration**: Logs interactions for business insights.

## Tech Stack
- **Python**
- **LangChain**
- **OpenAI GPT**
- **FastAPI**

## Installation & Setup
1. **Clone the repository**:
   ```sh
   git clone https://github.com/vishwajeetchoudhary/imax_submission.git
   cd imax_submission
   ```

2. **Set up a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (`.env` file or export manually):
   ```sh
   export OPEN_AI_KEY="your-openai-api-key"
   export LLM_MODEL="gpt-4"
   ```

5. **Run the chatbot API**:
   ```sh
   python main.py
   ```

## Usage
* The chatbot supports three key scenarios:
   * **Demo Scheduling** (`scenario=1`): Persuades clients to book a CRM product demo.
   * **Candidate Interview** (`scenario=2`): Conducts AI-driven interview screening.
   * **Payment Follow-Up** (`scenario=3`): Sends polite reminders for pending payments.
* The session is managed using **SessionManager**, and responses are generated via **LLMService**.
* The CRM system logs all customer interactions for tracking.
