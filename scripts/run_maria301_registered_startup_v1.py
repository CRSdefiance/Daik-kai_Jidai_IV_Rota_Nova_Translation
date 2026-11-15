"""Cold-boot the exact cumulative candidate with ordinary Maria inputs andthe existing unlock."""
from pathlib import Path
import sys
from scripts.build_registered_maria301_v1 import CANDIDATE,STAGED,OUT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts import headless_desmume_v193 as harness

ROOT = OUT/'own_startup_run_v1'


def main():
    assert not ROOT.exists()
    staged = load(STAGED)
    assert digest(CANDIDATE) == staged['candidate_sha256'] and staged['clean_input_patch_byte_exact']
    assert staged['own_registered_startup_pending']
    prior_path = Path('work/Maria_current_context_20261109_v1/run_plan.json')
    prior = load(prior_path)
    donor = Path(prior['donor']);assert digest(donor) == prior['donor_sha256']
    unlock = load(prior['fixture_manifest'])
    assert digest(prior['fixture_manifest']) == prior['fixture_manifest_sha256']
    assert unlock['only_system_low_four_bits_and_original_checksum_changed']
    assert unlock['all_six_route_save_slots_and_footer_unchanged'] and not unlock['earned_unlock_verified']
    ROOT.mkdir();inputs = ROOT/'ordinary_Maria_inputs.json'
    inputs.write_bytes(Path(prior['inputs']).read_bytes());assert digest(inputs) == prior['inputs_sha256']
    unlock.update(production_ROM=str(CANDIDATE),production_ROM_sha256=digest(CANDIDATE),
        current_test_scope='Own cumulative Maria301 candidate coldboot/NewGame/complete unchanged opening to Hangzhou. Existing system-only unlock is not earned; no story/RAM/location/RNG/funds/outcome fixture.')
    fixture = ROOT/'existing_system_unlock_manifest.json';save(fixture,unlock)
    captures = [1600,2200,3340,4000,16000,31000]
    save(ROOT/'run_plan.json',dict(candidate=str(CANDIDATE),candidate_sha256=digest(CANDIDATE),
        staged=str(STAGED),staged_sha256=digest(STAGED),prior_plan=str(prior_path),prior_plan_sha256=digest(prior_path),
        frames=31000,inputs=str(inputs),inputs_sha256=digest(inputs),donor=str(donor),donor_sha256=digest(donor),
        fixture_manifest=str(fixture),fixture_manifest_sha256=digest(fixture),captures=captures,
        no_savestate_story_location_RNG_funds_actor_roster_oroutcome_fixture=True,
        only_preexisting_system_unlock_not_earned=True,producer_sha256=digest(Path(__file__)),new_credit=0))
    capture = ROOT/'capture'
    sys.argv = ['headless_desmume_v193.py','--rom',str(CANDIDATE),'--out',str(capture),'--frames','31000',
        '--inputs-json',str(inputs),'--battery-save',str(donor),'--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest',str(fixture),'--capture-every','999999',
        '--capture-at',*map(str,captures),'--dump-ram']
    harness.main()
    report_path = capture/'capture_report.json';report = load(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 31000 and report['ROM_sha256'] == staged['candidate_sha256']
    assert digest(donor) == prior['donor_sha256']
    save(ROOT/'terminal.json',dict(terminal=True,frames=31000,candidate_sha256=staged['candidate_sha256'],
        report=str(report_path),report_sha256=digest(report_path),source_donor_unchanged=True,
        existing_system_unlock_not_earned=True,visual_andnative_own_startup_verification_pending=True,new_credit=0))
    print('Own cumulative Maria301 coldboot terminal;31,000 frames. Verify native state andreview new captures before registration.')


if __name__ == '__main__':main()
