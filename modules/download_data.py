import paramiko
import csv
import os
from utils.clean_csv import clean_csv
from config.settings import SSH_HOST, SSH_PORT, SSH_USER, SSH_PASSWORD


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