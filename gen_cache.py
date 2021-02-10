import os
import pandas as pd
from datetime import date
import subprocess

from src.pages.prescriptor.base import add_geo_id, NPI_COLUMNS

N_DAYS = 90

# output file paths
OUTPUT_DIR = './cache'
PRES_OUTPUT = os.path.join(OUTPUT_DIR, 'pres_cache.csv')
PRED_OUR_IP_OUTPUT = os.path.join(OUTPUT_DIR, 'pred_our_ipX_cache.csv')
PRED_CONST_IP_OUTPUT = os.path.join(OUTPUT_DIR, 'pred_const_ip_cache.csv')

# prescription and prediction scripts
PRESCRIBE_SCRIPT = './src/pages/large_ensemble_prescribe.py'
PREDICT_SCRIPT = './src/pages/standard_predict.py'

# auxiliary inputs
OXFORD_URL = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest.csv'
OXFORD_FILEPATH = './src/data/OxCGRT_latest.csv'
EQUAL_COSTS_FILE = './src/data/fixed_equal_costs.csv'

# auxiliary output (can be deleted after the script finishes)
TMP_IP_FILE = os.path.join(OUTPUT_DIR, 'npi_tmp.csv')

print('Updating Oxford data...')
df = pd.read_csv(OXFORD_URL,
                 parse_dates=['Date'],
                 encoding="ISO-8859-1",
                 dtype={'RegionName': str,
                        'RegionCode': str},
                 error_bad_lines=False)
df.to_csv(OXFORD_FILEPATH)

start_date = pd.to_datetime('today').floor('D') - pd.Timedelta(days=3)
end_date = start_date + pd.Timedelta(days=N_DAYS-1)
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

try:
    os.makedirs(os.path.dirname(TMP_IP_FILE), exist_ok=True)
except:
    pass

cost_df = pd.read_csv(EQUAL_COSTS_FILE)
cost_df = add_geo_id(cost_df)
geos = cost_df['GeoID'].unique()

df = add_geo_id(df)
df = df[df['GeoID'].isin(geos)]
for npi in NPI_COLUMNS:
    df.update(df.groupby('GeoID')[npi].ffill().fillna(0))
npi_df = df[['CountryName', 'RegionName', 'Date']+NPI_COLUMNS]
npi_df.to_csv(TMP_IP_FILE)

print('Generating prescriptions ({} - {})...'.format(start_date_str, end_date_str))
output_str = subprocess.check_output(
    [
            'python', PRESCRIBE_SCRIPT,
            '-s', start_date_str,
            '-e', end_date_str,
            '-c', EQUAL_COSTS_FILE,
            '-ip', TMP_IP_FILE,
            '-o', PRES_OUTPUT
    ],
    stderr=subprocess.STDOUT
)

all_pres = pd.read_csv(PRES_OUTPUT, parse_dates=['Date'])
for ip_idx in all_pres['PrescriptionIndex'].unique():
    pres_df = all_pres[all_pres['PrescriptionIndex'] == ip_idx]
    pres_df.drop(columns=['PrescriptionIndex'])
    pres_df.to_csv(TMP_IP_FILE)
    output_name = PRED_OUR_IP_OUTPUT.replace('X', str(ip_idx))

    print('Generating predictions with intervention plan {}'.format(ip_idx))
    output_str = subprocess.check_output(
        [
            'python', PREDICT_SCRIPT,
            '--start_date', start_date_str,
            '--end_date', end_date_str,
            '--interventions_plan', TMP_IP_FILE,
            '--output_file', output_name
        ],
        stderr=subprocess.STDOUT
    )

# repeat current values of the interventions until end_date
npi_df = npi_df[npi_df['Date'] < start_date]
npi_df = add_geo_id(npi_df)
new_dates = pd.date_range(start=start_date, end=end_date)
geos = npi_df['GeoID'].unique()
for geo in geos:
    country_name = npi_df[npi_df['GeoID'] == geo]['CountryName'].to_list()[0]
    region_name = npi_df[npi_df['GeoID'] == geo]['RegionName'].to_list()[0]
    df_dict = {
        'CountryName': [country_name]*len(new_dates),
        'RegionName': [region_name]*len(new_dates),
        'GeoID': [geo]*len(new_dates),
        'Date': new_dates,
    }
    npi_df = npi_df.append(pd.DataFrame(df_dict)).reset_index(drop=True)
for npi in NPI_COLUMNS:
    npi_df.update(npi_df.groupby('GeoID')[npi].ffill().fillna(0))
npi_df = npi_df.drop(columns=['GeoID'])
npi_df.to_csv(TMP_IP_FILE)

print('Generating predictions with current intervention plan')
output_str = subprocess.check_output(
    [
        'python', PREDICT_SCRIPT,
        '--start_date', start_date_str,
        '--end_date', end_date_str,
        '--interventions_plan', TMP_IP_FILE,
        '--output_file', PRED_CONST_IP_OUTPUT
    ],
    stderr=subprocess.STDOUT
)
