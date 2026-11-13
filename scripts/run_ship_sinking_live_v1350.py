"""Cold-load the ordinary five-ship save for original sinking-event tests.

Starts fixture-free at the established departure prefix. A future declared
prebattle fixture is lazily loaded only if explicitly requested in the journal.
"""
import sys
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts import native_battle_fixture_v620 as dispatch
from scripts.run_activity_special_live_v988 import GrowingCommands
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_live_v1350')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_v1350_1344')
ROM = Path('out/all_routes_combined_v1344_candidate.nds')
HARNESS = 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'


def fixture(arm,raw,request):
    from scripts.native_ship_sinking_fixture_v1351 import apply_fixture
    return apply_fixture(arm,raw,request)


def main():
    assert not ROOT.exists() and not CAP.exists()
    release = read('work/analysis/ship_sinking_release_v1343/registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']=='9d455782724d98198b7bc3fdac7be755945e58d406e66a4634094d9a0eab301b'
    assert sha(Path(harness.__file__).read_bytes())==HARNESS
    saved = read('work/analysis/full_fleet_battle_v652/staffing_proof.json')['prepared_save']
    source = Path(saved['path'])
    assert sha(source.read_bytes())==saved['sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
    ROOT.mkdir(parents=True)
    donor = ROOT/'disposable_five_ship.dsv'
    copy2(source,donor)
    inputs = ROOT/'original_departure_inputs.json'
    copy2(Path('work/analysis/full_fleet_battle_v652/departure_prefix.json'),inputs)
    journal = ROOT/'navigation.jsonl'
    journal.write_text('',encoding='utf-8')
    save(ROOT/'run_plan.json',{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'source_donor':str(source),'source_donor_sha256':saved['sha256'],'disposable_donor':str(donor),
        'original_load_inputs':str(inputs),'original_load_inputs_sha256':sha(inputs.read_bytes()),
        'capture_folder':str(CAP),'append_only_navigation':str(journal),
        'initial_pause_frame':4800,'initial_load_is_fixture_free':True,
        'only_declared_prebattle_fixture_may_be_requested_later':True,
        'no_actor_ID_RNG_eligibility_or_result_injection_or_during_battle_health_position_changes':True,
        'harness_sha256':HARNESS,'runner_sha256':sha(Path(__file__).read_bytes())})
    stream = GrowingCommands(journal)
    old_stdin,old_fixture = sys.stdin,dispatch.apply_fixture
    sys.stdin,dispatch.apply_fixture = stream,fixture
    sys.argv = ['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','100000',
        '--inputs-json',str(inputs),'--touchscreen','--capture-every','999999','--capture-at','4800',
        '--battery-save',str(donor),'--pause-at','4800','--dump-capture-ram','--dump-pause-ram','--dump-ram',
        '--allow-battle-fixtures']
    try:
        harness.main()
    finally:
        sys.stdin,dispatch.apply_fixture = old_stdin,old_fixture
        stream.close()
    assert sha(source.read_bytes())==sha(donor.read_bytes())==saved['sha256']
    save(ROOT/'terminal_preservation.json',{'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':saved['sha256'],'navigation_sha256':sha(journal.read_bytes()),
        'no_scene_or_completion_credit_without_separate_actual_verification':True})
    print('Original five-ship sinking test terminal;source/disposable saves unchanged.',flush=True)


if __name__=='__main__':
    main()
