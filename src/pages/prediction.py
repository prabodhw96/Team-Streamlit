import numpy as np
import pandas as pd
import streamlit as st
import datetime
import time
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from src.pages.predict import predict
from typing import List, Optional
import random
import base64
import awesome_streamlit as ast

@st.cache(persist=True, allow_output_mutation=True)
def load_data():
	data = pd.read_csv("src/data/casesanddeaths.csv", parse_dates=["Date"])
	return data

@st.cache(persist=True, allow_output_mutation=True)
def load_weights():
	data = pd.read_csv("src/data/weights_today.csv")
	return data

@st.cache(persist=True, allow_output_mutation=True)
def change_in_ip(df, country, date):
	df["Date"] = pd.to_datetime(df["Date"])
	df_country = df[df["CountryName"]==country].reset_index(drop=True)
	df_country = df_country[df_country["Date"] <= pd.to_datetime(date)][-2:].reset_index(drop=True)
	df_country_series = abs(df_country.drop(columns=["CountryName", "Date"]).loc[1] - df_country.drop(columns=["CountryName", "Date"]).loc[0])
	intervention = df_country_series[df_country_series == df_country_series.max()].index[0]
	res = intervention + " changed from "+str(df_country[intervention][0])+" to "+str(df_country[intervention][1])
	return res

@st.cache(persist=True, allow_output_mutation=True)
def load_ip_change():
	data = pd.read_csv("src/data/change_in_ip.csv", parse_dates=["Date"])
	return data

def get_table_download_link(df):
	csv = df.to_csv(index=False)
	b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
	href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
	return href

def create_ip(selected_country, c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6, n_days=30):
	data = load_data()
	cols = ["CountryName", "RegionName", "GeoID", "Date", "NewCases", "C1_School closing", "C2_Workplace closing", 
	"C3_Cancel public events", "C4_Restrictions on gatherings", "C5_Close public transport", 
	"C6_Stay at home requirements", "C7_Restrictions on internal movement", "C8_International travel controls", 
	"H1_Public information campaigns", "H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings"]
	ip = pd.DataFrame(columns=cols)
	for i in range(1,n_days+1):
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
	st.markdown(f"""<style>
		.reportview-container .main .block-container{{
		padding-top: 0em;
		max-width: 900px;
		}}</style>""", unsafe_allow_html=True)

	cip = load_ip_change()
	start = time.time()
	st.markdown("<h1 style='text-align: center;'>Prediction - Phase 1</h1>", unsafe_allow_html=True)
	st.write("This dashboard allows the user to visualize the forecasts made by the predictor we had developed for Phase 1 of this competition.")
	st.write("1. Select the country from the drop down list.")
	st.write("2. Enter the number of days we wish to forecast into the future.")
	st.write("3. Enter the currrent intervention plan in effect.")
	st.write("4. Click on Submit. ")
	st.markdown("### Select country")
	data = load_data()
	countries = list(data.sort_values(by="ConfirmedCases", ascending=False)["CountryName"].unique())
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country')
	col0, colx, coly = st.beta_columns(3)
	with col0:
		n_days = st.number_input("Enter no. of days", 30, 90, value=30)

	weights = load_weights()

	fourvals = [0, 1, 2, 3]
	threevals = [0, 1, 2]
	fivevals = [0, 1, 2, 3, 4]

	col1, cx1, col2, cx2, col3 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col4, cx4, col5, cx5, col6 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col7, cx7, col8, cx8, col9 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col10, cx10, col11, cx11, col12 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])

	with col1:
		c1_val = int(weights[weights["CountryName"]==selected_country]["C1_School closing"].reset_index(drop=True)[0])
		c1 = st.select_slider("C1_School closing", fourvals, key='c1_'+selected_country, value=c1_val) #vals
	with col2:
		c2_val = int(weights[weights["CountryName"]==selected_country]["C2_Workplace closing"].reset_index(drop=True)[0])
		c2 = st.select_slider("C2_Workplace closing", fourvals, key='c2_'+selected_country, value=c2_val) #vals
	with col3:
		c3_val = int(weights[weights["CountryName"]==selected_country]["C3_Cancel public events"].reset_index(drop=True)[0])
		c3 = st.select_slider("C3_Cancel public events", threevals, key='c3_'+selected_country, value=c3_val) #vals[:-1]
	with col4:
		c4_val = int(weights[weights["CountryName"]==selected_country]["C4_Restrictions on gatherings"].reset_index(drop=True)[0])
		c4 = st.select_slider("C4_Restrictions on gatherings", fivevals, key='c4_'+selected_country, value=c4_val) #vals_v2
	with col5:
		c5_val = int(weights[weights["CountryName"]==selected_country]["C5_Close public transport"].reset_index(drop=True)[0])
		c5 = st.select_slider("C5_Close public transport", threevals, key='c5_'+selected_country, value=c5_val) #vals[:-1]
	with col6:
		c6_val = int(weights[weights["CountryName"]==selected_country]["C6_Stay at home requirements"].reset_index(drop=True)[0])
		c6 = st.select_slider("C6_Stay at home requirements", fourvals, key='c6_'+selected_country, value=c6_val) #vals
	with col7:
		c7_val = int(weights[weights["CountryName"]==selected_country]["C7_Restrictions on internal movement"].reset_index(drop=True)[0])
		c7 = st.select_slider("C7_Restrictions on internal movement", threevals, key='c7_'+selected_country, value=c7_val) #vals[:-1]
	with col8:
		c8_val = int(weights[weights["CountryName"]==selected_country]["C8_International travel controls"].reset_index(drop=True)[0])
		c8 = st.select_slider("C8_International travel controls", fivevals, key='c8_'+selected_country, value=c8_val) #vals_v2
	with col9:
		h1_val = int(weights[weights["CountryName"]==selected_country]["H1_Public information campaigns"].reset_index(drop=True)[0])
		h1 = st.select_slider("H1_Public information campaigns", threevals, key='h1_'+selected_country, value=h1_val) #vals[:-1]
	with col10:
		h2_val = int(weights[weights["CountryName"]==selected_country]["H2_Testing policy"].reset_index(drop=True)[0])
		h2 = st.select_slider("H2_Testing policy", fourvals, key='h2_'+selected_country, value=h2_val) #vals
	with col11:
		h3_val = int(weights[weights["CountryName"]==selected_country]["H3_Contact tracing"].reset_index(drop=True)[0])
		h3 = st.select_slider("H3_Contact tracing", threevals, key='h3_'+selected_country, value=h3_val) #vals[:-1]
	with col12:
		h6_val = int(weights[weights["CountryName"]==selected_country]["H6_Facial Coverings"].reset_index(drop=True)[0])
		h6 = st.select_slider("H6_Facial Coverings", fivevals, key='h6_'+selected_country, value=h6_val) #vals_v2

	flag = False
	str_ip = str(c1)+str(c2)+str(c3)+str(c4)+str(c5)+str(c6)+str(c7)+str(c8)+str(h1)+str(h2)+str(h3)+str(h6)
	
	if st.button("Submit", False):
		st.write(selected_country)
		st.write("It takes ⏳ ~ {} seconds to run for 30 days".format(10))
		flag = True
		ip = create_ip(selected_country, c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6, n_days)
		#st.write(ip)
		#st.markdown(get_table_download_link(ip), unsafe_allow_html=True)
		pred = predict(ip)
		#st.write(pred)
		#st.markdown(get_table_download_link(pred), unsafe_allow_html=True)
		df = data[data["CountryName"]==selected_country].reset_index(drop=True)
		df = df[["CountryName", "Date", "ConfirmedCases", "ConfirmedDeaths", "DailyNewCases", "DailyNewDeaths"]]
		t = pred.copy()
		t = t[["CountryName", "Date", "PredictedDailyTotalCases", "PredictedDailyTotalDeaths", "PredictedDailyNewCases", "PredictedDailyNewDeaths"]]
		t.rename(columns={"PredictedDailyTotalCases":"ConfirmedCases",
			"PredictedDailyTotalDeaths":"ConfirmedDeaths",
			"PredictedDailyNewCases":"DailyNewCases",
			"PredictedDailyNewDeaths":"DailyNewDeaths"}, inplace=True)
		#t = t.round()
		dfn = pd.concat([df, t])
		dfn = dfn.tail(150+n_days).reset_index(drop=True) #dfn[334:].reset_index(drop=True)
		dfn["DailyNewCasesMA"] = dfn["DailyNewCases"].rolling(7).mean()
		dfn["DailyNewCasesMA"].fillna(dfn["DailyNewCases"], inplace=True)
		dfn["DailyNewCases"] = dfn["DailyNewCasesMA"]

		#dfn.to_csv("src/data/cached_30/cached_30_{}.csv".format(selected_country), index=False)
		#st.write("Saved ", selected_country,"!")
		st.success("Predictions are ready!")
		end = time.time()
		st.write("✔️ Took {} seconds".format(round(end-start, 2)))
		
		dfn1 = dfn[dfn["Date"] < pred["Date"].min()].reset_index(drop=True)
		dfn2 = dfn[dfn["Date"] >= pred["Date"].min()].reset_index(drop=True)

		req_cip = cip[cip["CountryName"]==selected_country].reset_index(drop=True)
		req_cip = req_cip[(req_cip["Date"] >= dfn1["Date"].min()) & (dfn1["Date"] <= dfn1["Date"].max())].reset_index(drop=True)
		req_cip = req_cip.sort_values(by=["Date"]).reset_index(drop=True)
		req_cip["DailyNewCases"] = dfn1[dfn1["Date"].isin(req_cip["Date"])]["DailyNewCases"].reset_index(drop=True)

		fig = make_subplots(rows=1, cols=1, subplot_titles=["Daily New Cases - "+str(selected_country)+" (7 Day Moving Average)"], specs=[[{"secondary_y": True}]])
		fig.add_trace(go.Scatter(x=dfn1["Date"], y=dfn1["DailyNewCases"], 
			name="Ground Truth", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1, secondary_y=False)
		fig.add_trace(go.Scatter(x=dfn2["Date"], y=dfn2["DailyNewCases"], name="Predicted", 
			mode='lines', line={'color':'#636efa'}), row=1, col=1, secondary_y=False)

		fig.update_layout(height=600, width=900)
		fig.update_xaxes(spikesnap="cursor", spikecolor="#999999", spikedash="solid", spikethickness=3)
		fig.update_yaxes(spikesnap="cursor", spikecolor="#999999", spikedash="solid", spikethickness=3)

		fig.add_trace(go.Scatter(x=req_cip["Date"], y=req_cip["DailyNewCases"], mode='markers', name="Changes in IP",
			marker=dict(size=12), hoverinfo="all", hovertext=req_cip["change"]))

		st.plotly_chart(fig)