"""Verify the original sea dialogue from the provisioned Madeira departure."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import check_swimmer_leak_square_dialogue_20261120 as verification
from scripts import replay_madeira_resupply_numerals_20261120 as replay
from scripts import stage_madeira_resupply_numerals_20261120 as stage
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold


ROOT = Path('E:/Rota Nova translations/Generated/work/madeira_provisioned_events_20261120_v2')
SHEET, PROOF = stage.ROOT / 'sea_playback.png', stage.ROOT / 'sea_gameplay.json'
batch = stage.batch


def main():
    assert not SHEET.exists() and not PROOF.exists()
    prior = batch.load(batch.ROOT / 'staging.json')
    combined = batch.load(stage.PROOF)
    assert prior['candidate_sha256'] == combined['staged_parent_sha256']
    assert verification.digest(stage.ROM) == combined['candidate_sha256']
    rom = batch.NdsImage.open(stage.ROM)
    arm, kanji = [rom.read_file(p) for p in (batch.ARM, '/GRP/KANJI.FNT')]
    painter, _, _ = batch.font_tools(rom)
    expand, display = [unpack_from('<I', arm, offset)[0] - stage.BASE for offset in (0x5444C, 0x54450)]
    outcomes, panels, evidence = {}, [], {}
    for event, expected, count in (('mermaid', batch.SWIMMER, 2), ('leak', range(573, 580), 1)):
        report_path = ROOT / event / 'capture_report.json'
        report = batch.load(report_path)
        assert report['ROM_sha256'] == combined['candidate_sha256'] and report['cold_boot']
        assert not report['savestate_loaded'] and not report['callback_errors']
        assert {k for k, v in report.items() if k.startswith('synthetic_') and v} == {'synthetic_condition_fixtures'}
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and verification.digest(donor['source']) == donor['source_sha256']
        controls = report['synthetic_condition_fixtures']
        assert len(controls) == 4 and all(value['no_encounter_branch_temporarily_bypassed'] for value in controls[2:])
        assert [value['frame'] for value in controls[-2:]] == [13307, 13907]
        first, last = controls[-2:]
        reversed_changes = [dict(address=change['address'], before=change['after'], after=change['before'])
                            for change in first['changes']]
        assert last['changes'] == reversed_changes
        assert all(change['address'] in range(0x02030F08, 0x02030F14) for change in first['changes'])
        history = {}
        for row in prior['records']:
            if row['message_ID'] not in expected:
                continue
            layout, = row['native_displays']
            assert layout['display_hex'] not in history
            history[layout['display_hex']] = row, layout
        observed = []
        for frame in (13907, 14247, 14587):
            snap, ram = verification.ram_at(report, frame)
            shown = ram[display:display+256].split(b'\0', 1)[0]
            if shown.hex() not in history:
                continue
            row, layout = history[shown.hex()]
            if any(earlier['id'] == row['message_ID'] for earlier in observed):
                continue
            assert ram[expand:expand+256].split(b'\0', 1)[0].hex() == row['staged_hex']
            pixels, glyphs = batch.render_portrait(painter, arm, kanji, shown)
            assert batch.digest(pixels) == layout['complete_ink_sha256'] and len(glyphs) == layout['glyph_count']
            shot, panel = verification.one_frame(report, frame)
            ink = native_hold(panel, pixels)
            evidence.update({snap['path']: snap['sha256'], shot['path']: shot['PNG_sha256']})
            observed.append(dict(id=row['message_ID'], frame=frame, lines=layout['visible_lines'], visible_ink=ink))
            panels.append((panel, f"{event} / COMMON {row['message_ID']}"))
        assert len(observed) == count, (event, observed)
        if event == 'mermaid':
            assert observed[0]['id'] in range(441, 449) and observed[1]['id'] in range(449, 457)
        after, panel = verification.one_frame(report, 14927)
        snap, ram = verification.ram_at(report, 14927)
        assert ram[0x30F08:0x30F14] == arm[0x30F08:0x30F14]
        assert not any(panel.getpixel((x, y)) == (0, 8, 0) for x in range(16, 244) for y in range(296, 360))
        evidence.update({snap['path']: snap['sha256'], after['path']: after['PNG_sha256'],
                         str(report_path): verification.digest(report_path)})
        panels.append((panel, f'{event} / Returned to sailing'))
        outcomes[event] = dict(observed=observed, following_sailing_frame=after, restored_dispatch_bytes=True,
                               temporary_selection=first, full_restore=last)
    sheet = Image.new('RGB', (1040, 405 * ((len(panels) + 1) // 2)), '#242932')
    draw = ImageDraw.Draw(sheet)
    for i, (panel, label) in enumerate(panels):
        x, y = (i % 2) * 520, (i // 2) * 405
        draw.text((x + 4, y + 3), label, fill='white')
        sheet.paste(panel.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 17))
    sheet.save(SHEET)
    evidence[str(SHEET)] = verification.digest(SHEET)
    batch.write(PROOF, dict(candidate_sha256=combined['candidate_sha256'], outcomes=outcomes,
         natural_encounter_selection=False, actual_emulator=True, hardware=False,
         changed_records_observed=sorted({row['id'] for result in outcomes.values() for row in result['observed']}
                                         & batch.EDITS.keys()), evidence=evidence))
    print('Both original sea encounters and both sailing returns verified.')


if __name__ == '__main__':
    main()
