# Databricks notebook source
# MAGIC %md
# MAGIC ## Input game name and number of desired reviews 
# MAGIC (integer value for both positive and negative, final output will be double the number input)

# COMMAND ----------

game_name = "No Man's Sky"
num_reviews = 1000

# COMMAND ----------

"""Web Scraper for Steam Reviews"""
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_reviews(appid, params={"json": 1}):
    """Get reviews for a given appid of a Steam Game"""
    url = "https://store.steampowered.com/appreviews/"
    response = requests.get(
        url=url + appid,
        params=params,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    return response.json()


def get_n_reviews(appid, n=100, type="all"):
    """Get n reviews for a given appid of a Steam Game"""
    reviews = []
    cursor = "*"
    params = {
        "json": 1,
        "filter": "all",
        "language": "english",
        "day_range": 9223372036854775807,
        "review_type": type,
        "purchase_type": "all",
    }

    while n > 0:
        params["cursor"] = cursor.encode()
        params["num_per_page"] = min(100, n)
        n -= 100

        response = get_reviews(appid, params)
        cursor = response["cursor"]
        reviews += response["reviews"]

        if len(response["reviews"]) < 100:
            break

    return reviews


def get_app_id(game_name):
    """Get the appID for a given game"""
    response = requests.get(
        url=f"https://store.steampowered.com/search/?term={game_name}&category1=998",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    soup = BeautifulSoup(response.text, "html.parser")
    app_id = soup.find(class_="search_result_row")["data-ds-appid"]
    return app_id


def create_dataframe(reviews):
    """Create a dataframe from a list of reviews"""
    data_out = pd.DataFrame()
    for i, review in enumerate(reviews):
        review_df = pd.json_normalize(review, sep="_")
        data_out = pd.concat([data_out, review_df])
    return data_out



# COMMAND ----------


"""Function for scraping Steam reviews and saving them to a parquet file, data for a given game will be saved to a data folder in the root directory as a parquet file"""
appid = get_app_id(game_name)
positive_reviews = get_n_reviews(appid, num_reviews, "positive")
negative_reviews = get_n_reviews(appid, num_reviews, "negative")
reviews = positive_reviews + negative_reviews
df = create_dataframe(reviews)
file_name = game_name.replace(" ", "_")
df.to_parquet(f"../data/{file_name}.parquet")

