
import os
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import ftplib
import tempfile
from pathlib import Path
import numpy as np


############# ############## PAGE 2 INSERT TO DATABASE USER+TRIAL ############## ############ #############################
st.set_page_config(
    page_title="Tefaa Metrics",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

#Make the connection with Supabase - Database:
@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    #client = create_client(url, key)
    return create_client(url, key)
con = init_connection()


st.sidebar.info("Hello, lets try to insert a new entry to database!!!!!!")
st.sidebar.info("- Give the full name of the person!")
st.sidebar.info("- Give the email adress of the person!")
st.sidebar.info("- Give the occupy of the person!")
st.sidebar.info("- Choose the proper kind of trial!")
st.sidebar.info("- Choose the file of the trial. Please use only undescrores, not spaces in the file name!")
st.sidebar.info("- Click on Show All Entries to check the database!")

st.title("Import Entry to Database!")


def select_all_from_balance_table():
    query=con.table("balance_table").select("*").execute()
    return query
query = select_all_from_balance_table()

df_balance_table = pd.DataFrame(query.data)

df_balance_table_unique_values = df_balance_table.copy()

fullname_input = st.selectbox("Select a person from the database or fill in the fields below. " , (df_balance_table_unique_values['fullname']))
row_index = df_balance_table_unique_values.index[df_balance_table_unique_values['fullname']==fullname_input].tolist()
st.markdown("""---""")

#Create the Form to submit data to database:
with st.form("Create a new entry", clear_on_submit=False):
    col1,col2,col3 = st.columns(3)
    with col1:
        fullname = st.text_input("Fullname", value = df_balance_table_unique_values.loc[row_index[0]]['fullname'])
        age = st.number_input("Age", value = int(df_balance_table_unique_values.loc[row_index[0]]['age']), min_value=0, max_value=100, step=1)
        kind_of_trial = st.selectbox("Kind of Trial", ('-','SB Bilateral', 'SB Unilateral (LL)','SB Unilateral (RL)','SB Unilateral (RL)', 'Tandem' ))
    with col2:
        weight = st.number_input("Weight in kg", value = df_balance_table_unique_values.loc[row_index[0]]['weight'])
        email = st.text_input("Email address")
        occupy = st.text_input("Occupy", value = df_balance_table_unique_values.loc[row_index[0]]['occupy'])
    with col3:
        height = st.number_input("Height in cm", value = df_balance_table_unique_values.loc[row_index[0]]['height'])
        instructor = st.text_input("Instructor")
        description = st.text_area('More Description (optional)')
    filepath = st.file_uploader("Choose a file")
    submitted = st.form_submit_button("Submit values")


    if submitted:
        
        if fullname and age and height and weight and occupy !='-' :
            
            filename_with_extension = filepath.name
            # Filename without extension
            filename = os.path.splitext(filename_with_extension)[0]

            def storage_connection():
                hostname = st.secrets["hostname"]
                username = st.secrets["username"]
                password = st.secrets["password"]
                
                return hostname,username,password
            hostname,username,password = storage_connection()
            
            ftp = ftplib.FTP(hostname,username,password)
            
            
            # This is the method to take the temporary path of the uploaded file and the value in bytes of it.
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                fp_PosixPath = Path(tmp_file.name)
                fp_PosixPath.write_bytes(filepath.getvalue())
            # This is to take the str of PosixPath.
            fp_str = str(fp_PosixPath)
            # This is our localfile's path in str.
            localfile = fp_str
            # This is the remote path of the server to be stored.
            remotefile='/sportsmetrics.geth.gr/storage/' + filename_with_extension

            # This is the method to store the localfile in remote server through ftp.
            with open(localfile, "rb") as file:
                ftp.storbinary('STOR %s' % remotefile, file)
            ftp.quit()
            
            filepath="https://sportsmetrics.geth.gr/storage/" + filename_with_extension
                     
            list = (fullname,email,occupy,filename)
            def add_entries_to_balance_table(supabase):
                value = {'fullname': fullname, "age": age, "height": height, "weight": weight , 'email': email, 'occupy': occupy, 
                         "filepath": filepath, 'filename': filename, 'kind_of_trial': kind_of_trial, 'description': description, 'instructor': instructor}
                data = supabase.table('balance_table').insert(value).execute()
            def main():
                new_entry = add_entries_to_balance_table(con)
            main()
            st.success('Thank you! A new entry has been inserted to database!')
            st.write(list)
        else:
            st.error("One of the field values is missing")
#@st.experimental_memo(ttl=600)
def select_all_from_balance_table():
    query=con.table("balance_table").select("*").execute()
    return query
balance_table_all = select_all_from_balance_table()
df_all_from_balance_table = pd.DataFrame(balance_table_all.data)


# url = st.text_input("Paste the desire url")
#
# if url:
#     storage_options = {'User-Agent': 'Mozilla/5.0'}
#     df = pd.read_csv(url,storage_options=storage_options)
#     st.write(df)






