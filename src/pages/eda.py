import streamlit as st
import numpy as np
import pandas as pd
import datetime
import plotly.express as px
import pydeck as pdk
import folium
from streamlit_folium import folium_static

import awesome_streamlit as ast

@st.cache(persist=True)
def load_data():
	data = pd.read_csv("src/data/casesanddeaths.csv", parse_dates=["Date"])
	return data

@st.cache(persist=True)
def load_pop_data():
	data = pd.read_csv("src/data/population.csv")
	return data

def write():
	#with st.spinner("Loading Exploratory Data Analsysis..."):
	st.markdown("## Cases - Exploratory Data Analsysis")
	data = load_data()
	stat = st.sidebar.selectbox("Select statistics to display", list(data.columns[4:]), key='stat')

	pop_data = load_pop_data()
	pop = st.sidebar.slider("Show countries with at least ... million inhabitants", 0, 100, key='pop')
	pop *= 1000000
	countries = list(pop_data[pop_data["Population"]>=pop]["CountryName"])
	selected_countries = st.multiselect("Select countries to plot", countries, key='selected_countries')

	if len(selected_countries) > 0:
		df = data[data["CountryName"].isin(selected_countries)].reset_index(drop=True)
	else:
		df = data[data["CountryName"].isin(countries)].reset_index(drop=True)

	#df = data[data["CountryName"].isin(countries)].reset_index(drop=True)

	if stat.startswith("Conf"):
		zx = st.sidebar.slider("No. of cases to observe from", 0, 20000, key='zx')

		fig = px.line(df[df[stat] >= zx].reset_index(drop=True), 
			x="Date", y=stat, color="CountryName", line_group="CountryName")
		st.write(fig)
	else:
		date = st.sidebar.date_input('start date', datetime.date(2020,1,23), key='date')
		if date < df["Date"].min():
			st.markdown("*Invalid date selected.* Setting it to 23/01/2020...")
			date = "2020-01-23"
		elif date > df["Date"].max():
			st.markdown("*Invalid date selected.* Setting it to 22/12/2020...")
			date = "2020-12-22"

		fig = px.line(df[df["Date"]>=str(date)].reset_index(drop=True), 
			x="Date", y=stat, color="CountryName", line_group="CountryName")
		st.write(fig)

	st.markdown("Source: [OxCGRT_latest.csv] (https://github.com/OxCGRT/covid-policy-tracker/blob/master/data/OxCGRT_latest.csv)&nbsp;\
		[Additional_Context_Data_Global.csv] (https://github.com/leaf-ai/covid-xprize/blob/master/covid_xprize/examples/predictors/lstm/data/Additional_Context_Data_Global.csv)")

	if st.checkbox("Show experimental (noqa)", False):
		st.markdown("### Flight traffic - pairwise data (TODO)")
		ftdf = pd.read_json("src/data/flights.json")
		ftdf["from_name"] = ftdf["from"].apply(lambda f: f["name"])
		ftdf["to_name"] = ftdf["to"].apply(lambda t: t["name"])

		layer = pdk.Layer(
		    "GreatCircleLayer",
		    ftdf,
		    pickable=True,
		    get_stroke_width=12,
		    get_source_position="from.coordinates",
		    get_target_position="to.coordinates",
		    get_source_color=[64, 255, 0],
		    get_target_color=[0, 128, 200],
		    auto_highlight=True,
		)

		view_state = pdk.ViewState(latitude=50, longitude=-40, zoom=1, bearing=0, pitch=0)
		r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{from_name} to {to_name}"},)
		r.picking_radius = 10
		st.write(r)