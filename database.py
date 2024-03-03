import streamlit as st  # pip install streamlit
from deta import Deta  # pip install deta
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")


#DETA_KEY = "c06szqbzn1w_B32r3xDfsePCuuyvgP19q5oW8gRmFxBN"

# Load the environment variables
DETA_KEY = st.secrets["DETA_KEY"]
# Initialize with a project key
deta = Deta(DETA_KEY)

# This is how to create/connect a database
db_worker = deta.Base("worker_profile")
db_salary = deta.Base("Worker_salary")

def insert_data(current,input_date,period,
                worker_name, worker_joining_date, 
                worker_gender, worker_phone_number, 
                worker_passport, worker_pass_expiry, 
                worker_visa_expiry,
                worker_current_company,
                worker_current_workplace, 
                worker_state,worker_pic, 
                worker_currentcompany_joindate, 
                worker_base_salary, comments):
    return db_worker.put({"key": current,"input_date": input_date,"period": period,
                   "worker_name":worker_name, 
                    "worker_joining_date":worker_joining_date, 
                    "worker_gender":worker_gender,
                    "worker_phone_number":worker_phone_number, 
                    "worker_passport":worker_passport, 
                    "worker_pass_expiry":worker_pass_expiry, 
                    "worker_visa_expiry":worker_visa_expiry, 
                    "worker_current_company":worker_current_company,
                    "worker_current_workplace":worker_current_workplace, 
                    "worker_state":worker_state,
                    "worker_pic":worker_pic, 
                    "worker_currentcompany_joindate":worker_currentcompany_joindate, 
                    "worker_base_salary":worker_base_salary, 
                    "comments":comments
                   })


def fetch_all_periods():
    """Returns a dict of all periods"""
    res = db_worker.fetch()
    return res.items

def update_info(current,input_date,period,
                worker_name, worker_joining_date, 
                worker_gender, worker_phone_number, 
                worker_passport, worker_pass_expiry, 
                worker_visa_expiry,
                worker_current_company,
                worker_current_workplace, 
                worker_state,worker_pic, 
                worker_currentcompany_joindate, 
                worker_base_salary, comments):
    return db_worker.update({"input_date": input_date,"period": period,
                   "worker_name":worker_name, 
                    "worker_joining_date":worker_joining_date, 
                    "worker_gender":worker_gender,
                    "worker_phone_number":worker_phone_number, 
                    "worker_passport":worker_passport, 
                    "worker_pass_expiry":worker_pass_expiry, 
                    "worker_visa_expiry":worker_visa_expiry, 
                    "worker_current_company":worker_current_company,
                    "worker_current_workplace":worker_current_workplace, 
                    "worker_state":worker_state,
                    "worker_pic":worker_pic, 
                    "worker_currentcompany_joindate":worker_currentcompany_joindate, 
                    "worker_base_salary":worker_base_salary, 
                    "comments":comments
                   },str(current))
# ---- WORKER SALARY DB ----- 
def insert_salary_data(current,payment_date,w_name,year_month,
                       today_pay,payment_purpose,salary_remain):
    return db_salary.put({
                   "key": current,"payment_date": payment_date,
                   "worker_name":w_name,
                   'year_month':year_month,
                   'today_pay':today_pay,
                   'payment_purpose':payment_purpose,
                   'salary_remain':salary_remain
                    
                   })

def fetch_all_salary():
    """Returns a dict of all periods"""
    res = db_salary.fetch()
    return res.items