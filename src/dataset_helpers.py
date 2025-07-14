import csv

#still in progress
def fetch_from_chexpert_pneumothorax_only(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row["Pneumothorax"] == "1.0"):
                row["Pneumothorax"]

