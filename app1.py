import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS (Visibility & Print) ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    h1, h2, h3, p, label { color: black !important; }
    .header { background-color: #0053E1; padding: 10px; text-align: center; color: white !important; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; }
    @media print {
        .no-print, header, footer, .stSidebar, div[data-testid="stToolbar"] { display: none !important; }
        .print-only { display: block !important; width: 100%; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA (FAST) ---
@st.cache_data
def load_data():
    try:
        p_df = pd.read_excel("Products.xlsx")
        a_df = pd.read_excel("AccountCodes.xlsx")
        return p_df, a_df
    except:
        return pd.DataFrame(), pd.DataFrame()

if 'p_data' not in st.session_state:
    p_df, a_df = load_data()
    st.session_state.p_data = p_df
    st.session_state.a_data = a_df

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- MENU ---
st.sidebar.title("Noor Pharmacy")
choice = st.sidebar.radio("Go to:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("New Entry")
        cust_list = st.session_state.a_data['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        p_name = st.selectbox("Search Product", [""] + list(st.session_state.p_data['ProductName'].dropna().unique()))
        
        if p_name:
            item = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_name].iloc[0]
            st.write(f"**Rate:** Rs {item['RetailPrice']} | **Stock:** {item['StockInHand']}")
            qty = st.number_input("Quantity", min_value=1, value=1)
            
            if st.button("➕ Add to Bill"):
                total = round(float(item['RetailPrice']) * qty, 2)
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": total})
                st.rerun()

    with col
