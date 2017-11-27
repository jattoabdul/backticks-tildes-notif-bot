# -*- coding: utf-8 -*-
"""
A routing layer for the task notification bot tutorial built using
Python
"""
import time
import json
from flask import Flask, request, make_response, render_template
import bot
import setting
from datetime import datetime
from multiprocessing import Process

# connect to the GoogleSheet Client
CLIENT = setting.CLIENT
WORKBOOK = 'BT-Logs-Bot-Copy'

app = Flask(__name__)

def _slash_command_handler(slash_command):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.

    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event

    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error

    """
    return "event handler"

@app.route("/", methods=["GET"])
def home():
    """
    This route renders the Application Home PAge and and install button which rediects you to theinstall page.
    """
    # rendering home template
    return render_template("index.html")

@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    # client_id = pyBot.oauth["client_id"]
    # scope = pyBot.oauth["scope"]
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming commands from Slack and uses the slack command handler helper function to route events to our Bot.
    """
    data = request.data
    slack_command = json.loads(data)
    print(slack_command)
    commandTypes = ["today", "tomorrow", "mytask"]
    if slack_command == "today":
        print("i am your today's task")
    return "listening"


# Main function
def main():
    while True:
        curent_time = datetime.now()
        current_hour = a.hour
        current_minute = a.minute

        if current_hour - 8 > 0:
            sleep_time = 24 - current_hour + 8 - (current_minute/60)
        elif current_hour - 8 < 0:
            sleep_time = 8 - current_hour - (current_minute/60)
        elif current_hour == 8:
            if current_minute == 0:
                sleep_time = 0
            else:
                sleep_time = 24 - current_hour + 8 - (current_minute/60)

        time.sleep(sleep_time * 3600)
        # time.sleep(120)
        sheet = CLIENT.open('BT-Logs-Bot-Copy').sheet1
        sheet_hash = sheet.get_all_records(empty2zero=False, head=1, default_blank='')
        for index, row in enumerate(sheet_hash):
            check_date = datetime.strptime(row['Next Check-In'], '%dth %B %Y').date()
            todays_date = datetime.now().date()
            send_notif_date = check_date - todays_date

            if send_notif_date.days == 0:
                text_detail = (
                    '*Task #{} for {}:* \n\n'
                    '*Hey {},* Today is the check-in day for your writeup titled\n'
                    '`{}`.\n\n'
                    'Whats the status of the article?\n'
                    'PS: Please reply to this thread, the managers will review and reply you ASAP').format(str(index + 1), row['Next Check-In'], row['Name'], row['Most Recent Learning Experience you\'d like to write about'])
                setting.SC.api_call(
                    'chat.postMessage',
                    channel='#bt-bot-test',
                    as_user=False,
                    username='BT-BOT',
                    parse='full',
                    text=text_detail
                    )
        print('sent notification to slack')

if __name__ == '__main__':
    # if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    main_app = Process(target=main)
    main_app.start()
    app.run(debug=True, use_reloader=False)
    main_app.join()