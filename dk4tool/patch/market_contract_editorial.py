"""Market advice and complete contract-location prose without executable growth."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
IDS = tuple(range(754, 762))
GOV = 0x02157064
INVESTMENT = GOV + 20
PALACE = 0x02143E12
PORT = 0x0214466E
TARGET = 0x0215FA25
DISPATCH = GOV + 32
REGION = b'Govt\0\0\0\0Palace\0\0Investment\0\0Port\0\0\0\0Target\0\0'
NAMES = ("Governor's Office", 'Palace')
DIRECTORY = 'daa82ab9ba0f0df082939785923c98279cc546dce2b5faa2edfc5825fe2c9a47'


def compile_text(row):
    if row['message_id'] != 761:
        return compile_paragraph(row['english'])[0]
    text = row['english'].removesuffix('{PAD}')
    if text.count('%s') != 1 or '%' in text.replace('%s', ''):
        raise ValueError('One original building substitution is required')
    if (not text.isascii() or text != ' '.join(text.split()) or any(c in text for c in '{}')
            or any(c in text for c in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('Contract prose requires one ASCII paragraph without authored controls')
    return b' ' + text.encode('ascii')


def wrap_guard(arm):
    # Reuse the existing post-printf balancing adapter. Its original four stock
    # IDs remain exact; add only761. The full parent guard in its Thumb body is
    # unchanged. Moving its literal into four proven unused source bytes makes
    # room for an exact five-ID test without growing any executable allocation.
    entry, main, literal, stub = 0x021399B4, 0x0213B958, 0x02139830, 0x01FFC664
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old = bytes(ks.asm(f'ldr r3,[sp,#0x36c]; sub ip,r3,#764; sub ip,ip,#3; cmp ip,#3; bhi 0x01ffca00; ldr ip,[pc,#0]; bx ip; .word {main+1}', entry)[0])
    displacement = literal - (entry + 24 + 8)
    new = bytes(ks.asm(f'ldr r3,[sp,#0x36c]; sub ip,r3,#768; cmn ip,#7; addne ip,ip,#1; cmpne ip,#3; bhi 0x01ffca00; ldr ip,[pc,#{displacement}]; bx ip', entry)[0])
    old_stub = bytes(ks.asm('sub ip,r3,#688; cmp ip,#53; bls 0x01ffcf78; add ip,ip,#13; cmp ip,#6; bls 0x01ffcf78; b 0x01ffcbd8', stub)[0])
    new_stub = old_stub[:24] + bytes(ks.asm(f'b {DISPATCH}', stub + 24)[0])
    dispatch = bytes(ks.asm('cmp ip,#86; beq 0x01ffcf78; b 0x01ffcbd8', DISPATCH)[0])
    assert len(old) == len(new) == 32 and len(old_stub) == len(new_stub) == 28
    assert arm[entry-BASE:entry-BASE+32] == old
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[literal-BASE:literal-BASE+4] == clean[literal-BASE:literal-BASE+4]
    target = bytearray(arm)
    target[entry-BASE:entry-BASE+32] = new
    struct.pack_into('<I', target, literal-BASE, main+1)
    assert target[DISPATCH-BASE:DISPATCH-BASE+12] == bytes(12)
    target[DISPATCH-BASE:DISPATCH-BASE+12] = dispatch
    code = MainCodeFile(bytes(target), BASE)
    assert bytes(code.sections[4].data[0x664:0x680]) == old_stub
    code.sections[4].data[0x664:0x680] = new_stub
    return bytes(code.save()), {'entry': entry, 'literal': literal, 'stub': stub, 'new_dispatch': DISPATCH, 'new_dispatch_hex': dispatch.hex(),
        'old_entry_hex': old.hex(), 'new_entry_hex': new.hex(), 'old_stub_hex': old_stub.hex(), 'new_stub_hex': new_stub.hex(),
        'exact_balanced_IDs': [761, 767, 768, 769, 770], 'full_original_parent_guard_unchanged': True}


def provider_patch(arm):
    assert arm[GOV - BASE:GOV - BASE + 44] == REGION
    assert arm[PALACE - BASE:PALACE - BASE + 7] == b'Palace\0'
    assert arm[PORT - BASE:PORT - BASE + 5] == b'Port\0'
    assert arm[TARGET - BASE:TARGET - BASE + 7] == b'Target\0'
    rom = NdsImage.open('out/all_routes_combined_v757_candidate.nds')
    assert rom.read_file('/__arm9__.bin') == arm
    units = [(f'section{k}', s.ramAddress, bytes(s.data)) for k, s in enumerate(MainCodeFile(arm, BASE).sections)]
    units += [(f'overlay{k}', s.ramAddress, bytes(s.data)) for k, s in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).items()]
    aliases, branches = [], []
    for label, base, data in units:
        for off in range(len(data) - 3):
            value = struct.unpack_from('<I', data, off)[0]
            if GOV <= value < GOV + 44:
                aliases.append((label, base + off, value))
        for off in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, off)[0]
            if (word >> 25) & 7 != 5:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            target = base + off + 8 + 4 * delta
            if GOV <= target < GOV + 44:
                branches.append((label, base + off, target))
    assert aliases == [('section0', 0x020BA47C, GOV), ('section0', 0x020BA480, GOV + 8),
                       ('section0', 0x020BCA3C, GOV + 16), ('section0', 0x0211AEC0, GOV + 36), ('section0', 0x0211AED8, GOV + 28)], aliases
    assert branches == []
    target = bytearray(arm)
    payload = NAMES[0].encode('ascii') + b'\0\0\0' + b'Investment\0' + bytes(13)
    assert len(payload) == 44 and payload[20:31] == b'Investment\0'
    target[GOV - BASE:GOV - BASE + 44] = payload
    fields = {0xBA480: PALACE, 0xBCA3C: INVESTMENT, 0x11AED8: PORT, 0x11AEC0: TARGET}
    for at, pointer in fields.items():
        struct.pack_into('<I', target, at, pointer)
    return bytes(target), {'all_current_unaligned_owners': aliases, 'all_current_branch_owners': branches,
        'merged_five_complete_source_provider_slots': [GOV, GOV + 44],
        'relocated_pointer_fields': fields, 'full_governor_office_name': NAMES[0],
        'Palace_Investment_Port_Target_visible_bytes_preserved': True}


def plan(common, arm, authored):
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 5 <= e.block <= 18]
    assert [e.message_id for e in selected] == list(range(344, 1713))
    for e in selected:
        assert set(blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]) <= {0, 32}
    for block in range(5, 19):
        first = next(e for e in selected if e.block == block)
        assert set(blocks[block][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for e in selected:
        text = authored.get(e.message_id, e.text) + b'\0'
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body)))
            group, body = [], bytearray()
        group.append((e.message_id, len(body), text))
        body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 14, [len(raw) for _, raw in groups]
    rebuilt, target = list(blocks), bytearray(arm)
    fields, mapping = [], []
    for block, (group, raw) in zip(range(5, 19), groups, strict=True):
        rebuilt[block] = raw
        field = DIRECTORY_OFFSET + 4 * block
        struct.pack_into('<HH', target, field, group[0][0], len(raw))
        fields.append((field, 4))
        for number, offset, text in group:
            field = TABLE_OFFSET + 2 * number
            struct.pack_into('<H', target, field, offset)
            fields.append((field, 2))
            mapping.append({'id': number, 'block': block, 'offset': offset, 'text_hex': text[:-1].hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    path = '/COMMON/MESFILE.DK4'
    clean, accepted = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(accepted.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    jp, canonical, before = [common_message_entries(r.read_file(path), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, accepted, NdsImage.open('out/all_routes_combined_v757_candidate.nds'))]
    assert sha(arm) == manuscript['current_ARM9_sha256'] and sha(common) == manuscript['current_COMMON_sha256']
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert jp[n].text == bytes.fromhex(row['source_hex']) and canonical[n].text == bytes.fromhex(row['canonical_source_hex'])
        assert before[n].text == bytes.fromhex(row['current_text_hex'])
        assert jp[n].text.count(b'%s') == (1 if n == 761 else 0)
        authored[n] = compile_text(row)
    renamed, providers = provider_patch(arm)
    runtime, guard = wrap_guard(renamed)
    common2, arm2, fields, mapping = plan(common, runtime, authored)
    assert sha(arm2[DIRECTORY_OFFSET:TABLE_OFFSET]) == DIRECTORY
    after = common_message_entries(common2, arm2, clean=False)
    assert all(b.text == authored.get(a.message_id, a.text) for a, b in zip(before, after, strict=True))
    blocks, rebuilt = map(lambda c: IlnkContainer.parse(c).blocks, (common, common2))
    assert all(a == b for k, (a, b) in enumerate(zip(blocks, rebuilt, strict=True)) if k not in range(5, 19))
    restored = bytearray(arm2)
    for at, size in fields:
        restored[at:at + size] = runtime[at:at + size]
    assert bytes(restored) == runtime and cache_plan(arm2) == cache_plan(arm)
    return common2, arm2, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS],
        'provider_ownership': providers, 'wrap_guard': guard, 'owned_metadata_fields': fields, 'complete1369_selection_map': mapping,
        'all3660_unselected_texts_and27_other_blocks_exact': True,
        'no_font_section_pool_cache_startup_or_allocator_growth': True,
        'native_directory_sha256': DIRECTORY, 'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-market-contract-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    common, arm, proof = transform(common, arm, read(manuscript))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, proof
