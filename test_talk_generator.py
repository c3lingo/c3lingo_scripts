from extract import extract_talks, TRANSLATION_RE, extract_spacetime_coordinates
from hamcrest import assert_that, equal_to, contains_exactly, empty
from datetime import timedelta, time
import re


def test_translation_re():
    result = re.match(TRANSLATION_RE, '')
    assert_that(result, equal_to(None))
    result = re.match(TRANSLATION_RE, '→ ')
    assert_that(result, equal_to(None))
    result = re.match(TRANSLATION_RE, '→ f: blah')
    assert_that(result, equal_to(None))
    result = re.match(TRANSLATION_RE, '→ french: blah')
    assert_that(result, equal_to(None))
    result = re.match(TRANSLATION_RE, '→ fr: blah')
    assert_that(result, not equal_to(None))
    assert_that(result.group('lang'), equal_to('fr'))
    result = re.match(TRANSLATION_RE, '→ en: blah')
    assert_that(result, not equal_to(None))
    assert_that(result.group('lang'), equal_to('en'))
    result = re.match(TRANSLATION_RE, '→ ru: blah')
    assert_that(result, not equal_to(None))
    assert_that(result.group('lang'), equal_to('ru'))


def test_talk_moved():
    test_content = ['### #1  ',
                    '**MOVED TO 16:00**',
                    '']
    talks = list(extract_talks(test_content, "none"))
    assert_that(talks, empty())


def test_talk_no_translation():
    test_content = ['### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ',
                    '**R3S Opening** (Lightning Talk)  ',
                    'heyhej  ',
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  ',
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  ',
                    '']

    talks = list(extract_talks(test_content, "none"))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(talk.title, equal_to('R3S Opening'))
    assert_that(talk.speaker, equal_to('heyhej'))
    assert_that(talk.fahrplan_url, equal_to('https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/'))
    assert_that(talk.date, equal_to(0))
    assert_that(talk.time, equal_to(time.fromisoformat('10:45')))
    assert_that(talk.place, equal_to('r3s - Monheim/Rhein'))


def test_talk_with_day():
    test_content = ['# Translations for rc3-2021 · Day 1',
                    '### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ',
                    '**R3S Opening** (Lightning Talk)  ',
                    'heyhej  ',
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  ',
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  ',
                    '']

    talks = list(extract_talks(test_content, "none"))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(talk.title, equal_to('R3S Opening'))
    assert_that(talk.speaker, equal_to('heyhej'))
    assert_that(talk.fahrplan_url, equal_to('https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/'))
    assert_that(talk.date, equal_to(1))
    assert_that(talk.time, equal_to(time.fromisoformat('10:45')))
    assert_that(talk.place, equal_to('r3s - Monheim/Rhein'))


def test_talk_translations():
    test_content = ['### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ',
                    '**R3S Opening** (Lightning Talk)  ',
                    'heyhej  ',
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  ',
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  ',
                    '→ en: one',
                    '→ ru: three, four',
                    '']
    talks = list(extract_talks(test_content, "none"))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(len(talk.translations), equal_to(2))
    print(talk.translations)
    assert_that(talk.translations, contains_exactly('en', 'ru'))
    assert_that(talk.translators, contains_exactly('one', 'three', 'four'))


def test_talk_translation_with_glossary():
    test_content = ['### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ',
                    '**R3S Opening** (Lightning Talk)  ',
                    'heyhej  ',
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  ',
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  ',
                    'Glossary',
                    '→ en: one',
                    '→ ru: three, four',
                    '']
    talks = list(extract_talks(test_content, "none"))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(len(talk.translations), equal_to(2))
    print(talk.translations)
    assert_that(talk.translations, contains_exactly('en', 'ru'))
    assert_that(talk.translators, contains_exactly('one', 'three', 'four'))


def test_talk_no_translator():
    test_content = ['### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ',
                    '**R3S Opening** (Lightning Talk)  ',
                    'heyhej  ',
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  ',
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  ',
                    '→ en:',
                    '→ fr:  ',
                    '']
    talks = list(extract_talks(test_content, "none"))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(talk.translations, empty())
    assert_that(talk.translators, empty())


def test_extract_spacetime_coordinates():
    the_language, the_time, the_duration, the_place = extract_spacetime_coordinates('[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ')
    assert_that(the_language, equal_to('de'))
    assert_that(the_time, equal_to(time(hour=10, minute=45)))
    assert_that(the_duration, equal_to(timedelta(hours=0, minutes=15)))
    assert_that(the_place, equal_to('r3s - Monheim/Rhein'))
