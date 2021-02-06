import streamlit as st

import numpy as np
import pandas as pd
import src.pages.rerun as rerun

def generate_sequence_for_change(changed_index, changed_value):
	fixed_sum = 12
	req_sum = fixed_sum - changed_value
	random_vec = np.random.rand(11)
	rand_sum = random_vec.sum()
	coef = req_sum/rand_sum
	req_rand_vec = coef*random_vec
	final_vec = np.insert(req_rand_vec,changed_index,changed_value)
	d = pd.DataFrame(final_vec)
	d.to_csv("src/data/init.csv", index=False)
	rerun.rerun()

def load_data():
	df = pd.read_csv("src/data/init.csv")
	return df

@st.cache(persist=True, allow_output_mutation=True)
def load_countries():
	df = pd.read_csv("src/data/country_cc_desc.csv")
	return df

def write():
	st.markdown(f"""<style>
	.reportview-container .main .block-container{{
	padding-top: 0em;
	max-width: 900px;
	}}</style>""", unsafe_allow_html=True)

	st.markdown("<h1 style='text-align: center;'>Prescription - Phase 2</h1>", unsafe_allow_html=True)

	countries = load_countries()
	countries = list(countries["CountryName"].unique())
	selected_country = st.selectbox("Type the country to select", countries, key='selected_country')

	col1, col2, col3 = st.beta_columns(3)
	col4, col5, col6 = st.beta_columns(3)
	col7, col8, col9 = st.beta_columns(3)
	col10, col11, col12 = st.beta_columns(3)

	val_list = np.arange(0.0, 12.01, 0.01)
	my_rounded_list = [ round(elem, 2) for elem in val_list]

	df = load_data()
	#st.dataframe(df)
	arr_df = list(df["0"])
	arr = [round(elem, 2) for elem in arr_df]
	st.write(sum(arr))

	with col1:
		c1 = st.number_input(key='c1', label='C1_School closing', min_value=0.00, max_value=12.00, step=0.01, value=arr[0])
		#c1 = st.select_slider('c1', my_rounded_list, value=arr[0])
	with col2:
		c2 = st.number_input(key='c2', label='C2_Workplace closing', min_value=0.00, max_value=12.00, step=0.01, value=arr[1])
		#c2 = st.select_slider('c2', my_rounded_list, value=arr[1])
	with col3:
		c3 = st.number_input(key='c3', label='C3_Cancel public events', min_value=0.00, max_value=12.00, step=0.01, value=arr[2])
		#c3 = st.select_slider('c3', my_rounded_list, value=arr[2])
	with col4:
		c4 = st.number_input(key='c4', label='C4_Restrictions on gatherings', min_value=0.00, max_value=12.00, step=0.01, value=arr[3])
		#c4 = st.select_slider('c4', my_rounded_list, value=arr[3])
	with col5:
		c5 = st.number_input(key='c5', label='C5_Close public transport', min_value=0.00, max_value=12.00, step=0.01, value=arr[4])
		#c5 = st.select_slider('c5', my_rounded_list, value=arr[4])
	with col6:
		c6 = st.number_input(key='c6', label='C6_Stay at home requirements', min_value=0.00, max_value=12.00, step=0.01, value=arr[5])
		#c6 = st.select_slider('c6', my_rounded_list, value=arr[5])
	with col7:
		c7 = st.number_input(key='c7', label='C7_Restrictions on internal movement', min_value=0.00, max_value=12.00, step=0.01, value=arr[6])
		#c7 = st.select_slider('c7', my_rounded_list, value=arr[6])
	with col8:
		c8 = st.number_input(key='c8', label='C8_International travel controls', min_value=0.00, max_value=12.00, step=0.01, value=arr[7])
		#c8 = st.select_slider('c8', my_rounded_list, value=arr[7])
	with col9:
		h1 = st.number_input(key='h1', label='H1_Public information campaigns', min_value=0.00, max_value=12.00, step=0.01, value=arr[8])
		#h1 = st.select_slider('h1', my_rounded_list, value=arr[8])
	with col10:
		h2 = st.number_input(key='h2', label='H2_Testing policy', min_value=0.00, max_value=12.00, step=0.01, value=arr[9])
		#h2 = st.select_slider('h2', my_rounded_list, value=arr[9])
	with col11:
		h3 = st.number_input(key='h3', label='H3_Contact tracing', min_value=0.00, max_value=12.00, step=0.01, value=arr[10])
		#h3 = st.select_slider('h3', my_rounded_list, value=arr[10])
	with col12:
		h6 = st.number_input(key='h6', label='H6_Facial Coverings', min_value=0.00, max_value=12.00, step=0.01, value=arr[11])
		#h6 = st.select_slider('h6', my_rounded_list, value=arr[11])

	k = [c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6]
	for i in range(len(k)):
		if arr[i] != k[i]:
			generate_sequence_for_change(i, k[i])
			break

	cols = ["CountryName", "RegionName", "C1_School closing", "C2_Workplace closing", "C3_Cancel public events", 
			"C4_Restrictions on gatherings", "C5_Close public transport", "C6_Stay at home requirements",
			"C7_Restrictions on internal movement", "C8_International travel controls", "H1_Public information campaigns",
			"H2_Testing policy", "H3_Contact tracing", "H6_Facial Coverings"]
	
	if st.button("Submit", False):
		#st.write(c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6)
		cost = pd.DataFrame([[selected_country, np.nan, c1, c2, c3, c4, c5, c6, c7, c8, h1, h2, h3, h6]], columns=cols)
		st.write(cost)