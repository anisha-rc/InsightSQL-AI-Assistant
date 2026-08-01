import re


def clean_sql(sql):

    # Remove ```sql
    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)

    # Remove ```
    sql = sql.replace("```", "")

    # Remove leading/trailing spaces
    sql = sql.strip()

    # Remove semicolon at the end (optional)
    if sql.endswith(";"):
        sql = sql[:-1]

    return sql