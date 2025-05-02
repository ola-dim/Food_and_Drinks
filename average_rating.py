import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_NAME = os.getenv("PG_DATABASE")

def get_average_rating_by_type():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASSWORD,
            database=DB_NAME)
        cur = conn.cursor()

        cur.execute(""" 
            SELECT brewery_type, AVG(ratings) AS average_rating
            FROM food_drinks
            GROUP BY brewery_type
            ORDER BY average_rating DESC      
        """)
        results = cur.fetchall()
        for row in results:
            print(f"Brewery Type: {row[0]}, Average Rating: {row[1]:.2f}")
        
        cur.close()
    except psycopg2.Error as e: 
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    get_average_rating_by_type()