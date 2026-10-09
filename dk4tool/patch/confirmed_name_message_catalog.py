"""Research exact-string substitutions at the native story copy boundary."""

import struct

from ndspy.code import MainCodeFile

from dk4tool.patch.confirmed_character_names import transform as name_fields
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from scripts.probe_common_display_name_hook import branch_link

CALLS = (0x242C8, 0x24310, 0x24330)
MACRO = BASE + 0x53914


def helper(address, table, count):
    """Preserve the original ABI and tail-call the unchanged native expander."""
    words, labels, branches, loads, literals = [], {}, [], [], {}

    def emit(word):
        words.append(word)

    def mark(name):
        labels[name] = len(words)

    def branch(name, condition=14):
        branches.append((len(words), name, condition))
        emit(0)

    def load(register, name, value):
        literals[name] = value
        loads.append((len(words), register, name))
        emit(0)

    emit(0xE92D51FD)  # push r0,r2-r8,ip,lr; r1 is the selected input pointer
    for index, field in enumerate(CALLS):
        load(12, f"caller{index}", BASE + field + 4)
        emit(0xE15E000C)  # cmp lr,ip
        branch("scoped", 0)
    branch("finish")
    mark("scoped")
    emit(0xE1A03001)  # mov r3,r1
    load(4, "table", table)
    if not 0 < count < 256:
        raise ValueError("Bounded message catalog entry count required")
    emit(0xE3A05000 | count)
    mark("next")
    emit(0xE3550000)
    branch("finish", 0)
    emit(0xE5946000)  # key pointer
    emit(0xE5947008)  # byte count INCLUDING NUL
    emit(0xE3A08000)
    mark("compare")
    emit(0xE7D6C008)  # ldrb ip,[r6,r8]
    emit(0xE7D32008)  # ldrb r2,[r3,r8]
    emit(0xE15C0002)
    branch("miss", 1)
    emit(0xE2888001)
    emit(0xE1580007)
    branch("compare", 3)
    emit(0xE5941004)  # replacement pointer; original speaker/actor is preserved
    branch("finish")
    mark("miss")
    emit(0xE284400C)
    emit(0xE2555001)
    branch("next")
    mark("finish")
    emit(0xE8BD51FD)
    at = address + len(words) * 4
    emit(0xEA000000 | ((MACRO - at - 8) // 4 & 0xFFFFFF))
    for name, value in literals.items():
        mark(name)
        emit(value)
    for index, name, condition in branches:
        words[index] = (condition << 28) | 0x0A000000 | ((labels[name] - index - 2) & 0xFFFFFF)
    for index, register, name in loads:
        delta = (labels[name] - index - 2) * 4
        if not 0 <= delta < 4096:
            raise ValueError("Message helper literal escaped its bounded pool")
        words[index] = 0xE59F0000 | register << 12 | delta
    return struct.pack(f"<{len(words)}I", *words)


def transform(source, clean, entries):
    named, names = name_fields(source, clean)
    code = MainCodeFile(named, BASE)
    before = [bytes(section.data) for section in code.sections]
    inherited_cache = cache_plan(named)
    if not inherited_cache or len(before[3]) != 20624:
        raise ValueError("Exact complete V190 staged pool/cache contract required")
    packed = bytearray(before[3][:-48])
    records, pointers = [], {}

    def store(raw):
        if not raw or b"\0" in raw or len(raw) >= 512:
            raise ValueError("Complete bounded message without interior NUL required")
        if raw not in pointers:
            packed.extend(bytes((-len(packed)) % 4))
            pointers[raw] = POOL + len(packed)
            packed.extend(raw + b"\0")
        return pointers[raw]

    seen = {}
    for entry in entries:
        key, target = bytes.fromhex(entry["key_hex"]), bytes.fromhex(entry["target_hex"])
        if key in seen and seen[key] != target:
            raise ValueError("Identical native inputs have conflicting translations")
        seen[key] = target
    for key, target in sorted(seen.items()):
        records.append({"key_pointer": store(key), "target_pointer": store(target),
                        "key_bytes_with_NUL": len(key) + 1,
                        "key_hex": key.hex(), "target_hex": target.hex()})
    packed.extend(bytes((-len(packed)) % 4))
    table = POOL + len(packed)
    for row in records:
        packed.extend(struct.pack("<3I", row["key_pointer"], row["target_pointer"], row["key_bytes_with_NUL"]))
    entry = POOL + len(packed)
    implementation = helper(entry, table, len(records))
    packed.extend(implementation)
    for field in CALLS:
        if struct.unpack_from("<I", named, field)[0] != branch_link(BASE + field, MACRO):
            raise ValueError("Original story macro-copy call changed")
        struct.pack_into("<I", code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    cache_entry, copy_entry = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(cache_entry, copy_entry, size, named))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, cache_entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for field in (*CALLS, 0x8E4, 0xE45DC):
        restored[field:field + 4] = before[0][field:field + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    if bytes(restored) != before[0] or any(bytes(parsed.sections[i].data) != before[i] for i in (1, 2)):
        raise ValueError("Message catalog changes unrelated code or native sections")
    if bytes(parsed.sections[3].data[:len(before[3]) - 48]) != before[3][:-48]:
        raise ValueError("Inherited text/helpers/staged payload changed")
    return saved, {"source_arm9_sha256": sha(source), "named_arm9_sha256": sha(named),
                   "target_arm9_sha256": sha(saved), "name_fields": names,
                   "entry": entry, "table": table, "records": records,
                   "helper_bytes": len(implementation), "helper_sha256": sha(implementation),
                   "inherited_pool_bytes_preserved": len(before[3]) - 48,
                   "pool_payload_bytes": size, "copy_entry": copy_entry,
                   "cache": cache_plan(saved), "pool_span": [POOL, POOL + size],
                   "staging_span": [STAGE, STAGE + size + 48],
                   "scoped_call_sites": [BASE + field for field in CALLS],
                   "script_instruction_boundaries_untouched": True,
                   "original_native_macro_expander_untouched": True,
                   "research_only": True, "startup_ABI_and_native_pixels_pending": True}
