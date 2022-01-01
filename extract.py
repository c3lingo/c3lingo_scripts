import re
from collections import namedtuple
from datetime import timedelta, time


def format_toot(format, title, date, time, place):
    return format.format(title, date, time, place)


Talk = namedtuple('Talk', ['title',
                           'date',
                           'time',
                           'duration',
                           'place',
                           'speaker',
                           'language',
                           'fahrplan_url',
                           'translations',
                           'translators'],
                  defaults=['',
                            0,
                            '',
                            '',
                            '',
                            '',
                            '',
                            '',
                            (),
                            ()])


TRANSLATION_RE = r'^\s*→\s*(?P<lang>[a-z]{2})\s*:(?P<translators>.*)'


def extract_duration(duration_string):
    """Create a timedelta from a String like '+00:15'"""
    hours, minutes = duration_string.strip('+').split(':')
    hours = int(hours)
    minutes = int(minutes)
    return timedelta(hours=hours, minutes=minutes)


def extract_spacetime_coordinates(line):
    (the_language, the_time, the_duration, *the_place) = line.strip().split()
    the_language = the_language.strip('[]')
    the_time = time.fromisoformat(the_time.strip('*'))
    the_duration = extract_duration(the_duration.strip(','))
    the_place = ' '.join(the_place)
    the_place = the_place.split(']')[0].strip('[')
    return the_language, the_time, the_duration, the_place


def extract_talks(day, content):
    current_talk = Talk(date=day)

    current_state = 'Start'

    for index, line in enumerate(content, start=1):
        try:
            if current_state == 'Start' and line.startswith('### #'):
                current_state = 'Need coordinates'

            elif current_state == 'Need coordinates':
                the_language, the_time, the_duration, the_place = extract_spacetime_coordinates(line)
                current_talk = current_talk._replace(time=the_time,
                                                     duration=the_duration,
                                                     place=the_place,
                                                     language=the_language)
                current_state = 'Need title'

            elif current_state == 'Need title':
                the_title = line.split('**')[1]
                current_talk = current_talk._replace(title=the_title)
                current_state = 'Need speaker'

            elif current_state == 'Need speaker':
                current_talk = current_talk._replace(speaker=line.strip())
                current_state = 'Need Fahrplan'

            elif current_state == 'Need Fahrplan':
                current_talk = current_talk._replace(fahrplan_url=line.replace('Fahrplan:', '').strip())
                current_state = 'Need Slides'

            elif current_state == 'Need Slides':
                current_state = 'Need translations'

            elif current_state == 'Need translations':
                match = re.match(TRANSLATION_RE, line)
                if match:
                    the_translations = current_talk.translations + (match.group('lang'),)
                    new_translators = tuple(t.strip()
                                            for t
                                            in match.group('translators').split(',')
                                            if match.group('translators').strip())
                    the_translators = current_talk.translators + new_translators
                    if new_translators:
                        current_talk = current_talk._replace(translations=the_translations,
                                                             translators=the_translators)
                elif not line.strip():
                        yield current_talk
                        current_talk = Talk(date=day)
                        current_state = 'Start'
        except Exception as e:
            print('Line {}: {}'.format(index, e))
            print('Skip to next talk')
            current_state = 'Start'
