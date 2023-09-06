import requests

# ENDPOINT = 'https://indexer.mainnet.aptoslabs.com/v1/graphql'
ENDPOINT = 'https://aptos-mainnet.nodeinfra.com/indexer'

headers = {
    'Content-Type': 'application/json'
}

def fetch_graphql_data(query):
    response = requests.post(ENDPOINT, json={"query": query}, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()['data']
    else:
        raise Exception("GraphQL query failed.")
    
def load_query(filename):
    with open('./queries/' + filename, 'r') as file:
        return file.read()
