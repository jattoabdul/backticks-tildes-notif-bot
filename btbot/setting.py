import os
import sys
import json
import dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slackclient import SlackClient

dotenv.load()


# Define Global Variables (Settings and Constants)
CLIENT_SECRET_FILE = 'client_secret.json'
MAXIMUM_WAITING_PERIOD = 900 # waiting period in seconds
ROOM = 'backtilde'
BOT_NAME = 'Ranti'

# Get Data from .env / json file
# ========START================
# SLACK SECRET OBJECT
SLACK_BOT_SECRET = {
    'token': dotenv.get('SLACK_TOKEN', ''),
    'slack_channel': dotenv.get('SLACK_CHANNEL', 'bt-bot-test')
}

# GOOGLE SHEET CLIENT SECRET OBJECT
with open(CLIENT_SECRET_FILE, 'r') as f:
    CLIENT_BOT_SECRET = json.load(f)

# ==========END==================

# setup for google sheet - Google Drive API Instance
SCOPE = ['http://spreadsheets.google.com/feeds']
CREDENTIALS = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET_FILE, SCOPE)
# Use credentials to create a client to interact with Google Drive API
CLIENT = gspread.authorize(CREDENTIALS)

# setup for slack interaction - Slack Connection Instance
SC = SlackClient(SLACK_BOT_SECRET['token'])
