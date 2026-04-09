import zipfile
from io import BytesIO

import pandas as pd


def load_csv_from_zip(zip_file, filename):
    """
    ZIP içindeki belirli bir CSV dosyasını pandas DataFrame olarak yükler.
    """
    with zip_file.open(filename) as file:
        df = pd.read_csv(file)
    return df


def normalize_letterboxd_filename(filename):
    """
    ZIP içindeki dosya adını normalize eder.
    Örnek:
        'letterboxd-yourname-2026-04-09-ratings.csv' -> 'ratings'
    """
    lower_name = filename.lower()

    if lower_name.endswith("ratings.csv"):
        return "ratings"
    elif lower_name.endswith("watchlist.csv"):
        return "watchlist"
    elif lower_name.endswith("watched.csv"):
        return "watched"
    elif lower_name.endswith("diary.csv"):
        return "diary"
    elif lower_name.endswith("reviews.csv"):
        return "reviews"
    elif lower_name.endswith("profile.csv"):
        return "profile"
    elif lower_name.endswith("comments.csv"):
        return "comments"
    elif lower_name.endswith("lists.csv"):
        return "lists"
    elif lower_name.endswith("likes.csv"):
        return "likes"
    else:
        return None


def load_letterboxd_zip(uploaded_zip):
    """
    Kullanıcının yüklediği Letterboxd export ZIP dosyasını açar,
    içindeki bilinen CSV dosyalarını okur ve dictionary döndürür.

    Dönen yapı örneği:
    {
        "ratings": DataFrame,
        "watchlist": DataFrame,
        ...
    }
    """
    data = {}

    zip_bytes = BytesIO(uploaded_zip.read())

    with zipfile.ZipFile(zip_bytes, "r") as zip_file:
        file_list = zip_file.namelist()

        for filename in file_list:
            normalized_name = normalize_letterboxd_filename(filename)

            if normalized_name is not None and filename.lower().endswith(".csv"):
                df = load_csv_from_zip(zip_file, filename)
                data[normalized_name] = df

    return data


def get_available_dataframes(letterboxd_data):
    """
    Hangi veri tablolarının bulunduğunu liste olarak döndürür.
    """
    return list(letterboxd_data.keys())