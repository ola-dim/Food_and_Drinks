import os
import psycopg2
from dotenv import load_dotenv
import math
import argparse 

load_dotenv()

DB_HOST = os.getenv("PG_HOST")
DB_PORT = os.getenv("PG_PORT")
DB_USER = os.getenv("PG_USER")
DB_PASSWORD = os.getenv("PG_PASSWORD")
DB_NAME = os.getenv("PG_DATABASE")

def haversine(lat1, lon1, lat2, lon2):
    R = 6371 # Radius of Earth in kilometres
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance

def find_closest_brewery(user_lat, user_lon):
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            user=DB_USER, password=DB_PASSWORD,
            database=DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT name, latitude, longitude FROM food_drinks" \
        "WHERE latitude IS NOT NULL AND longitude IS NOT NULL")
        breweries = cur.fetchall()

        closest_brewery = None
        min_distance = float('inf')

        for name, lat, lon in breweries:
            if lat is not None and lon is not None:
                distance = haversine(user_lat, user_lon, lat, lon)
                if distance < min_distance:
                    min_distance = distance
                    closest_brewery = name
        
        cur.close()
        if closest_brewery:
            print(f"The closest brewery is: {closest_brewery} (approximately {min_distance:.2f} km away).")
        else: 
            print(f"No breweries with valid coordinates found.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find the closest brewery to your location.")
    parser.add_argument("--latitude", type=float, required=True, help="Your latitude")
    parser.add_argument("--longitude", type=float, required=True, help="Your longitude")
    args = parser.parse_args()
    find_closest_brewery(args.latitude, args.longitude)


        
        
        