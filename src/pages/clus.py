import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

import streamlit.components.v1 as components

import awesome_streamlit as ast

@st.cache(persist=True, allow_output_mutation=True)
def load_clus_data():
	data = pd.read_csv("src/data/clus.csv")
	return data

@st.cache(persist=True, allow_output_mutation=True)
def load_json():
	data = pd.read_json("src/data/world-countries.json")
	return data

def write():
	#st.markdown(f"""<style>
	#	.reportview-container .main .block-container{{
	#	max-width: 1500px;
	#	padding-top: 0rem;
	#	padding-left: 0rem;
	#	}}</style>""", unsafe_allow_html=True)
	#components.iframe("https://pop.xprize.org/Prizes/PrizeDetails?codename=pandemic_response_challenge",width=1500,height=4500)
	st.markdown("# Countries with similar seasonal nature")
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

	st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
	c = st.radio("Select Cluster#", ["Show all",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
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
