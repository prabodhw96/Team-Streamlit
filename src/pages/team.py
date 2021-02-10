import pandas as pd
import streamlit as st

import awesome_streamlit as ast
from PIL import Image

st.cache(persist=True, allow_output_mutation=True)
def load_data():
	data = pd.read_csv("src/data/team.csv", encoding="cp1252")
	return data

def write():
	#with st.spinner("Loading Team..."):
	data = load_data()
	st.title("Team")
	st.markdown("## Team Leaders")
	with st.beta_expander("Marc-Andre Rousseau"):
		st.write("Marc-Andre Rousseau")

	with st.beta_expander("Brady Neal"):
		st.write("Brady Neal")

		#st.markdown("Brady Neal")

	st.markdown("## Team Members")
	with st.beta_expander("Diogo Pernes"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			dp_photo = Image.open("src/images/dpernes_photo.jpg")
			dp_photo = dp_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(dp_photo)
		with txt:
			st.write(data[data["Name"]=="Diogo Pernes"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Diogo Pernes"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Diogo Pernes"]["links"].reset_index(drop=True)[0])
	
	with st.beta_expander("Thin Nguyen"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			tn_photo = Image.open("src/images/Nguyen.PNG")
			tn_photo = tn_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(tn_photo)
		with txt:
			st.write(data[data["Name"]=="Thin Nguyen"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Thin Nguyen"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Thin Nguyen"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Andrew Williams"):
		st.markdown("Andrew Williams")

	with st.beta_expander("Chen-Yang Su"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			cy_photo = Image.open("src/images/Chen-Yang.JPG")
			cy_photo = cy_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(cy_photo)
		with txt:
			st.write(data[data["Name"]=="Chen-Yang Su"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Chen-Yang Su"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Chen-Yang Su"]["links"].reset_index(drop=True)[0])
		

	with st.beta_expander("Olexa Bilaniuk"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			ob_photo = Image.open("src/images/obilaniu.jpg")
			ob_photo = ob_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(ob_photo)
		with txt:
			st.write(data[data["Name"]=="Olexa Bilaniuk"]["p1"].reset_index(drop=True)[0])
		st.markdown("[GitHub](https://github.com/obilaniu)")

	with st.beta_expander("Makesh Narsimhan"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			mn_photo = Image.open("src/images/Makesh.JPG")
			mn_photo = mn_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(mn_photo)
		with txt:
			st.write(data[data["Name"]=="Makesh Narsimhan"]["p1"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Makesh Narsimhan"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Marharyta Aleksandrova"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			ma_photo = Image.open("src/images/Marharyta.jpg")
			ma_photo = ma_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(ma_photo)
		with txt:
			st.write(data[data["Name"]=="Marharyta Aleksandrova"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marharyta Aleksandrova"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Marharyta Aleksandrova"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Sai Aravind Sreeramadas"):
		st.markdown("Sai Aravind Sreeramadas")

	with st.beta_expander("Djallel Bouneffouf"):
		st.markdown("Djallel Bouneffouf")

	with st.beta_expander("Baihan Lin"):
		st.markdown("Baihan Lin")

	with st.beta_expander("Prabodh Wankhede"):
		img, txt = st.beta_columns([0.25, 0.75])
		with img:
			pw_photo = Image.open("src/images/Prabodh.jpg")
			pw_photo = pw_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(pw_photo)
		with txt:
			st.write(data[data["Name"]=="Prabodh Wankhede"]["p1"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Prabodh Wankhede"]["links"].reset_index(drop=True)[0])