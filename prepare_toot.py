
translation_table = {
    'de': 'Der Vortrag "{talk.title}" (Tag {talk.date} {talk.time} im Raum {talk.place}) wird auf Deutsch übersetzt. {talk.fahrplan_url}',
    'en': 'The talk "{talk.title}" (day {talk.date} {talk.time} in room {talk.place}) will be translated to english. {talk.fahrplan_url}',
    'es': 'La charla "{talk.title}" (día {talk.title}, a las {talk.time}, salón {talk.place}) será traducida al español. {talk.fahrplan_url}',
    'fr': 'La conférence «{talk.title}» (jour {talk.date}, {talk.time} en salle {talk.place}) sera traduite en français. {talk.fahrplan_url}',
    'pl': 'Wykład "{talk.title}" (dzień {talk.date}, {talk.time} w sali {talk.place}) będzie tłumaczony na polski. {talk.fahrplan_url}',
    'ru': 'Лекция «{talk.title}» (день {talk.date} {talk.time} в зале {talk.place}) будет переведена на английский. {talk.fahrplan_url}',
}


def format_toot(talk, language):
    return translation_table[language].format(talk=talk)

