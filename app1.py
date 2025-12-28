import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    h1, h2, h3, p, label { color: black !important; }
    .header { background-color: #0053E1; padding: 10px; text-align: center; color: white !important; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; }
    @media print {
        .no-print, header, footer, .stSidebar, div[data-testid="stToolbar"] { display: none !important; }
        .print-only { display: block !important; width: 100%; position: absolute; top: 0; left: 0; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
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
# Sidebar Logo
try: st.sidebar.image("Noor Pharmacy logo.jpg", width=150)
except: pass

choice = st.sidebar.radio("Go to:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# Default Customer to avoid NameError
selected_cust = "Cash Sales"

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("New Entry")
        cust_list = st.session_state.a_data['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        p_names = [""] + list(st.session_state.p_data['ProductName'].dropna().unique())
        p_name = st.selectbox("Search Product", p_names)
        
        if p_name:
            item = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_name].iloc[0]
            st.write(f"**Rate:** Rs {item['RetailPrice']} | **Stock:** {item['StockInHand']}")
            qty = st.number_input("Quantity", min_value=1, value=1)
            
            if st.button("➕ Add to Bill"):
                total = round(float(item['RetailPrice']) * qty, 2)
                st.session_state.cart.append({"Item": p_name, "Price": item['RetailPrice'], "Qty": qty, "Total": total})
                st.rerun()

    with col2:
        st.subheader("📋 Current Bill")
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            g_total = round(df_cart['Total'].sum(), 2)
            st.markdown(f"### Total: Rs {g_total}")
            
            if st.button("🖨️ Print Receipt"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
                
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()

    # PRINT TEMPLATE
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only">
            <center><h1>NOOR PHARMACY</h1><hr>
            <p>Customer: {selected_cust} | Date: {datetime.now().strftime('%d-%m-%Y')}</p></center>
            <table style="width:100%; border-bottom:1px solid black;">
                <tr><th align="left">Item</th><th>Qty</th><th align="right">Total</th></tr>
                {''.join([f"<tr><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table><hr>
            <h2 style="text-align:right;">Total: Rs {g_total}</h2>
        </div>
        """, unsafe_allow_html=True)

# --- ⚙️ MANAGE STOCK/RATES ---
elif choice == "⚙️ Manage Stock/Rates":
    st.markdown("<div class='header'><h1>Inventory Management</h1></div>", unsafe_allow_html=True)
    
    edit_p = st.selectbox("Select Product to Edit", st.session_state.p_data['ProductName'].unique())
    idx = st.session_state.p_data[st.session_state.p_data['ProductName'] == edit_p].index[0]
    
    c1, c2 = st.columns(2)
    new_price = c1.number_input("New Price", value=float(st.session_state.p_data.at[idx, 'RetailPrice']))
    new_stock = c2.number_input("New Stock", value=int(st.session_state.p_data.at[idx, 'StockInHand']))
    
    if st.button("💾 Save Changes"):
        st.session_state.p_data.at[idx, 'RetailPrice'] = new_price
        st.session_state.p_data.at[idx, 'StockInHand'] = new_stock
        st.success(f"Updated {edit_p} successfully!")
