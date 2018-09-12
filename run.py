import os
import sys

import requests

from clubhouse import ClubHouseAPI
from console_progressbar import ProgressBar
from CycleLogic import CycleLogic
from Story import Story


def help_me():
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
    if os.environ.get('CLUBHOUSE_TOKEN') is not None:
        return os.environ['CLUBHOUSE_TOKEN']
    elif os.path.isfile('./CLUBHOUSE_TOKEN.txt'):
        fh = open('./CLUBHOUSE_TOKEN.txt', 'r')
        return fh.readline().strip()
    else:
        help_me()
        sys.exit(1)


def main():
    clubhouse_apikey = get_clubhouse_apikey_or_exit()
    chApi = ClubHouseAPI(clubhouse_apikey)
    cycleLogic = CycleLogic()

    members = chApi.getActiveMembers()
    pb = ProgressBar(total=len(members))

    for i, member in enumerate(members):
        pb.print_progress_bar(i+1)
        cycleLogic.add_member(member)
        stories = chApi.storiesByMention(member['profile']['mention_name'])
        for chStory in stories:
            story = Story(load_from_dict=chStory, owner_id=member['id'])
            cycleLogic.add_story(story)

    print('\n\n')
    print(cycleLogic.tabulate_result())


if __name__ == '__main__':
    main()
