"""
Load and process data from console
"""


import argparse
import os
import sys

from console_progressbar import ProgressBar

from clubhouse import ClubHouseAPI
from cycle_logic import CycleLogic
from story import Story


SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
SHEET_ID = '15RePTcQH63tsBrxl_9oBLUho4QOjaLUXI7TJxAnWVkg'
GOOGLE_SERVICE_ACCOUNT_FILE = 'CycleTime-c5d6a9b5a35b.json'


def help_me():
    """Show help, mostly notibly how to set the CLUBHOUSE token"""
    print('')
    print('\033[91mAPI TOKEN IS MISSING\033[0m')
    print('You need to provide an API Token from ClubHoue. The token is ')
    print('available on the ClubHouse web application under')
    print('Settings->Settings->API Tokens')
    print('')
    print('You can set it as environment variale:')
    print('    \033[1mexport CLUBHOUSE_TOKEN=aaa000-bbb-ccc\033[0m')
    print('')
    print('Or you can add the key to a file called CLUBHOUSE_TOKEN.txt:')
    print('    \033[1mecho aaa000-bbb-ccc > CLUBHOUSE_TOKEN.txt\033[0m')
    print('')
    print('')


def get_clubhouse_apikey_or_exit():
    """
    Get CLUBHOUSE token from ENV variable or static file
    (keep the file name in .gitignore)
    """
    if os.environ.get('CLUBHOUSE_TOKEN') is not None:
        return os.environ['CLUBHOUSE_TOKEN']
    if os.path.isfile('./CLUBHOUSE_TOKEN.txt'):
        token_file = open('./CLUBHOUSE_TOKEN.txt', 'r')
        return token_file.readline().strip()

    help_me()
    sys.exit(1)


def arg_parser_setup():
    """ALl the things Google"""
    parser = argparse.ArgumentParser(
        description='Calculate cyle time per person per week'
    )
    parser.add_argument(
        '-g',
        '--googlesheets',
        help='Send output to Google Sheets if token is present',
        action='store_true'
    )
    parser.add_argument(
        '-m',
        '--debugmember',
        help='Print stories for particular member'
    )
    args = parser.parse_args()
    return args


def main():
    """Load data, display data"""
    args = arg_parser_setup()
    clubhouse_apikey = get_clubhouse_apikey_or_exit()
    ch_api = ClubHouseAPI(clubhouse_apikey)
    cycle_logic = CycleLogic()

    if args.googlesheets:
        cycle_logic.enable_google_sheets_output(
            sheet_id=SHEET_ID,
            scopes=SCOPES,
            service_account_file=GOOGLE_SERVICE_ACCOUNT_FILE
        )

    members = ch_api.get_active_members()
    progress_bar = ProgressBar(total=len(members))

    for i, member in enumerate(members):
        progress_bar.print_progress_bar(i+1)
        cycle_logic.add_member(member)
        stories = ch_api.stories_by_mention(member['profile']['mention_name'])
        for ch_story in stories:
            story = Story(load_from_dict=ch_story, owner_id=member['id'])
            cycle_logic.add_story(story)


    print('\n\n')
    print(cycle_logic.tabulate_result(debug_member=args.debugmember))


if __name__ == '__main__':
    main()
