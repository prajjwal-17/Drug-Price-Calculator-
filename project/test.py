import pandas as pd
import streamlit as st
from datetime import datetime

# Load the dataset
file_path = "All Drugs Ceiling Prices.csv"
df = pd.read_csv(file_path)

# Clean and preprocess the dataset
df.columns = df.columns.str.strip()
df['Ceiling_Price'] = df['Ceiling Price ( Excluding Taxes) (Rs.)(Per Unit)'].str.extract(r'₹\s*([\d.]+)').astype(float)
df['Price'] = df['Ceiling_Price'] * 0.9  # Example: Price as 90% of Ceiling Price

# Function to calculate the final price
def calculate_final_price(price, factors, ceiling_price):
    tax_amount = price * (factors.get("gst", 0) / 100)
    discount_amount = price * (factors.get("discount", 0) / 100)
    margin_amount = price * (factors.get("margin", 0) / 100)
    final_price = (price + tax_amount + margin_amount + factors.get("transport_cost", 0)
                   + factors.get("storage_cost", 0) + factors.get("packaging_cost", 0)) - discount_amount
    return round(min(final_price, ceiling_price), 2)

# Streamlit UI setup
st.title("Pharmacy Dashboard with Drag-and-Drop Pricing")

# Drag-and-drop container for factors
st.subheader("Drag and Drop Cost Factors")
columns = st.columns(2)
with columns[0]:
    st.write("Available Factors")
    if "available_factors" not in st.session_state:
        st.session_state.available_factors = [
            "GST (%)", "Discount (%)", "Margin (%)",
            "Transportation Cost", "Storage Cost", "Packaging Cost"
        ]
    st.write(st.session_state.available_factors)

with columns[1]:
    st.write("Active Factors")
    if "active_factors" not in st.session_state:
        st.session_state.active_factors = []

    for factor in st.session_state.active_factors:
        if st.button(f"Remove {factor}"):
            st.session_state.active_factors.remove(factor)
            st.session_state.available_factors.append(factor)

# Add functionality to move items between containers
for factor in st.session_state.available_factors:
    if st.button(f"Activate {factor}"):
        st.session_state.available_factors.remove(factor)
        st.session_state.active_factors.append(factor)

# Generate sliders dynamically for active factors
active_values = {}
if st.session_state.active_factors:
    st.subheader("Adjust Active Factors")
    for factor in st.session_state.active_factors:
        if factor == "GST (%)":
            active_values["gst"] = st.slider("GST (%)", min_value=0, max_value=20, value=12)
        elif factor == "Discount (%)":
            active_values["discount"] = st.slider("Discount (%)", min_value=0, max_value=50, value=10)
        elif factor == "Margin (%)":
            active_values["margin"] = st.slider("Margin (%)", min_value=0, max_value=50, value=20)
        elif factor == "Transportation Cost":
            active_values["transport_cost"] = st.slider("Transportation Cost (Rs.)", min_value=0, max_value=500, value=50)
        elif factor == "Storage Cost":
            active_values["storage_cost"] = st.slider("Storage Cost (Rs.)", min_value=0, max_value=200, value=30)
        elif factor == "Packaging Cost":
            active_values["packaging_cost"] = st.slider("Packaging Cost (Rs.)", min_value=0, max_value=200, value=20)

# Apply calculation dynamically
df['Final_Price'] = df.apply(lambda row: calculate_final_price(
    row['Price'], active_values, row['Ceiling_Price']), axis=1)

# Drug search and selection
st.subheader("Search and Add Medicines")
search_query = st.text_input("Search for a drug:")
filtered_df = df[df['Formulation'].str.contains(search_query, case=False, na=False)] if search_query else df

# Display filtered drugs with selection
selected_drugs = st.multiselect("Select Drugs:", filtered_df['Formulation'].tolist())

# Maintain drug quantities in session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}

for drug in selected_drugs:
    if drug not in st.session_state.cart:
        st.session_state.cart[drug] = 1

# Adjust quantities for selected drugs
if st.session_state.cart:
    st.subheader("Adjust Quantities")
    for drug, qty in st.session_state.cart.items():
        st.session_state.cart[drug] = st.number_input(f"Quantity for {drug}:", min_value=1, value=qty, key=f"qty_{drug}")

# Input fields for additional details
buyer_name = st.text_input("Buyer Name:")
seller_name = st.text_input("Seller Name:")
payment_date = st.date_input("Payment Date:", value=datetime.today().date())

# Generate receipt
if st.button("Generate Receipt"):
    if st.session_state.cart:
        st.subheader("Pharmacy Receipt")

        # Receipt Header
        receipt_header = f"""
        ----------------------------
        PHARMA RECEIPT
        ----------------------------
        Buyer Name: {buyer_name if buyer_name else 'N/A'}
        Seller Name: {seller_name if seller_name else 'N/A'}
        Payment Date: {payment_date}
        ----------------------------
        """

        # Receipt Table Header
        receipt_table = """
        Drug Name           Quantity    Price/Unit    Total Price    Govt Set Price
        --------------------------------------------------------------------------
        """

        total_price = 0
        total_govt_price = 0

        for drug, qty in st.session_state.cart.items():
            selected_drug = df[df['Formulation'] == drug].iloc[0]
            price_per_unit = selected_drug['Final_Price']
            govt_price_per_unit = selected_drug['Ceiling_Price']
            total_cost = price_per_unit * qty
            govt_total_cost = govt_price_per_unit * qty

            receipt_table += f"{drug:<20} {qty:<12} {price_per_unit:<12.2f} {total_cost:<12.2f} {govt_total_cost:<12.2f}\n"
            total_price += total_cost
            total_govt_price += govt_total_cost

        # Receipt Totals
        receipt_totals = f"""
        --------------------------------------------------------------------------
        Total Price:        {total_price:.2f}
        Govt Set Price:     {total_govt_price:.2f}
        --------------------------------------------------------------------------
        """

        st.text(receipt_header + receipt_table + receipt_totals)

        # Combine all receipt data for download
        full_receipt = receipt_header + receipt_table + receipt_totals
        st.download_button("Download Receipt", full_receipt, file_name="pharmacy_receipt.txt")
    else:
        st.warning("Please add at least one drug to the cart.")

# Display the updated data
st.subheader("Updated Drug Prices")
st.dataframe(df[['Formulation', 'Price', 'Ceiling_Price', 'Final_Price']])

# Price comparison chart
st.subheader("Price Comparison")
st.bar_chart(df[['Price', 'Final_Price']].head(10))
