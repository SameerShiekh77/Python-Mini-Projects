import requests

place_id = ""
api_key = ""
def get_reviews(place_id,api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,review&key={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data['result']['reviews'])
    print(len(data['result']['reviews']))
    if response.status_code == 200 and "result" in data:
        reviews = data["result"].get("reviews", [])
        for review in reviews:
            print(f"Rating: {review['rating']}, Review: {review['text']}")
    else:
        print("Failed to fetch reviews")



def get_place_id(query,api_key):
    url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={query}&inputtype=textquery&fields=place_id&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and "candidates" in data:
        place_id = data["candidates"][0]["place_id"]
        print(f"Place ID for '{query}': {place_id}")
    else:
        print("Failed to find place ID")


get_place_id("Al Nafi",api_key)
get_reviews(place_id,api_key)
