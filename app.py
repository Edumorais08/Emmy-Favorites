from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/<int:year>/<category>/")
def winners_by_year(year, category):

    category = category.replace('-', ' ').replace('_', ' ')

    valid_categories = ["comedy", "drama", "limited series"]

    if category not in valid_categories:
        return "Invalid category", 404
    if year < 1949 or year > 2024:
        return "Ano inválido", 404

    archive = None
    if 1949 <= year <= 1958:
        archive = "data/emmys_1949_1958.json"
    elif 1959 <= year <= 1968:
        archive = "data/emmys_1959_1968.json"
    elif 1969 <= year <= 1978:
        archive = "data/emmys_1969_1978.json"
    elif 1979 <= year <= 1988:
        archive = "data/emmys_1979_1988.json"
    elif 1989 <= year <= 1998:
        archive = "data/emmys_1989_1998.json"
    elif 1999 <= year <= 2008:
        archive = "data/emmys_1999_2008.json"
    elif 2009 <= year <= 2018:
        archive = "data/emmys_2009_2018.json"
    elif 2019 <= year <= 2024:
        archive = "data/emmys_2019_2024.json"

    if not archive:
        return "Arquivo não encontrado.", 404
    try:
        with open(archive, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return f"Dados para o ano {year} não encontrados.", 404
    filtred_data = [item for item in data if item.get("category", "").lower() == category]

    active_page = f"{year}-{category.replace(' ', '-').lower()}"

    return render_template(
        f'category.html',
        category=category,
        year=year,
        data=filtred_data,
        active_page=active_page
    )
