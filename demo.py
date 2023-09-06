import streamlit as st
import pandas as pd
import json

from data_functions import getNumberOfBurn, getNumberOfMint, getNumberOfNfts, getTopAccount, getTopModudle, getTopContracts
from graphql_functions import load_query, fetch_graphql_data
from display_functions import display_box

st.title("Nodeinfra Aptos GraphQL")

tables = ['Overview', 'thala', 'test3', 'test4', 'testestsafcsd'] 
selected_table = None

for table in tables:
    if st.sidebar.button(table):
        selected_table = table


if selected_table == 'Overview' :
    st.title("Overview")
    queries = ["a" for _ in range(6)]

    top_accounts, queries[0] = getTopAccount()
    number_of_nfts, queries[5] = getNumberOfNfts()
    number_of_mint, queries[3] = getNumberOfMint()
    number_of_burn, queries[4] = getNumberOfBurn()
    top_module, queries[1] = getTopModudle()
    top_contract, queries[2] = getTopContracts()

    data = {
            "Top Accounts": top_accounts,
            "Top Module": top_module,
            "Top Contracts": top_contract,
            "Number of Minted": number_of_mint,
            "Number of Burns": number_of_burn,
            "Number of NFTS": number_of_nfts
        }
    i = 0
    for title, value in data.items():
        display_box(title, value, queries[i])
        i += 1

elif selected_table != None : 
    query = load_query(selected_table + '.graphql')
    data = fetch_graphql_data(query)
    first_key = list(data.keys())[0]

    df = pd.DataFrame(data[first_key])

    st.title(selected_table)
    st.write("### GraphQL Query:")
    st.code(query) 

    st.write(df)