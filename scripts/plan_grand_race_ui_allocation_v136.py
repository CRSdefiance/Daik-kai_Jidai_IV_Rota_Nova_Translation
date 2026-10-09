"""Research allocation for complete Grand Race UI prose; never write a ROM."""

import hashlib
import json
import struct
from bisect import bisect_right
from pathlib import Path

from dk4tool.patch.grand_race_waiting_widget import rewrite_function
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_waiting_widgets import TABLE, execute
from scripts.prepare_grand_race_remaining_ui_manuscript import (
    BASE,
    CANONICAL,
    CANONICAL_SHA,
    CLEAN_ARM9_SHA,
)
from scripts.probe_grand_race_wireless_return import balanced_lines

CANDIDATE = Path("out/all_routes_combined_v136_candidate.nds")
CANDIDATE_SHA = "967343c300ce23cc1665ee497b1a85f734460f9ca71aa1f3bee479027d96ca6c"
FIXED_BATCHES = (
    "translations/grand_race_transition_status_arm9_v2.json",
    "translations/grand_race_menu_arm9_v2.json",
)

ALIASES = {"TITLE": 0x137A98, "BASIC_RULES": 0x1379CC, "ABOUT": 0x137AA8}


def merge_ranges(ranges):
    merged = []
    for lo, hi in sorted(ranges):
        if lo >= hi:
            raise ValueError("Invalid owned source range")
        if merged and lo < merged[-1][1]:
            raise ValueError("Overlapping source owners")
        if merged and lo == merged[-1][1]:
            merged[-1][1] = hi
        else:
            merged.append([lo, hi])
    return merged


def allocate(entries, free):
    """Bounded bin packing; preserve full strings even when greedy fitting fails."""
    spans = [list(span) for span in free]
    ordered = sorted(entries, key=lambda entry: (-len(entry[1]), entry[0]))
    failed, result = set(), {}
    visits = 0

    def search(index):
        nonlocal visits
        visits += 1
        if visits > 500000:
            raise ValueError("Allocation search limit reached; no incomplete plan may ship")
        if index == len(ordered):
            return True
        capacities = tuple(sorted(hi - lo for lo, hi in spans))
        state = (index, capacities)
        if state in failed:
            return False
        key, raw = ordered[index]
        choices = sorted(
            (hi - lo, lo, slot) for slot, (lo, hi) in enumerate(spans) if hi - lo >= len(raw)
        )
        tried = set()
        for capacity, offset, slot in choices:
            if capacity in tried:
                continue
            tried.add(capacity)
            spans[slot][0] += len(raw)
            result[key] = offset
            if search(index + 1):
                return True
            spans[slot][0] = offset
            result.pop(key)
        failed.add(state)
        return False

    if sum(len(raw) for _, raw in entries) > sum(hi - lo for lo, hi in spans) or not search(0):
        raise ValueError("Complete strings do not fit the owned pool; relocation must expand")
    return result, [span for span in spans if span[0] < span[1]]


def subtract_ranges(ranges, reserved):
    free = [list(span) for span in ranges]
    for start, end in reserved:
        next_free = []
        for lo, hi in free:
            if end <= lo or start >= hi:
                next_free.append([lo, hi])
            else:
                if lo < start:
                    next_free.append([lo, start])
                if end < hi:
                    next_free.append([end, hi])
        free = next_free
    return free


def byte_pointer_references(arm9, ranges):
    """Find literal ARM9 pointers into owned spans at every byte position."""
    ranges = merge_ranges(ranges)
    starts = [lo for lo, _ in ranges]
    found = {}
    for field in range(len(arm9) - 3):
        target = struct.unpack_from("<I", arm9, field)[0] - BASE
        index = bisect_right(starts, target) - 1
        if index >= 0 and target < ranges[index][1]:
            found[field] = target
    return found


def main():
    for path, expected in ((CANONICAL, CANONICAL_SHA), (CANDIDATE, CANDIDATE_SHA)):
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError("Pinned input ROM differs")
    sources = [
        NdsImage.open(path).read_file("/__arm9__.bin")
        for path in ("work/clean.nds", CANONICAL, CANDIDATE)
    ]
    if hashlib.sha256(sources[0]).hexdigest() != CLEAN_ARM9_SHA:
        raise ValueError("Clean Japanese ARM9 differs")
    original = sources[2]
    manuscript_path = Path("translations/grand_race_remaining_ui_manuscript_v2.json")
    manuscript = json.loads(manuscript_path.read_text(encoding="utf-8"))
    rows = {row["id"].removeprefix("GRAND_RACE_UI_"): row for row in manuscript["records"]}
    parts = [part for row in rows.values() for part in row["source_parts_in_reading_order"]]
    if len(rows) != 51 or len(parts) != 59:
        raise ValueError("Complete scoped manuscript changed")
    fixed = {}
    for batch_path in FIXED_BATCHES:
        batch = json.loads(Path(batch_path).read_text(encoding="utf-8"))
        for row in batch["records"]:
            name = row["id"].removeprefix("GRAND_RACE_UI_")
            fixed[name] = row
    if len(fixed) != 8:
        raise ValueError("All eight inherited messages must be pinned")
    reserved = [
        (r["offset"], r["offset"] + len(bytes.fromhex(r["source_hex"]))) for r in fixed.values()
    ]
    ranges, expected_refs = [], {}
    for name, row in rows.items():
        for part in row["source_parts_in_reading_order"]:
            lo, size = part["offset"], part["aligned_source_bytes_including_nul"]
            raw = bytes.fromhex(part["source_hex"])
            if any(
                source[lo : lo + size] != raw + bytes(size - len(raw)) for source in sources[:2]
            ):
                raise ValueError("Source text/padding differs")
            expected_current = (
                fixed[name]["english"].encode("ascii").ljust(size, b"\0")
                if name in fixed
                else raw.ljust(size, b"\0")
            )
            if original[lo : lo + size] != expected_current:
                raise ValueError("Current V136 source or inherited English differs")
            ranges.append((lo, lo + size))
            for field in part["aligned_pointer_fields"]:
                if any(
                    struct.unpack_from("<I", source, field)[0] != BASE + lo for source in sources
                ):
                    raise ValueError("Original pointer selection differs")
                expected_refs[field] = lo
    shared_headings = []
    for name, start, size, field in (
        ("BASIC_RULES", 0x1379CC, 12, 0x1152DC),
        ("ABOUT", 0x137AA8, 16, 0x1152CC),
    ):
        raw = fixed[name]["english"].encode("ascii") + b"\0"
        if any(source[start : start + size] != raw.ljust(size, b"\0") for source in sources[2:]):
            raise ValueError("Complete duplicate help heading differs")
        if any(struct.unpack_from("<I", source, field)[0] != BASE + start for source in sources):
            raise ValueError("Help heading descriptor differs")
        # Exhaustive byte-position literal-pointer scan, including interior targets.
        actual = byte_pointer_references(original, [(start, start + size)])
        if actual != {field: start}:
            raise ValueError("Duplicate heading has an unmapped reference")
        expected_refs[field] = start
        ranges.append((start, start + size))
        shared_headings.append(
            {
                "message": name,
                "old_offset": start,
                "size": size,
                "descriptor_field": field,
                "new_offset": fixed[name]["offset"],
                "english": fixed[name]["english"],
                "clean_source_hex": sources[0][start : start + size].hex(),
                "inherited_source_hex": original[start : start + size].hex(),
            }
        )
    owned = merge_ranges(ranges)
    # Reconcile all literal pointers, including unaligned fields and interior targets.
    actual_refs = byte_pointer_references(original, owned)
    if actual_refs != expected_refs:
        extra = {
            hex(field): hex(target)
            for field, target in actual_refs.items()
            if expected_refs.get(field) != target
        }
        missing = sorted(hex(field) for field in expected_refs.keys() - actual_refs.keys())
        raise ValueError(
            f"Unmapped literal references: {extra}; missing expected fields: {missing}"
        )
    role_report = json.loads(
        Path("work/qa/grand_race_wireless_roles/report.json").read_text(encoding="utf-8")
    )
    if (
        role_report["manuscript_sha256"] != hashlib.sha256(manuscript_path.read_bytes()).hexdigest()
        or not role_report["preview_reviewed"]
    ):
        raise ValueError("Role allocation requires the current reviewed complete prose")
    proposed, code_changes = rewrite_function(original)
    proposed = bytearray(proposed)
    for lo, hi in subtract_ranges(owned, reserved):
        proposed[lo:hi] = bytes(hi - lo)
    for heading in shared_headings:
        struct.pack_into("<I", proposed, heading["descriptor_field"], BASE + heading["new_offset"])
    selections, entries = [], []
    for name, row in rows.items():
        source_parts = row["source_parts_in_reading_order"]
        count = 3 if name == "HOST_SELECTING" else len(source_parts)
        lines = (
            [selection["line"] for selection in role_report["selections"]]
            if name == "ROLES"
            else balanced_lines(row["english"], count)
        )
        if " ".join(lines) != row["english"]:
            raise ValueError("Formatted text changes full prose")
        for index, line in enumerate(lines):
            raw = line.encode("ascii") + b"\0"
            selection = {
                "key": f"{name}:{index}",
                "message": name,
                "line": line,
                "raw_hex": raw.hex(),
                "pointer_fields": source_parts[index]["aligned_pointer_fields"]
                if index < len(source_parts)
                else [],
            }
            if name in fixed:
                if row["english"] != fixed[name]["english"]:
                    raise ValueError("Inherited full English differs from manuscript")
                selection["offset"] = fixed[name]["offset"]
                selection["inherited_from_V136"] = True
            elif name == "ROLES":
                if raw.hex() != role_report["selections"][index]["replacement_hex"][: len(raw) * 2]:
                    raise ValueError("Reviewed role line differs")
                entries.append((selection["key"], raw))
            elif name == "RETURN_MENU":
                selection["offset"] = 0x16B93C + sum(
                    len(previous["line"]) + 1
                    for previous in selections
                    if previous["message"] == name
                )
            elif name in ALIASES:
                selection["offset"] = ALIASES[name]
                if original[selection["offset"] : selection["offset"] + len(raw)] != raw:
                    raise ValueError("Shared title is not exactly identical and terminated")
                selection["alias_sha256"] = hashlib.sha256(raw).hexdigest()
            else:
                entries.append((selection["key"], raw))
            selections.append(selection)
    # A complete identical native line can be shared without changing prose.
    # Prefer fixed/previously existing selections so duplicate fragments consume
    # no further owned bytes (e.g. the two "Touch the lower screen" instructions).
    representatives = {}
    entries = []
    for selection in sorted(
        selections, key=lambda selection: ("offset" not in selection, selection["key"])
    ):
        raw = bytes.fromhex(selection["raw_hex"])
        if raw in representatives:
            selection["shared_key"] = representatives[raw]["key"]
        else:
            representatives[raw] = selection
            if "offset" not in selection:
                entries.append((selection["key"], raw))
    free = subtract_ranges(owned, reserved + [(0x16B93C, 0x16B980), (TABLE, TABLE + 12)])
    try:
        allocations, unused = allocate(entries, free)
    except ValueError:
        output = Path("work/analysis/grand_race_ui_allocation_v136")
        output.mkdir(parents=True, exist_ok=True)
        demand = sum(len(raw) for _, raw in entries)
        capacity = sum(hi - lo for lo, hi in free)
        failure = {
            "status": "complete-prose-allocation-requires-expanded-ownership",
            "candidate_sha256": CANDIDATE_SHA,
            "rom_written": False,
            "inherited_reserved_spans": reserved,
            "inherited_message_count": len(fixed),
            "remaining_message_count": len(rows) - len(fixed),
            "required_unique_string_bytes": demand,
            "available_bytes": capacity,
            "minimum_extra_bytes": max(0, demand - capacity),
            "free_ranges": free,
            "entries": [{"key": key, "bytes": len(raw)} for key, raw in entries],
            "limitation": "Total capacity or fragmentation prevents a complete allocation; no truncation permitted.",
        }
        (output / "capacity_failure.json").write_text(json.dumps(failure, indent=2) + "\n")
        print(
            json.dumps(
                {
                    key: value
                    for key, value in failure.items()
                    if key not in ("entries", "free_ranges", "inherited_reserved_spans")
                },
                indent=2,
            )
        )
        return
    by_key = {selection["key"]: selection for selection in selections}
    for selection in selections:
        if "shared_key" not in selection:
            selection["offset"] = selection.get("offset", allocations.get(selection["key"]))
    for selection in selections:
        offset = (
            by_key[selection["shared_key"]]["offset"]
            if "shared_key" in selection
            else selection["offset"]
        )
        selection["offset"] = offset
        raw = bytes.fromhex(selection["raw_hex"])
        proposed[offset : offset + len(raw)] = raw
        for field in selection["pointer_fields"]:
            struct.pack_into("<I", proposed, field, BASE + offset)
    if TABLE & 3 or not any(lo <= TABLE and TABLE + 12 <= hi for lo, hi in owned):
        raise ValueError("Extra table is outside owned aligned source data")
    if any(
        selection["offset"] < TABLE + 12
        and TABLE < selection["offset"] + len(bytes.fromhex(selection["raw_hex"]))
        for selection in selections
    ):
        raise ValueError("Extra table overlaps complete prose")
    host = [selection for selection in selections if selection["message"] == "HOST_SELECTING"]
    for index, selection in enumerate(host):
        struct.pack_into("<I", proposed, TABLE + index * 4, BASE + selection["offset"])
    struct.pack_into("<I", proposed, 0xF89DC, BASE + TABLE)
    execution = execute(
        proposed, tuple(BASE + selection["offset"] for selection in host), scratch_table=False
    )
    for selection in selections:
        offset = selection["offset"]
        saved = bytes(proposed[offset : proposed.index(0, offset)])
        if saved.decode("ascii") != selection["line"]:
            raise ValueError("Saved allocation lost a leading character or string boundary")
        for field in selection["pointer_fields"]:
            if struct.unpack_from("<I", proposed, field)[0] != BASE + offset:
                raise ValueError("Saved text pointer differs")
    allowed = (
        owned
        + [[field, field + 4] for field in expected_refs]
        + [[change["offset"], change["offset"] + 4] for change in code_changes]
        + [[0xF89DC, 0xF89E0]]
    )
    if len(proposed) != len(original):
        raise ValueError("Research plan changes ARM9 size")
    changed = [
        offset
        for offset, (old, new) in enumerate(zip(original, proposed, strict=True))
        if old != new
    ]
    if any(not any(lo <= offset < hi for lo, hi in allowed) for offset in changed):
        raise ValueError("Research allocation changed unrelated bytes")
    for heading in shared_headings:
        selected = struct.unpack_from("<I", proposed, heading["descriptor_field"])[0] - BASE
        if (
            bytes(proposed[selected : proposed.index(0, selected)]).decode("ascii")
            != heading["english"]
        ):
            raise ValueError("Shared help heading loses complete original English")
    for lo, hi in reserved:
        if proposed[lo:hi] != original[lo:hi]:
            raise ValueError("Allocation overwrites an inherited V136 slot")
    output = Path("work/analysis/grand_race_ui_allocation_v136")
    output.mkdir(parents=True, exist_ok=True)
    report = {
        "status": "research-complete-prose-allocation-not-release-ready",
        "rom_written": False,
        "manuscript_sha256": hashlib.sha256(manuscript_path.read_bytes()).hexdigest(),
        "candidate_sha256": CANDIDATE_SHA,
        "owned_ranges": owned,
        "inherited_message_count": len(fixed),
        "remaining_message_count": len(rows) - len(fixed),
        "inherited_reserved_spans": reserved,
        "inherited_slots_byte_exact": True,
        "shared_complete_help_headings": shared_headings,
        "duplicate_heading_bytes_reclaimed": sum(r["size"] for r in shared_headings),
        "all_byte_position_literal_references_reconciled": True,
        "literal_reference_count": len(actual_refs),
        "owned_bytes": sum(hi - lo for lo, hi in owned),
        "unused_pool_ranges": unused,
        "selections": selections,
        "extra_table": [TABLE, TABLE + 12],
        "bounded_native_execution": execution,
        "changed_byte_count": len(changed),
        "limitations": [
            "All byte-position literal pointers reconciled; computed/dynamic references still require consumer proof.",
            "Complete headings now share fixed V136 menu labels; revised help ownership/profile gates pending.",
            "Other menu/wireless screen consumers and exact-font layouts still pending.",
            "Full screen composition and gameplay are not verified.",
            "No build batch, ROM or completion/progress credit generated.",
        ],
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(
        f"{len(rows)} messages / {len(selections)} saved strings; {report['owned_bytes']} owned bytes; allocation and native third-widget execution pass; no ROM written"
    )


if __name__ == "__main__":
    main()
