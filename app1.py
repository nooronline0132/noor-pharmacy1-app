import streamlit as st
import pandas as pd
import os
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy V2", layout="wide")

# Windows XP Style Styling
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .header { background-color: #0053E1; padding: 20px; text-align: center; color: white; border-bottom: 5px solid #F9B000; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; }
    .bill-box { background-color: #F0F4F8; padding: 20px; border: 2px solid #0053E1; border-radius: 10px; color: black; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
def load_data():
    # Updating file names to match your GitHub
    p_file = "Products.xlsx"
    a_file = "AccountCodes.xlsx"
    
    try:
        if os.path.exists(p_file) and os.path.exists(a_file):
            # Reading directly from Excel files
            p_df = pd.read_excel(p_file)
            a_df = pd.read_excel(a_file)
            return p_df, a_df
    except Exception as e:
        st.error(f"File parhne mein masla: {e}")
    return None, None

prods, accounts = load_data()

if 'cart' not in st.session_state:
    st.session_state.cart = []

st.markdown("<div class='header'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)

if prods is not None:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("🛒 Billing Entry")
        # Using columns from your Excel
        cust_list = accounts['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        p_name = st.selectbox("Search Medicine", [""] + list(prods['ProductName'].dropna().unique()))
        
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            st.info(f"Price: Rs {item['RetailPrice']} | Salt: {item['SaltName']}")
            
            qty = st.number_input("Quantity", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                total = float(item['RetailPrice']) * qty
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": total})
                st.rerun()

    with col2:
        st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
        st.subheader("📋 Final Bill")
        st.write(f"**Customer:** {selected_cust}")
        
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            grand_total = df_cart['Total'].sum()
            st.write(f"### Total: Rs {grand_total}")
            
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Excel files nahi milin! Please ensure Products.xlsx and AccountCodes.xlsx are in GitHub.")
