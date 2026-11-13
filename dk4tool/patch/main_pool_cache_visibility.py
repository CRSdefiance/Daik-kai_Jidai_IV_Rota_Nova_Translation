"""Source-locked SDK cache maintenance after the expanded main-pool copy."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE, POOL, STAGE = 0x02000000, 0x02387A20, 0x023A7200
SOURCE = 'c55a2530af7816a5f612494c42c16af5911e58791d571d92ad9297b7e87980ee'


def target(source, field):
    word = struct.unpack_from('<I', source, field)[0]
    if word >> 24 != 0xEB:
        raise ValueError('Startup hook is not native BL')
    delta = word & 0xFFFFFF
    if delta & 0x800000:
        delta -= 0x1000000
    return BASE + field + 8 + delta * 4


def sdk_ops(source):
    # Retain the game's exact drain / I-line invalidate / D-line clean+flush
    # opcodes, changing only their register operand to our preserved scratch.
    original = struct.unpack_from('<3I', source, 0xA34)
    expected = (0xEE077F9A, 0xEE074F35, 0xEE074F3E)
    if original != expected:
        raise ValueError('Exact SDK cache operations differ')
    return ((original[0] & ~0xF000) | 0x2000,
            original[1] & ~0xF000, original[2] & ~0xF000)


def wrapper(entry, copy_entry, size, source):
    drain, instruction, data = sdk_ops(source)
    return struct.pack('<16I', 0xE92D400F, branch_link(entry + 4, copy_entry),
                       0xE59F0024, 0xE59F1024, 0xE3A02000,
                       drain, instruction, data, 0xE2800020, 0xE2511020,
                       0x1AFFFFF9, drain, 0xE8BD800F, POOL, size, 0)


def cache_plan(source):
    stage = MainCodeFile(source, BASE).sections[3]
    if stage.ramAddress != STAGE:
        raise ValueError('Late-copy stage differs')
    payload = bytes(stage.data[:-48])
    size = struct.unpack_from('<I', stage.data, len(stage.data) - 4)[0]
    if size != len(payload):
        raise ValueError('Late-copy payload extent differs')
    entry = target(source, 0x8E4)
    copy_entry = STAGE + size
    if entry == copy_entry:
        return None
    if size % 32:
        raise ValueError('Executable late-copy payload cache alignment differs')
    if entry != copy_entry - 64 or payload[-64:] != wrapper(entry, copy_entry, size, source):
        raise ValueError('Startup cache wrapper differs from its source-locked sequence')
    return {'entry': entry, 'copy_entry': copy_entry, 'payload_bytes': size,
            'pool_span': [POOL, POOL + size], 'line_bytes': 32,
            'operations': {entry + 20: 'drain', entry + 24: 'invalidate_instruction',
                           entry + 28: 'clean_flush_data', entry + 44: 'drain_final'},
            'SDK_opcode_fields': [BASE + 0xA34, BASE + 0xA38, BASE + 0xA3C]}


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact complete item research source required')
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    if len(before) != 4 or len(before[3]) != 19568 or code.sections[3].ramAddress != STAGE:
        raise ValueError('Source item staging differs')
    if cache_plan(source) is not None:
        raise ValueError('Source already has cache maintenance')
    payload = before[3][:-48]
    size = len(payload) + 64
    entry, copy_entry = STAGE + len(payload), STAGE + size
    cache_code = wrapper(entry, copy_entry, size, source)
    code.sections[3].data = bytearray(payload + cache_code + before[3][-48:-4] + struct.pack('<I', size))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    # The former copy entry becomes the wrapper entry. The startup BL is exact.
    if target(source, 0x8E4) != entry:
        raise ValueError('Source startup target differs')
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    restored[0xE45DC:0xE45E0] = before[0][0xE45DC:0xE45E0]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if (bytes(restored) != before[0] or any(bytes(loaded.sections[i].data) != before[i] for i in (1, 2))
            or bytes(loaded.sections[3].data[:len(payload)]) != payload):
        raise ValueError('Cache wrapper changes item prose/helpers or unrelated data')
    plan = cache_plan(saved)
    return saved, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(saved),
                   'item_payload_prefix_bytes_preserved': len(payload), 'cache': plan,
                   'staging_span': [STAGE, STAGE + size + 48],
                   'new_main_arena_low': POOL + size,
                   'status': 'cache-sequence-research-native-and-model-verification-pending',
                   'physical_cache_visibility_verified': False}
