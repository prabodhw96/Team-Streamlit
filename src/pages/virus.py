import streamlit as st
import numpy as np
import pandas as pd
import datetime
import pydeck as pdk
import plotly.express as px
import time
import folium
from streamlit_folium import folium_static

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

@st.cache(persist=True, allow_output_mutation=True)
def load_clus_data():
	data = pd.read_csv("src/data/clus.csv")
	return data

@st.cache(persist=True, allow_output_mutation=True)
def load_json():
	data = pd.read_json("src/data/world-countries.json")
	return data

def write():
	st.markdown(f"""<style>
	.reportview-container .main .block-container{{
	max-width: 900px;
	padding-top: 0em;
	}}</style>""", unsafe_allow_html=True)
	#st.markdown("# SARS-CoV-2")
	st.markdown("<h1 style='text-align: center;'>SARS-CoV-2</h1>", unsafe_allow_html=True)
	st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
		labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
		nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit \
		esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
		culpa qui officia deserunt mollit anim id est laborum.")
	st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
		labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
		nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit \
		esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
		culpa qui officia deserunt mollit anim id est laborum.")
	st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
		labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
		nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit \
		esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
		culpa qui officia deserunt mollit anim id est laborum.")
	st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
		labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
		nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit \
		esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
		culpa qui officia deserunt mollit anim id est laborum.")

	st.markdown("<h2 style='text-align: center;'>Pandemic Spread Chart</h2>", unsafe_allow_html=True)
	data = load_data(parse=False)

	access_token = 'pk.eyJ1IjoicHJhYm9kaHc5NiIsImEiOiJja2s5a3p5Y2gwNGIzMndueGd1MmoxbDB3In0.EdO-eu9KIA_Sz9-JBNs4Uw'
	px.set_mapbox_access_token(access_token)

	fig = px.scatter_mapbox(
		data, lat="Latitude", lon="Longitude",
		size="% of Population", size_max=50,
		color="Active", color_continuous_scale=['#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E', '#F4564E'],
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

	#data = load_data(parse=True)
	#dft = data[data["Date"] == data["Date"].max()].sort_values(by="Active").reset_index(drop=True)[["CountryName", "Date", "Active"]]
	#day = dft["Date"].max().strftime("%b %d, %Y")
	#fig = px.bar(dft.tail(), x="CountryName", y="Active", title="Top 5 countries by active cases on "+day)
	#st.plotly_chart(fig)
	st.markdown("Source: [CCSE@JHU daily reports] (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)&nbsp;\
		[Bing COVID-19 Data] (https://github.com/microsoft/Bing-COVID-19-Data)")

	st.markdown("<h2 style='text-align: center;'>Countries with similar seasonal nature</h2>", unsafe_allow_html=True)
	st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut \
		labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
		nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit \
		esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
		culpa qui officia deserunt mollit anim id est laborum.")
	clus = load_clus_data()

#	st.markdown(f"""<style>
#		.reportview-container .main .block-container{{
#		max-width: 1000px;
#		padding-left: 10rem;
#		}}</style>""", unsafe_allow_html=True)
						
	gj = load_json()
	gj = gj.assign(id=gj["features"].apply(pd.Series)["id"], name=gj["features"].apply(pd.Series)["properties"].apply(pd.Series)["name"])
	gj = gj[gj.name.isin(list(clus.country.unique()))]

	colors  = {}
	colors[0] = "#264653"
	colors[1] = "#277da1"
	colors[2] = "#577590"
	colors[3] = "#4d908e"
	colors[4] = "#43aa8b"
	colors[5] = "#90be6d"
	colors[6] = "#b0f2b4"
	colors[7] = "#FFD700"
	colors[8] = "#edb6a3"
	colors[9] = "#cbac88"
	colors[10] = "#9aa373"
	colors[11] = "#915e3d"
	colors[12] = "#fe9234"
	colors[13] = "#eda80c"
	colors[14] = "#f3722c"
	colors[15] = "#f94144"

	colours = clus.copy()
	colours = colours.replace({"cluster":colors})
	colours["colour1"] = colours["cluster"]
	colours["colour2"] = colours["cluster"]
	colours = colours.drop(columns=["cluster"])
	colours = colours.set_index("country")

	def style_fn(feature):
		cc = colours.loc[feature["properties"]["name"]]
		ss = {'fillColor':f'{cc[0]}', 'color':f'{cc[1]}'}
		return ss

	#st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	col1, col2 = st.beta_columns([0.2, 0.8])
	with col1:
		c = st.radio("Select Cluster#", ["Show all",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
	#c = st.radio("Select Cluster#", ["Show all",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
	with col2:
		if c == "Show all":
			m = folium.Map(location=[51.5074, 0.1728], zoom_start=2, control_scale=True, max_bounds=True)
			for r in gj.to_dict(orient="records"):
				folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
			folium_static(m)
		else:
			x = clus[clus["cluster"]==c]
			dx = gj[gj["name"].isin(x["country"].unique())].reset_index(drop=True)
			m = folium.Map(location = [51.5074, 0.1728], zoom_start=2, control_scale=True, max_bounds=True)
			for r in dx.to_dict(orient="records"):
				folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
			folium_static(m)
			st.write(list(x["country"].unique()))