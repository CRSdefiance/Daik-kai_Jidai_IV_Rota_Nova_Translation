"""Fresh current-ROM Maria New Game context;only the existing system-unlock save is a fixture."""
from pathlib import Path
import sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts import headless_desmume_v193 as harness
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/current_Maria_context_v4997')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/current_Maria_context_v4997_V4987')
ROM=Path('out/all_routes_combined_v4987_candidate.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not CAP.exists();digest=sha(ROM.read_bytes())
    assert digest==read(ROM.with_suffix('.manifest.json'))['candidate_sha256']==read('work/analysis/editorial_handoff_verification_v4993/verified_handoff.json')['candidate_sha256']
    priorpath=Path('work/analysis/maria_opening_context_v2035/run_plan.json');prior=read(priorpath)
    donor=Path(prior['existing_isolated_system_unlock_save']);assert sha(donor.read_bytes())==prior['save_sha256']
    fixture=read(prior['fixture_manifest']);assert fixture['only_system_low_four_bits_and_original_checksum_changed'] and fixture['all_six_route_save_slots_and_footer_unchanged'] and not fixture['earned_unlock_verified']
    fixture.update(production_ROM=str(ROM),production_ROM_sha256=digest,current_test_scope='Fresh current-ROM ordinary Maria NewGame context for native speaker/macro binding. Existing system unlock is not earned;no B97 activation,story,location,RNG,funds,roster or outcome fixture.')
    sourcepath=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030/capture_report.json');source=read(sourcepath)
    schedule=[r for r in source['scripted_input_schedule'] if r['start']<31001]
    ROOT.mkdir(parents=True);inputs=ROOT/'original_Maria_inputs.json';save(inputs,schedule);fp=ROOT/'existing_system_unlock_manifest.json';save(fp,fixture)
    captures=[1,60,180,2000,3200,4000,10000,20000,28000,30000,31000]
    save(ROOT/'run_plan.json',dict(candidate=str(ROM),candidate_sha256=digest,frames=31001,captures=captures,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        prior_plan=str(priorpath),prior_plan_sha256=sha(priorpath.read_bytes()),prior_report=str(sourcepath),prior_report_sha256=sha(sourcepath.read_bytes()),
        existing_isolated_system_unlock_save=str(donor),save_sha256=sha(donor.read_bytes()),fixture_manifest=str(fp),fixture_manifest_sha256=sha(fp.read_bytes()),
        no_savestate_story_location_RNG_funds_actor_roster_or_outcome_fixture=True,earned_unlock_verified=False,not_selected_B97_activation=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    sys.argv=['headless_desmume_v193.py','--rom',str(ROM),'--out',str(CAP),'--frames','31001','--inputs-json',str(inputs),
        '--battery-save',str(donor),'--allow-gallery-fixtures','--gallery-save-fixture-manifest',str(fp),
        '--capture-every','999999','--capture-at',*map(str,captures),'--dump-capture-ram','--dump-ram','--touchscreen']
    harness.main();report=read(CAP/'capture_report.json')
    assert report['cold_boot'] and report['frames']==31001 and not report['savestate_loaded'] and not report['callback_errors']
    assert sha(donor.read_bytes())==prior['save_sha256']
    save(ROOT/'terminal.json',dict(terminal=True,candidate=str(ROM),candidate_sha256=digest,frames=31001,report=str(CAP/'capture_report.json'),
        report_sha256=sha((CAP/'capture_report.json').read_bytes()),existing_system_unlock_not_earned=True,source_donor_unchanged=True,
        no_new_RAM_code_story_location_RNG_funds_actor_roster_or_outcome_fixture=True,not_selected_B97_activation=True,full_goal_complete=False))
    print('Fresh31001-frame Maria NewGame context terminal;existing system unlock only. No B97 activation or earned unlock claim.')
