import logging
import requests


# set up logger
logging.basicConfig(filename='..\\logs\\bot.log',
                     level=logging.INFO,
                     format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('food_drinks_etl')

def fetch_breweries(page:int =1, per_page:int =20):
    logger.info(f"Fetching breweries data from page{page}, per_page {per_page}")
    url = "https://informed-data-challenge.netlify.app/api/breweries"
    params = {"page": page, "per_page":per_page}
    response = requests.get(url,params=params)
    response.raise_for_status()
    data = response.json()["data"]
    logger.info(f"Fetched {len(response.json())} breweries from API")
    return data


def fetch_all_breweries(per_page=20):
    page = 1
    breweries = []
    while True:
        all_data = fetch_breweries(page,per_page)
        if not all_data:
            break
        breweries.append(all_data)
        page += 1
    return print(breweries)

# if __name__ == "__main__":
#     breweries_df = fetch_all_breweries(per_page=20)

print(fetch_all_breweries(per_page=20))
