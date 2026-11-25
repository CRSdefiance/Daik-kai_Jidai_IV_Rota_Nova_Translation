"""Bound the current context-sensitive Help entry for inventoried native views."""

from collections import defaultdict
from pathlib import Path
from struct import iter_unpack, pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import reconcile_help_topic_navigation_20261124 as graph
from scripts.reconcile_class_names_20261123 import c_string
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine

BASE = graph.BASE
current = graph.current
OUT = graph.OUT.with_name("help_direct_entries_current_20261124.json")
ANCHORS = {0x020C7E74: 0x54, 0x020C8288: 0x58, 0x0200A544: 0x8C, 0x020C82E8: 0x90}
GETTER_TYPES = {
    0x0200A544: (None, "disabled"),
    0x02012A4C: (None, "constant"), 0x020166D0: (None, "constant"),
    0x020210A4: (0x0201DBA4, "crew"),
    0x0204EB38: (0x0204D298, "context stack"), 0x0205345C: (0x02052C98, "context stack"),
    0x0206ECB8: (None, "ocean mode"), 0x0207C6C4: (0x0207B4E4, "ocean scene"),
    0x02086244: (0x020831B8, "organize load"),
    0x02087E48: (None, "constant"), 0x02090054: (0x0208C610, "constant"),
    0x0209997C: (0x020997E0, "constant"), 0x0209DA10: (0x0209B96C, "constant"),
    0x020AAE60: (0x020A4C60, "proxy fleet"), 0x020AAC60: (0x020A4C54, "constant"),
    0x020AAAE8: (0x020A4C4C, "constant"), 0x020B7A88: (None, "constant"),
    0x020C59CC: (0x020BD9B4, "constant"), 0x020C533C: (0x020C06DC, "constant"),
    0x020C6BA4: (0x020C6678, "context stack"),
}
NO_TOPIC = 0xFFFFFFFF
OBJECT = 0x02451000
STACK_GLOBAL = 0x022CF7D8
VALUES = {
    0x02012A4C: 105, 0x020166D0: 51, 0x02087E48: 103, 0x0208C610: 104,
    0x020997E0: 76, 0x0209B96C: 135, 0x020A4C54: 65, 0x020A4C4C: 63,
    0x020B7A88: 11, 0x020BD9B4: 24, 0x020C06DC: 22,
}
STACK_CTOR = 0x020C989C
CREW_CTOR, CREW_WRAPPER = 0x0202015C, 0x0201DBC0


def word(memory, at):
    assert BASE <= at <= BASE + len(memory) - 4, hex(at)
    return unpack_from("<I", memory, at - BASE)[0]


def span(source, installed, lo, hi):
    value = source[lo - BASE:hi - BASE]
    assert len(value) == hi - lo and value == installed[lo - BASE:hi - BASE], (hex(lo), hex(hi))
    return value


def native_return_sites(rom, functions):
    calls, pointers = defaultdict(list), defaultdict(list)
    for component, base, raw in graph.loaded_components(rom):
        for i, (value,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
            pc = base + 4 * i
            if value & ~1 in functions:
                pointers[value & ~1].append((component, pc, value))
            if value >> 28 == 15 or value & 0x0E000000 != 0x0A000000:
                continue
            relative = value & 0xFFFFFF
            if relative & 0x800000:
                relative -= 1 << 24
            target = pc + 8 + 4 * relative
            if target in functions:
                calls[target].append((component, pc, value))
    return dict(calls), dict(pointers)


def class_name(arm, address):
    type_info = word(arm, address - 4)
    name = word(arm, type_info + 4)
    return c_string(arm, name, limit=64)[:-1].decode("ascii")


def virtual_tables(arm):
    sources = defaultdict(list)
    for i, (value,) in enumerate(iter_unpack("<I", arm[:len(arm) & ~3])):
        at = BASE + 4 * i
        if at >= 0x02120000 and value in ANCHORS:
            owner = at - ANCHORS[value]
            name = class_name(arm, owner)
            assert name and name[0].isdigit(), (hex(owner), name)
            sources[owner].append(dict(anchor=at, slot=ANCHORS[value], method=value))
    return {at: dict(address=at, class_name=class_name(arm, at), input_dispatch=word(arm, at + 0x54),
                     help_getter=word(arm, at + 0x8C), exact_vtable_hex=arm[at - BASE - 8:at - BASE + 0x94].hex(),
                     anchors=anchors) for at, anchors in sorted(sources.items())}


def assembler(raw, address):
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    return {ins.address: (ins.mnemonic, ins.op_str) for ins in engine.disasm(raw, address)}


def producer_ranges(clean_rom, installed_rom, source, arm):
    targets = {STACK_CTOR, CREW_CTOR, CREW_WRAPPER, 0x020C98F0, 0x020C7E74}
    calls, pointers = native_return_sites(clean_rom, targets)
    assert (calls, pointers) == native_return_sites(installed_rom, targets)
    assert len(calls[0x020C7E74]) == 11 and len(pointers[0x020C7E74]) == 195
    cut = {}
    menu = {}
    for area, pc, _ in calls[STACK_CTOR]:
        assert area == "arm9_section_0"
        asm = assembler(span(source, arm, pc - 4, pc + 4), pc - 4)[pc - 4]
        if pc == 0x0203FB14:
            assert asm == ("mov", "r1, fp")
            assert assembler(span(source, arm, 0x0203FB00, 0x0203FB04), 0x0203FB00)[0x0203FB00] == ("mov", "fp, #0x8c")
            value = 140
            cut[0x0203FB00] = span(source, arm, 0x0203FB00, pc + 4).hex()
        else:
            assert asm[0] == "mov" and asm[1].startswith("r1, #")
            value = int(asm[1].split("#")[1], 0)
            cut[pc - 4] = span(source, arm, pc - 4, pc + 4).hex()
        menu[pc] = value
    assert len(menu) == 18 and not pointers.get(STACK_CTOR)
    assert [(area, pc) for area, pc, _ in calls[0x020C98F0]] == [("arm9_section_0", 0x020C98B8)]
    assert not pointers.get(0x020C98F0)
    assert [(area, pc) for area, pc, _ in calls[CREW_CTOR]] == [("arm9_section_0", 0x0201DC1C)]
    assert not pointers.get(CREW_CTOR)
    crew = {}
    for area, pc, _ in calls[CREW_WRAPPER]:
        assert area == "arm9_section_0"
        raw = span(source, arm, pc - 4, pc + 4)
        mnemonic, ops = assembler(raw, pc - 4)[pc - 4]
        assert mnemonic == "mov" and ops.startswith("r1, #")
        crew[pc] = int(ops.split("#")[1], 0)
        cut[pc - 4] = raw.hex()
    assert len(crew) == 5 and set(crew.values()) == {15, 139}
    pointer, = pointers[CREW_WRAPPER]
    assert pointer == ("arm9_section_0", 0x02034C94, CREW_WRAPPER)
    thunk = span(source, arm, 0x02034C84, 0x02034C98)
    assert assembler(thunk, 0x02034C84)[0x02034C8C] == ("mov", "r1, #0x8b")
    cut[0x02034C84] = thunk.hex()
    crew[0x02034C90] = 139
    for lo, hi in ((STACK_CTOR, 0x020C9904), (CREW_CTOR, 0x020202B0), (CREW_WRAPPER, 0x0201DC20),
                   (0x020C7EAC, 0x020C7EE8)):
        cut[lo] = span(source, arm, lo, hi).hex()
    return dict(menu_context_constructor_calls=menu, crew_constructor_wrapper_sources=crew, code_spans=cut,
                direct_input_dispatch_calls=calls[0x020C7E74], bound_stack_push_call=0x020C98B8)


def method_body(source, arm, address, target, kind):
    code = {}
    shift = 0
    if target is not None:
        raw = span(source, arm, address, address + 16)
        ins = assembler(raw, address)
        assert ins[address] == ("ldr", "ip, [pc, #4]") and ins[address + 4] == ("add", "r0, r0, ip")
        assert ins[address + 8] == ("b", f"#{target:#x}")
        shift, = unpack_from("<i", raw, 12)
        code[address] = raw.hex()
    body = target or address
    size = {"disabled": 8, "constant": 8, "crew": 12, "context stack": 20, "ocean mode": 48,
            "ocean scene": 56, "organize load": 20, "proxy fleet": 24}[kind]
    code[body] = span(source, arm, body, body + size).hex()
    if kind == "context stack":
        assert word(arm, body + 12) == 0x020C98C8 and word(arm, body + 16) == 0x022CF784
        code[0x020C98C8] = span(source, arm, 0x020C98C8, 0x020C98DC).hex()
    return body, shift, code


def execute_methods(source, arm, raw, methods, producers):
    cpu, get = get_machine(arm, raw)
    def live(at, *args):
        return get(at - BASE, *args)

    contexts = live(0x020903AC)
    original_context = bytes(cpu.mem_read(contexts + 8, 8))
    original_stack = bytes(cpu.mem_read(STACK_GLOBAL, 4))
    proofs = {}
    for entry in sorted(methods):
        target, kind = GETTER_TYPES[entry]
        body, shift, code = method_body(source, arm, entry, target, kind)
        arg = OBJECT - shift
        result = []
        if kind in ("constant", "disabled"):
            expected = NO_TOPIC if kind == "disabled" else VALUES[body]
            assert live(entry, arg) == expected
            result.append(dict(topic=expected))
        elif kind == "context stack":
            cpu.mem_write(STACK_GLOBAL, bytes(4))
            assert live(entry, arg) == NO_TOPIC
            result.append(dict(empty=True, topic=NO_TOPIC))
            # The original constructor supplies each bounded stock topic.
            for ident in sorted(set(producers["menu_context_constructor_calls"].values())):
                node = OBJECT + 0x7F00
                assert live(STACK_CTOR, node, ident) == node
                assert bytes(cpu.mem_read(STACK_GLOBAL, 4)) == pack("<I", node)
                assert live(entry, arg) == ident
                live(0x020C987C, node)
                assert bytes(cpu.mem_read(STACK_GLOBAL, 4)) == bytes(4)
                result.append(dict(stock_constructor_topic=ident, topic=ident))
            cpu.mem_write(STACK_GLOBAL, original_stack)
        elif kind == "ocean scene":
            for a, b, expected in ((1, 0, 89), (1, 1, 89), (0, 1, 84), (0, 0, 82), (2, 2, 82)):
                cpu.mem_write(contexts + 8, pack("<2I", a, b))
                assert live(entry, arg) == expected
                result.append(dict(scene_fields=[a, b], topic=expected))
            cpu.mem_write(contexts + 8, original_context)
        else:
            offset, samples = {
                "crew": (0x6F38, [(topic, topic) for topic in sorted(set(producers["crew_constructor_wrapper_sources"].values()))]),
                "ocean mode": (0x74, [(0, 85), (1, 87), (2, 86), (NO_TOPIC, 86)]),
                "organize load": (0x10, [(0, 79), (1, NO_TOPIC), (NO_TOPIC, NO_TOPIC)]),
                "proxy fleet": (0x7564, [(0, 71), (1, 66), (NO_TOPIC, 66)]),
            }[kind]
            for value, expected in samples:
                cpu.mem_write(OBJECT + offset, pack("<I", value))
                assert live(entry, arg) == expected
                result.append(dict(receiver_field=offset, stock_value_or_branch_sample=value, topic=expected))
        proofs[entry] = dict(kind=kind, tail_target=target, receiver_adjustment=shift, source_and_installed_code=code,
                            checked_cases=result, view_tables=methods[entry])
    assert bytes(cpu.mem_read(STACK_GLOBAL, 4)) == original_stack
    assert bytes(cpu.mem_read(contexts + 8, 8)) == original_context
    return proofs


def main():
    release, known = map(read, (current.RELEASE, graph.OUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == known["candidate_sha256"] == release["candidate_sha256"]
    clean, installed = map(NdsImage.open, (CLEAN, current.ROM))
    source, arm = (image.read_file(current.ARM) for image in (clean, installed))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    startup = Path(release["own_registered_startup"])
    assert digest(startup) == release["own_registered_startup_sha256"]
    snapshot = read(startup)["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert sha256(raw).hexdigest() == snapshot["sha256"] and snapshot["read_only_export"]
    tables = virtual_tables(source)
    active = virtual_tables(arm)
    assert active == virtual_tables(raw[:len(arm)]) and active.keys() == tables.keys() and len(tables) == 329
    names = {address: [row["class_name"], active[address]["class_name"]]
             for address, row in tables.items() if row["class_name"] != active[address]["class_name"]}
    assert names == {0x021501E8: ["15CSelectBirthDay", "15CSelectBirthday"]}
    assert all(row | {"class_name": active[address]["class_name"]} == active[address] for address, row in tables.items())
    by_method = defaultdict(list)
    for address, row in tables.items():
        by_method[row["help_getter"]].append(address)
    assert set(by_method) == set(GETTER_TYPES)
    producers = producer_ranges(clean, installed, source, arm)
    checks = execute_methods(source, arm, raw, by_method, producers)
    topics = sorted({case["topic"] for row in checks.values() for case in row["checked_cases"]} - {NO_TOPIC})
    assert topics and max(topics) < 202 and not ({203, 205} & set(topics))
    prior = read(graph.OUT.with_name("lisbon_salt_and_trade_help_20261124.json"))
    assert prior["candidate_sha256"] == release["candidate_sha256"] and prior["ordinary_gameplay"]
    assert prior["Help_direct_trade_article"] == 22 and prior["Help_linked_continuation"] == 212
    trade, = [row for row in tables.values() if row["class_name"] == "12CTradingView" and row["help_getter"] == 0x020C533C]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], active_archive=reference(graph.OUT),
        startup=reference(startup), snapshot=snapshot, native_view_table_census=list(tables.values()),
        method_proofs=checks, producer_ranges=producers, all_observed_or_bounded_direct_topic_values=topics,
        exact_same_vtable_bytes=True, type_name_string_correction=names,
        trade_view_gameplay_binding=dict(view=trade, direct_topic=22, continuation_topic=212,
                                        gameplay=reference(graph.OUT.with_name("lisbon_salt_and_trade_help_20261124.json"))),
        slot_205_scope="Help links and the 329 inventoried native view tables exclude slot 205. Its source text is displayed by the original widget through the linked continuation 204.",
        other_unenumerated_virtual_or_indirect_references_provably_absent=False,
        offline_native_verification=True, new_gameplay_runs=0, ROM_changed=False, new_editorial_credit=0))
    print(f"Verified {len(tables)} native view tables, {len(checks)} getters, and {len(topics)} bounded Help topics.")


if __name__ == "__main__":
    main()
