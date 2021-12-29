from extract import extract_talks

def tally_up(talks):
    scoreboard = {}
    for talk in talks:
        for translator in talk.translators:
            if translator in scoreboard:
                scoreboard[translator] = (scoreboard[translator][0] + talk.duration,
                                          scoreboard[translator][1] + (talk,))
            else:
                scoreboard[translator] = (talk.duration, (talk,))
    return scoreboard


def csv_by_nick(scoreboard):
    nicks = list(scoreboard.keys())
    nicks.sort()
    for nick in nicks:
        print('{},{}'.format(nick, scoreboard[nick][0]))


def details_by_nick(scoreboard):
    nicks = list(scoreboard.keys())
    nicks.sort()
    for nick in nicks:
        print('{},{}'.format(nick, scoreboard[nick][0]))
        for talk in scoreboard[nick][1]:
            print('* {}: {}'.format(talk.title, talk.duration))
    

if __name__ == '__main__':
    csv_by_nick(tally_up(extract_talks(1, open('/home/informancer/Downloads/Translations for rc3-2021 · Day 1.md'))))
    details_by_nick(tally_up(extract_talks(1, open('/home/informancer/Downloads/Translations for rc3-2021 · Day 1.md'))))
