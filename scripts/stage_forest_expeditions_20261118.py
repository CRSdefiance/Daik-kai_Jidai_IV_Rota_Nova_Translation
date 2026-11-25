"""Compile the reviewed forest script objects over the relocated current scenes."""

from collections import defaultdict
from struct import pack_into, unpack_from

from dk4tool.dialogue.reviewed_actor_style_object_v1 import compile_styles, unpack
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices, count_and_base
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import review_forest_expeditions_20261118 as review
from scripts import ruin_puzzle_fe_20261118 as system
from scripts import stage_palace_and_village_exchanges_20261115 as progressive


base, native, parent = review.base, review.native, review.parent
ROOT = review.ROOT / "research_v2"
ROM = ROOT / "Forest_Expeditions_RESEARCH_ONLY.nds"
PROOF = ROOT / "stored_proof.json"
RELATIVE = (0x100, 0x200, 0x300, 0x400)
MENU = (0x2100, 0x2200)
STYLE, SPEECH = 0x4100, 0x4000
PROTECTED = (
    "without a map.", "don't move!", "behind you...", "our crew!", "Let's get out of here!",
    "we could get hurt too!", "Forget it, let's run!", "a man-eater!", "the ones in trouble!",
    "no sign of leaving.", "no sign of moving.", "didn't work...", "scare it off!",
    "looks like we made it...", "Thank goodness.", "we're out of the forest!",
    "we've reached the ruins.", "these are the ruins!", "Those are the ruins!",
    "Are those the ruins?", "Lots of funny stones", "today's meeting!",
    "Let's be careful.", "It's attacked our crew!", "We have to run",
    "The crew's been attacked!", "We're in danger too!", "It might be a man-eater!",
    "if we take it on,",
)


def phrases(paragraph):
    return tuple(term for term in PROTECTED if term.lower() in paragraph.lower())


def plan_progressive(row, selector, raw, original):
    paragraph = row["english"]
    terms = phrases(paragraph)
    norm = progressive.layout.prior.layout.norm
    pairs = [(norm(a), norm(b)) for p in terms for a, b in zip(p.split(), p.split()[1:])]
    # No runtime text escapes occur here. The virtual selector is used solely
    # for the existing text-width planner and removed before writing a 4100 body.
    assert not any(k in v for k in (b"FI", b"FA", b"FO", b"FU", b"%") for v in (raw, original, paragraph.encode("ascii")))
    virtual = dict(id=row["id"], kind="progressive", source_selector=2, source_hex=(b"\x02" + original).hex(),
        current_hex=(b"\x02" + b" " * (len(paragraph) + 16)).hex(), english="{SPEAKER:02}" + paragraph,
        protected_pairs=pairs)
    plan = progressive.layout.PLANNER(virtual)
    body = bytes.fromhex(plan["encoded_hex"])[1:]
    assert " ".join(body.decode("ascii").split()) == paragraph
    assert len(plan["lines"]) <= 4 and not any(d["severity"] == "error" for d in plan["diagnostics"])
    return body, plan | dict(logical_English=paragraph, source_selector=selector,
        planning_record=dict(source_hex=(bytes([selector]) + original).hex()),
        encoded_hex=(bytes([selector]) + body).hex())


def plan_fe(row, painter):
    paragraph = row["english"]
    for _, lines, compiled in system.candidate_rows(paragraph, phrases(paragraph)):
        try:
            plane = painter(compiled[1:])
            system.check_FE_rows(compiled[1:], plane)
        except AssertionError:
            continue
        return compiled[1:], dict(lines=lines, expected_native_pages=1, encoded_hex=compiled.hex())
    raise AssertionError(row["id"])


def changed_speech(row, original, current, painter):
    raw_source, raw_current = [bytes.fromhex(row[f"{side}_hex"]) for side in ("source", "current")]
    selector = original[5]
    assert original[:6] == current[:6] and raw_source[0] == raw_current[0] == selector
    for command, raw in ((original, raw_source), (current, raw_current)):
        assert command[5:5 + len(raw)] == raw and not any(command[5 + len(raw):])
    if row["decision"] == "retention":
        return current, {}
    if selector == 254:
        body, plan = plan_fe(row, painter)
    else:
        body, plan = plan_progressive(row, selector, raw_current[1:], raw_source[1:])
    if (len(body) - len(raw_current[1:])) % 2:
        body += b" "
    target = current[:6] + body + current[5 + len(raw_current):]
    return target, {row["id"]: plan}


def changed_styles(rows, original, current):
    source_offsets, source_texts = unpack(original)
    current_offsets, current_texts = unpack(current)
    rows.sort(key=lambda r: r["source_reference"]["offset"])
    assert len(rows) == len(source_texts) == len(current_texts)
    selector = original[19]
    prepared, plans = [], {}
    for row, offset in zip(rows, sorted(source_texts), strict=True):
        indices = [i for i, x in enumerate(source_offsets) if x == offset]
        raw = current_texts[current_offsets[indices[0]]]
        jp = source_texts[offset]
        prepared.append(row | dict(native_object_kind="4100-style-alternative", source_style_indices=indices,
            current_style_indices=indices, source_selector=selector, source_header_hex=original[:20].hex(),
            source_choice_object_hex=original.hex(), current_style_object_hex=current.hex(),
            virtual_formatter_prefix_is_not_part_of_stored_alternative_text=True))
        if row["decision"] == "revision":
            _, plan = plan_progressive(row, selector, raw, jp)
        else:
            plan = dict(logical_English=row["english"], source_selector=selector,
                        planning_record=dict(source_hex=(bytes([selector]) + jp).hex()),
                        encoded_hex=(bytes([selector]) + raw).hex())
        plans[row["id"]] = plan
    target = compile_styles(original, current, prepared, plans, require_formatting=False)
    if all(row["decision"] == "retention" for row in rows):
        assert target == current
    return target, plans


def changed_choices(rows, original, current):
    rows.sort(key=lambda row: row["source_reference"]["offset"])
    for side, raw in (("source", original), ("current", current)):
        count, body = count_and_base(raw)
        assert len(rows) == count
        for i, row in enumerate(rows):
            ref = row[f"{side}_reference"]
            assert ref.get("source_index", i) == i
            assert ref["offset"] == ref["command_offset"] + body + unpack_from("<H", raw, 2 + 2 * i)[0]
    prepared = [row | dict(source_index=i, source_choice_object_hex=original.hex(),
                           current_choice_object_hex=current.hex()) for i, row in enumerate(rows)]
    target = compile_choices(original, current, prepared, require_formatting=False)
    if all(row["decision"] == "retention" for row in rows):
        assert target == current
    return target


def logical_end(block):
    end = 8 + unpack_from("<H", block, 4)[0]
    assert end <= len(block) and not any(block[end:])
    return end


def offsets(commands, end):
    return {c["offset"]: i for i, c in enumerate(commands)} | {end: len(commands)}


def jump(raw, offset):
    return offset + 4 + unpack_from("<H", raw, 2)[0]


def rebuild(rows, source, current, inventory, clean_arm, arm, painter):
    clean_commands, _ = inventory(clean_arm, source)
    current_commands, _ = inventory(arm, current)
    assert [c["word"] for c in clean_commands] == [c["word"] for c in current_commands]
    assert source[:4] == current[:4] and source[6:8] == current[6:8]
    clean_at = offsets(clean_commands, logical_end(source))
    current_at = offsets(current_commands, logical_end(current))
    clean_offsets = list(clean_at)
    current_offsets = list(current_at)
    by_owner = defaultdict(list)
    for row in rows:
        ref = row["source_reference"]
        field = "command_offset" if "command_offset" in ref else "header_offset"
        by_owner[ref[field]].append(row)

    compiled, plans, jumps, receipts = [], {}, {}, []
    for i, (a, b) in enumerate(zip(clean_commands, current_commands, strict=True)):
        w, j, c = a["word"], a["offset"], b["offset"]
        old = source[j:clean_offsets[i + 1]]
        now = current[c:current_offsets[i + 1]]
        assert clean_at[j + a["native_extent"]] == current_at[c + b["native_extent"]]
        assert [clean_at[p] for p in a["ancestor_0100_offsets"]] == [current_at[p] for p in b["ancestor_0100_offsets"]]
        owners = by_owner.pop(j, [])
        if w == SPEECH:
            row, = owners
            assert row["current_reference"]["offset"] == c + 5
            target, new_plans = changed_speech(row, old, now, painter)
        elif w == STYLE:
            assert all(r["current_reference"]["command_offset"] == c for r in owners)
            target, new_plans = changed_styles(owners, old, now)
        elif w in MENU:
            assert all(r["current_reference"]["command_offset"] == c for r in owners)
            target, new_plans = changed_choices(owners, old, now), {}
        else:
            assert not owners
            target, new_plans = now, {}
            if w in RELATIVE:
                assert old[:2] == now[:2] and len(old) == len(now) == 4, (
                    hex(w), j, c, old.hex(), now.hex()
                )
                jumps[i] = current_at[jump(now, c)]
                assert clean_at[jump(old, j)] == jumps[i]
            else:
                assert old == now, (hex(w), j, c, old.hex(), now.hex())
        assert len(target) % 2 == 0 and len(target) > 0
        compiled.append(target)
        plans.update(new_plans)
        receipts.append(dict(word=w, source_offset=j, current_offset=c, source=old.hex(), current=now.hex(),
                             record_ids=[r["id"] for r in owners]))
    assert not by_owner

    target_offsets, pos = [], 8
    for raw in compiled:
        target_offsets.append(pos)
        pos += len(raw)
    target_offsets.append(pos)
    for i, dest in jumps.items():
        raw = bytearray(compiled[i])
        distance = target_offsets[dest] - target_offsets[i] - 4
        assert 0 <= distance <= 65535 and distance % 2 == 0
        pack_into("<H", raw, 2, distance)
        compiled[i] = bytes(raw)
    header = bytearray(current[:8])
    assert pos < 0x2400
    pack_into("<H", header, 4, pos - 8)
    target = bytes(header) + b"".join(compiled) + bytes(-pos % 4)
    parsed, _ = inventory(arm, target)
    assert offsets(parsed, logical_end(target)) == {at: i for i, at in enumerate(target_offsets)}
    inverse = []
    for i, (cmd, old, receipt, expected) in enumerate(zip(parsed, current_commands, receipts, compiled, strict=True)):
        w = receipt["word"]
        assert cmd["word"] == w and target[cmd["offset"]:target_offsets[i + 1]] == expected
        assert cmd["offset"] + cmd["native_extent"] == target_offsets[
            current_at[old["offset"] + old["native_extent"]]
        ]
        assert cmd["ancestor_0100_offsets"] == [target_offsets[current_at[p]] for p in old["ancestor_0100_offsets"]]
        if i in jumps:
            assert jump(expected, cmd["offset"]) == target_offsets[jumps[i]]
            receipt["target_command_index"] = jumps[i]
        receipt.update(stored=expected.hex(), stored_offset=cmd["offset"])
        inverse.append(bytes.fromhex(receipt["current"]))
    assert current[:8] + b"".join(inverse) + current[logical_end(current):] == current
    return target, receipts, plans


def main():
    ledger = base.load(review.MANUSCRIPT)
    registry = base.load(base.REGISTRY)
    release = base.load(parent.RELEASE)
    assert ledger["previous_sha256"] == base.digest(parent.ROM) == release["candidate_sha256"]
    assert ledger["previous_registry_sha256"] == base.digest(base.REGISTRY) == release["registry_sha256"]
    reviewed = {(r["file_path"], r["id"]): r for r in ledger["records"]}
    assert len(reviewed) == 370 and not ROOT.exists()
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    current = base.NdsImage.open(parent.ROM)
    clean = base.NdsImage.open(native.CLEAN)
    clean_arm = clean.read_file(native.ARM)
    painter = system.native_painter(ctx)
    inv, _, _ = native.scoped_inventory()
    evidence, inverse, candidates = [], {}, {}
    for entry in base.load(review.INDEX)["route_packets"]:
        route, file, block = [entry[k] for k in ("route", "file_path", "block")]
        source_arc, current_arc = [native.IlnkContainer.parse(rom.read_file(file)) for rom in (clean, current)]
        source_block, current_block = source_arc.blocks[block], current_arc.blocks[block]
        assert native.digest(source_block) == entry["source_sha256"]
        assert native.digest(current_block) == entry["current_sha256"]
        rows = [reviewed[file, r["id"]] for r in base.load(entry["exact_packet"])["records"]]
        target, commands, plans = rebuild(rows, source_block, current_block, inv, clean_arm, ctx.arm, painter)
        assert target != current_block
        original_bytes = current_arc.to_bytes()
        current_arc.blocks[block] = target
        compiled = current_arc.to_bytes()
        current_arc.blocks[block] = current_block
        assert current_arc.to_bytes() == original_bytes == current.read_file(file)
        candidates[file] = compiled
        inverse[file] = original_bytes
        evidence.append(dict(route=route, file_path=file, block=block, record_count=len(rows),
            before=native.digest(current_block), after=native.digest(target),
            source=native.digest(source_block), commands=commands, plans=plans,
            source_controls_checked=True, current_and_compiled_branches_exact=True))
    original = native.files(current)
    for path, blob in candidates.items():
        current.replace_file(path, blob)
    changed = native.files(current)
    assert {p for p in original if original[p] != changed[p]} == candidates.keys()
    assert original[native.ARM] == changed[native.ARM]
    guard = bind_registered_story_percent_guard(registry["profiles"][release["profile"]]["source25_multiarchive_guard"])
    bound = guard(native.files(clean), changed)
    assert bound["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(bound["source_bound_new_command_counts"].values())
    data = bytes(current.rom.save())
    for file, archive in inverse.items():
        current.replace_file(file, archive)
    assert bytes(current.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(data)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release["candidate_sha256"],
        source_sha256=release["clean_input_sha256"], manuscript_sha256=base.digest(review.MANUSCRIPT),
        preserved_ARM9_sha256=native.digest(changed[native.ARM]), whole_parent_inverse=True,
        source25=bound, groups=evidence, stored_check_only=True, release_registered=False))
    print("Four forest blocks compiled with exact branches, style ownership, and whole-ROM inverse.")


if __name__ == "__main__":
    main()
