import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS FOR PRINT & STYLE ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    .header { background-color: #0053E1; padding: 10px; text-align: center; color: white; border-bottom: 5px solid #F9B000; }
    @media print {
        .no-print { display: none !important; }
        .print-only { display: block !important; font-family: 'Courier New', monospace; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- SPEED FIX: CACHING ---
@st.cache_data
def get_data():
    # Reading your specific files
    p_df = pd.read_excel("Products.xlsx")
    a_df = pd.read_excel("AccountCodes.xlsx")
    return p_df, a_df

# Load Initial Data
if 'p_data' not in st.session_state:
    p_df, a_df = get_data()
    st.session_state.p_data = p_df
    st.session_state.a_data = a_df

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- SIDEBAR FOR NAVIGATION ---
st.sidebar.title("Main Menu")
choice = st.sidebar.radio("Go to:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("New Entry")
        # Customer selection from AccountCodes
        cust_list = st.session_state.a_data['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        # Fast Product Search
        p_name = st.selectbox("Search Product", [""] + list(st.session_state.p_data['ProductName'].dropna().unique()))
        
        if p_name:
            item = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_name].iloc[0]
            st.write(f"**Current Rate:** Rs {item['RetailPrice']} | **Salt:** {item['SaltName']}")
            
            qty = st.number_input("Quantity", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                total = float(item['RetailPrice']) * qty
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": total})
                st.rerun()

    with col2:
        st.markdown("<div class='no-print'>", unsafe_allow_html=True)
        st.subheader("📋 Current Bill")
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            g_total = df_cart['Total'].sum()
            st.markdown(f"### Total: Rs {g_total}")
            
            if st.button("🖨️ Print Receipt"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
                
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- ⚙️ MANAGE STOCK/RATES ---
elif choice == "⚙️ Manage Stock/Rates":
    st.subheader("Edit Product Rates & Stock")
    
    # Select Product to Edit
    edit_p = st.selectbox("Select Product to Edit", st.session_state.p_data['ProductName'].unique())
    idx = st.session_state.p_data[st.session_state.p_data['ProductName'] == edit_p].index[0]
    
    new_price = st.number_input("New Retail Price", value=float(st.session_state.p_data.at[idx, 'RetailPrice']))
    new_stock = st.number_input("Update Stock", value=int(st.session_state.p_data.at[idx, 'StockInHand']))
    
    if st.button("💾 Save Changes"):
        st.session_state.p_data.at[idx, 'RetailPrice'] = new_price
        st.session_state.p_data.at[idx, 'StockInHand'] = new_stock
        st.success("Rate Update Ho Gaya! (Note: Ye sirf temporary hai, permanent save k liye Excel upload karni hogi)")

# --- PRINT TEMPLATE (Only visible when printing) ---
if st.session_state.cart:
    st.markdown(f"""
    <div class="print-only">
        <center>
            <h2>NOOR PHARMACY</h2>
            <p>Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            <p>Customer: {selected_cust}</p>
        </center>
        <hr>
        {pd.DataFrame(st.session_state.cart)[['Item', 'Qty', 'Total']].to_html(index=False)}
        <hr>
        <h3>Total Bill: Rs {g_total}</h3>
        <center><p>Health is Wealth - Noor Pharmacy</p></center>
    </div>
    """, unsafe_allow_html=True)
