import pandas as pd
# import psycopg2

# updated headers
col_redefine = {
          'SEQNUMC': 'child_id',
          'SEQNUMHH': 'house_id',
          'CEN_REG': 'census_region',
          'AGEGRP': 'age_cat',
          'RACEETHK': 'race_ethn',
          'SEX': 'birth_sex',
          'EDUC1': 'mother_edu',
          'MARITAL2': 'mother_marital',
          'INCPOV1': 'poverty_status',
          'INCPORAR': 'income_poverty_ratio',
          'CWIC_01': 'wic_child_ever',
          'CWIC_02': 'wic_child_cur',
          'PDAT': 'good_data',
          'P_NUMVRC': 'mmrv_doses',
          'PROV_FAC': 'provider_site',
          'INS_STAT2_I': 'insur_type',
          'INS_BREAK_I': 'insur_stat'
      }

# update headers and refine list
file = 'nis_child/csv_data/'
df = (pd.read_csv(file)
      .rename(columns=col_redefine))
df = df[list(col_redefine.values())]
print(df.head())

# load into database