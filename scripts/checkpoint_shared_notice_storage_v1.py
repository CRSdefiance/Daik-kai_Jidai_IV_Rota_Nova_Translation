"""Archive the exact stored notices and their focused gameplay evidence."""

import gzip
import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import ROOT as DYNAMIC, font_tools, render
from scripts.review_literal_notice_callers_v1 import ARCHIVE, OUTPUT
from scripts.stage_shared_notices_storage_v1 import ARM, ROOT, STATIC
from scripts.verify_personal_gameplay_v841 import get_machine


BASE = 0x02000000
STARTUP = Path('out/shared_notice_research_startup_20261110_v2/capture/capture_report.json')
PRIOR = Path('work/ship_command_label_release_v1')
DEPARTURE = Path('out/shared_notice_departure_research_20261110_v2/capture/capture_report.json')
DISMISSAL = Path('out/shared_notice_departure_research_20261110_v1/capture/capture_report.json')
DEST = ARCHIVE / 'stored_notices_v1'


def checked_report(path, rom_sha, frames):
    report = load(path)
    assert report['ROM_sha256'] == rom_sha and report['frames'] == frames
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification']
    for shot in report['frames_captured']:
        assert digest(shot['path']) == shot['PNG_sha256']
    raw = Path(report['read_only_RAM_snapshot']['path'])
    assert digest(raw) == report['read_only_RAM_snapshot']['sha256'] and raw.stat().st_size == 0x400000
    return report, raw.read_bytes()


def startup_proof(arm, sha):
    report, raw = checked_report(STARTUP, sha, 31000)
    previous_path = PRIOR / 'own_startup_run_v1/capture/capture_report.json'
    previous = load(previous_path)
    frames = (1600, 2200, 3340, 4000, 16000, 31000)
    a = {shot['frame']: shot for shot in report['frames_captured']}
    b = {shot['frame']: shot for shot in previous['frames_captured']}
    assert all(a[n]['framebuffer_sha256'] == b[n]['framebuffer_sha256'] for n in frames)
    assert raw[DIRECTORY_OFFSET:TABLE_END] == arm[DIRECTORY_OFFSET:TABLE_END]
    cpu, get = get_machine(arm, raw)
    assert get(0x7F244) == 3
    prior_getters = PRIOR / 'own_registered_name_getters_v1.json'
    rows = load(prior_getters)['own_name_consumers']['rows']
    assert len(rows) == 24 and len({r['actor_ID'] for r in rows}) == 12
    names = []
    for row in rows:
        value = bytes.fromhex(row['text_hex'])
        obj = row['actor_object']
        pointer = get(row['getter'] - BASE, obj)
        assert bytes(cpu.mem_read(pointer, len(value) + 1)) == value + b'\0'
        names.append({key: row[key] for key in ('actor_ID', 'consumer', 'getter', 'text', 'text_hex')})
    return dict(frames=31000, exact_matching_Maria_frames=[a[n] for n in frames],
        relocated_catalogue_exact_in_own_startup_WRAM=True, original_protected_name_getters=names,
        existing_system_unlock_fixture=report['synthetic_gallery_fixtures'],
        evidence={str(p): digest(p) for p in (STARTUP, previous_path, prior_getters)})


def departure_proof(rom, arm, sha):
    report, raw = checked_report(DEPARTURE, sha, 4800)
    dismissal, _ = checked_report(DISMISSAL, sha, 5400)
    assert not any(report[key] or dismissal[key] for key in report if key.startswith('synthetic_'))
    assert report['battery_save_preloaded']['source_sha256'] == dismissal['battery_save_preloaded']['source_sha256']
    assert digest(report['battery_save_preloaded']['source']) == report['battery_save_preloaded']['source_sha256']
    raster, _, _ = font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    by_frame = {shot['frame']: shot for shot in report['frames_captured']}
    by_frame_dismissed = {shot['frame']: shot for shot in dismissal['frames_captured']}
    observed = []
    cases = (
        (85, 4000, 'Sailing days left: about ２８.'),
        (86, 4800, ' ５/２４\n  Sky: Sunny\n  Departed Copenhagen.'),
    )
    crop = (16, 296, 244, 344)
    for number, frame, expanded in cases:
        data = expanded.encode('cp932')
        plane, _ = render(raster, arm, kanji, data)
        shot = by_frame[frame]
        with Image.open(shot['path']) as im:
            actual = im.convert('RGB').crop(crop)
        assert bytes(color == (0, 8, 0) for color in actual.get_flattened_data()) == bytes(p == 1 for p in plane)
        observed.append(dict(message_ID=number, capture=shot, crop=crop, expanded_hex=data.hex(),
            complete_foreground_and_blank_margin_match=True, foreground_pixels=plane.count(1)))
    expansion = bytes.fromhex(observed[-1]['expanded_hex']) + b'\0'
    for address in struct.unpack_from('<2I', arm, 0x54890):
        at = address - BASE
        assert raw[at:at + len(expansion)] == expansion
    assert by_frame[4800]['framebuffer_sha256'] == by_frame_dismissed[4800]['framebuffer_sha256']
    assert dict(start=5001, duration=8, buttons=['A']) in dismissal['scripted_input_schedule']
    assert by_frame_dismissed[5300]['framebuffer_sha256'] != by_frame[4800]['framebuffer_sha256']
    return dict(observed=observed, dated_notice_exact_in_both_live_text_buffers=True,
        docked_depart_command=by_frame[3600], depart_submenu=by_frame[4400],
        A_dismissed_to_sailing=by_frame_dismissed[5300], donor_isolated=True,
        controller_only=True, no_scene_or_world_state_override=True,
        evidence={str(p): digest(p) for p in (DEPARTURE, DISMISSAL)})


def main():
    assert not DEST.exists()
    stored_path, dynamic_path = ROOT / 'stored_verification.json', DYNAMIC / 'native_preflight.json'
    stored, dynamic = load(stored_path), load(dynamic_path)
    rom = NdsImage.open(stored['target'])
    assert digest(stored['target']) == stored['target_sha256']
    arm = rom.read_file(ARM)
    boot = startup_proof(arm, stored['target_sha256'])
    live = departure_proof(rom, arm, stored['target_sha256'])
    visual = []
    for index, sheet in enumerate(dynamic['contact_sheets'], 1):
        path = Path(sheet['path'])
        assert digest(path) == sheet['sha256']
        if index != 1:
            assert digest(path.parent.with_name('dynamic_notice_layout_v2') / path.name) == sheet['sha256']
        visual.append(dict(**sheet, directly_viewed=True, exact_prior_sheet_reused=index != 1))
    assert sum(sheet['pages'] for sheet in visual) == 42
    source = {r['message_ID']: r for r in load(OUTPUT)['records']}
    amendments = {r['message_ID']: r for r in stored['final_editorial_amendments']}
    static = {r['message_ID']: r for r in load(STATIC / 'layout.json')['records']}
    rows = []
    for refs in stored['exact_record_references']:
        n = refs['message_ID']
        row = source[n]
        changed = amendments.get(n)
        decision = 'revision' if changed else row['decision']
        english = changed['revised_English'] if changed else (
            static[n]['logical_English'] if n in static else row['english'])
        rationale = changed['rationale'] if changed else row['localization_note']
        rows.append(dict(**refs, id=row['id'], file_path=row['file_path'], source_hex=row['source_hex'],
            previous_hex=row['current_hex'], source_Japanese=row['source_Japanese'], english=english,
            decision=decision, rationale=rationale, review=row['review'],
            layout_reason=static.get(n, {}).get('layout_reason') or row['manual_break_reason'],
            native_storage_and_display_checks_passed=True, observed_in_gameplay=n in (85, 86), new_credit=0))
    counts = dict(Counter(row['decision'] for row in rows))
    assert counts == {'revision': 11, 'retention': 19}
    DEST.mkdir()
    archives = {}
    for path in (stored_path, dynamic_path):
        raw = path.read_bytes()
        target = DEST / f'{path.name}.gz'
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        archives[target.name] = dict(original=str(path), original_sha256=digest(path), archive_sha256=digest(target))
    save(DEST / 'checkpoint.json', dict(research_ROM=stored['target'], research_ROM_sha256=stored['target_sha256'],
        counts=counts, records=rows, startup=boot, observed_gameplay=live, native_dynamic_visual_review=visual,
        exact_proof_archives=archives, pending_live_new_selector_and_pagination=True,
        research_only_and_zero_new_credit=True, full_goal_complete=False))
    print('Archived 30 decisions, 42 viewed dynamic pages, 24 protected getters and two live departure notices.')


if __name__ == '__main__':
    main()
