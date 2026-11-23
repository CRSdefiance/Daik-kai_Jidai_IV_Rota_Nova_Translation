"""Stage the active New Game confirmation and system-data notices."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts import preflight_setup_save_equipment_v1 as modal
from scripts import register_square_shop_captions_20261115 as parent
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.review_setup_save_equipment_v1 import OUTPUT as HISTORICAL
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts
from scripts.stage_setup_save_equipment_v1 import check_stored
from scripts.verify_release_baseline import files

base = parent.base
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
COMMON = parent.parent.stage.COMMON
ROOT = Path('work/setup_confirmation_prose_20261115_v2')
ROM = ROOT / 'Setup_Confirmation_Prose_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
SHEET = ROOT / 'setup_modal_previews.png'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
DECISIONS = {
    112: (None, 'System data is absent.',
          'The absence notice can precede the generic load failure.',
          'System data not found is concise and distinguishes an absent file from a corrupt one.'),
    118: (None, 'The system data is corrupt.',
          'Reports damage detected before the default-data startup notice.',
          'The existing wording identifies system data and states its condition precisely.'),
    120: ('Is everything OK?', 'Asks whether all the selected details are acceptable.',
          'The player has reviewed the character settings and opened the confirmation.',
          'Use a complete, conversational question and retain the reference to all the selected settings.'),
    121: (None, 'Asks whether to start the game.',
          'An independent start decision.',
          'Start the game? states the pending action directly and reads naturally in a menu.'),
    122: ("Couldn't load system data. The game will start with defaults.",
          'The load failed. The game will start with the system data initialized to its defaults.',
          'The original recovery branch displays this after reporting system-data corruption.',
          'Use the same direct failure wording as the short notice, then explain that the game will start with default data.'),
    123: ("Couldn't load system data.", 'Reports that the system data could not be loaded.',
          'The standalone failure notice applies to three original calls, including the missing-data path.',
          'Use an idiomatic error sentence. Preserve the distinction from the separate notice that announces a default-data start.'),
}


def digest(raw):
    return sha256(raw).hexdigest()


def main():
    assert not ROM.exists() and not STORED.exists()
    prior = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == prior['registry_sha256']
    assert base.digest(CLEAN) == prior['clean_input_sha256']
    runtime = modal.RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    context = {row['message_ID']: row for row in base.load(HISTORICAL)['legacy_setup_and_save_records']}
    clean = base.NdsImage.open(CLEAN)
    source_arm = clean.read_file(ARM)
    originals = common_message_entries(clean.read_file(COMMON), source_arm)
    arm, common = runtime.arm, runtime.common
    stored = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    raster, _, _ = modal.font_tools(runtime.image)
    font = modal.GameAsciiFont.from_arm9(arm)
    records, replacement = {}, {}
    for n, (revision, meaning, situation, note) in DECISIONS.items():
        old = stored[n]
        source = originals[n]
        evidence = context[n]
        assert evidence['already_credited'] and evidence['direct_consumer_found']
        assert evidence['source_hex'] == source.text.hex()
        for caller in evidence['native_callers']:
            at = caller['code_start'] - 0x02000000
            exact = bytes.fromhex(caller['exact_hex'])
            assert source_arm[at:at + len(exact)] == arm[at:at + len(exact)] == exact
        callers = [r for r in evidence['native_callers'] if r['target'] != 0x0205528C]
        assert callers and b'%' not in source.text + old.text
        prose = revision or ' '.join(old.text.decode('ascii').split())
        record = {
            'id': f'COMMON_MESSAGE_{n}', 'message_ID': n, 'file_path': COMMON, 'speaker': 'System',
            'context': situation, 'source_meaning': meaning, 'localization_note': note,
            'source_Japanese': source.text.decode('cp932'), 'source_hex': source.text.hex(),
            'source_reference': reference(source), 'current_reference': reference(old), 'current_hex': old.text.hex(),
            'previous': old.text.decode('ascii'), 'english': prose,
            'decision': 'revision' if revision else 'retention', 'native_callers': callers,
            'review': dict.fromkeys(GATES, True),
        }
        records[n] = record
        if n == 122:
            scope = compile_layouts.__globals__ | {'PHRASES': {122: ('The game will start with defaults.',)}}
            formatter = FunctionType(compile_layouts.__code__, scope)
            replacement[n] = formatter({n: record})[n]
        elif revision:
            probe, _ = modal.check_modal(runtime, record, (), raster, font)
            assert probe['complete_glyphs_bounds_and_words']
            replacement[n] = probe['storage_markup'].replace('{LB}', '\n').encode('ascii')

    new_common, rebound, storage = owned_deployment(common, arm, stored, replacement)
    deployed = with_components(runtime, arm, new_common)
    native = check_stored()
    sheet = Image.new('RGB', (944, 348), '#263238')
    drawing = ImageDraw.Draw(sheet)
    for index, (n, record) in enumerate(records.items()):
        text = rebound[n].text
        wrapper = record['native_callers'][0]['target']
        result = native(deployed, {**record, 'english': text.decode('ascii'), 'current_hex': text.hex(),
                                   'current_copies': [{'wrapper': wrapper}]}, ())
        deployed.calls.clear()
        display = bytes.fromhex(result['native_wrapper_output_hex'])
        plane, lines, origins, glyphs = modal.render(raster, font, arm, display)
        assert ' '.join(' '.join(lines).split()) == record['english']
        if n == 122:
            assert lines == ["Couldn't load system data.", "The game will start with defaults."]
        record['registered_reference'] = reference(rebound[n])
        record['deployed_hex'] = text.hex()
        record['display'] = {'lines': lines, 'origins': origins, 'glyph_count': len(glyphs),
                             'native_plane_sha256': digest(plane), 'complete_native_format': result}
        x, y = (index % 2) * 472, (index // 2) * 116
        drawing.text((x + 5, y + 2), f"{n}  {record['decision']}", fill='white')
        page = Image.frombytes('L', (228, 48), bytes(0 if value else 255 for value in plane))
        sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 5, y + 16))

    direct_112 = modal.current_copy(deployed, records[112], 0x0205528C)
    assert direct_112['copied_hex'] == records[112]['current_hex']
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(COMMON, new_common)
    after = files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {COMMON}
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    sheet.save(SHEET)
    base.save(STORED, {
        'candidate_sha256': base.digest(ROM), 'previous_sha256': prior['candidate_sha256'],
        'target_ARM9_sha256': digest(arm), 'target_COMMON_sha256': digest(new_common),
        'records': list(records.values()), 'allocations': storage, 'whole_parent_inverse': True,
        'separate_112_getter': direct_112, 'native_sheet': {'path': str(SHEET), 'sha256': base.digest(SHEET)},
    })
    print('Staged three revisions and three retentions. All six native modal pages passed.')


if __name__ == '__main__':
    main()
