"""Expand three standard ship names in their original class and design records."""

from hashlib import sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy.code import MainCodeFile

from scripts import register_special_target_labels_20261115 as parent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.stage_special_target_labels_20261115 import native_layout
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path('work/ship_class_label_review_20261115_v1')
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
ROM, STORED = ROOT / 'Ship_Class_Names_RESEARCH_ONLY.nds', ROOT / 'staged.json'
BASE = 0x02000000
BANK = 0x15D484
SLOT_SIZE = 16
RETIRED = (
    ('カップル女', 0x122020, 0x02387E7C),
    ('イベント用', 0x1221A4, 0x02387F78),
    ('ヨーロッパ', 0x122004, 0x02387DE0),
    ('新羅の金冠', 0x11EEE8, 0x0215E520),
)
RECORDS = (
    (5, 0x11C8C0, 0x15D2F8, 0x11D10C, 0x15D4FC, '軽ガレオン', 'Lt Galleon', 'Light Galleon'),
    (20, 0x11CC08, 0x15D3AC, 0x11D3A0, 0x15CA58, '小型ガレー', 'Sm Galley', 'Small Galley'),
    (22, 0x11CC78, 0x15D3C4, 0x11D3F8, 0x15CA94, '大型ガレー', 'Lg Galley', 'Large Galley'),
)


def references(images, start, size):
    """Find literal references to every byte of the bank, including interior addresses."""
    result = {}
    for addr in range(BASE + start, BASE + start + size):
        needle = addr.to_bytes(4, 'little')
        matches = []
        for name, raw in images.items():
            offset = raw.find(needle)
            while offset >= 0:
                matches.append((name, offset))
                offset = raw.find(needle, offset + 1)
        if matches:
            result[addr] = matches
    return result


def digest(raw):
    return sha256(raw).hexdigest()


def executable(rom):
    sections = {ARM: rom.read_file(ARM), '/__arm7__.bin': rom.rom.arm7}
    for cpu, overlays in (('arm9', rom.rom.loadArm9Overlays()), ('arm7', rom.rom.loadArm7Overlays())):
        sections.update({f'{cpu} overlay {i}': overlay.data for i, overlay in overlays.items()})
    return sections


def owned_patch(clean_rom, current_rom):
    source, current = map(executable, (clean_rom, current_rom))
    clean, arm = source[ARM], current[ARM]
    size = len(RECORDS) * SLOT_SIZE
    bank_source = b''.join(label.encode('cp932').ljust(12, b'\0') for label, _, _ in RETIRED)
    assert len(bank_source) == size and clean[BANK:BANK + size] == arm[BANK:BANK + size] == bank_source
    source_owners = {BASE + BANK + 12 * i: [(ARM, owner)] for i, (_, owner, _) in enumerate(RETIRED)}
    assert references(source, BANK, size) == source_owners
    assert not references(current, BANK, size)
    assert all(unpack_from('<I', arm, owner) == (p,) for _, owner, p in RETIRED)
    target = bytearray(arm)
    records = []
    for i, (class_id, class_field, class_slot, design_field, design_slot, jp, old, name) in enumerate(RECORDS):
        assert class_field == 0x11C7A8 + 56 * class_id
        at = BANK + SLOT_SIZE * i
        desired = name.encode('ascii') + b'\0'
        assert len(desired) <= SLOT_SIZE
        target[at:at + SLOT_SIZE] = desired.ljust(SLOT_SIZE, b'\0')
        fields = []
        for consumer, field, slot in (('class', class_field, class_slot), ('stock design', design_field, design_slot)):
            assert unpack_from('<I', arm, field) == unpack_from('<I', clean, field) == (BASE + slot,)
            actual_source = clean[slot:slot + 12]
            actual_current = arm[slot:slot + 12]
            assert actual_source == jp.encode('cp932').ljust(12, b'\0')
            assert actual_current == old.encode('ascii').ljust(12, b'\0')
            pack_into('<I', target, field, BASE + at)
            fields.append(dict(consumer=consumer, file_path=ARM, pointer_field=field, source_offset=slot,
                Japanese=jp, clean_hex=actual_source.hex(), previous=old, previous_hex=actual_current.hex(),
                target_offset=at, english=name, target_hex=desired.hex()))
        records.append(dict(id=f'SHIP_CLASS_NAME_{class_id}', class_id=class_id, source_references=fields,
            Japanese=jp, english=name, decision='revision', context='Standard ship design and hull class',
            localization_note=f'Write out the Japanese size or weight qualifier in {old} without changing the hull type.',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            sea_inspection_format=native_layout(arm, 'Pirates', name)))
    deployed = bytes(target)
    previous, changed = (MainCodeFile(data, BASE) for data in (arm, deployed))
    assert [(s.ramAddress, len(s.data)) for s in previous.sections] == [(s.ramAddress, len(s.data)) for s in changed.sections]
    assert bytes(changed.save()) == deployed
    for record in records:
        for ref in record['source_references']:
            pack_into('<I', target, ref['pointer_field'], BASE + ref['source_offset'])
    target[BANK:BANK + size] = bank_source
    assert bytes(target) == arm
    return deployed, records


def main():
    assert not ROM.exists() and not STORED.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, rom = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(rom)
    arm, records = owned_patch(clean, rom)
    verify_runtime(arm, release)
    rom.replace_file(ARM, arm)
    after = files(rom)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {ARM}
    ROOT.mkdir(parents=True, exist_ok=True)
    rom.save(ROM)
    rom.replace_file(ARM, before[ARM])
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(candidate_sha256=base.digest(ROM), previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), records=records, allocation_offset=BANK,
        allocation_size=SLOT_SIZE * len(RECORDS), whole_parent_inverse=True))
    print('Staged three full names and six owned pointers. Verified each complete sea-inspection format and parent inverse.')


if __name__ == '__main__':
    main()
