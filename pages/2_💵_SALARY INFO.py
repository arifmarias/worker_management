import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
from datetime import date
import pandas as pd
import numpy as np
import database as db

import plotly.graph_objects as go  # pip install plotly
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
import streamlit_shadcn_ui as ui

# -------------- SETTINGS --------------
currency = "RM"
page_title = "AD HCare Salary Management"
page_icon = "💵"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------

# -------------Home Page----------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
home = st.button("HOME 🏠")
if home:
    switch_page("HOME")
st.title(page_title + " " + page_icon)
# --------------------------------------

# --- GET CURRENT MONTH YEAR ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day
current_year_month = str(current_year) + "-" + str(current_month)

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
    options=["Salary Payment","Salary Info"],
    icons=["bank2","search"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)
# ----- GET ALL WORKER DATA FROM WORKER_PROFILE ------------
items = db.fetch_all_periods()
df_info = pd.DataFrame(items)
# ----- GET ALL WORKER DATA FROM WORKER_SALARY ------------
items_salary = db.fetch_all_salary()
df_salary = pd.DataFrame(items_salary)
# ----- REMAIN SALARY ------------
salary_remain = 0
worker_name_update = ""
# --- INPUT & SAVE WORKER SALARY INFO ---
if selected == "Salary Payment":
    st.header("Payment Entry")
    "---"
    # ----- SEARCHBOX FOR WORKER------------
    worker_name = df_info["worker_name"].drop_duplicates().sort_values(ascending=True)
    lst_worker_name = list(worker_name)
    lst_worker_name.insert(0,"Select")
    w_name = st.selectbox(options = lst_worker_name, label="Select Worker Name")
    if w_name!='Select':
        selected_worker = df_info[df_info["worker_name"] == w_name]
        base_salary = selected_worker['worker_base_salary'].values[0]
        #st.subheader("Current Base Salary: "+f"RM {selected_worker['worker_base_salary'].values[0]:,}")
        worker_name_update = selected_worker['worker_name'].values[0]
        # -------------- PAYMENT DATE ------------------------
        pay_date = st.date_input("Payment Date")
        year = pay_date.year
        month = pay_date.month
        day = pay_date.day
        payment_date = str(day) + "/" + str(month) + "/" +str(year) 
        year_month = str(year) + "-" + str(month)
        # -------------- REMAINING SALARY ------------------------
        if not df_salary.empty:
            match_df = df_salary[(df_salary['worker_name']==w_name)&(year_month==df_salary['year_month'])]
            if not match_df.empty:
                match_df = pd.DataFrame(match_df.sort_values("salary_remain").head(1))
                salary_remain = match_df["salary_remain"].values[0]
                cols = st.columns(2)
                with cols[0]:
                    ui.metric_card(title="Base Salary", content=f"RM {selected_worker['worker_base_salary'].values[0]:,}", key="card1")
                with cols[1]:
                    ui.metric_card(title="Remining Salary, "+ calendar.month_name[month], content=f"RM {salary_remain:,}", key="card2")
                    #st.subheader("Remining Salary for Selected Month: "+f"RM {salary_remain:,}")
        
        with st.form("entry_form", clear_on_submit=True):       
            cols = st.columns(2)
            with cols[0]:
                today_pay = st.number_input("Today's Payment ⋆")
            with cols[1]:
                payment_purpose = st.selectbox("Payment Purpose ⋆",("Select","Salary Payment","Advance Salary Payment","Other Purposes"))
            
            submitted = st.form_submit_button("Save Data")
            
            if submitted:
                if payment_purpose == 'Select' or today_pay == 0:
                    st.error('Missing Data',icon='❌')
                else:
                    salary_remain = 0.0
                    if df_salary.empty:
                        salary_remain = base_salary - today_pay
                        db.insert_salary_data(str(datetime.utcnow()), 
                                          payment_date,w_name,year_month,
                                          today_pay,payment_purpose,salary_remain)
                    else:
                        match_df = df_salary[(df_salary['worker_name']==w_name)&(year_month==df_salary['year_month'])]
                        if not match_df.empty:
                            match_df = pd.DataFrame(match_df.sort_values("salary_remain").head(1))
                            salary_remain = match_df["salary_remain"].values[0]
                            salary_remain = salary_remain - today_pay
                            if salary_remain <= 0:
                                st.warning('Worker is taking More Advance than his Base Salary',icon='🔥')
                            db.insert_salary_data(str(datetime.utcnow()), 
                                          payment_date,w_name,year_month,
                                          today_pay,payment_purpose,salary_remain)
                        else:
                            salary_remain = base_salary - today_pay
                            db.insert_salary_data(str(datetime.utcnow()), 
                                          payment_date,w_name,year_month,
                                          today_pay,payment_purpose,salary_remain)   
                    
                    st.success("Data saved!")
                    
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     # ----- RETRIVE WORKER DATAFRAME ------------
#     selected_worker = df_info[df_info["worker_name"] == w_name]
#     if w_name!='Select':
#         # --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
#         years = [datetime.today().year, datetime.today().year + 1]
#         months = list(calendar.month_name[1:])
#         pay_date = st.date_input("Payment Date")
#         year = pay_date.year
#         month = pay_date.month
#         day = pay_date.day
#         left, right = st.columns(2)
#         with st.form("entry_form", clear_on_submit=True):
#             st.subheader("Base Salary: "+f"RM {selected_worker['worker_base_salary'].values[0]:,}")
#             cols = st.columns(2)
#             with cols[0]:
#                 today_pay = st.number_input("Today's Payment ⋆")
#             with cols[1]:
#                 payment_purpose = st.selectbox("Payment Purpose ⋆",("Select","Salary Payment","Advance Salary Payment","Other Purposes"))
                
#             "---"
#             submitted = st.form_submit_button("Save Data")
            
#             if submitted:
#                 if payment_purpose == 'Select' or today_pay == 0:
#                     st.error('Data Missing',icon='❌')
#                 else:    
#                     input_date = str(day) + "/" + str(month) + "/" +str(year)
#                     year_month = str(year) + "_" + str(month)
#                     period = str(year)
#                     # Save Data into Database
#                     base_salary = selected_worker['worker_base_salary'].values[0]
#                     # st.write(type(base_salary))
#                     db.insert_salary_data(
#                                     worker_name
#                                     )
                       
                        
#                     # Success Message
#                     st.success("Data saved!")

# # --- SEARCH WORKER INFO ---

# if selected == "Salary Info":
#     st.header("Search Worker Information")
#     # ----- GET ALL GOAT DATA FROM DATABASE------------
#     items = db.fetch_all_periods()
#     df = pd.DataFrame(items)

#     # ----- SEARCHBOX ------------
#     worker_name = df["worker_name"].drop_duplicates().sort_values(ascending=False)
#     lst_worker_name = list(worker_name)
#     lst_worker_name.insert(0,"Select")
#     w_name = st.selectbox(options = lst_worker_name, label="")
#     if w_name!='Select':
#         selected_worker = df[df["worker_name"] == w_name]
#         cols = st.columns(3)
#         with cols[0]:
#             ui.metric_card(title="Name", content=selected_worker["worker_name"].values[0], description="Join in "+selected_worker['worker_joining_date'].values[0]+","+selected_worker['worker_gender'].values[0]+"\n Mobile: "+selected_worker['worker_phone_number'].values[0], key="card1")
#         with cols[1]:
#             ui.metric_card(title="Passport Details", content=selected_worker["worker_passport"].values[0], description="Expiry Date: "+selected_worker['worker_pass_expiry'].values[0]+"\n Visa Expiry: "+selected_worker['worker_visa_expiry'].values[0], key="card2")
#         with cols[2]:
#             ui.metric_card(title="Workplace", content=selected_worker["worker_current_company"].values[0], description="Joined "+selected_worker['worker_currentcompany_joindate'].values[0]+"\n Address: "+selected_worker['worker_current_workplace'].values[0], key="card3")

    