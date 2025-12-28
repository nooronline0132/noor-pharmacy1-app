import streamlit as st
import pandas as pd
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(page_title="Noor Pharmacy POS", layout="wide")

# --- CUSTOM CSS (Keyboard & Print Fix) ---
st.markdown("""
<style>
    .stApp { background-color: white; color: black; }
    h1, h2, h3, p, label { color: black !important; font-weight: bold; }
    .header { background-color: #0053E1; padding: 10px; text-align: center; color: white !important; margin-bottom: 20px; }
    
    /* Buttons Design */
    div.stButton > button { background-color: #388E3C !important; color: white !important; font-weight: bold; width: 100%; border-radius: 5px; }
    
    /* PRINTING LOGIC: Hides everything except receipt when printing */
    @media print {
        .no-print, header, footer, .stSidebar, div[data-testid="stToolbar"], div[data-testid="stDecoration"] { display: none !important; }
        .print-only { display: block !important; position: absolute; top: 0; left: 0; width: 100%; border: none !important; }
        .stApp { background-color: white !important; }
    }
    .print-only { display: none; }
</style>
""", unsafe_allow_html=True)

# --- LOAD DATA (FAST) ---
@st.cache_data
def load_data():
    try:
        # Loading your specific Excel files
        p_df = pd.read_excel("Products.xlsx")
        a_df = pd.read_excel("AccountCodes.xlsx")
        return p_df, a_df
    except Exception as e:
        return None, None

# Initialize Data in Session
if 'p_data' not in st.session_state:
    p_df, a_df = load_data()
    st.session_state.p_data = p_df
    st.session_state.a_data = a_df

if 'cart' not in st.session_state:
    st.session_state.cart = []

# --- SIDEBAR MENU ---
st.sidebar.title("Noor Pharmacy")
choice = st.sidebar.radio("Main Menu:", ["🛒 Sale Counter", "⚙️ Manage Stock/Rates"])

# Initialize Global Variables to avoid errors
selected_cust = "Cash Sales"
g_total = 0.0

# --- 🛒 SALE COUNTER ---
if choice == "🛒 Sale Counter":
    st.markdown("<div class='header no-print'><h1>NOOR PHARMACY - KASUR</h1></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("New Entry")
        if st.session_state.a_data is not None:
            cust_list = st.session_state.a_data['Description'].dropna().unique()
            selected_cust = st.selectbox("Select Customer", cust_list)
        
        # Product Search
        if st.session_state.p_data is not None:
            p_names = [""] + list(st.session_state.p_data['ProductName'].dropna().unique())
            p_name = st.selectbox("Search Product (Type name)", p_names)
            
            if p_name:
                item = st.session_state.p_data[st.session_state.p_data['ProductName'] == p_name].iloc[0]
                st.write(f"**Rate:** Rs {item['RetailPrice']} | **Salt:** {item['SaltName']}")
                
                qty = st.number_input("Quantity", min_value=1, value=1)
                
                if st.button("➕ Add to Bill (Enter)"):
                    price = float(item['RetailPrice'])
                    st.session_state.cart.append({
                        "Item": p_name, 
                        "Price": price, 
                        "Qty": qty, 
                        "Total": round(price * qty, 2)
                    })
                    st.rerun()

    with col2:
        st.subheader("📋 Final Bill")
        if st.session_state.cart:
            df_cart = pd.DataFrame(st.session_state.cart)
            st.table(df_cart[['Item', 'Qty', 'Total']])
            g_total = round(df_cart['Total'].sum(), 2)
            st.markdown(f"## Total: Rs {g_total}")
            
            # Simplified Print Button
            if st.button("🖨️ Print Receipt"):
                st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
                
            if st.button("❌ Clear Bill"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Cart is empty.")

    # --- 🖨️ RECEIPT TEMPLATE (Only for Print) ---
    if st.session_state.cart:
        st.markdown(f"""
        <div class="print-only" style="padding: 20px; font-family: sans-serif;">
            <center>
                <h1 style="margin:0;">NOOR PHARMACY</h1>
                <p style="margin:5px;">Main Bazar, Kasur | Cell: 0300-XXXXXXX</p>
                <hr style="border: 1px solid black;">
                <h3>CASH RECEIPT</h3>
            </center>
            <p><b>Customer:</b> {selected_cust}<br><b>Date:</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}</p>
            <table style="width:100%; border-collapse: collapse;">
                <tr style="border-bottom: 2px solid black; text-align: left;">
                    <th>Item Description</th>
                    <th style="text-align: center;">Qty</th>
                    <th style="text-align: right;">Amount</th>
                </tr>
                {''.join([f"<tr style='border-bottom: 1px dashed #ccc;'><td>{r['Item']}</td><td align='center'>{r['Qty']}</td><td align='right'>{r['Total']}</td></tr>" for r in st.session_state.cart])}
            </table>
            <br>
            <h2 style="text-align:right; border-top: 2px solid black; padding-top:10px;">Net Total: Rs {g_total}</h2>
            <hr style="border: 1px solid black;">
            <center><p>Wish you a speedy recovery!<br>Noor Pharmacy Team</p></center>
        </div>
        """, unsafe_allow_html=True)

# --- ⚙️ MANAGE STOCK ---
elif choice == "⚙️ Manage Stock/Rates":
    st.markdown("<div class='header'><h1>Inventory Management</h1></div>", unsafe_allow_html=True)
    if st.session_state.p_data is not None:
        edit_p = st.selectbox("Select Product to Edit", st.session_state.p_data['ProductName'].unique())
        idx = st.session_state.p_data[st.session_state.p_data['ProductName'] == edit_p].index[0]
        
        new_price = st.number_input("New Price", value=float(st.session_state.p_data.at[idx, 'RetailPrice']))
        if st.button("💾 Update Rate"):
            st.session_state.p_data.at[idx, 'RetailPrice'] = new_price
            st.success("Price updated locally!")
    else:
        st.error("Data load nahi hua!")
