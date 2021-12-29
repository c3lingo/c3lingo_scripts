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
                           'translations'])


TRANSLATION_RE = r'^\s*→\s*(?P<lang>[a-z]{2})\s*:'


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
    current_talk = Talk(title='',
                        date=day,
                        time='',
                        duration='',
                        place='',
                        speaker='',
                        language='',
                        fahrplan_url='',
                        translations=())

    current_state = 'Start'

    for line in content:

        if current_state == 'Start' and line.startswith('### #'):
            current_state = 'Need coordinates'
            continue

        if current_state == 'Need coordinates':
            the_language, the_time, the_duration, the_place = extract_spacetime_coordinates(line)
            current_talk = current_talk._replace(time=the_time,
                                                 duration=the_duration,
                                                 place=the_place,
                                                 language=the_language)
            current_state = 'Need title'
            continue

        if current_state == 'Need title':
            print(line)
            the_title = line.split('**')[1]
            print(the_title)
            current_talk = current_talk._replace(title=the_title)

            current_state = 'Need speaker'
            continue

        if current_state == 'Need speaker':
            current_talk = current_talk._replace(speaker=line.strip())
            current_state = 'Need Fahrplan'
            continue

        if current_state == 'Need Fahrplan':
            current_talk = current_talk._replace(fahrplan_url=line.split(':')[1].strip())
            current_state = 'Need Slides'
            continue

        if current_state == 'Need Slides':
            current_state = 'Need translations'
            continue

        if current_state == 'Need translations':
            match = re.match(TRANSLATION_RE, line)
            if match:
                the_translations = current_talk.translations + (match.group('lang'),)
                current_talk = current_talk._replace(translations=the_translations)
            else:
                yield current_talk
                current_talk = Talk(title='',
                                    date=day,
                                    time='',
                                    duration='',
                                    place='',
                                    speaker='',
                                    language='',
                                    fahrplan_url='',
                                    translations=())
                current_state = 'Start'


def main():
    new_talk = False
    current_talk = ''
    the_date = '3'
    the_time = ''
    the_place = ''

    for line in open('/home/informancer/Downloads/36c3-day3-latest.txt'):

        # This marks the start of a talk in the plan
        if line.startswith('#'):
            #print(line.strip())
            new_talk = True
            continue

        if new_talk and line.startswith('['):
            _, the_time, _, the_place = line.strip().split()
            continue

        if new_talk and line.startswith('[') is False:
            #print(line.strip())
            current_talk = line.strip()
            new_talk = False
            continue

        # The talk has a marker for a french translation
        if current_talk and re.match(r'^\s*→\s*fr\s*:', line):
            # there is more than one translator
            print(format_toot('La présentation "{}" (jour {} {} à {}) sera traduite en Francais.',
                              current_talk, the_date, the_time, the_place))
            continue

        # The talk has a marker for an english translation
        if current_talk and re.match(r'^\s*→\s*en\s*:', line):
            # there is more than one translator
            print(format_toot('The talk "{}" (day {} {} in {}) will be translated in english.',
                              current_talk, the_date, the_time, the_place))
            continue

        # The talk has a marker for a german translation
        if current_talk and re.match(r'^\s*→\s*de\s*:', line):
            # there is more than one translator
            print(format_toot('Der Vortrag "{}" (Tag {} {} im Raum {}) wird auf Deutsch übersetzt.',
                              current_talk, the_date, the_time, the_place))

        # The talk has a marker for a polish translation
        if current_talk and re.match(r'^\s*→\s*pl\s*:', line):
            # there is more than one translator
            print(format_toot('Wykład "{}" (dzień {}, {} w sali {}) będzie tłumaczony na polski.',
                              current_talk, the_date, the_time, the_place))

        # The talk has a marker for a spanish translation
        if current_talk and re.match(r'^\s*→\s*es\s*:', line):
            # there is more than one translator
            print(format_toot('La charla "{}" (día {}, a las {}, salón {}) será traducida al español.',
                              current_talk, the_date, the_time, the_place))

        # The talk has a marker for a russian translation
        if current_talk and re.match(r'^\s*→\s*ru\s*:', line):
            # there is more than one translator
            print(format_toot('Лекция «{}» (день {} {} в зале {}) будет переведена на английский',
                              current_talk, the_date, the_time, the_place))
        
        # An empty line is the end of a talk block
        if not line.strip():
            current_talk = ''
            the_time = ''
            the_place = ''
            continue
