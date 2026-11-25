"""Keep already-expanded story text literal during final dialogue preparation."""

from struct import pack_into, unpack_from

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.patch.captain_name_delete import CAPTAIN_PROVIDERS, DELETE_CALL, SECTION_LIMIT
from dk4tool.patch.main_pool_cache_visibility import BASE, cache_plan, target
from scripts.probe_common_display_name_hook import branch_link


COPY_LITERAL = 0x01FF9FAC
NATIVE_EXPANDER = 0x02053914
# Site, inherited formatter, and the saved returns proving this input has passed the story expander.
FRAMES = {
    0x54160: (0x01FFCF3C, ((0x264, 0x02054048), (0x26C, 0x020242F4))),
    0x54798: (0x01FFC828, ((0xC4, 0x02054764), (0xCC, 0x0202431C))),
    0x53AF0: (NATIVE_EXPANDER, ((0x14, 0x0202433C),)),
}


def guard(entry, fallback, frames):
    # Restore the original argument registers and stack before either tail call.
    body = ["push {r3}"]
    for index, (sp_offset, saved_return) in enumerate(frames):
        body.extend((f"ldr ip, [sp, #{sp_offset + 4:#x}]",
                     f"ldr r3, expected_{index}", "cmp ip, r3", "bne unexpanded"))
    body.extend(("pop {r3}", f"b {COPY_LITERAL:#x}", "unexpanded:", "pop {r3}", f"b {fallback:#x}"))
    body.extend(f"expected_{i}: .word {saved_return:#x}" for i, (_, saved_return) in enumerate(frames))
    return bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm("\n".join(body), entry)[0])


def stage(arm, clean, deletion_proof):
    code = MainCodeFile(arm, BASE)
    assert bytes(code.save()) == arm
    storage = code.sections[-1]
    original_payload = bytes(storage.data)
    assert storage.ramAddress == CAPTAIN_PROVIDERS and not storage.bssSize
    assert target(arm, DELETE_CALL) == deletion_proof["entry"]
    at = deletion_proof["entry"] - CAPTAIN_PROVIDERS
    assert original_payload[at:] == bytes.fromhex(deletion_proof["helper_hex"])
    assert arm[0x242CC:0x24310] == clean[0x242CC:0x24310]
    assert arm[0x24314:0x24330] == clean[0x24314:0x24330]
    assert arm[0x24334:0x2434C] == clean[0x24334:0x2434C]
    for site in (0x242C8, 0x24310, 0x24330):
        assert target(arm, site) == 0x023A4DC4 and target(clean, site) == NATIVE_EXPANDER
    copy_owner = next(s for s in code.sections if s.ramAddress <= COPY_LITERAL < s.ramAddress + len(s.data))
    off = COPY_LITERAL - copy_owner.ramAddress
    assert bytes(copy_owner.data[off:off+20]) == bytes.fromhex("0130d1e40130c0e4000053e3fbffff1a1eff2fe1")

    added = bytearray()
    changes = []
    for site, (fallback, frames) in FRAMES.items():
        assert unpack_from("<I", clean, site)[0] == branch_link(BASE+site, NATIVE_EXPANDER)
        assert target(arm, site) == fallback
        assert arm[site-12:site] == clean[site-12:site]
        entry = storage.ramAddress + len(original_payload) + len(added)
        item = guard(entry, fallback, frames)
        added.extend(item)
        pack_into("<I", code.sections[0].data, site, branch_link(BASE+site, entry))
        changes.append(dict(site=BASE+site, previous_formatter=fallback, expected_saved_returns=frames,
                            entry=entry, helper_hex=item.hex()))
    stop = CAPTAIN_PROVIDERS + len(original_payload) + len(added)
    assert stop <= SECTION_LIMIT and stop % 4 == 0
    assert all(s.ramAddress + len(s.data) + s.bssSize <= CAPTAIN_PROVIDERS
               or s.ramAddress >= SECTION_LIMIT for s in code.sections[:-1])

    storage.data.extend(added)
    result = bytes(code.save())
    assert cache_plan(result) == cache_plan(arm)
    inverse = MainCodeFile(result, BASE)
    assert bytes(inverse.sections[-1].data) == original_payload + added
    inverse.sections[-1].data = bytearray(original_payload)
    for site in FRAMES:
        inverse.sections[0].data[site:site+4] = arm[site:site+4]
    assert bytes(inverse.save()) == arm
    return result, dict(hooks=changes, native_literal_copy=COPY_LITERAL, new_tail_size=len(added),
        inherited_autoload_size=len(original_payload), changed_code_interval_end=stop, exact_arm9_inverse=True)

