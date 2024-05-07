import requests
import json
import warnings
import pprint
import yaml
import pprint
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

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


def fetch_slices_and_nsr_refs():
    slice_url = f"https://nbi:9999/osm/nsilcm/v1/netslice_instances"
    response = requests.get(slice_url, headers=headers, verify=False)
    nsr_refs = []
    if response.status_code != 200:
        print("Failed to retrieve slice details. Status code:", response.status_code)
    else:
        slices = response.json()
        for slice in slices:
            template = slice.get('network-slice-template', {})
            snssai_identifier = template.get('SNSSAI-identifier', {})
            slice_service_type = snssai_identifier.get('slice-service-type', 'Not specified')
            slice_name = slice.get('name', 'Not specified')
            slice_identifier = slice.get('id', 'Not specified')
            print(f"Network_Slice: {slice_name} - ID: {slice_identifier} - Service_Type: {slice_service_type} ")
            if 'nsr-ref-list' in slice:
                for nsr in slice['nsr-ref-list']:
                    nsr_ref = nsr.get('nsr-ref')
                    if nsr_ref:
                        nsr_refs.append(nsr_ref)
                        print(f"  NS_ID: {nsr_ref}")
            print("\n")
    return nsr_refs


nsr_refs = fetch_slices_and_nsr_refs()


def fetch_vnfr_ids_from_ns(nsr_refs):
    base_url = "https://nbi:9999/osm/nslcm/v1/ns_instances/"
    vnfr_ids = []
    vnfd_ids = []
    for nsr_ref in nsr_refs:
        url = f"{base_url}/{nsr_ref}"
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            ns_details = response.json()
            constituent_vnfr_refs = ns_details.get('constituent-vnfr-ref', [])[0]
            vnfd_identifier = ns_details.get('vnfd-id', [])[0]
            # for vnfr in constituent_vnfr_refs:
            # vnfr_id = vnfr.get('vnfr-id')
            if constituent_vnfr_refs:
                vnfr_ids.append(constituent_vnfr_refs)
            if vnfd_identifier:
                vnfd_ids.append(vnfd_identifier)
                #print(f"NS_ID: {nsr_ref}, VNF_ID: {constituent_vnfr_refs}, VNFD_ID: {vnfd_identifier}")
        else:
            print(f"Failed to retrieve details for NSR Ref {nsr_ref}. Status code: {response.status_code}")
    return vnfr_ids and vnfd_ids


vnfd_ids = fetch_vnfr_ids_from_ns(nsr_refs)


def fetch_vdu_details_from_vnfs(vnfd_ids):
    base_url = "https://nbi:9999/osm/vnfpkgm/v1/vnf_packages/"
    vdu_details_list = []

    for vnfd_identifier in vnfd_ids:
        url = f"{base_url}/{vnfd_identifier}"
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            vnfd_details = response.json()

            if 'vdu' in vnfd_details and 'virtual-compute-desc' in vnfd_details and 'virtual-storage-desc' in vnfd_details:
                compute_desc_map = {vcd['id']: vcd for vcd in vnfd_details['virtual-compute-desc']}
                storage_desc_map = {vsd['id']: vsd for vsd in vnfd_details['virtual-storage-desc']}

                for vdu in vnfd_details['vdu']:
                    vdu_id = vdu.get('id')
                    compute_id = vdu.get('virtual-compute-desc', '')
                    storage_ids = vdu.get('virtual-storage-desc', [])

                    compute_data = compute_desc_map.get(compute_id, {})
                    storage_data = [storage_desc_map.get(sid, {}) for sid in storage_ids] if isinstance(storage_ids, list) else [storage_desc_map.get(storage_ids, {})]

                    # dicionário aplainado para cada VDU
                    for storage in storage_data:
                        vdu_details_list.append({
                            'vnfd_id': vnfd_identifier,
                            'vdu_id': vdu_id,
                            'num_virtual_cpu': compute_data.get('virtual-cpu', {}).get('num-virtual-cpu', ''),
                            'virtual_memory_size': compute_data.get('virtual-memory', {}).get('size', ''),
                            'size_of_storage': storage.get('size-of-storage', '')

                        })

                        #print(f" vnfd_id: {vnfd_identifier}, vdu_id:{vdu_id}, num_virtual_cpu:{compute_data.get('virtual-cpu', {}).get('num-virtual-cpu', '')}, virtual_memory_size: {compute_data.get('virtual-memory', {}).get('size', '')}")
            else:
                print(f"No VDU or compute/storage description data available for VNFD_ID {vnfd_identifier}")
        else:
            print(f"Failed to retrieve details for VNFD_ID {vnfd_identifier}. Status code: {response.status_code}")

    df_resource = pd.DataFrame(vdu_details_list)
    #print(df_resource)
    return df_resource


vdu_details_df = fetch_vdu_details_from_vnfs(vnfd_ids)


def consulta_banco():
   try:
    # Configuração da conexão com o SQLAlchemy
    database_url = "postgresql+psycopg2://postgres:1401@192.168.1.21/postgres"
    engine = create_engine(database_url)

     # Consulta SQL
    query = "SELECT * FROM slice_vm1"

    # tranformando em um dataframe
    df_banco = pd.read_sql(query, engine)
    #print(df_banco)

    # Fechar a conexão
    engine.dispose()

    return df_banco
   except psycopg2.Error as e:
    print("Erro ao conectar ao PostgreSQL:", e)


df_forecast = consulta_banco()

print(vdu_details_df.columns)
print(df_forecast.columns)

# Comparação de vnfd_id e recursos
#merged_df = pd.merge(vdu_details_df, df_forecast, left_on='vnfd_id', right_on='vnf_id', how='inner')
#discrepancies = merged_df[(merged_df['num_virtual_cpu'] != merged_df['cpu_forecast']) | (merged_df['virtual_memory_size'] != merged_df['memory_forecast'])]

# Supondo que 'vnfd_id' é a chave no DataFrame vdu_details_df e 'vnf_id' é a chave correspondente em df_forecast
merged_df = pd.merge(vdu_details_df, df_forecast, left_on='vnfd_id', right_on='vnf_id', how='inner')
