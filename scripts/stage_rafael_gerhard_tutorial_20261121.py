"""Reflow the existing B84 commands, including both installed FE continuations."""

from collections import defaultdict
from struct import pack_into
from types import SimpleNamespace

from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import review_rafael_gerhard_tutorial_20261121 as review
from scripts import stage_forest_expeditions_20261118 as compiler
from scripts.review_rafael_east_asia_followup_20261121 import plan_progressive
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "gerhard_staged_v3"
ROM, PROOF = ROOT / "Rafael_Gerhard_Tutorial_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = review.OUTPUT
PATH = "/data/SC0.DK4"


def compile_FE(english, painter, phrases):
    for _, lines, encoded in compiler.system.candidate_rows(english, phrases):
        try:
            result = painter(encoded[1:])
            assert result["complete_consumed_bytes"] == len(encoded) - 1
            compiler.system.check_FE_rows(encoded[1:], result)
        except AssertionError:
            continue
        return encoded[1:], dict(lines=lines, encoded_hex=encoded.hex(), expected_native_pages=1)
    raise ValueError(f"No verified FE layout for {english!r}")


def change_body(row, current, page, painter):
    if row["decision"] == "retention":
        return current, None
    selector, end = current[5], current.index(0, 6)
    assert selector == row["source_selector"]
    if selector == 254:
        body, plan = compile_FE(row["editable_FE_pages"][page - 1], painter, row["protected_phrases"])
    else:
        assert page == 1
        body, plan = plan_progressive(row, selector, current[6:end], bytes.fromhex(row["source_hex"])[1:])
    if (len(body) - (end - 6)) % 2:
        body += b" "
    return current[:6] + body + current[end:], plan


def map_sources(source, installed, draft):
    source_by_at = {c["offset"]: c for c in source}
    target_by_at = {c["offset"]: c for c in installed}
    continuation = {p["command_offset"] for r in draft for p in r["current_reference"]["installed_pages"][1:]}
    ordinary = [c for c in installed if c["offset"] not in continuation]
    assert len(ordinary) == len(source) == 217 and len(continuation) == 2 and len(installed) == 219
    sources = {}
    for original, current in zip(source, ordinary, strict=True):
        assert original["word"] == current["word"]
        sources[current["offset"]] = original
    by_command = defaultdict(list)
    for row in draft:
        clean_at = row["source_reference"]["command_offset"]
        assert source_by_at[clean_at]["word"] == row["native_command_word"]
        for number, page in enumerate(row["current_reference"]["installed_pages"], 1):
            offset = page["command_offset"]
            assert target_by_at[offset]["word"] == row["native_command_word"]
            if number == 1:
                assert sources[offset]["offset"] == clean_at
            else:
                assert offset in continuation and row["source_selector"] == 254
            by_command[offset].append((row, number, page))
    return sources, by_command


def rebuild(current, historical, installed, draft, painter, inventory, arm):
    sources, owners = map_sources(historical, installed, draft)
    original_offsets = compiler.offsets(installed, compiler.logical_end(current))
    boundaries = list(original_offsets)
    results, compiled, offsets, jumps = [], [], [8], {}
    for index, command in enumerate(installed):
        at, word = (command[key] for key in ("offset", "word"))
        raw = current[at:boundaries[index + 1]]
        whole = bytes.fromhex(command["whole_command_hex"])
        assert whole[:len(raw)] == raw
        assert len(raw) == 4 if word in compiler.RELATIVE else raw == whole
        members = owners.pop(at, [])
        updated, plan, page = raw, None, None
        owner = sources.get(at)
        if word == compiler.SPEECH:
            (row, page, binding), = members
            assert raw[:6] == bytes.fromhex("0040ffff00") + bytes([row["source_selector"]])
            assert raw[6:raw.index(0, 6)].hex() == binding["body_hex"]
            updated, plan = change_body(row, raw, page, painter)
            if page == 2:
                assert row["source_selector"] == 254 and installed[index - 1]["ancestor_0100_offsets"] == command["ancestor_0100_offsets"]
        elif word in compiler.MENU:
            assert owner is not None and all(n == 1 for _, n, _ in members)
            source_raw = bytes.fromhex(owner["whole_command_hex"])
            updated = compiler.changed_choices([row for row, _, _ in members], source_raw, raw)
        else:
            assert not members and owner is not None
            if word in compiler.RELATIVE:
                jumps[index] = original_offsets[compiler.jump(raw, at)]
        results.append(dict(word=word, current_offset=at, source_offset=owner["offset"] if owner else None,
                            current=raw.hex(), record_ids=[row["id"] for row, _, _ in members], page=page, plan=plan))
        assert len(updated) % 2 == 0
        compiled.append(updated)
        offsets.append(offsets[-1] + len(updated))
    assert not owners and offsets[-1] < 0x2400
    for index, target in jumps.items():
        raw = bytearray(compiled[index])
        assert 0 <= offsets[target] - offsets[index] - 4 <= 0xffff
        pack_into("<H", raw, 2, offsets[target] - offsets[index] - 4)
        compiled[index] = bytes(raw)
    header = bytearray(current[:8])
    pack_into("<H", header, 4, offsets[-1] - 8)
    target = bytes(header) + b"".join(compiled) + bytes(-offsets[-1] % 4)
    parsed, _ = inventory(arm, target)
    assert compiler.offsets(parsed, compiler.logical_end(target)) == {at: index for index, at in enumerate(offsets)}
    for index, (before, after, result, raw) in enumerate(zip(installed, parsed, results, compiled, strict=True)):
        assert before["word"] == after["word"] == result["word"]
        assert after["ancestor_0100_offsets"] == [offsets[original_offsets[at]] for at in before["ancestor_0100_offsets"]]
        confirmed = bytes.fromhex(after["whole_command_hex"])
        assert confirmed[:len(raw)] == raw
        assert index in jumps or confirmed == raw
        assert after["offset"] + after["native_extent"] == offsets[original_offsets[before["offset"] + before["native_extent"]]]
        if index in jumps:
            assert compiler.jump(raw, after["offset"]) == offsets[jumps[index]] and raw[:2].hex() == result["current"][:4]
        elif not result["record_ids"]:
            assert raw.hex() == result["current"]
        result.update(stored_offset=after["offset"], stored=raw.hex())
    assert current[:8] + b"".join(bytes.fromhex(r["current"]) for r in results) + current[compiler.logical_end(current):] == current
    return target, results, len(jumps)


def main():
    assert not ROOT.exists()
    packet, draft, release = map(base.load, (review.SOURCE, OUTPUT, parent.RELEASE))
    predecessor = base.digest(parent.ROM)
    assert packet["candidate_sha256"] == draft["previous_sha256"] == release["candidate_sha256"] == predecessor
    assert base.digest(review.SOURCE) == draft["source_packet_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"] == draft["previous_registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, image = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    clean_arm, arm = (item.read_file(native.ARM) for item in (clean, image))
    clean_archive, current_archive = (item.read_file(PATH) for item in (clean, image))
    source, current = [native.IlnkContainer.parse(data).blocks[84] for data in (clean_archive, current_archive)]
    assert native.digest(source) == packet["clean_block_sha256"] and native.digest(current) == packet["current_block_sha256"]
    assert native.digest(clean_archive) == packet["clean_archive_sha256"] and native.digest(current_archive) == packet["current_archive_sha256"]
    inventory, _, _ = native.scoped_inventory()
    a, b = [inventory(code, block)[0] for code, block in ((clean_arm, source), (arm, current))]
    painter = current_fe_painter(SimpleNamespace(arm=arm, image=image))
    updated, commands, branches = rebuild(current, a, b, draft["records"], painter, inventory, arm)
    bank = native.IlnkContainer.parse(current_archive)
    bank.blocks[84] = updated
    image.replace_file(PATH, bank.to_bytes())
    guard = base.load(base.REGISTRY)["profiles"][release["profile"]]["source25_multiarchive_guard"]
    protected = bind_registered_story_percent_guard(guard)(native.files(clean), native.files(image))
    assert protected["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(protected["source_bound_new_command_counts"].values())
    ROOT.mkdir()
    image.save(ROM)
    reopened = base.NdsImage.open(ROM)
    assert reopened.read_file(PATH) == bank.to_bytes()
    reopened.replace_file(PATH, current_archive)
    assert bytes(reopened.rom.save()) == parent.ROM.read_bytes()
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=predecessor,
        manuscript_sha256=base.digest(OUTPUT), changed_blocks={PATH: [84]}, whole_parent_inverse=True,
        original_installed_commands=219, original_clean_commands=217, branch_targets_preserved=branches,
        preserved_FE_continuations=2, checked_story_format_guard=protected,
        groups=[dict(file_path=PATH, block=84, before=native.digest(current), after=native.digest(updated), commands=commands)]))
    print(f"Staged 219 installed commands, preserving both FE continuations and {branches} branch targets.")


if __name__ == "__main__":
    main()
