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

questions = [f"Question {i+1}: Lorem ipsum dolor sit amet?" for i in range(20)]
options = ["Option A", "Option B", "Option C", "Option D"]

responses = []

with st.form("ranking_form"):
    for q_idx, question in enumerate(questions):
        st.markdown(f"### {question}")
        scores = {}
        cols = st.columns(4)
        for i, opt in enumerate(options):
            with cols[i]:
                scores[opt] = st.selectbox(
                    f"{opt} (0-2)", options=[0, 1, 2], key=f"q{q_idx}_opt{i}"
                )
        comment = st.text_input("Comment (optional)", key=f"q{q_idx}_comment")

        responses.append({
            "question": question,
            **{f"{opt}_score": scores[opt] for opt in options},
            "comment": comment
        })

    submitted = st.form_submit_button("Submit")

if submitted:
    # Append rows
    for response in responses:
        sheet.append_row(list(response.values()))


