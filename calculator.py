import pandas as pd
file_path = "All Drugs Ceiling Prices.csv"
df = pd.read_csv(file_path)


import pandas as pd

def calculate_final_price(base_price, profit_margin, tax_percent, transport_cost, ceiling_price):
    """
    Calculates the final selling price and ensures it does not exceed the ceiling price.
    
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

# User Input
base_price = float(input("Enter cost of manufacturing per unit: "))
profit_margin = float(input("Enter profit margin (decimal for % or fixed amount): "))
transport_cost = float(input("Enter transportation and other charges: "))
tax_percent = float(input("Enter tax percentage: "))
ceiling_price = float(input("Enter government-fixed ceiling price: "))

final_price = calculate_final_price(base_price, profit_margin, tax_percent, transport_cost, ceiling_price)
print("Final Selling Price:", final_price)