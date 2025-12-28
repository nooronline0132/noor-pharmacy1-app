import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- SAKHT PRINT LOGIC (CSS) ---
st.markdown("""
<style>
    /* Screen par dikhne wala design */
    .stApp { background-color: white; color: black; }
    .header { background-color: #0053E1; color: white !important; padding: 10px; text-align: center; }
    
    /* PRINTING FIX: Jab Ctrl+P dabayein to baki sab ghaib ho jaye */
    @media print {
        header, footer, .stSidebar, .no-print, div[data-testid="stToolbar"], button {
            display: none !important;
        }
        .print-only {
            display: block !important;
            width: 100%;
            color: black !important;
        }
        .stApp { background-color: white !important; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        p_df = pd.read_excel("Products.xlsx")
        a_df = pd.read_excel("AccountCodes.xlsx")
        return p_df, a_df
    except:
        return None, None

# Session State Fix
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'p_data' not in st.session_state:
    p, a = load_data()
    st.session_state.p_data = p
    st.session_state.a_data = a

# --- INTERFACE ---
st.sidebar.title("Noor Pharmacy")
choice = st.sidebar.radio("Menu", ["Sale Counter", "Manage Stock"])

if choice == "Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - POS</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.session_state.a_data is not None:
            cust = st.selectbox("Customer", st.session_state.a_data['Description'].unique())
        
        p_list = [""] + list(st.session_state.p_data['ProductName'].unique())
        p_select = st.selectbox("Search Medicine", p_list)
        
        if p_select:
            row = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_select].iloc[0]
            price = float(row['RetailPrice'])
            qty = st.number_input("Qty", min_value=1, value=1)
            
            if st.button("➕ Add Item"):
                st.session_state.cart.append({
                    "Item": p_select, "Price": price, "Qty": qty, "Total": round(price * qty, 2)
                })
                st.rerun()

    with col2:
        st.subheader("Bill Details")
        if st.session_state.cart:
            df = pd.DataFrame(st.session_state.cart)
            st.table(df[['Item', 'Qty', 'Total']])
            total_bill = round(df['Total'].sum(), 2)
            st.markdown(f"### Grand Total: Rs {total_bill}")
            
            # Print Button
            if st.button("🖨️ Open Print View"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
            
            if st.button("❌ Clear All"):
                st.session_state.cart = []
                st.rerun()

    # --- THE ACTUAL RECEIPT ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only">
            <center>
                <h1>NOOR PHARMACY</h1>
                <p>Main Bazar, Kasur</p>
                <hr>
                <h3>INVOICE</h3>
            </center>
            <p><b>Date:</b> {datetime.now().strftime('%d-%m-%Y')}<br><b>Customer:</b> {cust}</p>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid black;"><th>Item</th><th>Qty</th><th>Amount</th></tr>
                {''.join([f"<tr><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <hr>
            <h2 style="text-align:right;">Total: Rs {total_bill}</h2>
            <center><p>Thanks for visiting!</p></center>
        </div>
        """, unsafe_allow_html=True)

else:
    st.subheader("Update Rates")
    st.write("Yahan se aap Excel file ke rates temporary badal sakte hain.")
