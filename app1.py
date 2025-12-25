import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy V2", layout="wide")

# Windows XP Style Theme
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .header { background-color: #0053E1; padding: 20px; text-align: center; color: white; border-bottom: 5px solid #F9B000; font-family: 'Tahoma'; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; border: 2px solid #1B5E20; width: 100%; height: 3em; }
    .bill-box { background-color: #F0F4F8; padding: 15px; border: 1px solid #0053E1; border-radius: 5px; color: black; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
def load_data():
    p_file = "Products.xlsx - Products.csv"
    a_file = "AccountCodes.xlsx - AccountCodes.csv"
    if os.path.exists(p_file) and os.path.exists(a_file):
        #
        p_df = pd.read_csv(p_file)
        a_df = pd.read_csv(a_file)
        return p_df, a_df
    return None, None

prods, accounts = load_data()

st.markdown("<div class='header'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)

if prods is not None:
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("🛒 Billing")
        # Column 'Description' used for customers
        cust = st.selectbox("Select Customer", accounts['Description'].dropna().unique())
        
        # Column 'ProductName' used for products
        p_name = st.selectbox("Search Medicine", [""] + list(prods['ProductName'].dropna().unique()))
        
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            st.info(f"Price: Rs {item['RetailPrice']} | Packing: {item['Packing']} | Formula: {item['SaltName']}")
            qty = st.number_input("Quantity", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                st.success(f"{p_name} Added!")

    with col2:
        st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
        st.subheader("📋 Final Bill")
        st.write(f"**Customer:** {cust}")
        st.write("---")
        st.markdown("### Total: Rs 0.00")
        st.button("✅ FINALIZE & WHATSAPP")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Files nahi milin! Kya aapne GitHub par files upload kar di hain?")
