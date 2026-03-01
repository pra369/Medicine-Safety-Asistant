import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
import datetime
import re

# --- CONFIG ---
CSV_FILE = "medicines.csv"

# --- LOAD CSV ---
try:
    df = pd.read_csv(CSV_FILE)
except:
    st.error("medicines.csv file sapdat nahiye. Kripaya ti upload kara.")
    st.stop()

# --- FUNCTION: Get top matches ---
def get_top_matches(user_input, n=3):
    matches = process.extract(user_input, df['Name'], scorer=fuzz.WRatio, limit=n)
    results = []
    for match in matches:
        med_name = match[0]
        med_info = df[df['Name'] == med_name].iloc[0]
        results.append({
            "Name": med_name,
            "Risk": med_info['Risk'],
            "SideEffects": med_info['SideEffects'],
            "Interaction": med_info['Interaction']
        })
    return results

# --- FUNCTION: Risk Color ---
def risk_color(risk):
    if risk.lower() == "high": return "🔴"
    elif risk.lower() == "medium": return "🟡"
    else: return "🟢"

# --- STREAMLIT UI ---
st.set_page_config(page_title="MedSafe AI", layout="wide")
st.title("💊 MedSafe AI - Medicine Safety Assistant")

# --- User Input Search ---
st.subheader("Search Medicine")
user_input = st.text_input("Aushadhache naav taka (उदा. Paracetamol):")

if st.button("Search"):
    if user_input:
        top_matches = get_top_matches(user_input)
        cols = st.columns(len(top_matches))
        for idx, med in enumerate(top_matches):
            with cols[idx]:
                st.markdown(f"### {risk_color(med['Risk'])} {med['Name']}")
                st.write(f"**Risk:** {med['Risk']}")
                st.write(f"**Side Effects:** {med['SideEffects']}")
                st.write(f"**Interaction:** {med['Interaction']}")
    else:
        st.warning("Kripaya naav type kara.")

st.markdown("---")
st.write("MedSafe AI © 2026")




