import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS (Keyboard Friendly & Print) ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    h1, h2, h3, p, label { color: black !important; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; }
    /* Cursor focus design */
    input:focus { border: 2px solid #0053E1 !important; }
    @media print {
        .no-print, header, footer, .stSidebar, div[data-testid="stToolbar"] { display: none !important; }
        .print-only { display: block !important; width: 100%; position: absolute; top: 0; }
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
choice = st.sidebar.radio("Go to:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print' style='background-color:#0053E1; color:white; padding:10px; text-align:center;'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("New Entry")
        cust_list = st.session_state.a_data['Description'].dropna().unique()
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        # Product Search with Auto-focus
        p_names = [""] + list(st.session_state.p_data['ProductName'].dropna().unique())
        p_name = st.selectbox("Search Product (Type & Press Enter)", p_names, key="p_search")
        
        if p_name:
            item = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_name].iloc[0]
            st.write(f"**Rate:** Rs {item['RetailPrice']} | **Stock:** {item['StockInHand']}")
            qty = st.number_input("Quantity", min_value=1, value=1, key="qty_input")
            
            # Button works with Enter key
            if st.button("➕ Add to Bill (Enter)"):
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
            
            # Print Button Fix: Direct HTML Link
            if st.button("🖨️ Print Bill"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
                
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()

    # --- PRINT TEMPLATE ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only">
            <center>
                <h1>NOOR PHARMACY</h1>
                <p>Main Bazar, Kasur</p>
                <hr>
                <p><b>Customer:</b> {selected_cust} | <b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}</p>
            </center>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid black;">
                    <th align="left">Item</th><th>Qty</th><th align="right">Total</th>
                </tr>
                {''.join([f"<tr><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <hr>
            <h2 style="text-align:right;">Total Bill: Rs {g_total}</h2>
            <center><p>Health is Wealth</p></center>
        </div>
        """, unsafe_allow_html=True)

elif choice == "⚙️ Manage Stock/Rates":
    st.subheader("Edit Product Data")
    # Admin tools logic...
    st.write("Rates yahan se update karein.")
