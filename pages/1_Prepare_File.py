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
def get_data():
    if uploaded_file:
        df = pd.read_csv(uploaded_file, sep='\s+', skiprows=3, index_col = None)
        #Define Header columns
        columns_count = len(df.axes[1])
        if columns_count == 6:
            df.columns = ['Time', 'Trigger', 'Mass_1', 'Mass_2', 'Mass_3', 'Mass_4']
        
        C = 406.831
        #sr = 1000
        resolution = 16
        # Calculate for A Sensor Mass $ Weight
        Vfs_1 = 2.00016
        df['Mass_1'] = df['Mass_1'] * C / (Vfs_1 * ( (2**resolution) - 1 ) )
        # Calculate for B Sensor Mass $ Weight
        Vfs_2 = 2.00002
        df['Mass_2'] = df['Mass_2'] * C / (Vfs_2 * ( (2**resolution) - 1 ) )
        # Calculate for C Sensor Mass $ Weight
        Vfs_3 = 2.00057
        df['Mass_3'] = df['Mass_3'] * C / (Vfs_3 * ( (2**resolution) - 1 ) )
        # Calculate for D Sensor Mass $ Weight
        Vfs_4 = 2.00024
        df['Mass_4'] = df['Mass_4'] * C / (Vfs_4 * ( (2**resolution) - 1 ) )
        # Calculate the sum of all sensors Mass $ Weight
        df['Mass_Sum'] = (df['Mass_1'] + df['Mass_2'] + df['Mass_3'] + df['Mass_4'])

        # Find the CoPX, CoPY for whole time range:
        W = 450
        L = 450
        df['X'] =  (W / 2) * (( df['Mass_2'] + df['Mass_3'] - df['Mass_1'] - df['Mass_4'] )) / ( df['Mass_1'] + df['Mass_2'] + df['Mass_3'] + df['Mass_4'] )
        df['Y'] =  (L / 2) * (( df['Mass_2'] + df['Mass_1'] - df['Mass_3'] - df['Mass_4'] )) / ( df['Mass_1'] + df['Mass_2'] + df['Mass_3'] + df['Mass_4'] ) 
        
        df['Rows_Count'] = df.index

        # Find for each sensor the platform mass and subtract it
        mean_weight_A = df.loc[0:500, 'Mass_1'].mean()
        mean_weight_B = df.loc[0:500, 'Mass_2'].mean()
        mean_weight_C = df.loc[0:500, 'Mass_3'].mean()
        mean_weight_D = df.loc[0:500, 'Mass_4'].mean()
        df['Mass_1'] = df['Mass_1'] - mean_weight_A
        df['Mass_2'] = df['Mass_2'] - mean_weight_B
        df['Mass_3'] = df['Mass_3'] - mean_weight_C
        df['Mass_4'] = df['Mass_4'] - mean_weight_D

        return df

if uploaded_file:
    
    df= get_data()
    st.dataframe(df, use_container_width=True)

    if df is not None:
        min_time = int(df['Time'].min()) 
        max_time = int(df['Time'].max())
        st.write("#")
        
        with st.form("Give the times in stable state to find the means in X & Y columns"):
            st.markdown("Give the times in Balance & Trial period.")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                from_balance_time = st.number_input("From Balance Time", step=1)
            with col2:
                till_balance_time = st.number_input("Till Balance Time", step=1)
            with col3:
                from_trial_time = st.number_input("From Trial Time", step=1)
            with col4:
                till_trial_time = st.number_input("Till Trial Time", step=1)
            st.write("#")
            selected_time_range = st.slider('Choose the Trial Time Period, between Triggers. This will be your final dataset.', min_time, max_time, (min_time, max_time), 1)
            selected_area = (df.Time.between(selected_time_range[0], selected_time_range[1]) )

            submitted = st.form_submit_button("Calculate")
            
            if submitted :
                #----Before Trigger----#
                #Find the means of stable state:
                Xp = df.loc[int(from_balance_time):int(till_balance_time), 'X'].mean()
                Yp = df.loc[int(from_balance_time):int(till_balance_time), 'Y'].mean()
                

                #----After Trigger----#
                #Find the ML, AP:
                df['ML'] = df['X'] - Xp
                df['AP'] = df['Y'] - Yp
                if selected_time_range[0]>1000:
                    
                    ML_mean = df.loc[int(from_trial_time):int(till_trial_time), 'ML'].mean()
                    AP_mean = df.loc[int(from_trial_time):int(till_trial_time), 'AP'].mean()
                    st.write("MPIKA",ML_mean)
                    #Find the Xn, Yn:
                    df['Xn'] = df['ML'] - ML_mean       
                    df['Yn'] = df['AP'] - AP_mean
                    st.write("df")
                    st.dataframe(df, use_container_width=True)
                    df_prepared = df.copy()
                    st.write("df_[prepared")
                    st.dataframe(df_prepared, use_container_width=True)
                    df_prepared = pd.DataFrame(df_prepared[selected_area])
                    st.write("EDWW")
                    st.write(ML_mean, df_prepared['Xn'].mean())
                    st.dataframe(df_prepared, use_container_width=True)
                    
            
    ### CHART A ###
    if submitted:

        # st.write(df_prepared['ML'].mean())
        # K = len(df_prepared)
        # st.write(( 1 / K ) * df_prepared['ML'].sum())
        # st.write(df['ML'].mean())
        # st.write('Mean ML & AP:', round(df_prepared['ML'].mean(),3),'&', round(df_prepared['AP'].mean(),3))
        # st.write('Mean Xn & Yn:', round(df_prepared['Xn'].mean(),3),'&', round(df_prepared['Yn'].mean(),3))
        #st.dataframe(df, use_container_width=True)
        st.write("2o if submitted")
        st.write("df")
        st.dataframe(df, use_container_width=True)
        st.write("df_[prepared")
        st.write("MPIKA",ML_mean)
        st.dataframe(df_prepared, use_container_width=True)
        fig_trigger = px.line(df_prepared, x="Time", y="Trigger")
        fig_trigger.update_layout(
                        margin=dict(l=0, r=20, t=0, b=60),
                        #paper_bgcolor="LightSteelBlue",   
                    )
        fig1 = px.line(df_prepared, x="Time", y="Mass_1", title='Sensor A')
        fig1.update_layout(
                        margin=dict(l=0, r=20, t=30, b=0),
                        #paper_bgcolor="LightSteelBlue",   
                    )
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig_trigger, use_container_width=True)

    else:
        fig_trigger = px.line(df, x="Time", y="Trigger")
        fig_trigger.update_layout(
                        margin=dict(l=0, r=20, t=0, b=60),
                        #paper_bgcolor="LightSteelBlue",   
                    )
        fig1 = px.line(df, x="Time", y="Mass_1", title='Sensor A')
        fig1.update_layout(
                        margin=dict(l=0, r=20, t=30, b=0),
                        #paper_bgcolor="LightSteelBlue",   
                    )
        st.plotly_chart(fig1, use_container_width=True)
        st.plotly_chart(fig_trigger, use_container_width=True)


    #     #### CHART C ####
    #     if submitted:
    #         fig3 = px.line(df_prepared, x="Time", y="Mass_3", title='Sensor C')
    #         st.plotly_chart(fig3, use_container_width=True)

    #     else:
    #         fig3 = px.line(df, x="Time", y="Mass_3", title='Sensor C')
    #         st.plotly_chart(fig3, use_container_width=True)            
        
    # with col2:
    #     ### CHART B ####
    #     if submitted:
    #         fig2 = px.line(df_prepared, x="Time", y="Mass_2", title='Sensor B')
    #         st.plotly_chart(fig2, use_container_width=True)
    #     else:
    #         fig2 = px.line(df, x="Time", y="Mass_2", title='Sensor B')
    #         st.plotly_chart(fig2, use_container_width=True) 


    #     ### CHART D ####
    #     if submitted:
    #         fig4 = px.line(df_prepared, x="Time", y="Mass_4", title='Sensor D')
    #         st.plotly_chart(fig2, use_container_width=True)
    #     else:
    #         fig4 = px.line(df, x="Time", y="Mass_4", title='Sensor D')
    #         st.plotly_chart(fig4, use_container_width=True)

    if submitted :

        #df_prepared.drop(['Time'], axis = 1, inplace=True)
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
            


                
                