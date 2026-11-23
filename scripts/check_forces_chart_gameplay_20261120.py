"""Verify all eight revised chart fields in paired original game screens."""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_forces_chart_native_20261120 as native
from scripts import replay_forces_chart_fields_20261120 as replay
from scripts import stage_forces_chart_fields_20261120 as stage
from scripts.check_swimmer_leak_square_dialogue_20261120 import one_frame
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.verify_inn_numerals_native_20261119 import read_cstring


ROOT = Path('E:/Rota Nova translations/Generated/work/forces_chart_fields_20261120')
PROOF, SHEET = stage.ROOT / 'gameplay_fields.json', stage.ROOT / 'gameplay_fields.png'
COLOR = 230, 230, 230
FONT_FIELDS = tuple(kind for kind in native.STATIC if kind.startswith('UNKNOWN_'))
PANELS = {13280: ('REGIONAL_POWER', 'SELF_TIES'), 13580: FONT_FIELDS,
          13980: ('REGIONAL_POWER', 'NO_HOME', 'SELF_TIES'), 14480: ('REGIONAL_POWER', 'SELF_TIES')}
COMMON = dict(who='Forces chart', written=True)
FIELD_CONTEXT = {
    'UNKNOWN_LEADER': ('The original chart hides the faction leader’s identity until the player knows this faction.',
                       'The leader is unknown.', 'Use the normal font for the same question mark.'),
    'UNKNOWN_LEVEL': ('The chart withholds the leader’s experience level.',
                      'The level is unknown.', 'Use the same question mark as the other unknown values.'),
    'UNKNOWN_FUNDS': ('The chart obscures the faction’s funds under limited information.',
                      'The funds are unknown.', 'Keep the distinction between unknown funds and an actual amount of zero.'),
    'UNKNOWN_POWER': ('The chart has no Power figure to reveal for this faction.',
                      'The faction’s Power is unknown.', 'Preserve the unknown value and normalize the glyph.'),
    'REGIONAL_POWER': ('The Power row shows the global total followed by the selected region and its subtotal.',
                       'Total Power, followed by the region name and that region’s Power in parentheses.',
                       'Use standard punctuation and retain all three arguments in order. The existing region abbreviations supply the labels.'),
    'UNKNOWN_HOME': ('The faction has a home base but insufficient information keeps the player from seeing it.',
                     'The faction’s home is unknown.', 'Keep it distinct from a known absence of a home.'),
    'NO_HOME': ('The chart has no home port for a faction and the original getter returns the no-home sentinel.',
                'The faction has no home port.', 'None is a compact value under Home and preserves the distinction from the question mark.'),
    'SELF_TIES': ('The player’s faction is selected, so the chart shows no relationship rating with itself.',
                  'A dash marks the inapplicable score.', 'Use the regular-width dash and retain the original position.'),
}


def memory(report, n):
    entry, = [r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == n]
    data = Path(entry['path']).read_bytes()
    assert entry['read_only_export'] and len(data) == 0x400000 and stage.parent.base.digest(entry['path']) == entry['sha256']
    return entry, data


def company_state(arm, raw):
    cpu, get = replay.history.get_machine(arm, raw)
    record = get(0xCB160) + 4
    assert get(0x397D8) == 0
    assert read_cstring(cpu, get(0x3CF9C, record)) == b'Castor Co.'
    assert get(0x3CBFC, record) == get(0x3CC74, record, 1) == 122
    return get(0x3CD24, record), bytes(cpu.mem_read(record, 76)).hex()


def targets(identifier):
    if identifier == 'REGIONAL_POWER':
        return '122 (Med.: 122)', 56, 128
    return native.STATIC[identifier][:3]


def main():
    assert not PROOF.exists() and not SHEET.exists()
    base, batch = stage.parent.base, stage.batch
    stored = batch.load(stage.PROOF)
    docs = [ROOT / side / 'capture/capture_report.json' for side in ('current', 'revised')]
    reports = [batch.load(path) for path in docs]
    assert reports[0]['scripted_input_schedule'] == reports[1]['scripted_input_schedule']
    assert reports[0]['core_DLL_sha256'] == reports[1]['core_DLL_sha256'] and reports[0]['core_options'] == reports[1]['core_options']
    checks = [13000, 13280, 13580, 13980, 14480, 14980]
    capture, model = [], []
    chart_sheets = Image.new('RGB', (1032, 3 * 263), '#263238')
    draw = ImageDraw.Draw(chart_sheets)
    ledger = []
    evidence = {str(path): base.digest(path) for path in docs}
    for index, report in enumerate(reports):
        rom = stage.ROM if index else stage.parent.ROM
        assert report['ROM_sha256'] == base.digest(rom) == stored['candidate_sha256' if index else 'parent_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == 14980
        donor = report['battery_save_preloaded']
        assert donor['copied_byte_exact_before_cold_boot'] and base.digest(donor['source']) == donor['source_sha256']
        fixtures = report['synthetic_condition_fixtures']
        assert [(r['frame'], r['mode']) for r in fixtures] == [(13600, 'show-no-home'), (14000, 'restore-home')]
        assert all(len(r['changes']) == 1 for r in fixtures)
        remove, restore = [r['changes'][0] for r in fixtures]
        assert remove == dict(address=restore['address'], before=restore['after'], after=restore['before'])
        assert remove['after'] == 0x73
        arm = batch.NdsImage.open(rom).read_file(batch.ARM)
        control = {n: one_frame(report, n) for n in checks}
        capture.append(control)
        states = {}
        for n in (13280, 13980, 14480, 14980):
            entry, raw = memory(report, n)
            evidence[entry['path']] = entry['sha256']
            states[n] = company_state(arm, raw)
        assert [key for key, _ in states.values()] == [remove['before'], 0x73, remove['before'], remove['before']]
        assert states[13280] == states[14480] == states[14980]
        model.append(states)
        font = GameAsciiFont.from_arm9(arm)
        for n, (shot, image) in control.items():
            evidence[shot['path']] = shot['PNG_sha256']
            if n in PANELS and index:
                for field in PANELS[n]:
                    text, x, y = targets(field)
                    box = (x, y, x + max(len(text) * 6 + 6, 25), y + 12)
                    count = font_mask(image, font, text, x, y + 1, box, COLOR)
                    ledger.append(dict(field=field, frame=n, value=text, origin=[x, y], complete_pixels=count))
        for row, n in enumerate((13280, 13580, 13980)):
            xp, yp = index * 516, row * 263
            draw.text((xp + 6, yp + 3), f'{("Previous", "Revised")[index]}  /  frame {n}', fill='white')
            section = control[n][1].crop((0, 62 if n != 13580 else 22, 256, 182 if n != 13580 else 164))
            if n == 13580:
                section = section.resize((384, 213), Image.Resampling.NEAREST)
            else:
                section = section.resize((512, 240), Image.Resampling.NEAREST)
            chart_sheets.paste(section, (xp + 2, yp + 18))
    assert model[0] == model[1]
    assert all(a['changes'] == b['changes'] for a, b in zip(
        *(r['synthetic_condition_fixtures'] for r in reports), strict=True))
    assert {row['field'] for row in ledger} == set(native.STATIC) | {'REGIONAL_POWER'}
    fields_changed = {}
    for n in checks:
        diff = ImageChops.difference(*(r[n][1] for r in capture))
        if n not in PANELS:
            assert diff.getbbox() is None
            continue
        for field in PANELS[n]:
            _, x, y = targets(field)
            width = 170 if field == 'REGIONAL_POWER' else 32
            diff.paste((0, 0, 0), (x, y, x + width, y + 13))
        assert diff.getbbox() is None, (n, diff.getbbox())
        fields_changed[n] = PANELS[n]
    chart_sheets.save(SHEET)
    decisions = []
    for row in stored['rows']:
        identifier = row['id'].removeprefix('DK4_FORCES_')
        context, gloss, reason = FIELD_CONTEXT[identifier]
        decisions.append(row | dict(file_path=batch.ARM, speaker=COMMON['who'], context=context,
            source_meaning=gloss, localization_note=reason, decision='revision', review=dict.fromkeys(batch.GATES, True)))
    clean = batch.NdsImage.open(batch.CLEAN).read_file(batch.ARM)
    current = batch.NdsImage.open(stage.parent.ROM).read_file(batch.ARM)
    for identifier, offset, size, literal, gloss, reason in (
        ('LEADER_FORMAT', 0x14C1E8, 12, 0x8D7D4, 'The company head’s title, followed by the original class or occupation.',
         'Leader is a neutral title for a faction head and the parenthetical role uses the original substitution.'),
        ('UNKNOWN_FORCE', 0x14C1FC, 16, 0x8D7E0, 'A faction whose identity is unknown.',
         'Unknown Force follows the terminology used by the Forces chart and does not imply a particular identity.'),
    ):
        source, existing = [data[offset:offset + size] for data in (clean, current)]
        decisions.append(dict(id=f'DK4_FORCES_{identifier}', file_path=batch.ARM, speaker=COMMON['who'],
            offset=offset, slot_bytes=size, literal_offset=literal, source_hex=source.hex(),
            current_hex=existing.hex(), clean_Japanese=source.split(b'\0', 1)[0].decode('cp932'),
            english=existing.split(b'\0', 1)[0].decode('ascii'), context='Original Forces chart caption.',
            source_meaning=gloss, localization_note=reason, decision='retention', review=dict.fromkeys(batch.GATES, True)))
    batch.write(PROOF, dict(candidate_sha256=stored['candidate_sha256'], predecessor_sha256=stored['parent_sha256'],
        fixtures=['Original home lookup set to its existing no-home sentinel, then restored.'], gameplay=ledger,
        fields_changed=fields_changed, same_before_and_after=[13000, 14980], states=model[1], evidence=evidence,
        records=decisions, sheet=str(SHEET), sheet_sha256=base.digest(SHEET), hardware=False))
    print('Original chart, unknown fields, no-home state and exact return verified across both ROMs.')


if __name__ == '__main__':
    main()
