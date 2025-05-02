import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_NAME = os.getenv("PG_DATABASE")
API_ENDPOINT = os.getenv("API_ENDPOINT")
PER_PAGE = int(os.getenv("PER_PAGE"))


def fetch_breweries(page:int =1, per_page:int =20):
    """Ftches breweries from the API for a given page."""
    #logger.info(f"Fetching breweries data from page{page}, per_page {per_page}")
    #url = "https://informed-data-challenge.netlify.app/api/breweries"
    params = {"page": page, "per_page":per_page}
    try:
        response = requests.get(API_ENDPOINT, params=params, timeout=50)
        response.raise_for_status() # Raise an exception for bad status code
        return response.json()
    except requests.exceptions.RequestException as e:
        # logger.info(f"Fetched {len(response.json())} breweries from API")
        print(f"Error fetching page {page}: {e}")
        return None

# if __name__ == "__main__":
#     breweries_df = fetch_all_breweries(per_page=20)

# print(fetch_all_breweries(per_page=20))

def create_breweries_table(conn, cur):
    """ Create the breweries table in the database if it doesn't exist."""
    try:
        cur.execute("""
            DROP TABLE IF EXISTS food_drinks;
            CREATE TABLE food_drinks (
	            id VARCHAR(255) PRIMARY KEY
	            ,name VARCHAR(255)
	            ,brewery_type VARCHAR(255)
	            ,street VARCHAR(255)
	            ,address_2 VARCHAR(255)
	            ,address_3 VARCHAR(255)
	            ,city VARCHAR(255)
	            ,state VARCHAR(255)
	            ,country_province VARCHAR(255)
	            ,postal_code VARCHAR(255)
	            ,website_url VARCHAR(255)
	            ,phone VARCHAR(255)
	            ,country VARCHAR(255)
	            ,longitude FLOAT
	            ,latitude FLOAT
	            ,tags VARCHAR(255)
	            ,rating FLOAT
	            ,number_of_ratings INTEGER
	            ,updated_at TIMESTAMP
	            ,created_at TIMESTAMP
            );

                -- Indexes for potential performance improvements
        CREATE INDEX idx_brewery_type ON food_drinks (brewery_type);
        CREATE INDEX idx_state ON food_drinks (state);
        CREATE INDEX idx_rating ON food_drinks (rating);
        CREATE INDEX idx_number_of_ratings ON food_drinks (number_of_ratings);
        """)
        conn.commit()
        print("'food_drinks' Table created or dropped and recreated succesfullly.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()


def main():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASSWORD,
            database=DB_NAME)
        cur = conn.cursor()

        create_breweries_table(conn, cur)
        page = 1
        breweries = []
        while True:
            all_data = fetch_breweries(page, per_page=20)
            if not all_data:
                break
            breweries.append(all_data)
            page += 1
            return print(breweries)
        cur.close()
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
