"""Source-owned, question-specific post-substitution wrapping for COMMON742."""

import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.script.common_native_repack import repack_native_records
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
DISPATCH = 0x01FFCE1C
TAIL = BASE + 0x151714
SLOT = (0x151714, 0x151728)
FLEET_COPY = BASE + 0x151730
OLD = '''ldr ip,[pc,#-0x3c]
eor ip,r3,ip
cmp ip,#0
cmpne ip,#0x9c
bne 0x01ffcd98
b 0x01ffcf78
nop
nop
nop'''
NEW = f'''ldr ip,[pc,#-0x3c]
eor ip,r3,ip
cmp ip,#0
cmpne ip,#0x9c
beq 0x01ffcf78
cmp ip,#0x274
ldreq ip,[sp,#0x274]
beq {TAIL}
b 0x01ffcd98'''


def wrap_question(arm):
    """Preserve all existing dispatches; add only parent53FCC / message742."""
    code = MainCodeFile(arm, BASE)
    original = [bytes(s.data) for s in code.sections]
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    lo, hi = SLOT
    source = '隊列　　　　　　　　'.encode('cp932')
    assert len(source) == hi - lo == 20
    assert clean[lo:hi] == source
    assert original[0][lo:hi] == b'Fleet\0' + bytes(14)
    assert original[0][FLEET_COPY - BASE:FLEET_COPY - BASE + 20] == b'Fleet\0' + bytes(14)
    # This entire allocation originally holds one Japanese label with spaces.
    # Rebind its sole owner to an existing identical English copy before using
    # the slot. It is not a zero-filled mutable buffer. Inspect all byte-aligned
    # pointer fields in every loaded section; reject any interior alias.
    owners = []
    for section_index, section in enumerate(code.sections):
        raw = bytes(section.data)
        for at in range(len(raw) - 3):
            value = struct.unpack_from('<I', raw, at)[0]
            if BASE + lo <= value < BASE + hi:
                assert value == BASE + lo, (section.ramAddress + at, value)
                owners.append((section_index, at))
    assert owners
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    before, after = (bytes(ks.asm(s, DISPATCH)[0]) for s in (OLD, NEW))
    stub = bytes(ks.asm('sub ip,ip,#736; cmp ip,#6; beq 0x01ffcf78; b 0x01ffcd98', TAIL)[0])
    assert len(before) == len(after) == 36 and len(stub) == 16
    offset = DISPATCH - code.sections[4].ramAddress
    assert original[4][offset:offset + 36] == before
    code.sections[4].data[offset:offset + 36] = after
    for section_index, at in owners:
        struct.pack_into('<I', code.sections[section_index].data, at, FLEET_COPY)
    code.sections[0].data[lo:hi] = stub + bytes(4)
    target = bytes(code.save())
    parsed = MainCodeFile(target, BASE)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in parsed.sections]
    restored = [bytearray(s.data) for s in parsed.sections]
    restored[0][lo:hi] = original[0][lo:hi]
    for section_index, at in owners:
        restored[section_index][at:at + 4] = original[section_index][at:at + 4]
    restored[4][offset:offset + 36] = before
    assert all(bytes(a) == b for a, b in zip(restored, original, strict=True))
    return target, {'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(target),
        'source_owned_Fleet_slot': list(SLOT),
        'unchanged_complete_Fleet_string_owner_fields': [code.sections[i].ramAddress + at for i, at in owners],
        'identical_existing_Fleet_copy': FLEET_COPY,
        'source_Japanese_hex': source.hex(), 'preserved_complete_label': 'Fleet',
        'read_only_source_owned_label_slot_code': [TAIL, TAIL + 16],
        'in_place_dispatch': [DISPATCH, DISPATCH + 36],
        'new_parent_message_pair': [0x02053FCC, 742],
        'no_section_pool_startup_allocator_cache_or_mutable_caption_growth': True,
        'native_dispatch_and_display_verification_pending': True}


def compile_template(english):
    text = english.removesuffix('{PAD}')
    if (not text or not text.isascii() or text != ' '.join(text.split())
            or any(c in text for c in '{}') or len(text) >= 200
            or text.count('%s') != 2 or '%' in text.replace('%s', '')
            or any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('One safe paragraph with exactly the source item/product substitutions required')
    return b' ' + text.encode('ascii')


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert [r['message_id'] for r in manuscript['records']] == [742]
    row = manuscript['records'][0]
    path = '/COMMON/MESFILE.DK4'
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))[742]
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)[742]
    before = common_message_entries(common, arm, clean=False)
    assert source.text == bytes.fromhex(row['source_hex']) and source.text.count(b'%s') == 2
    assert accepted.text == bytes.fromhex(row['canonical_source_hex'])
    assert before[742].text == bytes.fromhex(row['current_text_hex'])
    owner = before[742].block, before[742].record_index
    blocks = IlnkContainer.parse(common).blocks
    first = next(e for e in before if (e.block, e.record_index) == owner)
    prefix = blocks[owner[0]].split(b'\0')[owner[1]][:first.start]
    template = compile_template(row['english'])
    result = repack_native_records(common, arm, {742: template}, {owner: prefix},
        preserved_packed_neighbors={743: before[743].text}, generated_linebreaks=True,
        spare_padding_before_first_entry=True)
    target_arm, ownership = wrap_question(result.arm9)
    after = common_message_entries(result.common, target_arm, clean=False)
    for a, b in zip(before, after, strict=True):
        assert (a.message_id, a.block, a.record_index) == (b.message_id, b.block, b.record_index)
        assert b.text.rstrip(b' ') == (template if a.message_id == 742 else a.text).rstrip(b' ')
    assert all(a == b for i, (a, b) in enumerate(zip(blocks, IlnkContainer.parse(result.common).blocks, strict=True)) if i != owner[0])
    assert len(common) == len(result.common) and len(arm) == len(target_arm)
    return result.common, target_arm, {'changed_records': ['COMMON_MESSAGE_742'],
        'changed_native_offset_fields': sorted(result.changed_offsets), 'ownership': ownership,
        'all_other3667_messages_and40_other_blocks_preserved': True,
        'original_Yes_No_parent_and_other_dispatches_preserved': True,
        'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, config_path):
    config = read(config_path)
    assert config['format'] == 'dk4-specialty-question-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest
    common, arm, proof = transform(common, arm, read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, proof
