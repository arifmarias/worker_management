import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
from datetime import date
import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.switch_page_button import switch_page
import streamlit_shadcn_ui as ui
import database as db

# -------------- SETTINGS --------------
currency = "RM"
page_title = "Worker Management - AD HCare"
page_icon = ":people_holding_hands:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"
# --------------------------------------
st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""---""")
with st.container(): 
    left_column, middle_column, right_column = st.columns(3)
    worker = left_column.button("🙆🏻‍♂️ Worker Profile")
    salary = middle_column.button("💵 Salary Information")
    report = right_column.button("📈 Reports")
    if worker:
        switch_page("WORKER PROFILE")
    if salary:
        switch_page("SALARY INFO")
    if report:
        switch_page("REPORT")
st.markdown("""---""")
# ----- GET ALL WORKER DATA FROM WORKER_PROFILE ------------
items = db.fetch_all_periods()
df_info = pd.DataFrame(items)
# ----- GET ALL WORKER DATA FROM WORKER_SALARY ------------
items_salary = db.fetch_all_salary()
df_salary = pd.DataFrame(items_salary)

# --- GET CURRENT MONTH YEAR ---
years = [datetime.today().year, datetime.today().year + 1]
months = list(calendar.month_name[1:])
current_date = date.today()
current_year = current_date.year
current_month = current_date.month
current_day = current_date.day
current_year_month = str(current_year) + "-" + str(current_month)
total_salary_remain = 0
total_pay_out = 0
if not df_info.empty:
    total_number_of_workers = df_info['worker_name'].drop_duplicates().count()
    total_base_salary = df_info['worker_base_salary'].sum()
    for items in df_info.worker_name.unique():
        view_df = df_salary[(df_salary['worker_name'] == items) & (df_salary['year_month']==current_year_month)]
        if not view_df.empty:
            match_df = pd.DataFrame(view_df.sort_values("salary_remain",ascending=True).head(1))
            salary_remain = match_df["salary_remain"].sum()
            pay_out = view_df["today_pay"].sum()
            total_salary_remain +=salary_remain
            total_pay_out +=pay_out
    
    

    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(title="Number of Workers", content=str(total_number_of_workers), description="Working with AD HCARE ", key="card1")
    with cols[1]:
        ui.metric_card(title="Total Salary", content=f"RM {total_base_salary:,}", description="For All Workers", key="card2")
    with cols[2]:
        ui.metric_card(title="Paid Out", content=f"RM {total_pay_out:,}", description="This Month", key="card3")