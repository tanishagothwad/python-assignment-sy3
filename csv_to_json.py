"""
=====================================================================
 CSV TO JSON CONVERTER
=====================================================================
IN PLAIN ENGLISH:
  A CSV file is like a simple spreadsheet saved as plain text \u2014 rows
  and columns separated by commas, with a header row naming each
  column. JSON represents the SAME data differently: each row becomes
  a labeled record made of "key": "value" pairs, which many programs
  (especially web applications) find easier to work with.

  This script reads a CSV file, converts every row into a JSON
  record using the header row as the labels, and saves the result
  as a brand-new .json file.
=====================================================================
"""

import csv
import json


# =====================================================================
# 1. READ THE CSV FILE
#    Plain English: open the CSV, and turn each row into a dictionary,
#    using the header row's column names as the dictionary's keys.
# =====================================================================
def read_csv(input_path):
    """Returns a list of dictionaries, one dictionary per CSV row."""
    with open(input_path, "r", newline="") as f:
        reader = csv.DictReader(f)   # uses row 1 as the dictionary keys
        return list(reader)


# =====================================================================
# 2. WRITE THE DATA AS JSON
#    Plain English: take our list of dictionaries and save it as a
#    neatly formatted JSON file.
# =====================================================================
def write_json(output_path, data):
    """Writes `data` (a list of dicts) to output_path as formatted JSON."""
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)


# =====================================================================
# 3. MAIN CONVERSION FUNCTION
#    Plain English: ties the two steps above together \u2014 read the
#    CSV, then immediately write it back out as JSON.
# =====================================================================
def convert_csv_to_json(input_path, output_path):
    """Reads a CSV file and writes its contents as JSON.
    Returns the data that was written, as a list of dictionaries."""
    data = read_csv(input_path)
    write_json(output_path, data)
    return data


# =====================================================================
# 4. DEMO / DRIVER CODE
# =====================================================================
if __name__ == "__main__":

    input_path = "students.csv"
    output_path = "students.json"

    # ---- create a sample CSV file, just for this demo ------------------
    sample_csv = (
        "id,name,department,marks\n"
        "1,Aditi Sharma,Computer Science,88\n"
        "2,Rahul Verma,Mechanical,76\n"
        "3,Sneha Iyer,Electronics,92\n"
    )
    with open(input_path, "w", newline="") as f:
        f.write(sample_csv)
    print(f"Created sample CSV file: {input_path}\n")

    # ---- show the raw CSV content ----------------------------------------
    print(f"Contents of '{input_path}':")
    with open(input_path, "r") as f:
        print(f.read())

    # ---- convert CSV to JSON ------------------------------------------------
    data = convert_csv_to_json(input_path, output_path)
    print(f"Converted {len(data)} row(s) from CSV to JSON.")
    print(f"JSON written to: {output_path}\n")

    # ---- show the resulting JSON content -------------------------------------
    print(f"Contents of '{output_path}':")
    with open(output_path, "r") as f:
        print(f.read())