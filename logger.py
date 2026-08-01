from datetime import datetime


def log_query(question, sql, status, error=""):

    with open("query_logs.txt", "a", encoding="utf-8") as file:

        file.write("\n" + "=" * 80 + "\n")

        file.write(f"Timestamp : {datetime.now()}\n")

        file.write(f"Question  : {question}\n")

        file.write(f"SQL       : {sql}\n")

        file.write(f"Status    : {status}\n")

        file.write(f"Error     : {error}\n")