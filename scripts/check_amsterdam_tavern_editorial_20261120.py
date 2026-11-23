"""Check the Amsterdam Tavern conversation against clean text and native display."""

from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.observe_amsterdam_facilities_20261119 import REGISTERED
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.probe_tavern_conversations_v764 import format_case
from scripts.seal_shared_text_source_v1 import reference
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_rafael_custom_name_20261119 import read, snapshot


ROOT = Path('work/amsterdam_tavern_editorial_20261120_v2')
EVIDENCE = Path('E:/Rota Nova translations/Generated/work')
PREVIOUS = EVIDENCE / 'amsterdam_town_route_20261120_v2/capture'
SQUARE = EVIDENCE / 'amsterdam_facilities_20261119/capture'
REPLAY = EVIDENCE / 'amsterdam_tavern_editorial_20261120_v2/capture'
ARM, COMMON = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
NATIVE = ROOT / 'native_display.json'
SHEET = ROOT / 'native_pages.png'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/amsterdam_tavern_editorial_20261120_v1.json')

EDITS = {59: b'How about one more drink?', 827: b' %s, huh? Cheers! Glad we met.'}
GLOSSES = {
    51: 'Welcome. What will you have?',
    53: 'It costs five gold coins.',
    55: 'The named hostess is called over to attend to a customer.',
    56: 'The hostess calls back an affirmative.',
    57: 'The hostess notices the customer and welcomes them.',
    59: 'The hostess invites the customer to have another drink.',
    61: 'It costs ten gold coins.',
    657: 'You are a sailor, right? The Market is the place to go for business on a large scale.',
    821: 'Locally, someone of the supplied name, hometown and occupation has considerable influence.',
    826: 'The hostess expresses teasing surprise at how little the customer can drink.',
    827: 'The hostess confirms the customer’s name and proposes a toast to becoming acquainted.',
}
DECISIONS = {
    51: ('Barkeep', 'The opening welcome leads into the order menu.',
         'The brief welcome and open question already sound like a barkeep taking an order.'),
    53: ('Barkeep', 'Ordering a drink before the barkeep shares a rumor.',
         'The matter-of-fact price preserves the five-coin amount and keeps the pace of the exchange.'),
    55: ('Barkeep', 'The barkeep calls the hostess over after sharing a rumor.',
         'The casual call keeps the hostess substitution and sounds natural when calling across the room.'),
    56: ('Wanda', 'On the first order, the hostess answers the call.',
         'The short, upbeat reply fits someone responding from across the room.'),
    57: ('Wanda', 'On the second order, the hostess greets Lil before the next offer.',
         'The fresh greeting sounds friendly and preserves the change from answering the barkeep to addressing Lil.'),
    59: ('Wanda', 'The hostess offers a second drink and the player answers Yes or No.',
         'The invitation becomes a friendly question that the two choices answer directly.'),
    61: ('Barkeep', 'The barkeep gives the price after Lil accepts the second drink.',
         'The direct price quote preserves the ten-coin charge and makes room for the hostess to resume the conversation.'),
    657: ('Shopkeeper', 'The Jewelry Shop agent sends a bulk trader to the Market.',
          'The complete question tag sounds friendly. The second line directs bulk traders to the Market, the actual facility.'),
    821: ('Barkeep', 'A drink prompts local gossip. Two successive orders produced different people and home ports.',
          'The informal “real pull” fits the barkeep. “Here” retains the local scope and the role remains a native substitution.'),
    826: ('Wanda', 'Declining the second drink gets a gently teasing response.',
          'The existing reaction carries the source’s playful surprise through a complete phrase without changing the relationship.'),
    827: ('Wanda', 'After Lil accepts and the barkeep quotes the price, the hostess confirms Lil’s name and makes a toast.',
          'The name check and short toast sound conversational. The two thoughts keep their cadence when a wide name moves the last sentence to the next row.'),
}

EVENTS = (
    (19210, 51, ()), (19910, 53, ()), (20250, 821, ('Clifford', 'London', 'soldier')),
    (20590, 55, ('Wanda',)), (20920, 56, ()), (21250, 59, ()), (21580, 61, ()),
    (21910, 827, ('Lil',)), (22900, 821, ('Bergstrom', 'Stockholm', 'soldier')),
    (23230, 55, ('Wanda',)), (23560, 57, ()), (23890, 59, ()), (24220, 826, ()),
)


def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()


def path_at(directory, frame):
    path, = (path for path in directory.glob(f'frame_{frame:06}_*.png')
             if not path.name.endswith('_final.png'))
    return path


def visible(directory, frame, font, raw, values):
    text = raw.decode('ascii')
    if values:
        text = text % values
    words = text.split()
    picture = Image.open(path_at(directory, frame)).convert('RGB')
    matches = []
    for count in range(1, min(3, len(words)) + 1):
        for cuts in combinations(range(1, len(words)), count - 1):
            segments = zip((0, *cuts), (*cuts, len(words)), strict=True)
            lines = [' '.join(words[first:last]) for first, last in segments]
            try:
                matches.append(body_mask(picture, font, lines))
            except AssertionError:
                continue
    assert len(matches) == 1, (directory.name, frame, text, matches)
    return dict(frame=frame, arguments=values, complete_visible_rows=matches[0],
                image=path_at(directory, frame).as_posix(), sha256=digest(path_at(directory, frame)))


def write_json(path, data):
    assert not path.exists(), path
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def offline(target, arm, english, original_capture):
    raw, ram_ref = snapshot(original_capture['read_only_pause_RAM_snapshots'], 21910, 'sha256')
    cpu, _ = get_machine(arm, raw)
    ascii_cases = [b'W' * n for n in range(1, 17)]
    mixed_cases = [b'FI' + bytes.fromhex('834a') * n for n in range(1, 8)]
    names = [b'Rafael', b'Hodram', b'Lil', b'Maria', b'Camille', b'Joakim', b'ICARUS', b'FALCON',
             b'Mary Ann Watson', b'Fiona I. Franklin', bytes.fromhex('834a') * 8, *ascii_cases, *mixed_cases]
    rows = [format_case(cpu, dict(message_id=827, english=english[827][1:].decode('ascii')), (name,))
            for name in names]
    for row in rows:
        assert not row['findings'] and len(row['lines']) in (1, 2), row
        if len(row['lines']) == 2:
            assert row['lines'][-1] in ('Glad we met.', 'Cheers! Glad we met.'), row
    rows.insert(0, dict(id=59, values_hex=[], formatted_hex=english[59].hex(),
                        lines=[english[59].decode('ascii')], findings=[]))
    raster, independent, _ = font_tools(target)
    kanji = target.read_file('/GRP/KANJI.FNT')
    columns, width, height = 2, 472, 84
    contact = Image.new('RGB', (width * columns, height * ((len(rows) + columns - 1) // columns)), '#242932')
    draw = ImageDraw.Draw(contact)
    for i, row in enumerate(rows):
        body = bytes.fromhex(row['formatted_hex'])
        events = []
        pixels = raster(arm, body, 0x01FFCE40 - 0x02000000, size=(228, 48),
                        instruction_limit=2_000_000, glyph_events=events)
        predicted = independent(arm, kanji, row['lines'])
        expected = bytearray(228 * 48)
        for line_no, line in enumerate(row['lines']):
            source_x = 6
            target_x = 0 if row['id'] == 59 else 6
            for character in line:
                wide = len(character.encode('cp932')) == 2
                span = 12 if wide else 6
                # The registered runtime drops ASCII ink one pixel. Kana
                # stays on the original baseline, including in mixed names.
                for offset in range(12):
                    y = line_no * 16 + offset
                    src = y * 228 + source_x
                    dest = (y + int(not wide)) * 228 + target_x
                    expected[dest:dest + span] = predicted[src:src + span]
                source_x += span
                target_x += span
        assert pixels == expected, row
        assert [event['code'] for event in events if event['code'] != 32] == glyph_codes(body)
        assert all(0 <= event['x'] <= 228 - (12 if event['code'] > 255 else 6)
                   and 0 <= event['y'] <= 36 for event in events)
        x, y = i % columns * width, i // columns * height
        draw.text((x + 6, y + 3), f"{row['id']} / case {i + 1}", fill='white')
        preview = Image.frombytes('L', (228, 48), bytes(0 if value else 255 for value in pixels))
        contact.paste(preview.crop((0, 0, 228, 32)).resize((456, 64), Image.Resampling.NEAREST), (x + 6, y + 17))
        row.update(complete_native_ink=True, single_page=True, ink_sha256=sha256(pixels).hexdigest())
    assert not SHEET.exists()
    contact.save(SHEET)
    return dict(cases=rows, source_RAM=ram_ref, contact_sheet=SHEET.as_posix(),
                contact_sha256=digest(SHEET), independent_full_glyph_masks=True)


def inputs_only(report, expected_sha):
    assert report['ROM_sha256'] == expected_sha
    assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded')
    assert not report['callback_errors'] and not any(v for k, v in report.items() if k.startswith('synthetic_'))


def main(visual_sha256=None):
    release, stage = read(REGISTERED), read(ROOT / 'staging.json')
    parent_path, clean_path, target_path = Path(release['candidate']), Path('work/clean.nds'), ROOT / 'candidate.nds'
    assert digest(parent_path) == release['candidate_sha256'] == stage['parent']
    assert digest(clean_path) == release['clean_input_sha256']
    assert digest(target_path) == stage['target']
    clean, latest, target = map(NdsImage.open, (clean_path, parent_path, target_path))
    arm = target.read_file(ARM)
    assert arm == latest.read_file(ARM) and sha256(arm).hexdigest() == release['target_ARM9_sha256']
    directory_sha = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    old, new = [owned_entries(image.read_file(COMMON), arm, directory_sha) for image in (latest, target)]
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    assert {a.message_id for a, b in zip(old, new, strict=True) if a.text != b.text} == set(EDITS)
    for number in DECISIONS:
        assert new[number].text == EDITS.get(number, old[number].text)
        assert re.findall(rb'%[a-z]', source[number].text) == re.findall(rb'%[a-z]', new[number].text)
        assert old[number].text.startswith(b' ') == new[number].text.startswith(b' ')

    original = read(PREVIOUS / 'capture_report.json')
    inputs_only(original, stage['parent'])
    if not NATIVE.exists():
        assert visual_sha256 is None
        write_json(NATIVE, offline(target, arm, EDITS, original) | dict(candidate_sha256=stage['target']))
    if visual_sha256 is None:
        print(f"Native display passed. Contact sheet {digest(SHEET)}")
        return
    assert visual_sha256 == digest(SHEET) == read(NATIVE)['contact_sha256']

    replay = read(REPLAY / 'capture_report.json')
    inputs_only(replay, stage['target'])
    assert replay['scripted_input_schedule'] == original['scripted_input_schedule']
    assert replay['frames'] > 24550
    cases = {n: [] for n in DECISIONS}
    font = GameAsciiFont.from_arm9(arm)
    square = read(SQUARE / 'capture_report.json')
    inputs_only(square, stage['parent'])
    cases[657].append(dict(previous=visible(SQUARE, 16830, font, old[657].text, ()),
                           installed_text_unchanged=True))
    cases[53].append(dict(previous=visible(PREVIOUS, 22570, font, old[53].text, ()),
                          installed_text_unchanged=True))
    sections = []
    for frame, number, values in EVENTS:
        before = visible(PREVIOUS, frame, font, old[number].text, values)
        after = visible(REPLAY, frame, font, new[number].text, values)
        if number not in EDITS:
            assert before['complete_visible_rows'] == after['complete_visible_rows']
        if number in (59, 827):
            regions = ([(0, 191, 256, 294), (150, 313, 245, 375)] if number == 59 else [(0, 192, 256, 293)])
            before_image, after_image = [Image.open(path['image']).convert('RGB') for path in (before, after)]
            for region in regions:
                assert before_image.crop(region).tobytes() == after_image.crop(region).tobytes(), (number, frame, region)
            sections.append(dict(frame=frame, message_id=number, identical_prompt_or_portrait_regions=regions))
        cases[number].append(dict(previous=before, staged=after))
    for frame in (19560, 22240, 24550):
        before, after = [Image.open(path_at(directory, frame)).convert('RGB') for directory in (PREVIOUS, REPLAY)]
        assert before.crop((0, 192, 256, 384)).tobytes() == after.crop((0, 192, 256, 384)).tobytes(), frame

    gates = sorted(REQUIRED_REVIEW_GATES)
    rows = []
    for number, (speaker, context, note) in DECISIONS.items():
        rows.append(dict(id=f'COMMON_MESSAGE_{number}', message_ID=number, file_path=COMMON,
                         speaker=speaker, context=context, source_meaning=GLOSSES[number], localization_note=note,
                         clean_Japanese=source[number].text.decode('cp932'),
                         source_reference=reference(source[number]), current_reference=reference(old[number]),
                         staged_reference=reference(new[number]),
                         source_hex=source[number].text.hex(), current_hex=old[number].text.hex(),
                         staged_hex=new[number].text.hex(),
                         english=' '.join(new[number].text.decode('ascii').split()),
                         decision='revision' if number in EDITS else 'retention',
                         observed_gameplay=cases[number], review=dict.fromkeys(gates, True)))
    reports = (PREVIOUS / 'capture_report.json', REPLAY / 'capture_report.json', SQUARE / 'capture_report.json')
    result = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                  review_gates=gates, records=rows, candidate_sha256=stage['target'],
                  parent_sha256=stage['parent'], clean_input_sha256=release['clean_input_sha256'],
                  new_contextual_credit=0, native_formatting=read(NATIVE), viewed_native_sheet=visual_sha256,
                  capture_reports={str(p): digest(p) for p in reports}, ordinary_replay=True,
                  usual_prompt_and_portrait_regions=sections, tavern_menu_stock_return_frames=[19560, 22240, 24550],
                  scope='Two drink orders, two local rumors, both responses to the second drink and one Jewelry Shop referral. Hardware and unvisited branches remain open.')
    validate_natural_dialogue_batch(result)
    write_json(MANUSCRIPT, result)
    print(f'{len(rows)} checked records, {len(EVENTS)} played Tavern frames, {len(EDITS)} revisions.')


if __name__ == '__main__':
    import sys

    main(*sys.argv[1:])
