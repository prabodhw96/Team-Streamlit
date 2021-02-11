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
	st.write("SARS-COV-2 is a highly infectious pathogen capable of causing a disease called Covid-19 which usually presents as inflammation in the lungs.  The virus itself is not particularly harmful however the immune response to the virus in some people can cause devastating problems.  Most notably, it is thought that tight junctions are affected which loosens the connections between adjacent cells making the infected organ more prone to damage from physical stress.  Furthermore, the virus seems to disproportionately cause disease in the elderly where an exponential distribution is observed when plotting the probability of death vs age of patients who have Covid-19 and been hospitalized.  The cause for this age-susceptibility relationship is currently a matter of scientific debate however the same pattern can be observed when plotting the output of the thymus gland over time and comparing the charts from men and women.  Many hypotheses have been advanced including one due to entropy, another due to the reduction of the production of regulatory T-cells that suppress auto-immune reactions and other genetic factors such as changes in the expression of Angiotensin Convertin Enzyme-2 receptor availability on the cell membrane.  The threat to humanity of a similar virus had been established in 2015 where a partnership between the Wuhan institute of virology and an American university investigated the potential for a SARS-like coronavirus to develop affinity to the human ACE2 receptor.")
	st.write("In 2017, a company with an organic synthesis for a safe biological response modifier capable of accelerating the maturation and production of T-cells from the thymus, already shown to be effective against SARS-COV-1 was delisted from the NASDAQ and privatized by a Chinese company.  The Chinese government acted quickly to contain the spread of the virus and built two hospitals in record time and a large cohort of medical staff were sent to Hubei, the province at the epicenter of the outbreak.  These medical staff were administered this medication, seemingly ignored by Western medicine and the success of this prophylactic immune boosting campaign were reported in the medical literature.  Furthermore, retrospective studies showed efficacy in reducing mortality, repopulating the depleted immune system and .  The first North American manuscript, published in June, recommended that thymosin be evaluated and there is now a clinical trial in Rhode Island being conducted by a Harvard professor.  The benefit of this approach is that it does not depend on a specific sequence of the virus and instead it seems to increase the diversity of available T-cells thereby theoretically facilitating the recognition of virally infected cells.")
	st.write("In fact, this approach has recently been tried and found to be successful against certain cancers that display abberrant proteins on their cell surface much like a virally infected cell would.")
	st.write("In addition to this effort, there is a widescale attempt to vaccinate the public against a rapidly mutating and highly transmissible agent that is losing steam due to the new strains such as the one in South Africa.  As a result, a part of our contribution to this contest is to highlight the potential use of this agent and to encourage others to follow the clinical trial in Rhode Island closely because it may be a light at the end of the tunnel of a very difficult time in human history.")
	st.write("In addition to causing a terrible burden on the healthcare systems, there have been widespread economic repercussions disproportionately affecting low income and client facing employees whose jobs depend on a healthy service industry.  The problems do not stop there since the closure of schools have resulted in a disproportionate effect on women's careers as they have been shown to be more likely to have chosen to take care of the children at home.  It is clear that a solution that is capable of addressing the problem of not only this particular virus but all future pandemics is needed so that our society is resilient to future outbreaks similar to the ones that happened in 1917-1918 and 1928 and that will most likely happen in the future.")
	st.write("The pandemic spread chart essentially shows the spread of the disease but is slightly affected by the ability of a country to test for covid (many countries in the African continent lacked that ability in the early stages of the outbreak) as well as large differences in the successes that countries have had in containing the virus.")

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
	st.write("Given that our team's predictor was the top predictor throughout all offline evaluation periods and almost the \
		entire time since the submission, we believe that there is evidence to support the hypothesis that the virus is \
		predominantly spread via aerosolized particles. While many Countries like Canada focus on fomite transmission and \
		have people wash their hands frequently, this kind of transmission would not be so heavily affected by changes in \
		weather patterns. Whereas a virus that is spread via aerosolized particles would see radical increases in countries \
		with seasons where cold weather drives people indoors thereby increasing the viral density of the air being breathed \
		given that the virus is now endemic to most of the world. While the solution to phase 2 uses a predictor that does not \
		use weather, our solution uses a population-weighted temperatures in our model to allow the model to learn from their \
		associations within this context")
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
		c = st.radio("Select Cluster#", ["Show all",0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],unsafe_allow_html=True)
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