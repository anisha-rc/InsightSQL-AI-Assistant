import pandas as pd


# ============================================================
# Helper Functions
# ============================================================

def format_metric_name(metric):
    """
    Convert SQL column names into readable names.
    """

    metric = str(metric)

    metric = metric.replace("`", "")
    metric = metric.replace("SUM(", "")
    metric = metric.replace("AVG(", "")
    metric = metric.replace("COUNT(", "")
    metric = metric.replace("MIN(", "")
    metric = metric.replace("MAX(", "")
    metric = metric.replace(")", "")

    metric = metric.replace("_", " ")

    return metric.title()


def get_numeric_columns(df):
    """Return all numeric columns."""

    return df.select_dtypes(include="number").columns.tolist()


def get_text_columns(df):
    """Return all text columns."""

    return df.select_dtypes(exclude="number").columns.tolist()


# ============================================================
# Detect Result Type
# ============================================================

def detect_result_type(df):

    if df.empty:
        return "empty"

    numeric_cols = get_numeric_columns(df)
    text_cols = get_text_columns(df)

    rows = len(df)
    cols = len(df.columns)

    # -----------------------------
    # Single aggregate
    # Example:
    # Total Sales
    # -----------------------------
    if rows == 1 and len(numeric_cols) == 1:
        return "single"

    # -----------------------------
    # Category + Metric
    # Example:
    # Region | Sales
    # Ship Mode | Quantity
    # Customer | Revenue
    # -----------------------------
    if len(text_cols) == 1 and len(numeric_cols) == 1:
        return "category_metric"

    # -----------------------------
    # Category + Multiple Metrics
    # Example:
    # Region | Sales | Profit
    # -----------------------------
    if len(text_cols) == 1 and len(numeric_cols) > 1:
        return "multiple_metrics"

    # ---------------------------------------------------------
    # Yearly Trend
    #
    # Detect by values instead of column name.
    # First numeric column contains years like 2014–2035.
    # ---------------------------------------------------------
    if cols == 2:

        first = df.iloc[:, 0]

        if pd.api.types.is_numeric_dtype(first):

            if first.between(2000, 2100).all():

                return "yearly"

    # ---------------------------------------------------------
    # Monthly Trend
    #
    # Year column
    # Month column
    # Metric column
    # ---------------------------------------------------------
    if cols == 3:

        first = df.iloc[:, 0]
        second = df.iloc[:, 1]

        if (
            pd.api.types.is_numeric_dtype(first)
            and pd.api.types.is_numeric_dtype(second)
        ):

            if (
                first.between(2000, 2100).all()
                and second.between(1, 12).all()
            ):

                return "monthly"

    # ---------------------------------------------------------
    # Ranked Results
    #
    # Top 10 customers
    # Bottom 10 products
    # ---------------------------------------------------------
    if rows <= 20 and len(text_cols) == 1 and len(numeric_cols) == 1:
        return "ranked"

    return "unknown"


# ============================================================
# Analysis Functions
# ============================================================

def analyze_empty(df):

    return [
        "No records found."
    ]


def analyze_single_value(df):

    numeric = get_numeric_columns(df)[0]

    metric = format_metric_name(numeric)

    value = df.iloc[0][numeric]

    return [
        f"Total records analysed: {len(df)}",
        f"{metric}: {value:,.2f}"
    ]


def analyze_category_metric(df):

    text = get_text_columns(df)[0]
    metric = get_numeric_columns(df)[0]

    highest = df.loc[df[metric].idxmax()]
    lowest = df.loc[df[metric].idxmin()]

    metric_name = format_metric_name(metric)

    return [

        f"Total records analysed: {len(df)}",

        f"Highest {metric_name}: "
        f"{highest[text]} "
        f"({highest[metric]:,.2f})",

        f"Lowest {metric_name}: "
        f"{lowest[text]} "
        f"({lowest[metric]:,.2f})",

        f"Difference: "
        f"{highest[metric]-lowest[metric]:,.2f}"
    ]
# ============================================================
# Multiple Metrics
# ============================================================

def analyze_multiple_metrics(df):

    text = get_text_columns(df)[0]
    metrics = get_numeric_columns(df)

    insights = [
        f"Total records analysed: {len(df)}"
    ]

    for metric in metrics:

        highest = df.loc[df[metric].idxmax()]
        lowest = df.loc[df[metric].idxmin()]

        metric_name = format_metric_name(metric)

        insights.append(f"")
        insights.append(f"📊 {metric_name}")

        insights.append(
            f"Highest: {highest[text]} ({highest[metric]:,.2f})"
        )

        insights.append(
            f"Lowest: {lowest[text]} ({lowest[metric]:,.2f})"
        )

    return insights


# ============================================================
# Yearly Trend
# ============================================================

def analyze_yearly(df):

    year_col = df.columns[0]
    metric = df.columns[1]

    highest = df.loc[df[metric].idxmax()]
    lowest = df.loc[df[metric].idxmin()]

    metric_name = format_metric_name(metric)

    return [

        f"Years analysed: {len(df)}",

        f"Highest {metric_name}: "
        f"{int(highest[year_col])} "
        f"({highest[metric]:,.2f})",

        f"Lowest {metric_name}: "
        f"{int(lowest[year_col])} "
        f"({lowest[metric]:,.2f})"
    ]


# ============================================================
# Monthly Trend
# ============================================================

def analyze_monthly(df):

    year_col = df.columns[0]
    month_col = df.columns[1]
    metric = df.columns[2]

    highest = df.loc[df[metric].idxmax()]
    lowest = df.loc[df[metric].idxmin()]

    metric_name = format_metric_name(metric)

    return [

        f"Months analysed: {len(df)}",

        f"Highest {metric_name}: "
        f"{int(highest[month_col])}/{int(highest[year_col])} "
        f"({highest[metric]:,.2f})",

        f"Lowest {metric_name}: "
        f"{int(lowest[month_col])}/{int(lowest[year_col])} "
        f"({lowest[metric]:,.2f})"
    ]


# ============================================================
# Ranked Results
# ============================================================

def analyze_ranked(df):

    text = get_text_columns(df)[0]
    metric = get_numeric_columns(df)[0]

    first = df.iloc[0]

    metric_name = format_metric_name(metric)

    return [

        f"Top {len(df)} records analysed",

        f"Top {text}: {first[text]}",

        f"{metric_name}: {first[metric]:,.2f}"
    ]


# ============================================================
# Main Function
# ============================================================

def generate_insights(df):

    result_type = detect_result_type(df)

    if result_type == "empty":
        return analyze_empty(df)

    elif result_type == "single":
        return analyze_single_value(df)

    elif result_type == "category_metric":
        return analyze_category_metric(df)

    elif result_type == "multiple_metrics":
        return analyze_multiple_metrics(df)

    elif result_type == "yearly":
        return analyze_yearly(df)

    elif result_type == "monthly":
        return analyze_monthly(df)

    elif result_type == "ranked":
        return analyze_ranked(df)

    return [
        f"Total records analysed: {len(df)}",
        "Insights are not available for this result format."
    ]
