import streamlit as st
import pandas as pd
import urllib.parse

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# Windows XP Style - Colors Fixed for Clear Visibility
st.markdown("""
<style>
    /* Sab text ko black karne ke liye */
    .stApp { background-color: white !important; }
    h1, h2, h3, p, label, .stSelectbox div { color: black !important; font-weight: bold; }
    .header { background-color: #0053E1; padding: 15px; text-align: center; color: white !important; border-bottom: 5px solid #F9B000; margin-bottom: 20px; }
    .header h1 { color: white !important; }
    /* Button Style */
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-size: 18px; font-weight: bold; }
    .bill-box { background-color: #F0F4F8; padding: 20px; border: 2px solid #0053E1; border-radius: 10px; color: black !important; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
@st.cache_data
def load_data():
    try:
        # Aap ki Excel files ke exact naam
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
        # Description column for customer
        cust_list = accounts['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        # Product selection from Excel
        p_names = [""] + list(prods['ProductName'].dropna().unique())
        p_name = st.selectbox("Search Medicine", p_names)
        
        if p_name:
            item = prods[prods['ProductName'] == p_name].iloc[0]
            st.write(f"🏷️ **Price:** Rs {item['RetailPrice']} | 🧪 **Salt:** {item['SaltName']}")
            
            qty = st.number_input("Quantity", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                total_price = float(item['RetailPrice']) * qty
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": total_price})
                st.rerun()

    with col2:
        st.markdown("<div class='bill-box'>", unsafe_allow_html=True)
        st.subheader("📋 Final Bill")
        st.write(f"**Customer:** {selected_cust}")
        
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            grand_total = df_cart['Total'].sum()
            st.markdown(f"## Total: Rs {grand_total}")
            
            if st.button("✅ WhatsApp Bill"):
                msg = f"Noor Pharmacy Bill\nCustomer: {selected_cust}\nTotal: Rs {grand_total}"
                st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:10px; cursor:pointer;">Send to WhatsApp</button></a>', unsafe_allow_html=True)

            if st.button("❌ Clear"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Cart empty hai. Medicine select kar ke Add karein.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Data Load Nahi Hua! Files check karein.")
