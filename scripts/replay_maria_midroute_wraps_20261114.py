"""Exercise Maria's discipline story, the breakup, and Mikhail's peppercorn joke."""

import argparse
import sys
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import replay_maria_opening_wraps_20261114 as previous
from scripts import refine_maria_midroute_wraps_20261114 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = Path('out/maria_midroute_wraps_20261114_v2')
ROM = ROOT / 'maria_midroute_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'maria_midroute_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
PLAY_ORDER = (
    'DK4_MES_B116_R0024', 'DK4_MES_B116_R0030', 'DK4_MES_B116_R0036',
    'DK4_MES_B136_R0110', 'DK4_MES_B136_R0113',
    'DK4_MES_B139_R0072', 'DK4_MES_B139_R0076', 'DK4_MES_B139_R0080', 'DK4_MES_B139_R0084',
)
REVISED_IDS = (PLAY_ORDER[0], PLAY_ORDER[3], PLAY_ORDER[5], PLAY_ORDER[7])
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)
PAGED_ID = PLAY_ORDER[0]
RETRY_DIRECTORY = ROOT / 'before_return_retry_v1'
RETURN_FRAMES = {'before': (3900, 9350, 9650), 'after': (3900, 8850, 9050)}
CONDITIONAL_EXCERPTS = {
    'DK4_MES_B116_R0030': [340],
    'DK4_MES_B136_R0110': [510],
    'DK4_MES_B136_R0113': [510],
}


def capture_baseline_return():
    fixture = base.load(SETUP)['fixture_ROMs']['before']
    assert base.digest(fixture['path']) == fixture['sha256']
    assert base.digest(fixture['unlock']) == fixture['unlock_sha256']
    unlock = previous.validate_fixture(fixture['unlock'])
    assert not RETRY_DIRECTORY.exists()
    inputs = ROOT / 'before_return_inputs.json'
    assert not inputs.exists()
    base.save(inputs, base.load(INPUTS) + [dict(start=8750, duration=16, buttons=['A'])])
    original = sys.argv
    try:
        sys.argv = [original[0], '--rom', fixture['path'], '--out', str(RETRY_DIRECTORY),
            '--frames', str(previous.FRAME_COUNT), '--inputs-json', str(inputs),
            '--battery-save', unlock['fixture_save'], '--allow-gallery-fixtures',
            '--gallery-save-fixture-manifest', fixture['unlock'], '--touchscreen',
            '--capture-every', '999999', '--capture-at', *map(str, RETURN_FRAMES['before'])]
        previous.harness.main()
    finally:
        sys.argv = original


def verify():
    tools = previous.precedent.verify.__globals__['previous'].previous.prior
    setup, draft = map(base.load, (SETUP, stage.REVIEW))
    records = {row['id']: row for row in draft['records']}
    observed, outside = {}, {}
    evidence = {str(SETUP): base.digest(SETUP), str(INPUTS): base.digest(INPUTS)}
    for side in ('before', 'after'):
        report_path = ROOT / side / 'capture_report.json'
        report = base.load(report_path)
        previous.validate_capture(report)
        assert report['ROM_sha256'] == setup['fixture_ROMs'][side]['sha256']
        assert report['frames'] == previous.FRAME_COUNT and report['scripted_input_schedule'] == base.load(INPUTS)
        photos = tools.photos(report)
        candidates = [(frame, receipt, tools.body_masks(image))
                      for frame, (receipt, image) in sorted(photos.items()) if 4350 <= frame <= 8250]
        shown, cursor = {}, 4350
        for ident in PLAY_ORDER:
            if ident in FOLLOWING_IDS:
                planes = [setup['unchanged_transition_planes'][ident]]
            else:
                planes = [page['native_plane_hex'] for page in records[ident][side + '_native']['pages']]
            assert len(planes) == (2 if side == 'before' and ident == PAGED_ID else 1), (side, ident)
            holds = []
            for plane in planes:
                expected = tools.prior.masks(bytes.fromhex(plane))
                matches = [(frame, receipt) for frame, receipt, masks in candidates if frame > cursor and masks == expected]
                assert matches, (side, ident, cursor)
                cursor, receipt = matches[0]
                holds.append(receipt)
                evidence[receipt['path']] = base.digest(receipt['path'])
            shown[ident] = holds
        assert cursor < RETURN_FRAMES[side][1]
        observed[side] = shown
        outside_photos = photos
        if side == 'before':
            retry_path = RETRY_DIRECTORY / 'capture_report.json'
            retry = base.load(retry_path)
            previous.validate_capture(retry)
            assert retry['ROM_sha256'] == report['ROM_sha256'] and retry['frames'] == report['frames']
            assert retry['scripted_input_schedule'] == report['scripted_input_schedule'] + [
                dict(start=8750, duration=16, buttons=['A'])]
            outside_photos = tools.photos(retry)
            assert outside_photos[3900][0]['framebuffer_sha256'] == photos[3900][0]['framebuffer_sha256']
            evidence[str(retry_path)] = base.digest(retry_path)
        outside[side] = [outside_photos[frame][0]['framebuffer_sha256'] for frame in RETURN_FRAMES[side]]
        for frame in RETURN_FRAMES[side]:
            receipt = outside_photos[frame][0]
            evidence[receipt['path']] = base.digest(receipt['path'])
        evidence[str(report_path)] = base.digest(report_path)
    assert outside['before'] == outside['after'], outside
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        observed=observed, outside_exact_frames=list(zip(*RETURN_FRAMES.values(), strict=True)),
        source_commands_preserved=True, additional_baseline_page_turn_frame=8750,
        initialized_excerpts_at_Maria_entry=True, hardware=False, natural_event_eligibility_observed=False,
        earned_unlock_verified=False, verified_revised_pages=len(REVISED_IDS),
        verified_following_pages=len(FOLLOWING_IDS), observed_Ian_pages_before_after=[2, 1], evidence=evidence))


env = previous.prepare.__globals__ | globals()
prepare_source = checked_text(getsource(previous.prepare), {
    "        assert not group['existing_extra_FE_commands']":
        "        assert group['existing_extra_FE_commands'] == ([630, 1026] if block == 116 else [])",
    "        for japanese, current in zip(group['source_progressive_exchange'], group['current_progressive_exchange'], strict=True):":
        """        continuations = group['existing_extra_FE_commands']
        current_rows = [row for row in group['current_progressive_exchange'] if row['offset'] - 5 not in continuations]
        for japanese, current in zip(group['source_progressive_exchange'], current_rows, strict=True):""",
    "            assert row['word'] == 0x4000 and not row['ancestor_0100_offsets']":
        "            assert row['word'] == 0x4000 and row['ancestor_0100_offsets'] == CONDITIONAL_EXCERPTS.get(ident, [])",
    "excerpts.append(dict(id=ident, block=block, offset=offset, command=row['whole_command_hex']))":
        """excerpts.append(dict(id=ident, block=block, offset=offset, command=row['whole_command_hex'],
                                 original_conditional_ancestors=row['ancestor_0100_offsets']))""",
})
exec(compile(prepare_source, __file__ + '::same-Maria-host-and-source-mapping', 'exec'), env)
prepare = env['prepare']
capture = FunctionType(previous.capture.__code__, previous.capture.__globals__ | globals())
startup = FunctionType(previous.startup.__code__, previous.startup.__globals__ | {
    'base': base, 'ROOT': ROOT, 'ROM': ROM, 'STARTUP': STARTUP, 'SETUP': SETUP, 'stage': stage,
})
verify_storage = FunctionType(previous.verify_storage.__code__, previous.verify_storage.__globals__ | {
    'base': base, 'ROOT': ROOT, 'ROM': ROM, 'PROOF': PROOF, 'SETUP': SETUP, 'stage': stage,
})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'verify', 'verify_storage', 'startup',
                                         'capture_baseline_return'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

