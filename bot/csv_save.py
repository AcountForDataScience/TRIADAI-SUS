import csv
# import json

def save_to_csv(message, filename='output.csv'):
    fieldnames = ['user_id', 'user_name', 'date', 'run_id', 'direction', 'test_name', 'score', 'context']
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file.readline():
            writer.writeheader()  # Writes the first row (headers)
        writer.writerow(message)  # Writes data rows