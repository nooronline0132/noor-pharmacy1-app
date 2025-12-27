import streamlit as st
import pandas as pd
import os
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy V2", layout="wide")

# Windows XP Theme with Print Styling
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .header { background-color: #0053E1; padding: 20px; text-align: center; color: white; border-bottom: 5px solid #F9B000; font-family: 'Tahoma'; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; }
    .bill-box { background-color: #F0F4F8; padding: 20px; border: 2px solid #0053E1; border-radius: 10px; color: black; }
    @media print {
        .no-print { display: none !important; }
        .print-only { display: block !important; font-family: 'Courier New', Courier, monospace; }
    }
    .print-only { display: none; }
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

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- HEADER (Hidden on Print) ---
st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)

if prods is not None:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown("<div class='no-print'>", unsafe_allow_html=True)
        st.subheader("🛒 Sale Entry")
        cust_row = st.selectbox("Select Customer", accounts['Description'].dropna().unique())
        customer_info = accounts[accounts['Description'] == cust_row].iloc[0]
        
        p_name = st.selectbox("Search Medicine", [""] + list(prods['ProductName'].dropna().unique()))
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            qty = st.number_input("Quantity", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": float(item['RetailPrice']) * qty})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
        st.subheader("📋 Final Bill")
        st.write(f"**Customer:** {cust_row}")
        
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            grand_total = df_cart['Total'].sum()
            st.write(f"### Grand Total: Rs {grand_total}")
            
            # Print Button
            if st.button("🖨️ Print Receipt"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
            
            # WhatsApp Button
            if st.button("✅ WhatsApp Bill"):
                msg = f"Noor Pharmacy Bill\nTotal: Rs {grand_total}"
                wa_link = f"https://wa.me/?text={urllib.parse.quote(msg)}"
                st.markdown(f'<a href="{wa_link}" target="_blank">Click to Send</a>', unsafe_allow_html=True)
                
            if st.button("❌ Clear"):
                st.session_state.cart = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- PRINT TEMPLATE ---
if st.session_state.cart:
    st.markdown(f"""
    <div class="print-only">
        <center><h2>NOOR PHARMACY</h2><p>Customer: {cust_row}</p></center>
        <hr>
        {pd.DataFrame(st.session_state.cart)[['Item', 'Qty', 'Total']].to_html(index=False)}
        <hr>
        <h3>Total: Rs {grand_total}</h3>
        <center><p>Thank You!</p></center>
    </div>
    """, unsafe_allow_html=True)
