from langchain_core.tools import Tool
from pydantic import BaseModel, Field
import requests
import os
from exception.customexception import handle_tool_exception

class PlaceSearchInput(BaseModel):
    query: str = Field(description="The search query for places (e.g., 'Bakeries in Berlin', 'Hotels in Paris').")

class PlaceSearchTool:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Missing GOOGLE_API_KEY environment variable.")
        self.place_search_tool_list = [
            Tool.from_function(
                name="search_places",
                description="Search for places like bakeries, hotels, restaurants, etc. using Google Places API or Tavily fallback.",
                func=self.search_places,
                args_schema=PlaceSearchInput
            )
        ]

    def search_places(self, query: str):
        try:
            # 1. Try Google Places API first
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&key={self.api_key}"
            response = requests.get(url)
            
            google_results = []
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    google_results = [
                        f"{place['name']} ({place['formatted_address']}) | Rating: {place.get('rating', 'N/A')} | place_id: {place['place_id']}"
                        for place in data["results"][:5]
                    ]

            if google_results:
                return "\n".join(google_results)
            
            # 2. Fallback to Tavily if Google fails or returns nothing
            # Check for API key first
            if not os.getenv("TAVILY_API_KEY"):
                return f"Google Search failed and TAVILY_API_KEY is missing. Cannot perform fallback search for '{query}'."

            # Lazy import to avoid circular deps
            try:
                from langchain_community.tools.tavily_search import TavilySearchResults
            except ImportError:
                try:
                    from langchain_tavily import TavilySearchResults
                except ImportError:
                    return "Google Search failed and 'langchain_community' or 'langchain_tavily' is not installed."
            
            tavily_tool = TavilySearchResults(max_results=5)
            tavily_results = tavily_tool.invoke({"query": query})
            
            formatted_tavily = []
            for result in tavily_results:
                formatted_tavily.append(f"{result['content']} (Source: {result['url']})")
                
            if formatted_tavily:
                return "Google Search yielded no results. Here are results from the web:\n" + "\n".join(formatted_tavily)
            
            return f"No information found for '{query}' using both Google and Web search."

        except Exception as e:
            return handle_tool_exception("PlaceSearchTool", e)

if __name__ == "__main__":
    tool = PlaceSearchTool()
    print(tool.search_bakeries("Berlin"))
