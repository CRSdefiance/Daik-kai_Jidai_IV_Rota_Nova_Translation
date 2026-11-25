"""Current Bribe display capture with declared bounded room/XP/date fixture."""
import ctypes as ct
import io
import json
import sys
import types
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_town_yard_context_v2156 as observed
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/scheme_bribe_actual_v2207')
ROM = Path('out/all_routes_combined_v2171_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/scheme_bribe_actual_v2207_V2171')
PRIOR = Path('E:/Rota Nova translations/Generated/work/emulation_v193/followup_v778_bribe_live/capture_report.json')
HARNESS = Path('scripts/headless_desmume_v193.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not CAP.exists()
    original = HARNESS.read_text()
    assert sha(HARNESS.read_bytes()) == 'd5bcc9a11b5602bfb44d54e75b02a7a7a0165c9ee819a07cd0cbdac2130b8c6e'
    old = 'from scripts.native_strategist_fixture_v624 import assign, assign_expert'
    assert original.count(old) == 1
    effective = original.replace(old, 'from scripts.native_scheme_context_fixture_v2204 import assign, assign_expert')
    harness = types.ModuleType('current_bribe_harness')
    harness.__file__ = str(HARNESS.resolve())
    exec(compile(effective, str(HARNESS), 'exec'), harness.__dict__)
    observed.ROOT, observed.ROM = ROOT, ROM
    observed.prepare_contract()
    prior = read(PRIOR)
    donor = Path(prior['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == '05fa512b078fd01a8f6bee605254e9f72bfe3453c0ea098d977c87d86b6b693e'
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    inputs = ROOT/'recorded_input_schedule.json'
    save(inputs, prior['scripted_input_schedule'])
    frames = sorted({r['frame'] for r in prior['frames_captured']})
    commands = [{'until': 13200, 'strategist_expert_fixture': True, 'duration': 8}, {'stop': True}]
    save(ROOT/'run_plan.json', dict(candidate=str(ROM), candidate_sha256=digest, inputs=str(inputs), inputs_sha256=sha(inputs.read_bytes()), commands=commands, maximum_frames=13201, captures=frames, prior_report=str(PRIOR), prior_report_sha256=sha(PRIOR.read_bytes()), battery_donor=str(donor), donor_sha256=sha(donor.read_bytes()), source_battery_provenance_is_inherited_not_reearned=True, fixture='three room/assignment bytes, one XP word to300000, calendar+528 ticks=11days; no other 4MiB bytes', no_earned_assignment_XP_time_or_campaign_credit=True, no_savestate=True, fixture_producer='scripts/native_scheme_context_fixture_v2204.py', fixture_producer_sha256=sha(Path('scripts/native_scheme_context_fixture_v2204.py').read_bytes()), harness_sha256=sha(HARNESS.read_bytes()), single_import_replacement=True, effective_harness_sha256=sha(effective.encode()), observer_sha256=sha(Path(observed.__file__).read_bytes()), producer_sha256=sha(Path(__file__).read_bytes()), full_goal_complete=False))
    observers = []
    class Proxy:
        def __getattr__(self, name): return getattr(ct, name)
        def CDLL(self, path, *args, **kwargs):
            core = ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith('desmume_libretro.dll'):
                observer = observed.Observer(core, CAP/'common_observer')
                observers.append(observer)
                observer.install()
                old_run = core.retro_run
                old_run.restype = None
                def run():
                    observer.next_frame()
                    old_run()
                core.retro_run = run
            return core
    harness.ct = Proxy()
    previous_stdin = sys.stdin
    sys.stdin = io.StringIO(''.join(json.dumps(c)+'\n' for c in commands))
    sys.argv = ['headless_desmume_v193.py', '--rom', str(ROM), '--out', str(CAP), '--frames', '13201', '--inputs-json', str(inputs), '--battery-save', str(donor), '--touchscreen', '--capture-every', '999999', '--capture-at', *map(str, frames), '--dump-capture-ram', '--dump-ram', '--pause-at', '3200', '--dump-pause-ram', '--allow-strategist-fixtures']
    try:
        harness.main()
    finally:
        sys.stdin = previous_stdin
        for observer in observers: observer.close()
    for observer in observers: observer.save()
    report = read(CAP/'capture_report.json')
    fixture, = report['synthetic_strategist_room_assignment_fixtures']
    assert report['frames'] == 13200 and fixture['frame'] == 3200
    assert fixture['all_other4MiB_bytes_exact'] and fixture['only_three_assignment_bytes_one_XP_word_one_calendar_word_owned']
    assert len(fixture['changes']) <= 11
    assert sha(donor.read_bytes()) == prior['battery_save_preloaded']['source_sha256']
    assert HARNESS.read_text() == original
    save(ROOT/'terminal.json', dict(terminal=True, frames=13200, candidate_sha256=digest, original_harness_core_donor_unchanged=True, all_observer_host_slots_restored=True, declared_fixture_only=True, no_earned_progress_or_full_route_claim=True, full_goal_complete=False))
