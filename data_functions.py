from graphql_functions import load_query, fetch_graphql_data

from collections import Counter

def getTopAccount() :
    query = load_query('account.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

    return data["account_transactions_aggregate"]["aggregate"]["max"]["account_address"], query

def getNumberOfNfts() :
    query = load_query('nfts.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

    return data['current_token_ownerships_v2_aggregate']['aggregate']['count'], query

def getNumberOfMint() :
    query = load_query('mint.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

    return data['token_activities_v2_aggregate']['aggregate']['count'], query

def getNumberOfBurn() :
    query = load_query('burn.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")

    return data['token_activities_v2_aggregate']['aggregate']['count'], query

def getTopModudle() :
    query = load_query('events.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")
    first_key = list(data.keys())[0]

    types = [item['type'] for item in data[first_key]]
    modules = ['::'.join(t.split('::')[:2]) for t in types]
    counter = Counter(modules)

    top_module, _ = counter.most_common(1)[0]
    return top_module, query

def getTopContracts() :
    query = load_query('events.graphql')
    data = fetch_graphql_data(query, "https://aptos-mainnet.nodeinfra.com/indexer")
    first_key = list(data.keys())[0]

    types = [item['type'] for item in data[first_key]]
    contracts = ['::'.join(t.split('::')[:3]) for t in types]
    counter = Counter(contracts)

    top_contract, _ = counter.most_common(1)[0]
    return top_contract, query