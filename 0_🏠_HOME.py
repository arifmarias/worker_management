import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
import pandas as pd
import numpy as np

import plotly.express as px
import streamlit as st  # pip install streamlit
from streamlit_option_menu import option_menu  # pip install streamlit-option-menu
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from streamlit_extras.switch_page_button import switch_page
import streamlit_shadcn_ui as ui
#import database as db  # local import

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