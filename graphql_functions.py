import requests
import os
from dotenv import load_dotenv

# .env 파일의 내용을 불러옴
load_dotenv()

# 환경 변수에서 x-hasura-admin-secret 값을 가져옴
x_hasura_admin_secret = os.getenv("X_HASURA_ADMIN_SECRET")

headers = {
    'Content-Type': 'application/json',
    "x-hasura-admin-secret": x_hasura_admin_secret
}

# ENDPOINT = 'https://indexer.mainnet.aptoslabs.com/v1/graphql'
ENDPOINT = 'https://aptos-mainnet.nodeinfra.com/indexer'

def fetch_graphql_data(query):
    response = requests.post(ENDPOINT, json={"query": query}, headers=headers)
    if response.status_code == 200:
        # print(response.json())
        return response.json()['data']
    else:
        raise Exception("GraphQL query failed.")
    
def load_query(filename):
    with open('./queries/' + filename, 'r') as file:
        return file.read()
