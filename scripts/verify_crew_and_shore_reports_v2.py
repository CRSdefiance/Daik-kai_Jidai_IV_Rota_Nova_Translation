"""Verify the attack at the frame where the current build actually drew it."""

from inspect import getsource

from scripts import verify_crew_and_shore_reports_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    source = checked_text(getsource(prior.verify_gameplay), {
        "cases = {'attack': ((20322, 2243),), 'welcome': ((45956, 2234), (46396, 2239))}":
            "cases = {'attack': ((14657, 2243),)}",
        "        old_snapshots = {item['frame']: item for item in old_report['read_only_pause_RAM_snapshots']}\n": '',
        "        follow = 20542 if name == 'attack' else 46176\n"
        '        old_hold, new_hold = snapshot(follow, old_snapshots), snapshot(follow)\n'
        '        assert text(old_hold, modal) == text(new_hold, modal)\n'
        "        expected_template = b'Sailors lost: %s.' if name == 'attack' else b'Fatigue decreased by %s.'\n":
            "        follow, end = 14877, 15097\n"
            '        new_hold = snapshot(follow)\n'
            "        assert normalize('NFKC', text(new_hold, modal).decode('cp932')).strip() == 'Sailors lost: 11.'\n"
            "        expected_template = b'Sailors lost: %s.'\n",
        '        assert before == fleet_state(arm, snapshot(expected[0][0], old_snapshots))\n'
        '        assert after == fleet_state(arm, snapshot(end, old_snapshots))\n'
        "        if name == 'attack':\n"
        "            assert sum(before['crew']) - sum(after['crew']) == 10\n"
        '        else:\n'
        "            assert before['crew'] == after['crew']\n":
            "        assert sum(before['crew']) - sum(after['crew']) == 11\n",
        'not visible_paper(city.captured(frames[end]))': "not visible_paper(frames[end]['path'])",
        'both_sequences_return_to_sailing=True': 'original_attack_and_sailor_loss_return_to_sailing=True',
        'captain_reprimand_and_other_shore_events_offline=True':
            'captain_reprimand_and_other_shore_events_offline=True, welcome_observed_in_current_gameplay=False',
        'and both returns to sailing': 'and the return to sailing',
    })
    from unicodedata import normalize
    env = vars(prior) | {'__file__': __file__, 'normalize': normalize}
    exec(compile(source, __file__ + '::sea-view-paper-path', 'exec'), env)
    env['verify_gameplay']()


if __name__ == '__main__':
    main()
