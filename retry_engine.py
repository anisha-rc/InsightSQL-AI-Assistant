import ollama


def retry_sql(user_question, failed_sql, error_message):

    retry_prompt = f"""
The following MySQL query failed.

User Question:
{user_question}

Generated SQL:
{failed_sql}

MySQL Error:
{error_message}

Fix the SQL.

Rules:

1. Return ONLY valid MySQL SQL.
2. Do not explain anything.
3. Do not use markdown.
4. Keep the same business logic.
5. Use correct column names.
"""

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": retry_prompt
            }
        ]
    )

    corrected_sql = response["message"]["content"].strip()

    return corrected_sql