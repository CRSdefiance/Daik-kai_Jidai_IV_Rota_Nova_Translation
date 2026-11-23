"""Review the 60 outfitted ship designs and stage six readable labels."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into

from ndspy.code import MainCodeFile

from scripts import register_specialized_ship_labels_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_ship_class_names_20261115 import executable, references
from scripts.stage_specialized_ship_labels_20261115 import (
    ARM, BASE, CLEAN, GATES, class_field, design_field, source_reference,
)
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path('work/trade_and_armed_ship_labels_20261115_v1')
ROM = ROOT / 'Trade_and_Armed_Ship_Labels_RESEARCH_ONLY.nds'
OUTPUT = parent.stage.OUTPUT.with_name('trade_and_armed_ship_labels_20261115_v1.json')
REVISIONS = {
    85: ('Trade LtGall.', 'Trade Lt Galleon',
         'Give Galleon its full spelling. The 18-character design field requires a short weight qualifier. The separate class reads Light Galleon.'),
    93: ('Armed Seki', 'Armed Sekibune', 'Spell out the same Sekibune hull named in the class field.'),
    114: ('Armed HanseCog', 'Armed Hanse Cog', 'Match the word spacing of the established Hanse Cog class label.'),
    119: ('War LtGalleon', 'War Light Galleon', 'Spell out Light to distinguish this military design from War Galleon.'),
    134: ('Armed SmGalley', 'Armed Small Galley', 'Spell out Small to distinguish it from the other two armed galley sizes.'),
    136: ('Armed LgGalley', 'Armed Large Galley', 'Spell out Large to distinguish it from the other two armed galley sizes.'),
}
VERBS = {
    '商用': ('commercial', 'Trade'), '武装': ('armed', 'Armed'),
    '軍用': ('military', 'War'), '輸送用': ('transport', 'Transport'),
}
# Existing catalogue regions and their padding. Every owner in each
# region is listed in on-disk order. The adjacent retained names move only
# when sharing a packed region eliminates a size constraint.
BANKS = (
    (0x15DF73, 0x15DF84, (85,)),
    (0x15C070, 0x15C080, (93,)),
    (0x15E094, 0x15E0A4, (114,)),
    (0x15E0B4, 0x15E0D4, (118, 119)),
    (0x15E15E, 0x15E194, (130, 134, 136)),
)
NEIGHBORS = (
    (0x15DF64, 0x15DF73, b"Horace's Poems\0"),
    (0x15C068, 0x15C070, b'Lisbon\0'),
    (0x15E154, 0x15E15E, b'Lelystad\0'),
)


def review_designs(runtime, ja, arm):
    cpu, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    earlier = {row['id']: row for row in base.load(parent.REVIEW)['records']}
    design_rows = {}
    for index in range(84, 144):
        field = design_field(index)
        row = source_reference(ja, arm, cpu, field)
        klass = ja[field + 5]
        assert arm[field + 5] == klass and klass < 39
        hull = source_reference(ja, arm, cpu, class_field(klass))
        japanese, hull_source = row['clean_text'], hull['clean_text']
        prefix = next(prefix for prefix in VERBS if japanese == prefix + hull_source)
        fitting, english_prefix = VERBS[prefix]
        hull_english = hull['current']['text']
        old = row['current']['text']
        ident = f'SHIP_DESIGN_{index}'
        note = f'Keep {english_prefix} and the complete {hull_english} class wording.'
        english = old
        if index in REVISIONS:
            expected, english, note = REVISIONS[index]
            assert old == expected
        elif ident in earlier:
            assert earlier[ident]['english'] == old
            note = earlier[ident]['localization_note']
        else:
            assert old == f'{english_prefix} {hull_english}', (ident, japanese, old, hull_english)
        assert len(english.encode('ascii')) <= 18
        design_rows[index] = dict(id=ident, model_id=index, class_id=klass, Japanese=japanese, english=english,
            decision='revision' if index in REVISIONS else 'retention', speaker='Ship catalogue',
            context='Outfitted stock design, shown with the hull class in the Shipyard catalogue.',
            source_meaning=f'The {fitting} fitting of the {hull_english} hull.', localization_note=note,
            source_references=[row], hull_reference=hull,
            review=dict.fromkeys(GATES, True) | {'formatting': False},
            previous_review=str(parent.REVIEW) if ident in earlier else None)
    return design_rows


def deploy(runtime, clean, old):
    ja, arm = (image.read_file(ARM) for image in (clean, old))
    images = executable(old)
    rows = review_designs(runtime, ja, arm)
    for start, end, name in NEIGHBORS:
        assert arm[start:end].startswith(name) and not any(arm[start + len(name):end])
    target = bytearray(arm)
    storage = []
    for start, end, members in BANKS:
        refs = [rows[n]['source_references'][0] for n in members]
        pointers = [ref['current_pointer'] for ref in refs]
        assert pointers == sorted(pointers)
        owners = {ref['current_pointer']: [(ARM, ref['pointer_field'])] for ref in refs}
        assert references(images, start, end - start) == owners
        assert not any(arm[start:pointers[0] - BASE])
        for ref, next_ptr in zip(refs, pointers[1:] + [BASE + end], strict=True):
            p = ref['current_pointer'] - BASE
            before = bytes.fromhex(ref['current']['hex_with_NUL'])
            assert arm[p:next_ptr - BASE] == before.ljust(next_ptr - BASE - p, b'\0')

        cursor = start
        for index, ref in zip(members, refs, strict=True):
            row = rows[index]
            field = ref['pointer_field']
            text = row['english'].encode('ascii') + b'\0'
            assert cursor + len(text) <= end
            target[cursor:cursor + len(text)] = text
            pack_into('<I', target, field, BASE + cursor)
            row.update(target_pointer=BASE + cursor, target_hex=text.hex())
            cursor += len(text)
        target[cursor:end] = bytes(end - cursor)
        storage.append(dict(start=BASE + start, end=BASE + end, model_ids=members,
            before_hex=arm[start:end].hex(), after_hex=target[start:end].hex()))
    for index, row in rows.items():
        if 'target_pointer' not in row:
            ref = row['source_references'][0]
            row.update(target_pointer=ref['current_pointer'], target_hex=ref['current']['hex_with_NUL'])

    result = bytes(target)
    base_code, staged_code = (MainCodeFile(data, BASE) for data in (arm, result))
    assert bytes(staged_code.save()) == result
    assert [(s.ramAddress, s.bssSize, len(s.data)) for s in base_code.sections] == [
        (s.ramAddress, s.bssSize, len(s.data)) for s in staged_code.sections]
    assert all(a.data == b.data for a, b in zip(base_code.sections[1:], staged_code.sections[1:], strict=True))
    for start, end, members in BANKS:
        target[start:end] = arm[start:end]
        for index in members:
            field = design_field(index)
            target[field:field + 4] = arm[field:field + 4]
    assert bytes(target) == arm
    return result, list(rows.values()), storage


def main():
    assert not ROM.exists() and not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean, old = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(old)
    arm, rows, storage = deploy(runtime, clean, old)
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
        records=rows, owned_banks=storage, research_ROM=str(ROM), clean_input_sha256=release['clean_input_sha256'],
        whole_parent_inverse_exact=True, changed_internal_files=[ARM], new_dialogue_credit=0,
        display_checks_pending=True, new_gameplay_runs=0, registered=False))
    print(f'Staged {len(REVISIONS)} design revisions and recorded {len(rows) - len(REVISIONS)} retentions.')


if __name__ == '__main__':
    main()
