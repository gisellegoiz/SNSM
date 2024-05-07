from sqlalchemy import create_engine
import pandas as pd
from io import StringIO

dbname = 'postgres'
host = 'localhost'
user = 'postgres'
password = '1401'
port = '5432'

postgres_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
cnx = create_engine(postgres_str)

data = {
    'num-virtual-cpu': ['4'],
    'virtual-memory-size': ['2'],
    'vnfd_id': ['83d40159-e8e8-4452-ad8e-391d10f1cb69'],
    'vnf_id': ['d99f8f96-7a65-4786-9371-8da254bbdde8'],
    'ns_id': ['07adf4c2-a446-4b1e-9f71-7da67c748be0'],
    'netslice_id': ['38c7aa24-a1d5-41fa-af3b-729de60682dd'],
    'Service_Type': ['eMBB']

}

df = pd.DataFrame(data)
print(df)


df.to_sql('slice_vm1', con=cnx, if_exists='append', index=False)
