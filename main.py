import os
#from modules.ssh_client import generate_liquidation_list,download_data,organize_files_by_company,create_email,send_emails
from modules.generate_liquidation_list import generate_liquidation_list
from modules.download_data import download_data
from modules.organize_files_by_company import organize_files_by_company
from modules.send_emails import send_emails

def main():
    
    base_path = os.getcwd()
    xls_path = os.path.join(base_path, 'operadores.xls')
    download_path = os.path.join(base_path, 'downloads')
    
    franchise = input("Enter the franchise or source (215, 317 or IRC): ").upper()
    download=input("Download files? (Y/N)").upper()
    if download == "Y":
        date_from = input("Enter the date from (DD-MM-YYYY): ")
        date_to = input("Enter the date to (DD-MM-YYYY): ")
        generate_liquidation_list(franchise, date_from, date_to)
        download_data(franchise)
    
    #organize_files_by_company(xls_path, download_path, franchise)
    send_emails(franchise)
    
if __name__ == "__main__":
    main()