import requests
import os
from dotenv import load_dotenv

# .env 파일의 내용을 불러옴
load_dotenv()

# 환경 변수에서 x-hasura-admin-secret 값을 가져옴
x_hasura_admin_secret = os.getenv("X_HASURA_ADMIN_SECRET")

# headers = {
#     'Content-Type': 'application/json',
#     "x-hasura-admin-secret": x_hasura_admin_secret
# }

# ENDPOINT = 'https://indexer.mainnet.aptoslabs.com/v1/graphql'
# ENDPOINT = 'https://aptos-mainnet.nodeinfra.com/indexer'

def fetch_graphql_data(query, ENDPOINT):
    if ENDPOINT == "https://aptos-mainnet.nodeinfra.com/indexer" :
        headers = {
            'Content-Type': 'application/json',
            "x-hasura-admin-secret": x_hasura_admin_secret
        }
    else :
        headers = {
            'Content-Type': 'application/json'
        }
    response = requests.post(ENDPOINT, json={"query": query}, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        # if 'errors' in response.json():
        # for error in response.json()['errors']:
        #     print(error['message'])
        print(response.json())
        raise Exception("GraphQL query failed.")
    
def load_query(filename):
    with open('./queries/' + filename, 'r') as file:
        return file.read()

def get_event_data_query(address, type) :
    query = f"""
        query MyQuery {{
            events(
                where: {{
                    account_address: {{_eq: "{address}"}},
                    type: {{_eq: "{type}"}}
                }},
                limit: 1000
            ) {{
                data
            }}
        }}
    """
    return query

def get_volume_data_query(now) :
    query = f"""
        query MyQuery {{
            events(
                where: {{account_address: {{_in: ["0x6970b4878c3aea96732be3f31c2dded12d94d9455ff0c76c67d84859dce35136", "0x6b3720cd988adeaf721ed9d4730da4324d52364871a68eac62b46d21e4d2fa99", "0x6f986d146e4a90b828d8c12c14b6f4e003fdff11a8eecceceb63744363eaac01", "0x092e95ed77b5ac815d3fbc2227e76db238339e9ca43ace45031ec2589bea5b8c", "0x48271d39d0b05bd6efca2278f22277d6fcc375504f9839fd73f74ace240861af", "0x4dcae85fc5559071906cd5c76b7420fcbb4b0a92f00ab40ffc394aadbbff5ee9", "0x4dcae85fc5559071906cd5c76b7420fcbb4b0a92f00ab40ffc394aadbbff5ee9"]}}, type: {{_eq: "0x1::coin::DepositEvent"}}, inserted_at: {{_gte: "{now}"}}}}
            ) {{
                data
            }}
        }}
    """
    return query