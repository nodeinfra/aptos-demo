import streamlit as st
import requests
import pandas as pd

ENDPOINT = 'https://indexer.mainnet.aptoslabs.com/v1/graphql'

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


st.title("Streamlit and GraphQL App")

tables = ['test1', 'test2'] 
selected_table = st.sidebar.selectbox('Choose a table:', tables)

query = load_query(selected_table + '.graphql')
data = fetch_graphql_data(query)
df = pd.DataFrame(data['token_activities_v2'])

st.write(df)