
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
    'slice_id': ['8ff832c8-e6c6-4eb0-b3fc-2b9cf330b7d1'],
    'service_type': ['eMBB'],
    'ns_id': ['427c9595-9432-40c7-b876-79181551af7f'],
    'vnf_id': ['27fea911-254f-4f1c-805b-bf7efb7bc8eb'],
    'vnfd_id': ['94a5eab2-5910-4be5-a508-a8605f1aeeb7'],
    'vdu_id': ['ubuntu_slice-VM_1'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_eMBB = pd.DataFrame(data_eMBB)
print(df_eMBB)

df_eMBB.to_sql('slice_embb_1', con=engine, if_exists='replace', index=False)




data_uRLLC = {
    'slice_id': ['4af3f24c-3c33-4f93-abb1-0edca9e4f4c3'],
    'service_type': ['URLLC'],
    'ns_id': ['05afa55c-fc12-4553-b0f9-6c1df0283416'],
    'vnf_id': ['b4498e7a-4d88-4a01-9507-0c569751084f'],
    'vnfd_id': ['e4e996d9-51af-4cd3-842c-437ef5f24ee9'],
    'vdu_id': ['buntu_slice-VM_2'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_uRLLC = pd.DataFrame(data_uRLLC)
print(df_uRLLC)

df_uRLLC.to_sql('slice_urllc_2', con=engine, if_exists='replace', index=False)




data_mMTC = {
    'slice_id': ['a7ed8693-9cd9-43f5-9bbd-114d4b9d1f00'],
    'service_type': ['mMTC'],
    'ns_id': ['5cab8486-779c-4f0f-a397-563c2eaa9f97'],
    'vnf_id': ['34092c89-d36e-47af-ae6b-933bec9179bf'],
    'vnfd_id': ['e152158a-1404-422a-a974-c36de9572efa'],
    'vdu_id': ['ubuntu_slice-VM_3'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_mMTC = pd.DataFrame(data_mMTC)
print(df_mMTC)

df_mMTC.to_sql('slice_mmtc_3', con=engine, if_exists='replace', index=False)



engine.dispose()
