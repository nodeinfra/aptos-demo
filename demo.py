import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

from data_functions import getNumberOfBurn, getNumberOfMint, getNumberOfNfts, getTopAccount, getTopModudle, getTopContracts
from graphql_functions import load_query, fetch_graphql_data, get_event_data_query, get_volume_data_query
from display_functions import display_box, wrap_text_by_char_count

utc_timezone = pytz.timezone('UTC')

st.title("Nodeinfra Aptos GraphQL")

tables = ['Overview', 'Statistics', 'thala', 'topaz', 'msafe'] 
addresses = {
    'thala': '0x6f986d146e4a90b828d8c12c14b6f4e003fdff11a8eecceceb63744363eaac01',
    'msafe': '0xaa90e0d9d16b63ba4a289fb0dc8d1b454058b21c9b5c76864f825d5c1f32582e',
    'topaz': '0x2c7bccf7b31baf770fdbcc768d9e9cb3d87805e255355df5db32ac9a669010a2'
}
period = {
    '1h': 1,
    '1D': 24,
    '3D': 72,
    '7D': 168,
    '30D': 720
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
    st.write("## Docs")
    st.write("https://docs.nodeinfra.com")

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

elif st.session_state.selected_table == 'thala' :
    st.title(st.session_state.selected_table)
    st.session_state.selected_event = None
    query = load_query(st.session_state.selected_table + '_events.graphql')

    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")
    first_key = list(data.keys())[0]

    event_types = [event['type'] for event in data[first_key]]
    event_types.insert(0, 'Volume')

    st.session_state.selected_event = st.sidebar.selectbox('Choose a type:', event_types)
    
    if st.session_state.selected_event == 'Volume' :
        st.session_state.selected_period = st.sidebar.selectbox('Choose a period:', ["1h", "1D", "3D", "7D", "30D"])
        if st.session_state.selected_period != None :
            current_time = datetime.now(utc_timezone)
            time_ago = current_time - timedelta(hours=period[st.session_state.selected_period])
            formatted_time = time_ago.strftime("%Y-%m-%d %H:%M:%S.%f")

            query = get_volume_data_query(formatted_time)
            data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

            events_data = [event["data"] for event in data["events"]]

            df = pd.DataFrame(events_data)
            df['amount'] = df['amount'].astype(int)
            total_amount = df['amount'].sum()

            divided_value = total_amount / 10**8
            formatted_value = "{:,.2f}".format(divided_value)

            st.write(f"### Trading Volume ({st.session_state.selected_period})")
            st.write("### GraphQL Query:")
            st.code(query)
            st.write("###", formatted_value, "APT")

        # time_3_days_ago = current_time - timedelta(hours=72)
        # formatted_time = time_3_days_ago.strftime("%Y-%m-%d %H:%M:%S.%f")

        # query = get_volume_data_query(formatted_time)
        # data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

        # events_data = [event["data"] for event in data["events"]]

        # df = pd.DataFrame(events_data)
        # df['amount'] = df['amount'].astype(int)
        # total_amount = df['amount'].sum()

        # st.write("### Trading Volume (3D)")
        # st.write("### GraphQL Query:")
        # st.code(query)
        # st.write("###", total_amount)

        # time_7_days_ago = current_time - timedelta(hours=168)
        # formatted_time = time_7_days_ago.strftime("%Y-%m-%d %H:%M:%S.%f")

        # query = get_volume_data_query(formatted_time)
        # data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

        # events_data = [event["data"] for event in data["events"]]

        # df = pd.DataFrame(events_data)
        # df['amount'] = df['amount'].astype(int)
        # total_amount = df['amount'].sum()

        # st.write("### Trading Volume (7D)")
        # st.write("### GraphQL Query:")
        # st.code(query)
        # st.write("###", total_amount)

        # time_30_days_ago = current_time - timedelta(hours=720)
        # formatted_time = time_30_days_ago.strftime("%Y-%m-%d %H:%M:%S.%f")

        # query = get_volume_data_query(formatted_time)
        # data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

        # events_data = [event["data"] for event in data["events"]]

        # df = pd.DataFrame(events_data)
        # df['amount'] = df['amount'].astype(int)
        # total_amount = df['amount'].sum()

        # st.write("### Trading Volume (30D)")
        # st.write("### GraphQL Query:")
        # st.code(query)
        # st.write("###", total_amount)


    elif st.session_state.selected_event != None :
        query = get_event_data_query(addresses[st.session_state.selected_table], st.session_state.selected_event)
        data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

        events_data = [event["data"] for event in data["events"]]

        df = pd.DataFrame(events_data)

        text = f'You selected {st.session_state.selected_event}'
        wrapped_text = wrap_text_by_char_count(text, 20)
        st.write(f'### {wrapped_text}')

        st.write("### GraphQL Query:")
        st.code(query)
        st.write(df)

elif st.session_state.selected_table != None : 
    st.title(st.session_state.selected_table)
    st.session_state.selected_event = None
    query = load_query(st.session_state.selected_table + '_events.graphql')
    print(query)
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")
    first_key = list(data.keys())[0]

    event_types = [event['type'] for event in data[first_key]]

    if '0xaa90e0d9d16b63ba4a289fb0dc8d1b454058b21c9b5c76864f825d5c1f32582e::creator::MomentumSafeCreation' in event_types :
        event_types.remove('0xaa90e0d9d16b63ba4a289fb0dc8d1b454058b21c9b5c76864f825d5c1f32582e::creator::MomentumSafeCreation')
        event_types.insert(0, '0xaa90e0d9d16b63ba4a289fb0dc8d1b454058b21c9b5c76864f825d5c1f32582e::creator::MomentumSafeCreation')

    st.session_state.selected_event = st.sidebar.selectbox('Choose a type:', event_types)
    
    if st.session_state.selected_event != None :
        query = get_event_data_query(addresses[st.session_state.selected_table], st.session_state.selected_event)
        data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

        events_data = [event["data"] for event in data["events"]]

        df = pd.DataFrame(events_data)

        text = f'You selected {st.session_state.selected_event}'
        wrapped_text = wrap_text_by_char_count(text, 20)
        st.write(f'### {wrapped_text}')

        st.write("### GraphQL Query:")
        st.code(query)
        st.write(df)
