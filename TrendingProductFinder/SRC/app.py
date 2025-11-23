import streamlit as st
import pandas as pd
import plotly.express as px

from scraper import get_trending_products
from collectors import fetch_interest_over_time
from preprocess import compute_growth_and_baseline
from scoring import compute_trend_score


st.title("Trending Product Finder")


keyword = st.text_input("Enter a product keyword:", value="smart watch")
keywords_input = st.text_area("Enter related keywords (one per line):",
                              value="wireless earbuds\nsmart watch\nportable charger")

timeframe = st.selectbox("Google Trends timeframe", ['now 7-d', 'today 3-m', 'today 12-m'])
geo = st.text_input("Geo (country code, e.g. IN)", value="IN")


if st.button("Fetch & Analyze"):
    if keyword.strip() == "":
        st.error("Please enter a keyword.")
    else:
       
        st.header("📦 Marketplace Live Data (Amazon + Flipkart)")
        st.info(f"Fetching products for: **{keyword}** ...")
        
        market_results = get_trending_products(keyword)

        if len(market_results) == 0:
            st.warning("No marketplace results found (Amazon/Flipkart may have blocked or no products).")
        else:
            df_market = pd.DataFrame(market_results)
            st.dataframe(df_market)

       
        st.header("📈 Google Trends Analysis")

        keywords = [k.strip() for k in keywords_input.splitlines() if k.strip()]
        if len(keywords) == 0:
            st.error("Please enter at least one related keyword.")
        else:
            st.info("Fetching Google Trends...")
            df_trends = fetch_interest_over_time(keywords, timeframe=timeframe, geo=geo)

            st.subheader("Raw Trends Data (last few rows)")
            st.dataframe(df_trends.tail())

           
            feats = compute_growth_and_baseline(df_trends)
            scored = compute_trend_score(feats)

            st.subheader("🔥 Trend Ranking")
            st.dataframe(scored[['keyword','baseline','recent','growth','trend_score']])

           
            top_k = scored['keyword'].tolist()[:5]
            if top_k:
                df_top = df_trends[top_k]
                fig = px.line(df_top, x=df_top.index, y=df_top.columns,
                              labels={'value': 'Interest', 'index': 'Date'},
                              title="Top Trending Keywords (Google Trends)")
                st.plotly_chart(fig)
