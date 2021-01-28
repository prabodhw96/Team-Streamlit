import numpy as np
import pandas as pd
import streamlit as st
import datetime
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from src.pages.predict import predict

import awesome_streamlit as ast

@st.cache(persist=True)
def load_data():
	data = pd.read_csv("src/data/casesanddeaths.csv", parse_dates=["Date"])
	return data

def create_ip(selected_country, c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6):
	data = load_data()
	cols = ["CountryName", "RegionName", "GeoID", "Date", "NewCases", "C1_School closing", "C2_Workplace closing", 
	"C3_Cancel public events", "C4_Restrictions on gatherings", "C5_Close public transport", 
	"C6_Stay at home requirements", "C7_Restrictions on internal movement", "C8_International travel controls", 
	"H1_Public information campaigns", "H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings"]
	ip = pd.DataFrame(columns=cols)
	for i in range(1,31):
		val = {}
		val["CountryName"] = selected_country
		val["RegionName"] = np.nan
		val["GeoID"] = selected_country + "__nan"
		val["Date"] = data["Date"].max() + datetime.timedelta(days=i)
		val["NewCases"] = np.nan
		val["C1_School closing"] = c1
		val["C2_Workplace closing"] = c2
		val["C3_Cancel public events"] = c3
		val["C4_Restrictions on gatherings"] = c4
		val["C5_Close public transport"] = c5
		val["C6_Stay at home requirements"] = c6
		val["C7_Restrictions on internal movement"] = c7
		val["C8_International travel controls"] = c8
		val["H1_Public information campaigns"] = h1
		val["H2_Testing policy"] = h2
		val["H3_Contact tracing"] = h3
		val["H6_Facial Coverings"] = h6
		ip = ip.append(pd.Series(val, name='i'))
	ip = ip.sort_values(by="CountryName").reset_index(drop=True)
	return ip

def write():
	start = time.time()
	st.markdown("## Predict cases by prescribing stringency of containment and closure policies")

	npi_dict = {}
	npi_dict["None"] = 0
	npi_dict["Medium"] = 1
	npi_dict["Hard"] = 2
	npi_dict["Strict"] = 3

	vals = ("None", "Medium", "Hard", "Strict")

	npi_dict_v2 = {}
	npi_dict_v2["None"] = 0
	npi_dict_v2["Medium"] = 1
	npi_dict_v2["Medium-Hard"] = 2
	npi_dict_v2["Hard"] = 3
	npi_dict_v2["Strict"] = 4

	vals_v2 = ("None", "Medium", "Medium-Hard", "Hard", "Strict")

	col1, col2, col3 = st.beta_columns(3)
	col4, col5, col6 = st.beta_columns(3)
	col7, col8, col9 = st.beta_columns(3)
	col10, col11, col12 = st.beta_columns(3)
	with col1:
		c1 = st.selectbox("C1_School closing", vals, key='c1')
		#c1 = st.radio("C1_School closing", vals, key='c1')
		#c1 = st.selectbox("C1_School closing", np.arange(0,4,1), key='c1')
	with col2:
		c2 = st.selectbox("C2_Workplace closing", vals, key='c2')
		#c2 = st.radio("C2_Workplace closing", vals, key='c2')
		#c2 = st.selectbox("C2_Workplace closing", np.arange(0,4,1), key='c2')
	with col3:
		c3 = st.selectbox("C3_Cancel public events", vals[:-1], key='c3')
		#c3 = st.radio("C3_Cancel public events", vals[:-1], key='c3')
		#c3 = st.selectbox("C3_Cancel public events", np.arange(0,3,1), key='c3')
	with col4:
		c4 = st.selectbox("C4_Restrictions on gatherings", vals_v2, key='c4')
		#c4 = st.radio("C4_Restrictions on gatherings", vals, key='c4')
		#c4 = st.selectbox("C4_Restrictions on gatherings", np.arange(0,5,1), key='c4')
	with col5:
		c5 = st.selectbox("C5_Close public transport", vals[:-1], key='c5')
		#c5 = st.radio("C5_Close public transport", vals[:-1], key='c5')
		#c5 = st.selectbox("C5_Close public transport", np.arange(0,3,1), key='c5')
	with col6:
		c6 = st.selectbox("C6_Stay at home requirements", vals, key='c6')
		#c6 = st.radio("C6_Stay at home requirements", vals, key='c6')
		#c6 = st.selectbox("C6_Stay at home requirements", np.arange(0,4,1), key='c6')
	with col7:
		c7 = st.selectbox("C7_Restrictions on internal movement", vals[:-1], key='c7')
		#c7 = st.radio("C7_Restrictions on internal movement", vals, key='c7')
		#c7 = st.selectbox("C7_Restrictions on internal movement", np.arange(0,3,1), key='c7')
	with col8:
		c8 = st.selectbox("C8_International travel controls", vals_v2, key='c8')
		#c8 = st.radio("C8_International travel controls", vals, key='c8')
		#c8 = st.selectbox("C8_International travel controls", np.arange(0,5,1), key='c8')
	with col9:
		h1 = st.selectbox("H1_Public information campaigns", vals[:-1], key='h1')
		#h1 = st.radio("H1_Public information campaigns", vals[:-1], key='h1')
		#h1 = st.selectbox("H1_Public information campaigns", np.arange(0,3,1), key='h1')
	with col10:
		h2 = st.selectbox("H2_Testing policy", vals, key='h2')
		#h2 = st.radio("H2_Testing policy", vals, key='h2')
		#h2 = st.selectbox("H2_Testing policy", np.arange(0,4,1), key='h2')
	with col11:
		h3 = st.selectbox("H3_Contact tracing", vals[:-1], key='h3')
		#h3 = st.radio("H3_Contact tracing", vals[:-1], key='h3')
		#h3 = st.selectbox("H3_Contact tracing", np.arange(0,3,1), key='h3')
	with col12:
		h6 = st.selectbox("H6_Facial Coverings", vals_v2, key='h6')
		#h6 = st.radio("H6_Facial Coverings", vals, key='h6')
		#h6 = st.selectbox("H6_Facial Coverings", np.arange(0,5,1), key='h6')

	st.markdown("### Select countries")
	data = load_data()
	countries = list(data["CountryName"].unique())
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country')

	if st.button("Submit", False):
		ip = create_ip(selected_country,
						npi_dict[c1],
						npi_dict[c2],
						npi_dict[c3],
						npi_dict_v2[c4],
						npi_dict[c5],
						npi_dict[c6],
						npi_dict[c7],
						npi_dict_v2[c8],
						npi_dict[h1],
						npi_dict[h2],
						npi_dict[h3],
						npi_dict_v2[h6])
		pred = predict(ip)
		df = data[data["CountryName"]==selected_country].reset_index(drop=True)
		df = df[["CountryName", "Date", "ConfirmedCases", "ConfirmedDeaths", "DailyNewCases", "DailyNewDeaths"]]
		t = pred.copy()
		t = t[["CountryName", "Date", "PredictedDailyTotalCases", "PredictedDailyTotalDeaths", "PredictedDailyNewCases", "PredictedDailyNewDeaths"]]
		t.rename(columns={"PredictedDailyTotalCases":"ConfirmedCases",
			"PredictedDailyTotalDeaths":"ConfirmedDeaths",
			"PredictedDailyNewCases":"DailyNewCases",
			"PredictedDailyNewDeaths":"DailyNewDeaths"}, inplace=True)
		t = t.round()
		dfn = pd.concat([df, t])
		dfn = dfn.tail(120).reset_index(drop=True) #dfn[334:].reset_index(drop=True)

		dfn1 = dfn[dfn["Date"] < pred["Date"].min()].reset_index(drop=True)
		dfn2 = dfn[dfn["Date"] >= pred["Date"].min()].reset_index(drop=True)
		fig = make_subplots(rows=1, cols=1, subplot_titles=["Daily New Cases - "+str(selected_country)])
		fig.add_trace(go.Scatter(x=dfn1["Date"], y=dfn1["DailyNewCases"], 
			name="Ground Truth", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1)
		fig.add_trace(go.Scatter(x=dfn2["Date"], y=dfn2["DailyNewCases"], name="Predicted", 
			mode='lines', line={'color':'#636efa'}), row=1, col=1)
		st.plotly_chart(fig)

		#fig = px.line(dfn, x="Date", y="DailyNewCases")
		#st.plotly_chart(fig)
		#fig = px.line(dfn, x="Date", y="DailyNewDeaths")
		#st.plotly_chart(fig)

		#dfn1 = dfn[dfn["Date"] < pred["Date"].min()].reset_index(drop=True)
		#dfn2 = dfn[dfn["Date"] >= pred["Date"].min()].reset_index(drop=True)

		#fig = make_subplots(rows=2, cols=1, subplot_titles=["Daily New Cases", "Daily New Deaths"])
		#fig.add_trace(go.Scatter(x=dfn1["Date"], y=dfn1["DailyNewCases"], 
		#	name="Ground Truth (Cases)", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1)
		#fig.add_trace(go.Scatter(x=dfn2["Date"], y=dfn2["DailyNewCases"], name="Predicted (Cases)", 
		#	mode='lines', line={'color':'#636efa'}), row=1, col=1)
		#fig.add_trace(go.Scatter(x=dfn1["Date"], y=dfn1["DailyNewDeaths"], name="Ground Truth (Deaths)", 
		#	mode='lines', line={'dash': 'dash', 'width':3, 'color':'#ed6d59'}), row=2, col=1)
		#fig.add_trace(go.Scatter(x=dfn2["Date"], y=dfn2["DailyNewDeaths"], name="Predicted (Deaths)", 
		#	mode='lines', line={'color':'#ab63fa'}), row=2, col=1)
		#fig.update_layout(height=700, width=700)
		#st.plotly_chart(fig)
		
		#fig = make_subplots(rows=2, cols=1)
		#fig.add_trace(go.Scatter(x=dfn["Date"], y=dfn["DailyNewCases"], name="Daily New Cases"), row=1, col=1)
		#fig.add_trace(go.Scatter(x=dfn["Date"], y=dfn["DailyNewDeaths"], name="Daily New Deaths"), row=2, col=1)
		#fig.update_layout(height=700, width=700)
		#st.plotly_chart(fig)
		#st.write(pred.drop(columns=["RegionName", "GeoID"]).round())

		end = time.time()
		st.write(round(end-start, 2), "seconds")