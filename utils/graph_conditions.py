from langgraph.graph import MessagesState

def tools_condition(state: MessagesState) -> bool:
    """
    Decide if tools should be called based on last assistant message.
    """
    last_message = state["messages"][-1]
    content = last_message.get("content", "").lower()

    keywords = [
        "tool:",
        "invoke tool",
        "call tool",
        "use tool",
        "search",
        "weather",
        "cost",
        "estimate",
        "transport",
        "itinerary",
        "opening hours",
        "bakery"
    ]

    return any(keyword in content for keyword in keywords)
