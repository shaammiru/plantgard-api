import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore

encoded_service_account = os.getenv("SA_BASE64_KEY")
if encoded_service_account:
    service_account_json = base64.b64decode(encoded_service_account).decode("utf-8")
    service_account_cred = json.loads(service_account_json)

cred = credentials.Certificate(service_account_cred)
firebase_admin.initialize_app(cred)

db = firestore.client()
