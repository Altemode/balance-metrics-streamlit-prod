import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Balance App | SPESS",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# #Define paths:
# current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
# css_file = current_dir / "style" / "style.css"

# #Load css:
# with open(css_file) as f:
#     st.write("<style>{}</style>".format(f.read()), unsafe_allow_html=True)



st.title("Welcome to the Balance Data Analysis App")
st.subheader("In cooperation with the School of Physical Education and Sports Science of Athens.")
st.write("#")
st.sidebar.info("Select a page above.")

col1, col2 = st.columns([2.5,1])
with col1:
    st.markdown("""
        **Brief Description:**

        Balance App developed for the purpose of research of School of Physical Education and Sports Science of Athens. 
        For this purpose a force platform by PLUX Biosignals has been used to test balance and collects the raw data of athletes.
        
        The main scope of this app is to be calculate the ballance of athletes by collecing raw data from the force platform,
        proccesing these and calculating the center of pressure in the x and y axis (ML & AP).
        For these reason the streamlit app framework is a great choice to transform the python code into a nice wep app.

        **Navigate to the left menu sidebar to choose a page.**

        """
    )
with col2:
    st.write("")
