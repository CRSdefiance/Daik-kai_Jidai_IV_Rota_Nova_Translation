"""Verify name substitutions and a two-page rumor on Rafael's current route."""

import argparse
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_rafael_name_wraps_20261114 as previous
from scripts import stage_rafael_crew_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/rafael_crew_wraps_20261114_v2')
ROM = ROOT / 'rafael_crew_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_crew_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 8801
EXCERPTS = ((84, 1068, 1218), (91, 744, 860), (101, 820, 1126))
FOLLOWING_IDS = ('DK4_MES_B84_R0097', 'DK4_MES_B91_R0073', 'DK4_MES_B101_R0071')
REVISED_IDS = ('DK4_MES_B84_R0089', 'DK4_MES_B84_R0093', 'DK4_MES_B91_R0070', 'DK4_MES_B101_R0068')
PLAY_ORDER = (REVISED_IDS[0], REVISED_IDS[1], FOLLOWING_IDS[0], REVISED_IDS[2],
              FOLLOWING_IDS[1], REVISED_IDS[3], FOLLOWING_IDS[2])
env = vars(previous) | globals() | {'previous': previous.previous}


def derive(function, changes):
    source = checked_text(getsource(function), changes)
    exec(compile(source, __file__ + '::prior-Rafael-fixture-contract', 'exec'), env)
    return env[function.__name__]


prepare = derive(previous.prepare, {
    "assert len(selected) == 2 and all": "assert len(selected) in (2, 3) and all",
    'first, last = selected': 'first, last = selected[0], selected[-1]',
    "assert first['offset'] + first['native_extent'] == last['offset']":
        "assert all(a['offset'] + a['native_extent'] == b['offset'] for a, b in zip(selected, selected[1:]))",
    'assert len(speeches) == 10 and len(rows) == 21': 'assert len(speeches) == 7 and len(rows) == 18',
    'Ten original speech commands': 'Seven original speech commands',
    'stage.bare_tokens(body)': 'stage.previous.bare_tokens(body)',
    "group['current_progressive_exchange'], strict=True":
        "[row for row in group['current_progressive_exchange'] if row['offset'] - 5 not in group['existing_extra_FE_commands']], strict=True",
})
capture = FunctionType(previous.capture.__code__, vars(previous) | globals() | {'previous': previous.previous})
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | globals() | {'previous': previous.previous})


def verify():
    tools = previous.previous.previous.prior
    setup, draft = map(base.load, (SETUP, stage.REVIEW))
    records = {row['id']: row for row in draft['records'] if row['id'] in REVISED_IDS}
    assert set(records) == set(REVISED_IDS)
    observed, outside, evidence = {}, {}, {str(SETUP): base.digest(SETUP)}
    for side in ('before', 'after'):
        report_path = ROOT / side / 'capture_report.json'
        report = base.load(report_path)
        assert report['ROM_sha256'] == setup['fixture_ROMs'][side]['sha256'] and report['frames'] == FRAME_COUNT
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not any(v for k, v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule'] == base.load(INPUTS)
        photos = tools.photos(report)
        candidates = [(frame, photo, tools.body_masks(image)) for frame, (photo, image) in sorted(photos.items())]
        shown, last_frame = {}, 2200
        for ident in PLAY_ORDER:
            transition = setup['unchanged_transition_planes'].get(ident)
            planes = [transition] if transition else [page['native_plane_hex'] for page in records[ident][side + '_native']['pages']]
            holds = []
            for plane in planes:
                expected = tools.prior.masks(bytes.fromhex(plane))
                found = [(frame, photo) for frame, photo, mask in candidates if frame > last_frame and mask == expected]
                assert found, (side, ident, last_frame)
                last_frame, photo = found[0]
                holds.append(photo)
                evidence[photo['path']] = base.digest(photo['path'])
            shown[ident] = holds
        assert len(shown['DK4_MES_B101_R0068']) == 2
        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in (2200, 8500, 8700)]
        observed[side] = shown
        evidence[str(report_path)] = base.digest(report_path)
    assert outside['before'] == outside['after']
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        observed=observed, outside_exact_frames=[2200, 8500, 8700], source_commands_preserved=True,
        initialized_excerpts_at_Rafael_entry=True, hardware=False, natural_event_eligibility_observed=False,
        verified_revised_pages=5, verified_following_pages=3, evidence=evidence))
    print('Matched the company and full name, the two-page rumor, the charm and three following replies.')


verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | dict(
    stage=stage, SETUP=SETUP, ROM=ROM, PROOF=PROOF, __file__=__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

