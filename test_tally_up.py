from tallyUpHours import tally_up
from extract import Talk
from hamcrest import assert_that, equal_to, contains_exactly
from datetime import timedelta, time
import re


def test_tally_empty_list():
    scoreboard = tally_up([])
    assert_that(scoreboard, equal_to({}))


def test_tally_one_talk():
    scoreboard = tally_up([Talk(title='',
                                date=1,
                                time='',
                                duration=timedelta(hours=0, minutes=15),
                                place='',
                                speaker='',
                                language='',
                                fahrplan_url='',
                                translations=(),
                                translators=('one', 'two'))])
    assert_that(scoreboard.keys(), contains_exactly('one', 'two'))
    assert_that(scoreboard['one'][0], equal_to(timedelta(hours=0, minutes=15)))


def test_tally_multiple_talks():
    scoreboard = tally_up([Talk(title='',
                                date=1,
                                time='',
                                duration=timedelta(hours=0, minutes=15),
                                place='',
                                speaker='',
                                language='',
                                fahrplan_url='',
                                translations=(),
                                translators=('one', 'two')),
                           Talk(title='',
                                date=1,
                                time='',
                                duration=timedelta(hours=1, minutes=0),
                                place='',
                                speaker='',
                                language='',
                                fahrplan_url='',
                                translations=(),
                                translators=('one', 'three')),
                           Talk(title='',
                                date=1,
                                time='',
                                duration=timedelta(hours=0, minutes=30),
                                place='',
                                speaker='',
                                language='',
                                fahrplan_url='',
                                translations=(),
                                translators=('two',))])
    assert_that(scoreboard.keys(), contains_exactly('one', 'two', 'three'))
    assert_that(scoreboard['one'][0], equal_to(timedelta(hours=1, minutes=15)))
    assert_that(scoreboard['two'][0], equal_to(timedelta(hours=0, minutes=45)))
    assert_that(scoreboard['three'][0], equal_to(timedelta(hours=1, minutes=00)))
