import requests
import json
import warnings
import pprint
import yaml
import pprint

warnings.filterwarnings('ignore', message='Unverified HTTPS request')

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

json_data = {
    'username': 'admin',
    'password': 'admin',
    'project_id': 'admin',
}
response = requests.post(f'https://nbi:9999/osm/admin/v1/tokens', headers=headers, json=json_data, verify=False)
token_auth = response.json()

if token_auth:
    # Extrai o token do JSON de resposta
    bearer_token = token_auth['id']
    # pprint.pprint(bearer_token)

    if bearer_token:
        # usa o token para fazer uma solicitação GET
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            'accept': 'application/json',
        }


def fetch_vims():
    base_url = "https://nbi:9999/osm/admin/v1/vims"
    url = f"{base_url}"
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print("Falha ao buscar detalhes dos VIMs. Status code:", response.status_code)
        return []


vims = fetch_vims()


def calculate_and_print_resources(vims):
    for vim in vims:
        print(f"VIM: {vim.get('name', 'No Name')} - ID: {vim.get('_id', 'Unknown ID')} ")

        if 'resources' in vim:
            res = vim['resources']
            compute = res['compute']
            storage = res['storage']

            available_instances = compute['instances']['total'] - compute['instances']['used']
            available_ram = compute['ram']['total'] - compute['ram']['used']
            available_vcpus = compute['vcpus']['total'] - compute['vcpus']['used']
            available_storage = storage['storage']['total'] - storage['storage']['used']


            print("Available Resources:")
            print(f"  Instances: {available_instances}")
            print(f"  RAM: {available_ram} MB")
            print(f"  vCPUs: {available_vcpus}")
            print(f"  Storage: {available_storage} GB")
            print("\n--------------------------------------------------\n")

vims = fetch_vims()
calculate_and_print_resources(vims)