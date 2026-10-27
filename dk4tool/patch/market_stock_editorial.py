"""Market stock and letters: faithful paragraphs and scoped runtime balancing."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from keystone import KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.patch.town_stock_rows import scatter
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import (
    DIRECTORY_OFFSET,
    TABLE_OFFSET,
    common_message_entries,
)
from scripts.probe_market_stock_layout_v755 import experimental_arm
from scripts.verify_village_wrap_v608 import read

BASE=0x02000000
ENTRY, MAIN, RETRY, WEAK = 0x021399B4, 0x0213B958, 0x02139934, 0x02139818
DONE=MAIN+144
WIDTH=0x021398A4
WIDTH_BLOCKS=[(WIDTH,WIDTH+28),(0x0213E320,0x0213E330),(0x0213B9FC,0x0213BA04),
              (0x0213E2F8,0x0213E300),(0x0213E310,0x0213E318),
              (0x0213E33C,0x0213E344),(0x0213E354,0x0213E35C)]
IDS=tuple(range(767,784))
DIRECTORY='9cde16387f9932ad0d566212537b6387f502c4dd6e6005308427f1708dfe825c'


def balance_runtime(arm):
    inventory = read('work/analysis/market_stock_v755/readonly_source_span_inventory_RESEARCH.json')
    for row in inventory['free']:
        at = row['lo'] - BASE
        assert arm[at:row['hi'] - BASE] == bytes.fromhex(row['source_hex'])
    code = MainCodeFile(arm, BASE)
    main = code.sections[0].data
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    entry = bytes(ka.asm(f'''ldr r3,[sp,#0x36c]
sub ip,r3,#764
sub ip,ip,#3
cmp ip,#3
bhi 0x01ffca00
ldr ip,[pc,#0]
bx ip
.word {MAIN + 1}''', ENTRY)[0])
    assert len(entry) == 32
    # All internal long jumps are Thumb-1 BL, using the already saved LR.
    # The only interworking call is the native ARM helper through BLX r3.
    text = f'''push {{r4-r7,lr}}
sub sp,#8
mov r4,r0
mov r5,r1
movs r0,#35
str r0,[sp,#0]
run:
mov r0,r4
mov r1,r5
ldr r3,native_helper
blx r3
str r0,[sp,#4]
ldr r1,[sp,#0]
cmp r1,#0
beq success
cmp r0,#0
beq failed
mov r6,r5
movs r2,#0
movs r7,#0
scan:
ldrb r0,[r6]
adds r6,#1
cmp r0,#0
beq finish
cmp r0,#10
beq line_end
adds r2,#1
cmp r0,#32
beq space
lsls r7,r7,#8
orrs r7,r0
b scan
space:
movs r7,#0
b scan
line_end:
bl {WEAK}
movs r2,#0
subs r2,#2
movs r7,#0
b scan
finish:
cmp r2,#8
bgt success
failed:
bl {RETRY}
success:
bl {DONE}
.align 2
native_helper: .word 0x01ffca00
'''
    body = bytes(kt.asm(text, MAIN)[0])
    assert len(body) == 96, len(body)
    instructions = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(body, MAIN))
    call = next(i for i in instructions if i.mnemonic == 'blx')
    assert call.size == 2 and call.op_str == 'r3'
    return_pc = (call.address + 2) | 1
    # Thumb BL target run is first source instruction after initial width store.
    run = MAIN + 12
    retry = bytes(kt.asm(f'''ldr r0,[sp,#0]
subs r0,#1
movs r1,#127
ands r1,r0
cmp r1,#24
bge store
cmp r0,#127
bgt fallback
movs r0,#162
b store
fallback:
movs r0,#0
store:
str r0,[sp,#0]
bl {run}
''', RETRY)[0])
    assert len(retry) <= 32, len(retry)
    done = bytes(kt.asm('ldr r0,[sp,#4]; add sp,#8; pop {r4-r7,pc}', DONE)[0])
    weak = bytes(kt.asm(f'''ldr r0,table
movs r1,#11
loop:
ldmia r0!,{{r3}}
cmp r3,r7
bne next
bl {RETRY}
next:
subs r1,#1
bne loop
bx lr
.align 2
table: .word 0x01ffcb44
''', WEAK)[0])
    assert len(weak) <= 28, len(weak)
    # All existing callers of this project-owned helper are ARM calls. The
    # scoped retry adapter is its sole Thumb caller; ownership is a release gate.
    width = bytes(ka.asm('''ldr ip,[sp,#32]
tst ip,#1
bne selected
ldr r7,portrait_return
cmp ip,r7
mov r7,#37
moveq r7,#35
bx lr
selected:
ldr r7,[sp,#36]
and r7,r7,#127
cmp r7,#0
moveq r7,#35
bx lr
portrait_return: .word 0x01ffcfd4
''', WIDTH)[0])
    patches, mapping = scatter(width, 52, WIDTH, WIDTH_BLOCKS)
    first_at = MAIN + len(body)
    first = bytes(ka.asm('''ldr ip,[sp,#32]
tst ip,#1
moveq r7,#36
bxeq lr
ldr r7,[sp,#36]
tst r7,#128
andne r7,r7,#127
addne r7,r7,#1
moveq r7,#36
bx lr''', first_at)[0])
    assert first_at + len(first) <= DONE
    used = [(ENTRY, entry), (MAIN, body), (first_at, first), (DONE, done), (RETRY, retry), (WEAK, weak), *patches]
    for at, raw in used:
        assert any(lo <= at and at + len(raw) <= hi for lo, hi in inventory['merged']), (hex(at), len(raw))
        main[at - BASE:at - BASE + len(raw)] = raw
    section = code.sections[4].data
    assert section[0xA14:0xA18] == bytes(ka.asm('mov r7,#36', 0x01FFCA14)[0])
    section[0xA14:0xA18] = bytes(ka.asm(f'bl {first_at}', 0x01FFCA14)[0])
    assert section[0xFD0:0xFD4] == bytes(ka.asm('bl 0x01ffca00', 0x01FFCFD0)[0])
    section[0xFD0:0xFD4] = bytes(ka.asm(f'bl {ENTRY}', 0x01FFCFD0)[0])
    section[0xB40:0xB44] = bytes(ka.asm(f'b {WIDTH}', 0x01FFCB40)[0])
    words = ('a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with')
    section[0xB44:0xB70] = struct.pack('<11I', *(int.from_bytes(s.encode('ascii'), 'big') for s in words))
    result = bytes(code.save())
    return result, {'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(result),
        'private_Thumb_return_PC': return_pc, 'main_bytes': len(body), 'retry_bytes': len(retry),
        'weak_bytes': len(weak), 'source_string_patches': [(a, raw.hex()) for a, raw in used],
        'width_mapping': mapping, 'experimental': True}


def compile_text(row):
    text = row['english'].removesuffix('{PAD}')
    number = row['message_id']
    slots = 2 if number in (767, 769) else 1 if number in (768, 770) else 0
    if (not text.isascii() or text != ' '.join(text.split()) or any(c in text for c in '{}')
            or text.count('%s') != slots or '%' in text.replace('%s', '')
            or any(token in text for token in ('FI', 'FA', 'FO', 'FU', 'IC'))):
        raise ValueError('One source-faithful paragraph and exact product substitutions required')
    if len(text) >= 200:
        raise ValueError('Template exceeds the existing bounded scratch')
    return b' ' + text.encode('ascii') if slots else compile_paragraph(row['english'])[0]


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    source = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    before = common_message_entries(common, arm, clean=False)
    authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert source[n].text == bytes.fromhex(row['source_hex'])
        assert accepted[n].text == bytes.fromhex(row['canonical_source_hex'])
        assert before[n].text == bytes.fromhex(row['current_text_hex'])
        assert source[n].text.count(b'%s') == row['english'].count('%s')
        authored[n] = compile_text(row)
    filtered, filter_proof = experimental_arm(arm)
    owner_path = Path('work/analysis/market_stock_v755/experimental_filter_ownership.json')
    ownership = read(owner_path)
    assert ownership['source_ARM9_sha256'] == sha(arm)
    assert ownership['research_ARM9_sha256'] == sha(filtered)
    assert ownership['all_unaligned_absolute_aliases'] == []
    assert ownership['all_direct_branch_owners'] == [['section4', 0x01FFCBFC, 0x01FFCF54]]
    assert len(ownership['all180_inherited_complete_output_controls']) == 180
    assert ownership['producer_sha256'] == sha(Path('scripts/verify_market_filter_owners_v755.py').read_bytes())
    filter_proof.update({'all_branch_and_pointer_owners_not_yet_audited': False,
        'complete_existing_owner_audit_and180_inherited_controls_pass': True,
        'ownership_report': str(owner_path), 'ownership_report_sha256': sha(owner_path.read_bytes())})
    runtime, runtime_proof = balance_runtime(filtered)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 10 <= e.block <= 18]
    assert [e.message_id for e in selected] == list(range(767, 1713))
    for e in selected:
        # Bytes after the visible NUL are discarded only when they are the
        # proven old inter-selection NUL/ASCII guards, never packed payload.
        assert set(blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]) <= {0, 32}
    for b in range(10, 19):
        first = next(e for e in selected if e.block == b)
        assert set(blocks[b][:first.block_offset]) <= {0, 32}
    groups, body, group = [], bytearray(), []
    for e in selected:
        text = authored.get(e.message_id, e.text) + b'\0'
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body)))
            body, group = bytearray(), []
        group.append((e.message_id, len(body), text))
        body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 9
    rebuilt, target_arm = list(blocks), bytearray(runtime)
    fields, mappings = [], []
    for b, (group, raw) in zip(range(10, 19), groups, strict=True):
        assert len(raw) <= 4096
        rebuilt[b] = raw
        field = DIRECTORY_OFFSET + b * 4
        struct.pack_into('<HH', target_arm, field, group[0][0], len(raw))
        fields.append((field, 4))
        for number, offset, text in group:
            field = TABLE_OFFSET + number * 2
            struct.pack_into('<H', target_arm, field, offset)
            fields.append((field, 2))
            mappings.append({'id': number, 'block': b, 'offset': offset, 'text_hex': text[:-1].hex()})
    target_arm = bytes(target_arm)
    target_common = IlnkContainer(rebuilt).to_bytes()
    assert sha(target_arm[DIRECTORY_OFFSET:TABLE_OFFSET]) == DIRECTORY
    after = common_message_entries(target_common, target_arm, clean=False)
    assert all(b.text == authored.get(a.message_id, a.text) for a, b in zip(before, after, strict=True))
    assert all(a == b for i, (a, b) in enumerate(zip(blocks, rebuilt, strict=True)) if i not in range(10, 19))
    restored = bytearray(target_arm)
    for at, size in fields:
        restored[at:at + size] = runtime[at:at + size]
    assert bytes(restored) == runtime and len(target_arm) == len(arm)
    assert cache_plan(target_arm) == cache_plan(arm)
    return target_common, target_arm, {
        'changed_records': [f'COMMON_MESSAGE_{i}' for i in IDS],
        'filter': filter_proof, 'runtime_balancing': runtime_proof,
        'native_directory_sha256': DIRECTORY, 'repacked_complete_selection_map': mappings,
        'owned_ARM9_metadata_fields': fields,
        'groups': [{'block': b, 'first_id': g[0][0], 'last_id': g[-1][0], 'bytes': len(raw)}
                   for b, (g, raw) in zip(range(10, 19), groups, strict=True)],
        'all3651_unselected_text_bytes_and32_other_blocks_exact': True,
        'no_section_pool_cache_startup_or_allocator_growth': True,
        'experimental': True, 'full_goal_complete': False}


def apply_release(common, arm, config_path):
    config = read(config_path)
    assert config['format'] == 'dk4-market-stock-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    for p, digest in config['dependencies'].items():
        assert sha(Path(p).read_bytes()) == digest, p
    path = Path(config['manuscript'])
    assert sha(path.read_bytes()) == config['manuscript_sha256']
    common, arm, proof = transform(common, arm, read(path))
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return common, arm, proof
