# Email Sender - Automated Email Sending System

Automated system for downloading, organizing, and sending emails with liquidation files to customers. The system integrates with Oracle databases, downloads files via SSH, and automatically organizes data by company for personalized delivery.

## 🚀 Features

- **Automated Download**: Downloads liquidation files via SSH from remote servers
- **Company Organization**: Automatically organizes files by operator/company
- **Email Sending**: Sends personalized emails with attached files to each customer
- **Oracle Integration**: Connects to Oracle databases to extract liquidation lists
- **Multi-Franchise Support**: Supports franchises 215, 317, and IRC
- **Automatic Backup**: Creates backups of processed files
- **Detailed Logging**: Complete logging system for monitoring

## 📋 Prerequisites

- Python 3.7+
- Oracle SQL*Plus client
- SSH access to data servers
- Oracle database credentials
- Windows PowerShell (for script execution)

## 🛠️ Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the `config/` folder:
```env
# Oracle Database Configuration
SQL_USERNAME=your_username
SQL_PASSWORD=your_password
SQL_DATABASE=database_alias

# SSH Configuration
SSH_HOST=ssh_server
SSH_USERNAME=ssh_user
SSH_PASSWORD=ssh_password
SSH_PORT=22

# Email Configuration
SMTP_SERVER=smtp_server
SMTP_PORT=587
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_email_password
```

## 🚀 Usage

### Main Execution
```bash
python main.py
```

The system will prompt for:
1. **Franchise**: Enter 215, 317, or IRC
2. **Download**: Whether to download files (Y/N)
3. **Start Date**: Start date in DD-MM-YYYY format (if download = Y)
4. **End Date**: End date in DD-MM-YYYY format (if download = Y)

### Usage Example
```
Enter the franchise or source (215, 317 or IRC): 215
Download files? (Y/N): Y
Enter the date from (DD-MM-YYYY): 01-01-2024
Enter the date to (DD-MM-YYYY): 31-01-2024
```

## 📁 Project Structure

```
Email Sender/
├── main.py                          # Main entry point
├── modules/                         # System modules
│   ├── download_data.py             # File download via SSH
│   ├── generate_liquidation_list.py # Liquidation list generation
│   ├── organize_files_by_company.py # Company organization
│   ├── send_emails.py              # Email sending
│   └── ssh_client.py               # SSH client
├── config/                         # Configuration
│   └── settings.py                 # System settings
├── utils/                          # Utilities
│   ├── clean_csv.py               # CSV file cleaning
│   ├── create_email.py            # Email template creation
│   └── helpers.py                 # Helper functions
├── downloads/                      # Downloaded files
├── download_BKP/                   # Download backups
├── Signature/                      # Email signatures
├── operadores.xls                  # Operator list
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔧 Configuration

### Operator File
The `operadores.xls` file contains the list of operators and their email configurations. Make sure this file is updated with:
- Operator name
- Destination email
- Specific configurations

### SSH Configuration
Configure SSH access in the configuration file to connect to data servers.

### Email Configuration
Configure SMTP server and email credentials for automatic sending.

## 📊 Workflow

1. **List Generation**: Creates liquidation list based on franchise and period
2. **File Download**: Downloads files via SSH (if requested)
3. **Organization**: Organizes files by company/operator
4. **Email Sending**: Sends personalized emails with attached files

## 🐛 Troubleshooting

### Common Issues

1. **SSH Connection Error**
   - Check SSH credentials in configuration file
   - Test connectivity with the server

2. **Database Error**
   - Verify Oracle credentials
   - Confirm SQL*Plus is installed

3. **Email Error**
   - Check SMTP configuration
   - Verify email credentials

### Logs
Check logs in the `Logs/` folder for detailed information about errors and processing.

## 📝 Dependencies

- `paramiko==3.5.1`: SSH connections
- `pandas==2.2.2`: Data manipulation
- `python-dotenv==1.1.0`: Environment variable management
- `xlrd==2.0.1`: Excel file reading
- `pywin32`: Windows integration
- `bcrypt==4.3.0`: Encryption
- `cryptography==44.0.2`: Advanced encryption


## 👥 Author

**Leandro Assega**
- GitHub: [@LeandroAssega12](https://github.com/LeandroAssega12)

## 🔄 Changelog

### v1.0.0
- Initial system implementation
- Support for franchises 215, 317, and IRC
- Oracle and SSH integration
- Automated email sending system
