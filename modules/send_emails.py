import os
import pandas as pd
import locale
from datetime import datetime
from utils.create_email import create_email

def send_emails(franchise):
    try:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        xls_path = os.path.join(base_path, 'operadores.xls')
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        
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
            #subject = str(row["Subject"])
            if franchise == '317':
                subject = f'Liquidaciones TELEFONICA CHILE a {str(row["name"])} - Emisión {datetime.today().strftime("%B %Y")}'
            elif franchise == '215':
                subject = f'Liquidaciones MOVISTAR a {str(row["name"])} - Emisión {datetime.today().strftime("%B %Y")}'
            else:
                print("New franchise must be configured")
            recipient = str(row["Recipient"])
            cc_recipient = str(row["cc_recipient"]) if pd.notna(row["cc_recipient"]) else ""
            # Combine row-specific CC and the extra CC (if both are not empty)
            combined_cc = '; '.join(filter(None, [cc_recipient, extra_cc]))
            
            # Verificar se o nome da empresa existe
            company_name = str(row['name']) if pd.notna(row['name']) else None
            if not company_name:
                print(f"⚠️  Aviso: Nome da empresa está vazio ou nulo na linha {_}")
                continue  # Pular este operador
            
            # Verificar se o arquivo de anexo existe
            attachment = f"{company_name}.zip"
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            downloads_path = os.path.join(base_path, 'downloads')
            full_attachment_path = os.path.join(downloads_path, attachment)
            
            if not os.path.exists(full_attachment_path):
                print(f"❌ PULANDO: Arquivo de anexo não encontrado para '{company_name}': {attachment}")
                print(f"   Caminho completo: {full_attachment_path}")
                continue  # Pular este operador - não gerar email
            
            print(f"✅ Enviando email para: {recipient} | Assunto: {subject} | CC: {combined_cc}")
            print(f"   Anexo: {attachment}")
            create_email(subject, recipient, combined_cc, str(body_html), attachment)
    except Exception as e:
        print(f"Error reading or processing file: {e}")