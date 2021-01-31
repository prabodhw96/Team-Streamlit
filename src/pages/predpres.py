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

@st.cache(persist=True)
def load_weights():
	data = pd.read_csv("src/data/weights_today.csv")
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
	st.markdown("# Prediction of cases from prescription of stringencies")

	st.markdown("### Select country")
	data = load_data()
	countries = list(data.sort_values(by="ConfirmedCases", ascending=False)["CountryName"].unique())
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country')

	weights = load_weights()

	fourvals = [0, 0.33, 0.67, 1]
	threevals = [0, 0.5, 1]
	fivevals = [0, 0.25, 0.5, 0.75, 1]

	c1 = st.sidebar.select_slider("C1_School closing", fourvals, key='c1',
								value=weights[weights["CountryName"]==selected_country]["C1_School closing"].reset_index(drop=True)[0]) #vals
	c2 = st.sidebar.select_slider("C2_Workplace closing", fourvals, key='c2',
								value=weights[weights["CountryName"]==selected_country]["C2_Workplace closing"].reset_index(drop=True)[0]) #vals
	c3 = st.sidebar.select_slider("C3_Cancel public events", threevals, key='c3',
								value=weights[weights["CountryName"]==selected_country]["C3_Cancel public events"].reset_index(drop=True)[0]) #vals[:-1]
	c4 = st.sidebar.select_slider("C4_Restrictions on gatherings", fivevals, key='c4',
								value=weights[weights["CountryName"]==selected_country]["C4_Restrictions on gatherings"].reset_index(drop=True)[0]) #vals_v2
	c5 = st.sidebar.select_slider("C5_Close public transport", threevals, key='c5',
								value=weights[weights["CountryName"]==selected_country]["C5_Close public transport"].reset_index(drop=True)[0]) #vals[:-1]
	c6 = st.sidebar.select_slider("C6_Stay at home requirements", fourvals, key='c6',
								value=weights[weights["CountryName"]==selected_country]["C6_Stay at home requirements"].reset_index(drop=True)[0]) #vals
	c7 = st.sidebar.select_slider("C7_Restrictions on internal movement", threevals, key='c7',
								value=weights[weights["CountryName"]==selected_country]["C7_Restrictions on internal movement"].reset_index(drop=True)[0]) #vals[:-1]
	c8 = st.sidebar.select_slider("C8_International travel controls", fivevals, key='c8',
								value=weights[weights["CountryName"]==selected_country]["C8_International travel controls"].reset_index(drop=True)[0]) #vals_v2
	h1 = st.sidebar.select_slider("H1_Public information campaigns", threevals, key='h1',
								value=weights[weights["CountryName"]==selected_country]["H1_Public information campaigns"].reset_index(drop=True)[0]) #vals[:-1]
	h2 = st.sidebar.select_slider("H2_Testing policy", fourvals, key='h2',
								value=weights[weights["CountryName"]==selected_country]["H2_Testing policy"].reset_index(drop=True)[0]) #vals
	h3 = st.sidebar.select_slider("H3_Contact tracing", threevals, key='h3',
								value=weights[weights["CountryName"]==selected_country]["H3_Contact tracing"].reset_index(drop=True)[0]) #vals[:-1]
	h6 = st.sidebar.select_slider("H6_Facial Coverings", fivevals, key='h6',
								value=weights[weights["CountryName"]==selected_country]["H6_Facial Coverings"].reset_index(drop=True)[0]) #vals_v2

	if st.button("Submit", False):
		ip = create_ip(selected_country, fourvals.index(c1), fourvals.index(c2), threevals.index(c3), fivevals.index(c4),
			threevals.index(c5), fourvals.index(c6), threevals.index(c7), fivevals.index(c8), threevals.index(h1),
			fourvals.index(h2), threevals.index(h3), fivevals.index(h6))
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
		fig.update_layout(height=500, width=750)
		st.plotly_chart(fig)

		end = time.time()
		st.write(round(end-start, 2), "seconds")