import ollama
import pandas as pd

from prompts import get_prompt
from prompts import get_insight_prompt


# ==========================================================
# Generate SQL
# ==========================================================

def generate_sql(user_question):

    prompt = get_prompt(user_question)

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    generated_sql = response["message"]["content"].strip()

    return generated_sql


# ==========================================================
# Helper Functions
# ==========================================================

def get_text_columns(df):

    text_cols = []

    for col in df.columns:

        if pd.api.types.is_object_dtype(df[col]):
            text_cols.append(col)

    return text_cols


def get_numeric_columns(df):

    numeric_cols = []

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_cols.append(col)

    return numeric_cols


def detect_time_columns(df):

    time_columns = []

    keywords = [
        "year",
        "month",
        "date",
        "quarter"
    ]

    for col in df.columns:

        name = col.lower()

        if any(k in name for k in keywords):
            time_columns.append(col)

    return time_columns


def format_dataframe(df):

    if len(df) <= 200:
        return df.to_string(index=False)

    return df.head(200).to_string(index=False)


# ==========================================================
# Build Verified Facts
# ==========================================================

def build_verified_facts(results_df):

    if results_df.empty:
        return "No records returned."

    facts = []

    facts.append(f"Total Records Returned: {len(results_df)}")

    text_columns = get_text_columns(results_df)
    numeric_columns = get_numeric_columns(results_df)
    time_columns = detect_time_columns(results_df)

    dimension_columns = []

    # Detect dimensions

    for col in text_columns:
        dimension_columns.append(col)

    for col in time_columns:
        if col not in dimension_columns:
            dimension_columns.append(col)

    measure_columns = []

    for col in numeric_columns:
        if col not in dimension_columns:
            measure_columns.append(col)

    # ------------------------------------------------------
    # CASE 1
    # Single Aggregate
    # ------------------------------------------------------

    if len(measure_columns) == 1 and len(dimension_columns) == 0:

        metric = measure_columns[0]

        value = results_df.iloc[0][metric]

        facts.append("")
        facts.append("Result Type: Single Aggregate")
        facts.append(f"{metric}: {value}")

        return "\n".join(facts)

    # ------------------------------------------------------
    # CASE 2
    # Dimension + Metrics
    # ------------------------------------------------------

    if len(dimension_columns) >= 1 and len(measure_columns) >= 1:

        dimension = dimension_columns[0]

        facts.append("")
        facts.append(f"Primary Dimension: {dimension}")

        for metric in measure_columns:

            idx_max = results_df[metric].idxmax()
            idx_min = results_df[metric].idxmin()

            highest_dimension = results_df.loc[idx_max, dimension]
            lowest_dimension = results_df.loc[idx_min, dimension]

            highest_value = results_df.loc[idx_max, metric]
            lowest_value = results_df.loc[idx_min, metric]

            facts.append("")
            facts.append(f"Metric: {metric}")

            facts.append(
                f"Highest {metric}: "
                f"{highest_dimension} ({highest_value})"
            )

            facts.append(
                f"Lowest {metric}: "
                f"{lowest_dimension} ({lowest_value})"
            )

        # Trend Detection

        if dimension.lower() in ["year", "month"]:

            first_metric = measure_columns[0]

            first_value = results_df.iloc[0][first_metric]
            last_value = results_df.iloc[-1][first_metric]

            if last_value > first_value:
                trend = "Increasing"

            elif last_value < first_value:
                trend = "Decreasing"

            else:
                trend = "Stable"

            facts.append("")
            facts.append(f"Overall Trend: {trend}")

        return "\n".join(facts)

    # ------------------------------------------------------
    # CASE 3
    # Only dimensions returned
    # ------------------------------------------------------

    if len(measure_columns) == 0:

        facts.append("")
        facts.append("Result contains descriptive information only.")

        return "\n".join(facts)

    return "\n".join(facts)


# ==========================================================
# Generate AI Business Insights
# ==========================================================

def generate_business_insights(user_question, results_df):
        # Handle empty results

    if results_df.empty:
        return "No records found. Unable to generate business insights."

    # Build verified facts using Python
    verified_facts = build_verified_facts(results_df)

    # Format dataframe
    dataframe_text = format_dataframe(results_df)

    # Build prompt
    prompt = get_insight_prompt(
        user_question,
        verified_facts,
        dataframe_text
    )

    # Call LLM
    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    insights = response["message"]["content"].strip()

    return insights