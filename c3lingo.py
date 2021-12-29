#!/usr/bin/env python
import argparse
from datetime import timedelta
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
    talks_count = {}

    for nick in scoreboard:
        nick_hours = scoreboard[nick][0]
        if nick_hours in hours:
            hours[nick_hours].append(nick)
        else:
            hours[nick_hours] = [nick]

        nick_talks = len(scoreboard[nick][1])
        if nick_talks in talks_count:
            talks_count[nick_talks].append(nick)
        else:
            talks_count[nick_talks] = [nick]


    print("Most active by time")
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

    print('-'*40)
    print("Most active by number of talks")
    sorted_talks_count = list(talks_count.keys())
    sorted_talks_count.sort()
    sorted_talks_count.reverse()
    for c in sorted_talks_count:
        talks_count[c].sort()
        for nick in talks_count[c]:
            print('{},{}'.format(nick, c))


def print_toots(args):
    for talk in extract_talks(args.day, args.infile):
        for lang in talk.translations:
            print(format_toot(talk, lang))


def stats(args):
    all_talks = [t for f in args.infile
                 for t in extract_talks(0, f)]

    interpreted_talks = [t for t in all_talks if t.translations]

    print("All translatable talks", len(all_talks))
    print("Talks interpreted: ", len(interpreted_talks))
    print("Percentage: ", (float(len(interpreted_talks))/len(all_talks))*100)

    print("Total hours: ", sum((talk.duration for talk in interpreted_talks), timedelta()))

    all_translators = set(translator for talk in all_talks
                          for translator in talk.translators)

    if args.verbose:
        for t in all_translators:
            print('\t* ', t)

    print("Size of team: ", len(all_translators))


def untranslated(args):
    untranslated = [t for t in extract_talks(0, args.infile)
                    if not t.translations]
    for talk in untranslated:
        print("* ", talk.title)


if __name__ == '__main__':

    # Create the top level parser
    parser = argparse.ArgumentParser(description="C3lingo utility script")
    subparsers = parser.add_subparsers()

    # Create the subparser for the stats
    parser_timesheet = subparsers.add_parser('timesheet', description="Create a timesheet for a day")
    parser_timesheet.add_argument("infile", type=argparse.FileType(), help="Markdown file containing the shift assignments")
    parser_timesheet.add_argument("-v", "--verbose", action="store_true", help="Print the talks and duration for checking")
    parser_timesheet.set_defaults(func=timesheet)

    # Create the subparser for the leaderboard
    parser_leaderboard = subparsers.add_parser('leaderboard', description="Show who translated most")
    parser_leaderboard.add_argument("infile", type=argparse.FileType(), nargs='+', help="The files containing the shift assignments (multiple files possible)")
    parser_leaderboard.add_argument("-v", "--verbose", action="store_true", help="Print the talks and duration for checking")
    parser_leaderboard.set_defaults(func=leaderboard)

    # Create the parser for the toots
    parser_toot = subparsers.add_parser('toot', description='Print the announcements to toot')
    parser_toot.add_argument("day", help="The day of the talks in the infile")
    parser_toot.add_argument("infile", type=argparse.FileType(), help="Markdown file containing the shift assignments")
    parser_toot.set_defaults(func=print_toots)

    # Create the parser for the stats
    parser_stats = subparsers.add_parser('stats', description="Show statistics about translations")
    parser_stats.add_argument("infile", type=argparse.FileType(), nargs='+', help="The files containing the shift assignments (multiple files possible)")
    parser_stats.add_argument("-v", "--verbose", action="store_true", help="Print the details")
    parser_stats.set_defaults(func=stats)

    # Create the parse for the untranslated talks
    parser_untranslated = subparsers.add_parser('untranslated', description="List the untranslated talks")
    parser_untranslated.add_argument("infile", type=argparse.FileType(), help="Markdown file containing the shift assignments")
    parser_untranslated.set_defaults(func=untranslated)

    # go for it
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
