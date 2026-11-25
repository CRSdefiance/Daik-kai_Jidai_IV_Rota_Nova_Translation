"""Find exact source item terms that use another wording in story archives."""
from collections import Counter, defaultdict
from pathlib import Path
from struct import unpack_from
import re

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts import register_hodram_mihwa_crown_20261119 as parent

base, native = parent.base, parent.stage.native
ROOT = Path("work/current_item_story_terms_20261119_v1")
SOURCE = Path("translations/all_item_names_arm9_v1.json")


def sections(arm):
    parts = MainCodeFile(arm, BASE).sections
    spans = [(p.ramAddress, bytes(p.data)) for p in parts]
    if len(parts) >= 4:
        spans.append((POOL, bytes(parts[3].data[:-48])))
    return spans


def raw(mapping, pointer):
    for start, data in mapping:
        if start <= pointer < start + len(data):
            at = pointer - start
            return data[at:data.index(0, at, at + 160)]
    raise ValueError(hex(pointer))


def main():
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    source, current = (base.NdsImage.open(x) for x in (native.CLEAN, parent.ROM))
    arms = [x.read_file(native.ARM) for x in (source, current)]
    mapping = list(map(sections, arms))
    items = []
    for entry in base.load(SOURCE)["records"]:
        if not entry["id"].startswith("DK4_ITEM_POINTER_"):
            continue
        at = entry["offset"]
        ptrs = [unpack_from("<I", arm, at)[0] for arm in arms]
        a, z = [raw(m, p) for m, p in zip(mapping, ptrs, strict=True)]
        if len(a) < 8 or not z.isascii() or len(z) < 8:
            continue
        terms = z.split()
        pattern = re.compile(rb"\b" + rb"\s+".join(map(re.escape, terms)) + rb"\b", re.I)
        item_id = int(entry["id"].rsplit("_", 1)[1])
        items.append((item_id, a, z, at, ptrs, pattern))

    receipts = defaultdict(list)
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        archives = [x.read_file(path) for x in (source, current)]
        banks = [IlnkContainer.parse(x).blocks for x in archives]
        assert len(banks[0]) == len(banks[1])
        for block, (jp, en) in enumerate(zip(*banks, strict=True)):
            for item_id, a, z, at, pointers, pattern in items:
                source_hits = [m.start() for m in re.finditer(re.escape(a), jp)]
                if not source_hits:
                    continue
                current_hits = [m.start() for m in pattern.finditer(en)]
                receipts[item_id].append(dict(item_ID=item_id, Japanese=a.decode("cp932"), English=z.decode("ascii"),
                    ARM9_pointers=pointers, ARM9_pointer_field_offset=at, file_path=path, block=block,
                    source_term_offsets=source_hits, current_term_offsets=current_hits,
                    source_block_sha256=native.digest(jp), current_block_sha256=native.digest(en)))
    ROOT.mkdir(parents=True, exist_ok=False)
    base.save(ROOT / "block_term_inventory.json", dict(candidate_sha256=release["candidate_sha256"],
        source_rom_sha256=release["clean_input_sha256"], item_list_sha256=base.digest(SOURCE),
        source_length_minimum_bytes=8, english_length_minimum_cells=8, selected_item_term_count=len(items),
        by_item=dict(sorted(receipts.items())), status="Block-level leads. Resolve each mismatch in the complete exchange."))
    for ident, packet in sorted(receipts.items()):
        mismatches = [(row["file_path"][-5], row["block"], len(row["source_term_offsets"]), len(row["current_term_offsets"]))
                      for row in packet if len(row["source_term_offsets"]) > len(row["current_term_offsets"])]
        if mismatches:
            print(ident, packet[0]["Japanese"], packet[0]["English"], len(mismatches), mismatches[:14])


if __name__ == "__main__":
    main()
