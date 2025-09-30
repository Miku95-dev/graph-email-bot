import requests
import json
import base64
import os

# Load secrets from environment
client_id = os.environ['CLIENT_ID']
client_secret = os.environ["CLIENT_SECRET"]
tenant_id = os.environ['TENANT_ID']
user_email = os.environ['USER_EMAIL']

# Get access token
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
    "scope": "https://graph.microsoft.com/.default"
}
token_r = requests.post(token_url, data=token_data)
access_token = token_r.json().get("access_token")

# Prepare email
email_url = "https://graph.microsoft.com/v1.0/users/" + user_email + "/sendMail"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

content = "Chào bạn, đây là tệp anime2d được gửi từ Graph API."
encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")

email_data = {
    "message": {
        "subject": "Tự động gửi email bằng Graph API",
        "body": {
            "contentType": "Text",
            "content": "Email này được gửi tự động để duy trì hoạt động tài khoản E5 Developer."
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "address": user_email
                }
            }
        ],
        "attachments": [
            {
                "@odata.type": "#microsoft.graph.fileAttachment",
                "name": "anime2d.txt",
                "contentBytes": encoded
            }
        ]
    },
    "saveToSentItems": "true"
}

r = requests.post(email_url, headers=headers, data=json.dumps(email_data))
print("Status:", r.status_code)
print("Response:", r.text)
