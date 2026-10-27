"""Verify saved English, alignment and pointers for mapped B29-B32 items."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.sjis_scan import contains_japanese
from dk4tool.script.common_entry_tables import ITEM_TABLES, native_item_entries
from dk4tool.script.common_message_table import TABLE_OFFSET, common_message_entries


def verify_relocated_items(candidate: Path, profile_name: str, profile: dict,
                           expected: dict, blocks: list[int]) -> dict:
    clean, saved = NdsImage.open('work/clean.nds'), NdsImage.open(candidate)
    common_path, arm9_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
    clean_common, clean_arm9 = clean.read_file(common_path), clean.read_file(arm9_path)
    saved_common, saved_arm9 = saved.read_file(common_path), saved.read_file(arm9_path)
    sources = common_message_entries(clean_common, clean_arm9)
    current = common_message_entries(saved_common, saved_arm9, clean=False)
    config = json.loads(Path(profile['common_native_reblocking']).read_text(encoding='utf-8'))
    if (hashlib.sha256(saved_common).hexdigest() != config['expected_common_sha256']
            or hashlib.sha256(saved_arm9).hexdigest() != config['expected_arm9_sha256']):
        raise ValueError('Saved item relocation differs from registered complete map')
    final_blocks = IlnkContainer.parse(saved_common).blocks
    checks = []
    for block in blocks:
        for item in native_item_entries(clean_common, clean_arm9, block):
            message_id = (item.table_offset - TABLE_OFFSET) // 2
            source, selected = sources[message_id], current[message_id]
            if source.table_offset != item.table_offset or source.text != item.source:
                raise ValueError('Source item identity differs from the native global map')
            key = f'DK4_MES_B{block:02d}_R{item.record_index:04d}'
            declaration = expected[key]
            pos = declaration['entry_offsets'].index(item.start)
            english = declaration['display_entries'][pos]
            if (selected.text.rstrip(b' ') != english.encode('cp932')
                    or contains_japanese(selected.text.decode('cp932'))
                    or b'\n' in selected.text
                    or not selected.text.startswith(english[0].encode('cp932'))):
                raise ValueError(f'Item {item.item_index}: English/first character or native boundary differs')
            # This complete owner was moved byte-for-byte. Validate its raw
            # parent declaration too, not merely a guessed string substring.
            actual_owner = final_blocks[selected.block].split(b'\0')[selected.record_index]
            if actual_owner != bytes.fromhex(declaration['replacement_hex']):
                raise ValueError('Relocated item owner differs from its reviewed parent allocation')
            checks.append({'item_index': item.item_index, 'message_id': message_id,
                           'native_table_offset': item.table_offset, 'new_block': selected.block,
                           'new_record': selected.record_index, 'english': english,
                           'first_character_verified': True})
    return {'status': 'pass', 'candidate': candidate.as_posix(),
            'candidate_sha256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
            'profile': profile_name, 'source_item_blocks': blocks, 'native_entry_count': len(checks),
            'global_native_item_ids_preserved': True, 'relocated_complete_owners_verified': True,
            'native_pointer_offsets_changed_as_mapped': True, 'japanese_records_in_mapped_items': 0,
            'entries': checks}


def verify(candidate: Path, profile_name: str, blocks: list[int], previous: Path | None = None) -> dict:
    stack = json.loads(Path("translations/release_stack.json").read_text(encoding="utf-8"))
    profile = stack["profiles"][profile_name]
    expected = {}
    for name in profile["batches"]:
        batch = json.loads(Path(name).read_text(encoding="utf-8"))
        if batch.get("file_path") == "/COMMON/MESFILE.DK4":
            for row in batch.get("records", []):
                expected[row["id"]] = row
    if profile.get('common_native_reblocking'):
        if previous is not None:
            from scripts.verify_common_native_reblocking import verify as verify_reblock
            verify_reblock(candidate, previous, Path(profile['common_native_reblocking']))
        return verify_relocated_items(candidate, profile_name, profile, expected, blocks)
    clean = NdsImage.open("work/clean.nds")
    saved = NdsImage.open(candidate)
    common_path = "/COMMON/MESFILE.DK4"
    clean_common = clean.read_file(common_path)
    saved_common = saved.read_file(common_path)
    clean_blocks = IlnkContainer.parse(clean_common).blocks
    saved_blocks = IlnkContainer.parse(saved_common).blocks
    clean_arm9 = clean.read_file("/__arm9__.bin")
    saved_arm9 = saved.read_file("/__arm9__.bin")
    checks = []
    checked_record_ids = set()
    unmapped_japanese_records = {}
    for block in blocks:
        table_offset, count, _, _, _ = ITEM_TABLES[block]
        span = slice(table_offset, table_offset + count * 2)
        if saved_arm9[span] != clean_arm9[span]:
            raise ValueError(f"B{block}: native pointer table changed")
        entries = native_item_entries(clean_common, clean_arm9, block)
        rows = saved_blocks[block].split(b"\0")
        clean_rows = clean_blocks[block].split(b"\0")
        if [len(row) for row in rows] != [len(row) for row in clean_rows]:
            raise ValueError(f"B{block}: NUL allocations changed")
        owned_records = {entry.record_index for entry in entries}
        unmapped_japanese_records[block] = sum(
            contains_japanese(row.decode("cp932"))
            for index, row in enumerate(rows) if index not in owned_records
        )
        if any(contains_japanese(rows[index].decode("cp932")) for index in owned_records):
            raise ValueError(f"B{block}: Japanese remains in mapped item records")
        for entry in entries:
            key = f"DK4_MES_B{block:02d}_R{entry.record_index:04d}"
            checked_record_ids.add(key)
            row = expected[key]
            if rows[entry.record_index] != bytes.fromhex(row["replacement_hex"]):
                raise ValueError(f"{key}: saved ROM differs from active layout")
            pos = row["entry_offsets"].index(entry.start)
            table_offsets = row.get("native_table_offsets")
            if table_offsets is None:
                table_offsets = [row["native_table_offset"]]
            if row["entry_ends"][pos] != entry.end or table_offsets[pos] != entry.table_offset:
                raise ValueError(f"{key}: active metadata contradicts native entry")
            text = row["display_entries"][pos]
            actual = rows[entry.record_index][entry.start:entry.end]
            if actual.rstrip(b" ") != text.encode("cp932") or not actual.startswith(text[0].encode("cp932")):
                raise ValueError(f"{key}: native English/first character differs")
            if b"\n" in actual:
                raise ValueError(f"{key}: native entry contains an authored break")
            first = row["entry_offsets"][0]
            if rows[entry.record_index][:first] != clean_rows[entry.record_index][:first]:
                raise ValueError(f"{key}: source alignment prefix changed")
            checks.append({"item_index": entry.item_index, "record": key, "native_table_offset": entry.table_offset,
                           "start": entry.start, "end": entry.end, "english": text,
                           "first_character_verified": True})
    changed_paths = []
    changed_records = []
    if previous is not None:
        old = NdsImage.open(previous)
        changed_paths = [path for _, path, data in old.iter_files() if data != saved.read_file(path)]
        changed_paths += [path for path, data in old.iter_components() if data != saved.read_file(path)]
        if changed_paths != [common_path]:
            raise ValueError(f"unexpected changed paths from previous checkpoint: {changed_paths}")
        old_blocks = IlnkContainer.parse(old.read_file(common_path)).blocks
        for block, (old_block, new_block) in enumerate(zip(old_blocks, saved_blocks, strict=True)):
            for index, (before, after) in enumerate(zip(old_block.split(b"\0"), new_block.split(b"\0"), strict=True)):
                if before != after:
                    key = f"DK4_MES_B{block:02d}_R{index:04d}"
                    if key not in checked_record_ids:
                        raise ValueError(f"unexpected change outside mapped item entries: {key}")
                    changed_records.append(key)
    return {"status": "pass", "candidate": candidate.as_posix(),
            "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
            "profile": profile_name, "blocks": blocks, "native_entry_count": len(checks),
            "native_tables_unchanged": True, "japanese_records_in_mapped_items": 0,
            "unmapped_japanese_records_by_block": unmapped_japanese_records,
            "previous": previous.as_posix() if previous else None,
            "changed_paths_from_previous": changed_paths, "changed_records": changed_records, "entries": checks}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--blocks", type=int, nargs="+", choices=(29, 30, 31, 32), default=[29, 30, 31, 32])
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = verify(args.candidate, args.profile, args.blocks, args.previous)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "entries"}, indent=2))


if __name__ == "__main__":
    main()
