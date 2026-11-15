"""Frozen harness with mapped location/date/access fixtures; actual hero retained."""

import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


if __name__=='__main__':
    path=Path('scripts/headless_desmume_v193.py');source=path.read_text(encoding='utf-8')
    assert sha(path.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    effective=source
    for old,new in (
        ('from scripts.native_condition_fixture_v520 import set_condition','from scripts.native_ceremony_hero_fixture_v825 import set_condition'),
        ('from scripts.native_location_fixture_v519 import relocate','from scripts.native_ceremony_hero_fixture_v825 import relocate')):
        assert effective.count(old)==1;effective=effective.replace(old,new)
    exec(compile(effective,str(path),'exec'),{'__name__':'__main__','__file__':str(path.resolve())})
    assert path.read_text(encoding='utf-8')==source
    out=Path(sys.argv[sys.argv.index('--out')+1]);d=read(out/'capture_report.json')
    d['actual_hero_fixture_adapter_v825']=dict(original_harness_sha256=sha(path.read_bytes()),
        effective_program_sha256=sha(effective.encode()),only_two_declared_fixture_import_replacements=True,
        adapter_sha256=sha(Path(__file__).read_bytes()),
        fixture_sha256=sha(Path('scripts/native_ceremony_hero_fixture_v825.py').read_bytes()),
        no_captain_actor_dialogue_or_random_state_fixture_available=True)
    save(out/'capture_report.json',d)
