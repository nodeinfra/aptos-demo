import streamlit as st
import requests
import pandas as pd
import json

ENDPOINT = 'https://indexer.mainnet.aptoslabs.com/v1/graphql'
# ENDPOINT = 'https://aptos-mainnet.nodeinfra.com/indexer'

headers = {
    'Content-Type': 'application/json'
}

def fetch_graphql_data(query):
    response = requests.post(ENDPOINT, json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception("GraphQL query failed.")
    
def load_query(filename):
    with open('./queries/' + filename, 'r') as file:
        return file.read()


def display_box(title, value):
    box = f"""
    <div style="padding:20px; border: 2px solid black; border-radius: 5px; margin: 5px">
        <h3 style="color:blue;">{title}</h3>
        <p style="font-size:20px;">{value}</p>
    </div>
    """
    st.markdown(box, unsafe_allow_html=True)

st.title("Streamlit and GraphQL App")

tables = ['test1', 'test2', 'test3', 'test4'] 
selected_table = st.sidebar.selectbox('Choose a table:', tables)

if selected_table == 'test4' :
    query = load_query('account.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    addresses = [item['account_address'] for item in data[first_key]]

    address_count = {}
    for address in addresses:
        if address in address_count:
            address_count[address] += 1
        else:
            address_count[address] = 1

    top_accounts = max(address_count, key=address_count.get)

    query = load_query('nfts.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    number_of_nfts = len(data[first_key])

    query = load_query('mint.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    number_of_mint = len(data[first_key])

    query = load_query('burn.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    number_of_burn = len(data[first_key])

    data = {
            "Top Accounts": top_accounts,
            "Top Module": "Module A",
            "Top Contracts": "Contracts A",
            "Number of Minted": number_of_mint,
            "Number of Burns": number_of_burn,
            "Number of NFTS": number_of_nfts
        }

    for title, value in data.items():
        display_box(title, value)
else :
    query = load_query(selected_table + '.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    df = pd.DataFrame(data[first_key])

    st.write(df)