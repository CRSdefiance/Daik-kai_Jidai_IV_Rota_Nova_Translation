"""Verify the original 126 notice, live ITCM, growth and ordinary dismissal."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image

from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS as MARKET_FIELDS, NEW_FORMAT
from dk4tool.patch.shared_notice_wrap_v1 import HOOK, SELECTOR
from dk4tool.patch.ship_command_label_v1 import FIELD as SHIP_FIELD, NEW_POINTER
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_shared_notice_storage_v1 import checked_report
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.run_shared_notice_boom_v1 import ARM, BASE, RESEARCH, fixture, inspect_town


CAPTURE = Path('out/shared_notice_boom_20261110_v1')
TARGET = RESEARCH.with_name('live_boom_verification.json')


def main():
    assert not TARGET.exists()
    research = load(RESEARCH)
    terminal_path, journal = CAPTURE / 'terminal.json', CAPTURE / 'navigation.jsonl'
    terminal = load(terminal_path)
    report_path = Path(terminal['report'])
    assert terminal['exit_code'] == 0 and terminal['donor_unchanged']
    assert digest(journal) == terminal['navigation_sha256'] and digest(report_path) == terminal['report_sha256']
    report, _ = checked_report(report_path, research['target_sha256'], 9300)
    assert digest(research['target']) == report['ROM_sha256']
    donor = report['battery_save_preloaded']
    assert digest(donor['source']) == donor['source_sha256'] and donor['copied_byte_exact_before_cold_boot']
    assert Path(donor['source']) != Path(donor['destination'])
    key = 'synthetic_battle_recovery_proximity_fixtures'
    assert not any(report[k] for k in report if k.startswith('synthetic_') and k != key)
    applied, = report[key]
    assert applied['frame'] == 5300
    game = NdsImage.open(research['target'])
    arm = game.read_file(ARM)
    snapshots = {row['frame']: row for row in report['read_only_pause_RAM_snapshots']}
    raw, town_states = {}, {}
    for frame in (5300, 7500, 9000, 9300):
        row = snapshots[frame]
        assert row['read_only_export'] and digest(row['path']) == row['sha256']
        raw[frame] = Path(row['path']).read_bytes()
        _, get, town = inspect_town(arm, raw[frame])
        town_states[frame] = (get(0xB3FC8, town, 0), get(0xB3FD4, town, 0), get(0xB2E04, town))
    _, expected_fixture = fixture(arm, raw[5300], applied['action'])
    assert applied == dict(**expected_fixture, frame=5300)
    assert town_states == {5300: (0, 3400, 12), 7500: (400000, 3400, 12),
        9000: (0, 6943, 3), 9300: (0, 6943, 3)}

    fmt, output = struct.unpack_from('<2I', arm, 0x54890)
    def buffer(frame, address):
        at = address - BASE
        return raw[frame][at:at + 256].split(b'\0')[0]
    expanded = b'Substantial commercial investment has brought an economic boom to Copenhagen.'
    wrapped = b'Substantial commercial investment\n  has brought an economic boom to\n  Copenhagen.'
    assert buffer(9000, fmt) == expanded and buffer(9000, output) == wrapped
    assert b' '.join(wrapped.split()) == expanded and len(expanded) > 36
    raster, _, _ = font_tools(game)
    kanji = game.read_file('/GRP/KANJI.FNT')
    plane, glyphs = render(raster, arm, kanji, wrapped)
    captures = {row['frame']: row for row in report['frames_captured'] if row['path'].endswith('navigation.png')}
    assert set(captures) == set(snapshots)
    crop = (16, 296, 244, 344)
    with Image.open(captures[9000]['path']) as shot:
        view = shot.convert('RGB').crop(crop)
    assert bytes(pixel == (0, 8, 0) for pixel in view.get_flattened_data()) == bytes(p == 1 for p in plane)
    assert captures[9300]['framebuffer_sha256'] != captures[9000]['framebuffer_sha256']
    commands = load(CAPTURE / 'capture/navigation_command_journal.json')['commands_received']
    assert [row['frame'] for row in commands] == [5300, 7500, 9000, 9300]
    assert commands[1]['command']['buttons'] == ['B'] and commands[2]['command']['buttons'] == ['A']
    assert all(row['validation_passed'] for row in commands)

    live = report['read_only_native_state']
    assert live['read_only_export'] and not live['state_loaded'] and live['main_RAM_unchanged_by_export']
    assert digest(live['path']) == live['sha256']
    itcm_record = live['regions']['ITCM']
    assert digest(itcm_record['path']) == itcm_record['sha256']
    itcm = Path(itcm_record['path']).read_bytes()
    patch, tail = MainCodeFile(arm, BASE).sections[-2:]
    assert (patch.ramAddress, tail.ramAddress) == (0x01FFC000, 0x01FFD000)
    patch_at = patch.ramAddress & 0x7FFF
    loaded = itcm[patch_at:patch_at + len(patch.data)]
    # The inherited font footer helper caches a heap pointer in this word.
    cache = 0x2D8
    pointer, = struct.unpack_from('<I', loaded, cache)
    assert BASE <= pointer < BASE + len(raw[9000])
    assert loaded[:cache] == patch.data[:cache] and loaded[cache + 4:] == patch.data[cache + 4:]
    assert itcm[tail.ramAddress & 0x7FFF:(tail.ramAddress & 0x7FFF) + len(tail.data)] == tail.data
    assert HOOK >= patch.ramAddress and SELECTOR == tail.ramAddress + 32
    preserved_pointers = [(field, NEW_FORMAT) for field in MARKET_FIELDS] + [(SHIP_FIELD, NEW_POINTER)]
    for at, expected in preserved_pointers:
        assert struct.unpack_from('<I', raw[9000], at)[0] == expected
    save(TARGET, dict(candidate_sha256=research['target_sha256'], message_ID=126, native_caller_return=0x020B3E08,
        original_city_update_consumed_fixture=True, fixture=applied, town_states=town_states,
        expanded_hex=expanded.hex(), wrapped_hex=wrapped.hex(), three_complete_rows_and_blank_margins_exact=True,
        live_rendered_glyph_count=len(glyphs), complete_foreground_pixels=plane.count(1), crop=crop,
        live_ITCM_selector_and_both_prior_literals_exact=True, prior_Market_and_ship_pointers_exact=True,
        original_font_footer_heap_cache_pointer=pointer,
        B_dismissed_dock_prompt_and_A_dismissed_notice_to_normal_sailing=True, captures=captures,
        original_emulator_play=True, earned_investment=False, hardware=False,
        evidence={str(p): digest(p) for p in (RESEARCH, report_path, terminal_path, journal, Path(__file__))}))
    print('The original 126 notice renders three complete rows, dismisses to sailing and uses the exact live ITCM selector.')


if __name__ == '__main__':
    main()
