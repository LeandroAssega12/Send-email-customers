import os
import win32com.client

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