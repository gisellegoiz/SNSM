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
    'slice_id': ['bb5e3eed-9fd7-491b-a49d-f5ed58b8f460'],
    'service_type': ['eMBB'],
    'ns_id': ['203e09eb-5d6f-443c-bb1f-9ff0fb4d30d9'],
    'vnf_id': ['be8de8c3-73f4-43ba-a3ce-a5f7dcef9512'],
    'vnfd_id': ['83d40159-e8e8-4452-ad8e-391d10f1cb69'],
    'vdu_id': ['ubuntu_slice-VM'],
    'num-virtual-cpu': ['4'],
    'virtual-memory-size': ['2'],


}
df_eMBB = pd.DataFrame(data_eMBB)
print(df_eMBB)

df_eMBB.to_sql('slice_embb', con=engine, if_exists='append', index=False)

engine.dispose()

