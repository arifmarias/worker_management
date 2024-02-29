import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
from datetime import date
import pandas as pd
import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit_shadcn_ui as ui
from streamlit_extras.switch_page_button import switch_page
import database as db

# -------------- SETTINGS --------------
currency = "RM"
page_title = "AD HCare Worker Profile"
page_icon = "🙎‍♂️"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

# -------------Home Page----------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
home = st.button("HOME 🏠")
if home:
    switch_page("HOME")
st.title(page_title + " " + page_icon)
# --------------------------------------

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])
d = date.today()
year = d.year
month = d.month
day = d.day




 # ----- GET ALL WORKER DATA FROM DATABASE------------
# items = db.fetch_all_periods()
# df = pd.DataFrame(items)
# --------------------------------------
# --- DATABASE INTERFACE ---
# def get_all_periods():
#     items = db.fetch_all_periods()
#     periods = [item["key"] for item in items]
#     return periods

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Employee/Worker Information","Search","Edit Worker Information"],
    icons=["person-plus-fill","search","pencil"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE WORKER INFO ---
if selected == "Employee/Worker Information":
    st.header("Worker Information Entry")
    #------------- STATES MALAYSIA----------------------
    my_states = ['Kuala Lumpur','Putrajaya','Labuan','Selangor','Malacca',\
    'Negeri Sembilan','Penang','Johor','Kedah','Kelantan','Perak','Pahang',\
    'Terengganu','Perlis','Sabah','Sarawak']
    "---"
    left, right = st.columns(2)
    with st.form("entry_form", clear_on_submit=True):
        with left:
            with st.expander("General Information"):
                worker_name = st.text_input("Worker Name")
                worker_joining_date = st.date_input("Employee Join Date")
                worker_gender = st.radio("Gender", options=("Male","Female"), horizontal=True)
                worker_phone_number = st.text_input("Personal Phone Number")
                
            with st.expander("Passport Information"):
                worker_passport = st.text_input("Passport Number")
                worker_pass_expiry = st.date_input("Passport Expiry Date")
                worker_visa_expiry = st.date_input("Visa Expiry Date")
                
        with right:
            with st.expander("Work Related Info"):
                worker_current_company = st.text_input("Current Working Company Name")
                worker_current_workplace = st.text_area("Address")
                worker_state = st.selectbox("State",my_states)
                worker_pic = st.text_area("Current Company PIC(Person-in-Charge) Details")
                worker_currentcompany_joindate = st.date_input("Current Company Join Date")
                
            with st.expander("Salary info"):
                worker_base_salary = st.number_input("Worker Current Base Salary")
               
        with st.expander("Other"):
            comments = st.text_input("Comments(if any)")
        
        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            if worker_name!="":
                input_date = str(day) + "/" + str(month) + "/" +str(year)
                year_month = str(year) + "_" + str(month)
                period = str(year)
                # Save Data into Database
                db.insert_data(str(datetime.utcnow()), input_date,period,
                            worker_name, str(worker_joining_date), worker_gender,
                            worker_phone_number, worker_passport, str(worker_pass_expiry), 
                            str(worker_visa_expiry), worker_current_company,
                            worker_current_workplace, worker_state,worker_pic, 
                            str(worker_currentcompany_joindate), worker_base_salary, 
                            comments
                            )
                # Success Message
                st.success("Data saved!")
            else:
                st.error('Worker Name Empty',icon='❌')

# --- SEARCH WORKER INFO ---

if selected == "Search":
    st.header("Search Worker Information")
     # ----- GET ALL WORKER DATA FROM DATABASE------------
    items = db.fetch_all_periods()
    df = pd.DataFrame(items)
    # --------------------------------------
   

    # ----- SEARCHBOX ------------
    worker_name = df["worker_name"].drop_duplicates().sort_values(ascending=False)
    lst_worker_name = list(worker_name)
    lst_worker_name.insert(0,"Select")
    w_name = st.selectbox(options = lst_worker_name, label="Select Worker Name")
    if w_name!='Select':
        selected_worker = df[df["worker_name"] == w_name]
        cols = st.columns(3)
        with cols[0]:
            ui.metric_card(title="Name", content=selected_worker["worker_name"].values[0], description="Join in "+selected_worker['worker_joining_date'].values[0]+","+selected_worker['worker_gender'].values[0]+"\n Mobile: "+selected_worker['worker_phone_number'].values[0], key="card1")
        with cols[1]:
            ui.metric_card(title="Passport Details", content=selected_worker["worker_passport"].values[0], description="Expiry Date: "+selected_worker['worker_pass_expiry'].values[0]+"\n Visa Expiry: "+selected_worker['worker_visa_expiry'].values[0], key="card2")
        with cols[2]:
            ui.metric_card(title="Workplace", content=selected_worker["worker_current_company"].values[0], description="Joined "+selected_worker['worker_currentcompany_joindate'].values[0]+"\n Address: "+selected_worker['worker_current_workplace'].values[0], key="card3")

# --- Edit WORKER INFO ---

if selected == "Edit Worker Information":
    st.header("Edit Worker Information")
    state_list = ['Kuala Lumpur','Putrajaya','Labuan','Selangor','Malacca',\
    'Negeri Sembilan','Penang','Johor','Kedah','Kelantan','Perak','Pahang',\
    'Terengganu','Perlis','Sabah','Sarawak']
     # ----- GET ALL WORKER DATA FROM DATABASE------------
    items = db.fetch_all_periods()
    df = pd.DataFrame(items)
# --------------------------------------
    # ----- SEARCHBOX ------------
    worker_name = df["worker_name"].drop_duplicates().sort_values(ascending=False)
    lst_worker_name = list(worker_name)
    lst_worker_name.insert(0,"Select")
    w_name = st.selectbox(options = lst_worker_name, label="Select Worker Name",index=0)
    if w_name!='Select':
        def state_list():
            st.session_state['state_list'] = ['Kuala Lumpur','Putrajaya','Labuan','Selangor','Malacca',\
                                            'Negeri Sembilan','Penang','Johor','Kedah','Kelantan','Perak','Pahang',\
                                            'Terengganu','Perlis','Sabah','Sarawak']
            
        selected_worker = df[df["worker_name"] == w_name]
        st.text_input("Worker Name",selected_worker['worker_name'].values[0])
        "---"
        #st.dataframe(selected_worker)
        left, right = st.columns(2)
        with st.form("edit_form", clear_on_submit=True):
            with left:
                with st.expander("General Information"):
                    worker_name = st.text_input("Worker Name",value=selected_worker['worker_name'].values[0],key=1,disabled=True)
                    #worker_joining_date = st.date_input("Employee Join Date",selected_worker['worker_joining_date'].values[0],key=selected_worker['key'].values[0])
                    worker_gender = st.radio("Gender", options=("Male","Female"), horizontal=True)
                    worker_phone_number = st.text_input("Personal Phone Number",selected_worker['worker_phone_number'].values[0],key=2)
                    
                with st.expander("Passport Information"):
                    worker_passport = st.text_input("Passport Number",selected_worker['worker_passport'].values[0],key=3)
                    #worker_pass_expiry = st.date_input("Passport Expiry Date",selected_worker['worker_pass_expiry'].values[0])
                    #worker_visa_expiry = st.date_input("Visa Expiry Date",selected_worker['worker_visa_expiry'].values[0])
                    #uploaded_file = st.file_uploader("Upload Passport with Visa Page(.pdf)")
            with right:
                with st.expander("Work Related Info"):
                    worker_current_company = st.text_input("Current Working Company Name",selected_worker['worker_current_company'].values[0],key=4)
                    worker_current_workplace = st.text_area("Address",selected_worker['worker_current_workplace'].values[0],key=6)
                    worker_state = st.selectbox("State",options=selected_worker['worker_state'],on_change= state_list,key='first_sb')
                    worker_state_new = st.selectbox("State",options=st.session_state['state_list'],key='second_sb')
                    worker_pic = st.text_area("Current Company PIC(Person-in-Charge) Details",selected_worker['worker_pic'].values[0],key=7)
                   # worker_currentcompany_joindate = st.date_input("Current Company Join Date",selected_worker['worker_currentcompany_joindate'].values[0])
                    
                with st.expander("Salary info"):
                    worker_base_salary = st.number_input("Worker Current Base Salary",selected_worker['worker_base_salary'].values[0])
                
            with st.expander("Other"):
                comments = st.text_input("Comments(if any)",selected_worker['comments'].values[0],key=5)
            "---"
            submitted = st.form_submit_button("Update Data")
    