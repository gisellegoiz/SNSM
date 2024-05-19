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
    'slice_id': ['557c6d51-3b04-42e4-bbf5-c836abcc0ea3'],
    'service_type': ['eMBB'],
    'ns_id': ['dc9aeb25-c285-43c4-8560-30fcae1be71b'],
    'vnf_id': ['51cd1af8-56e8-4bc1-8b68-8dc47b228cff,'],
    'vnfd_id': ['936edd48-0ff5-49fc-bcd4-7d2b56415172'],
    'vdu_id': ['ubuntu_slice-VM'],
    'num_virtual_cpu': ['2'],
    'virtual_memory_size': ['2'],


}
df_eMBB = pd.DataFrame(data_eMBB)
print(df_eMBB)

df_eMBB.to_sql('slice_embb', con=engine, if_exists='append', index=False)

engine.dispose()

