# SQL-Genie: AI-Powered Text-to-SQL Agent 

**SQL-Genie** is an intelligent natural language interface for structured databases. It allows non-technical users to query business data using plain English, automatically transforming conversational questions into optimized SQL queries, interactive data tables, and dynamic visualizations.

---

## Overview

Writing SQL is often a barrier for business managers and non-technical stakeholders. **SQL-Genie** removes this friction by acting as an **AI Data Analyst**. By leveraging the high-speed inference of the **Groq API** and the reasoning capabilities of **LLaMA 3.3 70B**, the system provides a seamless bridge between human language and relational databases.

## Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)

- **Core Engine:** Python
- **LLM:** LLaMA 3.3 70B (via **Groq API**)
- **Orchestration:** LangChain
- **Database:** SQLite
- **UI/Frontend:** Streamlit
- **Data Visualization:** Plotly Express & Pandas

---

## How It Works

1. **Schema Injection:** The system automatically extracts the database schema (tables, columns, and relationships) and injects it into the LLM prompt to prevent hallucinations.
2. **SQL Generation:** LLaMA 3.3 70B converts the English query into a precise SQLite `SELECT` statement.
3. **Execution:** The Python backend executes the query against the local SQLite database.
4. **Intelligent Visualization:** A second LLM agent analyzes the returned data and selects the most appropriate chart type (Bar, Line, Pie, or Table).
5. **Rendering:** Streamlit and Plotly display the results in a clean, interactive dashboard.

---

## Key Features

- **Natural Language to SQL:** No coding required; talk to your data like a human.
- **Dual-Agent Logic:** Separate LLM calls for query generation and visualization strategy.
- **Real-time Analytics:** Interactive charts that update instantly based on your questions.
- **Safety First:** Implementation of `SELECT-only` guardrails to protect data integrity.
- **Schema Awareness:** Deep understanding of table relationships (Joins) and aggregations.

---

## Project Structure

This project was developed with a modular approach to ensure clean code and scalability:

- `database.py` — Scripts to initialize and populate the sample business database.
- `app.py` — The main Streamlit application and UI logic.
- `prompts.py` — Optimized prompt templates for SQL generation and chart selection.
- `.env` — Secure storage for API credentials.

---

## Installation & Setup

Follow these steps to get **SQL-Genie** running locally:

### 1. Clone the Repository
git clone https://github.com/yourusername/sql-genie.git
cd sql-genie

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Configure API Key
cp .env.example .env
Then open the .env file and add your Groq API key

### 4. Initialize the Database
Bashpython database.py

### 5. Launch the Application
Bashstreamlit run app.py

### Disclaimer
*This project is built for demonstration purposes using fictional business data. It is intended to showcase the capabilities of Text-to-SQL agents and should be configured with additional security layers for production use with sensitive data.*
