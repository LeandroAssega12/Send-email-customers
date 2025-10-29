import paramiko
import subprocess
from config.settings import SSH_HOST, SSH_PORT, SSH_USER, SSH_PASSWORD, SQL_DATABASE, SQL_USERNAME ,SQL_PASSWORD

def generate_liquidation_list(franchise, date_from, date_to):
        
	if franchise == '215':
		SQL_FILE = 'move215.sql'
	elif franchise == '317':
		SQL_FILE = 'move317.sql'
	elif franchise.upper() == 'IRC':
		SQL_FILE = 'moveIRC.sql'
	else:
		raise ValueError(f"Unknown franchise value : {franchise}, registered franchises: 215, 317 and IRC")


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
	
	sftp = ssh.open_sftp()
	
	# Executando o comando SQL
	connection_string = f"sqlplus -s {SQL_USERNAME}/{SQL_PASSWORD}@{SQL_DATABASE} @{SQL_FILE} {date_from} {date_to}"
	result = subprocess.run(connection_string, shell=True, capture_output=True, text=True)

	sftp.close()
	ssh.close()