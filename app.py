import streamlit as st
st.set_page_config(page_title="SQL Genie", page_icon="📊", layout="wide")
import streamlit as st
import pandas as pd
import plotly.express as px
from database import create_database, get_schema, execute_query
from llm import generate_sql, generate_chart_suggestion

st.set_page_config(
    page_title="SQL Chatbot — Business Analytics",
    page_icon="📊",
    layout="wide"
)

create_database()
schema = get_schema()


if "history" not in st.session_state:
    st.session_state.history = []


st.title("📊 SQL Chatbot")
st.caption("Ask business questions in plain English — get tables and charts instantly")
st.divider()

col_main, col_sidebar = st.columns([2, 1])


with col_sidebar:
    st.subheader("💡 Example Questions")
    example_questions = [
        "Show top 5 customers by total spending",
        "What is the monthly revenue trend?",
        "Which product category generates most revenue?",
        "How many orders were placed per city?",
        "Show all products with their prices",
        "Which customer placed the most orders?",
        "Show total revenue by product",
        "What are the top 3 selling products?",
        "Show monthly order count for 2023",
        "Which city has the highest spending customers?"
    ]

    for question in example_questions:
        if st.button(question, use_container_width=True):
            st.session_state.clicked_question = question

    st.divider()
    st.subheader("🗄️ Database Schema")
    with st.expander("View Schema"):
        st.code(schema, language="sql")

    st.divider()
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()


with col_main:
    default_question = st.session_state.get("clicked_question", "")

    user_question = st.text_input(
        "Ask a business question:",
        value=default_question,
        placeholder="e.g. Show top 5 products by total sales..."
    )

    ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)

    if "clicked_question" in st.session_state:
        del st.session_state.clicked_question

    st.divider()

    if ask_button and user_question.strip():

        with st.spinner("Generating SQL query..."):

            sql_query = generate_sql(user_question, schema)

        st.subheader("Generated SQL")
        st.code(sql_query, language="sql")

        with st.spinner("Executing query on database..."):
            columns, rows, error = execute_query(sql_query)

        if error:
            st.error(f"Query Error: {error}")
            st.info(
                "The AI generated an invalid query. "
                "Try rephrasing your question more specifically."
            )

        elif rows and len(rows) > 0:
            df = pd.DataFrame(rows, columns=columns)

            st.subheader(f"Results — {len(rows)} rows")
            st.dataframe(df, use_container_width=True)

            with st.spinner("Choosing best chart type..."):
                chart_type = generate_chart_suggestion(
                    user_question, columns, len(rows)
                )

            st.subheader(f"Chart — {chart_type.title()} Chart")

            try:
                if chart_type == "bar" and len(columns) >= 2:
                    fig = px.bar(
                        df,
                        x=columns[0],
                        y=columns[1],
                        title=user_question,
                        color=columns[0],
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "line" and len(columns) >= 2:
                    fig = px.line(
                        df,
                        x=columns[0],
                        y=columns[1],
                        title=user_question,
                        markers=True
                    )
                    st.plotly_chart(fig, use_container_width=True)

                elif chart_type == "pie" and len(columns) >= 2:
                    fig = px.pie(
                        df,
                        names=columns[0],
                        values=columns[1],
                        title=user_question,
                        color_discrete_sequence=px.colors.qualitative.Set2
                    )
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.info("Data displayed as table above.")

            except Exception:
                st.info("Chart could not be rendered — data shown as table above.")

            st.session_state.history.append({
                "question": user_question,
                "sql": sql_query,
                "rows": len(rows),
                "chart": chart_type
            })

        else:
            st.warning("Query returned no results. Try a different question.")

    if st.session_state.history:
        st.divider()
        st.subheader("📋 Query History")
        for i, item in enumerate(reversed(st.session_state.history)):
            with st.expander(
                f"Q{len(st.session_state.history) - i}: {item['question']}"
            ):
                st.code(item["sql"], language="sql")
                st.caption(
                    f"Returned {item['rows']} rows — "
                    f"Chart: {item['chart'].title()}"
                )
