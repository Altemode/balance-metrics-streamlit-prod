# biosignalsnotebooks project own package.
import biosignalsnotebooks as bsnb
import streamlit as st
# Powerful scientific package for array operations.
from numpy import array
import pandas as pd

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



with st.expander("Show File Form", expanded=True):
    uploaded_file = st.file_uploader("Choose a file")

def get_data():
    if uploaded_file:
        df_raw_data = pd.read_csv(uploaded_file, sep='\s+', skiprows=10, index_col = None)
        #Define Header columns
        columns_count = len(df_raw_data.axes[1])
        if columns_count == 6:
            df_raw_data.columns = ['Time', 'Col_2', 'Mass_1', 'Mass_2', 'Mass_3', 'Mass_4']
        

    #path_to_file = "BAL_LOAD-0_2022-11-04_11-25-02.txt"

    # Load the data from the file
    #force_platform = bsnb.load(path_to_file)

    # Identify the mac address of the device
    #force_platform_mac, _ = force_platform.keys()

    # Get the signals acquired by the force_platform
    #force_platform_signals = force_platform[force_platform_mac]


    # load_cells = []
    # for load_cell in force_platform_signals.keys():
    #     load_cells.append(force_platform_signals[load_cell])

    # Constant for load cell 1.
    Vfs_1 = 2.00061
    # Constant for load cell 2.
    Vfs_2 = 2.00026
    # Constant for load cell 3.
    Vfs_3 = 2.00011
    # Constant for load cell 4.
    Vfs_4 = 2.00038

    C = 406.831 # kg.mV/V

    # Sampling rate used during the acquisition.
    sr = 1000 # Hz

    # Resolution of the device.
    resolution = 16 # bits

    def weight(ADC, Vfs, C, resolution):
        return array(ADC) * C / (Vfs * ( (2**resolution) - 1 ) )

    weight_1 = weight(df_raw_data['Mass_1'], Vfs_1, C, resolution)
    weight_2 = weight(df_raw_data['Mass_2'], Vfs_2, C, resolution)
    weight_3 = weight(df_raw_data['Mass_3'], Vfs_3, C, resolution)
    weight_4 = weight(df_raw_data['Mass_4'], Vfs_4, C, resolution)


    W = 450 # mm
    L = 450 # mm
    C1 = weight_1
    C2 = weight_2
    C3 = weight_3
    C4 = weight_4

    # Get the center of pressure on the x axis
    center_of_pressure_x = (W/2)*(C2 + C3 - C1 - C4)/(C1 + C2 + C3 + C4)
    # Get the center of pressure on the y axis
    center_of_pressure_y = (L/2)*(C2 + C1 - C3 - C4)/(C1 + C2 + C3 + C4)
    Xn = center_of_pressure_x - center_of_pressure_x.mean()
    Yn = center_of_pressure_y - center_of_pressure_y.mean()
    return df_raw_data, center_of_pressure_x, center_of_pressure_y , Xn, Yn

if uploaded_file:
    
    df_raw_data, center_of_pressure_x, center_of_pressure_y, Xn, Yn = get_data()
    
    st.write("aasa")
    # st.write(center_of_pressure_x, center_of_pressure_y, Xn, Yn)

def make_charts():       
    fig = px.scatter( x=Xn, y=Yn, opacity= 0.4)
    fig.update_traces(marker={'size': 1})
    fig.add_trace(go.Scatter(x=[round(center_of_pressure_x.mean(),3)], y=[round(center_of_pressure_y.mean(),3)], mode = 'markers',
                    marker_symbol = 'circle', name="Zero Point" ,marker_color='red',
                    marker_size = 5))
    fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=60),
            #paper_bgcolor="LightSteelBlue",
    )
    
    return fig

fig = make_charts()
st.plotly_chart(fig,use_container_width=True)
