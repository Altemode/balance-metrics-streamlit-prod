import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
import plotly.figure_factory as ff


 
############## ############## PAGE 1 PREPARE THE FILE ############# ############# ############## ##############
      
      
st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
   
)

st.title('Prepare the file')
st.write('**Into the below form insert the txt file of unconverted raw values from the force platform.**')

st.sidebar.info("Instructions")
st.sidebar.info("-Use the adjacent form and choose the txt file with the raw data from the force platform for the trial that interests you.")
st.sidebar.info("-Use the slider to select the time period you want.")
st.sidebar.info("-Finaly check the Verify box and export the file from the 'Export File' button!")




with st.expander("Show File Form", expanded=True):
    uploaded_file = st.file_uploader("Choose a file")
#platform_mass = st.number_input("Give the platfrom mass:")
#@st.cache(allow_output_mutation=True)
#@st.experimental_singleton
@st.cache  # No need for TTL this time. It's static data :)
def get_data():
    if uploaded_file:
        df_raw_data = pd.read_csv(uploaded_file, sep='\s+', skiprows=10, index_col = None)
        #Define Header columns
        columns_count = len(df_raw_data.axes[1])
        if columns_count == 6:
            df_raw_data.columns = ['Time', 'Col_2', 'Mass_1', 'Mass_2', 'Mass_3', 'Mass_4']
        
        C = 406.831
        #sr = 1000
        resolution = 16
        # Calculate for A Sensor Mass $ Weight
        Vfs_1 = 2.00016
        df_raw_data['Mass_1'] = df_raw_data['Mass_1'] * C / (Vfs_1 * ( (2**resolution) - 1 ) )
        # Calculate for B Sensor Mass $ Weight
        Vfs_2 = 2.00002
        df_raw_data['Mass_2'] = df_raw_data['Mass_2'] * C / (Vfs_2 * ( (2**resolution) - 1 ) )
        # Calculate for C Sensor Mass $ Weight
        Vfs_3 = 2.00057
        df_raw_data['Mass_3'] = df_raw_data['Mass_3'] * C / (Vfs_3 * ( (2**resolution) - 1 ) )
        # Calculate for D Sensor Mass $ Weight
        Vfs_4 = 2.00024
        df_raw_data['Mass_4'] = df_raw_data['Mass_4'] * C / (Vfs_4 * ( (2**resolution) - 1 ) )
        # Calculate the sum of all sensors Mass $ Weight
        df_raw_data['Mass_Sum'] = (df_raw_data['Mass_1'] + df_raw_data['Mass_2'] + df_raw_data['Mass_3'] + df_raw_data['Mass_4'])
        df_raw_data['Rows_Count'] = df_raw_data.index
        mean_weight_A = df_raw_data.loc[0:500, 'Mass_1'].mean()
        mean_weight_B = df_raw_data.loc[0:500, 'Mass_2'].mean()
        mean_weight_C = df_raw_data.loc[0:500, 'Mass_3'].mean()
        mean_weight_D = df_raw_data.loc[0:500, 'Mass_4'].mean()
        df_raw_data['Mass_1'] = df_raw_data['Mass_1'] - mean_weight_A
        df_raw_data['Mass_2'] = df_raw_data['Mass_2'] - mean_weight_B
        df_raw_data['Mass_3'] = df_raw_data['Mass_3'] - mean_weight_C
        df_raw_data['Mass_4'] = df_raw_data['Mass_4'] - mean_weight_D

        return df_raw_data

if uploaded_file:
    
    df_raw_data= get_data()
    
    # if st.button('Reload Dataframe with Raw Data'):
    #     get_data()
    if df_raw_data is not None:
        #df_prepared = df_raw_data.copy()
        min_time = int(df_raw_data.index.min())
        max_time = int(df_raw_data.index.max())
        
        with st.form("Give the numbers"):
            col1,col2 = st.columns(2)
            st.write("Give duration")
            with col1:
                from_time = st.number_input("Give the first time")
            with col2:
                till_time = st.number_input("Give the second time")
            
            
            selected_time_range = st.slider('Select the whole time range of the graph, per 1000', min_time, max_time, (min_time, max_time), 1)
            selected_area = (df_raw_data.Rows_Count.between(selected_time_range[0], selected_time_range[1]) )

            submitted = st.form_submit_button("Calculate")

            if submitted :
                mean_weight_A = df_raw_data.loc[from_time:till_time, 'Mass_1'].mean()
                mean_weight_B = df_raw_data.loc[from_time:till_time, 'Mass_2'].mean()
                mean_weight_C = df_raw_data.loc[from_time:till_time, 'Mass_3'].mean()
                mean_weight_D = df_raw_data.loc[from_time:till_time, 'Mass_4'].mean()
                df_prepared = df_raw_data.copy()
                df_prepared['Mass_1'] = df_raw_data['Mass_1'] - mean_weight_A
                df_prepared['Mass_2'] = df_raw_data['Mass_2'] - mean_weight_B
                df_prepared['Mass_3'] = df_raw_data['Mass_3'] - mean_weight_C
                df_prepared['Mass_4'] = df_raw_data['Mass_4'] - mean_weight_D
                df_prepared = pd.DataFrame(df_prepared[selected_area])
            
            
        

    col1, col2 = st.columns(2, gap='large')
    with col1:
        ### CHART A ###
        if submitted:
            fig1 = px.line(df_prepared, x="Rows_Count", y="Mass_1", title='Sensor A')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            fig1 = px.line(df_raw_data, x="Rows_Count", y="Mass_1", title='Sensor A')
            st.plotly_chart(fig1, use_container_width=True)


        #### CHART C ####
        if submitted:
            fig3 = px.line(df_prepared, x="Rows_Count", y="Mass_3", title='Sensor C')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            fig3 = px.line(df_raw_data, x="Rows_Count", y="Mass_3", title='Sensor C')
            st.plotly_chart(fig3, use_container_width=True)            
        
    with col2:
        ### CHART B ####
        if submitted:
            fig2 = px.line(df_prepared, x="Rows_Count", y="Mass_2", title='Sensor B')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            fig2 = px.line(df_raw_data, x="Rows_Count", y="Mass_2", title='Sensor B')
            st.plotly_chart(fig2, use_container_width=True) 


        ### CHART D ####
        if submitted:
            fig4 = px.line(df_prepared, x="Rows_Count", y="Mass_4", title='Sensor D')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            fig4 = px.line(df_raw_data, x="Rows_Count", y="Mass_4", title='Sensor D')
            st.plotly_chart(fig4, use_container_width=True)

        if submitted :

            # To Drop the unnecessary Columns
            df_prepared.drop(['Rows_Count'], axis = 1, inplace=True)
            filename = uploaded_file.name
            # To Get only the filename without extension (.txt)
            final_filename = os.path.splitext(filename)[0]
            st.write("The file name of your file is : ", final_filename)
            show_df_prepared = st.checkbox("Display the final dataframe")
            st.dataframe(df_prepared)
            st.download_button(
                label="Export File",
                data=df_prepared.to_csv(index=False),
                file_name=final_filename +'.csv',
                mime='text/csv',
            )
            


                
                