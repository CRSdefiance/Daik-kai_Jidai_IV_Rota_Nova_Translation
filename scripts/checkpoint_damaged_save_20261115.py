"""Verify the visible damaged-save prompt and the distinct legacy message."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont, REFERENCE_KANJI_FONT_SHA256
from dk4tool.patch.damaged_save_release import OFFSET, ENGLISH, formatted_suffix
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_damaged_save_20261115 as replay
from scripts.seal_shared_text_source_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots


base, current = replay.base, replay.current
ROOT = Path('work/damaged_save_20261115_v2')
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/damaged_save_observed_20261115_v1.json')
MESSAGE = 117
INK = (0, 8, 0)


def complete_mask(arm, kanji, text):
    first, second = text.split('\n')
    assert first.startswith('１:') and second.startswith('  ')
    codes = unpack_from('<3340H', arm, 0x125EC4)
    at = codes.index(0x8250) * 22
    cell = kanji[at:at + 22]
    number = {(16 + x, 296 + y) for x in range(11) for y in range(11)
              if cell[y * 2 + x // 8] & (0x80 >> (x % 8))}
    font = GameAsciiFont.from_arm9(arm)
    expected = set(number)
    for x, y, row in ((28, 297, first[1:]), (22, 313, second.lstrip())):
        for index, char in enumerate(row):
            glyph = font.decode(char)
            expected.update((x + index * 6 + dx, y + dy) for dx in range(6) for dy in range(11)
                            if glyph.getpixel((dx, dy)))
    assert len(number) == 11 and len(expected) == 489
    return expected


def build():
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    clean, candidate = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    clean_arm, arm = (rom.read_file(current.stage.ARM) for rom in (clean, candidate))
    active_common = candidate.read_file(current.stage.COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(active_common).hexdigest() == release['target_COMMON_sha256']
    kanji = candidate.read_file('/GRP/KANJI.FNT')
    assert sha256(kanji).hexdigest() == REFERENCE_KANJI_FONT_SHA256
    assert unpack_from('<I', clean_arm, 0xEE7D0)[0] == unpack_from('<I', arm, 0xEE7D0)[0] == replay.BASE + OFFSET
    clean_suffix = clean_arm[OFFSET:OFFSET + 52].split(b'\0', 1)[0]
    current_suffix = arm[OFFSET:OFFSET + 52].split(b'\0', 1)[0]
    assert current_suffix == formatted_suffix().encode('ascii')
    expected_body = b'\x82\x50' + current_suffix
    expected_mask = complete_mask(arm, kanji, expected_body.decode('cp932'))
    source = common_message_entries(clean.read_file(current.stage.COMMON), clean_arm)[MESSAGE]
    stored = owned_entries(active_common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())[MESSAGE]
    assert source.text.decode('cp932') == 'ゲームデータが\n壊れています。'

    fixture_path = ROOT / replay.FIXTURE.name
    fixture = base.load(fixture_path)
    assert base.digest(fixture['donor']) == fixture['donor_sha256']
    assert base.digest(fixture['disposable_copy']) == fixture['copy_sha256']
    donor, copy = (Path(fixture[key]).read_bytes() for key in ('donor', 'disposable_copy'))
    assert [i for i, (old, new) in enumerate(zip(donor, copy, strict=True)) if old != new] == [4]
    assert donor[4] ^ copy[4] == 1
    spans = fixture['source_exact_ARM9_ranges']
    assert all(clean_arm[lo:hi] == arm[lo:hi] for lo, hi in spans)

    folder = ROOT / 'corrupt_slot'
    receipt, requests, capture = (folder / p for p in ('terminal.json', 'requests.json', 'capture/capture_report.json'))
    terminal, trace, video = map(base.load, (receipt, requests, capture))
    assert video['ROM_sha256'] == terminal['ROM_sha256'] == release['candidate_sha256']
    assert all(base.digest(path) == digest for path, digest in terminal['evidence'].items())
    assert video['frames'] == terminal['completed_frames'] == 5150
    assert video['cold_boot'] and not video['savestate_loaded'] and not video['callback_errors']
    assert not any(value for key, value in video.items() if key.startswith('synthetic_'))
    assert video['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert video['battery_save_preloaded']['source_sha256'] == fixture['copy_sha256']
    assert trace['all_host_slots_restored_and_core_file_exact'] and not trace['errors'] and not trace['mismatches']
    assert not trace['source_requests'] and terminal['COMMON_requests'] == 0
    branch, modal = trace['rows']
    assert branch['frame'] == modal['frame'] and branch['slot'] == fixture['slot_index'] == 0
    assert branch['PC'] == replay.LOAD_BRANCH and modal['PC'] == replay.ERROR_MODAL
    assert branch['stored'] != branch['calculated']
    for key in ('stored', 'calculated'):
        assert branch[key] == fixture['native_checksum_results'][1][key]
    assert bytes.fromhex(modal['body_hex']) == expected_body

    frames = shots(video)
    samples = (2600, 3700, 3800, 4200, 4400, 4700)
    images = {frame: captured(frames[frame]) for frame in samples}
    for frame in (3700, 3800):
        found = {(x, y) for x in range(10, 246) for y in range(294, 355) if images[frame].getpixel((x, y)) == INK}
        assert found == expected_mask, frame
    assert ImageChops.difference(images[4200], images[4400]).getbbox() is None
    assert ImageChops.difference(images[2600], images[4200]).getbbox() == (0, 200, 256, 228)
    for frame, button in ((3601, 'A'), (4101, 'A'), (4501, 'B')):
        assert any(event['start'] == frame and event['buttons'] == [button]
                   for event in video['scripted_input_schedule'])

    lower = dict(id='COMMON_MESSAGE_117', message_ID=MESSAGE, file_path=current.stage.COMMON,
        source_reference=reference(source), current_reference=reference(stored), source_hex=source.text.hex(),
        current_hex=stored.text.hex(), source_Japanese=source.text.decode('cp932'),
        current_English=stored.text.decode('cp932'), english='The game data is corrupted.',
        speaker='System notice', context='The legacy notice names game data and reports corruption.',
        source_meaning='The game data is corrupted.', decision='draft revision',
        localization_note='Use a complete sentence. The legacy source gives no slot number or separate failed-load statement.',
        review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
        display_in_checksum_error=False, other_consumers_pending=True)
    evidence = {str(path): base.digest(path) for path in (current.RELEASE, fixture_path, receipt, requests, capture)}
    evidence.update({frames[n]['path']: frames[n]['PNG_sha256'] for n in samples})
    return dict(candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        visible_owner=dict(id='DAMAGED_SAVE_MESSAGE_SUFFIX', file_path=current.stage.ARM, source_offset=OFFSET,
            current_offset=OFFSET, native_pointer_field=0xEE7D0, allocation=52,
            source_Japanese=clean_suffix.decode('cp932'), source_hex=clean_suffix.hex(),
            source_meaning='The save data in the numbered slot is corrupted and could not be loaded.',
            english=ENGLISH, current_hex=current_suffix.hex(), decision='retention', speaker='System notice',
            context='After a confirmed Continue selection fails the original slot checksum.',
            localization_note='The original slot number and two full clauses give the cause and result. The wrap follows corrupted and leaves the second clause whole.',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=True)),
        legacy_record=lower, native_branch=branch, native_modal=modal, actual_COMMON_calls=trace['source_requests'],
        full_glyph_masks=[dict(frame=n, independent_ink_pixels=len(expected_mask)) for n in (3700, 3800)],
        original_slot_list_return_frames=[4200, 4400], title_return_frame=4700,
        actual_emulator_coverage='Original UI, load and dismissal with a disposable one-bit checksum fixture.',
        evidence=evidence, hardware=False, changed_release_bytes=False, new_dialogue_credit=0)


def main():
    document = build()
    if OUTPUT.exists():
        assert base.load(OUTPUT) == document
    else:
        base.save(OUTPUT, document)
    print('Verified two complete damaged-save glyph masks, exact checksum branch and return to the slot list.')


if __name__ == '__main__':
    main()
