import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    .header { background-color: #0053E1; padding: 10px; text-align: center; color: white; border-bottom: 5px solid #F9B000; }
    h1, h2, h3, p, label { color: black !important; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; }
    /* Print Styling */
    @media print {
        .no-print, .stSidebar, header, footer, div[data-testid="stToolbar"] { display: none !important; }
        .print-only { display: block !important; width: 100%; position: absolute; top: 0; left: 0; }
        .stApp { background-color: white !important; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA (FAST) ---
@st.cache_data
def load_data():
    try:
        # Loading your Excel files
        p_df = pd.read_excel("Products.xlsx")
        a_df = pd.read_excel("AccountCodes.xlsx")
        return p_df, a_df
    except:
        return pd.DataFrame(), pd.DataFrame()

# Initialize Session Data
if 'p_data' not in st.session_state:
    p_df, a_df = load_data()
    st.session_state.p_data = p_df
    st.session_state.a_data = a_df

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- MENU NAVIGATION ---
st.sidebar.title("Noor Pharmacy")
# Adding Logo to Sidebar
try: st.sidebar.image("Noor Pharmacy logo.jpg", width=150)
except: pass

choice = st.sidebar.radio("Go to:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# Initialize variable to avoid NameError
selected_cust = "Cash Sales"

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_
