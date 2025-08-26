import pandas as pd

def inspect_excel(file_path):
    """Prints the sheet names of an Excel file."""
    try:
        xls = pd.ExcelFile(file_path)
        print("Sheet names:", xls.sheet_names)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    inspect_excel("methyl_qc.xlsx")
