"""Bind the corrected map layout to actual gameplay, startup and reviewed pages."""

import argparse
from json import loads
from pathlib import Path
from types import FunctionType
from xml.etree import ElementTree

from PIL import Image, ImageChops

from scripts import probe_ancient_map_documents_v4 as original
from scripts import replay_arrival_month_labels_v1 as previous_replay
from scripts import stage_ancient_map_text_v2 as stage
from scripts import verify_setup_save_equipment_v1 as startup


base = stage.base
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BOOT = ROOT / 'own_startup_verification.json'
LIVE = ROOT / 'ancient_map_gameplay_verification.json'
NATIVE = ROOT / 'native_document_fields.json'
VISUAL = ROOT / 'ancient_map_visual_approval.json'
CHECKPOINT = ROOT / 'ready_to_register.json'
OUTPUT = ROOT / 'reviewed_ancient_map_source_inputs.json'
QA = Path('work/ancient_map_text_repo_qa_20261111.xml')
BIOGRAPHIES = previous_replay.STARTUP.parent
OBSERVED_IDS = (3649, 3626, 3646, 3607)
DOCUMENT_FRAME = 11100
BODY = (32, 224, 256, 352)
COLOR = (230, 230, 230)


def capture(folder, sha):
    terminal = folder / 'terminal.json'
    info = base.load(terminal)
    report_path, commands = Path(info['report']), Path(info['commands'])
    assert base.digest(report_path) == info['report_sha256'] and base.digest(commands) == info['commands_sha256']
    assert base.digest(info['original_donor_capture']) == info['original_donor_sha256']
    report = base.load(report_path)
    assert report['ROM_sha256'] == sha and report['frames'] == original.original.END
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    journal = report_path.with_name('navigation_command_journal.json')
    receipt = base.load(journal)
    received = receipt['commands_received']
    assert receipt['ROM_sha256'] == sha and receipt['last_command_frame'] == report['frames']
    assert receipt['commands_are_not_execution_receipts'] and received[-1]['command'] == {'stop': True}
    assert [row['command'] for row in received] == [loads(line) for line in commands.read_text(encoding='utf-8').splitlines()]
    assert all(row['validation_passed'] for row in received)
    fixture, = report['synthetic_condition_fixtures']
    assert fixture['frame'] == 9900 and not fixture['actual_earned_clues_or_save_progress']
    assert (fixture['document_pair_index'], fixture['lore_index'], fixture['clue_items']) == (18, 1, [198, 199, 200, 201])
    assert len(fixture['changes']) == 4 and all(row['before'] ^ row['after'] == 4 for row in fixture['changes'])
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    assert set(frames) == {9900, 10300, 10700, 11100, 11500, 11900}
    assert all(base.digest(row['path']) == row['PNG_sha256'] for row in frames.values())
    return fixture, frames, (terminal, report_path, commands, journal)


def check_gameplay():
    proof = base.load(PROOF)
    old, new = [capture(folder, sha) for folder, sha in (
        (original.ROOT, proof['registered_input']['candidate_sha256']),
        (ROOT / 'ancient_map', proof['research_ROM_sha256']),
    )]
    assert old[0] == new[0] and base.digest(old[2][2]) == base.digest(new[2][2])
    arm = base.NdsImage.open(ROM).read_file(stage.ARM)
    font = stage.GameAsciiFont.from_arm9(arm)
    rows = {row['message_ID']: row for row in proof['records']}
    before, after = [Image.open(run[1][DOCUMENT_FRAME]['path']).convert('RGB') for run in (old, new)]
    bounds = ImageChops.difference(before, after).getbbox()
    assert bounds and all(low <= actual for low, actual in zip(BODY[:2], bounds[:2]))
    assert all(high >= actual for high, actual in zip(BODY[2:], bounds[2:]))
    expected, y = set(), 225
    for n in OBSERVED_IDS:
        for line in rows[n]['visible_lines']:
            assert 32 + len(line) * 6 <= stage.prior.RIGHT and y + 11 <= BODY[3]
            for i, char in enumerate(line):
                mask = font.decode(char)
                expected.update((32 + i * 6 + gx, y + gy) for gy in range(11) for gx in range(6)
                                if mask.getpixel((gx, gy)))
            y += 12
        y += 12
    actual = {(x, y) for y in range(BODY[1], BODY[3]) for x in range(256) if after.getpixel((x, y)) == COLOR}
    assert expected == actual, (len(expected), len(actual), sorted(expected ^ actual)[:20])
    identical = [n for n in new[1] if n != DOCUMENT_FRAME]
    assert all(old[1][n]['framebuffer_sha256'] == new[1][n]['framebuffer_sha256'] for n in identical)
    evidence = (*old[2], *new[2], PROOF, NATIVE, Path(__file__),
                *(run[1][DOCUMENT_FRAME]['path'] for run in (old, new)))
    base.save(LIVE, dict(candidate_sha256=base.digest(ROM), observed_ids=OBSERVED_IDS,
        actual_emulator=True, hardware=False, fixture=old[0], exact_document_ink=len(expected),
        document_frame=new[1][DOCUMENT_FRAME], baseline_frame=old[1][DOCUMENT_FRAME], changed_pixels_bound=bounds,
        original_map_title_marker_buttons_and_returns_exact=True, exact_other_framebuffers=identical,
        fixture_scope='Original map and Hint actions using four temporary clue bits in a copied Syracuse save.',
        evidence={str(path): base.digest(path) for path in evidence}))
    print('Old Dagger live field masks and five unchanged navigation frames passed.')


def approve(viewed):
    proof, live, native, boot = map(base.load, (PROOF, LIVE, NATIVE, BOOT))
    assert proof['research_ROM_sha256'] == live['candidate_sha256'] == native['candidate_sha256'] == boot['candidate_sha256']
    assert len(native['all_masks_and_complete_ordered_glyph_positions_exact']) == 51
    assert len(proof['records']) == 61 and boot['cold_boot'] and len(boot['original_protected_name_getters']) == 24
    sheets = proof['map_sheets'] + proof['rumor_sheets']
    assert viewed == [row['sha256'] for row in sheets]
    assert all(base.digest(row['path']) == row['sha256'] for row in sheets)
    tests = list(ElementTree.parse(QA).iter('testsuite'))
    assert sum(int(t.get('tests', 0)) for t in tests) == 34
    assert not any(int(t.get(k, 0)) for t in tests for k in ('errors', 'failures', 'skipped'))
    map_draft, rumor_draft = map(base.load, (stage.prior.document.OUTPUT, stage.prior.rumor.OUTPUT))
    assert all(base.digest(path) == sha for path, sha in proof['manuscript_sha256'].items())
    base.save(OUTPUT, dict(records=map_draft['records'] + rumor_draft['records'],
        source_manuscript_sha256=proof['manuscript_sha256'],
        native_fields=map_draft['native_fields'], region_direction_pairs=map_draft['original_region_direction_pairs']))
    base.save(VISUAL, dict(viewed_sheets=sheets, map_previews=20, rumor_portraits=10,
        observed_document_frame=live['document_frame'], candidate_sha256=live['candidate_sha256'],
        layout_review='Whole words, common left margin, full glyphs, one blank row between four fields. '
                      'The last single words on two rumor pages remain in the native portrait wrap.'))
    base.save(CHECKPOINT, dict(candidate_sha256=live['candidate_sha256'], approved_for_registered_successor=True,
        live_messages=live['observed_ids'], stored_cases=61, viewed_pages=30,
        evidence={str(path): base.digest(path) for path in (PROOF, NATIVE, BOOT, LIVE, QA, OUTPUT, VISUAL, Path(__file__))}))
    print('All 30 page reviews and five individual review gates are ready for registration.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--approve', nargs=4, metavar='VIEWED_SHA256')
    parser.add_argument('--only', choices=('gameplay', 'startup'))
    args = parser.parse_args()
    if args.approve:
        approve(args.approve)
    elif args.only == 'gameplay':
        check_gameplay()
    elif args.only == 'startup':
        FunctionType(startup.verify_startup.__code__, vars(startup) | globals())()
    else:
        parser.error('Select an action')
