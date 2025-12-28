import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS (Visibility, Colors & Print Fix) ---
st.markdown("""
<style>
    .stApp { background-color: white !important; color: black !important; }
    h1, h2, h3, p, label { color: black !important; font-weight: bold !important; }
    .header { background-color: #0053E1; color: white !important; padding: 20px; text-align: center; border-bottom: 5px solid #F9B000; }
    .header h1 { color: white !important; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; border-radius: 8px; }
    
    @media print {
        header, footer, .stSidebar, .no-print, div[data-testid="stToolbar"], button { display: none !important; }
        .print-only { display: block !important; width: 100%; }
        .stApp { background-color: white !important; }
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
        return None, None

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'p_data' not in st.session_state:
    p, a = load_data()
    st.session_state.p_data = p
    st.session_state.a_data = a

# --- SIDEBAR LOGO ---
try:
    st.sidebar.image("Noor Pharmacy logo.jpg", width=150)
except:
    pass
choice = st.sidebar.radio("Main Menu", ["Sale Counter", "Manage Stock"])

if choice == "Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - KASUR</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("New Entry")
        cust_list = st.session_state.a_data['Description'].unique() if st.session_state.a_data is not None else ["Cash Sales"]
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        p_list = [""] + list(st.session_state.p_data['ProductName'].unique()) if st.session_state.p_data is not None else [""]
        p_select = st.selectbox("Search Product", p_list)
        
        if p_select:
            row = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_select].iloc[0]
            qty = st.number_input("Qty", min_value=1, value=1)
            if st.button("➕ Add to Bill"):
                st.session_state.cart.append({
                    "Item": p_select, "Price": row['RetailPrice'], "Qty": qty, "Total": round(row['RetailPrice'] * qty, 2)
                })
                st.rerun()

    with col2:
        st.subheader("📋 Current Bill")
        if st.session_state.cart:
            df = pd.DataFrame(st.session_state.cart)
            st.table(df[['Item', 'Qty', 'Total']])
            g_total = round(df['Total'].sum(), 2)
            st.markdown(f"### Grand Total: Rs {g_total}")
            
            if st.button("🖨️ Print Receipt"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()

    # --- PRINT RECEIPT TEMPLATE ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only" style="padding:10px;">
            <center>
                <h1>NOOR PHARMACY</h1>
                <p>Main Bazar, Kasur | Date: {datetime.now().strftime('%d-%m-%Y')}</p>
                <hr>
                <h3>CASH RECEIPT</h3>
            </center>
            <p><b>Customer:</b> {selected_cust}</p>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid black;"><th>Item</th><th>Qty</th><th>Total</th></tr>
                {''.join([f"<tr><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <hr>
            <h2 style="text-align:right;">Net Bill: Rs {g_total}</h2>
            <center><p>Wish you a speedy recovery!</p></center>
        </div>
        """, unsafe_allow_html=True)

else:
    st.markdown("<div class='header'><h1>Inventory Management</h1></div>", unsafe_allow_html=True)
    st.info("Stock aur rates update karne ke liye Excel file GitHub par upload karein.")
