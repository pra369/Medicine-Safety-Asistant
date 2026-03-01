import streamlit as st
import pandas as pd
from rapidfuzz import process, fuzz
from PIL import Image
import pytesseract
import datetime
import re

# --- CONFIG ---
CSV_FILE = "medicines.csv"

# --- LOAD CSV ---
try:
    df = pd.read_csv(CSV_FILE)
except:
    st.error("❌ medicines.csv file sapdat nahiye!")
    st.stop()

# --- FUNCTION: Risk Color ---
def risk_color(risk):
    r = str(risk).lower()
    if "high" in r: return "🔴"
    elif "medium" in r: return "🟡"
    else: return "🟢"

# --- FUNCTION: Expiry Check ---
def check_expiry(text):
    patterns = [r'(\d{2}/\d{2})', r'(\d{2}/\d{4})']
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            exp_str = match.group(1)
            try:
                if len(exp_str.split("/")[-1]) == 2:
                    exp_date = datetime.datetime.strptime(exp_str, "%m/%y")
                else:
                    exp_date = datetime.datetime.strptime(exp_str, "%m/%Y")
                return (exp_date < datetime.datetime.now(), exp_str)
            except: pass
    return None, None

# --- UI SETUP ---
st.set_page_config(page_title="MedSafe AI Advanced", layout="wide")
st.title("💊 MedSafe AI - Medicine Safety Assistant")

# 1️⃣ OCR Section
st.subheader("1️⃣ Prescription OCR & Expiry Check")
uploaded_file = st.file_uploader("Upload prescription/strip image", type=["png","jpg","jpeg"])
ocr_text = ""
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=250, caption="Uploaded Image")
    with st.spinner("Extracting text..."):
        ocr_text = pytesseract.image_to_string(img)
    
    st.text_area("OCR Extracted Text:", value=ocr_text, height=100)
    
    is_expired, date_found = check_expiry(ocr_text)
    if is_expired is True: 
        st.error(f"🚨 ALERT: Medicine Expired! (Detected Date: {date_found})")
    elif is_expired is False: 
        st.success(f"✅ Safe: Not Expired. (Detected Date: {date_found})")

# 2️⃣ Search Section
st.subheader("2️⃣ Search Medicine & Match Score")
user_input = st.text_input("Enter medicine name:", value=ocr_text[:20] if ocr_text else "")

if st.button("Search"):
    if user_input:
        # RapidFuzz for Percentage Match
        matches = process.extract(user_input, df['Name'], scorer=fuzz.WRatio, limit=3)
        
        cols = st.columns(3)
        for idx, match in enumerate(matches):
            med_name = match[0]
            score = round(match[1], 1) # Percentage Match
            med_info = df[df['Name'] == med_name].iloc[0]
            
            with cols[idx]:
                st.info(f"### {risk_color(med_info['Risk'])} {med_name}")
                st.metric("Match Score", f"{score}%")
                st.write(f"**Risk Level:** {med_info['Risk']}")
                st.write(f"**Side Effects:** {med_info['SideEffects']}")
                st.write(f"**Interactions:** {med_info['Interaction']}")
    else:
        st.warning("Please enter a name or upload an image.")

st.markdown("---")
st.caption("MedSafe AI © 2026 | Educational & Non-Diagnostic")

