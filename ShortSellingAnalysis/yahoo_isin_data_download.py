import time
import json
import requests
import datetime
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
import pandas as pd
from pandas_datareader import data as web


def convert_isin_to_ticker(infile="data/raw_isin.txt"):
    """
    Convert a list of ISINs (from a text file) to a dict of ISIN : ticker. 
    """
    with open(infile, "r") as f:
        isin_list = [f.rstrip() for f in f.readlines()]

    isin_mapper = {}

    base_url = "https://finance.yahoo.com"
    # Set up Chrome Driver with fake headers
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)
    time.sleep(3)
    print("Opened base search page. Beginning ticker searches...")

    for isin in tqdm(isin_list):
        try:
            input_element = driver.find_element_by_id("yfin-usr-qry")
            input_element.clear()
            input_element.send_keys(isin)

            time.sleep(2)
            html = driver.page_source
            if "<span>Symbols</span>" in html:
                soup = BeautifulSoup(driver.page_source)
                first_res = soup.find("div", {"role": "link", "data-test": "srch-sym"})
                if not first_res:
                    print(f"{isin} missing")
                    continue
                ticker = first_res.find(class_="C(black)").text
                isin_mapper[isin] = ticker
            else:
                print(f"{isin} missing")
        except Exception as e:
            print(f"Error for {isin_list.index(isin)}. {isin}: {e}")
            print("Resetting search")
            driver.get(base_url)
            time.sleep(2)
            continue

    driver.close()

    with open("data/isin_mapper.json", "w") as f:
        json.dump(isin_mapper, f)

    return isin_mapper


def download_price_data(tickerlist, outfile="data/short_price_data.csv"):

    missing_tickers = []
    price_series = []

    for t in tqdm(tickerlist):
        try:
            ohlcv = web.DataReader(t, "yahoo", datetime.datetime(1950, 1, 1),)
            if len(ohlcv) < 5:
                missing_tickers.append(t)
                continue
            close = ohlcv["Adj Close"].rename(t)
            price_series.append(close)
        except Exception as e:
            print(f"Failure for {tickerlist.index(t)}. {t} - {e}")
            missing_tickers.append(t)
            time.sleep(2)
            continue

    print("Price data collected. Creating csv...")
    df = pd.concat(price_series, axis=1)
    df.to_csv(outfile)


if __name__ == "__main__":
    # isin_mapper = convert_isin_to_ticker()
    with open("data/raw_isin.txt", "r") as f:
        isin_mapper = json.load(f)
    tickerlist = list(isin_mapper.values())
    download_price_data(tickerlist)
