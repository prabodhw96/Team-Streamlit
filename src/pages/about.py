import streamlit as st
import pandas as pd

import awesome_streamlit as ast
from PIL import Image

st.cache(persist=True, allow_output_mutation=True)
def load_data():
	data = pd.read_csv("src/data/team.csv", encoding="cp1252")
	return data

def write():
	st.markdown(f"""<style>
	.reportview-container .main .block-container{{
	padding-top: 0em;
	max-width: 900px;
	}}</style>""", unsafe_allow_html=True)
	#with st.spinner("Loading Home..."):
		#ast.shared.components.title_awesome("NPI RL")
	#st.markdown("# M-montreal-quebec")
	st.markdown("<h1 style='text-align: center;'>M-montreal-quebec</h1>", unsafe_allow_html=True)
	st.write("We are a team comprising of students and researchers who want to essentially help in showing the efficacy \
		of machine learning to enhance the ability of decision makers to carry out their decisions and see the consequence \
		so that they can reach optimal outcomes for the people.")
	st.markdown("## XPRIZE Foundation")
	st.write("Founded in 1994, XPRIZE is a non-profit organization that designs and hosts public competitions intended to \
		encourage technological development to benefit humanity. The XPRIZE mission is to bring about \
		""radical breakthroughs for the benefit of humanity"" through incentivized competition. Their board of trustees \
		include James Cameron, Larry Page, Arianna Huffington, and Ratan Tata among others.")
	st.markdown("## $500K Pandemic Response Challenge sponsored by Cognizant")
	st.write("The Pandemic Response Challenge focuses on the development of data-driven AI systems to predict COVID-19 infection \
		rates and prescribe Intervention Plans (IPs) that regional governments, communities, and organizations can implement to \
		minimize harm when reopening their economies.")
	st.markdown("### The competition consists of two phases:")
	st.markdown("#### Phase 1 - Predictor Development Overview")
	st.write("The goal of phase 1 is to provide accurate, localized predictions of COVID-19 transmission based on local data,\
		unique intervention strategies, community resilience characteristics, and mitigation policies and practices.")
	st.markdown("#### Phase 2 - Prescriptor Development Overview")
	st.write("Prescriptor development encompasses the rapid creation of custom, non-pharmaceutical and other intervention plan \
		prescriptions and mitigation models to help decision-makers minimize COVID-19 infection cases while lessening economic \
		and other negative implications of the virus.")

	data = load_data()
	st.title("Team")
	st.markdown("## Team Leaders")
	with st.beta_expander("Marc-Andre Rousseau"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			mar_photo = Image.open("src/images/Marc_Photo.jpg")
			mar_photo = mar_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(mar_photo)
		with txt:
			st.write(data[data["Name"]=="Marc-Andre Rousseau"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marc-Andre Rousseau"]["p2"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marc-Andre Rousseau"]["p3"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marc-Andre Rousseau"]["p4"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marc-Andre Rousseau"]["p3"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Marc-Andre Rousseau"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Brady Neal"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			bn_photo = Image.open("src/images/brady-small.jpg")
			bn_photo = bn_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(bn_photo)
		with txt:
			st.write(data[data["Name"]=="Brady Neal"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Baihan Lin"]["links"].reset_index(drop=True)[0])

	st.markdown("## Team Members")
	with st.beta_expander("Diogo Pernes"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			dp_photo = Image.open("src/images/dpernes_photo.jpg")
			dp_photo = dp_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(dp_photo)
		with txt:
			st.write(data[data["Name"]=="Diogo Pernes"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Diogo Pernes"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Diogo Pernes"]["links"].reset_index(drop=True)[0])
	
	with st.beta_expander("Thin Nguyen"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			tn_photo = Image.open("src/images/Nguyen.PNG")
			tn_photo = tn_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(tn_photo)
		with txt:
			st.write(data[data["Name"]=="Thin Nguyen"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Thin Nguyen"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Thin Nguyen"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Andrew Williams"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			aw_photo = Image.open("src/images/andrew.png")
			aw_photo = aw_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(aw_photo)
		with txt:
			st.write(data[data["Name"]=="Andrew Williams"]["p1"].reset_index(drop=True)[0])
		
		

	with st.beta_expander("Chen-Yang Su"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			cy_photo = Image.open("src/images/Chen-Yang.JPG")
			cy_photo = cy_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(cy_photo)
		with txt:
			st.write(data[data["Name"]=="Chen-Yang Su"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Chen-Yang Su"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Chen-Yang Su"]["links"].reset_index(drop=True)[0])
		

	with st.beta_expander("Olexa Bilaniuk"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			ob_photo = Image.open("src/images/obilaniu.jpg")
			ob_photo = ob_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(ob_photo)
		with txt:
			st.write(data[data["Name"]=="Olexa Bilaniuk"]["p1"].reset_index(drop=True)[0])
		st.markdown("[GitHub](https://github.com/obilaniu)")

	with st.beta_expander("Makesh Narsimhan"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			mn_photo = Image.open("src/images/Makesh.JPG")
			mn_photo = mn_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(mn_photo)
		with txt:
			st.write(data[data["Name"]=="Makesh Narsimhan"]["p1"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Makesh Narsimhan"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Marharyta Aleksandrova"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			ma_photo = Image.open("src/images/Marharyta.jpg")
			ma_photo = ma_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(ma_photo)
		with txt:
			st.write(data[data["Name"]=="Marharyta Aleksandrova"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Marharyta Aleksandrova"]["p2"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Marharyta Aleksandrova"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Sai Aravind Sreeramadas"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			sa_photo = Image.open("src/images/Sai_Photo.jpg")
			sa_photo = sa_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(sa_photo)
		with txt:
			st.write(data[data["Name"]=="Sai Aravind Sreeramadas"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Baihan Lin"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Baihan Lin"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			bl_photo = Image.open("src/images/Baihan_Lin_sq.jpg")
			bl_photo = bl_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(bl_photo)
		with txt:
			st.write(data[data["Name"]=="Baihan Lin"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Baihan Lin"]["p2"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Baihan Lin"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Prabodh Wankhede"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			pw_photo = Image.open("src/images/Prabodh.jpg")
			pw_photo = pw_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(pw_photo)
		with txt:
			st.write(data[data["Name"]=="Prabodh Wankhede"]["p1"].reset_index(drop=True)[0])
		st.markdown(data[data["Name"]=="Prabodh Wankhede"]["links"].reset_index(drop=True)[0])

	st.title("Advisors")
	with st.beta_expander("Irina Rish"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			ir_photo = Image.open("src/images/Irina_Rish.png")
			ir_photo = ir_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(ir_photo)
		with txt:
			st.write(data[data["Name"]=="Irina Rish"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Irina Rish"]["p2"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Irina Rish"]["links"].reset_index(drop=True)[0])
	
	with st.beta_expander("Djallel Bouneffouf"):
		img, txt = st.beta_columns([0.2, 0.8])
		with img:
			db_photo = Image.open("src/images/Djallel.jpg")
			db_photo = db_photo.resize((150, 180), Image.ANTIALIAS)
			st.image(db_photo)
		with txt:
			st.write(data[data["Name"]=="Djallel Bouneffouf"]["p1"].reset_index(drop=True)[0])
		st.write(data[data["Name"]=="Djallel Bouneffouf"]["links"].reset_index(drop=True)[0])

	with st.beta_expander("Yang Zhang"):
		st.write(data[data["Name"]=="Yang Zhang"]["p1"].reset_index(drop=True)[0])