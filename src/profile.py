def get_top_rated_movies(df, min_rating=4.0):
    """
    Belirli bir eşik puanın üstündeki filmleri seçer
    ve puana göre büyükten küçüğe sıralar.
    """
    top_movies = df[df["Rating"] >= min_rating]
    top_movies = top_movies.sort_values(by="Rating", ascending=False)
    return top_movies


def get_user_stats(df):
    """
    Kullanıcının genel rating istatistiklerini çıkarır.
    """
    total_movies = len(df)
    avg_rating = df["Rating"].mean()
    max_rating = df["Rating"].max()

    return {
        "total_movies": total_movies,
        "avg_rating": round(avg_rating, 2),
        "max_rating": max_rating,
    }


def get_most_watched_years(df):
    """
    Kullanıcının en çok puan verdiği yılları döndürür.
    """
    year_counts = df["Year"].value_counts()
    return year_counts.head(5)


def get_favorite_years(df, min_rating=4.0):
    """
    Kullanıcının yüksek puan verdiği filmler arasında
    en sevdiği yılları bulur.
    """
    high_rated = df[df["Rating"] >= min_rating]
    favorite_years = high_rated["Year"].value_counts()
    return favorite_years


def score_watchlist_by_year_preference(watchlist_df, ratings_df, min_rating=4.0):
    """
    Watchlist'teki filmleri, kullanıcının sevdiği yıllara göre skorlar.
    """
    favorite_years = get_favorite_years(ratings_df, min_rating=min_rating)

    scored_watchlist = watchlist_df.copy()

    # watchlist'teki Year değerini, favorite_years içinde arayıp skor ver
    scored_watchlist["Preference Score"] = (
        scored_watchlist["Year"].map(favorite_years).fillna(0)
    )

    scored_watchlist = scored_watchlist.sort_values(
        by="Preference Score",
        ascending=False
    )

    return scored_watchlist