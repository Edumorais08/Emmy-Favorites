from config.config import API_KEY
import requests
import json
from requests.exceptions import SSLError
import time
from functools import lru_cache

archives = {
    # "2019-2024": "data/emmys_2019_2024.json",
    "2009-2018": "data/emmys_2009_2018.json",
    # "1999-2008": "data/emmys_1999_2008.json",
    # "1989-1998": "data/emmys_1989_1998.json",
    # "1979-1988": "data/emmys_1979_1988.json",
    # "1969-1978": "data/emmys_1969_1978.json",
    # "1959-1968": "data/emmys_1959_1968.json",
    # "1949-1958": "data/emmys_1949_1958.json",
}


def get_movie_poster(name):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {
        "api_key": API_KEY,
        "query": name
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                poster_path = data["results"][0]["poster_path"]
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                return poster_url
            else:
                print(name + "- filme não encontrado.")
        else:
            print(f"Erro na requisição: {response.status_code}")
    except SSLError as ssl_err:
        print(f"Erro SSL ao buscar {name}: {ssl_err}")
    except requests.RequestException as req_err:
        print(f"Erro de requisição ao buscar {name}: {req_err}")
    return None

def get_tv_poster(name):

    url = "https://api.themoviedb.org/3/search/tv"
    params = {
        "api_key": API_KEY,
        "query": name
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                poster_path = data["results"][0]["poster_path"]
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                return poster_url
            else:
                print(name + "- Série não encontrada.")
        else:
            print(f"Erro na requisição: {response.status_code}")
    except SSLError as ssl_err:
        print(f"Erro SSL ao buscar {name}: {ssl_err}")
    except requests.RequestException as req_err:
        print(f"Erro de requisição ao buscar {name}: {req_err}")
    return None

def get_actor_img(name):
    url = "https://api.themoviedb.org/3/search/person"
    params = {
        "api_key": API_KEY,
        "query": name
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                person_path = data["results"][0]["profile_path"]
                person_url = f"https://image.tmdb.org/t/p/w500{person_path}"
                return person_url
            else:
                print(name + "- photo não encontrada.")
        else:
            print(f"Erro na requisição: {response.status_code}")
    except SSLError as ssl_err:
        print(f"Erro SSL ao buscar {name}: {ssl_err}")
    except requests.RequestException as req_err:
        print(f"Erro de requisição ao buscar {name}: {req_err}")
    return None

def get_all_img(archives):
    for key, archive in archives.items():
        print("opening archive: " + key)
        with open(archive, "r", encoding="utf-8") as file:
            series = json.load(file)
        for item in series:
            try:
                if "Actor" in item["subcategory"] or "Actress" in item["subcategory"]:
                    if "img" not in item:
                        img_url = get_actor_img(item["name"])  # Chama a função uma vez
                        item["img"] = img_url
                        print(f'{item["name"]} {item["series"]} {str(item["year"])} {img_url}')
                        time.sleep(0.5)
                else:
                    if "img" not in item:
                        img_url = get_tv_poster(item["name"])
                        item["img"] = img_url
                        print(f'{item["name"]} {str(item["year"])} {img_url}')
                        time.sleep(0.5)
            except Exception as e:
                print(f"Erro ao processar {item['name']}: {e}")
        with open(archive, "w", encoding="utf-8") as file:
            json.dump(series, file, indent=4, ensure_ascii=False)


# get_all_img(archives)

for key, archive in archives.items():
    print("opening archive: " + key)
    with open(archive, "r", encoding="utf-8") as file:
        series = json.load(file)
    for item in series:
        if item.get("series") and "Regina King" in item["name"] and "The People v. O.J. Simpson" in item["series"]:
            item['series'] = "American Crime"
            print(f'Adicionado poster para {item["name"]}')
    with open(archive, "w", encoding="utf-8") as file:
        json.dump(series, file, indent=4, ensure_ascii=False)




# if "img" not in item or item["img"] is None:
#     item["img"] = get_movie_poster(item["name"])