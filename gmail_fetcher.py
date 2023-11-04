import base64
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Setup the Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, prompt the user to log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_521620624353-25mefhi1mppgcu7v7to7epn7d8m9foo1.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

# Fetch latest 10 emails from LinkedIn
results = service.users().messages().list(userId='me', q="from:linkedin.com", maxResults=10).execute()
messages = results.get('messages', [])

# Save the email snippets to a file named linkedin_emails.txt
with open('linkedin_emails.txt', 'w') as file:
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        file.write(msg['snippet'] + '\n\n')

