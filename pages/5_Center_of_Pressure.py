import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import ftplib
import tempfile
from pathlib import Path
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



############# ############## PAGE 2 INSERT TO DATABASE USER+TRIAL ############## ############ #############################
st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    
)
df = pd.read_csv('https://sportsmetrics.geth.gr/storage/BAL_LOAD-0_2ND_2022-11-04_12-32-00.csv')

with st.sidebar.expander("Download a sample file:"):
    st.download_button(
        label="Sample",
        data=df.to_csv(),
        file_name='sample.csv',
        mime='text/csv',
    )

def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    #client = create_client(url, key)
    return create_client(url, key)
con = init_connection()

st.title("Calculate Results")
with st.sidebar.expander("DELETE USER", expanded=False):
    st.error("Warning this is pernament")
    with st.form("delete user"):
        id_to_delete = st.number_input("Type ID of user to delete", value=0, step=1)
        
        verify_delete_text_input = st.text_input("Type 'Delete' in the field above to proceed")
        id_to_delete_button = st.form_submit_button("Delete User")

    if id_to_delete_button and verify_delete_text_input=="Delete":
        def delete_entry_from_balance_table(supabase):
            query=con.table("balance_table").delete().eq("id", id_to_delete).execute()
            return query
        query = delete_entry_from_balance_table(con)
        # Check if list query.data is empty or not
        if query.data:
            def main():
                delete_entry = delete_entry_from_balance_table(con)
            main()
            st.success('Thank you! This entry has been deleted from database!')
        else:
            st.warning("There is no entry with this id to delete!")


url_list=[]
with st.expander("From here you may display and calculate results from any entry of the database!", expanded=True):
    st.caption("Use the below search fields to filter the datatable!")
    #uploaded_file = st.file_uploader("Choose a file1")
    #@st.experimental_memo(ttl=300)
    def select_all_from_balance_table():
        query=con.table("balance_table").select("*").execute()
        return query
    query = select_all_from_balance_table()


    df_balance_table = pd.DataFrame(query.data)
    if not df_balance_table.empty:
        df_balance_table.columns = ['ID', 'Created At', 'Fullname', 'Age', 'Height', 'Weight', 'Email', 'Occupy', 'Filepath', 'Filename']
        col1, col2 = st.columns([2,2])
        with col2:
            occupy_search = st.text_input("Occupy:")
        with col1:
            fullname_search = st.text_input("Fullname:")
            

        if not occupy_search and not fullname_search :
            df_balance_table[['ID', 'Created At', 'Fullname', 'Age', 'Height', 'Weight', 'Email', 'Occupy', 'Filepath', 'Filename']]
        
        elif fullname_search and not occupy_search :
            st.dataframe(df_balance_table[df_balance_table['Fullname']== fullname_search])

        elif occupy_search and not fullname_search :
            st.dataframe(df_balance_table[df_balance_table['Occupy']== occupy_search])

        elif fullname_search and occupy_search :
            df_balance_table[(df_balance_table['Fullname'] == fullname_search) & (df_balance_table['Occupy'] == occupy_search)]
        
        elif occupy_search :
            df_balance_table[(df_balance_table['Occupy'] == occupy_search) ]
        
        elif fullname_search and occupy_search :
            df_balance_table[(df_balance_table['Occupy'] == occupy_search) & (df_balance_table['Fullname'] == fullname_search)]

        #url_id_number_input = st.number_input("Type the ID of the person you want to calculate results of the current trial.",value=0,step=1)


        # In this form, you type the id of the person to calculate speicific trial.
        
    else:
        st.write("There are no entries in the database! Please insert first!")

with st.sidebar.form("Type the ID of your link:", clear_on_submit=False):   
    url_id_number_input = st.number_input("Type the ID of your prerferred trial and Press Calculate Results:",value = 0,step= 1)
    id_submitted = st.form_submit_button("Calculate Results")
    # Querry to find the data row of specific ID
    if url_id_number_input:
        def select_filepath_from_specific_id():
            query=con.table("balance_table").select("*").eq("id", url_id_number_input).execute()
            return query
        query = select_filepath_from_specific_id()  
        # Make a list with all values from database depending on the condition. 
        url_list =  query.data
        # List with values depending on the querry
        if url_list:
            url = url_list[0]['filepath'].replace(" ", "%20")
            st.write("Person ID:", url_list[0]['id'],url_list[0]['filepath'])
        else:
            st.write("There is no entry with this ID")

#@st.cache(allow_output_mutation=True)
def get_data():
    if url_list:
        storage_options = {'User-Agent': 'Mozilla/5.0'}
        df = pd.read_csv(url_list[0]['filepath'].replace(" ", "%20"), storage_options=storage_options)
        W = 450
        L = 450
        df['ML'] = (W / 2) * (( df['Mass_2'] + df['Mass_3'] - df['Mass_1'] - df['Mass_4'] )) / ( df['Mass_1'] + df['Mass_2'] + df['Mass_3'] + df['Mass_4'] )
        df['AP'] = (L / 2) * (( df['Mass_2'] + df['Mass_1'] - df['Mass_3'] - df['Mass_4'] )) / ( df['Mass_1'] + df['Mass_2'] + df['Mass_3'] + df['Mass_4'] )
        
        df['Rows_Count'] = df.index
        N = len(df)

        # # Get the center of pressure on the x axis 
        # center_of_pressure_x = (W/2)*(C2 + C3 - C1 - C4)/(C1 + C2 + C3 + C4) 

        # # Get the center of pressure on the y axis 
        # center_of_pressure_y = (L/2)*(C2 + C1 - C3 - C4)/(C1 + C2 + C3 + C4) 

        df['Xn'] = df['ML'] - ( 1 / N ) * df['ML'].sum()

        df['Yn'] = df['AP'] - ( 1 / N ) * df['AP'].sum()

        
    return df

if url_list:
    df = get_data()
    min_time = int(df.index.min())
    max_time = int(df.index.max())
    min_ML = min(df['ML'])
    max_ML = max(df['ML'])
    selected_time_range = st.sidebar.slider('Select the time range, per 100', min_time, max_time, (min_time, max_time), 100)
    df_selected_model = (df.Rows_Count.between(selected_time_range[0], selected_time_range[1]) )
    df = pd.DataFrame(df[df_selected_model])
   
    #@st.cache  # No need for TTL this time. It's static data :)
    def make_charts():       
        fig = px.scatter(df, x="Xn", y="Yn", opacity= 0.4)
        fig.update_traces(marker={'size': 1})
        fig.add_trace(go.Scatter(x=[round(df['ML'].mean(),3)], y=[round(df['AP'].mean(),3)], mode = 'markers',
                        marker_symbol = 'circle', name="Zero Point" ,marker_color='red',
                        marker_size = 5))
        fig.update_layout(
             margin=dict(l=10, r=10, t=10, b=60),
             #paper_bgcolor="LightSteelBlue",
        )
        
        return fig

    fig = make_charts()



    col1,col2 = st.columns([2,1],gap='large')
    with col1:
        st.markdown("<h4 style='text-align: center; padding-top: 35px; color: Darkblue; font-weight:900'>Xn | Yn Chart</h1>", unsafe_allow_html=True)

        st.plotly_chart(fig,use_container_width=True)

        
    with col2:
        st.markdown("<h4 style='text-align: center; padding-top: 35px; color: Darkblue; font-weight:100'>Infos</h1>", unsafe_allow_html=True)
        st.write('Min & Max ML:', round(min(df['ML']),3),'&', round(max(df['ML']),3))
        st.write('Min & Max AP:', round(min(df['AP']),3),'&', round(max(df['AP']),3))
        st.write('Mean ML & AP:', round(df['ML'].mean(),3),'&', round(df['AP'].mean(),3))
        st.write('Min & Max Xn::', round(min(df['Xn']),3),'&', round(max(df['Xn']),3))
        st.write('Min & Max Yn::', round(min(df['Yn']),3),'&', round(max(df['Yn']),3))
        st.write('Mean Xn & Yn:', round(df['Xn'].mean(),3),'&', round(df['Yn'].mean(),3))


        

    # st.write("")
    # st.sidebar.write('Time range from', min(df['Rows_Count']), 'to', max(df['Rows_Count']), 'ms')
    # st.sidebar.write('Min ML:', min(df['ML']))
    # st.sidebar.write('Max AP:', max(df['ML']))
    # st.sidebar.write('Min ML:',  min(df['AP']))
    # st.sidebar.write('Max AP:',  max(df['AP']))

    # col1,col2 = st.columns(2)
    # with col1:
    #     st.write('The Min & Max ML values of this time range are:', round(min(df['ML']),3), round(max(df['ML']),3))
    #     st.write('The Min & Max AP values of this time range are:', round(min(df['AP']),3), round(max(df['AP']),3))
    #     st.write('The Mean ML values of this time range are:', round(df['ML'].mean(),3))
    #     st.write('The Mean AP values of this time range are:', round(df['AP'].mean(),3))


    # with col2:
    #     st.write('The Min & Max Xn values of this time range are:', round(min(df['Xn']),3), round(max(df['Xn']),3))
    #     st.write('The Min & Max Yn values of this time range are:', round(min(df['Yn']),3), round(max(df['Yn']),3))
    #     st.write('The Mean ML values of this time range are:', df['Xn'].mean())
    #     st.write('The Mean AP values of this time range are:', df['Yn'].mean())

    


    selected_clear_columns = st.multiselect(
    label='What column do you want to display', default=('Time','Xn', 'Yn'), help='Click to select', options=df.columns)
    st.write(df[selected_clear_columns])
    st.download_button(
        label="Export Table",
        data=df[selected_clear_columns].to_csv(),
        file_name='df.csv',
        mime='text/csv',
    )

