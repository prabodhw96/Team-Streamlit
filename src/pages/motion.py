import streamlit as st
import numpy as np
import pandas as pd
import datetime
import pydeck as pdk
import plotly.express as px
import time

import awesome_streamlit as ast

@st.cache(persist=True, allow_output_mutation=True)
def load_data(parse=False):
	if parse:
		data = pd.read_csv("src/data/activecases.csv", parse_dates=["Date"])
		dow = pd.to_datetime(data["Date"]).iloc[-1].dayofweek
		data = data[pd.to_datetime(data["Date"]).dt.dayofweek == dow].reset_index(drop=True)
	else:
		data = pd.read_csv("src/data/activecases.csv")
		dow = pd.to_datetime(data["Date"]).iloc[-1].dayofweek
		data = data[pd.to_datetime(data["Date"]).dt.dayofweek == dow].reset_index(drop=True)
	return data

def write():
	#with st.spinner("Loading Motion Chart..."):
	st.markdown("# Pandemic Spread Chart")
	data = load_data(parse=False)

	access_token = 'pk.eyJ1IjoicHJhYm9kaHc5NiIsImEiOiJja2s5a3p5Y2gwNGIzMndueGd1MmoxbDB3In0.EdO-eu9KIA_Sz9-JBNs4Uw'
	px.set_mapbox_access_token(access_token)

	st.markdown(f"""<style>
		.reportview-container .main .block-container{{
		max-width: 1100px;
		padding-left: 5rem;
		}}</style>""", unsafe_allow_html=True)

	fig = px.scatter_mapbox(
		data, lat="Latitude", lon="Longitude",
		size="% of Population", size_max=50,
		color="Active", color_continuous_scale=px.colors.sequential.Pinkyl,
		hover_name="CountryName",
		mapbox_style='dark', zoom=1,
		animation_frame="Date", animation_group="CountryName",
	)
	fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
	fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
	fig.layout.coloraxis.showscale = False
	fig.layout.sliders[0].pad.t = 10
	fig.layout.updatemenus[0].pad.t= 10
	fig.update_layout(width=925, height=600)
	st.plotly_chart(fig, use_container_width=False)
	#with m:
	#	st.write(fig)

	date = data["Date"].min()

	data = load_data(parse=True)
	dft = data[data["Date"] == data["Date"].max()].sort_values(by="Active").reset_index(drop=True)[["CountryName", "Date", "Active"]]
	day = dft["Date"].max().strftime("%b %d, %Y")
	fig = px.bar(dft.tail(), x="CountryName", y="Active", title="Top 5 countries by active cases on "+day)
	st.plotly_chart(fig)
	st.markdown("Source: [CCSE@JHU daily reports] (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)&nbsp;\
		[Bing COVID-19 Data] (https://github.com/microsoft/Bing-COVID-19-Data)")