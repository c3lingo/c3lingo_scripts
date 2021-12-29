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
