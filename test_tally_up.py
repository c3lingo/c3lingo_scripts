from tallyUpHours import tally_up
from extract import Talk
from hamcrest import assert_that, equal_to, contains_exactly
from datetime import timedelta, time
import re


def test_tally_empty_list():
    scoreboard = tally_up([])
    assert_that(scoreboard, equal_to({}))

