"""Replay the five name-bearing speeches in a scoped Rafael opening fixture."""

import argparse
import sys
from pathlib import Path
from struct import pack_into, unpack_from
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_charlotte_wraps_20261114 as previous
from scripts import stage_rafael_name_wraps_20261114 as stage


base = stage.base
ROOT = Path('out/rafael_name_wraps_20261114_v1')
ROM = ROOT / 'rafael_name_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'rafael_name_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 8801
EXCERPTS = ((63, 1310, 1464), (64, 1752, 1902), (64, 2094, 2244), (69, 1120, 1296), (70, 444, 512))
FOLLOWING_IDS = ('DK4_MES_B63_R0117', 'DK4_MES_B64_R0138', 'DK4_MES_B64_R0155',
                 'DK4_MES_B69_R0146', 'DK4_MES_B70_R0055')
REVISED_IDS = tuple(stage.DECISIONS)
PLAY_ORDER = tuple(item for group in zip(REVISED_IDS, FOLLOWING_IDS, strict=True) for item in group)


def prepare():
    draft, proof = map(base.load, (stage.REVIEW, stage.PROOF))
    assert base.digest(stage.REVIEW) == proof['review_sha256']
    assert base.digest(stage.parent.ROM) == proof['candidate_sha256']
    original, target = (base.NdsImage.open(stage.parent.ROM) for _ in range(2))
    clean_archive = original.read_file(stage.FILE)
    for path, raw in stage.prior.transform(original, draft['records']):
        assert path == stage.FILE and raw == Path(proof['archives'][path]['path']).read_bytes()
        target.replace_file(path, raw)
    assert not ROOT.exists()
    ROOT.mkdir()
    target.save(ROM)
    target.replace_file(stage.FILE, clean_archive)
    assert bytes(target.rom.save()) == stage.parent.ROM.read_bytes()
    capture = base.load(stage.CAPTURE)
    inputs = capture['scripted_input_schedule'] + [
        dict(start=frame, duration=5, buttons=['A']) for frame in range(3800, 8401, 320)]
    base.save(INPUTS, inputs)

    inventory, _, _ = stage.prior.scoped_inventory()
    arm = original.read_file(stage.ARM)
    _, painter = stage.prior.precedent.planners(arm)
    font = original.read_file('/GRP/KANJI.FNT')
    transition = {}
    for group in draft['complete_exchange_references']:
        for ja, en in zip(group['source_progressive_exchange'], group['current_progressive_exchange'], strict=True):
            ident = f"DK4_MES_B{group['block']}_R{ja['record_index']:04d}"
            if ident in FOLLOWING_IDS:
                body = bytes.fromhex(en['raw_hex'])[1:]
                assert not stage.bare_tokens(body)
                page, = painter(arm, font, body)['pages']
                transition[ident] = page['native_plane_hex']
    assert set(transition) == set(FOLLOWING_IDS)

    fixtures = {}
    for side, source in [('before', stage.parent.ROM), ('after', ROM)]:
        image = base.NdsImage.open(source)
        archive = image.read_file(stage.FILE)
        bank = stage.IlnkContainer.parse(archive)
        initial = bank.blocks[44][:40]
        logical = bytearray(initial)
        commands = []
        for block, start, stop in EXCERPTS:
            raw = bank.blocks[block]
            selected = [row for row in inventory(arm, raw)[0] if start <= row['offset'] < stop]
            assert len(selected) == 2 and all(row['word'] == 0x4000 and not row['ancestor_0100_offsets'] for row in selected)
            first, last = selected
            assert first['offset'] == start and last['offset'] + last['native_extent'] == stop
            assert first['offset'] + first['native_extent'] == last['offset']
            commands.extend(selected)
            logical.extend(raw[start:stop])
        last = bank.blocks[EXCERPTS[-1][0]]
        end = 8 + unpack_from('<H', last, 4)[0]
        assert last[end - 4:end] == bytes(4)
        logical.extend(bytes(4))
        pack_into('<H', logical, 4, len(logical) - 8)
        body = bytes(logical) + bytes(-len(logical) % 4)
        rows, speeches = inventory(arm, body)
        assert len(speeches) == 10 and len(rows) == 21 and rows[-1]['word'] == 0
        assert [row['whole_command_hex'] for row in speeches] == [row['whole_command_hex'] for row in commands]
        bank.blocks[44] = body
        image.replace_file(stage.FILE, bank.to_bytes())
        path = ROOT / f'{side}_RESEARCH_ONLY.nds'
        image.save(path)
        image.replace_file(stage.FILE, archive)
        assert bytes(image.rom.save()) == source.read_bytes()
        fixtures[side] = dict(path=str(path), sha256=base.digest(path), excerpt_commands=commands)
    base.save(SETUP, dict(parent_sha256=proof['candidate_sha256'], candidate_sha256=base.digest(ROM),
        proof_sha256=base.digest(stage.PROOF), fixture_ROMs=fixtures, whole_parent_inverse_exact=True,
        unchanged_transition_planes=transition, excerpts=EXCERPTS,
        fixture_scope='Ten original speech commands at the initialized Rafael opening. Natural scene eligibility is outside this replay.'))


def capture(side):
    harness = previous.previous.prior.harness
    fixture = base.load(SETUP)['fixture_ROMs'][side]
    assert base.digest(fixture['path']) == fixture['sha256'] and not (ROOT / side).exists()
    old = sys.argv
    try:
        sys.argv = [old[0], '--rom', fixture['path'], '--out', str(ROOT / side), '--frames', str(FRAME_COUNT),
            '--inputs-json', str(INPUTS), '--capture-every', '999999', '--capture-at',
            *map(str, (2200, *range(2850, 7701, 25), 8500, 8700))]
        harness.main()
    finally:
        sys.argv = old


def verify():
    tools = previous.previous.prior
    setup, draft = map(base.load, (SETUP, stage.REVIEW))
    records = {row['id']: row for row in draft['records']}
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
            plane = setup['unchanged_transition_planes'].get(ident)
            if plane is None:
                page, = records[ident][side + '_native']['pages']
                plane = page['native_plane_hex']
            expected = tools.prior.masks(bytes.fromhex(plane))
            found = [(frame, photo) for frame, photo, mask in candidates if frame > last_frame and mask == expected]
            assert found, (side, ident, last_frame)
            last_frame, photo = found[0]
            shown[ident] = photo
            evidence[photo['path']] = base.digest(photo['path'])
        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in (2200, 8500, 8700)]
        observed[side] = shown
        evidence[str(report_path)] = base.digest(report_path)
    assert outside['before'] == outside['after']
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        observed=observed, outside_exact_frames=[2200, 8500, 8700], source_commands_preserved=True,
        initialized_excerpts_at_Rafael_entry=True, hardware=False, natural_event_eligibility_observed=False,
        verified_revised_pages=len(REVISED_IDS), verified_following_pages=len(FOLLOWING_IDS), evidence=evidence))
    print('Matched all five revised speeches and their original following replies.')


def startup():
    setup = base.load(SETUP)
    assert setup['candidate_sha256'] == base.digest(ROM)
    proof = ROOT / 'startup_input.json'
    base.save(proof, dict(research_ROM_sha256=setup['candidate_sha256'],
                          registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    boot = previous.previous.prior.prior.boot
    FunctionType(boot.startup_replay.main.__code__, vars(boot.startup_replay) | dict(
        EVIDENCE=proof, ROM=ROM, STARTUP=ROOT / 'own_startup',
        PRIOR=stage.parent.replay.ROOT / 'own_startup'))()
    FunctionType(boot.startup_check.verify_startup.__code__, vars(boot.startup_check) | dict(
        ROOT=ROOT, ROM=ROM, PROOF=proof, BIOGRAPHIES=stage.parent.replay.ROOT, BOOT=STARTUP))()


verify_storage = FunctionType(previous.verify_storage.__code__, vars(previous) | dict(
    stage=stage, SETUP=SETUP, ROM=ROM, PROOF=PROOF, __file__=__file__))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'startup', 'verify', 'verify_storage'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

