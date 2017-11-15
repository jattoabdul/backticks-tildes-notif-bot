import time
from . import setting
from flask import Flask, request, make_response, render_template
from datetime import datetime
# connect to the GoogleSheet Client
CLIENT = setting.CLIENT
WORKBOOK = 'BT-Logs-Bot-Copy'

# Methods

# Main function
def main():
    while True:
        a = datetime.now()
        b = a.hour
        c = a.minute

        if b - 8 > 0:
            sleep_time = 24 - b + 8 - (c/60)
        elif b - 8 < 0:
            sleep_time = 8 - b - (c/60)
        elif b == 8:
            if c == 0:
                sleep_time = 0
            else:
                sleep_time = 24 - b + 8 - (c/60)

        time.sleep(sleep_time * 3600)
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
        # time.sleep(60)

if __name__ == '__main__':
    print('bot running..')
    main()
