"""Route the one-day repair message through the proven portrait word wrapper."""

import json
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

HOOK = 0x01FFCF50
STUB = 0x01FFCBD8
ACTIVE = 0x01FFCF78
RETURN = 0x01FFCF54
ASM = f'''sub r3,r3,#800
cmp r3,#1
beq {ACTIVE}
sub r3,r3,#20
b {RETURN}'''


def transform(source):
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert len(before[4]) == 4096
    ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    original = bytes(ks.asm('sub r3,r3,#820', HOOK)[0])
    hook = bytes(ks.asm(f'b {STUB}', HOOK)[0])
    stub = bytes(ks.asm(ASM, STUB)[0])
    ho, so = HOOK - 0x01FFC000, STUB - 0x01FFC000
    assert len(stub) == 20 and before[4][ho:ho + 4] == original
    assert before[4][so:so + len(stub)] == b'\0' * len(stub)
    code.sections[4].data[ho:ho + 4] = hook
    code.sections[4].data[so:so + len(stub)] = stub
    target = bytes(code.save())
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in range(4))
    restored = bytearray(parsed.sections[4].data)
    restored[ho:ho + 4] = original
    restored[so:so + len(stub)] = b'\0' * len(stub)
    assert bytes(restored) == before[4]
    return target, {'changed_records': ['COMMON_MESSAGE_801_PORTRAIT_WORD_WRAP'],
                    'message_id': 801, 'original_parent_return': 0x02054014,
                    'hook_address': HOOK, 'owned_zero_padding': [STUB, len(stub)],
                    'all_OTHER_wrapper_dispatch_cases_preserved': True,
                    'all_prose_assets_and_directory_bytes_unchanged': True,
                    'SDK_section4_bytes': 4096, 'code_bank_growth': 0,
                    'full_graphics_goal_complete': False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-repair-wait-wrap-v1'
    assert sha(source) == config['source_arm9_sha256']
    target, report = transform(source)
    assert sha(target) == config['target_arm9_sha256']
    return target, report
