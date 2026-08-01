from database import get_connection
import pandas as pd


def execute_sql(sql):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    cursor.close()
    conn.close()

    df = pd.DataFrame(results, columns=columns)

    return df