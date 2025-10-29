# Email Sender - Sistema de Envio de Emails Automatizado

Sistema automatizado para download, organização e envio de emails com arquivos de liquidação para clientes. O sistema integra com bancos de dados Oracle, baixa arquivos via SSH e organiza automaticamente os dados por empresa para envio personalizado.

## 🚀 Funcionalidades

- **Download Automatizado**: Baixa arquivos de liquidação via SSH de servidores remotos
- **Organização por Empresa**: Organiza automaticamente os arquivos por operadora/empresa
- **Envio de Emails**: Envia emails personalizados com arquivos anexados para cada cliente
- **Integração com Oracle**: Conecta-se a bancos de dados Oracle para extrair listas de liquidação
- **Suporte a Múltiplas Franquias**: Suporta franquias 215, 317 e IRC
- **Backup Automático**: Cria backups dos arquivos processados
- **Logs Detalhados**: Sistema completo de logging para monitoramento

## 📋 Pré-requisitos

- Python 3.7+
- Oracle SQL*Plus client
- Acesso SSH aos servidores de dados
- Credenciais de banco de dados Oracle
- Windows PowerShell (para execução dos scripts)

## 🛠️ Instalação

### 1. Clone o Repositório
```bash
git clone https://github.com/LeandroAssega12/Send-email-customers.git
cd Send-email-customers
```

### 2. Instale as Dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as Variáveis de Ambiente
Crie um arquivo `.env` na pasta `config/`:
```env
# Configurações do Banco de Dados Oracle
SQL_USERNAME=seu_usuario
SQL_PASSWORD=sua_senha
SQL_DATABASE=alias_do_banco

# Configurações SSH
SSH_HOST=servidor_ssh
SSH_USERNAME=usuario_ssh
SSH_PASSWORD=senha_ssh
SSH_PORT=22

# Configurações de Email
SMTP_SERVER=servidor_smtp
SMTP_PORT=587
EMAIL_USERNAME=seu_email
EMAIL_PASSWORD=sua_senha_email
```

## 🚀 Como Usar

### Execução Principal
```bash
python main.py
```

O sistema irá solicitar:
1. **Franquia**: Digite 215, 317 ou IRC
2. **Download**: Se deseja baixar arquivos (Y/N)
3. **Data Inicial**: Data de início no formato DD-MM-YYYY (se download = Y)
4. **Data Final**: Data de fim no formato DD-MM-YYYY (se download = Y)

### Exemplo de Uso
```
Enter the franchise or source (215, 317 or IRC): 215
Download files? (Y/N): Y
Enter the date from (DD-MM-YYYY): 01-01-2024
Enter the date to (DD-MM-YYYY): 31-01-2024
```

## 📁 Estrutura do Projeto

```
Email Sender/
├── main.py                          # Ponto de entrada principal
├── modules/                         # Módulos do sistema
│   ├── download_data.py             # Download de arquivos via SSH
│   ├── generate_liquidation_list.py # Geração de listas de liquidação
│   ├── organize_files_by_company.py # Organização por empresa
│   ├── send_emails.py              # Envio de emails
│   └── ssh_client.py               # Cliente SSH
├── config/                         # Configurações
│   └── settings.py                 # Configurações do sistema
├── utils/                          # Utilitários
│   ├── clean_csv.py               # Limpeza de arquivos CSV
│   ├── create_email.py            # Criação de templates de email
│   └── helpers.py                 # Funções auxiliares
├── downloads/                      # Arquivos baixados
├── download_BKP/                   # Backup dos downloads
├── Signature/                      # Assinaturas de email
├── operadores.xls                  # Lista de operadoras
├── requirements.txt                # Dependências Python
└── README.md                       # Este arquivo
```

## 🔧 Configuração

### Arquivo de Operadoras
O arquivo `operadores.xls` contém a lista de operadoras e suas configurações de email. Certifique-se de que este arquivo está atualizado com:
- Nome da operadora
- Email de destino
- Configurações específicas

### Configurações SSH
Configure o acesso SSH no arquivo de configuração para conectar aos servidores de dados.

### Configurações de Email
Configure o servidor SMTP e credenciais de email para envio automático.

## 📊 Fluxo de Trabalho

1. **Geração de Lista**: Cria lista de liquidações baseada na franquia e período
2. **Download de Arquivos**: Baixa arquivos via SSH (se solicitado)
3. **Organização**: Organiza arquivos por empresa/operadora
4. **Envio de Emails**: Envia emails personalizados com arquivos anexados

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Erro de Conexão SSH**
   - Verifique as credenciais SSH no arquivo de configuração
   - Teste a conectividade com o servidor

2. **Erro de Banco de Dados**
   - Verifique as credenciais Oracle
   - Confirme se o SQL*Plus está instalado

3. **Erro de Email**
   - Verifique as configurações SMTP
   - Confirme as credenciais de email

### Logs
Verifique os logs na pasta `Logs/` para informações detalhadas sobre erros e processamento.

## 📝 Dependências

- `paramiko==3.5.1`: Conexões SSH
- `pandas==2.2.2`: Manipulação de dados
- `python-dotenv==1.1.0`: Gerenciamento de variáveis de ambiente
- `xlrd==2.0.1`: Leitura de arquivos Excel
- `pywin32`: Integração com Windows
- `bcrypt==4.3.0`: Criptografia
- `cryptography==44.0.2`: Criptografia avançada

## 🤝 Contribuição

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça suas alterações
4. Submeta um pull request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT.

## 👥 Autor

**Leandro Assega**
- GitHub: [@LeandroAssega12](https://github.com/LeandroAssega12)

## 📞 Suporte

Para suporte e dúvidas, abra uma issue no repositório GitHub.

## 🔄 Changelog

### v1.0.0
- Implementação inicial do sistema
- Suporte para franquias 215, 317 e IRC
- Integração com Oracle e SSH
- Sistema de envio de emails automatizado
