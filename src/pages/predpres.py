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
def load_leader_data():
	data = pd.read_csv("src/data/leaders.csv", parse_dates=["Date"])
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

init_str = "322412232314"

def write():
	leaders = load_leader_data()
	lc = list(leaders["CountryName"].unique())
	start = time.time()
	st.markdown("# Prescription of stringencies to predict the new cases")

	st.markdown("### Select country")
	data = load_data()
	countries = list(data.sort_values(by="ConfirmedCases", ascending=False)["CountryName"].unique())
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country')

	weights = load_weights()

	fourvals = [0, 1, 2, 3]
	threevals = [0, 1, 2]
	fivevals = [0, 1, 2, 3, 4]

	col1, col2, col3 = st.beta_columns(3)
	col4, col5, col6 = st.beta_columns(3)
	col7, col8, col9 = st.beta_columns(3)
	col10, col11, col12 = st.beta_columns(3)

	with col1:
		c1 = st.select_slider("C1_School closing", fourvals, key='c1',
									value=weights[weights["CountryName"]==selected_country]["C1_School closing"].reset_index(drop=True)[0]) #vals
	with col2:
		c2 = st.select_slider("C2_Workplace closing", fourvals, key='c2',
									value=weights[weights["CountryName"]==selected_country]["C2_Workplace closing"].reset_index(drop=True)[0]) #vals
	with col3:
		c3 = st.select_slider("C3_Cancel public events", threevals, key='c3',
									value=weights[weights["CountryName"]==selected_country]["C3_Cancel public events"].reset_index(drop=True)[0]) #vals[:-1]
	with col4:
		c4 = st.select_slider("C4_Restrictions on gatherings", fivevals, key='c4',
									value=weights[weights["CountryName"]==selected_country]["C4_Restrictions on gatherings"].reset_index(drop=True)[0]) #vals_v2
	with col5:
		c5 = st.select_slider("C5_Close public transport", threevals, key='c5',
									value=weights[weights["CountryName"]==selected_country]["C5_Close public transport"].reset_index(drop=True)[0]) #vals[:-1]
	with col6:
		c6 = st.select_slider("C6_Stay at home requirements", fourvals, key='c6',
									value=weights[weights["CountryName"]==selected_country]["C6_Stay at home requirements"].reset_index(drop=True)[0]) #vals
	with col7:
		c7 = st.select_slider("C7_Restrictions on internal movement", threevals, key='c7',
									value=weights[weights["CountryName"]==selected_country]["C7_Restrictions on internal movement"].reset_index(drop=True)[0]) #vals[:-1]
	with col8:
		c8 = st.select_slider("C8_International travel controls", fivevals, key='c8',
									value=weights[weights["CountryName"]==selected_country]["C8_International travel controls"].reset_index(drop=True)[0]) #vals_v2
	with col9:
		h1 = st.select_slider("H1_Public information campaigns", threevals, key='h1',
									value=weights[weights["CountryName"]==selected_country]["H1_Public information campaigns"].reset_index(drop=True)[0]) #vals[:-1]
	with col10:
		h2 = st.select_slider("H2_Testing policy", fourvals, key='h2',
									value=weights[weights["CountryName"]==selected_country]["H2_Testing policy"].reset_index(drop=True)[0]) #vals
	with col11:
		h3 = st.select_slider("H3_Contact tracing", threevals, key='h3',
									value=weights[weights["CountryName"]==selected_country]["H3_Contact tracing"].reset_index(drop=True)[0]) #vals[:-1]
	with col12:
		h6 = st.select_slider("H6_Facial Coverings", fivevals, key='h6',
									value=weights[weights["CountryName"]==selected_country]["H6_Facial Coverings"].reset_index(drop=True)[0]) #vals_v2

	flag = False
	str_ip = str(c1)+str(c2)+str(c3)+str(c4)+str(c5)+str(c6)+str(c7)+str(c8)+str(h1)+str(h2)+str(h3)+str(h6)

	if st.button("Submit", False):
		flag = True
		ip = create_ip(selected_country, c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6)
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
		#dfn.to_csv("us_df.csv", index=False)
		#st.write("Saved!")
		
		dfn1 = dfn[dfn["Date"] < pred["Date"].min()].reset_index(drop=True)
		dfn2 = dfn[dfn["Date"] >= pred["Date"].min()].reset_index(drop=True)
		fig = make_subplots(rows=1, cols=1, subplot_titles=["Daily New Cases - "+str(selected_country)], specs=[[{"secondary_y": True}]])
		fig.add_trace(go.Scatter(x=dfn1["Date"], y=dfn1["DailyNewCases"], 
			name="Ground Truth", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1, secondary_y=False)
		fig.add_trace(go.Scatter(x=dfn2["Date"], y=dfn2["DailyNewCases"], name="Predicted", 
			mode='lines', line={'color':'#636efa'}), row=1, col=1, secondary_y=False)
		#if selected_country in lc:
		#	df3 = leaders[leaders["CountryName"]==selected_country].reset_index(drop=True)
		#	df3 = df3[df3["Date"]>=dfn["Date"].min()].reset_index(drop=True)
		#	fig.add_trace(go.Scatter(x=df3["Date"], y=df3["approval"], name=list(df3["Name"].unique())[0]),
		#		secondary_y=True)
			#fig.update_yaxes(range=[40,85], secondary_y=True)
		fig.update_layout(height=500, width=800)
		st.plotly_chart(fig)

		if selected_country in lc:
			df_ = leaders[leaders["CountryName"]==selected_country].reset_index(drop=True)
			leader_name = list(df_["Name"].unique())[0]
			fig1 = make_subplots(rows=1, cols=1, subplot_titles=["Popular support amid COVID-19"], specs=[[{"secondary_y": True}]])
			fig1.add_trace(go.Scatter(x=df["Date"], y=df["DailyNewCases"], 
			name="Daily New Cases", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1, secondary_y=False)
			fig1.add_trace(go.Scatter(x=df_["Date"], y=df_["approval"], name="Popular support", line={'color':'#00cc96'}), secondary_y=True)
			fig1.update_layout(height=500, width=800)
			st.plotly_chart(fig1)

		end = time.time()
		st.write(round(end-start, 2), "seconds")

	if selected_country == "United States" and str_ip == init_str and flag==False:
		us_df = pd.read_csv("us_df.csv")
		us_df1 = us_df.head(us_df.shape[0] - 30).reset_index(drop=True)
		us_df2 = us_df.tail(30).reset_index(drop=True)
		fig_us = make_subplots(rows=1, cols=1, subplot_titles=["Daily New Cases - "+str(selected_country)], specs=[[{"secondary_y": True}]])
		fig_us.add_trace(go.Scatter(x=us_df1["Date"], y=us_df1["DailyNewCases"], 
			name="Ground Truth", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1, secondary_y=False)
		fig_us.add_trace(go.Scatter(x=us_df2["Date"], y=us_df2["DailyNewCases"], name="Predicted", 
			mode='lines', line={'color':'#636efa'}), row=1, col=1, secondary_y=False)
		fig_us.update_layout(height=500, width=800)
		st.plotly_chart(fig_us)

		dfw = data[data["CountryName"]=="United States"].reset_index(drop=True)
		dfw = dfw[["CountryName", "Date", "ConfirmedCases", "ConfirmedDeaths", "DailyNewCases", "DailyNewDeaths"]]

		df_1 = leaders[leaders["CountryName"]=="United States"].reset_index(drop=True)
		leader_name1 = list(df_1["Name"].unique())[0]
		fig2 = make_subplots(rows=1, cols=1, subplot_titles=["Popular support amid COVID-19"], specs=[[{"secondary_y": True}]])
		fig2.add_trace(go.Scatter(x=dfw["Date"], y=dfw["DailyNewCases"], 
		name="Daily New Cases", mode='lines', line={'dash': 'dash', 'width':3, 'color':'orange'}), row=1, col=1, secondary_y=False)
		fig2.add_trace(go.Scatter(x=df_1["Date"], y=df_1["approval"], name="Popular support", line={'color':'#00cc96'}), secondary_y=True)
		fig2.update_layout(height=500, width=800)
		st.plotly_chart(fig2)