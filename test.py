import pandas as pd

def calculate_final_price(base_price, profit_margin, tax_percent, transport_cost, ceiling_price):
    """
    Calculates the final selling price and ensures it does not exceed the ceiling price.
    
    Formula:
    Final Price = (Base Price + Profit + Transport Cost) * (1 + Tax Percent / 100)
    If Final Price > Ceiling Price, adjust to Ceiling Price.
    
    :param base_price: Cost of manufacturing per unit
    :param profit_margin: Profit margin (can be percentage or fixed amount)
    :param tax_percent: Percentage of tax applied
    :param transport_cost: Additional transport and overhead charges
    :param ceiling_price: Maximum allowable price set by the government
    :return: Final price per unit (adjusted if needed)
    """
    
    # If profit_margin is a percentage, calculate it
    if profit_margin < 1:
        profit = base_price * profit_margin
    else:
        profit = profit_margin
    
    # Calculate total cost
    total_price = base_price + profit + transport_cost
    total_price += total_price * (tax_percent / 100)  # Apply tax
    
    # Ensure it does not exceed ceiling price
    if total_price > ceiling_price:
        total_price = ceiling_price  # Adjust price to fit regulation
    
    return round(total_price, 2)

# Predefined dropdown values for selection
drug_options = {
    "Drug A": 10.0,
    "Drug B": 15.5,
    "Drug C": 8.75
}

tax_options = [5, 12, 18]
profit_options = [0.1, 0.2, 0.3]
transport_options = [2, 5, 8]

# User selects values from dropdowns
drug_choice = input(f"Select a drug {list(drug_options.keys())}: ")
base_price = drug_options.get(drug_choice, 0)
profit_margin = float(input(f"Select profit margin {profit_options}: "))
transport_cost = float(input(f"Select transport cost {transport_options}: "))
tax_percent = float(input(f"Select tax percentage {tax_options}: "))
ceiling_price = float(input("Enter government-fixed ceiling price: "))

# Calculate final price
final_price = calculate_final_price(base_price, profit_margin, tax_percent, transport_cost, ceiling_price)
print(f"Formula Used: (Base Price + Profit + Transport Cost) * (1 + Tax Percent / 100)")
print("Final Selling Price:", final_price)