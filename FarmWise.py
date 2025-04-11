import streamlit as st
import pandas as pd
import sqlite3

# Load CSVs
advisor_data = pd.read_csv(r"fle_path.csv")
market_data = pd.read_csv(r"filepath.csv")

# Show column names for debugging (you can remove this later)
# st.write("Advisor Data Columns:", advisor_data.columns.tolist())
# st.write("Market Data Columns:", market_data.columns.tolist())

# Setup SQLite
conn = sqlite3.connect("farm_ai.db")
conn.execute("CREATE TABLE IF NOT EXISTS memory (id INTEGER PRIMARY KEY, role TEXT, content TEXT)")
conn.commit()

# Simulated LLM (Ollama-style)
def query_llm(prompt):
    return f"🤖 Ollama says:\n\n{prompt[:100]}..."

# Simulated Weather & Market Price Functions
def get_weather():
    return {"rainfall": "moderate", "temperature": "warm"}

def get_crop_prices(region):
    if "location" in market_data.columns:
        match = market_data[market_data["location"].str.lower() == region.lower()]
    elif "region" in market_data.columns:
        match = market_data[market_data["region"].str.lower() == region.lower()]
    else:
        match = pd.DataFrame()

    return dict(match.iloc[0, 1:]) if not match.empty else {"rice": 22, "millets": 18}

# Farmer Agent
def farmer_advisor(data):
    weather = get_weather()
    if "recommended_crop" in advisor_data.columns:
        crop = advisor_data["recommended_crop"].iloc[0]
    else:
        crop = "millets"

    prompt = (
        f"Region: {data['location']}\nLand Size: {data['land_size']} acres\n"
        f"Financial Goal: ₹{data['financial_goal']}\n"
        f"Crop Preferences: {data['crop_preferences']}\nWeather: {weather}\n"
        f"Suggested Crop: {crop}\nRecommend a sustainable plan."
    )
    return query_llm(prompt)

# Market Agent
def market_research(region):
    prices = get_crop_prices(region)
    prompt = f"Analyze market in {region}\nCrop Prices: {prices}\nSuggest profitable crop strategy."
    return query_llm(prompt)

# Streamlit UI
st.title("🌾 Smart Farming Advisor (Hackathon Project)")

st.subheader("👩‍🌾 Enter Farmer Details:")
location = st.text_input("Location", "Andhra Pradesh")
land_size = st.slider("Land Size (acres)", 0.5, 10.0, 2.0, 0.5)
financial_goal = st.number_input("Financial Goal (₹)", 1000, 100000, 30000)
crop_preferences = st.multiselect("Crop Preferences", ["rice", "millets", "groundnut", "wheat"])

if st.button("Get Sustainable Farming Advice"):
    farmer_data = {
        "location": location,
        "land_size": land_size,
        "financial_goal": financial_goal,
        "crop_preferences": crop_preferences
    }

    with st.spinner("Analyzing..."):
        advice = farmer_advisor(farmer_data)
        market = market_research(location)

    st.success("✅ Advice Generated!")
    st.subheader("🧠 Farmer Advisor Output:")
    st.write(advice)
    st.subheader("📊 Market Research Output:")
    st.write(market)
