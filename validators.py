import re


def validate_sql(sql):

    sql = sql.strip().upper()

    # ==========================================
    # Guardrail 1: Allow only SELECT statements
    # ==========================================
    if not sql.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # ==========================================
    # Guardrail 2: Block dangerous SQL keywords
    # ==========================================
    blocked_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    for keyword in blocked_keywords:
        if re.search(r"\b" + keyword + r"\b", sql):
            return False, f"Blocked SQL keyword detected: {keyword}"

    # ==========================================
    # Guardrail 3: Allow only approved tables
    # ==========================================
    allowed_tables = ["ORDERS"]

    tables = re.findall(r"\bFROM\s+([A-Z_]+)|\bJOIN\s+([A-Z_]+)", sql)

    for table_pair in tables:
        for table in table_pair:
            if table:
                if table not in allowed_tables:
                    return False, f"Unknown table detected: {table}"

    # ==========================================
    # Guardrail 4: Block dangerous SQL functions
    # ==========================================
    blocked_functions = [
        "INTO OUTFILE",
        "LOAD DATA",
        "SHUTDOWN",
        "GRANT",
        "REVOKE"
    ]

    for func in blocked_functions:
        if func in sql:
            return False, f"Blocked SQL function detected: {func}"

    # ==========================================
    # Passed all validations
    # ==========================================
    return True, "SQL is valid."