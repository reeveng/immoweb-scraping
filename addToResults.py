import json
import requests


def results_from_api():
    API_URL = "https://www.immoweb.be/nl/search-results/huis/te-koop"
    params = {
        "countries": "BE",
        "epcScores": "A+,B,A++,A,C",
        "minBedroomCount": "2",
        "maxPrice": 50000,
        "orderBy": "newest",
        "hasRecommendationActivated": "false",
        "searchType": "similar",
    }
    for page in range(1, 9001):
        r = requests.get(API_URL, params={**params, "page": page})
        results = r.json()["results"]
        if not results:
            break
        for result in results:
            yield result


def get_distance(house):
    url = "https://api.tripgo.com/v1/routing.json"

    long = "Place A"
    lat = "Place B"

    # fetch with dotenv :), we don't wanna leak api key
    tripgo_key = "YOUR_TRIPGO_API_KEY"

    params = {
        "from": f"({lat},{long})",
        "to": "(-51.036351,3.711369)",
        "locale": "en",
        "modes": "pt_pub",
        "v": "11",
    }

    headers = {
        "X-TripGo-Key": tripgo_key,
        "Accept": "application/json",
    }

    return requests.get(url, params=params,headers=headers)


def main():
    seen_ids = set()
    with open("results.json", "r") as f:
        jason = json.load(f)
        saved_results = jason  # ["results"]

    for house in saved_results:
        seen_ids.add(house["id"])

    for house in results_from_api():
        if house["id"] not in seen_ids and house[""]:
            house["distance_to_station"] = get_distance(house)
            house["rejected"] = False
            saved_results.append(house)

    with open("results.json", "w") as f:
        json.dump(saved_results, f)


if __name__ == "__main__":
    main()
