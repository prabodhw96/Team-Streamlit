import streamlit as st
import numpy as np
import pandas as pd
import datetime
import pydeck as pdk
import plotly.express as px
import time

import awesome_streamlit as ast

@st.cache(persist=True)
def load_data():
	data = pd.read_csv("src/data/activecases.csv", parse_dates=["Date"])
	return data

def write():
	#with st.spinner("Loading Motion Chart..."):
	st.markdown("## Active Cases - Motion Chart")
	data = load_data()

	date = data["Date"].min()
	view = pdk.ViewState(latitude=0, longitude=0, zoom=0.2)
	#features = list(data.columns[4:])
	#features.insert(0, " ")
	#feature = st.selectbox("Select statistics to display", features, key='feature')
	feature = "Active"
	covidLayer = pdk.Layer(
		"ScatterplotLayer",
		data=data,
		pickable=False,
		opacity=0.3,
		stroked=True,
		filled=True,
		radius_scale=6,
		radius_min_pixels=5,
		radius_max_pixels=60,
		line_width_min_pixels=1,
		get_position=["Longitude", "Latitude"],
		get_radius=feature,
		get_fill_color=[252, 136, 3],
		get_line_color=[255,0,0],
		tooltip="test test",
	)
	r = pdk.Deck(layers=[covidLayer],
		initial_view_state=view,
		map_style="mapbox://styles/mapbox/light-v9",
	)
	st.write("Click on the Start button to see the motion chart")
	if st.button("Start", False):
		subheading = st.subheader("")
		map = st.pydeck_chart(r)
		days = (data["Date"].max() - data["Date"].min()).days
		#if feature != " ":
		for i in range(0, days, 1):
			date += datetime.timedelta(days=1)
			covidLayer.data = data[data['Date'] == date.isoformat()]
			r.update()
			map.pydeck_chart(r)
			subheading.subheader("Active cases on %s" % (date.strftime("%B %d, %Y")))
			#subheading.subheader("%s on %s" % (feature, date.strftime("%B %d, %Y")))
			time.sleep(0.05)

	dft = data[data["Date"] == data["Date"].max()].sort_values(by="Active").reset_index(drop=True)[["CountryName", "Date", "Active"]]
	day = dft["Date"].max().strftime("%b %d, %Y")
	fig = px.bar(dft.tail(), x="CountryName", y="Active", title="Top 5 countries by active cases on "+day)
	st.plotly_chart(fig)
	st.markdown("Source: [CCSE@JHU daily reports] (https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports)&nbsp;\
		[Bing COVI-19 Data] (https://github.com/microsoft/Bing-COVID-19-Data)")