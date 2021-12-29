from datetime import time, timedelta
from hamcrest import assert_that, equal_to
from prepare_toot import format_toot
from extract import Talk


def test_de():
    talk = Talk(title='some talk',
                date=1,
                time=time.fromisoformat("14:00"),
                duration=timedelta(hours=1),
                place='heaven',
                speaker='',
                language='',
                fahrplan_url='URL',
                translations=('de'),
                translators=('one', 'two'))
    assert_that(format_toot(talk, 'de'),
                equal_to('Der Vortrag "some talk" (Tag 1 14:00:00 im Raum heaven) wird auf Deutsch übersetzt. URL'))
