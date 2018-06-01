# -*- coding: utf-8 -*-
"""
A routing layer for the task notification bot tutorial built using
Python
"""
import os
import time
import json
import timestring
from flask import Flask, request, make_response, render_template
import bot
import setting
from datetime import datetime
from multiprocessing import Process

# connect to the GoogleSheet Client
CLIENT = setting.CLIENT
WORKBOOK = 'BT-Logs-Bot-Copy'

pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)

def _slash_command_handler(slash_command):


    return "event handler"

@app.route("/", methods=["GET"])
def home():
    # rendering home template
    return render_template("index.html")

@app.route("/install", methods=["GET"])
def pre_install():
    client_id = pyBot.oauth["client_id"]
    scope = pyBot.oauth["scope"]
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    code_arg = request.args.get('code')
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    data = request.data
    slack_command = json.loads(data)
    print(slack_command)
    commandTypes = ["today", "tomorrow", "mytask"]
    if slack_command == "today":
        print("i am your today's task")
    return "listening"

def num_suffix(check_in_date):
    """
    Strip the date suffix and return the date
    Before comparing the date
    """
    date_value = str(check_in_date).split(' ')
    day_value = date_value[0][:-2]
    date_value[0] = day_value
    return ' '.join(date_value)

# Main function
def main():
    while True:
        curent_time = datetime.now()
        current_hour = curent_time.hour
        current_minute = curent_time.minute

        if current_hour - 8 > 0:
            sleep_time = 24 - current_hour + 8 - (current_minute/60)
        elif current_hour - 8 < 0:
            sleep_time = 8 - current_hour - (current_minute/60)
        elif current_hour == 8:
            if current_minute == 0:
                sleep_time = 0
            else:
                sleep_time = 24 - current_hour + 8 - (current_minute/60)

        # time.sleep(sleep_time * 3600)
        time.sleep(60)
        sheet = CLIENT.open('BT-Logs-Bot-Copy').sheet1
        sheet_hash = sheet.get_all_records(empty2zero=False, head=1, default_blank='')
        for index, row in enumerate(sheet_hash):
            check_date = datetime.strptime(num_suffix(row['Next Check-In']), '%d %B %Y').date()
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
                    username='Ranti',
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