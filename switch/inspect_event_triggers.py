"""Inspect Switch WE event records without changing their condition tables."""

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import struct


HEADER_SIZE = 96


@dataclass(frozen=True)
class EventRecord:
    event_id: int
    group: int
    offset: int
    selector: int
    context: int
    action: int
    arguments: bytes


def read_event_records(archive):
    if len(archive) < HEADER_SIZE or archive[:2] != b"WE":
        raise ValueError("Expected a Switch WE event archive.")
    payload_size, = struct.unpack_from("<I", archive, 4)
    total, *counts = struct.unpack_from("<10H", archive, 8)
    offsets = struct.unpack_from("<14I", archive, 40)
    if (payload_size != len(archive) - HEADER_SIZE or offsets[0] != 0
            or sorted(offsets) != list(offsets) or offsets[-1] != payload_size
            or sum(counts) != total):
        raise ValueError("The event archive directory is invalid.")
    records = []
    for group, count in enumerate(counts):
        # Each group offset precedes the first event ID by one halfword.
        start = HEADER_SIZE + offsets[group] + 2
        stop = HEADER_SIZE + offsets[group + 1] + 2
        if (start == stop) != (count == 0):
            raise ValueError(f"Event group {group} has an invalid count.")
        for _ in range(count):
            if start + 6 > stop:
                raise ValueError(f"Truncated event header in group {group}.")
            event_id, words, selector, context, action = struct.unpack_from("<H4B", archive, start)
            end = start + words * 4
            if event_id != len(records) + 1 or words < 2 or end > stop:
                raise ValueError(f"Unexpected event boundary at {start:#x}.")
            records.append(EventRecord(event_id, group, start, selector, context,
                                       action, archive[start + 6:end]))
            start = end
        if start != stop:
            raise ValueError(f"Event records do not fill group {group}.")
    return records


def describe(record, value=None):
    positions = []
    if value is not None:
        needle = struct.pack("<H", value)
        positions = [record.offset + 6 + index for index in range(len(record.arguments) - 1)
                     if record.arguments[index:index + 2] == needle]
        if not positions:
            return None
    return {
        "event": record.event_id,
        "group": record.group,
        "file_offset": hex(record.offset),
        "selector": record.selector,
        "context": record.context,
        "action": hex(record.action),
        "arguments_hex": record.arguments.hex(" "),
        "candidate_value_offsets": [hex(position) for position in positions],
    }


def branch_target(index, table):
    if index in (0, 0x3FFF):
        return None
    if not index < len(table):
        raise ValueError(f"Event action index {index} is outside the action table.")
    entry = table[index]
    return entry & 0xFFF if (entry >> 12) & 3 == 2 else None


def scenario_triggers(archive, block, records):
    start, end = struct.unpack_from("<2I", archive, 0x4C)
    payload = archive[HEADER_SIZE + start:HEADER_SIZE + end]
    if len(payload) % 2:
        raise ValueError("The action table contains a partial entry.")
    table = [entry for entry, in struct.iter_unpack("<H", payload)]
    matches = []
    for record in records:
        header, = struct.unpack_from("<I", archive, record.offset - 2)
        passed = branch_target((header >> 16) & 0x3FFF, table)
        failed = branch_target(header & 0x3FFF, table)
        if block not in (passed, failed):
            continue
        detail = describe(record)
        detail.update(scenario_block=block, when_condition_passes=passed == block,
                      when_condition_fails=failed == block)
        if record.action & 1:
            absent, required = record.arguments[:2]
            count = required + absent
            if 2 + 2 * count > len(record.arguments):
                raise ValueError(f"Event {record.event_id} has a truncated prerequisite list.")
            event_indices = struct.unpack_from(f"<{count}H", record.arguments, 2)
            detail["required_completed_event_ids"] = [index + 1 for index in event_indices[:required]]
            detail["required_incomplete_event_ids"] = [index + 1 for index in event_indices[required:]]
        matches.append(detail)
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", type=Path, nargs="+")
    requested = parser.add_mutually_exclusive_group()
    requested.add_argument("--event", type=int)
    requested.add_argument("--argument-value", type=int)
    requested.add_argument("--scenario-block", type=int, help="Find branches to this scenario block.")
    args = parser.parse_args()
    if args.argument_value is not None and not 0 <= args.argument_value <= 0xFFFF:
        parser.error("Use an unsigned 16-bit argument value.")
    if args.scenario_block is not None and not 0 <= args.scenario_block <= 0xFFF:
        parser.error("Use a scenario block between 0 and 4095.")
    for path in args.archives:
        archive = path.read_bytes()
        records = read_event_records(archive)
        selected = [record for record in records if args.event is None or record.event_id == args.event]
        report = {"archive": str(path), "event_count": len(records)}
        if args.scenario_block is not None:
            report["records"] = scenario_triggers(archive, args.scenario_block, records)
        elif args.event is not None or args.argument_value is not None:
            report["records"] = [match for record in selected
                                 if (match := describe(record, args.argument_value)) is not None]
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
