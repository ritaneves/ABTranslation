""" Prototype for AB testing, to check ingestion into Streamlit Cloud """

import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets auth
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

creds_dict = json.loads(st.secrets["google"]["credentials"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Open sheet
sheet = client.open("ABTest").sheet1

st.set_page_config(page_title="Ranking Experiment", layout="centered")

st.title("Marking LLM Translations of Short Sentences")
st.markdown("""
Welcome! This experiment presents you with 20 questions.  
Each question has four options — your task is to **assign a score (0 to 2)** to each one  
(based on how good or bad you think it is), and optionally leave a **comment**.

Your responses will help us evaluate human preferences.
""")

# Setup
NUM_QUESTIONS = 20
NUM_OPTIONS = 4
SCORE_VALUES = [0, 1, 2]

# UI
st.title("Detailed Option Ranking Survey")
st.markdown("Please rate **each** option per question. Comments are optional. All scores are required.")

answers = []

for q_num in range(1, NUM_QUESTIONS + 1):
    st.markdown(f"### Question {q_num}")
    q_scores = []
    for opt_num in range(1, NUM_OPTIONS + 1):
        score = st.selectbox(
            f"Q{q_num} Option {opt_num} Score",
            SCORE_VALUES,
            key=f"q{q_num}_opt{opt_num}"
        )
        q_scores.append(score)
    comment = st.text_input(f"Optional comment for Q{q_num}", key=f"q{q_num}_comment")
    answers.extend(q_scores)
    answers.append(comment.strip())

# Submit
if st.button("Submit"):
    # Validate all option scores are filled
    if any(st.session_state.get(f"q{q}_opt{o}") is None for q in range(1, NUM_QUESTIONS+1) for o in range(1, NUM_OPTIONS+1)):
        st.error("Please fill in all option scores before submitting.")
    else:
        timestamp = datetime.now().isoformat()
        row = [timestamp] + answers
        sheet.append_row(row)
        st.success("Your responses were submitted successfully!")
        st.balloons()


