import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Arbitrage_Futures_Funding",
    user="postgres",
    password="12345678",
    port="5432"
)
cur = conn.cursor()
cur.execute("SHOW data_directory;")
print(cur.fetchone())

cur.execute("SELECT version();")
print(cur.fetchone())

cur.close()
conn.close()