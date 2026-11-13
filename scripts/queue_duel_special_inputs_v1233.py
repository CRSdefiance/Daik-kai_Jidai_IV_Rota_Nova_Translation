"""Predeclared ordinary timed-A coverage; never edits eligibility or RNG."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/duel_special_inputs_v1233')
JOURNAL = Path('work/analysis/duel_special_live_v1232/navigation.jsonl')


def main():
    assert not ROOT.exists()
    rows = [json.loads(s) for s in JOURNAL.read_text(encoding='utf-8').splitlines() if s]
    assert rows[-1] == {'until': 5902, 'duration': 1}
    presses = set(range(5902, 7903, 83))
    points = sorted({*range(5942, 9503, 40), *presses, 9502}-{5902})
    current, commands = 5902, []
    for target in points:
        assert target > current
        command = {'until': target, 'duration': 1}
        if current in presses:
            command['buttons'] = ['A']
        commands.append(command)
        current = target
    ROOT.mkdir(parents=True)
    save(ROOT/'ordinary_timed_A_intentions.json', {
        'journal_before_sha256': sha(JOURNAL.read_bytes()), 'commands': commands,
        'predeclared83frame_period_not_a_searched_seed_or_forced_outcome': True,
        'ordinary_A_events_begin_at_previous_pause_frame_plus1': True,
        'no_fixtures_or_RAM_RNG_eligibility_or_result_changes_after_duel': True,
        'intentions_are_not_execution_receipts': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    with JOURNAL.open('a', encoding='utf-8') as stream:
        for command in commands:
            stream.write(json.dumps(command)+'\n')
    print(len(commands), 'ordinary input/observation commands queued through9502.', flush=True)


if __name__ == '__main__':
    main()
