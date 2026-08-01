from llm import generate_sql
from sql_cleaner import clean_sql
from validators import validate_sql
from sql_executor import execute_sql
from retry_engine import retry_sql
from logger import log_query


def main():

    print("\n========== InsightSQL AI ==========\n")

    user_question = input("Ask your business question: ")

    generated_sql = generate_sql(user_question)

    generated_sql = clean_sql(generated_sql)

    print("\nGenerated SQL:\n")
    print(generated_sql)

    valid, message = validate_sql(generated_sql)

    if not valid:
        print("\nValidation Failed:")
        print(message)

        log_query(
            user_question,
            generated_sql,
            "FAILED",
            message
        )
        return

    try:

        results = execute_sql(generated_sql)

        print("\nResults:\n")

        for row in results:
            print(row)

        log_query(
            user_question,
            generated_sql,
            "SUCCESS"
        )

    except Exception as e:

        print("\nSQL Execution Failed...")
        print("Trying AI Auto Correction...\n")

        corrected_sql = retry_sql(
            user_question,
            generated_sql,
            str(e)
        )

        corrected_sql = clean_sql(corrected_sql)

        print("Corrected SQL:\n")
        print(corrected_sql)

        valid, message = validate_sql(corrected_sql)

        if not valid:

            print(message)

            log_query(
                user_question,
                corrected_sql,
                "FAILED",
                message
            )

            return

        try:

            results = execute_sql(corrected_sql)

            print("\nResults:\n")

            for row in results:
                print(row)

            log_query(
                user_question,
                corrected_sql,
                "SUCCESS (Retry)"
            )

        except Exception as retry_error:

            print("\nRetry Failed.")
            print(retry_error)

            log_query(
                user_question,
                corrected_sql,
                "FAILED",
                str(retry_error)
            )


if __name__ == "__main__":
    main()