import pandas as pd
import streamlit as st
from datetime import datetime

# Load the datasets
file_path = "All Drugs Ceiling Prices.csv"
df = pd.read_csv(file_path)

# Clean and preprocess the dataset
df.columns = df.columns.str.strip()  # Remove leading/trailing spaces from column names
df['Ceiling_Price'] = df['Ceiling Price ( Excluding Taxes) (Rs.)(Per Unit)'].str.extract(r'₹\s*([\d.]+)').astype(float)  # Extract numeric values from Ceiling Price

def calculate_final_price(Price, gst, discount, margin, transport_cost, storage_cost, packaging_cost, Ceiling_Price):
    """
    Calculates the final price of a drug while respecting the ceiling price set by the government.
    :param Price: Cost of the drug
    :param gst: GST percentage
    :param discount: Discount percentage
    :param margin: Profit margin percentage
    :param transport_cost: Transportation cost
    :param storage_cost: Storage cost per unit
    :param packaging_cost: Packaging cost per unit
    :param Ceiling_Price: Government-fixed ceiling price
    :return: Final price per unit (adjusted if needed)
    """
    tax_amount = Price * (gst / 100)
    discount_amount = Price * (discount / 100)
    margin_amount = Price * (margin / 100)
    final_price = (Price + tax_amount + margin_amount + transport_cost + storage_cost + packaging_cost) - discount_amount

    # Ensure the final price does not exceed the ceiling price
    if final_price > Ceiling_Price:
        final_price = Ceiling_Price

    return round(final_price, 2)

# Add a default Price column (assuming it's required for calculations and missing in the dataset)
df['Price'] = df['Ceiling_Price'] * 0.9  # Example: Setting Price as 90% of Ceiling Price for demonstration

# Streamlit UI setup
st.title("Drug Price and Report Dashboard")

# Sliders for user input
gst = st.slider("GST (%)", min_value=0, max_value=20, value=12)
discount = st.slider("Discount (%)", min_value=0, max_value=50, value=10)
margin = st.slider("Margin (%)", min_value=0, max_value=50, value=20)
transport_cost = st.slider("Transportation Cost (Rs.)", min_value=0, max_value=500, value=50)
storage_cost = st.slider("Storage Cost (Rs.)", min_value=0, max_value=200, value=30)
packaging_cost = st.slider("Packaging Cost (Rs.)", min_value=0, max_value=100, value=20)

# Apply the calculation dynamically
df['Final_Price'] = df.apply(lambda row: calculate_final_price(
    row['Price'], gst, discount, margin, transport_cost, storage_cost, packaging_cost, row['Ceiling_Price']), axis=1)

# Categorized drug selection
drug_categories = {}
for name in df['Formulation']:
    category = name[0].upper()
    if category not in drug_categories:
        drug_categories[category] = []
    drug_categories[category].append(name)

selected_category = st.selectbox("Select a Drug Category:", sorted(drug_categories.keys()))
selected_drugs = st.multiselect("Select Drugs from Category:", drug_categories[selected_category])

# Input fields for additional details
buyer_name = st.text_input("Buyer Name:")
seller_name = st.text_input("Seller Name:")
payment_date = st.date_input("Payment Date:", value=datetime.today().date())

if st.button("Generate Report"):
    if selected_drugs:
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

        st.text(receipt_header)

        # Receipt Table Header
        receipt_table = """
        Drug Name               Base Price      Tax         Final Price
        --------------------------------------------------------------
        """

        total_price = 0
        total_tax = 0
        total_final_price = 0

        for drug_name in selected_drugs:
            selected_drug = df[df['Formulation'] == drug_name].iloc[0]
            base_price = selected_drug['Price']
            ceiling_price = selected_drug['Ceiling_Price']
            tax_amount = round(base_price * (gst / 100), 2)
            final_price = selected_drug['Final_Price']

            total_price += base_price
            total_tax += tax_amount
            total_final_price += final_price

            # Formatting the drug details with consistent spacing
            receipt_table += f"{drug_name:<25} ₹{base_price:<12.2f} ₹{tax_amount:<10.2f} ₹{final_price:<10.2f}\n"

        # Receipt Totals
        receipt_totals = f"""
        --------------------------------------------------------------
        Total Base Price:      ₹{total_price:>10.2f}
        Total Tax:             ₹{total_tax:>10.2f}
        Total Final Price:    ₹{total_final_price:>10.2f}
        --------------------------------------------------------------
        """

        st.text(receipt_table + receipt_totals)

        # Combine all receipt data for download
        full_receipt = receipt_header + receipt_table + receipt_totals
        st.download_button("Download Receipt", full_receipt, file_name="pharmacy_receipt.txt")
    else:
        st.warning("Please select at least one drug.")

# Display the updated data
st.subheader("Updated Drug Prices")
st.dataframe(df[['Formulation', 'Price', 'Ceiling_Price', 'Final_Price']])

# Basic visualization
st.subheader("Price Comparison")
st.bar_chart(df[['Price', 'Final_Price']].head(10))