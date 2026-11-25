"""Stage Latin glyph normalization at the captain editor and two load boundaries."""

from struct import pack, pack_into, unpack_from

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, cache_plan, target
from dk4tool.patch.sailing_no_target import Assembly
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "a8d73fb0d3b71cdb85b06e323854df5586d7a6e6e29beba4931e5f59fc4c4a7d"
TITLES = (0x0215029C, 0x021502A1, 0x021502AD, 0x021502B2)
EDIT_CONSTRUCTOR, EDIT_APPEND, MODEL_RESTORE, SLOT_DISPLAY = 0xAEBE0, 0xAED2C, 0x83098, 0xEEE48


def emit_call(assembly, start, destination):
    assembly.emit(branch_link(start + len(assembly.words) * 4, destination))


def tail(assembly, start, destination):
    assembly.emit(branch_link(start + len(assembly.words) * 4, destination) & ~0x01000000)


def normalize_field():
    """r0 is a writable CP932 field, r1 is its capacity including NUL."""
    a = Assembly()
    a.emit(0xE92D40F0)  # push {r4-r7,lr}
    a.emit(0xE0804001)  # end of allocation
    a.emit(0xE1A02000)  # bounded search for existing terminator
    a.mark("find_end")
    a.emit(0xE1520004)
    a.branch("return", 2)
    a.emit(0xE4D23001)
    a.emit(0xE3530000)
    a.branch("find_end", 1)
    a.emit(0xE2424001)  # keep the original terminator address
    a.emit(0xE1A02000)  # read cursor
    a.emit(0xE1A05000)  # write cursor
    a.mark("character")
    a.emit(0xE1520004)
    a.branch("clear_tail", 2)
    a.emit(0xE4D26001)  # first byte
    a.emit(0xE1520004)
    a.branch("copy_byte", 2)
    a.emit(0xE3560081)
    a.branch("copy_byte", 3)
    a.emit(0xE356009F)
    a.branch("trail", 9)
    a.emit(0xE35600E0)
    a.branch("copy_byte", 3)
    a.emit(0xE35600FC)
    a.branch("copy_byte", 8)
    a.mark("trail")
    a.emit(0xE5D27000)
    a.emit(0xE3570040)
    a.branch("copy_byte", 3)
    a.emit(0xE35700FC)
    a.branch("copy_byte", 8)
    a.emit(0xE357007F)
    a.branch("copy_byte", 0)
    a.emit(0xE2822001)  # consume exactly one complete CP932 pair
    a.emit(0xE3560082)
    a.branch("copy_pair", 1)
    a.emit(0xE3570060)
    a.branch("copy_pair", 3)
    a.emit(0xE3570079)
    a.branch("uppercase", 9)
    a.emit(0xE3570081)
    a.branch("copy_pair", 3)
    a.emit(0xE357009A)
    a.branch("copy_pair", 8)
    a.emit(0xE2476020)
    a.branch("copy_byte")
    a.mark("uppercase")
    a.emit(0xE247601F)
    a.branch("copy_byte")
    a.mark("copy_pair")
    a.emit(0xE4C56001)
    a.emit(0xE1A06007)
    a.mark("copy_byte")
    a.emit(0xE4C56001)
    a.branch("character")
    a.mark("clear_tail")
    a.emit(0xE3A06000)
    a.mark("clear_byte")
    a.emit(0xE4C56001)  # clear through the old NUL; keep all later padding
    a.emit(0xE1550004)
    a.branch("clear_byte", 9)
    a.mark("return")
    a.emit(0xE8BD80F0)
    return a.finish()


def editor_marker(start, provider, previous):
    a = Assembly()
    for index, title in enumerate(TITLES):
        a.load(12, f"title_{index}", title)
        a.emit(0xE153000C)  # cmp r3,ip; title is the constructor's fourth argument
        a.branch("mark_editor", 0)
    tail(a, start, previous)
    a.mark("mark_editor")
    a.load(12, "provider", provider)
    a.emit(0xE580C004)
    tail(a, start, previous)
    return a.finish()


def append_key(start, provider, normalize, previous):
    a = Assembly()
    a.emit(0xE510C034)  # child is parent+0x38, provider pointer is at parent+4
    a.emit(0xE92D400F)  # preserve original key/child and align nested call
    a.emit(0xE24DD004)
    a.load(3, "provider", provider)
    a.emit(0xE15C0003)
    a.branch("delegate", 1)
    a.emit(0xE5D1C002)  # a keyboard key is a single terminated pair
    a.emit(0xE35C0000)
    a.branch("delegate", 1)
    a.emit(0xE1A00001)
    a.emit(0xE3A01003)
    emit_call(a, start, normalize)
    a.mark("delegate")
    a.emit(0xE28DD004)
    a.emit(0xE8BD400F)
    tail(a, start, previous)
    return a.finish()


def loaded_actor(start, normalize):
    a = Assembly()
    a.emit(0xE92D4008)  # retain original return point and stack alignment
    for field, capacity in ((0x20, 17), (0x31, 17), (0x42, 17), (0x55, 19)):
        a.emit(0xE2850000 | field)  # the restore method keeps its actor in r5
        a.emit(0xE3A01000 | capacity)
        emit_call(a, start, normalize)
    a.emit(0xE3A00001)  # displaced successful return value
    a.emit(0xE8BD8008)
    return a.finish()


def slot_summary(start, normalize, previous):
    a = Assembly()
    a.emit(0xE92D400F)
    a.emit(0xE24DD004)
    a.emit(0xE2820030)  # stack copy read for display; name ends before the next 20-byte field
    a.emit(0xE3A01014)
    emit_call(a, start, normalize)
    a.emit(0xE28DD004)
    a.emit(0xE8BD400F)
    tail(a, start, previous)
    return a.finish()


def stage(source, clean, overlay_table):
    assert sha(source) == SOURCE
    assert [unpack_from("<I", source, at)[0] for at in (0x9E058, 0x9E060, 0x9E064, 0x9E068)] == list(TITLES)
    assert source[MODEL_RESTORE:MODEL_RESTORE + 8] == clean[MODEL_RESTORE:MODEL_RESTORE + 8] == pack("<2I", 0xE3A00001, 0xE8BD81F0)
    assert source[0xEEE14:0xEEE4C] == clean[0xEEE14:0xEEE4C] and target(source, SLOT_DISPLAY) == 0x020EFCDC
    assert target(source, EDIT_CONSTRUCTOR) == 0x01FF9E18 and target(source, EDIT_APPEND) == 0x01FF9E40
    original_provider = source[0x15591C:0x155924]
    assert original_provider == pack("<2I", 0x020B10D4, 0x020AE8B8)

    code = MainCodeFile(source, BASE)
    assert len(code.sections) == 6
    assert len(overlay_table) == 32
    _, overlay_start, overlay_size, overlay_bss, *_ = unpack_from("<8I", overlay_table)
    assert (overlay_start, overlay_size, overlay_bss) == (0x01FFA000, 0x1840, 0x20)
    # Use an SDK autoload after the original overlay and BSS, below the next declared ITCM section.
    # This keeps the main-RAM heap and the late-copy cache and payload separate from the new code.
    start = overlay_start + overlay_size + overlay_bss
    payload = bytearray()
    provider = start
    payload.extend(original_provider)
    normalizer = start + len(payload)
    payload.extend(normalize_field())
    hooks = {}
    for site, build, args in (
        (EDIT_CONSTRUCTOR, editor_marker, (provider, target(source, EDIT_CONSTRUCTOR))),
        (EDIT_APPEND, append_key, (provider, normalizer, target(source, EDIT_APPEND))),
        (MODEL_RESTORE, loaded_actor, (normalizer,)),
        (SLOT_DISPLAY, slot_summary, (normalizer, target(source, SLOT_DISPLAY))),
    ):
        entry = start + len(payload)
        payload.extend(build(entry, *args))
        hooks[site] = entry
    end = start + len(payload)
    assert start % 32 == 0 and end <= 0x01FFC000
    for section in code.sections:
        assert section.ramAddress + len(section.data) + section.bssSize <= start or end <= section.ramAddress
    code.sections.append(MainCodeFile.Section(payload, start, 0))
    mutations = {site: branch_link(BASE + site, entry) for site, entry in hooks.items()}
    for offset, word in mutations.items():
        pack_into("<I", code.sections[0].data, offset, word)
    result = bytes(code.save())
    assert cache_plan(result) == cache_plan(source)

    # Rebuild from the generated ARM9 after restoring the exact parent sections and words.
    recovered = MainCodeFile(result, BASE)
    for offset in mutations:
        recovered.sections[0].data[offset:offset + 4] = source[offset:offset + 4]
    recovered.sections.pop()
    assert bytes(recovered.save()) == source
    return result, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(result),
                    "provider": provider, "normalizer": normalizer, "hooks": hooks,
                    "autoload_span": [start, end], "overlay_span_with_bss": [overlay_start, start],
                    "late_copy_payload_bytes_preserved": cache_plan(source)["payload_bytes"]}
