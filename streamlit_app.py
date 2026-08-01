import streamlit as st

from llm import generate_sql, generate_business_insights
from sql_cleaner import clean_sql
from validators import validate_sql
from sql_executor import execute_sql


# ==================================================
# Page Configuration
# ==================================================
st.set_page_config(
    page_title="InsightSQL AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# Sidebar
# ==================================================
with st.sidebar:

    st.title("🤖 InsightSQL AI")

    st.markdown("### Version")
    st.info("Version 1.0")

    st.divider()

    st.markdown("### ⚙️ Technology Stack")

    st.markdown("""
- 🐍 Python
- 🛢️ MySQL
- 🤖 Ollama
- 🦙 Llama 3.1
- 🎈 Streamlit
""")

    st.divider()

    st.markdown("### ✨ Features")

    st.markdown("""
- Natural Language to SQL
- SQL Guardrails
- Safe Query Execution
- AI Business Insights
""")

    st.divider()

    st.markdown("### 👩‍💻 Developed By")

    st.success("Anisha Roy Choudhury")


# ==================================================
# Main Page
# ==================================================

st.title("🤖 InsightSQL AI")

st.caption("Convert business questions into SQL queries using AI")

st.markdown("---")

st.subheader("Ask a Business Question")

question = st.text_input(
    "",
    placeholder="Example: Show sales by region",
    label_visibility="collapsed"
)

generate = st.button(
    "🚀 Generate SQL"
)

st.markdown("---")


# ==================================================
# Generate SQL
# ==================================================

if generate:

    # Empty input check
    if question.strip() == "":
        st.warning("Please enter a business question.")
        st.stop()

    # ==================================================
    # Generate SQL
    # ==================================================

    with st.spinner("🤖 AI is generating SQL..."):

        generated_sql = generate_sql(question)
        generated_sql = clean_sql(generated_sql)

    # ==================================================
    # Display Generated SQL
    # ==================================================

    st.subheader("Generated SQL")

    with st.expander("📄 View Generated SQL"):

        st.code(
            generated_sql,
            language="sql"
        )

    # ==================================================
    # Validate SQL
    # ==================================================

    valid, message = validate_sql(generated_sql)

    if not valid:
        st.error(message)
        st.stop()

    # ==================================================
    # Execute SQL
    # ==================================================

    try:

        results_df = execute_sql(generated_sql)

        st.success("✅ Query executed successfully!")

        # ==================================================
        # Query Results
        # ==================================================

        st.subheader("📊 Query Results")

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        # ==================================================
        # AI Business Insights
        # ==================================================

        st.subheader("🧠 AI Business Insights")

        with st.spinner("🧠 AI is analyzing your data..."):

            try:

                insights = generate_business_insights(
                    question,
                    results_df
                )

                st.markdown(insights)

            except Exception as insight_error:

                st.warning(
                    "⚠️ AI Business Insights are temporarily unavailable."
                )

                st.caption(str(insight_error))

    except Exception as e:

        st.error(f"Error: {str(e)}")


# ==================================================
# Footer
# ==================================================

st.markdown("---")

st.caption(
    "Built using Python • MySQL • Streamlit • Ollama • Llama 3.1"
)