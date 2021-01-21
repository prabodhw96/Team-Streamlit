import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import folium_static

import awesome_streamlit as ast

@st.cache(persist=True)
def load_clus_data():
	data = pd.read_csv("src/data/clus.csv")
	return data

@st.cache(persist=True)
def load_json():
	data = pd.read_json("src/data/world-countries.json")
	return data

def write():
	st.markdown("## Clustering of countries based on seasons being similar")
	clus = load_clus_data()
						
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

	if st.checkbox("Show all countries", False):
		m = folium.Map(location = [51.5074, 0.1728], zoom_start=2, control_scale=True)

		for r in gj.to_dict(orient="records"):
			folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)

		folium_static(m)

	if st.checkbox("Show countries by cluster", False):
		st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
		c = st.radio("Select Cluster#", np.arange(0, 16, 1))
		x = clus[clus["cluster"]==c]
		dx = gj[gj["name"].isin(x["country"].unique())].reset_index(drop=True)

		m = folium.Map(location = [51.5074, 0.1728], zoom_start=2, control_scale=True)

		for r in dx.to_dict(orient="records"):
			folium.GeoJson(r["features"], name=r["name"], tooltip=r["name"], style_function=style_fn).add_to(m)
		
		folium_static(m)

		if st.checkbox("Show name of countries", False):
			st.write(list(x["country"].unique()))