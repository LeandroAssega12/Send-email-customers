import pandas as pd
import os
import shutil
import zipfile

def organize_files_by_company(xls_path, source_folder, franchise):
    # Read the Excel file (.xls format) - specific sheet based on franchise
    df = pd.read_excel(xls_path, sheet_name=franchise, engine='xlrd')

    expanded_rows = []
    for _, row in df.iterrows():
        codes = str(row['code']).split(';')
        for code in codes:
            expanded_rows.append({'code': code.strip(), 'name': row['name']})
    expanded_df = pd.DataFrame(expanded_rows)

    # Create a dictionary {code: name} for easy lookup
    company_codes = dict(zip(expanded_df['code'], expanded_df['name']))

    # Track created folders for compression
    created_folders = set()

    # Ensure the "Not_found" folder exists
    not_found_folder = os.path.join(source_folder, "Not_found")
    os.makedirs(not_found_folder, exist_ok=True)
    created_folders.add(not_found_folder)

    # Organize files
    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith(('.xls', '.pdf')):
            matched = False
            for code, name in company_codes.items():
                if f"_{str(code)}_" in file_name:
                    company_folder = os.path.join(source_folder, name)
                    os.makedirs(company_folder, exist_ok=True)
                    created_folders.add(company_folder)

                    source_path = os.path.join(source_folder, file_name)
                    destination_path = os.path.join(company_folder, file_name)

                    shutil.move(source_path, destination_path)
                    print(f"File '{file_name}' moved to '{company_folder}'")
                    matched = True
                    break

            if not matched:
                source_path = os.path.join(source_folder, file_name)
                destination_path = os.path.join(not_found_folder, file_name)
                shutil.move(source_path, destination_path)
                print(f"File '{file_name}' moved to 'Not_found' folder")

    # Zip and remove folders
    for folder in created_folders:
        zip_name = f"{folder}.zip"
        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder)
                    zipf.write(file_path, arcname)
        print(f"Folder '{folder}' compressed into '{zip_name}'")

        shutil.rmtree(folder)
        print(f"Folder '{folder}' deleted after compression.")