import streamlit as st
import requests
import os
import pandas as pd
import tempfile

import base64
import ta

st.set_page_config(page_icon="📈", page_title="Crypto Dashboard")

st.sidebar.image(
    "https://freepngimg.com/save/137073-symbol-bitcoin-png-image-high-quality/512x512",
    width=50,
)

c1, c2 = st.columns([1, 8])

with c1:
    st.image(
        "https://www.pngall.com/wp-content/uploads/1/Bitcoin-PNG-Image.png",
        width=90,
    )




st.markdown(
    """# **Crypto Dashboard**
A profitable trade may or may not have been a good trade

"""
)

st.header("**Selected Price**")

# Load market data from Binance API
df = pd.read_json("https://api.binance.com/api/v3/ticker/24hr")

# Custom function for rounding values
def round_value(input_value):
    if input_value.values > 1:
        a = float(round(input_value, 2))
    else:
        a = float(round(input_value, 8))
    return a


crpytoList = {
    "Price 1": "BTCBUSD",
    "Price 2": "ETHBUSD",
    "Price 3": "BNBBUSD",
    "Price 4": "XRPBUSD",
    "Price 5": "ADABUSD",
    "Price 6": "DOGEBUSD",
    "Price 7": "SHIBBUSD",
    "Price 8": "DOTBUSD",
    "Price 9": "MATICBUSD",
}

col1, col2, col3 = st.columns(3)

for i in range(len(crpytoList.keys())):
    selected_crypto_label = list(crpytoList.keys())[i]
    selected_crypto_index = list(df.symbol).index(crpytoList[selected_crypto_label])
    selected_crypto = st.sidebar.selectbox(
        selected_crypto_label, df.symbol, selected_crypto_index, key=str(i)
    )
    col_df = df[df.symbol == selected_crypto]
    col_price = round_value(col_df.weightedAvgPrice)
    col_percent = f"{float(col_df.priceChangePercent)}%"
    if i < 3:
        with col1:
            st.metric(selected_crypto, col_price, col_percent)
    if 2 < i < 6:
        with col2:
            st.metric(selected_crypto, col_price, col_percent)
    if i > 5:
        with col3:
            st.metric(selected_crypto, col_price, col_percent)

st.header("")

# st.download_button(
#    label="Download data as CSV",
#    data=df,
#    #file_name='large_df.csv',
#    # mime='text/csv'
#    )


@st.cache_data()
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


csv = convert_df(df)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="large_df.csv",
    mime="text/csv",
)

st.dataframe(df, height=2000)


st.markdown(
    """
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
""",
    unsafe_allow_html=True,
)



st.markdown(
    """## **Enter your tokens and download with different indicators**


"""
)

# Set up the base URL and endpoint for the CoinGecko API
base_url = 'https://api.coingecko.com/api/v3/'
endpoint = 'coins/markets'

# Get the list of tokens from the user
user_input = st.text_input("Enter tokens separated by commas")
tokens = user_input.split(",")

# Set up the parameters for the API request
params = {
    'vs_currency': 'usd', # Set the currency to USD
    'ids': ','.join(tokens), # Join the list of tokens into a comma-separated string
    'include_market_cap': 'true', # Include market cap data
    'include_24hr_vol': 'true', # Include 24-hour volume data
    'include_24hr_change': 'true', # Include 24-hour price change data
    'include_last_updated_at': 'true', # Include last updated timestamp data
    'include_circulating_supply': 'true', # Include circulating supply data
    'include_total_supply': 'true', # Include total supply data
    'price_change_percentage': '24h,7d,30d' # Include 24-hour, 7-day and 30-day price change percentage data
}

# Make the API request
response = requests.get(base_url + endpoint, params=params)

# Convert the API response to a dataframe
data = pd.DataFrame(response.json())

# Extract the relevant columns from the dataframe
columns = ['name', 'symbol', 'current_price', 'market_cap', 'circulating_supply', 'total_supply', 'total_volume', 'price_change_24h', 'price_change_percentage_24h',  'last_updated']
data = data[columns]

# Format the data
data['current_price'] = data['current_price'].astype(float).round(2)
data['market_cap'] = data['market_cap'].astype(float).round(2)
data['total_volume'] = data['total_volume'].astype(float).round(2)
data['price_change_24h'] = data['price_change_24h'].astype(float).round(2)
data['price_change_percentage_24h'] = data['price_change_percentage_24h'].astype(float).round(2)

# Add the 50-day and 200-day moving average indicators to the dataframe
data['ma50'] = ta.trend.sma_indicator(data['current_price'], window=50)
data['ma200'] = ta.trend.sma_indicator(data['current_price'], window=200)

# Format the data
data['ma50'] = data['ma50'].astype(float).round(2)
data['ma200'] = data['ma200'].astype(float).round(2)




# Add the RSI indicator to the dataframe
data['rsi'] = ta.momentum.RSIIndicator(data['current_price'], window=14).rsi()

# Format the data
data['ma50'] = data['ma50'].astype(float).round(2)
data['ma200'] = data['ma200'].astype(float).round(2)
data['rsi'] = data['rsi'].astype(float).round(2)


# Display the data in a table
st.write(data)

# Create a button to download the data as a CSV file
def download_csv():
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button('Download CSV'):
    download_csv()



def fetch_coin_list():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    coin_list = response.json()
    return coin_list

coin_list = fetch_coin_list()

# Create a DataFrame to hold the coin details
data = {
    'Coin Name': [],
    'Symbol': [],
    'Coin ID': [],

}

for coin in coin_list:
    data['Coin Name'].append(coin['name'])
    data['Symbol'].append(coin['symbol'])
    data['Coin ID'].append(coin['id'])


df = pd.DataFrame(data)

# Streamlit UI
st.title("CoinGecko Coin List")
st.markdown(
    """## **10200+ Coins are supported, download CSV to view all...**


"""
)
st.write("Total Coins:", len(coin_list))

# Button to show the table
st.table(df.head())




# Button to download the table as a CSV file
def download_csv():
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="coin_details.csv">Download CSV File</a>'
    return href

st.markdown(download_csv(), unsafe_allow_html=True)



# Excahnges
def fetch_supported_exchanges():
    url = 'https://api.coingecko.com/api/v3/exchanges'
    response = requests.get(url)
    exchanges = response.json()
    return exchanges

exchanges = fetch_supported_exchanges()

# Create a DataFrame to hold the exchange details
data = {
    'Name': [],
    'Country': [],
    'Trust Score': []
}

for exchange in exchanges:
    data['Name'].append(exchange['name'])
    data['Country'].append(exchange['country'])
    data['Trust Score'].append(exchange['trust_score'])

df = pd.DataFrame(data)

# Streamlit UI
st.title("List of Supported Exchanges")
st.markdown(
    """## **100+ Exchanges are supported, download CSV to view all...**


"""
)

st.write("Total Exchanges:", len(exchanges))

# Display exchange details in a table
# Button to show the table

st.table(df.head())

# Button to download the table as a CSV file
def download_csv():
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="supported_exchanges.csv">Download CSV File</a>'
    return href

st.markdown(download_csv(), unsafe_allow_html=True)
