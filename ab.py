""" Prototype for AB testing, to check ingestion into Streamlit Cloud """

import streamlit as st
import pandas as pd
from datetime import datetime

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
    df = pd.DataFrame(responses)
    df["timestamp"] = datetime.now()
    df.to_csv("responses.csv", mode="a", header=not pd.read_csv("responses.csv").empty if "responses.csv" in df else True, index=False)
    st.success("Thank you! Your responses have been recorded.")

