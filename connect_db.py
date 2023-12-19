import psycopg2
from decouple import config

def init_db():
    try:
        conn = psycopg2.connect(
            database="postgres",
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            host='localhost',
            # port=5432
        )
    except Exception as e:
        print("Conn failed.")
        raise e

    conn.autocommit = True
    with conn.cursor() as curr:
        create_db = open("create_foods_db.sql", "r").readline()
        curr.execute(create_db)

        contents = open("create_foods_db.sql", "r").read().split(";")[1:-1]
        for c in contents:
            # print(f"Executing: {c} ")
            curr.execute(c)
    print("DB created.")

    conn.commit()
    conn.close()
