import awesome_streamlit as ast

import numpy as np 
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
from src.pages.hover_dict import hover_dict

@st.cache(persist=True, allow_output_mutation=True, show_spinner=False)
def load_pop_data():
	data = pd.read_csv("src/data/population.csv")
	return data

@st.cache(persist=True, allow_output_mutation=True, show_spinner=False)
def load_countries():
	df = pd.read_csv("src/data/country_cc_desc.csv")
	return df

@st.cache(persist=True, allow_output_mutation=True, show_spinner=False)
def load_oxford_data():
	data = pd.read_csv("src/data/OxCGRT_latest.csv", 
		parse_dates=['Date'], encoding="ISO-8859-1", 
		dtype={"RegionName": str, "RegionCode": str},
		 error_bad_lines=False)
	return data

@st.cache(persist=True, allow_output_mutation=True, show_spinner=False)
def load_cases_data():
	data = pd.read_csv("src/data/casesanddeaths.csv", parse_dates=["Date"])
	return data

def write():
	st.markdown(f"""<style>
		.reportview-container .main .block-container{{
		padding-top: 0em;
		max-width: 1200px;
		}}</style>""", unsafe_allow_html=True)
	st.markdown(f"""<style>
		.svg-container{{
		padding-left: 1em;
		}}</style>""", unsafe_allow_html=True)
	st.markdown("<h1 style='text-align: center;'>Country Comparator</h1>", unsafe_allow_html=True)
	st.write("This page allows you to compare the intervention plans put in force by various governments at different stages of the pandemic.\
		 We also plot the number of daily cases smoothened by a 7 day moving average atop the chart of intervention plans, thus indicating the actions the governments took in response to the rate of spread of the virus.")
	countries = load_countries()
	countries = countries.sort_values(by=["CountryName"]).reset_index(drop=True)
	countries = list(countries["CountryName"].unique())
	col_country1, col_country2 = st.beta_columns(2)
	nz_idx = countries.index("New Zealand")
	us_idx = countries.index("United States")
	with col_country1:
		selected_country1 = st.selectbox("Type the country to select", countries, key='selected_country1', index=nz_idx)
	with col_country2:
		selected_country2 = st.selectbox("Type the country to select", countries, key='selected_country2', index=us_idx)

	df = load_oxford_data()
	cases = load_cases_data()

	cases_grouped = cases.groupby("CountryName")
	for country,df_temp in cases_grouped:
		df_temp["DailyCasesMA"] = df_temp.DailyNewCases.rolling(window=7).mean
		for i in range(0,7):
			df_temp.iloc[i]["DailyCasesMA"] = df_temp.iloc[i]["DailyNewCases"]
	cases["DailyCasesMA"] = cases.groupby('CountryName').rolling(7)['DailyNewCases'].mean().reset_index(drop=True)
	cases["DailyCasesMA"].fillna(cases.DailyNewCases,inplace=True)

	population = load_pop_data()
	cases = cases.merge(population,on="CountryName")
	cases["DailyCasesMAPopulation"] = (cases["DailyCasesMA"]/cases["Population"] )*100


	cols = ["CountryName", "Date", "C1_School closing", "C2_Workplace closing", "C3_Cancel public events", 
			"C4_Restrictions on gatherings", "C5_Close public transport", "C6_Stay at home requirements",
			"C7_Restrictions on internal movement", "C8_International travel controls", "H1_Public information campaigns",
			"H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings"]

	def create_timeline(country, intervention):
		data = df[df["CountryName"]==country].reset_index(drop=True)
		data = data[cols].dropna().reset_index(drop=True)
		data = data[["Date", intervention]]

		dates = []
		ip = []
		dates.append(data["Date"].min())
		ip.append(data[data["Date"]==data["Date"].min()].reset_index(drop=True)[intervention][0])

		for i in range(1, len(data)):
			if data.loc[i-1][intervention] != data.loc[i][intervention]:
				dates.append(data.loc[i]["Date"])
				ip.append(data.loc[i][intervention])

		dates.append(data["Date"].max())
		ip.append(data[data["Date"]==data["Date"].max()].reset_index(drop=True)[intervention][0])

		gc = pd.DataFrame(zip(dates, ip), columns=["Start", "Stringency"])
		fin = list(gc["Start"])[1:]
		gc = gc[:-1]
		gc["Finish"] = fin
		gc["Task"] = intervention

		st_dict = {0: "None", 1:"Medium", 2:"Medium-Hard", 3:"Hard", 4:"Strict"}
		gc["Stringency"] = gc["Stringency"].replace(st_dict)
		return gc

	def add_hover_text(row):
		return hover_dict[row['Task']][row['Stringency']]

	def show_plot_compare(country1, country2):
		df1 = create_timeline(country1, cols[2])
		df2 = create_timeline(country2, cols[2])

		for i in cols[3:]:
			df1 = df1.append(create_timeline(country1, i))
			df2 = df2.append(create_timeline(country2, i))
		df1["Description"] = df1.apply(add_hover_text, axis=1)
		df2["Description"] = df2.apply(add_hover_text, axis=1)
		color = {"None":"#6f9c3d", "Medium":"#a5c90f", "Medium-Hard":"#ffb366", "Hard":"#ff8829", "Strict":"#ff6b40"}
		fig1 = ff.create_gantt(df1, group_tasks=True, index_col="Stringency", colors=color, show_colorbar=True,
								show_hover_fill=True,bar_width=0.5)
		fig2 = ff.create_gantt(df2, group_tasks=True, index_col="Stringency", colors=color, show_colorbar=True,
								show_hover_fill=True,bar_width=0.5)
		#fig1.update_layout(legend_orientation="h")
		#fig2.update_layout(legend_orientation="h")

		for i in range(5,10):
			fig1.data[i].update(hoverinfo="text",hoveron='points+fills')
			fig2.data[i].update(hoverinfo="text",hoveron='points+fills')

		fig1.update_traces(opacity=0.5)
		fig2.update_traces(opacity=0.5)

		figs = make_subplots(rows=2, cols=2, shared_xaxes=True, shared_yaxes=True, horizontal_spacing = 0.05,
							specs=[[{"secondary_y": True}, {"secondary_y": True}], [{"colspan": 2}, None]],
							subplot_titles=(selected_country1, selected_country2))

		fig1.data[0].showlegend=False
		fig1.data[1].showlegend=False
		fig1.data[2].showlegend=False
		fig1.data[3].showlegend=False
		fig1.data[4].showlegend=False
		fig1.data[5].showlegend=False

		figs.add_trace(fig1.data[2], row=1, col=1)
		figs.add_trace(fig1.data[3], row=1, col=1)
		figs.add_trace(fig1.data[4], row=1, col=1)
		figs.add_trace(fig1.data[1], row=1, col=1)
		figs.add_trace(fig1.data[0], row=1, col=1)

		figs.add_trace(fig2.data[2], row=1, col=2)
		figs.add_trace(fig2.data[3], row=1, col=2)
		figs.add_trace(fig2.data[4], row=1, col=2)
		figs.add_trace(fig2.data[1], row=1, col=2)
		figs.add_trace(fig2.data[0], row=1, col=2)

		for trace in fig1.data[5:]:
			figs.add_trace(trace)

		for trace in fig2.data[5:]:
			figs.add_trace(trace)

		cases_country1 = cases[cases.CountryName==country1]
		cases_x1 = cases_country1['Date']
		cases_y1 = cases_country1['DailyCasesMA']
		figs.add_trace(go.Scatter(x=cases_x1, y=cases_y1, mode='lines', showlegend=False,
						marker=dict(color='Teal',),line=dict(width=4), name="Daily New Cases"),
						secondary_y=True, row=1, col=1)

		cases_country2 = cases[cases.CountryName==country2]
		cases_x2 = cases_country2['Date']
		cases_y2 = cases_country2['DailyCasesMA']
		figs.add_trace(go.Scatter(x=cases_x2, y=cases_y2, mode='lines', showlegend=True,
						marker=dict(color='Teal',),line=dict(width=4), name="Daily New Cases"),
						secondary_y=True, row=1, col=2)

		figs.layout.xaxis.update(fig1.layout.xaxis)
		figs.layout.yaxis.update(fig2.layout.yaxis)
		figs['layout'].update(legend={'traceorder':'grouped'})
		figs['layout'].update(legend={'x': 1, 'y': 1})
		figs.update_layout(legend=dict(orientation="h", yanchor="bottom", y=0.5, xanchor="center", x=0.5))
		figs.layout.plot_bgcolor = "white"
		fig2.update_layout(showlegend=False)
		figs.update_xaxes(rangeselector_visible=False)
		figs.update_layout(height=800, width=1200)

		return figs

	st.plotly_chart(show_plot_compare(selected_country1, selected_country2))