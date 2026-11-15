"""Bind the observed Lisbon Baby Shark advice and return to the staged text."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from scripts import replay_item_production_advice_v1 as replay
from scripts import replay_item_production_advice_v2 as fixture
from scripts import verify_item_production_advice_v1 as verified
from scripts import verify_rumor_and_cooperation_v1 as portrait
from scripts.verify_plaque_release_v247 import find_mask


stage = replay.stage
ROOT, ROM, PROOF = stage.ROOT, stage.ROM, stage.PROOF
LIVE = ROOT / 'item_advice_gameplay_verification.json'
CHECKPOINT = ROOT / 'approved_checkpoint.json'
MESSAGE = 3037


def main():
    proof, visual, boot = map(stage.load, (PROOF, verified.VISUAL, verified.BOOT))
    sha = stage.digest(ROM)
    assert sha == proof['research_ROM_sha256'] == visual['candidate_sha256'] == boot['candidate_sha256']
    assert not LIVE.exists() and not CHECKPOINT.exists()
    terminal_path = fixture.ITEMS / 'terminal.json'
    terminal = stage.load(terminal_path)
    report_path = Path(terminal['report'])
    assert stage.digest(report_path) == terminal['report_sha256'] and terminal['candidate_sha256'] == sha
    report, _ = portrait.checked_report(report_path, sha, 11000)
    assert all(not value for key, value in report.items()
               if key.startswith('synthetic_') and key != 'synthetic_inventory_fixtures')
    donor = report['battery_save_preloaded']
    assert stage.digest(donor['source']) == donor['source_sha256'] == terminal['donor_sha256']
    assert donor['copied_byte_exact_before_cold_boot'] and terminal['unchanged_original_save']
    inventory, = report['synthetic_inventory_fixtures']
    item, = inventory['items']
    assert (item['item_id'], item['category'], item['name'], item['result_owner_kind']) == (4, 0, 'Baby Shark', 0)
    assert inventory['synthetic_advice_unlock'] and inventory['native_local_product_acquisition_flag']['bit'] == 29
    assert inventory['advice_flag_change'] == dict(address=replay.FLAG_OWNER + 4, before=0, after=16)
    journal_path = report_path.with_name('navigation_command_journal.json')
    journal = stage.load(journal_path)['commands_received']
    assert all(row['validation_passed'] for row in journal)
    assert [row['command'] for row in journal] == list(replay.COMMANDS)
    frames = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('_navigation.png')}
    snapshots = {row['frame']: row for row in report['read_only_capture_RAM_snapshots']}
    snapshot = snapshots[9900]
    assert snapshot['read_only_export'] and stage.digest(snapshot['path']) == snapshot['sha256']
    raw = Path(snapshot['path']).read_bytes()
    assert len(raw) == 0x400000
    image = stage.NdsImage.open(ROM)
    arm = image.read_file(stage.ARM)
    font = portrait.GameAsciiFont.from_arm9(arm)
    raster, _, _ = portrait.font_tools(image)
    addresses = [unpack_from('<I', arm, offset)[0] - 0x02000000 for offset in (0x5444C, 0x54450)]
    plain, display = [raw[at:at + 256].split(b'\0', 1)[0] for at in addresses]
    native, = [row for row in proof['native_display_cases']
               if (row['message_ID'], row['actor_ID']) == (MESSAGE, 75)]
    assert plain == display == bytes.fromhex(native['display_hex'])
    pixels, glyphs = portrait.render_portrait(raster, arm, image.read_file('/GRP/KANJI.FNT'), display)
    assert sha256(pixels).hexdigest() == native['native_ink_sha256']
    assert bytes(pixel == 1 for pixel in pixels) == portrait.portrait_ink(frames[9900]['path'], portrait.PAPER)
    header, bounds = portrait.complete_mask(font, 'Hans Letzel', portrait.captured(frames[9900]), 16, 277, (98, 97, 98))
    before, after = (portrait.captured(frames[n]) for n in (9600, 10200))
    assert before.tobytes() == after.tobytes()
    footer = find_mask(font, 'Advice', after, (152, 365, 209, 384))
    before_town, after_town = (portrait.captured(frames[n]) for n in (8400, 11000))
    assert before_town.tobytes() == after_town.tobytes()
    evidence = (PROOF, verified.VISUAL, verified.BOOT, terminal_path, report_path, journal_path)
    receipt = dict(candidate_sha256=sha, observed_ids=[MESSAGE], original_Advice_button=True,
        complete_dialogue_ink_and_blank_cells_exact=True, body_rows=native['visible_lines'], glyph_count=len(glyphs),
        header=dict(text='Hans Letzel', ink_pixels=header, bounds=bounds),
        original_item_view_restored=True, item_footer=footer, original_town_return=True,
        capture_frames={n: frames[n] for n in (8400, 9600, 9900, 10200, 11000)}, captured_RAM=snapshot,
        inventory_fixture=inventory, natural_advice_unlock=False, hardware=False,
        evidence={str(p): stage.digest(p) for p in evidence})
    stage.save(LIVE, receipt)
    checked = (*evidence, LIVE, verified.QA, Path(__file__))
    stage.save(CHECKPOINT, dict(candidate_sha256=sha, approved_for_registered_successor=True,
        live_messages=[MESSAGE], stored_cases=24, viewed_pages=24,
        evidence={str(p): stage.digest(p) for p in checked}))
    print('Verified Hans’s complete Baby Shark advice, exact Items return and Lisbon return.')


if __name__ == '__main__':
    main()
