# test_apis.py
import os
import requests
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -------------------------
# Google Places API (NEW)
# -------------------------
def test_google_places():
    print("\n=== Testing Google Places API (New) ===")
    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        print("GOOGLE_API_KEY not set!")
        return

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": google_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id"
    }

    body = {
        "textQuery": "bakeries in Berlin"
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        data = response.json()

        if "places" in data:
            print("✅ Google Places API (New) works! First result:")
            print(data["places"][0])
        else:
            print("❌ Google Places API (New) failed:", data)

    except Exception as e:
        print("❌ Google Places API error:", e)


# -------------------------
# OpenWeatherMap API
# -------------------------
def test_openweathermap():
    print("\n=== Testing OpenWeatherMap API ===")
    weather_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not weather_key:
        print("OPENWEATHERMAP_API_KEY not set!")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q=Berlin,DE&appid={weather_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            print("✅ OpenWeatherMap API works!")
            print(data)
        else:
            print("❌ OpenWeatherMap API failed:", data)
    except Exception as e:
        print("❌ OpenWeatherMap API error:", e)


# -------------------------
# Foursquare API
# -------------------------
def test_foursquare():
    print("\n=== Testing Foursquare API ===")
    fsq_key = os.getenv("FOURSQUARE_API_KEY")
    if not fsq_key:
        print("FOURSQUARE_API_KEY not set!")
        return

    url = "https://api.foursquare.com/v3/places/search"
    headers = {"Authorization": fsq_key}
    params = {"query": "bakery", "near": "Berlin", "limit": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        print("✅ Foursquare API response:")
        print(data)
    except Exception as e:
        print("❌ Foursquare API error:", e)


# -------------------------
# Groq LLM API
# -------------------------
def test_groq_llm():
    print("\n=== Testing Groq LLM API ===")
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        print("GROQ_API_KEY not set!")
        return

    try:
        model = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_key)
        response = model.invoke([{"role": "user", "content": "Hello, how are you?"}])
        print("✅ Groq LLM API works! Response:")
        print(response)
    except Exception as e:
        print("❌ Groq LLM API error:", e)


# -------------------------
# Run all tests
# -------------------------
if __name__ == "__main__":
    print("Testing all APIs...\n")
    test_google_places()
    test_openweathermap()
    test_foursquare()
    test_groq_llm()
