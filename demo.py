import streamlit as st
import pandas as pd

from data_functions import getNumberOfBurn, getNumberOfMint, getNumberOfNfts, getTopAccount, getTopModudle, getTopContracts
from graphql_functions import load_query, fetch_graphql_data, get_event_data_query
from display_functions import display_box, wrap_text_by_char_count

st.title("Nodeinfra Aptos GraphQL")

tables = ['Overview', 'Statistics', 'thala', 'topaz', 'msafe'] 
addresses = {
    'thala': '0x6f986d146e4a90b828d8c12c14b6f4e003fdff11a8eecceceb63744363eaac01',
    'msafe': '0xaa90e0d9d16b63ba4a289fb0dc8d1b454058b21c9b5c76864f825d5c1f32582e',
    'topaz': '0x2c7bccf7b31baf770fdbcc768d9e9cb3d87805e255355df5db32ac9a669010a2'
}

if 'selected_table' not in st.session_state:
    st.session_state.selected_table = 'Overview'

for table in tables:
    if st.sidebar.button(table):
        st.session_state.selected_table = table

if st.session_state.selected_table == 'Overview' :
    st.title("Overview")
    st.write("### If you want to get Aptos DATA")
    st.write("### Try to use our GraphQL ENDPOINT")
    st.write("https://aptos-mainnet.nodeinfra.com/indexer")

    query = load_query('example.graphql')
    data = fetch_graphql_data(query, 'https://aptos-mainnet.nodeinfra.com/indexer')

    st.write("### Example")
    st.code(query)
    st.json(data)

elif st.session_state.selected_table == 'Statistics' :
    st.title("Statistics")

    tasks = [
        ('Top Accounts', getTopAccount),
        ('Number of Minted', getNumberOfMint),
        ('Number of Burned', getNumberOfBurn),
        ('Number of NFTs', getNumberOfNfts)
    ]

    for label, func in tasks:
        value, query = func()
        display_box(label, value, query)

elif st.session_state.selected_table != None : 
    st.title(st.session_state.selected_table)
    st.session_state.selected_event = None
    query = load_query(st.session_state.selected_table + '_events.graphql')
    print(query)
    data = fetch_graphql_data(query, "https://indexer.mainnet.aptoslabs.com/v1/graphql")
    first_key = list(data.keys())[0]

    event_types = [event['type'] for event in data[first_key]]

    st.session_state.selected_event = st.sidebar.selectbox('Choose a type:', event_types)
    
    if st.session_state.selected_event != None :
        query = get_event_data_query(addresses[st.session_state.selected_table], st.session_state.selected_event)
        data = fetch_graphql_data(query, "https://indexer.mainnet.aptoslabs.com/v1/graphql")

        events_data = [event["data"] for event in data["events"]]

        df = pd.DataFrame(events_data)

        text = f'You selected {st.session_state.selected_event}'
        wrapped_text = wrap_text_by_char_count(text, 20)
        st.write(f'### {wrapped_text}')

        st.write("### GraphQL Query:")
        st.code(query)
        st.write(df)
