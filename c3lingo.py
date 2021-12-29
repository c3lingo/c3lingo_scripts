#!/usr/bin/env python
import argparse
from extract import extract_talks
from prepare_toot import format_toot
from tallyUpHours import tally_up


def timesheet(args):
    scoreboard = tally_up(extract_talks(1, args.infile))
    nicks = list(scoreboard.keys())
    nicks.sort()
    for nick in nicks:
        print('{},{}'.format(nick, scoreboard[nick][0]))
        if args.verbose:
            for talk in scoreboard[nick][1]:
                print('\t* {}: {}'.format(talk.title, talk.duration))


def leaderboard(args):
    all_talks = [t for f in args.infile
                 for t in extract_talks(0, f)]
    scoreboard = tally_up(all_talks)
    hours = {}

    for nick in scoreboard:
        nick_hours = scoreboard[nick][0]
        if nick_hours in hours:
            hours[nick_hours].append(nick)
        else:
            hours[nick_hours] = [nick]

    sorted_hours = list(hours.keys())
    sorted_hours.sort()
    sorted_hours.reverse()
    for h in sorted_hours:
        hours[h].sort()
        for nick in hours[h]:
            print('{},{}'.format(nick, h))
            if args.verbose:
                for talk in scoreboard[nick][1]:
                    print('\t* {}: {}'.format(talk.title, talk.duration))


def print_toots(args):
    for talk in extract_talks(args.day, args.infile):
        for lang in talk.translations:
            print(format_toot(talk, lang))


if __name__ == '__main__':

    # Create the top level parser
    parser = argparse.ArgumentParser(description="C3lingo utility script")
    subparsers = parser.add_subparsers()

    # Create the subparser for the stats
    parser_timesheet = subparsers.add_parser('timesheet', description="Create a timesheet for a day")
    parser_timesheet.add_argument("infile", type=argparse.FileType(), help="Markdown file containing the shift assignments")
    parser_timesheet.add_argument("-v", "--verbose", action="store_true", help="Print the talks and duration for checking")
    parser_timesheet.set_defaults(func=timesheet)

    # Create the subarser for the leaderboard
    parser_leaderboard = subparsers.add_parser('leaderboard', description="Show who translated most")
    parser_leaderboard.add_argument("infile", type=argparse.FileType(), nargs='+', help="The files containing the shift assignments")
    parser_leaderboard.add_argument("-v", "--verbose", action="store_true", help="Print the talks and duration for checking")
    parser_leaderboard.set_defaults(func=leaderboard)

    # Create the parser for the toots
    parser_toot = subparsers.add_parser('toot', description='Print the announcements to toot')
    parser_toot.add_argument("day", help="The day of the talks in the infile")
    parser_toot.add_argument("infile", type=argparse.FileType(), help="Markdown file containing the shift assignments")
    parser_toot.set_defaults(func=print_toots)
    
    # go for it
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
