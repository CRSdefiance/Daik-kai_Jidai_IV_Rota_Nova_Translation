"""Replay the existing Athens schedule, omitting one discarded scheduler random call for a causal control."""

import json
import sys
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save


if __name__=='__main__':
    rom=Path(sys.argv[sys.argv.index('--rom')+1])
    assert rom.name in ('all_routes_combined_v803_candidate.nds','all_routes_combined_v809_candidate.nds','all_routes_combined_v820_candidate.nds')
    version=803 if 'v803_' in rom.name else 809
    original=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/f'ceremony_v{version}_Athens_climb_frame_probe'
    journal=read(original/'navigation_command_journal.json')
    commands=[dict(r['command']) for r in journal['commands_received']]
    assert all(r['validation_passed'] for r in journal['commands_received'])
    indexes=[n for n,r in enumerate(journal['commands_received']) if r['frame']==18200]
    assert len(indexes)==1
    assert 'condition_fixture' not in commands[indexes[0]]
    iterator=iter(commands)
    def replay_input(prompt=''):
        return json.dumps(next(iterator))
    harness=Path('scripts/headless_desmume_v193.py');source=harness.read_text(encoding='utf-8')
    assert sha(harness.read_bytes())=='d5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    before='from scripts.native_condition_fixture_v520 import set_condition'
    assert source.count(before)==1
    effective=source.replace(before,'from scripts.native_ceremony_yield_control_v823 import set_condition')
    exec(compile(effective,str(harness),'exec'),{'__name__':'__main__','__file__':str(harness.resolve()),'input':replay_input})
    assert next(iterator,None) is None and harness.read_text(encoding='utf-8')==source
    out=Path(sys.argv[sys.argv.index('--out')+1]);report=read(out/'capture_report.json')
    report['ordinary_V820_Athens_replay_adapter_v823']=dict(original_schedule=str(original),
        original_harness_sha256=sha(harness.read_bytes()),effective_program_sha256=sha(effective.encode()),
        no_additional_condition_request=True,automatic_replay_of_original44_validated_commands=True,
        no_playable_ROM_registry_or_donor_changes=True,
        adapter_sha256=sha(Path(__file__).read_bytes()),
        trace_fixture_sha256=sha(Path('scripts/native_ceremony_yield_control_v823.py').read_bytes()))
    save(out/'capture_report.json',report)
