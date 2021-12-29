def tally_up(talks):
    scoreboard = {}
    for talk in talks:
        for translator in talk.translators:
            if translator in scoreboard:
                scoreboard[translator] = scoreboard[translator] + talk.duration
            else:
                scoreboard[translator] = talk.duration
    return scoreboard
