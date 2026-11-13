"""Run the full ceramics exchange with the same initialized Lil entry on both builds."""

import argparse
from pathlib import Path
from struct import pack_into, unpack_from
import sys
from types import FunctionType

from PIL import ImageChops

from scripts import headless_desmume_v193 as harness
from scripts import replay_visible_gallery_captions_v1 as boot
from scripts import stage_lil_ceramics_wrap_20261111 as stage
from scripts.audit_lil_B221_English_paths_v7004 import body_masks, photos
from scripts.verify_release_baseline import files


base = stage.base
ROOT = Path('out/lil_ceramics_wrap_20261111_v2')
ROM = ROOT / 'lil_ceramics_wrap_RESEARCH_ONLY.nds'
SETUP, LIVE = ROOT / 'fixture_receipt.json', ROOT / 'ceramics_gameplay.json'
STARTUP = ROOT / 'own_startup_verification.json'
INPUTS = Path('work/analysis/movie_viewport_v303/lil_start_inputs.json')
HISTORICAL = next(Path('work/analysis/square_shopkeeper_actual_v7024b').glob('four_full_scenes*.json'))
VIEWED = '86a5273cb1bd42764ce2dc4904fb793876d7964196b3da7f389d226cbb9d7e2c'


def prepare():
    proof = base.load(stage.PROOF)
    assert not ROOT.exists() and stage.sha(stage.ARCHIVE.read_bytes()) == proof['target_archive_sha256']
    release = base.load(stage.parent.RELEASE)
    assert proof['candidate_sha256'] == release['candidate_sha256'] == base.digest(stage.parent.ROM)
    assert base.digest(stage.REVIEW) == proof['review_sha256']
    assert base.digest(INPUTS) == '097df0c69d30d00532373b2b8b7fe2f5969ba581a0bd35e27074c22749631541'
    previous = stage.base.NdsImage.open(stage.parent.ROM)
    bank = stage.IlnkContainer.parse(previous.read_file(stage.FILE))
    new = stage.IlnkContainer.parse(stage.ARCHIVE.read_bytes())
    assert [i for i, (a, b) in enumerate(zip(bank.blocks, new.blocks, strict=True)) if a != b] == [stage.BLOCK]
    prelude = bank.blocks[22][8:56]
    historical = next(row for row in base.load(HISTORICAL)['versions'] if row['case'] == 'static_target')
    old_fixture = next(row for row in base.load('work/analysis/square_shopkeeper_scenes_v7022/four_complete_static_staged_nameplate_fixtures.json')['fixtures']
                       if row['case'] == 'static_target')
    assert prelude.hex() == old_fixture['original_B22_prelude_hex']
    frames = [row['complete_page_holds'][0][-1]['frame'] for row in historical['panels']]
    assert len(frames) == 17 and frames[-1] == 6910
    ROOT.mkdir()
    target = stage.base.NdsImage.open(stage.parent.ROM)
    target.replace_file(stage.FILE, stage.ARCHIVE.read_bytes())
    target.save(ROM)
    before_files, after_files = files(previous), files(target)
    assert before_files.keys() == after_files.keys()
    assert [key for key, value in before_files.items() if after_files[key] != value] == [stage.FILE]
    target.replace_file(stage.FILE, previous.read_file(stage.FILE))
    assert bytes(target.rom.save()) == stage.parent.ROM.read_bytes()
    variants = {}
    inventory, _, _ = stage.scoped_inventory()
    arm = previous.read_file(stage.ARM)
    for side, block in [('before', bank.blocks[stage.BLOCK]), ('after', new.blocks[stage.BLOCK])]:
        end = 8 + unpack_from('<H', block, 4)[0]
        logical = bytearray(bank.blocks[22][:8] + prelude + block[8:end])
        pack_into('<H', logical, 4, len(logical)-8)
        fixture = bytes(logical) + bytes(-len(logical) % 4)
        commands, _ = inventory(arm, fixture)
        original, _ = inventory(arm, block)
        assert len(commands) == 29 and len(original) == 20
        assert all(a['word'] == b['word'] and a['whole_command_hex'] == b['whole_command_hex'] and
                   a['offset'] + len(prelude) == b['offset'] for a, b in zip(original, commands[9:], strict=True))
        image = stage.base.NdsImage.open(stage.parent.ROM)
        bank.blocks[22] = fixture
        image.replace_file(stage.FILE, bank.to_bytes())
        path = ROOT / f'{side}_Lil_entry_RESEARCH_ONLY.nds'
        image.save(path)
        bank.blocks[22] = stage.IlnkContainer.parse(previous.read_file(stage.FILE)).blocks[22]
        assert stage.IlnkContainer.parse(stage.base.NdsImage.open(path).read_file(stage.FILE)).blocks[22] == fixture
        variants[side] = dict(path=path.as_posix(), sha256=base.digest(path), fixture_sha256=stage.sha(fixture))
    schedule = base.load(INPUTS) + [dict(start=f, duration=5, buttons=['A']) for f in range(2600, 7600, 240)]
    base.save(ROOT / 'inputs.json', schedule)
    base.save(SETUP, dict(candidate_sha256=base.digest(ROM), parent_sha256=release['candidate_sha256'],
        source_proof_sha256=base.digest(stage.PROOF), fixture_ROMs=variants, representative_frames=frames,
        end=7600, same_original_prelude=True, full_20_original_commands=True, scope='Only the Lil entry block changes in the scene fixtures.'))


def capture(side):
    setup = base.load(SETUP)
    info = setup['fixture_ROMs'][side]
    assert base.digest(info['path']) == info['sha256']
    folder = ROOT / side
    assert not folder.exists()
    input_path = ROOT / 'inputs.json'
    frames = [2100, *setup['representative_frames'], 7030, 7270, 7520]
    prior = sys.argv
    try:
        sys.argv = [sys.argv[0], '--rom', info['path'], '--out', str(folder), '--frames', str(setup['end']),
                    '--inputs-json', str(input_path), '--capture-every', '999999', '--capture-at', *map(str, frames)]
        harness.main()
    finally:
        sys.argv = prior


def masks(plane):
    return [{(i%216,i//216) for i,v in enumerate(plane) if v == color} for color in (1, 15)]


def verify():
    setup, stored, draft = map(base.load, (SETUP, stage.PROOF, stage.REVIEW))
    assert setup['source_proof_sha256'] == base.digest(stage.PROOF)
    assert stored['review_sha256'] == base.digest(stage.REVIEW)
    viewed_sheet = base.digest(stored['sheet'])
    assert viewed_sheet == stored['sheet_sha256'] == VIEWED
    reports, captures = [], []
    for side in ('before', 'after'):
        path = ROOT / side / 'capture_report.json'
        report = base.load(path)
        assert report['ROM_sha256'] == setup['fixture_ROMs'][side]['sha256'] and report['frames'] == setup['end']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule'] == base.load(ROOT / 'inputs.json')
        reports.append(path)
        captures.append(photos(report))
    old, new = captures
    differences, exact = [], []
    for row, frame in zip(draft['records'], setup['representative_frames'], strict=True):
        before, a = old[frame]
        after, b = new[frame]
        diff = ImageChops.difference(a, b).getbbox()
        if row['id'] in draft['stored_changes']:
            assert diff and 16 <= diff[0] < diff[2] <= 232 and 296 <= diff[1] < diff[3] <= 360
            for key, image in (('before', a), ('after', b)):
                plane = bytes.fromhex(row[key + '_native']['plane_hex'])
                assert body_masks(image) == masks(plane), (row['id'], frame, key)
            differences.append(dict(id=row['id'], frame=frame, before=before, after=after, changed_bounds=diff,
                                    complete_native_page_matches_actual=True))
        else:
            assert not diff, (row['id'], frame)
            exact.append(dict(id=row['id'], frame=frame, before=before, after=after))
    assert len(differences) == 5 and len(exact) == 12
    identical = [frame for frame in (2100, 7030, 7270, 7520) if old[frame][0]['framebuffer_sha256'] == new[frame][0]['framebuffer_sha256']]
    assert identical == [2100, 7030, 7270, 7520]
    base.save(LIVE, dict(candidate_sha256=setup['candidate_sha256'], parent_sha256=setup['parent_sha256'],
        revised_pages=differences, unchanged_scene_frames=exact, identical_before_and_after_scene_frames=identical,
        complete_revised_native_masks_match_captures=True, differences_confined_to_original_body_rectangle=True,
        reviewed_offline_sheet_sha256=viewed_sheet, actual_scope='Paired cold boots through the whole Hamburg scene staged at Lil’s entry.',
        naturally_triggered_Hamburg_event=False, hardware=False, evidence={str(p): base.digest(p) for p in (SETUP, *reports)}))
    print('Five changed body planes, 12 unchanged panels and four before/after scene frames verified.')


def startup():
    setup = base.load(SETUP)
    assert setup['candidate_sha256'] == base.digest(ROM)
    proof = ROOT / 'startup_input.json'
    base.save(proof, dict(research_ROM_sha256=setup['candidate_sha256'],
                         registered_input=dict(candidate_sha256=setup['parent_sha256'])))
    FunctionType(boot.startup_replay.main.__code__, vars(boot.startup_replay) | dict(EVIDENCE=proof, ROM=ROM,
        STARTUP=ROOT / 'own_startup', PRIOR=boot.ROOT / 'own_startup'))()
    FunctionType(boot.startup_check.verify_startup.__code__, vars(boot.startup_check) | dict(ROOT=ROOT, ROM=ROM,
        PROOF=proof, BIOGRAPHIES=boot.ROOT, BOOT=STARTUP))()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('prepare', 'before', 'after', 'verify', 'startup'))
    action = parser.parse_args().action
    if action in ('before', 'after'):
        capture(action)
    else:
        globals()[action]()
