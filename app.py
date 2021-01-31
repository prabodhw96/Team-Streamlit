import streamlit as st

#st.beta_set_page_config(page_title='M-montreal-quebec', initial_sidebar_state='auto')

import awesome_streamlit as ast
import src.pages.predpres
import src.pages.eda
import src.pages.team
import src.pages.motion
import src.pages.clus
import src.pages.about

ast.core.services.other.set_logging_format()

PAGES = {
	"Prediction": src.pages.predpres,
	"Pandemic Spread Chart": src.pages.motion,
	"Exploratory Data Analysis": src.pages.eda,
	"Clustering": src.pages.clus,
	"About": src.pages.about,
	"Team": src.pages.team,
}

def main():
	#st.markdown("<h1 style='text-align: center;'>M-montreal-quebec</h1>", unsafe_allow_html=True)
	st.sidebar.title("Navigation")
	selection = st.sidebar.radio("Go to", list(PAGES.keys()))

	page = PAGES[selection]

	with st.spinner(f"Loading {selection}..."):
		ast.shared.components.write_page(page)

if __name__ == "__main__":
	main()