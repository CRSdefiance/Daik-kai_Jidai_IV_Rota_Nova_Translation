"""Review specialized ship names and stage owned class and design fields."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from scripts import register_market_trade_dialogue_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_source_item_cards_and_coin_v1 import GETTER, POOL
from scripts.stage_ship_class_names_20261115 import executable, references
from scripts.stage_special_target_labels_20261115 import c_string, native_layout
from scripts.verify_release_baseline import files


base = parent.base
BASE, ARM, CLEAN = 0x02000000, parent.stage.ARM, parent.stage.CLEAN
ROOT = Path('work/specialized_ship_labels_20261115_v1')
ROM = ROOT / 'Specialized_Ship_Labels_RESEARCH_ONLY.nds'
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/specialized_ship_labels_20261115_v1.json')
NAGASAKI_MUSEUM = 'https://jmapps.ne.jp/nmhc_public/det.html?data_id=30343'
RMG = 'https://www.rmg.co.uk/collections/library/rmgl-152988'
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
BANK = (0x0238C58C, 0x0238C5C4)


def class_field(index):
    return 0x11C7A8 + 56 * index


def design_field(index):
    return 0x11D030 + 44 * (index - 50)


REVISIONS = (
    ('SHIP_CLASS_NAME_15', (class_field(15), design_field(65)), '戦列艦', 'Ship of the Line',
     'Standard hull and design. Use the established English term for a ship built to fight in the line of battle.', None),
    ('SHIP_CLASS_NAME_32', (class_field(32), design_field(82)), '末次船', 'Suetsugu',
     'Standard hull and design. The clean label names the Suetsugu type. Use the museum’s reading of 末次 and restore the missing English on the design.', 12),
    ('SHIP_DESIGN_89', (design_field(89),), '商用末次船', 'Trade Suetsugu',
     'Commercial design of the Suetsugu. Preserve the Trade designation and the recognizable class name.', None),
    ('SHIP_DESIGN_95', (design_field(95),), '武装末次船', 'Armed Suetsugu',
     'Armed design of the Suetsugu. Preserve the specific armed qualifier and use the complete class name.', None),
    ('SHIP_DESIGN_101', (design_field(101),), '輸送用戦列艦', 'Cargo Line Ship',
     'Transport design of the line ship. Cargo identifies its transport configuration in the catalogue. Line Ship is the compact form of the full hull label.', 16),
    ('SHIP_DESIGN_106', (design_field(106),), '輸送用ガレー', 'Cargo Galley',
     'Transport design of the ordinary galley. Name the complete hull to distinguish this design from the Galleass and Large Galley.', 16),
    ('SHIP_DESIGN_107', (design_field(107),), '輸送用大型ガレー', 'Large Cargo Galley',
     'Transport design of the large galley. Retain the size qualifier in full and match the other cargo galley labels.', 20),
    ('SHIP_DESIGN_108', (design_field(108),), '輸送用ガレアス', 'Cargo Galleass',
     'Transport design of the galleass. The whole class name distinguishes it from the ordinary Cargo Galley.', 16),
    ('SHIP_DESIGN_113', (design_field(113),), '輸送用鉄甲船', 'Cargo Ironclad',
     'Transport design of the Ironclad. Use the full established game class label with the fitting designation.', 16),
    ('SHIP_DESIGN_129', (design_field(129),), '軍用戦列艦', 'War Line Ship',
     'Military design of the line ship. Keep the catalogue’s War qualifier and separate the words in the short hull name.', 16),
)
RETAINS = (
    ('SHIP_CLASS_NAME_21', (class_field(21), design_field(71)), 'ガレー', 'Galley',
     'The unqualified Galley distinguishes this hull from the two size variants and the Galleass.'),
    ('SHIP_CLASS_NAME_22', (class_field(22), design_field(72)), '大型ガレー', 'Large Galley',
     'The complete size qualifier matches the ordinary hull and its separate cargo counterpart.'),
    ('SHIP_CLASS_NAME_23', (class_field(23), design_field(73)), 'ガレアス', 'Galleass',
     'The established class term distinguishes this hull from the three Galley sizes.'),
    ('SHIP_DESIGN_99', (design_field(99),), '輸送用コルベット', 'Transport Corvette',
     'The full designation identifies both the transport purpose and the distinct Corvette hull.'),
    ('SHIP_DESIGN_100', (design_field(100),), '輸送用フリゲート', 'Transport Frigate',
     'The complete label identifies the transport purpose and the Frigate hull.'),
    ('SHIP_DESIGN_135', (design_field(135),), '武装ガレー', 'Armed Galley',
     'The complete qualifier marks the armed standard galley, distinct from the Cargo Galley.'),
    ('SHIP_DESIGN_137', (design_field(137),), '軍用ガレアス', 'War Galleass',
     'Keep the military designation and the complete hull name.'),
)


def source_reference(ja, arm, cpu, field):
    source, active = (unpack_from('<I', blob, field)[0] for blob in (ja, arm))
    offset = source - BASE
    text = ja[offset:ja.index(b'\0', offset) + 1]
    return dict(file_path=ARM, pointer_field=field, clean_pointer=source, current_pointer=active,
                clean_text=text[:-1].decode('cp932'), clean_hex=text.hex(),
                current=c_string(cpu, active, 'cp932'))


def free_bank(images, code):
    start, end = BANK
    payload = bytes(code.sections[3].data[:-48])
    active = unpack_from('<I', payload, GETTER - POOL + 44)[0]
    pointers = unpack_from('<218I', payload, active - POOL)
    # The interval begins after the final item still stored in the retired
    # pointer table. It ends at the first instruction of the active getter.
    assert POOL + payload.index(b'\0\0', pointers[46] - POOL) + 2 == 0x0238C589
    assert all(not 0x0238C589 <= p < end for p in pointers)
    assert all(p >= active or payload.index(b'\0\0', p - POOL) + 2 <= start - POOL
               for p in pointers if POOL <= p < start)
    assert end == GETTER and not references(images, start - BASE, end - start)


def update_storage(code, address, text, extent):
    if address >= POOL:
        data, at = code.sections[3].data, address - POOL
    else:
        data, at = code.sections[0].data, address - BASE
    assert at >= 0 and at + extent <= len(data) and len(text) <= extent
    old = bytes(data[at:at + extent])
    data[at:at + extent] = text.ljust(extent, b'\0')
    return old


def stage(runtime, clean, old):
    arm, ja = (image.read_file(ARM) for image in (old, clean))
    images = executable(old)
    cpu, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    code = MainCodeFile(arm, BASE)
    free_bank(images, code)
    rows, inverses = [], []
    next_free = BANK[0]
    for ident, fields, jp, english, reason, extent in REVISIONS:
        refs = [source_reference(ja, arm, cpu, field) for field in fields]
        assert all(ref['clean_text'] == jp for ref in refs)
        data = english.encode('ascii') + b'\0'
        assert len(data) <= 19
        if extent is None:
            address, extent = next_free, len(data)
            next_free += extent
            assert next_free <= BANK[1]
        else:
            address = refs[0]['current_pointer']
            original = bytes.fromhex(refs[0]['current']['hex_with_NUL'])
            assert len(original) <= extent
            assert bytes(cpu.mem_read(address, extent)) == original.ljust(extent, b'\0')
            owners = [(ARM, ref['pointer_field']) for ref in refs if ref['current_pointer'] == address]
            assert references(images, address - BASE, extent) == {address: owners}
        inverses.append((address, update_storage(code, address, data, extent)))
        for ref in refs:
            pack_into('<I', code.sections[0].data, ref['pointer_field'], address)
        extras = dict(sea_inspection_format=native_layout(arm, 'Pirates', english)) if len(fields) > 1 else {}
        citations = [RMG] if ident == 'SHIP_CLASS_NAME_15' else [NAGASAKI_MUSEUM] if 'Suetsugu' in english else []
        rows.append(dict(id=ident, Japanese=jp, english=english, decision='revision',
            context='Shipyard class or design catalogue', source_meaning=reason, localization_note=reason,
            source_references=refs, target_pointer=address, target_hex=data.hex(), external_references=citations,
            review=dict.fromkeys(GATES, True) | {'formatting': False}, **extras))
    target = bytes(code.save())
    for row in rows:
        for ref in row['source_references']:
            pack_into('<I', code.sections[0].data, ref['pointer_field'], ref['current_pointer'])
    for address, contents in inverses:
        update_storage(code, address, contents, len(contents))
    assert bytes(code.save()) == arm

    for ident, fields, jp, english, reason in RETAINS:
        refs = [source_reference(ja, arm, cpu, field) for field in fields]
        assert all(ref['clean_text'] == jp and ref['current']['text'] == english for ref in refs)
        rows.append(dict(id=ident, Japanese=jp, english=english, decision='retention',
                         context='Adjacent Shipyard catalogue labels', source_meaning=reason, localization_note=reason,
                         source_references=refs, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    return target, rows


def main():
    assert not ROM.exists() and not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean, old = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(old)
    arm, rows = stage(runtime, clean, old)
    verify_runtime(arm, release)
    old.replace_file(ARM, arm)
    after = files(old)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {ARM}
    ROOT.mkdir(parents=True)
    old.save(ROM)
    old.replace_file(ARM, before[ARM])
    assert bytes(old.rom.save()) == parent.ROM.read_bytes()
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, candidate_sha256=base.digest(ROM),
        previous_sha256=release['candidate_sha256'], target_ARM9_sha256=sha256(arm).hexdigest(),
        records=rows, research_ROM=str(ROM), clean_input_sha256=release['clean_input_sha256'],
        whole_parent_inverse_exact=True, changed_internal_files=[ARM], new_dialogue_credit=0,
        display_checks_pending=True, new_gameplay_runs=0, registered=False))
    print(f'Staged {len(REVISIONS)} name changes. Recorded {len(RETAINS)} individual retentions.')


if __name__ == '__main__':
    main()
