import requests, json

def main():
    data = requests.get("https://restcountries.com/v3.1/all?fields=name,cca2").json()
    data.sort(key=lambda x: x["cca2"])
    country_fixtures = []

    for i, country in enumerate(data,start=1):
        name = country["name"]["common"] if country["cca2"] != "AQ" else "Undefined"
        country_fixtures.append({"model": "web.country", "pk": i, "fields":
            {"country_iso": country["cca2"], "name": name}})

    with open('country_fixture.json', 'w', encoding='utf-8') as file:
        json.dump(country_fixtures, file, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    main()