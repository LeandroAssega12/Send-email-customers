import csv

def clean_csv(file_path):  # Remove lines until it finds a target string and strips whitespace
    found = False
    with open(file_path, 'r', newline='') as infile, open('cleaned_' + file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            # Check if the target string exists in any cell of the row
            if not found and any("/tel/product/fm/reports/" in cell for cell in row):
                found = True  # Start writing from this line forward

            if found:
                cleaned_row = [cell.strip() for cell in row]
                writer.writerow(cleaned_row)