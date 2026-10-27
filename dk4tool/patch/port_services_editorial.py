"""Source-reviewed Port/companion/service prose and three scoped runtime IDs."""

import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import DISPATCH, LITERAL
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
SOURCE = '6508bf3e43144efc4a9b449564e1acd2a0eecacb7184ed23408ce1856cea1ddf'
IDS = (267, *range(805, 820), 1245, 1246)
PREFIX, TAIL = 0x02132020, 0x02147C20
ARGUMENTS = {808: ['literal_admiral_short_name'], 1245: ['native_gold_amount'], 1246: ['native_gold_amount']}
OWNERSHIP = Path('work/analysis/port_services_v762/owned_storage.json')


def assemble():
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    prefix = bytes(ka.asm(f'push {{r3,r4,lr}}; ldr r3,[sp,#0x270]; ldr r4,[sp,#0x280]; b {TAIL}', PREFIX)[0])
    tail = bytes(ka.asm(f'''
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,yes_parent
cmp r3,ip
bne fallback
sub r4,r4,#0x400
cmp r4,#0xde
beq selected
fallback:
b {DISPATCH + 4}
direct:
sub r4,r4,#0x300
cmp r4,#0x28
beq selected
sub r4,r4,#0x100
cmp r4,#0xdd
bne fallback
selected:
pop {{r3,r4,lr}}
b {LITERAL}
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
''', TAIL)[0])
    assert len(prefix) == 16 and len(tail) == 80
    return {PREFIX: prefix, TAIL: tail, DISPATCH: bytes(ka.asm(f'b {PREFIX}', DISPATCH)[0])}


def runtime_transform(arm):
    assert sha(arm) == SOURCE
    proof = read(OWNERSHIP)
    assert proof['source_ARM9_sha256'] == SOURCE
    assert proof['module_sha256'] == sha(Path(__file__).read_bytes())
    assert proof['all57_active_replacements_current_and_prior_source_ownership_verified']
    assert all(not proof[k] for k in ('free_span_absolute_aliases', 'free_span_ARM_branches', 'free_span_ADR', 'crossing_Cstrings'))
    target = bytearray(arm)
    patches = []
    for at, blob in assemble().items():
        before = arm[at - BASE:at - BASE + len(blob)]
        assert before.hex() == proof['source_patch_spans'][hex(at)]
        target[at - BASE:at - BASE + len(blob)] = blob
        patches.append({'address': at, 'source_hex': before.hex(), 'target_hex': blob.hex()})
    target = bytes(target)
    old_code, new_code = [MainCodeFile(a, BASE) for a in (arm, target)]
    assert [len(s.data) for s in old_code.sections] == [len(s.data) for s in new_code.sections]
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(old_code.sections[1:], new_code.sections[1:], strict=True))
    assert cache_plan(arm) == cache_plan(target)
    return target, {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(target), 'patches': patches,
        'no_section_pool_cache_startup_allocator_or_other_file_change': True, 'only_three_exact_new_call_memberships': True}


def compile_text(row):
    n = row['message_id']; text = row['english'].removesuffix('{PAD}')
    if (n not in IDS or not text or len(text) >= 200 or text != ' '.join(text.split())
            or not text.isascii() or any(ord(c) < 32 or ord(c) >= 127 for c in text)
            or any(c in text for c in '{}')):
        raise ValueError('One ordinary ASCII paragraph required')
    if n in ARGUMENTS:
        if text.count('%s') != 1 or '%' in text.replace('%s', '') or any(t in text for t in ('FI', 'FA', 'FO', 'FU', 'IC')):
            raise ValueError('Exactly one reviewed source argument required')
        return b' ' + text.encode('ascii')
    if n == 267:
        if '%' in text or len(text) > 36 or any(t in text for t in ('FI', 'FA', 'FO', 'FU', 'IC')):
            raise ValueError('System refusal must fit its original one-line surface')
        return text.encode('ascii')
    return compile_paragraph(row['english'])[0]


def plan(common, arm, authored):
    assert tuple(sorted(authored)) == IDS
    before = common_message_entries(common, arm, clean=False)
    blocks = IlnkContainer.parse(common).blocks
    selected = [e for e in before if 2 <= e.block <= 18]
    assert [e.message_id for e in selected] == list(range(164, 1713))
    for e in selected:
        assert set(blocks[e.block][e.block_offset + len(e.text) + 1:e.copy_end]) <= {0, 32}
    for k in range(2, 19):
        first = next(e for e in selected if e.block == k)
        assert set(blocks[k][:first.block_offset]) <= {0, 32}
    groups, group, body = [], [], bytearray()
    for e in selected:
        text = authored.get(e.message_id, e.text) + b'\0'
        if len(body) + len(text) > 4096:
            groups.append((group, bytes(body))); group, body = [], bytearray()
        group.append((e.message_id, len(body), text)); body.extend(text)
    groups.append((group, bytes(body)))
    assert len(groups) == 17
    rebuilt, target, fields, mapping = list(blocks), bytearray(arm), [], []
    for block, (group, raw) in zip(range(2, 19), groups, strict=True):
        rebuilt[block] = raw
        at = DIRECTORY_OFFSET + block * 4
        struct.pack_into('<HH', target, at, group[0][0], len(raw)); fields.append((at, 4))
        for n, offset, text in group:
            at = TABLE_OFFSET + n * 2
            struct.pack_into('<H', target, at, offset); fields.append((at, 2))
            mapping.append({'id': n, 'block': block, 'offset': offset, 'text_hex': text[:-1].hex()})
    return IlnkContainer(rebuilt).to_bytes(), bytes(target), fields, mapping


def transform(common, arm, manuscript):
    assert manuscript['translation_policy'] == 'natural-dialogue-v2'
    validate_natural_dialogue_batch(manuscript)
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    clean, accepted = [NdsImage.open(p) for p in ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(accepted.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    tables = [common_message_entries(r.read_file(path), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, accepted)]
    before = common_message_entries(common, arm, clean=False); authored = {}
    for row in manuscript['records']:
        n = row['message_id']
        assert tables[0][n].text.hex() == row['source_hex'] and tables[1][n].text.hex() == row['canonical_source_hex']
        assert before[n].text.hex() == row['current_text_hex']
        assert row['runtime_argument_contract'] == ARGUMENTS.get(n, [])
        authored[n] = compile_text(row)
        assert authored[n].count(b'%s') == tables[0][n].text.count(b'%s')
    runtime, proof = runtime_transform(arm)
    common2, arm2, fields, mapping = plan(common, runtime, authored)
    after = common_message_entries(common2, arm2, clean=False)
    assert all(b.text == authored.get(a.message_id, a.text) for a, b in zip(before, after, strict=True))
    old_blocks, new_blocks = [IlnkContainer.parse(c).blocks for c in (common, common2)]
    assert all(a == b for k, (a, b) in enumerate(zip(old_blocks, new_blocks, strict=True)) if k not in range(2, 19))
    restored = bytearray(arm2)
    for at, length in fields: restored[at:at + length] = runtime[at:at + length]
    assert bytes(restored) == runtime and cache_plan(arm2) == cache_plan(arm)
    return common2, arm2, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS], 'owned_runtime': proof,
        'metadata_fields': fields, 'complete1549_selection_map': mapping,
        'all3650_unselected_strings_and24_other_blocks_exact': True, 'experimental': True, 'actual_gameplay_pending': True}


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-port-services-editorial-v1'
    assert sha(common) == config['source_common_sha256'] and sha(arm) == config['source_arm9_sha256']
    for p, h in config['dependencies'].items(): assert sha(Path(p).read_bytes()) == h, p
    manuscript = Path(config['manuscript']); assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    c, a, proof = transform(common, arm, read(manuscript))
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    return c, a, proof
