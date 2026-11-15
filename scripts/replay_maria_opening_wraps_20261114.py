"""Verify selected revised exchanges at Maria's initialized New Game entry."""

import argparse
import sys
from pathlib import Path
from struct import pack_into
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import refine_maria_opening_wraps_20261114 as stage
from scripts import replay_lil_final_wraps_20261114 as precedent
from scripts.maria_existing_unlock_contract_v7680 import HISTORICAL, validate_capture, validate_fixture


base = stage.base
ROOT = Path('out/maria_opening_wraps_20261114_v1')
ROM = ROOT / 'maria_opening_wraps_RESEARCH_ONLY.nds'
SETUP = ROOT / 'fixture_receipt.json'
LIVE = ROOT / 'maria_opening_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = ROOT / 'inputs.json'
PROOF = stage.ROOT / 'command_and_catalog_proof.json'
FRAME_COUNT = 10201
RETURN_FRAMES = (3900, 8850, 9050)
PLAY_ORDER = (
    'DK4_MES_B5_R0005', 'DK4_MES_B5_R0008',
    'DK4_MES_B19_R0036', 'DK4_MES_B19_R0040', 'DK4_MES_B19_R0044',
    'DK4_MES_B48_R0083', 'DK4_MES_B48_R0088',
)
REVISED_IDS = (PLAY_ORDER[0], PLAY_ORDER[2], PLAY_ORDER[5])
FOLLOWING_IDS = tuple(ident for ident in PLAY_ORDER if ident not in REVISED_IDS)


def prepare():
    assert not ROOT.exists()
    draft, proof, cold = map(base.load, (stage.REVIEW, stage.PROOF, stage.CAPTURE))
    parent = stage.parent.ROM
    assert base.digest(parent) == proof['candidate_sha256'] == draft['candidate_sha256']
    assert base.digest(stage.REVIEW) == proof['review_sha256']
    original, target, clean = map(base.NdsImage.open, (parent, parent, stage.CLEAN))
    before_archive = original.read_file(stage.FILE)
    for path, raw in stage.prior.transform(original, draft['records']):
        assert path == stage.FILE and raw == Path(proof['archives'][path]['path']).read_bytes()
        target.replace_file(path, raw)
    ROOT.mkdir()
    target.save(ROM)
    target.replace_file(stage.FILE, before_archive)
    assert bytes(target.rom.save()) == parent.read_bytes()

    inventory, _, _ = stage.prior.scoped_inventory()
    arm = original.read_file(stage.ARM)
    clean_arm = clean.read_file(stage.ARM)
    clean_host = stage.IlnkContainer.parse(clean.read_file(stage.FILE)).blocks[33]
    clean_commands, clean_texts = inventory(clean_arm, clean_host)
    clean_end = clean_texts[-1]['offset'] + clean_texts[-1]['native_extent']
    host_tail = [command['whole_command_hex'] for command in clean_commands if command['offset'] >= clean_end]
    assert host_tail[0] == '4062' and host_tail[-1] == '00000000'

    rows = {}
    for group in draft['complete_exchange_references']:
        block = group['block']
        if not any(f'_B{block}_' in ident for ident in PLAY_ORDER):
            continue
        assert not group['existing_extra_FE_commands']
        for japanese, current in zip(group['source_progressive_exchange'], group['current_progressive_exchange'], strict=True):
            ident = f"DK4_MES_B{block}_R{japanese['record_index']:04d}"
            if ident in PLAY_ORDER:
                rows[ident] = block, current['offset'] - 5
    assert rows.keys() == set(PLAY_ORDER)
    _, painter = stage.prior.precedent.planners(arm)
    font = original.read_file('/GRP/KANJI.FNT')
    record_ids = {row['id'] for row in draft['records']}
    assert set(REVISED_IDS) == record_ids.intersection(PLAY_ORDER)

    fixtures, neighbor_planes = {}, {}
    for side, source in (('before', parent), ('after', ROM)):
        image = base.NdsImage.open(source)
        archive = image.read_file(stage.FILE)
        bank = stage.IlnkContainer.parse(archive)
        host = bank.blocks[33]
        host_commands, host_texts = inventory(arm, host)
        end = host_texts[-1]['offset'] + host_texts[-1]['native_extent']
        assert host[:4] == clean_host[:4] and host[6:34] == clean_host[6:34]
        assert len([row for row in host_commands if row['offset'] < 34]) == 7
        assert [row['whole_command_hex'] for row in host_commands if row['offset'] >= end] == host_tail
        logical = bytearray(host[:34])
        excerpts = []
        for ident in PLAY_ORDER:
            block, offset = rows[ident]
            commands, _ = inventory(arm, bank.blocks[block])
            row = next(row for row in commands if row['offset'] == offset)
            assert row['word'] == 0x4000 and not row['ancestor_0100_offsets']
            command = bytes.fromhex(row['whole_command_hex'])
            assert command == bank.blocks[block][offset:offset + row['native_extent']]
            logical.extend(command)
            excerpts.append(dict(id=ident, block=block, offset=offset, command=row['whole_command_hex']))
            if ident in FOLLOWING_IDS:
                body = command[6:command.index(0, 6)]
                assert not stage.initial_names.bare_tokens(body)
                page, = painter(arm, font, body)['pages']
                glyphs = page['native_plane_hex']
                assert side == 'before' or neighbor_planes[ident] == glyphs
                neighbor_planes[ident] = glyphs
        logical.extend(b''.join(bytes.fromhex(row) for row in host_tail))
        pack_into('<H', logical, 4, len(logical) - 8)
        replacement = bytes(logical) + bytes(-len(logical) % 4)
        assert len(replacement) <= 0x2400
        commands, speeches = inventory(arm, replacement)
        assert [row['whole_command_hex'] for row in speeches] == [row['command'] for row in excerpts]
        assert [row['whole_command_hex'] for row in commands[-len(host_tail):]] == host_tail
        bank.blocks[33] = replacement
        image.replace_file(stage.FILE, bank.to_bytes())
        path = ROOT / f'{side}_RESEARCH_ONLY.nds'
        image.save(path)
        image.replace_file(stage.FILE, archive)
        assert bytes(image.rom.save()) == source.read_bytes()
        unlock_path = ROOT / f'{side}_unlock_manifest.json'
        unlock = base.load(HISTORICAL)
        digest = base.digest(path)
        unlock.update(production_ROM=str(path), production_ROM_sha256=digest,
                      current_test_scope='Maria dialogue replay with an existing system-only unlock.')
        base.save(unlock_path, unlock)
        validate_fixture(unlock_path)
        fixtures[side] = dict(path=str(path), sha256=digest, excerpt_commands=excerpts,
                              unlock=str(unlock_path), unlock_sha256=base.digest(unlock_path))

    schedule = cold['scripted_input_schedule'] + [
        dict(start=frame, duration=16, buttons=['A']) for frame in range(4200, 8701, 325)]
    base.save(INPUTS, schedule)
    base.save(SETUP, dict(parent_sha256=proof['candidate_sha256'], candidate_sha256=base.digest(ROM),
        proof_sha256=base.digest(stage.PROOF), fixture_ROMs=fixtures, whole_parent_inverse_exact=True,
        unchanged_transition_planes=neighbor_planes, host_block=33, original_host_exit=host_tail,
        original_initializer_count=7, source_commands_preserved=True, earned_unlock_verified=False))


def capture(side):
    fixture = base.load(SETUP)['fixture_ROMs'][side]
    assert base.digest(fixture['path']) == fixture['sha256']
    assert base.digest(fixture['unlock']) == fixture['unlock_sha256']
    unlock = validate_fixture(fixture['unlock'])
    assert not (ROOT / side).exists()
    old = sys.argv
    try:
        sys.argv = [old[0], '--rom', fixture['path'], '--out', str(ROOT / side),
            '--frames', str(FRAME_COUNT), '--inputs-json', str(INPUTS),
            '--battery-save', unlock['fixture_save'], '--allow-gallery-fixtures',
            '--gallery-save-fixture-manifest', fixture['unlock'], '--touchscreen',
            '--capture-every', '999999', '--capture-at',
            *map(str, sorted(set(RETURN_FRAMES) | set(range(4350, 8251, 25))))]
        harness.main()
    finally:
        sys.argv = old


def verify():
    tools = precedent.verify.__globals__['previous'].previous.prior
    setup, draft = map(base.load, (SETUP, stage.REVIEW))
    records = {row['id']: row for row in draft['records']}
    observed, outside = {}, {}
    evidence = {str(SETUP): base.digest(SETUP), str(INPUTS): base.digest(INPUTS)}
    for side in ('before', 'after'):
        report_path = ROOT / side / 'capture_report.json'
        report = base.load(report_path)
        validate_capture(report)
        assert report['ROM_sha256'] == setup['fixture_ROMs'][side]['sha256']
        assert report['frames'] == FRAME_COUNT and report['scripted_input_schedule'] == base.load(INPUTS)
        photos = tools.photos(report)
        candidates = [(frame, receipt, tools.body_masks(image))
                      for frame, (receipt, image) in sorted(photos.items()) if 4350 <= frame <= 8250]
        shown, cursor = {}, 4350
        for ident in PLAY_ORDER:
            if ident in FOLLOWING_IDS:
                plane = setup['unchanged_transition_planes'][ident]
            else:
                page, = records[ident][side + '_native']['pages']
                plane = page['native_plane_hex']
            expected = tools.prior.masks(bytes.fromhex(plane))
            matches = [(frame, receipt) for frame, receipt, masks in candidates if frame > cursor and masks == expected]
            assert matches, (side, ident, cursor)
            cursor, receipt = matches[0]
            shown[ident] = receipt
            evidence[receipt['path']] = base.digest(receipt['path'])
        assert cursor < RETURN_FRAMES[1]
        observed[side] = shown
        outside[side] = [photos[frame][0]['framebuffer_sha256'] for frame in RETURN_FRAMES]
        for frame in RETURN_FRAMES:
            receipt = photos[frame][0]
            evidence[receipt['path']] = base.digest(receipt['path'])
        evidence[str(report_path)] = base.digest(report_path)
    assert outside['before'] == outside['after'], outside
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        observed=observed, outside_exact_frames=list(RETURN_FRAMES), source_commands_preserved=True,
        initialized_excerpts_at_Maria_entry=True, hardware=False, natural_event_eligibility_observed=False,
        earned_unlock_verified=False, verified_revised_pages=len(REVISED_IDS),
        verified_following_pages=len(FOLLOWING_IDS), evidence=evidence))


verify_storage = FunctionType(precedent.verify_storage.__code__, precedent.verify_storage.__globals__ | globals())
startup = FunctionType(precedent.startup.__code__, precedent.startup.__globals__ | globals())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'verify', 'verify_storage', 'startup'))
    action = parser.parse_args().action
    capture(action) if action in ('before', 'after') else globals()[action]()

