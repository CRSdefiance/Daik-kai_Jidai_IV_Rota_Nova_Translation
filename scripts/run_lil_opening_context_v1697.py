"""Ordinary current-build Lil New Game; pause on the unmodified opening."""
import json
import sys
from pathlib import Path
from scripts import headless_desmume_v193 as harness
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROM=Path('out/all_routes_combined_v1676_candidate.nds')
ROOT=Path('work/analysis/lil_opening_context_v1697')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_context_v1697_1676')


if __name__=='__main__':
    assert not ROOT.exists() and not CAP.exists()
    assert sha(ROM.read_bytes())==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    inputs=Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')
    assert sha(inputs.read_bytes())=='097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'
    ROOT.mkdir(parents=True)
    journal=ROOT/'navigation.jsonl';journal.write_text('',encoding='utf-8')
    save(ROOT/'run_plan.json',{'ROM':str(ROM),'ROM_sha256':sha(ROM.read_bytes()),'inputs':str(inputs),'inputs_sha256':sha(inputs.read_bytes()),
        'capture_folder':str(CAP),'no_save_savestate_or_fixtures':True,'pause_frame':6000,
        'navigation':str(journal),'runner_sha256':sha(Path(__file__).read_bytes()),'harness_sha256':sha(Path(harness.__file__).read_bytes()),
        'unchanged_opening_context_not_new_draft_gameplay_approval':True})
    stream=GrowingCommands(journal);old=sys.stdin;sys.stdin=stream
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--capture-every','999999','--capture-at','4000','6000','--pause-at','6000',
        '--dump-capture-ram','--dump-pause-ram','--dump-ram']
    try:harness.main()
    finally:sys.stdin=old;stream.close()
    save(ROOT/'terminal.json',{'terminal':True,'no_ROM_or_input_or_fixture_change':True,'ROM_sha256':sha(ROM.read_bytes())})
