import psycopg2

DATABASE_URL = 'postgresql://db::25060/db'


def connect():
    conn = None
    try:
        print("Connecting to database:")
        conn = psycopg2.connect(
            host="app-85c4167d-9ae1-4c32-8848-2ea00fde0dcc-do-user-11173886-0.b.db.ondigitalocean.com",
            database="db",
            user="db",
            port="25060",
            password="RGvDD4nIayE7xnAZ")
        cur = conn.cursor()
        print("Getting all portfolio id's")
        query = "SELECT id from public.database_projects_portfolio"
        cur.execute(query)
        all_ids = cur.fetchall()
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
                total_profit += 200  # round(position_profit[0])
                print(round(total_profit))

            query = f"UPDATE public.database_projects_portfolio SET total_profit = {total_profit} WHERE id = '{portfolio_id}'"
            cur.execute(query)
            print("query done: ", query)
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')


# def show_all_portfolios():
# current_session = connect()
# cur = current_session.cursor()
# query = "SELECT id from public.database_projects_portfolio"
# current_session.execute(query)
# all_ids = current_session.fetchone()
# print(all_ids)
# cur.close()


if __name__ == '__main__':
    connect()
