import requests
from bs4 import BeautifulSoup
import time
import json

categories = {
    # "Drama": {
    #     "Drama Series": "outstanding-drama-series",
    #     "Lead Actor": "outstanding-lead-actor-in-a-drama-series",
    #     "Lead Actress": "outstanding-lead-actress-in-a-drama-series",
    #     "Supporting Actor": "outstanding-supporting-actor-in-a-drama-series",
    #     "Supporting Actress": "outstanding-supporting-actress-in-a-drama-series",
    #     "Directing": "outstanding-directing-for-a-drama-series",
    #     "Writing": "outstanding-writing-for-a-drama-series",
    # },
    # "Comedy": {
    #     "Comedy Series": "outstanding-comedy-series",
    #     "Lead Actor": "outstanding-lead-actor-in-a-comedy-series",
    #     "Lead Actress": "outstanding-lead-actress-in-a-comedy-series",
    #     "Supporting Actor": "outstanding-supporting-actor-in-a-comedy-series",
    #     "Supporting Actress": "outstanding-supporting-actress-in-a-comedy-series",
    #     "Directing": "outstanding-directing-for-a-comedy-series",
    #     "Writing": "outstanding-writing-for-a-comedy-series",
    # },
    "Limited Series": {
        # "Limited Series": "outstanding-miniseries",
        # "Lead Actor": "outstanding-lead-actor-in-a-miniseries-or-a-movie",
        # "Lead Actress": "outstanding-lead-actress-in-a-miniseries-or-a-movie",
        # "Supporting Actor": "outstanding-supporting-actor-in-a-miniseries-or-a-movie",
        "Supporting Actress": "outstanding-supporting-actress-in-a-miniseries-or-a-movie",
        # "Directing": "outstanding-directing-for-a-miniseries-movie-or-a-dramatic-special",
        # "Writing": "outstanding-writing-in-a-miniseries-or-a-special"
    }
}

archives = {
    "2019-2024": "data/emmys_2019_2024.json",
    "2009-2018": "data/emmys_2009_2018.json",
    "1999-2008": "data/emmys_1999_2008.json",
    "1989-1998": "data/emmys_1989_1998.json",
    "1979-1988": "data/emmys_1979_1988.json",
    "1969-1978": "data/emmys_1969_1978.json",
    "1959-1968": "data/emmys_1959_1968.json",
    "1949-1958": "data/emmys_1949_1958.json",
}

def find_series(response, year, category, subcategory):

    data = []
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    nominees = site.findAll('div', attrs={'class': 'wrap col-12 col-md-7'})

    for nominee in nominees:

            is_winner = nominee.find('div', class_='label_24 accent winner-accent-text')
            name = nominee.find('h3', class_='mb-1 grey-dark pr-5')
            channel = nominee.find('div', class_='upper show-network mb-1')

            data.append({
                "year": year,
                "category": category,
                "subcategory": subcategory,
                "name": name.text.strip() if name else None,
                "channel": channel.text.strip() if channel else None,
                "is_winner": is_winner.text.strip() if is_winner else None,
                "series": None,
                "character": None
            })
    return data

def find_actors(response, year, category, subcategory):

    data = []
    content = response.content
    site = BeautifulSoup(content, 'html.parser')
    nominees = site.findAll('div', attrs={'class': 'wrap col-7 col-md-8 col-lg-9 nom-bio-info-area'})

    for nominee in nominees:

        is_winner = nominee.find('div', class_='label_24 accent winner-accent-text')
        name = nominee.find('h4', class_='mb-1 pr-5')
        series = nominee.find('div', class_='p1 show-title')
        character = nominee.find('div', class_='role-as upper')

        data.append({
            "year": year,
            "category": category,
            "subcategory": subcategory,
            "name": name.text.strip() if name else None,
            "channel": None,
            "is_winner": is_winner.text.strip() if is_winner else None,
            "series": series.text.strip() if series else None,
            "character": character.text.strip() if character else None
        })
    return data

def fetch_all_data(start_year, end_year, categories):
    all_data = []
    for year in range(start_year, end_year + 1):
        for category, subcategories in categories.items():
            for subcategory, url_suffix in subcategories.items():
                url = f'https://www.emmys.com/awards/nominees-winners/{year}/{url_suffix}'
                print(f"Fetching data for {year} - {category} - {subcategory}")
                response = requests.get(url)
                if response.status_code == 200:
                    if "Actor" in subcategory or "Actress" in subcategory:
                        all_data.extend(find_actors(response, year, category, subcategory))
                    else:
                        all_data.extend(find_series(response, year, category, subcategory))
                else:
                    print(f"Failed to fetch: {url}")
                time.sleep(2)
    return all_data


def save_partial_data(data):
    # with open(filename, "w", encoding="utf-8") as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    for key, archive in archives.items():
        print("opening archive: " + key)
        with open(archive, "r", encoding="utf-8") as file:
            series = json.load(file)
        series.extend(data)
        with open(archive, "w", encoding="utf-8") as file:
            json.dump(series, file, ensure_ascii=False, indent=4)
            print(f"Data saved to {archive}")



for start_year in range(1949, 2025, 10):
    end_year = min(start_year + 9, 2024)
    print(f"Fetching data for {start_year} to {end_year}")
    decade_data = fetch_all_data(start_year, end_year, categories)
    save_partial_data(decade_data)




