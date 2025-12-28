import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CSS FOR UI & PRINTING ---
st.markdown("""
<style>
    .stApp { background-color: white !important; }
    .header { background-color: #0053E1; color: white !important; padding: 15px; text-align: center; border-bottom: 5px solid #F9B000; }
    h1, h2, h3, p, label { color: black !important; font-weight: bold; }
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; border-radius: 8px; }
    
    /* PRINT LOGIC: Pure White Background & No UI */
    @media print {
        header, footer, .stSidebar, .no-print, [data-testid="stToolbar"], button { display: none !important; }
        .print-only { display: block !important; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: white !important; z-index: 9999; }
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
    except: return None, None

if 'cart' not in st.session_state: st.session_state.cart = []
if 'p_data' not in st.session_state:
    p, a = load_data()
    st.session_state.p_data, st.session_state.a_data = p, a

# --- SIDEBAR & LOGO ---
try: st.sidebar.image("Noor Pharmacy logo.jpg", width=150)
except: pass
choice = st.sidebar.radio("Main Menu", ["Sale Counter", "Manage Stock"])

if choice == "Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS V2.0</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("Billing Entry")
        cust_list = st.session_state.a_data['Description'].unique() if st.session_state.a_data is not None else ["Cash Sales"]
        selected_cust = st.selectbox("Select Customer", cust_list)
        
        # --- FORM FOR ENTER KEY ---
        with st.form("entry_form", clear_on_submit=True):
            p_list = [""] + list(st.session_state.p_data['ProductName'].unique()) if st.session_state.p_data is not None else [""]
            p_select = st.selectbox("Search Product", p_list)
            qty = st.number_input("Quantity", min_value=1, value=1)
            submitted = st.form_submit_button("➕ Add Item (Press Enter)")
            
            if submitted and p_select != "":
                row = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_select].iloc[0]
                st.session_state.cart.append({
                    "Item": p_select, "Price": float(row['RetailPrice']), "Qty": qty, "Total": round(float(row['RetailPrice']) * qty, 2)
                })
                st.rerun()

    with col2:
        st.subheader("📋 Current Bill")
        if st.session_state.cart:
            df = pd.DataFrame(st.session_state.cart)
            st.table(df[['Item', 'Qty', 'Total']])
            g_total = round(df['Total'].sum(), 2)
            st.markdown(f"### Total Bill: Rs {g_total}")
            
            if st.button("🖨️ Print Receipt"):
                # Force browser to print
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
            
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()

    # --- THE RECEIPT (Strictly Formatted) ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only" style="padding: 40px; font-family: 'Courier New', Courier, monospace;">
            <center>
                <h1 style="margin:0;">NOOR PHARMACY</h1>
                <p>Main Bazar, Kasur | Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
                <hr style="border: 1px solid black;">
            </center>
            <p><b>Customer:</b> {selected_cust}</p>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid black;">
                    <th align="left">Item</th><th align="center">Qty</th><th align="right">Amount</th>
                </tr>
                {''.join([f"<tr><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <div style="text-align: right; margin-top: 20px; border-top: 2px solid black;">
                <h2>Total: Rs {g_total}</h2>
            </div>
            <center><p style="margin-top: 30px;">Wish you a speedy recovery!</p></center>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Inventory settings yahan show honge.")
