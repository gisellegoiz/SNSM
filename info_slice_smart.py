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
            print("Network Slices Ativos:")
            print(f" {slice_name} - ID: {slice_identifier} - Service_Type: {slice_service_type} ")
            print(f" NS_ID associados:")
            if 'nsr-ref-list' in slice:
                for nsr in slice['nsr-ref-list']:
                    nsr_ref = nsr.get('nsr-ref')
                    if nsr_ref:
                        nsr_refs.append(nsr_ref)
                        print(f"  ID : {nsr_ref}")
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
                # print(f"NS_ID: {nsr_ref}, VNF_ID: {constituent_vnfr_refs}, VNFD_ID: {vnfd_identifier}")
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
                    storage_data = [storage_desc_map.get(sid, {}) for sid in storage_ids] if isinstance(storage_ids,
                                                                                                        list) else [
                        storage_desc_map.get(storage_ids, {})]

                    # dicionário aplainado para cada VDU
                    for storage in storage_data:
                        vdu_details_list.append({
                            'vnfd_id': vnfd_identifier,
                            'vdu_id': vdu_id,
                            'num_virtual_cpu': compute_data.get('virtual-cpu', {}).get('num-virtual-cpu', ''),
                            'virtual_memory_size': compute_data.get('virtual-memory', {}).get('size', ''),
                            'size_of_storage': storage.get('size-of-storage', '')

                        })

                        # print(f" vnfd_id: {vnfd_identifier}, vdu_id:{vdu_id}, num_virtual_cpu:{compute_data.get('virtual-cpu', {}).get('num-virtual-cpu', '')}, virtual_memory_size: {compute_data.get('virtual-memory', {}).get('size', '')}")
            else:
                print(f"No VDU or compute/storage description data available for VNFD_ID {vnfd_identifier}")
        else:
            print(f"Failed to retrieve details for VNFD_ID {vnfd_identifier}. Status code: {response.status_code}")

    df_resource = pd.DataFrame(vdu_details_list)
    # print(df_resource)
    return df_resource


vdu_details_df = fetch_vdu_details_from_vnfs(vnfd_ids)


def consulta_banco():
    try:
        # Configuração da conexão com o SQLAlchemy
        database_url = "postgresql+psycopg2://postgres:1401@192.168.1.21/postgres"
        engine = create_engine(database_url)

        # Consulta SQL
        query = "SELECT * FROM netslice_embb"

        # tranformando em um dataframe
        df_banco = pd.read_sql(query, engine)
        # print(df_banco)

        # Fechar a conexão
        engine.dispose()

        return df_banco
    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)


df_forecast = consulta_banco()

print('Recursos Atuais:')
print(vdu_details_df)
print("\n")
print('Recursos Previstos:')
print(df_forecast)
print("\n")


# smart - compara os recursos configurados com os recursos previstos
def compare_resources(df_forecast, vdu_details_df):
    # Garantindo que os dados estão no tipo correto antes do merge
    df_forecast['num_virtual_cpu'] = pd.to_numeric(df_forecast['num_virtual_cpu'], errors='coerce')
    vdu_details_df['num_virtual_cpu'] = pd.to_numeric(vdu_details_df['num_virtual_cpu'], errors='coerce')

    df_forecast['virtual_memory_size'] = pd.to_numeric(df_forecast['virtual_memory_size'], errors='coerce')
    vdu_details_df['virtual_memory_size'] = pd.to_numeric(vdu_details_df['virtual_memory_size'], errors='coerce')

    # Fazendo um merge dos DataFrames baseado em 'vnfd_id'
    merged_df = pd.merge(df_forecast, vdu_details_df, on='vdu_id', suffixes=('_forecast', '_current'))

    # Convertendo as colunas após o merge para garantir que estão em inteiros
    merged_df['num_virtual_cpu_forecast'] = pd.to_numeric(merged_df['num_virtual_cpu_forecast'], errors='coerce')
    merged_df['num_virtual_cpu_current'] = pd.to_numeric(merged_df['num_virtual_cpu_current'], errors='coerce')

    merged_df['virtual_memory_size_forecast'] = pd.to_numeric(merged_df['virtual_memory_size_forecast'],
                                                              errors='coerce')
    merged_df['virtual_memory_size_current'] = pd.to_numeric(merged_df['virtual_memory_size_current'], errors='coerce')

    # Verificando se os recursos correspondem
    for index, row in merged_df.iterrows():
        print("Resultado da Analise para Adequação de Recursos:")
        if pd.isna(row['num_virtual_cpu_forecast']) or pd.isna(row['num_virtual_cpu_current']) or pd.isna(
                row['virtual_memory_size_forecast']) or pd.isna(row['virtual_memory_size_current']):
            print(f"Algum valor está faltando para {row['vdu_id']}, não é possível comparar.")
            print("\n")
        elif row['num_virtual_cpu_forecast'] == row['num_virtual_cpu_current'] and row[
            'virtual_memory_size_forecast'] == row['virtual_memory_size_current']:
            print(f"Recursos para {row['vdu_id']} já estão atendidos.")
            print("\n")
        else:
            # Calcula a diferença para CPU e Memória
            cpu_diff = row['num_virtual_cpu_forecast'] - row['num_virtual_cpu_current']
            mem_diff = row['virtual_memory_size_forecast'] - row['virtual_memory_size_current']
            print(
                f"O vdu_id {row['vdu_id']} precisa de ajuste: {'aumentar' if cpu_diff > 0 else 'reduzir'} {abs(cpu_diff)} CPUs e {'aumentar' if mem_diff > 0 else 'reduzir'} {abs(mem_diff)} GB de memória.")
            print("\n")


# Supondo que df_forecast e vdu_details_df sejam DataFrames já definidos e carregados com os dados adequados.
compare_resources(df_forecast, vdu_details_df)


# infovim

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


def available_resources(vims):
    for vim in vims:
        vim_name = vim.get('name', 'No Name')
        vim_id = vim.get('_id', 'Unknown ID')
        print(f" Recursos Disponiveis no VIM: {vim_name} - ID: {vim_id} ")

        if 'resources' in vim:
            res = vim['resources']
            compute = res['compute']
            # storage = res['storage']

            available_instances = compute['instances']['total'] - compute['instances']['used'],
            available_ram = compute['ram']['total'] - compute['ram']['used'],
            available_vcpus = compute['vcpus']['total'] - compute['vcpus']['used']
            # 'available_storage': storage['storage']['total'] - storage['storage']['used']

            available_resources_list = {
                'available_instances': available_instances,
                'available_ram': available_ram,
                'available_vcpus': available_vcpus
            }
            df_available_resources = pd.DataFrame(available_resources_list)
            # print(df_available_resources)
    return df_available_resources


available_resources_vim = available_resources(vims)
print(available_resources_vim)
print("\n")


## smart - compara os recursos previstos com os recursos disponiveis nos VIMs
def compare_resources_vim():
    # Calculando a soma dos recursos previstos
    total_cpus_needed = df_forecast['num_virtual_cpu'].sum()
    total_memory_needed = df_forecast['virtual_memory_size'].sum()
    print(f" Total de vcpus necessarios: {total_cpus_needed}, Total de memoria ram necessária: {total_memory_needed}")

    # Recursos disponíveis do VIM
    available_vcpus = available_resources_vim.loc[0, 'available_vcpus']
    available_ram = available_resources_vim.loc[0, 'available_ram']

    # Verificação dos recursos
    print("Resultado da Analise de Recursos Disponíveis no VIM")
    if total_cpus_needed <= available_vcpus and total_memory_needed <= available_ram:
        print("O VIM possui recursos suficientes para suportar os recursos previstos.")
    else:
        print("O VIM não possui recursos suficientes:")
        if total_cpus_needed > available_vcpus:
            print(f"Faltam {total_cpus_needed - available_vcpus} vCPUs.")
        if total_memory_needed > available_ram:
            print(f"Faltam {total_memory_needed - available_ram} MB de memória.")


compare_resources_vim()


def verticalscale(df_forecast):
    for index, row in df_forecast.iterrows():
        print(row['vdu_id'])  # Exemplo de uso do vdu_id
        print(row['vnf_id'])
        print(row['ns_id'])

        update_data = {
            "verticalScale": "string",
            "changeVnfFlavorData": {
                "vnfInstanceId": row['vnf_id'],  # Uso direto da coluna
                "additionalParams": {
                    "vduid": row['vdu_id'],
                    "vduCountIndex": 0,
                    "virtualMemory": row['virtual_memory_size'],
                    "sizeOfStorage": 5,
                    "numVirtualCpu": row['num_virtual_cpu'],
                }
            }
        }
        verticalscale_up = requests.post(
            f'https://nbi:9999/osm/nslcm/v1/ns_instances/203e09eb-5d6f-443c-bb1f-9ff0fb4d30d9/verticalscale',
            headers=headers, json=update_data, verify=False)
        if verticalscale_up.status_code == 202:
            print("Update realizado com sucesso")

        else:
            print(f"Falha na solicitação. Código de resposta: {verticalscale_up.status_code}")
    return verticalscale_up

# Assume que headers é definido em algum lugar do seu script
verticalscale(df_forecast)
