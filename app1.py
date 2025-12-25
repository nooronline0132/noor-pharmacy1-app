import streamlit as st
import pandas as pd
import os
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy V2", layout="wide")

# Windows XP Theme
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .header { background-color: #0053E1; padding: 20px; text-align: center; color: white; border-bottom: 5px solid #F9B000; font-family: 'Tahoma'; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; border: 2px solid #1B5E20; width: 100%; height: 3em; }
    .bill-box { background-color: #F0F4F8; padding: 20px; border: 2px solid #0053E1; border-radius: 10px; color: black; }
    .total-text { font-size: 30px; color: #D32F2F; font-weight: bold; text-align: right; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
def load_data():
    p_file = "Products.xlsx - Products.csv"
    a_file = "AccountCodes.xlsx - AccountCodes.csv"
    if os.path.exists(p_file) and os.path.exists(a_file):
        p_df = pd.read_csv(p_file)
        a_df = pd.read_csv(a_file)
        return p_df, a_df
    return None, None

prods, accounts = load_data()

# Session State for Cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

st.markdown("<div class='header'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)

if prods is not None:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("🛒 Billing Entry")
        
        # Customer selection
        cust_row = st.selectbox("Select Customer", accounts['Description'].dropna().unique())
        customer_info = accounts[accounts['Description'] == cust_row].iloc[0]
        cust_phone = str(customer_info['Phone']) if 'Phone' in customer_info else ""

        # Product selection
        p_name = st.selectbox("Search Medicine", [""] + list(prods['ProductName'].dropna().unique()))
        
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            st.info(f"Price: Rs {item['RetailPrice']} | Packing: {item['Packing']} | Stock: {item['StockInHand']}")
            
            c1, c2 = st.columns(2)
            qty = c1.number_input("Quantity", min_value=1, value=1)
            
            if st.button("➕ Add to Bill"):
                total_price = float(item['RetailPrice']) * qty
                st.session_state.cart.append({
                    "Item": p_name,
                    "Price": item['RetailPrice'],
                    "Qty": qty,
                    "Total": total_price
                })
                st.rerun()

    with col2:
        st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
        st.subheader("📋 Final Bill")
        st.write(f"**Customer:** {cust_row}")
        
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.dataframe(df_cart, use_container_width=True)
            
            grand_total = df_cart['Total'].sum()
            st.markdown(f"<div class='total-text'>Grand Total: Rs {grand_total:,.2f}</div>", unsafe_allow_html=True)
            
            if st.button("✅ FINALIZE & SEND WHATSAPP"):
                # Creating WhatsApp Message
                msg = f"Noor Pharmacy Bill\nCustomer: {cust_row}\n---\n"
                for i, row in df_cart.iterrows():
                    msg += f"{row['Item']} x {row['Qty']} = {row['Total']}\n"
                msg += f"---\nTotal Bill: Rs {grand_total}"
                
                encoded_msg = urllib.parse.quote(msg)
                # Cleaning phone number
                clean_phone = cust_phone.replace(" ", "").replace("-", "")
                if not clean_phone.startswith("92"): clean_phone = "92" + clean_phone.lstrip("0")
                
                wa_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"
                st.markdown(f'<a href="{wa_link}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px; font-weight:bold; cursor:pointer;">Click to Send WhatsApp</button></a>', unsafe_allow_html=True)
            
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Cart is empty.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("Data Load Nahi Hua!")
