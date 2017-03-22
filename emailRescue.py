#!/usr/bin/env python
from __future__ import print_function
import httplib2
import os
import requests
import json

from datetime import date

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

# User token location
home_dir = os.path.expanduser('~')
credential_dir = os.path.join(home_dir, '.credentials')
credential_path = os.path.join(credential_dir, 'gmail.json')


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def getMessage(serv, msg_id):
    # This uses the Python client library for GMail API
    try:
        msg = serv.users().messages().get(userId='me', id=msg_id, format='raw').execute()
        return msg
    except Exception as e:
        raise e


def getAccessToken():
    # Read/parse JSON
    data = json.loads(open(credential_path).read())
    return data['access_token']


def sendMessage(msg):
    # Would have used the Python client library but it didn't support this
    # functionality
    url = 'https://www.googleapis.com/gmail/v1/users/me/messages/send?access_token=' + getAccessToken()
    r = requests.post(url, json={'raw': msg})
    print(r.status_code)
    print(r.text)


def getIDList(service):
    # Gets dates for Query
    dt = date.today()
    afterDate = dt.replace(year=dt.year - 1)
    beforeDate = dt.replace(year=dt.year - 1, day=dt.day + 7)
    afterStr = afterDate.strftime('%Y/%m/%d')
    beforeStr = beforeDate.strftime('%Y/%m/%d')

    # Build Query string
    query = 'after:' + afterStr + ' before:' + beforeStr

    # Gets emails that are about a year old
    return service.users().messages().list(userId='me', q=query).execute()


def main():
    # Get permissions to access your Gmail account and make modifications
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = getIDList(service);
    
    # Get list of unique message IDs
    msg_ids = results.get('messages', [])

    # Iterates overs the list of IDs found and sends them
    if not msg_ids:
        print('No messages found')
    else:
        print('Found ' + results.get('resultSizeEstimate', 0) + ' emails to rescue')
        print('Message IDs:')
        # print(msg_ids[0]['id'])
        for m_id in msg_ids:
            # print(m_id['id'])
            msg = getMessage(service, m_id['id'])['raw']
            sendMessage(msg)

        print('Rescued!')

if __name__ == '__main__':
    main()
