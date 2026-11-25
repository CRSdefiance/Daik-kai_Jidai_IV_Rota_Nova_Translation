"""Verify the first-voyage lesson reached by hiring sailors and leaving the Tavern."""

from pathlib import Path

from PIL import Image, ImageDraw

from scripts import check_rafael_tavern_lesson_20261119 as tavern
from scripts import register_rafael_first_voyage_20261119 as prior
from scripts import register_rafael_tavern_lesson_20261119 as current
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask

base, native, deck = tavern.base, tavern.native, tavern.deck
ROOT = tavern.replay.ROOT / 'followthrough_v3'
OUTPUT = current.VERIFY / 'ordinary_first_voyage_replay.json'
NAMES = {0: 'Rafael Castor', 4: 'Janus Pasar', 5: 'Claudio Manaus', 6: 'Julio Erneco'}


def main():
    assert not OUTPUT.exists()
    paths = [ROOT / p for p in ('capture/capture_report.json', 'observer/commands.json', 'inputs.json', 'source_contract.json')]
    report, trace, inputs, _ = map(base.load, paths)
    release, earlier = map(base.load, (current.RELEASE, prior.REVIEW))
    assert report['ROM_sha256'] == release['candidate_sha256'] == base.digest(current.ROM)
    assert report['frames'] == tavern.replay.END and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and report['scripted_input_schedule'] == inputs
    assert {'start': 22620, 'duration': 8, 'buttons': ['B']} in inputs
    assert not any(value for key, value in report.items() if key.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
    assert not trace['mismatches'] and not trace['errors']
    pending, = trace['unreturned_at_capture_end']
    assert trace['rows'][pending['entry_row']]['source']['block'] == 127
    assert trace['all_host_slots_restored_and_core_file_exact']
    evidence = {str(p): base.digest(p) for p in (*paths, prior.REVIEW, current.RELEASE, Path(__file__))}
    rom = base.NdsImage.open(current.ROM)
    bank = native.IlnkContainer.parse(rom.read_file(deck.SC0)).blocks
    prior_bank = native.IlnkContainer.parse(base.NdsImage.open(prior.ROM).read_file(deck.SC0)).blocks
    assert prior_bank[42] == bank[42]
    b138, b42, b127 = (tavern.observed_commands(trace, block, native.digest(bank[block])) for block in (138, 42, 127))
    assert len(b138) == 10 and len(b42) == 31 and b127
    assert b138[-1][1]['frame'] < 22620 < b42[0][0]['frame']
    assert b42[-1][1]['source']['first_word'] == b42[-1][1]['result_words'][0] == 0
    assert b42[-1][1]['frame'] < 29295 < b127[0][0]['frame']
    indexed = {row['registered_reference']['command_offset']: row for row in earlier['records']}
    assert len(indexed) == 28
    arm, cjk = rom.read_file(native.ARM), rom.read_file(deck.FONT)
    _, paint = tavern.stage.template.stage.progressive.layout.prior.precedent.planners(arm)
    font = deck.GameAsciiFont.from_arm9(arm)
    photos = deck.shots(report)
    audited, images = [], []
    for entered, returned in b42:
        at = entered['source']['instruction_offset']
        if entered['source']['first_word'] != 0x4000:
            assert at not in indexed
            continue
        row = indexed.pop(at)
        stored = bytes.fromhex(row['registered_reference']['exact_stored_hex'])
        assert bank[42][at+5:at+5+len(stored)+1] == stored + b'\0'
        selector, body = stored[0], stored[1:]
        assert selector == row['source_selector'] and selector in NAMES and body.isascii()
        swapped = row['id'] == 'DK4_MES_B42_R0080'
        if swapped:
            assert body.startswith(b'FI,') and body.count(b'FI') == 1
            body = body.replace(b'FI', b'Rafael')
        else:
            assert b'FI' not in body
        rendered = paint(arm, cjk, body)
        assert rendered['complete_consumed_bytes'] == len(body)
        page, = rendered['pages']
        assert page['native_independent_plane_equal']
        expected = deck.TOOL.prior.masks(bytes.fromhex(page['native_plane_hex']))
        candidates = range(entered['frame']+25, returned['frame']-4)
        for frame, photo in sorted(photos.items()):
            if frame not in candidates:
                continue
            screen = deck.captured(photo)
            if deck.TOOL.body_masks(screen) == expected:
                count, bounds = complete_mask(font, NAMES[selector], screen, 16, 277, (98, 97, 98))
                evidence[photo['path']] = photo['PNG_sha256']
                audited.append(dict(id=row['id'], source=row['source_reference'], current=row['registered_reference'],
                    capture=photo['path'], frame=frame, native_plane_sha256=native.digest(bytes.fromhex(page['native_plane_hex'])),
                    complete_exact_body_mask=True, nameplate=NAMES[selector], nameplate_ink=count, nameplate_bounds=bounds,
                    runtime_Rafael_substitution_observed=swapped))
                images.append((row['id'], screen))
                break
        else:
            raise AssertionError((row['id'], entered['frame'], returned['frame'], 'missing complete observed page'))
    assert not indexed and len(audited) == 28 and sum(r['runtime_Rafael_substitution_observed'] for r in audited) == 1
    for frame in (22565, 29295, 29985, 30610):
        shot = photos[frame]
        assert base.digest(shot['path']) == shot['PNG_sha256']
        evidence[shot['path']] = shot['PNG_sha256']

    sheets = []
    for i in range(0, len(images), 7):
        sheet = Image.new('RGB', (1024, 280), '#263238')
        draw = ImageDraw.Draw(sheet)
        for j, (ident, image) in enumerate(images[i:i+7]):
            x, y = 256 * (j % 4), 140 * (j // 4)
            draw.text((x+5,y+5), ident, fill='white')
            crop = image.crop((0,269,256,384))
            sheet.paste(crop, (x,y+20))
        path = ROOT / f'first_voyage_panels_{i//7+1}.png'
        sheet.save(path)
        evidence[str(path)] = base.digest(path)
        sheets.append(dict(path=str(path), sha256=evidence[str(path)]))
    base.save(OUTPUT, dict(candidate_sha256=release['candidate_sha256'], story_archive=deck.SC0, checked_block=42,
        source_candidate_review=str(prior.REVIEW), first_voyage_block_exact_to_prior_review=True,
        ordinary_gameplay_existing_Lisbon_save=True, hardware=False, tavern_exit_input_frame=22620,
        original_event_native_commands=len(b42), native_speech_pages=audited, normal_Port_menu_frame=29295,
        following_Ceuta_tutorial_returned_commands=len(b127), Ceuta_tutorial_page_in_progress_at_end=True, sheets=sheets,
        new_contextual_credit=0, evidence=evidence))
    print('All 28 first-voyage panels and nameplates matched the native renderer after ordinary crew recruitment.')


if __name__ == '__main__':
    main()
