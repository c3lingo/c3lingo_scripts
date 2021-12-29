from extract import extract_talks, TRANSLATION_RE, extract_spacetime_coordinates
from hamcrest import assert_that, equal_to, contains
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


def test_talk_no_translation():
    test_content = ['### #1  ',
                    '[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  '
                    '**R3S Opening** (Lightning Talk)  '
                    'heyhej  '
                    'Fahrplan: https://pretalx.c3voc.de/rc3-2021-r3s/talk/QED93K/  '
                    'Slides (if available): https://speakers.c3lingo.org/talks/ea266d48-e185-5dbe-90dd-801a8fbe6ecc/  '
                    '→ en: one',
                    '→ fr: two, three',]
    talks = list(extract_talks(3, test_content))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(talk.title, equal_to('R3S Opening'))
    assert_that(talk.date, equal_to(3))
    assert_that(talk.time, equal_to('10:45'))
    assert_that(talk.place, equal_to('Ada'))


def test_talk_translations():
    test_content = ['#1',
                    '[de] 11:30 +01:00, Ada',
                    'Von Menschen radikalisiert: Über Rassismus im Internet',
                    'Michael Kreil',
                    '→ en: one, two',
                    '→ ru: three, four',
                    '']
    talks = list(extract_talks(3, test_content))
    assert_that(len(talks), equal_to(1))
    talk = talks[0]
    assert_that(len(talk.translations), equal_to(2))
    print(talk.translations)
    assert_that(talk.translations, contains('en', 'ru'))


def test_extract_spacetime_coordinates():
    the_language, the_time, the_duration, the_place = extract_spacetime_coordinates('[de] **10:45** +00:15, [r3s - Monheim/Rhein](https://meet.ffmuc.net/rc3r3sc3lingolowlatency)  ')
