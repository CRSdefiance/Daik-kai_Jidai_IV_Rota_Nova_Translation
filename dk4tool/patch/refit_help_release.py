"""Source-locked Refit help selector with reviewed, generated paragraph layouts."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.dialogue.refit_help import PROFILE, compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_common_display_name_hook import branch_link

IDS = tuple(range(1248, 1256)) + tuple(range(1268, 1290))
CALL = 0x169BC


def selector(address, table):
    asm = f'''push {{r1-r3,ip}}
mrs ip,cpsr
push {{ip,lr}}
sub r1,r0,#1248
cmp r1,#7
bls selected
sub r1,r0,#0x4f0
sub r1,r1,#4
cmp r1,#21
bhi fallback
add r1,r1,#8
selected:
ldr r2,table
ldr r0,[r2,r1,lsl #2]
pop {{ip,lr}}
msr cpsr_f,ip
pop {{r1-r3,ip}}
bx lr
fallback:
pop {{ip,lr}}
msr cpsr_f,ip
pop {{r1-r3,ip}}
b 0x0205528c
table:
.word {table}
'''
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(asm, address)[0]), asm


def transform(source, manuscript):
    validate_natural_dialogue_batch(manuscript)
    assert manuscript['format'] == 'dk4-refit-help-manuscript-v1'
    assert [r['message_id'] for r in manuscript['records']] == list(IDS)
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    assert sha(clean.read_file(path)) == manuscript['source_clean_COMMON_sha256']
    assert sha(canonical.read_file(path)) == manuscript['source_canonical_COMMON_sha256']
    original = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    accepted = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    plan = cache_plan(source)
    assert plan and len(before) == 5 and len(before[3]) == plan['payload_bytes'] + 48
    assert struct.unpack_from('<I', source, CALL)[0] == branch_link(BASE + CALL, 0x0205528C)
    assert source[0x16868:0x169C8] == clean.read_file('/__arm9__.bin')[0x16868:0x169C8]
    # Retain every inherited payload byte up to its old cache wrapper.
    preserved = plan['payload_bytes'] - 64
    packed = bytearray(before[3][:preserved])
    pointers, layouts = [], []
    for row in manuscript['records']:
        i = row['message_id']
        assert bytes.fromhex(row['clean_source_hex']) == original[i].text
        assert bytes.fromhex(row['canonical_source_hex']) == accepted[i].text
        compiled, lines = compile_paragraph(row['english'])
        pointers.append(POOL + len(packed))
        packed.extend(compiled)
        layouts.append({'message_id': i, 'English': row['english'], 'lines': lines,
            'pointer': pointers[-1], 'compiled_hex': compiled.hex(), 'profile': PROFILE})
    packed.extend(bytes(-len(packed) % 4))
    table = POOL + len(packed)
    packed.extend(struct.pack('<30I', *pointers))
    entry = POOL + len(packed)
    helper, assembly = selector(entry, table)
    packed.extend(helper)
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError('Reviewed Refit paragraphs exceed the owned late-copy storage')
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    changes = [(CALL, branch_link(BASE + CALL, entry)),
        (0x8E4, branch_link(BASE + 0x8E4, cache_entry)), (0xE45DC, POOL + size)]
    for offset, value in changes:
        struct.pack_into('<I', code.sections[0].data, offset, value)
    result = bytes(code.save())
    after = MainCodeFile(result, BASE)
    restored = bytearray(after.sections[0].data)
    for offset, _ in changes:
        restored[offset:offset + 4] = before[0][offset:offset + 4]
    off = code.codeSettingsOffs
    restored[off:off + 12] = before[0][off:off + 12]
    assert bytes(restored) == before[0]
    assert all(bytes(after.sections[i].data) == before[i] for i in (1, 2, 4))
    assert bytes(after.sections[3].data[:preserved]) == before[3][:preserved]
    assert bytes(after.sections[3].data[-48:-4]) == before[3][-48:-4]
    return result, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(result),
        'dedicated_original_Refit_help_selector': 0x02016868,
        'only_help_provider_call_replaced': BASE + CALL, 'unchanged_original_message_provider': 0x0205528C,
        'helper_entry': entry, 'helper_bytes': len(helper), 'helper_assembly': assembly, 'table': table,
        'records': layouts, 'cache': cache_plan(result), 'preserved_inherited_pool_bytes': preserved,
        'all_other_main_bytes_ITCM_font_code_COMMON_tables_and_components_preserved': True,
        'unselected_IDs_tail_to_original_provider_with_original_arguments_flags_and_stack': True,
        'no_authored_line_breaks_or_shortened_source_meaning': True,
        'changed_records': [f'REFIT_HELP_{i}' for i in IDS], 'experimental': True, 'full_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-refit-help-release-v1' and sha(source) == config['source_arm9_sha256']
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    assert sha(Path('dk4tool/dialogue/refit_help.py').read_bytes()) == config['compiler_sha256']
    for dependency, digest in config['native_dependencies'].items():
        assert sha(Path(dependency).read_bytes()) == digest
    native = json.loads(Path(config['native_font_proof']).read_text(encoding='utf-8'))
    selectors = json.loads(Path(config['selector_proof']).read_text(encoding='utf-8'))
    assert native['native_bitmap_pixels_compared'] == 423360
    assert selectors['all3668_native_message_IDs_exercised']
    target, proof = transform(source, json.loads(manuscript.read_text(encoding='utf-8')))
    # JSON stores the cache operation addresses as string keys. Compare the
    # complete serialized proof form, while retaining the exact binary hash.
    assert sha(target) == config['target_arm9_sha256']
    assert json.loads(json.dumps(proof)) == config['proof']
    assert [(r['message_id'], r['compiled_hex']) for r in native['all30_complete_native_font_paints']] == [
        (r['message_id'], r['compiled_hex']) for r in proof['records']]
    return target, proof
