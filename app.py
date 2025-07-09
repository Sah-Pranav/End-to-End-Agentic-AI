import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="🥐 AI Bakery Visit Planner", page_icon="🥐", layout="centered")

st.title("🥐 AI Bakery Visit Planner")
st.subheader("Discover bakeries in Germany with AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("Your request", placeholder="e.g. Find me the best croissant bakery in Berlin")
    submit_button = st.form_submit_button("Plan my trip")

if submit_button and user_input.strip():
    with st.spinner("AI Bakery Planner is curating your experience..."):
        try:
            payload = {"question": user_input}
            response = requests.post(f"{BASE_URL}/query", json=payload)
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                st.markdown(f"""## 🍰 Your Bakery Visit Plan ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})  
---  
{answer}  

*Please confirm details before your visit.*  
""")
            else:
                st.error("The AI Bakery Planner failed: " + response.text)
        except Exception as e:
            st.error(f"Failed to get response: {e}")
