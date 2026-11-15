"""Compile four clean-source chooser biographies and replay the original screens."""

import argparse
import hashlib
import re
import struct
import sys
from itertools import combinations
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from dk4tool.graphics.fls import FlsArchive
from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.run_all_captain_chooser_v691 import STATES
from scripts.seal_shared_text_source_v1 import ARM
from scripts.stage_sera_assignment_review_v1 import OUTPUT as PARENT_ROOT


BASE = 0x02000000
TABLE = 0x14FC04
STORAGE = (0x14FD7C, 0x14FF24)
CALLER = (0x9E740, 0x9E768)
WIDTH = 39
HEIGHT = 3
ROOT = Path('out/captain_biographies_20261111_v1')
ROM = ROOT / 'captain_biographies_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PRIOR = PARENT_ROOT / 'own_startup'
INVENTORY = Path('translations/editorial_checkpoints/SharedText_20261110_v1/captain_biographies_source_current_inventory.json')
MAIN = Path('translations/promoted_build.json')
REGISTRY = Path('translations/release_stack.json')

DECISIONS = {
    'Rafael': (
        "A Portuguese boy dreams of the sea. A friend talks him into setting sail. Great for first-time players.",
        "A Portuguese boy vaguely dreams of being a sailor. A friend persuades him to go to sea. Recommended for people playing for the first time.",
        "Retain the boy's quiet dream of the sea and the advice for beginners. The friend talks him into setting sail, without assigning a worldwide itinerary to the friend's suggestion.",
        ('setting sail', 'first-time players'),
    ),
    'Hodram': (
        "Sweden is free again. Its admiral leads a navy in name only and aims to make his privateers second to none.",
        "Sweden has regained independence. Its admiral leads a privateering fleet that is a navy only in name and works to make his country's fleet the strongest in the world.",
        "Restore the regained independence and the gulf between the title of navy and the privateers he actually leads. 'Second to none' expresses his ambition for the fleet in the same brisk third-person voice.",
        ('navy in name only', 'privateers second to none', 'to make'),
    ),
    'Lil': (
        "A Dutch girl sails the world to make her name in trade with Camille, her childhood friend and partner.",
        "An enterprising Dutch girl takes to the seas of the world to make her mark alongside her childhood friend and partner Camille.",
        "Keep her Dutch origin and worldwide ambitions. The goal of making her name in trade expresses her entrepreneurial drive. Restore that Camille is also her partner, retaining the approved name and childhood friendship.",
        ('sails the world', 'make her name in trade', 'childhood friend and partner'),
    ),
    'Maria': (
        "Defying the law on isolation, a Ming admiral leads her own fleet to protect people from wokou raids.",
        "To protect the people suffering under wokou raids, a woman admiral of the Ming deliberately defies the country's isolation law and leads her private fleet into the fight.",
        "Keep the existing motivation and her own fleet, linking both to her defiance of the law. Use the source term 'wokou' with 'raids' for context and retain the Ming identity and naval rank.",
        ('law on isolation', 'Ming admiral', 'her own fleet', 'wokou raids'),
    ),
}


def format_biography(text, protected):
    """Choose three complete-word rows using the chooser's measured cell budget."""
    assert re.fullmatch(r"[ -~]+", text) and text == ' '.join(text.split())
    assert '%' not in text and all(text.count(phrase) == 1 for phrase in protected)
    spans = [match.span() for match in re.finditer(r' ', text)]
    options = []
    for first, second in combinations((start for start, _ in spans), HEIGHT - 1):
        if any(text.index(phrase) < split < text.index(phrase) + len(phrase)
               for phrase in protected for split in (first, second)):
            continue
        lines = (text[:first], text[first + 1:second], text[second + 1:])
        lengths = [len(line) for line in lines]
        if max(lengths) > WIDTH or min(lengths) < 20:
            continue
        weak = sum(re.search(r"\b(a|an|the|and|its|her|his|to|at|of|for|with|in|on)$", line) is not None
                   for line in lines[:-1])
        strength = sum(3 if line.endswith('.') else 2 if line.endswith(',') else 0
                       for line in lines[:-1])
        options.append(((weak, -strength, max(lengths) - min(lengths), first, second), lines))
    assert options, text
    return min(options)[1]


def pointer_owners(image, arm):
    """Locate direct pointers into the complete four-bio range, including interiors."""
    pattern = re.compile(rb'(?=(.[\xfd-\xff]\x14\x02))', re.DOTALL)
    low, high = (BASE + offset for offset in STORAGE)
    owners = []
    regions = [(ARM, arm), ('/__arm7__.bin', image.read_file('/__arm7__.bin'))]
    regions.extend((path, data) for _, path, data in image.iter_files())
    regions.extend((f'ARM9 overlay {n}', section.data) for n, section in image.rom.loadArm9Overlays().items())
    regions.extend((f'ARM7 overlay {n}', section.data) for n, section in image.rom.loadArm7Overlays().items())
    for path, data in regions:
        for match in pattern.finditer(data):
            address, = struct.unpack('<I', match.group(1))
            if low <= address < high:
                owners.append([path, match.start(), address])
    return owners


def references(raw, source_rows, original):
    for row in source_rows:
        at, size = row['ARM9_offset'], row['capacity']
        assert raw[at:at + size] == bytes.fromhex(row['clean_hex' if original else 'current_hex'])
        assert raw[at + size] == row['original_delimiter']
    start = source_rows[0]['ARM9_offset']
    end = source_rows[-1]['ARM9_offset'] + source_rows[-1]['capacity'] + 1
    payload = raw[start:end]
    return dict(ARM9_offset=start, runtime_address=BASE + start, byte_count=len(payload),
                exact_hex=payload.hex(), text=payload[:-1].decode('cp932' if original else 'ascii'))


def rebuild(parent, clean, inventory):
    arm, original = parent.read_file(ARM), clean.read_file(ARM)
    first, last = CALLER
    assert arm[first:last] == original[first:last]
    assert hashlib.sha256(arm[first:last]).hexdigest() == inventory['source_current_consumer_span_sha256']
    assert struct.unpack_from('<I', arm, 0x9E76C)[0] == BASE + TABLE
    assert struct.unpack_from('<I', original, 0x9E76C)[0] == BASE + TABLE
    original_addresses = [row['original_data_pointer'] for row in inventory['records']]
    expected = [[ARM, TABLE + 4 * index, address] for index, address in enumerate(original_addresses)]
    matches = pointer_owners(parent, arm)
    assert matches == pointer_owners(clean, original)
    assert [match for match in matches if match[0] == ARM] == expected
    asset_matches = [match for match in matches if match[0] != ARM]
    for path, offset, _ in asset_matches:
        for image in (parent, clean):
            asset = image.read_file(path)
            if path == '/data/WORLDMAP.DK4':
                assert asset[:4] == b'ILNK' and offset >= struct.unpack_from('<I', asset, 8)[0]
            else:
                assert path.startswith('/FLS/') and offset >= FlsArchive(asset).data_offset
    low, high = STORAGE
    assert arm[high:high + 4] == original[high:high + 4] == bytes.fromhex('48090000')
    rows = []
    out = bytearray(arm)
    out[low:high] = bytes(high - low)
    records = sorted(inventory['records'], key=lambda row: row['original_data_pointer'])
    cursor = low
    old_ends = [row['original_data_pointer'] - BASE for row in records[1:]] + [high]
    for row, old_end in zip(records, old_ends, strict=True):
        actor = row['actor']
        text, meaning, note, protected = DECISIONS[actor]
        index = row['chooser_index']
        assert row['source_pointer_field'] == BASE + TABLE + 4 * index
        clean_ref, current_ref = (references(raw, row['existing_source_rows'], is_clean)
                                  for raw, is_clean in ((original, True), (arm, False)))
        for ref, raw in ((clean_ref, original), (current_ref, arm)):
            assert ref['runtime_address'] == row['original_data_pointer']
            assert not any(raw[ref['ARM9_offset'] + ref['byte_count']:old_end])
        lines = format_biography(text, protected)
        payload = '\n'.join(lines).encode('ascii') + b'\0'
        assert payload.count(b'\0') == 1 and payload.count(b'\n') == 2
        assert cursor % 4 == 0 and cursor + len(payload) <= high
        out[cursor:cursor + len(payload)] = payload
        struct.pack_into('<I', out, TABLE + 4 * index, BASE + cursor)
        rows.append(dict(id=f'CAPTAIN_BIOGRAPHY_{actor.upper()}', actor=actor, speaker='New Game chooser',
            file_path=ARM, chooser_index=index, source_reference=clean_ref, current_reference=current_ref,
            source_line_references=row['existing_source_rows'], context='Independent introduction shown alongside the selected captain, portrait, name fields, and route selection prompt.',
            source_meaning=meaning, localization_note=note, english=text, decision='revision',
            preserved_controls=['original selection index and call', 'two LF row delimiters', 'NUL terminator'],
            runtime_substitutions=[], protected_phrases=protected,
            review={gate: gate != 'formatting' for gate in sorted(REQUIRED_REVIEW_GATES)},
            staged_reference=dict(ARM9_offset=cursor, runtime_address=BASE + cursor,
                                  pointer_field=BASE + TABLE + index * 4, byte_count=len(payload), exact_hex=payload.hex()),
            staged_rows=lines, row_width_pixels=[6 * len(line) for line in lines]))
        cursor = (cursor + len(payload) + 3) & ~3
    assert cursor <= high
    assert out[:TABLE] == arm[:TABLE] and out[TABLE + 16:low] == arm[TABLE + 16:low]
    assert out[high:] == arm[high:]
    for row in rows:
        ref = row['staged_reference']
        at = struct.unpack_from('<I', out, ref['pointer_field'] - BASE)[0] - BASE
        assert at == ref['ARM9_offset']
        assert out[at:at + ref['byte_count']] == bytes.fromhex(ref['exact_hex'])
    return bytes(out), sorted(rows, key=lambda row: row['chooser_index']), expected, asset_matches


def stage():
    inventory = load(INVENTORY)
    parent_path, clean_path = (Path(inventory[key]) for key in ('current_ROM', 'clean_ROM'))
    for key, path in (('current_ROM', parent_path), ('clean_ROM', clean_path), ('source_profile', inventory['source_profile'])):
        assert digest(path) == inventory[key + '_sha256']
    parent, clean = NdsImage.open(parent_path), NdsImage.open(clean_path)
    old_arm = parent.read_file(ARM)
    arm, rows, owners, asset_matches = rebuild(parent, clean, inventory)
    parent.replace_file(ARM, arm)
    candidate = bytes(parent.rom.save())
    parent.replace_file(ARM, old_arm)
    assert bytes(parent.rom.save()) == parent_path.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    assert NdsImage.open(ROM).read_file(ARM) == arm
    save(PROOF, dict(research_ROM=str(ROM), research_ROM_sha256=digest(ROM), changed_components=[ARM],
        changed_internal_files=[], registered_input=dict(candidate=str(parent_path), candidate_sha256=digest(parent_path)),
        clean_ROM=str(clean_path), clean_ROM_sha256=digest(clean_path), registry_sha256=digest(REGISTRY),
        promoted_sha256=digest(MAIN), inventory_sha256=digest(INVENTORY), producer_sha256=digest(__file__),
        parent_inverse_exact=True, old_direct_pointer_owners=owners, unchanged_asset_payload_matches=asset_matches,
        owned_ARM9_offsets=[(TABLE, TABLE + 16), STORAGE],
        candidate_ARM9_sha256=hashlib.sha256(arm).hexdigest(), records=rows))
    print(f'Stored four biographies; {digest(ROM)}', flush=True)


def replay(case):
    staged = load(PROOF)
    parent = load(PRIOR / 'capture/capture_report.json')
    assert parent['ROM_sha256'] == staged['registered_input']['candidate_sha256']
    assert digest(ROM) == staged['research_ROM_sha256']
    if case == 'startup':
        env = {**vars(startup), 'EVIDENCE': PROOF, 'ROM': ROM, 'STARTUP': ROOT / 'own_startup', 'PRIOR': PRIOR}
        FunctionType(startup.main.__code__, env)()
        return
    path = Path(staged['registered_input']['candidate']) if case == 'parent' else ROM
    out = ROOT / case
    out.mkdir()
    args = load(PRIOR / 'worker_argv.json')
    key = '--gallery-save-fixture-manifest'
    fixture = load(args[args.index(key) + 1])
    assert fixture['production_ROM_sha256'] == parent['ROM_sha256']
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']
    manifest = out / 'unlock_manifest.json'
    save(manifest, fixture | dict(production_ROM=str(path), production_ROM_sha256=digest(path),
        current_test_scope='Original New Game chooser and seven controller-only selections with the existing system unlock.'))
    inputs = [{'start': frame, 'duration': 8, 'buttons': [button]}
              for frame, button in ((1601, 'START'), (2001, 'DOWN'), (2401, 'A'),
                                    (2801, 'RIGHT'), (3201, 'RIGHT'), (3601, 'RIGHT'),
                                    (4001, 'LEFT'), (4401, 'LEFT'), (4801, 'LEFT'), (5201, 'B'))]
    save(out / 'inputs.json', inputs)
    sys.argv = [sys.argv[0], '--rom', str(path), '--out', str(out / 'capture'),
        '--frames', '5550', '--inputs-json', str(out / 'inputs.json'),
        '--battery-save', fixture['fixture_save'], '--allow-gallery-fixtures',
        '--gallery-save-fixture-manifest', str(manifest), '--capture-every', '999999',
        '--capture-at', '2200', *[str(frame) for frame, _ in STATES], '5500', '--dump-capture-ram', '--dump-ram']
    harness.main()
    assert digest(fixture['fixture_save']) == fixture['fixture_save_sha256']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('stage', 'parent', 'candidate', 'startup'))
    args = parser.parse_args()
    stage() if args.action == 'stage' else replay(args.action)
