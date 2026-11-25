"""Pair the Rafael and Maria scenes with their existing speakerless continuation panels."""

from collections import defaultdict
from pathlib import Path

from scripts import prepare_london_guild_assignments_20261118 as original
from scripts import register_company_name_dialogue_20261121 as parent


base, native, stage = original.base, original.native, original.stage
ROOT = Path("work/company_name_companion_scenes_20261121")
OUTPUT = ROOT / "paired_source.json"
# Each continuation is an original source paragraph's second FE page.
SCENES = {
    (0, 84): (217, 219, {6096: 470, 7436: 539}),
    (3, 116): (62, 64, {630: 41, 1026: 51}),
}


def command_bytes(command):
    return bytes.fromhex(command["whole_command_hex"])


def speech(raw):
    return raw[6:raw.index(0, 6)].decode("cp932")


def at_source(source, at):
    return source[:at + 5].count(b"\0")


def pair(source, current, clean_arm, arm, scan, counts):
    ja, en = scan(clean_arm, source)[0], scan(arm, current)[0]
    source_count, current_count, extras = counts
    assert (len(ja), len(en)) == (source_count, current_count)
    full = {cmd["offset"]: cmd for cmd in en}
    assert extras.keys() <= full.keys()
    retained = [cmd for cmd in en if cmd["offset"] not in extras]
    assert [c["word"] for c in ja] == [c["word"] for c in retained]
    ja_index = stage.offsets(ja, stage.logical_end(source))
    en_index = stage.offsets(retained, stage.logical_end(current))
    ja_next = dict(zip([cmd["offset"] for cmd in ja], [cmd["offset"] for cmd in ja[1:]] + [stage.logical_end(source)], strict=True))
    en_next = dict(zip([cmd["offset"] for cmd in en], [cmd["offset"] for cmd in en[1:]] + [stage.logical_end(current)], strict=True))
    children = defaultdict(list)
    for position, owner_id in extras.items():
        child = full[position]
        assert child["word"] == 0x4000
        ix = en.index(child)
        older = en[ix - 1]
        assert older["offset"] + older["native_extent"] == position
        assert at_source(source, ja[en_index[older["offset"]]]["offset"]) == owner_id
        assert command_bytes(older)[:6] == command_bytes(child)[:6] == bytes.fromhex("0040ffff00fe")
        assert older["ancestor_0100_offsets"] == child["ancestor_0100_offsets"]
        children[older["offset"]].append(child)
    differences, records, graph = [], [], []
    for x, y in zip(ja, retained, strict=True):
        source_at, current_at, word = x["offset"], y["offset"], x["word"]
        a, b = command_bytes(x), command_bytes(y)
        assert [ja_index[p] for p in x["ancestor_0100_offsets"]] == [en_index[p] for p in y["ancestor_0100_offsets"]]
        if word in stage.RELATIVE:
            a = source[source_at:ja_next[source_at]]
            b = current[current_at:en_next[current_at]]
            assert a[:2] == b[:2] and len(a) == len(b) == 4, (word, source_at, current_at, len(a), len(b))
            target = ja_index[stage.jump(a, source_at)]
            assert en_index[stage.jump(b, current_at)] == target
            graph.append(dict(source_at=source_at, current_at=current_at, target_index=target))
        elif word == 0x4000:
            assert a[:6] == b[:6], (source_at, current_at, a[:6], b[:6])
            pages = [y, *children[current_at]]
            records.append(dict(id=f"R{at_source(source, source_at):04}", source_selector=a[5],
                source_reference=dict(command_offset=source_at, offset=source_at+5,
                    record_index=at_source(source, source_at), exact_command_hex=a.hex()),
                current_reference=dict(command_offset=current_at, offset=current_at+5,
                    exact_command_hex=b.hex()),
                installed_pages=[dict(offset=c["offset"], exact_command_hex=command_bytes(c).hex()) for c in pages],
                Japanese=speech(a), current_English=" ".join(" ".join(speech(command_bytes(c)).split()) for c in pages)))
        elif word in (stage.STYLE, *stage.MENU):
            old_records = original.text_records(a, word)
            cur_records = original.text_records(b, word)
            assert [r[3] for r in old_records] == [r[3] for r in cur_records]
        elif a != b:
            differences.append(dict(word=word, source_at=source_at, current_at=current_at,
                                    source_hex=a.hex(), installed_hex=b.hex()))
    return dict(source_commands=len(ja), installed_commands=len(en), continuations=dict(extras),
                relative_targets=graph, retained_nontext_differences=differences, records=records)


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    clean_arm, arm = (image.read_file(native.ARM) for image in (clean, active))
    scan, _, _ = native.scoped_inventory()
    groups = []
    for (route, block), config in SCENES.items():
        path = f"/data/SC{route}.DK4"
        jp, en = [image.read_file(path) for image in (clean, active)]
        a, b = [native.IlnkContainer.parse(archive).blocks[block] for archive in (jp, en)]
        groups.append(pair(a, b, clean_arm, arm, scan, config) | dict(route=route, block=block, file_path=path,
            source_archive_sha256=native.digest(jp), current_archive_sha256=native.digest(en),
            source_block_sha256=native.digest(a), current_block_sha256=native.digest(b)))
    ROOT.mkdir(exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        source_pairing="All native commands paired after identifying four existing FE continuation pages.",
        groups=groups, new_coverage_credit=0))
    print("Paired both scenes, including all four FE continuations.")


if __name__ == "__main__":
    main()
