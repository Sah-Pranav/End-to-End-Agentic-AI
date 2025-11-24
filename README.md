# 🌍 End-to-End Agentic AI: Global Travel Planner

*Plan your perfect trip with AI - Hotels, Restaurants, Bakeries & More!*

---

## 🚀 Overview

The Global Travel Planner is an intelligent, agentic AI application that helps users plan detailed travel itineraries. It has memory of past conversations and can search the web for real-time data, making it more advanced than simple chatbots.

This AI agent helps you quickly find the best bakeries in Berlin, luxury hotels in Prague, or hidden gems in Paris. It estimates costs, checks the weather, and can generate a PDF itinerary for you.

---


## 📂 Screenshots Directory

You can find project screenshots and demo visuals in the [`/screenshots`](https://github.com/Sah-Pranav/End-to-End-Agentic-AI/blob/main/screenshot/screenshots.pdf) directory.

---

## ⚙️ Installation & Local Setup

### Prerequisites

-   Python 3.11+
-   Docker (optional, for containerization)
-   API Keys for: Groq, Google,Tavily,OpenWeatherMap, FOURSQUARE

### 1. Clone the Repository

```bash
git clone https://github.com/Sah-Pranav/End-to-End-Agentic-AI.git
cd End-to-End-Agentic-AI
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
FOURSQUARE_API_KEY="your_foursquare_api_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

You can run the app in two ways:

**Option A: Using Docker (Recommended)**

```bash
docker-compose up --build
```

**Option B: Manual Run**

Terminal 1 (Backend):
```bash
uvicorn main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
streamlit run app.py
```

---

## ☁️ Deployment to Azure

**Live Demo:** 🏠 [https://aitravelplannar.azurewebsites.net](https://aitravelplannar.azurewebsites.net)

> **Note:** The application is hosted on Azure's Student Plan. The deployment link may not be active if the Azure service has been deprovisioned. You can follow the project locally.

---
## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=langchain)
![LangGraph](https://img.shields.io/badge/LangGraph-Framework-FF9900?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED?style=for-the-badge&logo=docker)
![Azure](https://img.shields.io/badge/Azure-Deployed-0078D4?style=for-the-badge&logo=microsoftazure)

---

## 👨‍💻 Developed By **Pranav**

*Passionate about Agentic AI and Full-Stack Development.*

---
