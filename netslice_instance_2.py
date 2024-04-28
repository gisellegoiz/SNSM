import requests
import warnings
import pprint
import yaml

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


def fetch_slices_and_extract_nsr_refs():
    slice_url = f"https://nbi:9999/osm/nsilcm/v1/netslice_instances"
    response_slice = requests.get(slice_url, headers=headers, verify=False)
    nsr_refs = []

    if response_slice.status_code == 200:
        slices = response_slice.json()
        for slice in slices:
            template = slice.get('network-slice-template', {})
            snssai_identifier = template.get('SNSSAI-identifier', {})
            slice_service_type = snssai_identifier.get('slice-service-type', 'Not specified')
            print(f"Network_Slice_Name: {slice.get('name', 'No Name')} - ID: {slice.get('id', 'Unknown ID')} - Service_Type: {slice_service_type} ")
            if 'nsr-ref-list' in slice:
                for nsr in slice['nsr-ref-list']:
                    nsr_ref = nsr.get('nsr-ref')
                    if nsr_ref:
                        nsr_refs.append(nsr_ref)
                        #print(f"  NSR Ref: {nsr_ref}")



                        def fetch_vnfr_refs_from_ns(nsr_refs):
                            base_url = "https://nbi:9999/osm/nslcm/v1/ns_instances/"
                            for nsr_ref in nsr_refs:
                                url = f"{base_url}/{nsr_ref}"
                                response_ns = requests.get(url, headers=headers, verify=False)
                                if response_ns.status_code == 200:
                                    ns_details = response_ns.json()
                                    constituent_vnfr_refs = ns_details.get('constituent-vnfr-ref',
                                                                           [])  # Extrai referências das VNFs
                                    print(f"NS_Instances_ID: {nsr_ref}, VNF_Instance_ID: {constituent_vnfr_refs}")
                                else:
                                    print(
                                        f"Failed to retrieve details for NSR Ref {nsr_ref}. Status code: {response_ns.status_code}")



                        fetch_vnfr_refs_from_ns(nsr_refs)


fetch_slices_and_extract_nsr_refs()
