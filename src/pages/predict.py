import numpy as np
import pandas as pd
import pickle
import streamlit as st

from src.pages.predictor.tempgeolstm_predictor import tempGeoLSTMPredictor
from src.pages.predictor.tempgeolgbm_predictor import tempGeoLGBMPredictor

import awesome_streamlit as ast
import base64
ALPHA = 0.50

MODEL_WEIGHTS_FILE = "src/models/model_alldata.h5"
MODEL_FILE = "src/models/model_alldata.pkl"
DATA_FILE = "src/data/OxCGRT_latest.csv"
TEMPERATURE_DATA_FILE = "src/data/temperature_data.csv"
NPI_COLUMNS = ['C1_School closing', 'C2_Workplace closing', 'C3_Cancel public events', 'C4_Restrictions on gatherings', 
				'C5_Close public transport', 'C6_Stay at home requirements', 'C7_Restrictions on internal movement', 
				'C8_International travel controls', 'H1_Public information campaigns', 'H2_Testing policy', 
				'H3_Contact tracing', 'H6_Facial Coverings']

def get_predictions(predictor, model, npis_df, start_date_dt, end_date_dt):
	predictor.choose_train_test_split(start_date=start_date_dt, end_date=end_date_dt, update_data=False)
	preds_df = predictor.predict(npis_df, start_date=start_date_dt, end_date=end_date_dt)
	return preds_df

def get_ensemble_pred(alpha, lstm_predictions_df, lgbm_predictions_df):
	ensemble_data = pd.DataFrame()
	ensemble_data['CountryName'] = lstm_predictions_df['CountryName']
	ensemble_data['RegionName'] = lstm_predictions_df['RegionName']
	ensemble_data['GeoID'] = lstm_predictions_df['GeoID']
	ensemble_data['Date'] = lstm_predictions_df['Date']

	ensemble_data['PredictedDailyTotalCases'] = alpha * lstm_predictions_df['PredictedDailyTotalCases'] + (1 - alpha) * lgbm_predictions_df['PredictedDailyTotalCases']
	ensemble_data['PredictedDailyNewCases'] = alpha * lstm_predictions_df['PredictedDailyNewCases'] + (1 - alpha) * lgbm_predictions_df['PredictedDailyNewCases']
	ensemble_data['PredictedDailyTotalDeaths'] = alpha * lstm_predictions_df['PredictedDailyTotalDeaths'] + (1 - alpha) * lgbm_predictions_df['PredictedDailyTotalDeaths']
	ensemble_data['PredictedDailyNewDeaths'] = alpha * lstm_predictions_df['PredictedDailyNewDeaths'] + (1 - alpha) * lgbm_predictions_df['PredictedDailyNewDeaths']

	return ensemble_data
def get_table_download_link(df):
	"""Generates a link allowing the data in a given panda dataframe to be downloaded
	in:  dataframe
	out: href string
	"""
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
	href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
	return href


def predict(npis_df) -> None:
	#npis_df = pd.read_csv(path_to_ips_file, parse_dates=['Date'], encoding="ISO-8859-1", dtype={"RegionName": str, "RegionCode": str}, error_bad_lines=False)
	npis_df["GeoID"] = np.where(npis_df["RegionName"].isnull(), npis_df["CountryName"], npis_df["CountryName"] + ' / ' + npis_df["RegionName"])
	start_date_dt = npis_df["Date"].min()
	end_date_dt = npis_df["Date"].max()
	# for npi_col in NPI_COLUMNS:
	# 	npis_df.update(npis_df.groupby(['CountryName', 'RegionName'])[npi_col].ffill().fillna(0))
	predictors = ["LSTM", "LGBM"]
	for model in predictors:
		if model == "LSTM":
			predictor = tempGeoLSTMPredictor(path_to_model_weights=MODEL_WEIGHTS_FILE, use_embedding=False)
			lstm_predictions_df = get_predictions(predictor, model, npis_df, start_date_dt, end_date_dt)
		elif model == "LGBM":
			predictor = tempGeoLGBMPredictor()
			with open(MODEL_FILE, 'rb') as model_file:
				predictor.predictor = pickle.load(model_file)
			lgbm_predictions_df = get_predictions(predictor, model, npis_df, start_date_dt, end_date_dt)

	ensemble_predictions = get_ensemble_pred(ALPHA, lstm_predictions_df, lgbm_predictions_df)
	return ensemble_predictions