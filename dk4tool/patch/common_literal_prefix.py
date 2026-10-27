"""Preserve ordinary English F/I in the shared native macro expander."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.common_copy_alignment_release import branch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "1c6a248091defe2b7b5a5f94906782125c86476402d058a79efac7f595b7ba20"
ROOT = Path("work/analysis/common_literal_prefix_v255")


def guard(address, prefix):
    a = Assembly()
    a.emit(0xE3510000 | ord(prefix))  # original CMP r1,prefix
    a.branch("original", 1)
    a.emit(0xE5D50001)  # look ahead without advancing the input pointer
    if prefix == "F":
        for suffix in "AIOU":
            a.emit(0xE3500000 | ord(suffix))
            a.branch("original", 0)
    else:
        a.emit(0xE3500043)  # IC retains native actor-sensitive pronoun
        a.branch("original", 0)
        # Preserve legacy non-Latin/control suffix behavior; ordinary printable
        # English and a terminal I use the native single-byte literal copy.
        a.emit(0xE3500080)
        a.branch("original", 2)
        a.emit(0xE3500000)
        a.branch("literal", 0)
        a.emit(0xE3500020)
        a.branch("original", 3)
    a.mark("literal")
    a.emit(tail(address + len(a.words) * 4, BASE + 0x53A94))
    a.mark("original")
    a.emit(0xE3510000 | ord(prefix))  # restore flags for native BNE
    target = 0x53980 if prefix == "F" else 0x53A48
    a.emit(tail(address + len(a.words) * 4, BASE + target))
    return a.finish()


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Exact complete V254 ARM9 required")
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    cache_plan(source)
    packed = bytearray(before[3][:-48])
    preserved = len(packed)
    changes = []
    helpers = {}

    def replace(offset, expected, value):
        if struct.unpack_from("<I", source, offset)[0] != expected:
            raise ValueError("Native macro source differs at " + hex(offset))
        struct.pack_into("<I", code.sections[0].data, offset, value)
        changes.append({"offset": offset, "before": expected, "after": value})

    for offset, prefix in [(0x5397C, "F"), (0x53A44, "I")]:
        address = POOL + len(packed)
        blob = guard(address, prefix)
        helpers[prefix] = {"entry": address, "bytes": len(blob)}
        packed.extend(blob)
        replace(offset, 0xE3510000 | ord(prefix), branch(BASE + offset, address))
    packed.extend(bytes((-len(packed)) % 32))
    size = len(packed) + 64
    if POOL + size > STAGE or STAGE + size + 48 > 0x023F4000:
        raise ValueError("Macro guard escapes owned storage")
    entry, copy = STAGE + len(packed), STAGE + size
    packed.extend(wrapper(entry, copy, size, source))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack("<I", size)
    replace(0x8E4, struct.unpack_from("<I", source, 0x8E4)[0], branch_link(BASE + 0x8E4, entry))
    replace(0xE45DC, struct.unpack_from("<I", source, 0xE45DC)[0], POOL + size)
    saved = bytes(code.save())
    loaded = MainCodeFile(saved, BASE)
    restored = bytearray(loaded.sections[0].data)
    for row in changes:
        o = row["offset"]
        restored[o:o + 4] = before[0][o:o + 4]
    o = code.codeSettingsOffs
    restored[o:o + 12] = before[0][o:o + 12]
    if bytes(restored) != before[0] or any(bytes(loaded.sections[n].data) != before[n] for n in (1, 2)):
        raise ValueError("Macro guard changes unrelated native code/data")
    if bytes(loaded.sections[3].data[:preserved]) != before[3][:-48]:
        raise ValueError("Inherited pool differs")
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
                   "helpers": helpers, "changes": changes, "cache": cache_plan(saved),
                   "payload_bytes": size, "inherited_pool_bytes_preserved": preserved,
                   "recognized_F_tokens_preserved": ["FA", "FI", "FO", "FU"],
                   "IC_and_legacy_non_Latin_I_suffixes_preserved": True,
                   "ordinary_ASCII_F_and_I_copied_without_consuming_following_byte": True}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    if config["format"] != "dk4-common-literal-prefix-release-v1":
        raise ValueError("Unknown common literal-prefix release")
    for file, digest in config["dependencies"].items():
        if sha(Path(file).read_bytes()) != digest:
            raise ValueError("Literal-prefix proof dependency differs")
    saved, plan = transform(source)
    if sha(saved) != config["target_arm9_sha256"]:
        raise ValueError("Literal-prefix target differs")
    plan["changed_records"] = ["DK4_SHARED_COMMON_LITERAL_F_I_PREFIX_V1"]
    return saved, plan
