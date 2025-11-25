import streamlit as st
import pandas as pd
from collectors import generate_trending_products

st.set_page_config(page_title="Trending Product Finder", layout="wide")

st.title("📈 Trending Product Finder")
st.write("Using data from your **Shopping Trends dataset**")

# Load or generate dataset
try:
    df = pd.read_csv("shopping_trends.csv")
except:
    st.error("shopping_trends.csv not found in project folder!")
    st.stop()

# Generate trends
trending = generate_trending_products()

st.subheader("🔥 Top Trending Products")

st.dataframe(trending, use_container_width=True)

# Show top 10 visual
st.subheader("📊 Top 10 Trending Items")

top10 = trending.head(10)

st.bar_chart(
    top10.set_index("Item Purchased")["Count"]
)

st.success("Trending data loaded successfully!")
