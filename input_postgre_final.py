
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
    'slice_id': ['7373b8ab-6861-430f-bd38-563d29e35d74'],
    'service_type': ['eMBB'],
    'ns_id': ['e967f1db-06bd-4ee9-84b8-882b28afe678'],
    'vnf_id': ['b3d8f6f6-3e17-463f-b137-3c28910d3a2d'],
    'vnfd_id': ['94a5eab2-5910-4be5-a508-a8605f1aeeb7'],
    'vdu_id': ['ubuntu_slice-VM_1'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_eMBB = pd.DataFrame(data_eMBB)
print(df_eMBB)

df_eMBB.to_sql('slice_embb_1', con=engine, if_exists='replace', index=False)




data_uRLLC = {
    'slice_id': ['98dfca24-75fe-43dc-b0da-25ef300e1164'],
    'service_type': ['URLLC'],
    'ns_id': ['c94018f2-15fc-4420-b43b-426e47053bfa'],
    'vnf_id': ['4f58e3be-78a8-471c-8337-09dfb6727bc7'],
    'vnfd_id': ['e4e996d9-51af-4cd3-842c-437ef5f24ee9'],
    'vdu_id': ['buntu_slice-VM_2'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_uRLLC = pd.DataFrame(data_uRLLC)
print(df_uRLLC)

df_uRLLC.to_sql('slice_urllc_2', con=engine, if_exists='replace', index=False)




data_mMTC = {
    'slice_id': ['dcfa0503-555e-473a-824c-ba70cfe1a7a9'],
    'service_type': ['mMTC'],
    'ns_id': ['afc93b94-b325-4e99-b031-0112614ec0d7'],
    'vnf_id': ['e751627f-79b3-41c3-b51e-dcf5c6074ad9'],
    'vnfd_id': ['e152158a-1404-422a-a974-c36de9572efa'],
    'vdu_id': ['ubuntu_slice-VM_3'],
    'num_virtual_cpu': ['1'],
    'virtual_memory_size': ['1000'],

}
df_mMTC = pd.DataFrame(data_mMTC)
print(df_mMTC)

df_mMTC.to_sql('slice_mmtc_3', con=engine, if_exists='replace', index=False)



engine.dispose()
