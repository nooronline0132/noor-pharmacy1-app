import streamlit as st
import pandas as pd
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# Windows XP Theme - Colors Fixed for Visibility
st.markdown("""
<style>
    .stApp { background-color: white; }
    .header { background-color: #0053E1; padding: 15px; text-align: center; color: white; border-bottom: 5px solid #F9B000; margin-bottom: 20px; }
    h1, h2, h3, p, label { color: #000000 !important; }
    .bill-box { background-color: #F0F4F8; padding: 20px; border: 2px solid #0053E1; border-radius: 10px; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Loading your specific Excel files
        p_df = pd.read_excel("Products.xlsx")
        a_df = pd.read_excel("AccountCodes.xlsx")
        return p_df, a_df
    except:
        return None, None

prods, accounts = load_data()

if 'cart' not in st.session_state:
    st.session_state.cart = []

st.markdown("<div class='header'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)

if prods is not None:
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader("🛒 Billing Entry")
        cust_list = accounts['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        p_name = st.selectbox("Search Medicine", [""] + list(prods['ProductName'].dropna().unique()))
        
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            st.write(f"**Price:** Rs {item['RetailPrice']} | **Salt:** {item['SaltName']}")
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
            st.dataframe(df_cart[['Item', 'Qty', 'Total']], use_container_width=True)
            g_total = df_cart['Total'].sum()
            st.markdown(f"### Grand Total: Rs {g_total}")
            
            if st.button("✅ WhatsApp Bill"):
                msg = f"Noor Pharmacy Bill\nCustomer: {selected_cust}\nTotal: Rs {g_total}"
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank">Click to Send WhatsApp</a>', unsafe_allow_html=True)

            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Cart empty hai.")
        st.markdown("</div>", unsafe_allow_html=True)
