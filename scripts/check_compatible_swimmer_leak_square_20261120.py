"""Bind earlier successful encounter paths to the current native display evidence."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import check_swimmer_leak_square_dialogue_20261120 as captures
from scripts import replay_compatible_swimmer_leak_square_20261120 as replay
from scripts import stage_madeira_resupply_numerals_20261120 as price
from scripts import stage_swimmer_leak_square_dialogue_20261120 as stage
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


ROOT = replay.ROOT
CAPTURE = Path('E:/Rota Nova translations/Generated/work/swimmer_leak_compatible_playback_20261120_v1/leak/capture_report.json')
PROOF, SHEET = ROOT / 'compatible_gameplay.json', ROOT / 'sea_gameplay.png'
SQUARE = stage.ROOT / 'square_gameplay.json'
STORED = stage.ROOT / 'staging.json'


def published_release(path):
    doc = stage.load(path)
    assert replay.digest(doc['candidate']) == doc['candidate_sha256']
    return doc, stage.NdsImage.open(doc['candidate'])


def hold(target, painter, row, item):
    pane = Image.open(item['path']).convert('RGB')
    assert replay.digest(item['path']) == item['PNG_sha256']
    case, = row['native_displays']
    pixels, events = stage.render_portrait(painter, target.read_file(stage.ARM), target.read_file(replay.FONT),
                                          bytes.fromhex(case['display_hex']))
    assert stage.digest(pixels) == case['complete_ink_sha256'] and len(events) == case['glyph_count']
    ink = native_hold(pane, pixels)
    return pane, dict(message_ID=row['message_ID'], visible_lines=case['visible_lines'], exact_ink_pixels=ink, screenshot=item)


def verify_mermaid(rom, painter, rows):
    latest, earlier = published_release(replay.MERMAID_RELEASE)
    checked = stage.load(replay.MERMAID_HISTORY)['observed_gameplay']
    assert checked['candidate_sha256'] == latest['candidate_sha256'] and checked['original_sequences_initialized']
    observed, = [row for row in checked['outcomes'] if row['event'] == 'mermaid']
    assert observed['selector_restored']
    assert [row['message_ID'] for row in observed['observed']] == [448, 449]
    original = replay.entries(earlier)
    target = replay.entries(rom)
    seen, panes = [], []
    for item in observed['observed']:
        n = item['message_ID']
        assert original[n].text == target[n].text and original[n].text.hex() == rows[n]['staged_hex']
        assert item['original_display_hex'] == rows[n]['native_displays'][0]['display_hex']
        pane, bound = hold(rom, painter, rows[n], item['capture'])
        seen.append(bound)
        panes.append((f'Mermaid / COMMON {n}', pane))
    after = observed['following_port_sighting']
    assert replay.digest(after['path']) == after['PNG_sha256']
    panes.append(('Mermaid / Next port sighting', Image.open(after['path']).convert('RGB')))
    return dict(earlier_ROM_sha256=latest['candidate_sha256'], earlier_proof=str(replay.MERMAID_HISTORY),
                earlier_proof_sha256=replay.digest(replay.MERMAID_HISTORY),
                matched_spans=replay.compatible_arm(earlier, rom), observed=seen, following_port=after,
                inherited_representative_gameplay=True), panes


def verify_leak(rom, painter, rows):
    fixture = stage.load(replay.PROOF)
    assert replay.digest(replay.ROM) == fixture['fixture_sha256']
    assert replay.digest(price.ROM) == fixture['target_ROM_sha256']
    report = stage.load(CAPTURE)
    assert report['ROM_sha256'] == fixture['fixture_sha256'] and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 9827 and not report['hardware_device_verification']
    assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_condition_fixtures'}
    restored = report['synthetic_condition_fixtures']
    assert [row['mode'] for row in restored] == ['select-leak', 'restore-leak-selection']
    assert [row['frame'] for row in restored] == [8327, 9627]
    earlier = stage.load(replay.LEAK_HISTORY)['flagship_leak']
    held, = earlier['observed']
    donor = report['battery_save_preloaded']
    previous_capture = Path(held['capture']['path']).parent / 'capture_report.json'
    previous = stage.load(previous_capture)
    for key in ('scripted_input_schedule', 'core_options', 'synthetic_condition_fixtures'):
        assert previous[key] == report[key]
    assert donor['copied_byte_exact_before_cold_boot'] and replay.digest(donor['source']) == donor['source_sha256']
    assert donor['source_sha256'] == previous['battery_save_preloaded']['source_sha256']
    target_arm = rom.read_file(stage.ARM)
    plain, display = [unpack_from('<I', target_arm, offset)[0] - 0x02000000 for offset in (0x5444C, 0x54450)]
    assert plain < len(target_arm) + 0x300000 and display < len(target_arm) + 0x300000
    snap, raw = captures.ram_at(report, 9627)
    row = rows[573]
    assert raw[plain:plain+256].split(b'\0', 1)[0].hex() == row['staged_hex'] == fixture['target_display_record']
    assert raw[display:display+256].split(b'\0', 1)[0].hex() == row['native_displays'][0]['display_hex']
    png, _ = captures.one_frame(report, 9627)
    pane, new_hold = hold(rom, painter, row, png)
    after, returned = captures.one_frame(report, 9827)
    prior_return, _ = captures.one_frame(previous, 9827)
    assert after['framebuffer_sha256'] == prior_return['framebuffer_sha256']
    last, ram = captures.ram_at(report, 9827)
    assert ram[0x30F10:0x30F14] == target_arm[0x30F10:0x30F14]
    return dict(fixture_SHA256=fixture['fixture_sha256'], fixture_program=str(replay.PROOF),
                fixture_program_sha256=replay.digest(replay.PROOF), actual_fixture_gameplay=True,
                matched_spans=fixture['matched_original_arm_spans'], observed=[new_hold],
                original_release_return_frame_match=True, following_sailing=after,
                displayed_RAM=snap, transition_RAM=last,
                capture_report=str(CAPTURE), capture_report_sha256=replay.digest(CAPTURE),
                earlier_report=str(previous_capture), earlier_report_sha256=replay.digest(previous_capture)), [
                    ('Revised flagship warning / COMMON 573', pane), ('Leak / Sailing resumed', returned)]


def main():
    assert not PROOF.exists() and not SHEET.exists()
    data = stage.load(STORED)
    target = stage.NdsImage.open(price.ROM)
    staged = stage.NdsImage.open(stage.ROM)
    assert replay.digest(stage.ROM) == data['candidate_sha256']
    patch_proof = stage.load(price.PROOF)
    assert replay.digest(price.ROM) == patch_proof['candidate_sha256'] and patch_proof['staged_parent_sha256'] == data['candidate_sha256']
    assert staged.read_file(stage.COMMON) == target.read_file(stage.COMMON)
    assert replay.compatible_arm(staged, target)
    painter, _, _ = stage.font_tools(target)
    rows = {row['message_ID']: row for row in data['records']}
    mermaid, first = verify_mermaid(target, painter, rows)
    leak, second = verify_leak(target, painter, rows)
    square = stage.load(SQUARE)
    assert square['candidate_sha256'] == data['candidate_sha256'] and square['changed_records_observed'] == [682, 687]
    assert all(replay.digest(path) == sha for path, sha in square['evidence'].items())
    panels = first + second
    sheet = Image.new('RGB', (1040, 405 * ((len(panels)+1)//2)), '#242932')
    draw = ImageDraw.Draw(sheet)
    for i, (caption, image) in enumerate(panels):
        x, y = (i % 2) * 520, (i // 2) * 405
        draw.text((x + 4, y + 3), caption, fill='white')
        sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 17))
    sheet.save(SHEET)
    stage.write(PROOF, dict(candidate_sha256=patch_proof['candidate_sha256'], previous_square_sha256=data['candidate_sha256'],
        mermaid=mermaid, leak=leak, square_evidence=str(SQUARE), square_evidence_sha256=replay.digest(SQUARE),
        revised_emulator_samples=[573, 682, 687], exact_current_sea_ROM_play=False,
        fresh_leak_fixture_and_inherited_mermaid_gameplay=True, natural_encounter_selection=False, hardware=False,
        sheet=str(SHEET), sheet_sha256=replay.digest(SHEET)))
    print('Bound both earlier sailing transitions and the revised warning to the staged display.')


if __name__ == '__main__':
    main()
