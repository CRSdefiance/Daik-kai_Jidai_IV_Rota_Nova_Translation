"""Append ordinary frame advances only; no special input or state edits."""
import argparse
import json
from pathlib import Path
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

JOURNAL = Path('work/analysis/duel_special_live_v1225/navigation.jsonl')
ROOT = Path('work/analysis/duel_special_observation_v1229')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--through', type=int, required=True)
    args = parser.parse_args()
    rows = [json.loads(s) for s in JOURNAL.read_text(encoding='utf-8').splitlines() if s]
    current = rows[-1]['until']
    assert 5902 <= current < args.through <= 90000
    out = ROOT/f'queued_through{args.through}.json'
    assert not out.exists()
    points = list(range(current+40, args.through, 40))+[args.through]
    commands = [{'until': n, 'duration': 1} for n in points]
    save(out, {'from': current, 'through': args.through, 'commands': commands,
        'journal_before_sha256': sha(JOURNAL.read_bytes()),
        'ordinary_frame_advances_no_buttons_fixtures_or_state_changes': True,
        'intentions_require_separate_execution_and_actual_visible_evidence': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    with JOURNAL.open('a', encoding='utf-8') as stream:
        for command in commands:
            stream.write(json.dumps(command)+'\n')
    print(len(commands), 'frame-only observation commands queued through', args.through, flush=True)


if __name__ == '__main__':
    main()
