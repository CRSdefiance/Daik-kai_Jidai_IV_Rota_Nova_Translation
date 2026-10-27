"""Retain the full failing gate and separately record its completed glyph stage."""

import inspect
import traceback
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ceremony_families_gameplay_v815 as original
from scripts.native_ceremony_athens_fixture_v816 import set_condition
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_Athens_v816')
SPEC = Path('work/analysis/ceremony_access_v810/Athens_site_rites_spec_v816.json')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    old_proof = read('work/analysis/ceremony_access_v810/site_chant_gameplay_verification_v815.json')
    assert sha(Path(original.__file__).read_bytes()) == old_proof['producer_sha256']

    def Athens_condition(arm, raw, request):
        assert request['mode'] == 'ceremony-family'
        return set_condition(arm, raw, {**request, 'mode': 'ceremony-Athens'})

    loader = FunctionType(original.load.__code__, {**original.__dict__, 'set_condition': Athens_condition})
    source = inspect.getsource(original.verify)
    needle = '    states = []\n'
    assert source.count(needle) == 1
    insertion = '''    save(ROOT/'Athens_site_glyph_stage_only_v817.json', dict(
        candidate=new['ROM'], candidate_sha256=new['ROM_sha256'], specification=spec,
        capture_reports=[str(op),str(np)], complete_scene_holds=holds,
        full_screen_controls=controls, outside_body_controls=outside,
        all_complete_native_and_independent_font_planes_and_captured_buffers_pass=True,
        original_deterministic_and_persistent_state_stage_not_yet_approved=True,
        full_gate_passed=False, completion_credit=0, full_goal_complete=False,
        source_verifier_sha256=sha(Path(original.__file__).read_bytes()),
        effective_verifier_sha256=sha(effective_source.encode()),
        producer_sha256=sha(Path(__file__).read_bytes())))
    states = []
'''
    effective = source.replace(needle, insertion)
    assert effective.count('assert ') == source.count('assert ')
    env = {**original.__dict__, 'ROOT': ROOT, 'load': loader, 'original': original,
           'effective_source': effective, '__file__': str(Path(__file__).resolve())}
    exec(compile(effective, str(Path(__file__)), 'exec'), env)
    (ROOT/'effective_full_gate_with_glyph_checkpoint_v817.py').write_text(effective, encoding='utf-8')
    try:
        env['verify'](read(SPEC))
    except AssertionError as error:
        save(ROOT/'Athens_site_full_gate_failure_v817.json', dict(
            full_gate_passed=False, assertion=str(error), traceback=traceback.format_exc(),
            glyph_stage=str(ROOT/'Athens_site_glyph_stage_only_v817.json'),
            no_assertions_removed_or_failures_waived=True,
            source_verifier_sha256=sha(Path(original.__file__).read_bytes()),
            effective_verifier_sha256=sha(effective.encode()),
            producer_sha256=sha(Path(__file__).read_bytes()),
            next='Trace post-dismissal random calls/time update; obtain source-bound equal-input outcome evidence.',
            completion_credit=0, full_goal_complete=False))
        print('Full state gate remains FAILED: '+str(error), flush=True)
        raise


if __name__ == '__main__':
    main()
