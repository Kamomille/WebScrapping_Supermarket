import pandas as pd

import auchan_fonction_graph as auchan
import casino_fonction_graph as casi



df_merge = auchan.create_csv_merge(True)
df, list_name_csv_clean = auchan.cleaning_data(df_merge)
df = df.reset_index()
df['magasin'] = df.apply(lambda row: 'auchan', axis=1)


df_merge_c = casi.create_csv_merge(True)
df_c, list_name_csv_clean_c = casi.cleaning_data(df_merge_c)
df_c = df_c.reset_index()
df_c['magasin'] = df_c.apply(lambda row: 'casino', axis=1)

df = pd.concat([df, df_c], sort=False)

df.to_csv("TEST_MERGE.csv", sep=';')

