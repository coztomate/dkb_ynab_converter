import csv
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import argparse

def open_file_dialog():
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Information", "Choose Input File")

    file_path = filedialog.askopenfilename(
        title="Choose Input File",
        filetypes=[("CSV files", "*.csv")],
    )
    return file_path

def choose_output_folder():
    root = tk.Tk()
    root.withdraw()  

    messagebox.showinfo("Information", "Choose Output Folder")

    folder_path = filedialog.askdirectory(
        title="Choose Output Folder"
    )
    return folder_path

def transform_csv(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.reader(infile, delimiter=';')

            for row in reader:
                if "Buchungsdatum" in row:
                    header = row
                    break
            else:
                raise ValueError("Header containing 'Buchungsdatum' not found")

            column_mapping = {
                "Buchungsdatum": "Date",
                "Zahlungsempfänger*in": "Payee",
                "Betrag (€)": "Amount"
            }

            # Create a list of indices for the columns we want to keep
            indices = [header.index(col) for col in column_mapping.keys()]

            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)

                writer.writerow([column_mapping[header[i]] for i in indices])

                # Write the filtered and transformed rows to the output file
                for row in reader:
                    filtered_row = [row[i] for i in indices]

                    # Format the date from DD.MM.YY to DD/MM/YYYY
                    date = datetime.strptime(filtered_row[0], "%d.%m.%y").strftime("%d/%m/%Y")
                    filtered_row[0] = date

                    # Replace comma with dot in the Amount column (last column in the filtered row)
                    filtered_row[-1] = filtered_row[-1].replace(',', '.')

                    writer.writerow(filtered_row)

        print(f"File transformed successfully and saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Transform CSV file")
    parser.add_argument('--input', type=str, help="Path to the input CSV file")
    parser.add_argument('--output', type=str, help="Path to the output directory")

    args = parser.parse_args()

    input_file = args.input or open_file_dialog()
    if not input_file:
        print("No input file selected. Exiting...")
        return

    output_folder = args.output or choose_output_folder()
    if not output_folder:
        print("No output folder selected. Exiting...")
        return

    output_file = os.path.join(output_folder, 'output.csv')
    transform_csv(input_file, output_file)

if __name__ == "__main__":
    main()
