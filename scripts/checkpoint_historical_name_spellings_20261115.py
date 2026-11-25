"""Trace prior project spellings to current native text consumers."""

from collections import Counter
from inspect import getsource
from pathlib import Path
import re
from struct import pack, unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE
from dk4tool.patch.village_promised_words_release import resident_components
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts import register_cristina_recruitment_name_20261115 as current
from scripts import verify_artwork_caption_selector_v284 as gallery
from scripts.checkpoint_story_glyph_consistency_20261115 import catalogue
from scripts.probe_button_prompt_native import call, machine
from scripts.reconcile_shared_speaker_labels_20261111 import current_getters
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/historical_name_spellings_20261115_v1.json')
GLOSSARY = Path('docs/glossary.md')
OLD = re.compile(rb'\b(?:Raphael|Kamil|Joachim)\b', re.IGNORECASE)
DESC = 0x115678
MIDDLE = 0x148EBC
GATES = dict(source=True, context=True, localization=True, naturalness=True, formatting=True)


def gallery_proof(clean, arm, image, components):
    staged, = [raw for _, address, raw in components if address == STAGE]
    captions = validate(arm)
    assert all(not OLD.search(row['English'].encode('ascii')) for row in captions)
    names = [row for row in captions if re.search(r'\b(?:Rafael|Camille|Joakim)\b', row['English'])]
    assert len(names) == 15
    for row in names:
        source, = unpack_from('<I', clean, row['field'])
        raw = clean[source - BASE:].split(b'\0', 1)[0]
        row.update(source_pointer=source, source_hex=raw.hex(), Japanese=raw.decode('cp932'))

    original = checked_text(getsource(gallery.execute), {
        "NdsImage.open('out/all_routes_combined_v275_candidate.nds').rom": 'CURRENT_ROM',
        # The registered ASCII painter adds one pixel after the observed draw origin.
        'expected[(yy + gy) * 256 + xx + gx] = style': 'expected[(yy + 1 + gy) * 256 + xx + gx] = style',
        '0 <= yy <= 181': '0 <= yy <= 180',
    })
    namespace = vars(gallery) | dict(CURRENT_ROM=image.rom)
    exec(compile(original, __file__ + '::exact-current-gallery-native-overlay', 'exec'), namespace)
    rows, native = [], []
    for index, name in enumerate(('Rafael', 'Hodram', 'Lil', 'Maria')):
        field = DESC + 4 * index
        source, = unpack_from('<I', clean, field)
        pointer, = unpack_from('<I', arm, field)
        raw = clean[source - BASE:].split(b'\0', 1)[0]
        target = staged[pointer - POOL:].split(b'\0', 1)[0]
        English = f"Memorable scenes from {name}'s story."
        assert target.decode('ascii').rstrip(' ') == English
        row = dict(id=f'GALLERY_STORY_DESCRIPTION_{index}', index=index, english=English,
                   clean_pointer=source, source_hex=raw.hex(), Japanese=raw.decode('cp932'),
                   field=field, current_pointer=pointer, current_hex=target.hex(), decision='retention',
                   reason=f'The Gallery describes highlights from {name}’s own story. The wording fits the selected route and keeps the approved name.',
                   review=GATES)
        rows.append(row)
        native.extend(namespace['execute'](arm, row, mode, gallery=True) for mode in (4, 16))
    return dict(active_caption_count=len(captions), approved_name_captions=names, descriptions=rows,
                native_bitmaps=native, ascii_paint_offset_y=1)


def middle_cases(arm):
    entry, = unpack_from('<I', arm, MIDDLE)
    assert entry == 0x01FFCD00
    u = machine(arm)
    assert bytes(u.mem_read(0x01FFCE00, 25)) == b'Joachim\0Hodram\0Bergstrom\0'
    assert bytes(u.mem_read(0x0215C3D4, 7)) == b'Joakim\0'
    actor = 0x02402040
    cases = []
    for given, middle, surname, output in (
        ('Hodram', 'Joachim', 'Bergstrom', 'Joakim'),
        ('Hodram', 'Joakim', 'Bergstrom', 'Joakim'),
        ('Hodram', 'Alex', 'Bergstrom', 'Alex'),
        ('Rafael', 'Joachim', 'Bergstrom', 'Joachim'),
        ('Hodram', 'Joachim', 'Castor', 'Joachim'),
        ('Hodram', '', 'Bergstrom', ''),
    ):
        storage = bytearray(0x60)
        for start, text in ((0x20, given), (0x31, surname), (0x42, middle)):
            storage[start:start + len(text)] = text.encode('ascii')
        guarded = b'\xA5' * 16 + storage + b'\xA5' * 16
        u.mem_write(actor - 16, guarded)
        used = call(u, entry - BASE, (actor,))
        assert entry in used
        observed = u.reg_read(UC_ARM_REG_R0)
        assert observed == (0x0215C3D4 if output != middle else actor + 0x42)
        assert bytes(u.mem_read(observed, 16)).split(b'\0', 1)[0].decode('ascii') == output
        assert bytes(u.mem_read(actor - 16, len(guarded))) == guarded
        cases.append(dict(input=[given, middle, surname], displayed_middle=output, native_result_pointer=observed))
    return dict(vtable_field=MIDDLE, entry=entry, legacy_comparator=0x01FFCE00, result_cases=cases,
                original_name_record_and_neighbors_preserved=True)


def legacy_hits(components, config):
    stored, = [raw for _, address, raw in components if address == STAGE]
    keys = {}
    for row in config['records']:
        raw = bytes.fromhex(row['key_hex'])
        for match in OLD.finditer(raw):
            at = row['key_pointer'] - POOL + match.start()
            assert stored[at:at + len(match[0])] == match[0]
            keys.setdefault(at, []).append(dict(spelling=match[0].decode('ascii'), **row))
        assert not OLD.search(bytes.fromhex(row['target_hex']))

    found, retired = set(), []
    for label, address, raw in components:
        for match in OLD.finditer(raw):
            at = match.start()
            if address == STAGE and at in keys:
                found.add(at)
                continue
            if address + at == 0x01FFCE00:
                continue
            lo, hi = raw.rfind(b'\0', 0, at) + 1, raw.index(b'\0', match.end())
            start = (POOL if address == STAGE else address) + lo
            owners = []
            for owner, origin, contents in components:
                for pointer in range(start, start + hi - lo + 1):
                    needle = pack('<I', pointer)
                    owners.extend((owner, origin + m.start(), pointer) for m in re.finditer(re.escape(needle), contents))
            assert not owners, (label, start, owners)
            retired.append(dict(component=label, stored_pointer=start, old_text=raw[lo:hi].decode('ascii'),
                                term_offset=at-lo, direct_or_interior_literal_owners=owners))
    assert found == set(keys) and len(retired) == 14
    return dict(historical_lookup_key_records=[r for at in sorted(found) for r in keys[at]],
                unique_key_term_storage_offsets=len(found), retired_gallery_storage=retired)


def main():
    assert not OUTPUT.exists()
    release, manifest = map(base.load, (current.RELEASE, current.MANIFEST))
    clean, image = [base.NdsImage.open(path) for path in (stage.CLEAN, current.ROM)]
    assert base.digest(current.ROM) == release['candidate_sha256'] == manifest['candidate_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    source, arm = clean.read_file(stage.ARM), image.read_file(stage.ARM)
    assert stage.digest(arm) == release['target_ARM9_sha256']
    archives = [current.IlnkContainer.parse(image.read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)]
    assert sum(map(len, archives)) == 1307
    assert all(not OLD.search(block) for blocks in archives for block in blocks)
    common = owned_entries(image.read_file(stage.COMMON), arm, stage.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    assert len(common) == 3668 and all(not OLD.search(row.text) for row in common)
    assert not OLD.search(image.read_file('/COMMON/HELP.DK4'))

    config = manifest['relocations'][stage.ARM]['reviewed_name_integration']['catalog']
    checked = catalogue(arm, config, archives)
    assert all(not OLD.search(bytes.fromhex(row['key_hex'])) for row in checked['other_rows_with_stored_key'])
    components = resident_components(image)
    storage = legacy_hits(components, config)
    runtime = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    getters = current_getters(runtime)['rows']
    assert len(getters) == 414 and all(not OLD.search(row['text'].encode('ascii')) for row in getters)
    focused = [row for row in getters if re.search(r'\b(?:Rafael|Hodram|Joakim|Camille|Maria)\b', row['text'])]
    assert {row['actor_ID'] for row in focused}.issuperset({0, 1, 3})
    gallery_result = gallery_proof(source, arm, image, components)
    middle = middle_cases(arm)
    base.save(OUTPUT, dict(ROM_sha256=release['candidate_sha256'], ARM9_sha256=release['target_ARM9_sha256'],
        clean_input_sha256=release['clean_input_sha256'], glossary_sha256=base.digest(GLOSSARY),
        story_blocks_by_route=list(map(len, archives)), mapped_shared_records=len(common),
        tested_stock_name_getters=len(getters), approved_name_getters=focused,
        native_gallery=gallery_result, original_custom_name_behavior=middle, legacy_storage=storage,
        catalogue_checks={k: checked[k] for k in ('entry', 'table', 'helper_sha256', 'total_rows')},
        additional_dialogue_credit=0, new_gameplay=False, ROM_changed=False))
    print(Counter(r['spelling'] for r in storage['historical_lookup_key_records']))
    print(len(storage['retired_gallery_storage']), 'retired Gallery strings,', len(middle['result_cases']), 'middle-name cases,',
          len(gallery_result['native_bitmaps']), 'Gallery bitmaps and', len(getters), 'stock-name getters verified.')


if __name__ == '__main__':
    main()
