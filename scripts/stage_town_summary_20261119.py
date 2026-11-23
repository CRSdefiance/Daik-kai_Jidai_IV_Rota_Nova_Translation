"""Restore the full Town Summary status heading in its native text atlas."""

from itertools import combinations
from struct import pack, pack_into, unpack_from

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import observe_town_summary_20261119 as observe
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime

parent = observe.current
base, native = parent.base, parent.native
ARM, COMMON, CLEAN, PENDING = (getattr(parent.stage, key) for key in ('ARM', 'COMMON', 'CLEAN', 'PENDING'))
ROOT = observe.ROOT / 'staged_v1'
ROM, PROOF = ROOT / 'Town_Summary_STAGED.nds', ROOT / 'staged.json'
RELEASE = PROOF
TRACE = observe.ROOT / 'baseline_v2' / 'requests.json'
BASE = 0x02000000
TEXT, POINTER, LAYOUT = 0x15692C, 0xB6414, 0x11A65C
ATLAS = (228, 72)
CAPTIONS = (
    ('種類', 'Type', 'Type', 'The settlement category shown as City or Port. Type is concise and clear above the value.'),
    ('状態', 'Stat', 'Status', 'Status labels the current condition, such as Normal, and matches the Market Trade wording.'),
    ('発展度', 'Growth', 'Growth', 'The settlement development score. Growth is short and readable above the number.'),
    ('武装度', 'Arms', 'Arms', 'The settlement armament score. Arms describes what the number measures in the available heading space.'),
)


def rectangles(arm):
    return [unpack_from('<7i', arm, LAYOUT + i * 28) for i in range(21)]


def validate_rectangles(rows):
    boxes = []
    for _, dx, dy, sx, sy, width, height in rows:
        assert width >= 0 and height >= 0
        assert 0 <= sx <= sx + width <= ATLAS[0] and 0 <= sy <= sy + height <= ATLAS[1]
        assert 0 <= dx <= dx + width <= 256 and 0 <= dy <= dy + height <= 192
        if width and height:
            boxes.append((sx, sy, sx + width, sy + height))
    for (x0, y0, x1, y1), (a0, b0, a1, b1) in combinations(boxes, 2):
        assert x1 <= a0 or a1 <= x0 or y1 <= b0 or b1 <= y0
    return len(boxes)


def transform(clean, arm, trace):
    ordered = rectangles(arm)
    draw = observe.RETURN - BASE - 4
    assert clean[draw-20:draw+4] == arm[draw-20:draw+4]
    assert arm[draw:draw+4] == bytes.fromhex('ba7c00eb')
    pointer = pack('<I', BASE + TEXT)
    assert [i for i in range(0, len(arm)-3, 4) if arm[i:i+4] == pointer] == [POINTER]
    assert clean[POINTER:POINTER+4] == pointer
    assert trace['pointer'] == BASE + TEXT and trace['layout_pointer'] == BASE + LAYOUT
    assert bytes.fromhex(trace['layout_hex']) == arm[LAYOUT:LAYOUT+0x200]
    assert trace['caller_LR'] == observe.RETURN and tuple(trace['clip_rect']) == (0, 0, *ATLAS)
    assert trace['cursor'] == [84, 60] and bytes.fromhex(trace['text_hex']) == arm[TEXT:TEXT+24]
    source = ''.join(row[0] for row in CAPTIONS).encode('cp932')
    current = ''.join(row[1] for row in CAPTIONS).ljust(20).encode('ascii')
    target = ''.join(row[2] for row in CAPTIONS).encode('ascii')
    assert len(source) == len(current) == len(target) == 20
    assert clean[TEXT:TEXT+24] == source + bytes(4) and arm[TEXT:TEXT+24] == current + bytes(4)
    assert ordered[-4:] == rectangles(clean)[-4:]

    result = bytearray(arm)
    result[TEXT:TEXT+20] = target
    previous, revised, japanese, new_x = 0, 0, 0, 84
    records = []
    for i, (jp, old, new, note) in enumerate(CAPTIONS):
        descriptor = LAYOUT + (17 + i) * 28
        row = ordered[17 + i]
        width = max(row[5], 6 * len(new))
        pack_into('<i', result, descriptor + 12, new_x)
        pack_into('<i', result, descriptor + 20, width)
        source_length = len(jp.encode('cp932'))
        source_ref = dict(string_offset=TEXT+japanese, length=source_length, descriptor_offset=descriptor, draw=BASE+draw)
        current_ref = dict(string_offset=TEXT+previous, length=len(old), descriptor_offset=descriptor, draw=BASE+draw)
        target_ref = dict(string_offset=TEXT+revised, length=len(new), descriptor_offset=descriptor, draw=BASE+draw)
        records.append(dict(id=f'TOWN_SUMMARY_HEADING_{i}', file_path=ARM, speaker='Town Summary',
            context='Town Summary shows the settlement type, status, growth and armament above their current values.',
            clean_Japanese=jp, source_meaning=note.split('. ', 1)[0], previous_English=old, english=new, localization_note=note,
            decision='revision' if old != new else 'retention', source_reference=source_ref, current_reference=current_ref,
            staged_reference=target_ref, source_hex=source[japanese:japanese+source_length].hex(),
            current_hex=current[previous:previous+len(old)].hex(), staged_hex=target[revised:revised+len(new)].hex(),
            original_geometry=row, staged_geometry=unpack_from('<7i', result, descriptor),
            review=dict.fromkeys(REQUIRED_REVIEW_GATES, True)))
        japanese += source_length
        previous += len(old)
        revised += len(new)
        new_x += 6 * len(new)

    assert validate_rectangles(ordered) == validate_rectangles(rectangles(result)) == 16
    assert new_x <= ATLAS[0] and result[TEXT+20:TEXT+24] == bytes(4)
    inverse = bytearray(result)
    inverse[TEXT:TEXT+20] = arm[TEXT:TEXT+20]
    inverse[LAYOUT+17*28:LAYOUT+21*28] = arm[LAYOUT+17*28:LAYOUT+21*28]
    assert bytes(inverse) == arm
    return bytes(result), records


def main():
    assert not ROOT.exists()
    previous, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(parent.ROM) == previous['candidate_sha256'] == ledger['current_integrated_candidate']['sha256']
    assert base.digest(base.REGISTRY) == previous['registry_sha256']
    dependencies = (TRACE, TRACE.parent/'source_contract.json', TRACE.parent/'capture/capture_report.json')
    trace, report = map(base.load, (TRACE, dependencies[-1]))
    assert report['ROM_sha256'] == previous['candidate_sha256'] and report['cold_boot'] and not report['savestate_loaded']
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    observed, = trace['rows']
    image, clean = map(base.NdsImage.open, (parent.ROM, CLEAN))
    arm = image.read_file(ARM)
    target, records = transform(clean.read_file(ARM), arm, observed)
    verify_runtime(target, previous)
    image.replace_file(ARM, target)
    data = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    review = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=sorted(REQUIRED_REVIEW_GATES), candidate_sha256=native.digest(data), records=records)
    validate_natural_dialogue_batch(review)
    assert base.digest(CLEAN) == previous['clean_input_sha256']
    ROOT.mkdir()
    ROM.write_bytes(data)
    base.save(PROOF, review | dict(parent_sha256=previous['candidate_sha256'], clean_input_sha256=previous['clean_input_sha256'],
        entire_parent_inverse=True, atlas_bound=ATLAS, atlas_rectangles=16, target_ARM9_sha256=native.digest(target),
        source_proofs={str(p): base.digest(p) for p in (*dependencies, TRACE.parent/'terminal.json')}))
    print('Staged the full Status heading, with three retained labels and 16 disjoint atlas regions.')


if __name__ == '__main__':
    main()
