"""Explicit autonomous successor; position only while the original fleet is unseen."""
from pathlib import Path


def main():
    source = Path('scripts/run_sighting_gameplay_v1091.py')
    target = Path('scripts/run_sighting_gameplay_v1095.py')
    assert not target.exists()
    body = source.read_text(encoding='utf-8')
    body = body.replace('sighting_gameplay_v1091_', 'sighting_gameplay_v1095_').replace(
        'sighting_v1091_1086_', 'sighting_v1095_1086_')
    body = body.replace('from scripts.run_activity_special_live_v988 import GrowingCommands',
                        'from scripts.sighting_autonav_v1095 import CloseCommands')
    body = body.replace('stream=GrowingCommands(journal)', 'stream=CloseCommands(journal,cap,root,case)')
    target.write_text(body, encoding='utf-8')
    print('Created V1095 cold-boot successor; all prior runners preserved.')


if __name__ == '__main__':
    main()
