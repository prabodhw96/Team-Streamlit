import streamlit as st
import datetime
from datetime import timedelta
import time
import os

import numpy as np
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.figure_factory as ff
import src.pages.rerun as rerun
from src.pages.prescribe import prescribe
from src.pages.hover_dict import hover_dict

@st.cache(persist=True, allow_output_mutation=True)
def load_cases_data():
	data = pd.read_csv("src/data/casesanddeaths.csv", parse_dates=["Date"])
	return data

def load_data():
	df = pd.read_csv("src/data/init.csv")
	return df

@st.cache(persist=True, allow_output_mutation=True)
def load_countries():
	df = pd.read_csv("src/data/country_cc_desc.csv")
	return df

@st.cache(persist=True, allow_output_mutation=True, show_spinner=False)
def load_oxford_data():
    data = pd.read_csv("src/data/OxCGRT_latest.csv",
    					parse_dates=['Date'],
    					encoding="ISO-8859-1",
    					dtype={"RegionName": str, "RegionCode": str},
    					error_bad_lines=False)
    return data

def load_cost():
	data = pd.read_csv("src/data/cost.csv")
	return data

def load_res_df():
	data = pd.read_csv("src/data/res_df.csv", parse_dates=["Date"])
	return data

def write():
	st.markdown(f"""<style>
	.reportview-container .main .block-container{{
	padding-top: 0em;
	max-width: 900px;
	}}</style>""", unsafe_allow_html=True)

	st.markdown("<h1 style='text-align: center;'>Prescription - Phase 2</h1>", unsafe_allow_html=True)
	st.write("NOTE: Please note that this is not a full fledged website. \
		 If the Run button has been clicked, it would take ~100 seconds to render the results. Please wait until the graph appears. It will not be possible to move to another page when the process is running due to limitations of the script we use.\
		 In case there is an issue with rendering the graph, please move the stringency slider or reload the page (Ctrl+R/Cmd+R). ")
	
	
	st.write("This dashboard allows the user to visualize the intervention plans suggested by our prescriptor built for Phase 2.")
	st.markdown("1. Select the country from the drop down list.")
	st.markdown("2. Enter the number of days to prescribe intervention plans for.")
	st.markdown("3. Enter the costs associated with taking various intervention actions.")
	st.markdown("4. Click on Run. (Note: It takes ~100 seconds to run for 28 days)")
	st.markdown("5. Select the stringency level.")


	prior_ip = load_oxford_data()

	countries = load_countries()
	countries = countries.sort_values(by=["CountryName"]).reset_index(drop=True)
	countries = list(countries["CountryName"].unique())
	us_idx = countries.index("United States")
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country',index=us_idx)

	col0, colx, coly = st.beta_columns(3)
	with col0:
		n_days = st.number_input("Enter no. of days", 14, 90, value=28)

	col1, cx1, col2, cx2, col3 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col4, cx4, col5, cx5, col6 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col7, cx7, col8, cx8, col9 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])
	col10, cx10, col11, cx11, col12 = st.beta_columns([0.3, 0.05, 0.3, 0.05, 0.3])

	val_list = np.arange(0.0, 12.01, 0.01)
	my_rounded_list = [ round(elem, 2) for elem in val_list]

	df = load_data()
	
	with col1:
		c1 = st.number_input(key='c1', label='C1_School closing', min_value=0.00, step=0.01, value=1.00)
	with col2:
		c2 = st.number_input(key='c2', label='C2_Workplace closing', min_value=0.00, step=0.01, value=1.00)
	with col3:
		c3 = st.number_input(key='c3', label='C3_Cancel public events', min_value=0.00, step=0.01, value=1.00)
	with col4:
		c4 = st.number_input(key='c4', label='C4_Restrictions on gatherings', min_value=0.00, step=0.01, value=1.00)
	with col5:
		c5 = st.number_input(key='c5', label='C5_Close public transport', min_value=0.00, step=0.01, value=1.00)
	with col6:
		c6 = st.number_input(key='c6', label='C6_Stay at home requirements', min_value=0.00, step=0.01, value=1.00)
	with col7:
		c7 = st.number_input(key='c7', label='C7_Restrictions on internal movement', min_value=0.00, step=0.01, value=1.00)
	with col8:
		c8 = st.number_input(key='c8', label='C8_International travel controls', min_value=0.00, step=0.01, value=1.00)
	with col9:
		h1 = st.number_input(key='h1', label='H1_Public information campaigns', min_value=0.00, step=0.01, value=1.00)
	with col10:
		h2 = st.number_input(key='h2', label='H2_Testing policy', min_value=0.00, step=0.01, value=1.00)
	with col11:
		h3 = st.number_input(key='h3', label='H3_Contact tracing', min_value=0.00, step=0.01, value=1.00)
	with col12:
		h6 = st.number_input(key='h6', label='H6_Facial Coverings', min_value=0.00, step=0.01, value=1.00)

	cost_cols = ["CountryName", "RegionName", "C1_School closing", "C2_Workplace closing", "C3_Cancel public events", 
			"C4_Restrictions on gatherings", "C5_Close public transport", "C6_Stay at home requirements",
			"C7_Restrictions on internal movement", "C8_International travel controls", "H1_Public information campaigns",
			"H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings"]

	k = np.array([c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6])
	k = k/sum(k)
	k = k*12
	k = k.tolist()
	k.insert(0, selected_country)
	k.insert(1, np.nan)
	cost = pd.DataFrame([k], columns=cost_cols)

	ip_cols = cost_cols.copy()
	ip_cols.insert(2, "Date")

	start = 0
	if st.button("Run", False):
		time_value = round(100 * n_days/28)
		if n_days <= 28:
			st.write("This is a slow task; takes ⏳ ~ {} seconds to run".format(100))
		else:
			st.write("This is a slow task; takes ⏳ ~ {} seconds to run".format(time_value))
		start = time.time()
		prior_ip_country = prior_ip[prior_ip["CountryName"]==selected_country]
		prior_ip_country = prior_ip_country.dropna(subset=ip_cols[3:])
		prior_ip_country = prior_ip_country.tail(21).reset_index(drop=True)[ip_cols]

		start_date = str((prior_ip_country["Date"].max()+timedelta(days=1)).date())
		end_date = str((prior_ip_country["Date"].max()+timedelta(days=n_days)).date())
		#st.write(start_date, end_date)
		res_df = prescribe(str(start_date), str(end_date), prior_ip_country, cost)
		res_df.to_csv("src/data/res_df.csv", index=False)
		st.success("Prescriptions are ready!")
	
	try:
		res_df = load_res_df()
		cost_ = cost.copy() #load_cost()
		pres = res_df.groupby(["PrescriptionIndex"]).mean().reset_index().drop(columns=["RegionName"])
		cost_ = cost_.drop(columns=["CountryName", "RegionName"])
		pres["Stringency"] = pres.drop(columns=["PrescriptionIndex"]).mul(cost_.loc[0],axis=1).sum(axis=1)
		sl = list(pres["Stringency"])
		pres.sort_values(by=["Stringency"], inplace=True)
		pres.reset_index(drop=True, inplace=True)
		pres = pres.drop_duplicates(subset=["Stringency"], keep="first")
		sl = list(pres["Stringency"])
		pres = pres.round(0)
		pres["Stringency"] = ['%.2f' % elem for elem in sl]
		stringency_list = list(pres["Stringency"])
		np_arr = np.arange(0, len(stringency_list))
		np_arr = [str(i) for i in np_arr]
		stl_dict = dict(zip(np_arr, stringency_list))
		end = time.time()

		if start == 0:
			duration = 0
		else:
			duration = end - start
			st.write("✔️ Took {} seconds".format(round(duration, 2)))
		col1, col2 = st.beta_columns(2)
		if res_df["CountryName"].unique()[0] == selected_country:
			with col1:
				str_val = st.select_slider("Select Stringency (on a scale of {})".format(len(np_arr)-1), np_arr)
		
		stringency = stl_dict[str_val]

		presc_idx = pres[pres["Stringency"]==stringency].reset_index(drop=True)["PrescriptionIndex"][0]
		pareto_presc = pd.read_csv("src/data/pareto_presc.csv")
		source = pareto_presc[pareto_presc["PrescriptionIndex"]==presc_idx].reset_index(drop=True)["source"][0]
		fname = "src/data/pred_df_{}.csv".format(source)
		pred_df = pd.read_csv(fname, parse_dates=["Date"])
		pred_df = pred_df[pred_df["PrescriptionIndex"]==presc_idx].reset_index(drop=True)

		df = prior_ip.copy()
		cases = load_cases_data()
		cases_grouped = cases.groupby("CountryName")
		for country,df_temp in cases_grouped:
			df_temp["DailyCasesMA"] = df_temp.DailyNewCases.rolling(window=7).mean
			for i in range(0,7):
				df_temp.iloc[i]["DailyCasesMA"] = df_temp.iloc[i]["DailyNewCases"]
		cases["DailyCasesMA"] = cases.groupby('CountryName').rolling(7)['DailyNewCases'].mean().reset_index(drop=True)
		cases["DailyCasesMA"].fillna(cases.DailyNewCases,inplace=True)
		cases = cases[cases["Date"] <= res_df["Date"].min()].reset_index(drop=True)
		cols = cost_cols.copy()
		cols[1] = "Date"

		def create_timeline(country, intervention):
			data = df[df["CountryName"]==country].reset_index(drop=True)
			data = data[cols].dropna().reset_index(drop=True)
			data = data[["Date", intervention]]
			data = data[data["Date"] <= res_df["Date"].min()].reset_index(drop=True)

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

		def create_timeline_forecast(country, intervention):
			df = res_df.copy()
			df = df[df["PrescriptionIndex"]==presc_idx].reset_index(drop=True)
			data = df[df["CountryName"]==country].reset_index(drop=True)
			data = data[cols].dropna().reset_index(drop=True)
			data = data[["Date", intervention]]
			#data = data[data["Date"] <= res_df["Date"].min()].reset_index(drop=True)

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

		def ip_df(country):
			ip_df = pd.DataFrame(columns=["Start","Stringency","Finish","Task"])
			for intervention in  cols[2:]:
				df_temp = create_timeline_forecast(country, intervention)
				ip_df = ip_df.append(df_temp)
			return ip_df

		def add_hover_text(row):
			return hover_dict[row['Task']][row['Stringency']]

		def show_plot(country):
			df1 = create_timeline(country, cols[2])
			df2 = ip_df(country)
			#st.write(df2)
			#df2["Finish"] = res_df["Date"].max()
		   
			for i in cols[3:]:
				df1 = df1.append(create_timeline(country, i))
			df1['Description'] = df1.apply(add_hover_text, axis=1)
			df2['Description'] = df2.apply(add_hover_text, axis=1)
			df1 = df1.append(df2)
			color = {"None":"#6f9c3d", "Medium":"#a5c90f", "Medium-Hard":"#ffb366", "Hard":"#ff8829", "Strict":"#ff6b40"}
			fig = ff.create_gantt(df1, group_tasks=True, index_col="Stringency", colors=color, show_colorbar=True,show_hover_fill=True,bar_width=0.5)
			fig.update_layout(legend_orientation="h")

			for i in range(5,10):
				fig.data[i].update(hoverinfo="text",hoveron='points+fills')

			figs = make_subplots(shared_xaxes=True, specs=[[{"secondary_y": True}]])
			fig.update_traces(opacity=0.5)
			figs.add_trace(fig.data[2])
			figs.add_trace(fig.data[3])
			figs.add_trace(fig.data[4])
			figs.add_trace(fig.data[1])
			figs.add_trace(fig.data[0])
		    
			for trace in fig.data[5:]:
				figs.add_trace(trace)
			cases_country = cases[cases.CountryName==country]
			cases_x = cases_country['Date']
			cases_x = cases_x.append(pred_df["Date"])
			cases_y = cases_country['DailyCasesMA']

			pred_df["PredictedDailyNewCasesMA"] = pred_df["PredictedDailyNewCases"].rolling(7, min_periods=1).mean()
			pred_df["PredictedDailyNewCases"] = pred_df["PredictedDailyNewCasesMA"]

			cases_y = cases_y.append(pred_df["PredictedDailyNewCases"])
			figs.add_trace(go.Scatter(x=cases_x, y=cases_y, mode='lines', marker=dict(color='Teal',),line=dict(width=4),name="Daily New Cases"),secondary_y=True)
			figs.layout.xaxis.update(fig.layout.xaxis)
			figs.layout.yaxis.update(fig.layout.yaxis)
			figs['layout'].update(legend={'traceorder':'grouped'})
			figs['layout'].update(legend={'x': 1, 'y': 1})
			figs.update_layout(height=600, width=1000)
			figs.add_shape(type="line",
				x0=res_df["Date"].min(), y0=0, x1=res_df["Date"].min(), y1=1,
				line=dict(
					color="RoyalBlue",
					width=4,
					dash="dot",))
			figs.update_shapes(dict(xref='x', yref='paper'))
			return figs

		st.plotly_chart(show_plot(selected_country))
		#snpi = pres[pres["Stringency"] == stringency].drop(columns=["Stringency", "PrescriptionIndex"]).reset_index(drop=True)
		#snpi.index = ["Prescription"]
		#with st.beta_expander("Suggested interventions for the selected stringency:"):
		#	st.table(snpi.T)
		#st.markdown("#### Suggested interventions for the selected stringency:")
		#st.table(snpi.T)
	except:
		pass