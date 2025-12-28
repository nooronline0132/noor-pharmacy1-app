import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- SAKHT CSS FOR PRINT & ENTER ---
st.markdown("""
<style>
    .stApp { background-color: white !important; color: black !important; }
    .header { background-color: #0053E1; color: white !important; padding: 15px; text-align: center; border-bottom: 5px solid #F9B000; }
    
    /* PRINTING: Force hide everything except receipt */
    @media print {
        [data-testid="stSidebar"], .no-print, header, footer, [data-testid="stToolbar"], button, .stMarkdownContainer:not(.print-only) {
            display: none !important;
        }
        .print-only {
            display: block !important;
            position: absolute;
            top: 0;
            left: 0;
            width: 100% !important;
            font-size: 14pt;
        }
        .stApp { background-color: white !important; }
    }
    .print-only { display: none; }
    
    /* Input Styling */
    div[data-baseweb="input"] { border: 2px solid #0053E1 !important; }
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

if 'cart' not in st.session_state: st.session_state.cart = []
if 'p_data' not in st.session_state:
    p, a = load_data()
    st.session_state.p_data = p
    st.session_state.a_data = a

# --- SIDEBAR ---
try: st.sidebar.image("Noor Pharmacy logo.jpg", width=150)
except: pass
choice = st.sidebar.radio("Main Menu", ["Sale Counter", "Manage Stock"])

if choice == "Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Billing Entry")
        cust_list = st.session_state.a_data['Description'].unique() if st.session_state.a_data is not None else ["Cash Sales"]
        cust_name = st.selectbox("Customer", cust_list, key="cust_sel")
        
        # --- FORM START (For Enter Key Support) ---
        with st.form("entry_form", clear_on_submit=True):
            p_list = [""] + list(st.session_state.p_data['ProductName'].unique())
            p_select = st.selectbox("Search Medicine", p_list)
            qty = st.number_input("Quantity", min_value=1, value=1)
            add_btn = st.form_submit_button("➕ Add Item (Press Enter)")
            
            if add_btn and p_select != "":
                row = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_select].iloc[0]
                st.session_state.cart.append({
                    "Item": p_select, 
                    "Price": float(row['RetailPrice']), 
                    "Qty": qty, 
                    "Total": round(float(row['RetailPrice']) * qty, 2)
                })
                st.rerun()

    with col2:
        st.subheader("📋 Current Bill")
        if st.session_state.cart:
            df = pd.DataFrame(st.session_state.cart)
            st.table(df[['Item', 'Qty', 'Total']])
            g_total = round(df['Total'].sum(), 2)
            st.markdown(f"### Grand Total: Rs {g_total}")
            
            if st.button("🖨️ Click to Print"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
            
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()

    # --- RECEIPT TEMPLATE (Clean & Professional) ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only">
            <div style="text-align: center; border-bottom: 2px solid black; padding-bottom: 10px;">
                <h1 style="margin:0;">NOOR PHARMACY</h1>
                <p>Main Bazar, Kasur | Cell: 0300-XXXXXXX</p>
                <p><b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            </div>
            <p><b>Customer:</b> {cust_name}</p>
            <table style="width:100%; border-collapse: collapse; margin-top: 20px;">
                <tr style="border-bottom: 1px solid black; text-align: left;">
                    <th>Item</th><th style="text-align:center;">Qty</th><th style="text-align:right;">Amount</th>
                </tr>
                {''.join([f"<tr><td style='padding:5px;'>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <div style="text-align: right; border-top: 2px solid black; margin-top: 20px; padding-top: 10px;">
                <h2>Total: Rs {g_total}</h2>
            </div>
            <center><p style="margin-top: 50px;">Thank you for your visit!</p></center>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("Manage Stock page under maintenance.")
