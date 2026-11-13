"""Verify the visual, startup and representative gameplay gates for both advice families."""

import argparse
from hashlib import sha256
from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import replay_weapon_armor_advice_v1 as replay
from scripts import verify_item_production_advice_v1 as offline
from scripts import verify_rumor_and_cooperation_v1 as portrait
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_plaque_release_v247 import find_mask


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
BIOGRAPHIES = replay.PRIOR.parent
BOOT = ROOT / 'own_startup_verification.json'
VISUAL = ROOT / 'visual_layout_approval.json'
LIVE = ROOT / 'weapon_armor_advice_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
QA = Path('work/weapon_armor_advice_repo_qa_20261111.xml')
OBSERVED = (3057, 3105)


def verify_startup():
    FunctionType(offline.verify_startup.__code__, vars(offline) | globals())()


def approve_layout(viewed):
    code = checked_text(getsource(offline.approve_layout), {
        "len(proof['native_display_cases']) == 48": "len(proof['native_display_cases']) == 100",
        "len(proof['native_original_copies']) == 24": "len(proof['native_original_copies']) == 50",
        "len(manuscript['native_context']['offline_native_selector_cases']) == 144":
            "len(manuscript['native_context']['offline_native_selector_cases']) == 300",
        "proof['sheets']) == 24": "proof['sheets']) == 50",
        'full_native_planes_directly_reviewed=24': 'full_native_planes_directly_reviewed=50',
        'original_offline_loader_copies=24': 'original_offline_loader_copies=50',
        'original_offline_portrait_cases=48': 'original_offline_portrait_cases=100',
        'original_offline_caller_fragments=144': 'original_offline_caller_fragments=300',
        'two or three body rows': 'one to four body rows',
        'Approved all 24 native layouts': 'Approved all 50 native layouts',
    })
    env = vars(offline) | globals()
    exec(compile(code, __file__ + '::reviewed-equipment-advice-pages', 'exec'), env)
    env['approve_layout'](viewed)


def verify_live():
    proof, visual, boot = map(stage.load, (PROOF, VISUAL, BOOT))
    sha = stage.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == visual['candidate_sha256'] == boot['candidate_sha256']
    assert not LIVE.exists() and not CHECKPOINT.exists()
    terminal_path = replay.ITEMS / 'terminal.json'
    terminal = stage.load(terminal_path)
    report_path = Path(terminal['report'])
    assert stage.digest(report_path) == terminal['report_sha256'] and terminal['candidate_sha256'] == sha
    report, _ = portrait.checked_report(report_path, sha, 11800)
    assert all(not value for key, value in report.items()
               if key.startswith('synthetic_') and key != 'synthetic_inventory_fixtures')
    donor = report['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot'] and terminal['unchanged_original_save']
    inventory, = report['synthetic_inventory_fixtures']
    assert [(row['item_id'], row['category'], row['name'], row['result_owner_kind']) for row in inventory['items']] == [
        (24, 2, 'Black Rapier', 0), (72, 3, 'Charles Martel Armor', 0),
    ]
    assert inventory['synthetic_advice_unlock']
    assert inventory['advice_flag_change'] == dict(address=replay.previous.FLAG_OWNER + 4, before=0, after=16)
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = stage.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == list(replay.COMMANDS)
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
    image = stage.NdsImage.open(ROM)
    arm = image.read_file(stage.ARM)
    font = portrait.GameAsciiFont.from_arm9(arm)
    raster, _, _ = portrait.font_tools(image)
    kanji = image.read_file('/GRP/KANJI.FNT')
    addresses = [unpack_from('<I', arm, offset)[0] - 0x02000000 for offset in (0x5444C, 0x54450)]
    observed = []
    for message, rows, before, during, after in ((3057, 1, 9600, 9900, 10200), (3105, 4, 10400, 10700, 11000)):
        snapshot = snapshots[during]
        assert snapshot['read_only_export'] and stage.digest(snapshot['path']) == snapshot['sha256']
        raw = Path(snapshot['path']).read_bytes()
        assert len(raw) == 0x400000
        plain, display = [raw[at:at + 256].split(b'\0', 1)[0] for at in addresses]
        native, = [row for row in proof['native_display_cases']
                   if (row['message_ID'], row['actor_ID']) == (message, 75)]
        assert plain == display == bytes.fromhex(native['display_hex'])
        assert len(native['visible_lines']) == rows
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, display)
        assert sha256(pixels).hexdigest() == native['native_ink_sha256']
        assert bytes(pixel == 1 for pixel in pixels) == portrait.portrait_ink(frames[during]['path'], portrait.PAPER)
        header, bounds = portrait.complete_mask(font, 'Hans Letzel', portrait.captured(frames[during]),
                                                16, 277, (98, 97, 98))
        prior, returned = (portrait.captured(frames[n]) for n in (before, after))
        assert prior.tobytes() == returned.tobytes()
        footer = find_mask(font, 'Advice', returned, (152, 365, 209, 384))
        observed.append(dict(message_ID=message, body_rows=native['visible_lines'], glyph_count=len(glyphs),
            header=dict(text='Hans Letzel', ink_pixels=header, bounds=bounds), item_footer=footer,
            capture_frames=[frames[n] for n in (before, during, after)], captured_RAM=snapshot))
    town = [frames[n] for n in (8400, 11800)]
    assert portrait.captured(town[0]).tobytes() == portrait.captured(town[1]).tobytes()
    evidence = (PROOF, VISUAL, BOOT, terminal_path, report_path, journal_path)
    stage.save(LIVE, dict(candidate_sha256=sha, observed_ids=list(OBSERVED), observed=observed,
        original_Advice_button=True, complete_dialogue_ink_and_blank_cells_exact=True,
        original_item_view_restored=True, original_town_return=True, town_frames=town,
        inventory_fixture=inventory, natural_advice_unlock=False, hardware=False,
        evidence={str(path): stage.digest(path) for path in evidence}))
    stage.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=list(OBSERVED), stored_cases=50, viewed_pages=50,
        evidence={str(path): stage.digest(path) for path in (*evidence, LIVE, QA, Path(__file__))}))
    print('Verified the one-row weapon and four-row armor Advice portraits and exact Items/Lisbon returns.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('layout', 'startup', 'live'))
    parser.add_argument('--viewed-sheets', nargs='+')
    args = parser.parse_args()
    if args.action == 'layout':
        approve_layout(args.viewed_sheets)
    else:
        (verify_startup if args.action == 'startup' else verify_live)()
