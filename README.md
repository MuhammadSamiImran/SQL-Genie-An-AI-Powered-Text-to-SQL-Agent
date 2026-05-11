SQL-Genie: AI-Powered Text-to-SQL Agent 
SQL-Genie is an intelligent natural language interface for structured databases. It allows non-technical users to query business data using plain English, automatically transforming conversational questions into optimized SQL queries, data visualizations, and interactive tables.

Overview
Writing SQL can be a barrier for many business managers. SQL-Genie removes this friction by acting as an AI Data Analyst. By leveraging the high-speed inference of the Groq API and the reasoning power of LLaMA 3.3 70B, the system provides a seamless bridge between human language and relational databases.

Tech Stack
Core Engine: Python

LLM: LLaMA 3.3 70B (via Groq API)

Orchestration: LangChain

Database: SQLite

UI/Frontend: Streamlit

Data Visualization: Plotly Express & Pandas

How It Works
Schema Injection: The system automatically extracts the database schema (tables, columns, and relationships) and injects it into the LLM prompt to prevent hallucinations.

SQL Generation: LLaMA 3.3 70B converts the English query into a precise SQLite SELECT statement.

Execution: The Python backend executes the query against the local SQLite database.

Intelligent Visualization: A second LLM agent analyzes the returned data and selects the most appropriate chart type (Bar, Line, Pie, or Table).

Rendering: Streamlit and Plotly display the results in a clean, interactive dashboard.

Key Features
Natural Language to SQL: No coding required; talk to your data like a human.

Dual-Agent Logic: Separate LLM calls for query generation and visualization strategy.

Real-time Analytics: Interactive charts that update instantly based on your questions.

Safety First: Implementation of SELECT-only guardrails to protect data integrity.

Schema Awareness: Deep understanding of table relationships (Joins) and aggregations.

Project Structure
This project was developed through a modular approach to ensure clean code and scalability:

database.py: Scripts to initialize and populate the sample business database.

app.py: The main Streamlit application and UI logic.

prompts.py: Optimized prompt templates for SQL generation and chart selection.

.env: Secure storage for API credentials.

Installation & Setup
Follow these steps to get SQL-Genie running locally:

1. Install Dependencies
Ensure you have Python installed, then run:

Bash
pip install -r requirements.txt
2. Configure API Key
Copy the example environment file and add your Groq API key:

Bash
cp .env.example .env
# Open the .env file and paste your GROQ_API_KEY
3. Initialize the Database
Run the setup script once to create the SQLite tables and sample data:

Bash
python database.py
4. Launch the Application
Start the Streamlit server to view the app in your browser:

Bash
streamlit run app.py


Disclaimer
This project is built for demonstration purposes using fictional business data. It is intended to showcase the capabilities of Text-to-SQL agents and should be configured with additional security layers for production use with sensitive data.
