import streamlit as st

#st.beta_set_page_config(page_title='M-montreal-quebec', initial_sidebar_state='auto')

import awesome_streamlit as ast
import src.pages.prediction
import src.pages.eda
import src.pages.team
import src.pages.motion
import src.pages.clus
import src.pages.about
import src.pages.virus
import src.pages.prescription
import src.pages.country_comparator

import warnings
warnings.filterwarnings("ignore")

st.beta_set_page_config(initial_sidebar_state='expanded')
st.markdown(
  f'''
    <style>
        .sidebar .sidebar-content {{
          width:200px;
        }}
    </style>
  ''',
  unsafe_allow_html=True
)
st.markdown("""<style>.sidebar .sidebar-collapse-control{
  background-image: linear-gradient(#f6bdc0, #f6bdc0);
  color: white;
  }
  </style>
  """, unsafe_allow_html=True)

html = """
  <style>
    .reportview-container {
      flex-direction: row-reverse;
    }

    header > .toolbar {
      flex-direction: row-reverse;
      left: 1rem;
      right: auto;
    }

    .sidebar .sidebar-collapse-control,
    .sidebar.--collapsed .sidebar-collapse-control {
      left: auto;
      right: 0.5rem;
    }

    .sidebar .sidebar-content {
      transition: margin-right .3s, box-shadow .3s;
    }

    .sidebar.--collapsed .sidebar-content {
      margin-left: auto;
      margin-right: -21rem;
    }

    @media (max-width: 991.98px) {
      .sidebar .sidebar-content {
        margin-left: auto;
      }
    }
  </style>
"""
#st.markdown(html, unsafe_allow_html=True)

ast.core.services.other.set_logging_format()

PAGES = {
  "Prescription": src.pages.prescription,
  "Country Comparator": src.pages.country_comparator,
	"Prediction": src.pages.prediction,
	#"Pandemic Spread Chart": src.pages.motion,
	#"Exploratory Data Analysis": src.pages.eda,
	#"Clustering": src.pages.clus,
  "SARS-CoV-2": src.pages.virus,
	"About": src.pages.about,
	#"Team": src.pages.team,
}

def main():
	#hide_streamlit_style = """<style>#MainMenu {visibility: hidden;}</style>"""
	#st.markdown(hide_streamlit_style, unsafe_allow_html=True)
	#st.markdown("<h1 style='text-align: center;'>M-montreal-quebec</h1>", unsafe_allow_html=True)
	#st.sidebar.title("Navigation")
	selection = st.sidebar.radio(" ", list(PAGES.keys()))

	page = PAGES[selection]

	with st.spinner(f"Loading {selection}..."):
		ast.shared.components.write_page(page)

if __name__ == "__main__":
	main()