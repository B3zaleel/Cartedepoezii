#!/usr/bin/python3
'''A module for sending GMail messages.
'''
import base64
import os
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ['https://www.googleapis.com/auth/gmail.send']
'''The scopes needed for this client.'''


def create_message(to, subject, message_html):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_html, 'html', 'utf-8')
    message['to'] = to
    message['from'] = os.getenv('GOOGLE_MAIL_SENDER')
    message['subject'] = subject
    mime_message = {
        'raw': base64.urlsafe_b64encode(
            bytes(message.as_string(), 'utf-8')
        ).decode('utf-8')
    }
    return mime_message


def send_message(service, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        creds = get_credentials()
        service = build('gmail', 'v1', credentials=creds)
        message = (service.users().messages().send(userId='me', body=message)
            .execute())
        print('Message Id: {}'.format(message['id']))
        return message
    except HttpError as error:
        print('An error occurred: {}'.format(error))


def get_credentials():
    '''Generates the credentials for this GMail API client.
    '''
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=5050)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def deliver_message(dest, subject, message_html):
    '''Delivers a message to a user.

    Args:
        dest (str): The destination email address.
        subject (str): The subject of the mail.
        message_html (str): The contents of the message.
    '''
    try:
        creds = get_credentials()
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        message = create_message(dest, subject, message_html)
        send_message(service, message)
    except HttpError as error:
        print('An error occurred: {}'.format(error))
