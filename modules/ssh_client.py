import paramiko
import os
import subprocess
import csv
import shutil
import pandas as pd
import zipfile
import win32com.client
from config.settings import SSH_HOST, SSH_PORT, SSH_USER, SSH_PASSWORD, SQL_DATABASE, SQL_USERNAME ,SQL_PASSWORD


def generate_liquidation_list(franchise, date_from, date_to):
        
	if franchise == '215':
		SQL_FILE = 'move215.sql'
	elif franchise == '317':
		SQL_FILE = 'move317.sql'
	elif franchise.upper() == 'IRC':
		SQL_FILE = 'moveIRC.sql'
	else:
		raise ValueError(f"Unknown franchise value : {franchise}, choose between 215, 317 or IRC")


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
	
	sftp = ssh.open_sftp()
	
	# Executando o comando SQL
	if franchise.upper()=='IRC':
		connection_string = f"sqlplus -s {SQL_USERNAME}/{SQL_PASSWORD}@{SQL_DATABASE} @{SQL_FILE} {date_from} {date_to}"
		result = subprocess.run(connection_string, shell=True, capture_output=True, text=True)
	else:
		connection_string = f"sqlplus -s {SQL_USERNAME}/{SQL_PASSWORD}@{SQL_DATABASE} @{SQL_FILE} {franchise} {date_from} {date_to}"
		result = subprocess.run(connection_string, shell=True, capture_output=True, text=True)

	sftp.close()
	ssh.close()

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
                   
def download_data(franchise):
    TXT_FILE = f'liquidaciones_{franchise}.txt'
    CLEANED_TXT_FILE = 'cleaned_' + TXT_FILE

    clean_csv(TXT_FILE)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)

    sftp = ssh.open_sftp()

    # Cria a pasta "downloads" se ela não existir
    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(downloads_dir, exist_ok=True)

    # Usa csv.reader com um delimitador que nunca ocorrerá (ex: '|')
    with open(CLEANED_TXT_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if not row:
                continue
            remote_path = row[0].strip().strip('"')
            print(f"Reading path: {remote_path}")
            filename = os.path.basename(remote_path)
            local_path = os.path.join(downloads_dir, filename)
            print(f"Downloading from: {remote_path} to {local_path}")
            sftp.get(remote_path, local_path)

    sftp.close()
    ssh.close()

def organize_files_by_company(xls_path, source_folder, franchise):
    # Read the Excel file (.xls format) - specific sheet based on franchise
    df = pd.read_excel(xls_path, sheet_name=franchise, engine='xlrd')

    # Expand rows with multiple codes separated by semicolons
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
                if str(code) in file_name:
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
        
        
def create_email(SUBJECT,RECIPIENT,CC_RECIPIENT,MAIL_BODY,ATTACHMENT_FILE=None):
    # Get base path (same folder as script)
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    signature_folder = os.path.join(base_path, 'Signature')
    Attachement_folder = os.path.join(base_path, 'downloads')

    # Signature and image paths
    signature_path = os.path.join(signature_folder, 'TCH.htm')
    image_path = os.path.join(signature_folder, 'image001.png')

    # Check required files
    if not os.path.isfile(signature_path):
        raise FileNotFoundError(f"Signature file not found: {signature_path}")
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Handle attachment if provided
    if ATTACHMENT_FILE:
        attachment_path = os.path.join(Attachement_folder, ATTACHMENT_FILE)
        if not os.path.isfile(attachment_path):
            raise FileNotFoundError(f"Attachment file not found: {attachment_path}")

    # Load HTML and replace image ref with Content-ID
    with open(signature_path, 'r', encoding='cp1252') as f:
        signature_html = f.read()
    signature_html = signature_html.replace('image001.png', 'cid:image001.png@01D8ABE2.D020AAB0')

    # Create email
    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    # Add inline image
    inline_image = mail.Attachments.Add(image_path)
    inline_image.PropertyAccessor.SetProperty(
        "http://schemas.microsoft.com/mapi/proptag/0x3712001F",
        "image001"
    )

    # Add attachment if provided
    if ATTACHMENT_FILE:
        mail.Attachments.Add(attachment_path)

    # Compose email
    mail.SentOnBehalfOfName = "MS.Telefonica.Chile@csgi.com"
    mail.Subject = SUBJECT
    mail.To = RECIPIENT
    mail.cc = CC_RECIPIENT
    mail.HTMLBody = MAIL_BODY + signature_html

    mail.Display()


def send_emails(franchise):
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xls_path = os.path.join(base_path, 'operadores.xls')
        
        # Load Excel file and read the necessary sheets
        xls = pd.ExcelFile(xls_path)
        
        # Read the franchise-specific sheet
        df = xls.parse(franchise)
        
        # Read the additional CC recipients from the "settings" tab (cell A2)
        settings_df = xls.parse("Settings", header=None)
        extra_cc = str(settings_df.iloc[1, 0]) if pd.notna(settings_df.iloc[1, 0]) else ""
        
        message_cell = settings_df.iloc[1, 1]  #B1
        body_html = str(message_cell).replace('\r\n', '<br>').replace('\n', '<br>')
        for _, row in df.iterrows():
            subject = str(row["Subject"])
            recipient = str(row["Recipient"])
            cc_recipient = str(row["cc_recipient"]) if pd.notna(row["cc_recipient"]) else ""
            # Combine row-specific CC and the extra CC (if both are not empty)
            combined_cc = '; '.join(filter(None, [cc_recipient, extra_cc]))
            attachment = row.get("file", None)
            attachment_path = str(attachment) if pd.notna(attachment) else None
            
            # Verificar se o arquivo de anexo existe
            if attachment_path:
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                downloads_path = os.path.join(base_path, 'downloads')
                full_attachment_path = os.path.join(downloads_path, attachment_path)
                
                if not os.path.exists(full_attachment_path):
                    print(f"❌ PULANDO: Arquivo de anexo não encontrado: {attachment_path}")
                    print(f"   Caminho completo: {full_attachment_path}")
                    continue  # Pular este operador - não gerar email
            
            print(f"✅ Enviando email para: {recipient} | Assunto: {subject} | CC: {combined_cc}")
            if attachment_path:
                print(f"   Anexo: {attachment_path}")
            create_email(subject, recipient, combined_cc, str(body_html), attachment_path)
    except Exception as e:
        print(f"Error reading or processing file: {e}")