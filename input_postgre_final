
from sqlalchemy import create_engine
import pandas as pd
from io import StringIO

dbname = 'postgres'
host = '192.168.1.21'
user = 'postgres'
password = '1401'
port = '5432'

postgres_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(postgres_str)

data_eMBB = {
    'slice_id': ['4d321e63-9f9d-47b9-96cb-066b1bda1835'],
    'service_type': ['eMBB'],
    'ns_id': ['03b855bc-75c0-4726-b237-3113e04d94c6'],
    'vnf_id': ['f8129428-403f-4dca-9354-25a317c88ce1'],
    'vnfd_id': ['94a5eab2-5910-4be5-a508-a8605f1aeeb7'],
    'vdu_id': ['ubuntu_slice-VM_1'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_eMBB = pd.DataFrame(data_eMBB)
print(df_eMBB)

df_eMBB.to_sql('slice_embb_1', con=engine, if_exists='replace', index=False)




data_uRRLC = {
    'slice_id': ['bb9f0585-5bc4-4ed4-85b1-bfe9888421e2'],
    'service_type': ['URRLC'],
    'ns_id': ['ced1e226-1bdf-408f-8ead-50628653ce24'],
    'vnf_id': ['17e0e972-5c92-4914-8ee5-c13bc3e462b5'],
    'vnfd_id': ['e4e996d9-51af-4cd3-842c-437ef5f24ee9'],
    'vdu_id': ['buntu_slice-VM_2'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_uRRLC = pd.DataFrame(data_uRRLC)
print(df_uRRLC)

df_uRRLC.to_sql('slice_urrlc_2', con=engine, if_exists='replace', index=False)




data_mMTC = {
    'slice_id': ['29a36a25-3083-44a5-a987-3ee3b5a1f859'],
    'service_type': ['mMTC'],
    'ns_id': ['819826ae-a082-438c-a916-e7401463c790'],
    'vnf_id': ['6b0f3d41-1ad0-49c5-aa5c-f04f14415fdd'],
    'vnfd_id': ['e152158a-1404-422a-a974-c36de9572efa'],
    'vdu_id': ['ubuntu_slice-VM_3'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_mMTC = pd.DataFrame(data_mMTC)
print(df_mMTC)

df_mMTC.to_sql('slice_mmtc_3', con=engine, if_exists='replace', index=False)



engine.dispose()
