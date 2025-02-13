import requests

def google_sheet_to_csv(sheet_url, output_file):
    """
    Converts a Google Sheet shareable link into a CSV file and saves it locally.
    
    :param sheet_url: The shareable Google Sheet URL (ensure it's set to 'Anyone with the link' can view).
    :param output_file: The name of the CSV file to save.
    """
    try:
        # Convert Google Sheet shareable link to export CSV format
        if "edit" in sheet_url:
            csv_url = sheet_url.replace("/edit", "/export?format=csv")
        elif "spreadsheets/d/" in sheet_url:
            csv_url = f"{sheet_url}/export?format=csv"
        else:
            raise ValueError("Invalid Google Sheet link format!")

        # Fetch the CSV data
        response = requests.get(csv_url)
        response.raise_for_status()  # Check for HTTP errors

        # Save the data to a local CSV file
        with open(output_file, "wb") as file:
            file.write(response.content)
        print(f"Data saved to {output_file} successfully!")

    except Exception as e:
        print(f"Error: {e}")


# Get input from the user
sheet_url = input("Enter the Google Sheet shareable URL: ").strip()
output_file = input("Enter the desired output CSV file name (e.g., data.csv): ").strip()

# Call the function
google_sheet_to_csv(sheet_url, output_file)
