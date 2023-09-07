import streamlit as st
import pandas as pd

from data_functions import getNumberOfBurn, getNumberOfMint, getNumberOfNfts, getTopAccount, getTopModudle, getTopContracts
from graphql_functions import load_query, fetch_graphql_data
from display_functions import display_box

st.title("Nodeinfra Aptos GraphQL")

tables = ['Overview', 'thala', 'topaz', 'msafe'] 
selected_table = 'Overview'

for table in tables:
    if st.sidebar.button(table):
        selected_table = table


if selected_table == 'Overview' :
    st.title("Overview")

    tasks = [
        ('Top Accounts', getTopAccount),
        ('Popular Module (1000 events)', getTopModudle),
        ('Popular Contract (1000 events)', getTopContracts),
        ('Number of Minted', getNumberOfMint),
        ('Number of Burned', getNumberOfBurn),
        ('Number of NFTs', getNumberOfNfts)
    ]

    for label, func in tasks:
        value, query = func()
        display_box(label, value, query)
    

elif selected_table != None : 
    query = load_query(selected_table + '.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    df = pd.DataFrame(data[first_key])

    st.title(selected_table)
    st.write("### GraphQL Query:")
    st.code(query) 

    st.write(df)