import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- DESIGN & PRINT LOGIC ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    .header { background-color: #0053E1; color: white !important; padding: 20px; text-align: center; border-bottom: 5px solid #F9B000; margin-bottom: 20px; }
    h1, h2, h3, p, label { color: black !important; font-weight: bold; }
    
    /* Buttons Design */
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; border-radius: 8px; height: 3em; }
    
    /* PRINTING FIX: Sirf Receipt Nazar Aayegi */
    @media print {
        .no-print, header, footer, .stSidebar, div[data-testid="stToolbar"] { display: none !important; }
        .print-only { display: block !important; width: 100%; border: none !important; }
        .stApp { background-color: white !important; }
    }
    .print-only { display: none; }
