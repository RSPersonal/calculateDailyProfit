import psycopg2
import os
import requests
from decouple import config

HOST_URL = os.getenv("HOST_URL", config("HOST_URL"))


def connect():
    conn = None
    try:
        print("Connecting to database:")
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", config("DB_HOST")),
            database=os.getenv("DB_NAME", config("DB_NAME")),
            user=os.getenv("DB_USERNAME", config("DB_USERNAME")),
            port=os.getenv("DB_PORT", config("DB_PORT")),
            password=os.getenv("DB_PASSWORD", config("DB_PASSWORD")))
        cur = conn.cursor()
        print("Getting all portfolio id's")
        query = "SELECT id from public.database_projects_portfolio"
        cur.execute(query)
        all_ids = cur.fetchall()
        print(f"All id: {all_ids}")

        for fetched_id in all_ids:
            portfolio_id = fetched_id[0]
            query = f"SELECT id FROM public.database_projects_positions WHERE portfolio_id = '{portfolio_id}'"
            cur.execute(query)
            all_positions = cur.fetchall()
            total_profit = 0

            for position in all_positions:
                query = f"SELECT position_profit FROM public.database_projects_positions WHERE id = '{position[0]}'"
                cur.execute(query)
                position_profit = cur.fetchone()
                total_profit += round(position_profit[0])
            try:
                print(
                    f"requested url: {HOST_URL}/api/v1/daily-return/new/{portfolio_id}/{total_profit}")
                response = requests.post(
                    f"{HOST_URL}/api/v1/daily-return/new/{portfolio_id}/{total_profit}")
                print(response.json())
            except ConnectionError as e:
                print(e)
            except KeyError as e:
                print(e)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')


if __name__ == '__main__':
    connect()
