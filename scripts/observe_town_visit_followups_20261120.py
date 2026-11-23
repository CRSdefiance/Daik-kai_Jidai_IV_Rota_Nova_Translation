"""Follow Genoa's Tavern conversation and enter Tripoli from its loaded Port screen."""

from argparse import ArgumentParser
from inspect import getsource

from scripts import observe_additional_town_visits_20261120 as initial
from scripts.source_locked_derivation_v5118 import checked_text


def schedule(case):
    city = {'genoa_tavern': 'genoa', 'tripoli_town': 'tripoli'}[case]
    events, captures, end, path, donor = initial.schedule(city)
    if case == 'genoa_tavern':
        # The first visit stopped partway through Julio's complaint.
        # Advance with the regular confirm button and document the branch selected.
        events = [row for row in events if row['start'] <= 10601]
        starts = range(11001, 26602, 400)
        events += [dict(start=frame, duration=8, buttons=['A']) for frame in starts]
        captures = [9950, 10350, 10750, *(frame + 149 for frame in starts)]
        end = 27000
    else:
        # A at 3401 opens the Port menu on this save. Stay in town instead.
        events = [row for row in events if row['start'] != 3401]
    return events, captures, end, path, donor


def main(case):
    source = checked_text(getsource(initial.main), {'get_schedule=schedule': 'get_schedule=followup_schedule'})
    scope = vars(initial) | dict(followup_schedule=schedule, __file__=__file__)
    exec(compile(source, __file__ + '::follow-up-inputs', 'exec'), scope)
    scope['main'](case)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('genoa_tavern', 'tripoli_town'))
    main(parser.parse_args().case)
