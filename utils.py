import pandas as pd
import numpy as np


def process_data(bm, avg_temp, max_temp, air, air_avg,
                 yearly=True,
                 pop_zone=True):
  print('cleaning data\n')
  df_bm = process_lumi(bm)
  # print(df_bm.head())
  df_avg_temp = process_temp(avg_temp)
  # print(df_avg_gb.head())
  df_max_temp = process_temp(max_temp)
  # print(df_max_gb.head())

  if yearly:
    if pop_zone:
      merge_gb_cols = ['GID_2', 'POP_ZONE', 'YEAR']
    else:
      merge_gb_cols = ['GID_2', 'YEAR']
  else:
    if pop_zone:
      merge_gb_cols = ['GID_2', 'POP_ZONE', 'YEAR', 'MONTH']
    else:
      merge_gb_cols = ['GID_2', 'YEAR', 'MONTH']

  print('aggregating data\n')
  df_bm = df_bm.groupby(merge_gb_cols)\
               .agg(COUNTRY=('COUNTRY', 'first'),
                    GID_1=('GID_1', 'first'),
                    NAME_1=('NAME_1', 'first'),
                    NAME_2=('NAME_2', 'first'),
                    LUMINOSITY_SUM=('LUMINOSITY_SUM', 'sum'))\
               .reset_index()

  df_avg_gb = df_avg_temp.groupby(merge_gb_cols)\
                         .agg(AVERAGE_TEMPERATURE=('AVERAGE_TEMPERATURE', 'mean'))\
                         .reset_index()

  df_max_gb = df_max_temp.groupby(merge_gb_cols)\
                         .agg(MAX_TEMPERATURE=('MAX_TEMPERATURE', 'max'))\
                         .reset_index()

  print('combining data\n')
  if yearly:
    df_air = process_air(air)
    df_air_gb = df_air.groupby(merge_gb_cols)\
                      .agg(AIR_POLLUTION=('AIR_POLLUTION', 'sum'))\
                      .reset_index()
    df_air_avg = process_air(air_avg)
    df_air_avg = df_air_avg.groupby(merge_gb_cols)\
                           .agg(AIR_POLLUTION_AVG=('AIR_POLLUTION', 'mean'))\
                           .reset_index()

    df_list = [df_avg_gb, df_max_gb, df_air_gb, df_air_avg]
  else:
    df_list = [df_avg_gb, df_max_gb]

  df = df_bm.copy(deep=True)
  for d in df_list:
    df = pd.merge(df, d, on=merge_gb_cols, how='left')

  print('rest of steps')
  df_fin = process_combined(df, yearly=yearly, pop_zone=pop_zone)

  if pop_zone:
    df_fin['POP_ZONE_ENCODE'] = df_fin['POP_ZONE'].replace({'urban': 1,
                                                            'rural': 0})

  return df_fin

def process_lumi(bm):
  df_bm = bm.copy(deep=True)
  df_bm.columns = df_bm.columns.str.upper()
  df_bm = df_bm[(df_bm['YEAR'] != 2022) & (~df_bm['GID_2'].isin(['VNM.PI', 'VNM.SI']))]
  df_bm = df_bm.rename({'COUNTRY_ID': 'GID_0',
                      'PROVINCE': 'NAME_1',
                      'PROVINCE_ID': 'GID_1',
                      'DISTRICT': 'NAME_2',
                      'DISTRICT_ID': 'GID_2',
                      'CLSSFCT': 'POP_ZONE'}, axis=1)
  
  df_bm['POP_ZONE'] = df_bm['POP_ZONE'].replace({'semi-urban': 'urban'})
  
  return df_bm

def process_temp(df):
  df = df[df['year'].between(2014, 2021)]
  df = df[~df['GID_2'].isin(['VNM.PI', 'VNM.SI'])]
  df['month'] = pd.to_datetime(df['month'], format='%B').dt.month.astype(int)
  df.columns = df.columns.str.upper()
  df = df.rename({'CLSSFCT': 'POP_ZONE'}, axis=1)
  df['POP_ZONE'] = df['POP_ZONE'].replace({'semi-urban': 'urban'})

  return df

def process_air(air):
  df_air = air.copy(deep=True)
  df_air.columns = df_air.columns.str.upper()
  df_air = df_air.rename({'ADMIN2': 'GID_2',
                          'CLSSFCT': 'POP_ZONE'}, axis=1)
  df_air['POP_ZONE'] = df_air['POP_ZONE'].replace({'semi-urban': 'urban'})
  
  return df_air

def process_combined(df, yearly=True, pop_zone=True):
  df['LUMINOSITY_SUM'] = df['LUMINOSITY_SUM'].fillna(0)                                            
  df['LUMINOSITY_SUM'] = df['LUMINOSITY_SUM'] + 1                                 
  df['LOG_LUMINOSITY_SUM'] = np.log(df['LUMINOSITY_SUM']) 

  if yearly:
    if pop_zone:
      gb_cols = ['GID_2', 'POP_ZONE']
    else:
      gb_cols = ['GID_2']

    df = df.sort_values(by=gb_cols, ascending=True)
    df['LUMINOSITY_PCT_CHANGE'] = \
                100*(df.groupby(gb_cols)['LUMINOSITY_SUM'].apply(pd.Series.pct_change))
    df['AVG_TEMP_PCT_CHANGE'] = \
                100*(df.groupby(gb_cols)['AVERAGE_TEMPERATURE'].apply(pd.Series.pct_change))
    df['MAX_TEMP_PCT_CHANGE'] = \
                100*(df.groupby(gb_cols)['MAX_TEMPERATURE'].apply(pd.Series.pct_change))
    df['AIR_POLLUTION_PCT_CHANGE'] = \
                100*(df.groupby(gb_cols)['AIR_POLLUTION'].apply(pd.Series.pct_change))
    df['AIR_AVG_PCT_CHANGE'] = \
                100*(df.groupby(gb_cols)['AIR_POLLUTION_AVG'].apply(pd.Series.pct_change)) 
  
  else:
    if pop_zone:
      gb_cols = ['GID_2', 'POP_ZONE', 'YEAR']
    else:
      gb_cols = ['GID_2', 'YEAR']
    
    df = df.sort_values(by=gb_cols, ascending=True)
    df['LUMINOSITY_PCT_CHANGE'] = \
                (df.groupby(gb_cols)['LUMINOSITY_SUM'].apply(pd.Series.pct_change) + 1)
    df['AVG_TEMP_PCT_CHANGE'] = \
                (df.groupby(gb_cols)['AVERAGE_TEMPERATURE'].apply(pd.Series.pct_change) + 1)
    df['MAX_TEMP_PCT_CHANGE'] = \
                (df.groupby(gb_cols)['MAX_TEMPERATURE'].apply(pd.Series.pct_change) + 1)
    
    df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH']].assign(DAY=1)).astype(str)
    df['YEAR_MONTH'] = df['DATE'].str[:4] + df['DATE'].str[5:7]
    df['YEAR_MONTH'] = df['YEAR_MONTH'].astype(int)



  
  return df