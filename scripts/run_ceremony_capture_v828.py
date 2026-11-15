"""Frozen harness with one source-bound map/date access import replacement."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


if __name__ == '__main__':
    path = Path('scripts/headless_desmume_v193.py')
    source = path.read_text(encoding='utf-8')
    assert sha(path.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    old = 'from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(old) == 1
    effective = source.replace(old,'from scripts.native_ceremony_map_fixture_v828 import set_condition')
    exec(compile(effective,str(path),'exec'),{'__name__':'__main__','__file__':str(path.resolve())})
    assert path.read_text(encoding='utf-8') == source
    out = Path(sys.argv[sys.argv.index('--out')+1])
    report = read(out/'capture_report.json')
    report['source_map_fixture_adapter_v828'] = dict(original_harness_sha256=sha(path.read_bytes()),
        effective_program_sha256=sha(effective.encode()),single_declared_fixture_import_replacement=True,
        source_hashes={str(p):sha(p.read_bytes()) for p in (Path(__file__),Path('scripts/native_ceremony_map_fixture_v828.py'),
            Path('scripts/native_ceremony_map_fixture_v814.py'),Path('scripts/native_ceremony_istanbul_fixture_v827.py'))},
        no_captain_dialogue_source_code_random_state_or_quest_fixture_available=True)
    save(out/'capture_report.json',report)
