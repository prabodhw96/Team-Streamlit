import streamlit as st

import awesome_streamlit as ast

def write():
	with st.spinner("Loading Home..."):
		#ast.shared.components.title_awesome("NPI RL")
		st.write("We are a team comprising of students and researchers who want to essentially help in showing the efficacy \
			of machine learning to enhance the ability of decision makers to carry out their decisions and see the consequence \
			so that they can reach optimal outcomes for the people.")
		st.markdown("## XPRIZE Foundation")
		st.write("Founded in 1994, XPRIZE is a non-profit organization that designs and hosts public competitions intended to \
			encourage technological development to benefit humanity. The XPRIZE mission is to bring about \
			""radical breakthroughs for the benefit of humanity"" through incentivized competition. Their board of trustees \
			include James Cameron, Larry Page, Arianna Huffington, and Ratan Tata among others.")
		st.markdown("## XPRIZE Pandemic Response Challenge")
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