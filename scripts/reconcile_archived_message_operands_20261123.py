"""Classify the five archived COMMON numbers found in shipped SC and EV resources."""

from collections import Counter
from hashlib import sha256
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts.checkpoint_story_still_commands_20261120 import explicit_walk
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, COMMON, OUT
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_story_artwork_inventory_20261123 import DECODER_SPANS
from scripts.register_recruitment_shortfall_20261123 import RELEASE
from scripts.research_unmapped_shop_references_v1688 import occurrences
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_lisbon_azores_voyage_20261123 import town
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


KEYS = (284, 318, 750, 751, 752)
REPORT = OUT.with_name("archived_message_operands_20261123.json")
SHARED = OUT.with_name("shared_editorial_coverage_20261123.json")
EVENTS = OUT.with_name("retail_event_coverage_current_20261123.json")
SPANS = (*DECODER_SPANS, (0x21FC4, 0x2201C), (0x22C9C, 0x22CE0),
         (0x23840, 0x23928), (0x23E04, 0x23FFC), (0x2472C, 0x24900),
         (0x256A0, 0x257C0), (0x3CB30, 0x3CBB8))
RELATION, EVENT_CONDITION = 0x0203CB30, 0x020256A0
SCRATCH = 0x02450000


def matches(raw):
    return sorted((at, key) for key in KEYS for at in occurrences(raw, pack("<H", key)))


def scene_owner(walk, arm, block, lo, hi, hits):
    nested = block[:4] + pack("<2H", hi - lo, 0) + block[lo:hi]
    trace = walk(arm, nested)
    assert trace["error"] is None
    starts = {lo + row["offset"] - 8: row for row in trace["rows"]}
    predicate_hits = {row["source_offset"] for row in trace["opaque_effect_bridges"]
                      if row["PC"] == EVENT_CONDITION}
    for at, key in hits:
        offset = max(start for start in starts if start <= at)
        record = starts[offset]
        opcode, extent = record["word"], record["native_extent"]
        end = offset + extent
        assert at + 2 <= end
        delta = at - offset
        row = dict(offset=at, value=key, command_offset=offset, opcode=f"{opcode:04X}",
                   command_extent=extent, command_hex=block[offset:(end if extent <= 8 else offset + 20)].hex())
        if opcode == 0x0100 and delta >= 4:
            yield from scene_owner(walk, arm, block, offset + 4, end, [(at, key)])
        elif opcode in (0x0300, 0x0400) and delta == 2:
            destination = offset + 4 + key
            assert extent == 4 and offset + extent <= destination <= hi
            row.update(kind="relative branch length", relative_destination=destination)
            yield row
        elif opcode == 0x0100 and delta == 2:
            assert end == offset + 4 + key
            yield row | dict(kind="embedded command length")
        elif opcode == 0x4100 and 2 <= delta < 18 and delta % 2 == 0:
            index = (delta - 2) // 2
            assert unpack_from("<8H", block, offset + 2)[index] == key and offset + 20 + key < end
            yield row | dict(kind="personality variant text offset", style_slot=index, body_offset=offset + 20 + key)
        elif opcode == 0x8000 and delta == 5:
            # This hit spans two fields of the packed predicate operand.
            operand, = unpack_from("<I", block, offset + 4)
            assert extent == 8 and record["offset"] in predicate_hits and operand == 0x70011C1C
            yield row | dict(kind="overlap within a native predicate word", packed_predicate=f"{operand:08X}")
        else:
            raise AssertionError((at, key, opcode, delta))


def scenes(image, path, walk):
    archive = image.read_file(path)
    arm = image.read_file(ARM)
    rows, counts = [], Counter()
    blocks = IlnkContainer.parse(archive).blocks
    for number, block in enumerate(blocks):
        selected = matches(block)
        if not selected:
            continue
        assert block[:4] in (b"CS\0\1", b"CS\1\1")
        length, = unpack_from("<H", block, 4)
        limit = 8 + length
        assert limit <= len(block) and not any(block[limit:])
        header_hits = [dict(offset=at, value=key, kind="scene header length")
                       for at, key in selected if at < 8 and at == 4 and key == length]
        body_hits = [(at, key) for at, key in selected if 8 <= at < limit]
        assert len(header_hits) + len(body_hits) == len(selected)
        found = list(scene_owner(walk, arm, block, 8, limit, body_hits)) if body_hits else []
        assert sorted((row["offset"], row["value"]) for row in header_hits + found) == selected
        for row in header_hits + found:
            counts[row["kind"]] += 1
            rows.append(row | dict(block=number, block_sha256=sha256(block).hexdigest()))
    return dict(blocks=len(blocks), archive_sha256=sha256(archive).hexdigest(), counts=dict(counts), hits=rows)


def events(data):
    entries = parse_events(data)
    action_begin, action_end, conditions, conditions_end = (
        n + 96 for n in unpack_from("<4I", data, 0x4C))
    assert action_begin <= action_end == conditions <= conditions_end <= len(data)
    hits = []
    for at, key in matches(data):
        if conditions <= at < conditions_end:
            index, remainder = divmod(at - conditions, 4)
            word, = unpack_from("<I", data, at)
            assert remainder == 0 and word in (0xA300013E, 0xA310013E)
            hits.append(dict(offset=at, value=key, kind="packed faction relation predicate",
                             condition_index=index, word=word))
            continue
        row, = [r for r in entries if 96 + r["body_offset"] <= at < 96 + r["body_offset"] + r["source_record_bytes"]]
        delta = at - 96 - row["body_offset"]
        if delta == 2:
            assert row["action_index"] == key and action_begin + 2 * key < action_end
            kind = "event action index"
        else:
            assert delta >= 10 and delta % 2 == 0
            dependency = (delta - 10) // 2
            positive, negative = row["must_be_completed"], row["must_not_be_completed"]
            assert (positive + negative)[dependency] == key
            kind = "required event ID" if dependency < len(positive) else "excluded event ID"
        hits.append(dict(offset=at, value=key, kind=kind, event_ID=row["event_ID"],
                         record_byte_index=delta, record_hex=row["source_hex"], script_block=row["script_block"]))
    return dict(archive_sha256=sha256(data).hexdigest(), event_records=len(entries), hits=hits)


def check_conditions(arm, snapshot, conditions):
    cpu, get = get_machine(arm, snapshot)
    calls = []

    def observe(uc, _pc, _size, _data):
        calls.append((uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)))

    companies = get(0xCB160)
    hook = cpu.hook_add(UC_HOOK_CODE, observe, begin=RELATION, end=RELATION)
    results = []
    try:
        for word in sorted(conditions):
            calls.clear()
            cpu.mem_write(SCRATCH, pack("<3I", 0, SCRATCH + 8, word))
            result = get(EVENT_CONDITION - BASE, SCRATCH)
            company = (word >> 16) & 31
            other = (word >> 8) & 31
            expected = [(companies + 4 + 76 * company, other)]
            if company > other:
                expected.append((companies + 4 + 76 * other, company))
            assert calls == expected and result in (0, 1)
            results.append(dict(condition_word=f"{word:08X}", company_slot=company,
                counterpart_slot=other, relation_class=(word >> 5) & 7, result=result, relation_getter_calls=calls.copy()))
        assert bytes(cpu.mem_read(BASE, len(snapshot))) == snapshot
    finally:
        cpu.hook_del(hook)
    return results


def main():
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    clean, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    ja, en = (image.read_file(ARM) for image in (clean, current))
    assert all(ja[lo:hi] == en[lo:hi] for lo, hi in SPANS)
    before = common_message_entries(clean.read_file(COMMON), ja)
    installed = common_rows(current.read_file(COMMON), en)
    records = [row for row in read(SHARED)["records"] if row["message_ID"] in KEYS]
    assert {row["message_ID"] for row in records} == set(KEYS)
    for row in records:
        key = row["message_ID"]
        assert row["source_reference"] == town.reference(before[key]) and row["source_hex"] == before[key].text.hex()
        assert row["installed_reference"] == town.reference(installed[key]) and row["installed_hex"] == installed[key].text.hex()
    paths = [f"/{folder}/SC{route}.DK4" for folder in ("data", "testdata") for route in range(4)]
    walk = explicit_walk()
    original = {path: scenes(clean, path, walk) for path in paths}
    deployed = {path: (scenes(current, path, walk) if path.startswith("/data/")
                       else original[path]) for path in paths}
    assert all(clean.read_file(path) == current.read_file(path) for path in paths if path.startswith("/testdata/"))

    events_data = {}
    for path in clean.path_map():
        if path.lower().startswith(("/data/ev", "/testdata/ev")):
            source = clean.read_file(path)
            assert source == current.read_file(path)
            events_data[path] = events(source)
    assert len(events_data) == 8
    assert sum(data["event_records"] for path, data in events_data.items() if path.startswith("/data/")) == 1307
    for row in read(EVENTS)["scopes"]:
        assert events_data[row["event_file"]]["archive_sha256"] == row["clean_and_installed_event_sha256"]

    snapshot_path = release["own_registered_startup"]
    assert digest(snapshot_path) == release["own_registered_startup_sha256"]
    snapshot = read(snapshot_path)["read_only_snapshot"]
    conditions = {row["word"] for data in events_data.values() for row in data["hits"] if "word" in row}
    assert conditions == {0xA300013E, 0xA310013E}
    predicate_results = check_conditions(en, read_ram(snapshot), conditions)
    original_311, current_311 = (IlnkContainer.parse(image.read_file(paths[1])).blocks[311] for image in (clean, current))
    lead, = [row for row in deployed[paths[1]]["hits"] if row["value"] == 750 and row["kind"] != "scene header length"]
    assert lead["block"] == 311 and lead["command_offset"] == 1202 and lead["relative_destination"] == 1956
    assert original_311[1116:1120] == bytes.fromhex("00031803") and original_311[1908:1912] == bytes.fromhex("00012801")
    assert int.from_bytes(original_311[1118:1120], "little") + 1120 == 1912
    assert current_311[1952:1956] == bytes.fromhex("00011a01")
    destination_prefix = original_311[1912:1918]
    assert destination_prefix == current_311[1956:1962] == bytes.fromhex("7c4695800c63")

    totals = dict(clean_SC_hits=sum(len(group["hits"]) for group in original.values()),
        installed_SC_hits=sum(len(group["hits"]) for group in deployed.values()),
        exact_clean_and_installed_EV_hits=sum(len(group["hits"]) for group in events_data.values()))
    write(REPORT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        search_values=KEYS, all_byte_alignments=True, counts=totals, clean_story=original, installed_story=deployed,
        event_archives=events_data, source_and_installed_COMMON=records,
        hodram_B311=dict(original_command=1116, original_relative_length=792, original_destination=1912,
                        installed_command=1202, installed_relative_length=750, installed_destination=1956,
                        exact_original_and_installed_destination_prefix=destination_prefix.hex()),
        original_event_predicate_cases=predicate_results, snapshot=snapshot,
        exact_code_spans=[dict(start=BASE + lo, end=BASE + hi, sha256=sha256(en[lo:hi]).hexdigest()) for lo, hi in SPANS],
        evidence=[reference(p) for p in (RELEASE, SHARED, EVENTS)], new_gameplay=False, new_editorial_credit=0,
        other_possible_computed_or_indirect_callers_open=True))
    print(totals)


if __name__ == "__main__":
    main()
