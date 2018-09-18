"""
Load and process data from console
"""


import os
import sys

from console_progressbar import ProgressBar

from clubhouse import ClubHouseAPI
from cycle_logic import CycleLogic
from story import Story


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


def main():
    """Load data, display data"""
    clubhouse_apikey = get_clubhouse_apikey_or_exit()
    ch_api = ClubHouseAPI(clubhouse_apikey)
    cycle_logic = CycleLogic()

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
    print(cycleLogic.tabulate_result())
    # print(cycle_logic.wild_experiment())


if __name__ == '__main__':
    main()
