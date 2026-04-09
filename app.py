import streamlit as st       
from src.parser import load_letterboxd_zip, get_available_dataframes
from src.profile import (
    get_user_stats,
    get_top_rated_movies,
    get_most_watched_years,
    score_watchlist_by_year_preference,
)
st.set_page_config(page_title="Letterboxd Recommender", layout="wide")

st.title("Letterboxd Recommender")
st.write("Upload your Letterboxd data and get personalized movie recommendations.")

uploaded_zip = st.file_uploader(
    "Upload your Letterboxd export ZIP",
    type=["zip"]
)

if uploaded_zip is not None:
    letterboxd_data = load_letterboxd_zip(uploaded_zip)
    available_files = get_available_dataframes(letterboxd_data)

    
    st.success("ZIP uploaded successfully!")

    st.subheader("Detected Files")
    st.write(available_files)

    # ratings.csv varsa ana analizleri yap
    if "ratings" in letterboxd_data:
        ratings_df = letterboxd_data["ratings"]

        st.subheader("Ratings Preview")
        st.dataframe(ratings_df.head(10))

        st.subheader("Ratings Shape")
        st.write(ratings_df.shape)

        st.subheader("Ratings Columns")
        st.write(ratings_df.columns.tolist())

        st.subheader("User Stats")
        stats = get_user_stats(ratings_df)
        st.write("Total Movies Rated:", stats["total_movies"])
        st.write("Average Rating:", stats["avg_rating"])
        st.write("Max Rating Given:", stats["max_rating"])

        st.subheader("Most Watched Years")
        top_years = get_most_watched_years(ratings_df)
        st.write(top_years)

        st.subheader("Top Rated Movies")
        top_movies = get_top_rated_movies(ratings_df)
        st.dataframe(top_movies.head(10))

    else:
        st.warning("ratings.csv was not found in the uploaded ZIP.")

    # watchlist.csv varsa ve ratings de varsa önceliklendirme yap
    if "ratings" in letterboxd_data and "watchlist" in letterboxd_data:
        watchlist_df = letterboxd_data["watchlist"]
        ratings_df = letterboxd_data["ratings"]

        st.subheader("Watchlist Preview")
        st.dataframe(watchlist_df.head(10))

        st.subheader("Watchlist Priority")
        prioritized_watchlist = score_watchlist_by_year_preference(
            watchlist_df,
            ratings_df
        )
        st.dataframe(prioritized_watchlist.head(20))

    elif "watchlist" not in letterboxd_data:
        st.info("watchlist.csv not found, so watchlist prioritization was skipped.")
