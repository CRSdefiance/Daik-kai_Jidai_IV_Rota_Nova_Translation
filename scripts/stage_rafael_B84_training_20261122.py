"""Install reviewed B84 speech and choice text with both original continuations intact."""

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from struct import pack_into
from types import FunctionType

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import register_north_sea_and_hodram_reconciliation_20261122 as parent
from scripts import stage_forest_expeditions_20261118 as forest
from scripts import stage_north_sea_and_hodram_reconciliation_20261122 as previous


base, native = parent.base, parent.native
PATH, BLOCK = "/data/SC0.DK4", 84
INPUTS = Path("translations/editorial_checkpoints/north_sea_and_hodram_20261122")
BATCH = Path("work/analysis/rafael_B84_training_20261122")
ROOT = BATCH / "staged"
ROM = ROOT / "Rafael_B84_Training_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
LEDGER = INPUTS / "rafael_B84_training_contextual_review.json"
REFINED = INPUTS / "rafael_B84_refined_native_layouts.json"
PREVIEWS = INPUTS / "rafael_B84_native_preflight.json"
BINDING = INPUTS / "rafael_B84_choice_rebind.json"


def exact_inputs():
    review, refined, preflight, binding = map(base.load, (LEDGER, REFINED, PREVIEWS, BINDING))
    candidate = base.digest(parent.ROM)
    assert candidate == refined["candidate_sha256"] == binding["candidate_sha256"]
    assert binding["contextual_review_sha256"] == refined["source_ledger_sha256"] == base.digest(LEDGER)
    assert binding["speech_preflight_sha256"] == base.digest(PREVIEWS)
    assert binding["predecessor_sha256"] == review["playable_candidate_sha256"] == preflight["candidate_sha256"]
    assert binding["unchanged_block_sha256"] == refined["current_block_sha256"]
    polished = {x["id"]: x for x in refined["records"]}
    proposals = {r["id"]: r["plan"] for r in preflight["speech_plans"]}
    records = []
    for row in review["records"]:
        ident = row["id"]
        change = polished.get(ident)
        if change:
            assert change["exact_preceding_source_reference"] == row["source_command_hex"]
            assert change["current_command_hex"] == row["current_command_hex"]
            assert change["current_command_offset"] == row["current_command_offset"]
            row = row | {k: change[k] for k in ("english", "protected_phrases", "localization_note")}
            proposals[ident] = change["plan"]
        if ident in proposals:
            assert row["decision"] == "revision" and row["english"] == proposals[ident]["logical_English"]
            assert proposals[ident]["source_selector"] == row["source_selector"]
            assert row["kind"] == "progressive"
        records.append(row)
    revised = [r for r in records if r["decision"] == "revision"]
    assert len(records) == 131 and len(revised) == 9 and len(proposals) == 8
    assert [r["id"] for r in revised if r["kind"] == "choice"] == ["DK4_MES_B84_R0227"]
    return records, proposals, binding


def index(block, arm, inventory):
    commands, _ = inventory(arm, block)
    end = forest.logical_end(block)
    offsets = [c["offset"] for c in commands] + [end]
    assert offsets[0] == 8
    return commands, offsets


def speech(current, row, plan):
    selector_and_body = bytes.fromhex(plan["encoded_hex"])
    assert selector_and_body[0] == current[5] == row["source_selector"] != 254
    body = selector_and_body[1:]
    assert b"\0" not in body and not any(d["severity"] == "error" for d in plan["diagnostics"])
    assert " ".join(body.decode("ascii").split()) == row["english"]
    end = current.index(0, 6)
    assert not any(current[end:])
    terminator = current[end:]
    target = current[:6] + body + terminator
    if len(target) % 2:
        target = current[:6] + body + b" " + terminator
    return target


def choice(source, current, rows):
    source_labels, current_labels = labels(source), labels(current)
    assert len(source_labels) == len(current_labels) == len(rows)
    for slot, (ja, en, row) in enumerate(zip(source_labels, current_labels, rows, strict=True)):
        assert row["variant_slots"] == [slot]
        assert ja.decode("cp932") == row["source_Japanese"] and en.decode("ascii") == row["current_English"]
    prepared = [row | dict(kind="typed-choice-label", source_index=i,
        source_reference=dict(command_offset=row["source_command_offset"], offset=row["source_offset"]),
        current_reference=dict(command_offset=row["current_command_offset"], offset=row["current_offset"]),
        source_hex=source_labels[i].hex(), current_hex=current_labels[i].hex()) for i, row in enumerate(rows)]
    return forest.changed_choices(prepared, source, current)


def relocate(source, current, clean_arm, arm, records, plans, binding):
    inventory, _, _ = native.scoped_inventory()
    clean, clean_offsets = index(source, clean_arm, inventory)
    old, old_offsets = index(current, arm, inventory)
    by_current, children = defaultdict(list), {}
    for row in records:
        by_current[row["current_command_offset"]].append(row)
        if extra := row.get("current_FE_continuation"):
            children[extra["command_offset"]] = (row, extra)
    assert len(clean) == 217 and len(old) == 219 and len(children) == 2
    assert source[:4] == current[:4] and source[6:8] == current[6:8]
    primary = [c for c in old if c["offset"] not in children]
    corresponding = dict(zip((c["offset"] for c in clean), primary, strict=True))
    correspondence = {o: c["offset"] for o, c in corresponding.items()} | {clean_offsets[-1]: old_offsets[-1]}
    source_for = {v: k for k, v in correspondence.items()}
    lookup = {c["offset"]: (i, c) for i, c in enumerate(clean)}
    old_rank = {at: i for i, at in enumerate(old_offsets)}
    choices = {r["current_command_offset"]: r for r in binding["choice_objects"]}
    compiled, receipts, jumps = [], [], {}
    for i, command in enumerate(old):
        at, word = command["offset"], command["word"]
        raw = current[at:old_offsets[i + 1]]
        rows = by_current.pop(at, [])
        target = raw
        source_at = source_for.get(at)
        clean_raw = b""
        extra_id = None
        if at in children:
            owner, continuation = children[at]
            assert word == forest.SPEECH and raw[:6] == bytes.fromhex("0040ffff00fe")
            assert raw.hex() == continuation["exact_command_hex"] and not rows and source_at is None
            assert old[i - 1]["offset"] == owner["current_command_offset"]
            assert old[i - 1]["ancestor_0100_offsets"] == command["ancestor_0100_offsets"]
            extra_id = owner["id"]
        else:
            j, original = lookup[source_at]
            clean_raw = source[source_at:clean_offsets[j + 1]]
            assert original["word"] == word
            assert [correspondence[x] for x in original["ancestor_0100_offsets"]] == command["ancestor_0100_offsets"]
            original_end = correspondence[source_at + original["native_extent"]]
            installed_end = at + command["native_extent"]
            if installed_end in children:
                assert at == children[installed_end][0]["current_command_offset"]
                installed_end = old_offsets[i + 2]
            assert original_end == installed_end
            for row in rows:
                assert row["source_command_offset"] == source_at
                assert row["source_command_hex"] == clean_raw.hex() and row["current_command_hex"] == raw.hex()
            if word == forest.SPEECH:
                row, = rows
                assert clean_raw[:6] == raw[:6]
                if row["decision"] == "revision":
                    target = speech(raw, row, plans[row["id"]])
            elif word in forest.MENU:
                target = choice(clean_raw, raw, rows)
                assert target.hex() == choices.pop(at)["proposed_command_hex"]
            elif word in forest.RELATIVE:
                assert not rows and len(raw) == len(clean_raw) == 4 and raw[:2] == clean_raw[:2]
                destination = forest.jump(raw, at)
                assert destination == correspondence[forest.jump(clean_raw, source_at)]
                jumps[i] = old_rank[destination]
            else:
                assert not rows and raw == clean_raw
        assert len(target) % 2 == 0 and len(target) > 0
        compiled.append(target)
        receipts.append(dict(word=word, source_offset=source_at, current_offset=at,
            source=clean_raw.hex(), current=raw.hex(), record_ids=[r["id"] for r in rows],
            retained_continuation_of=extra_id))
    assert not by_current and not choices

    target_offsets, end = [], 8
    for raw in compiled:
        target_offsets.append(end)
        end += len(raw)
    target_offsets.append(end)
    for i, target in jumps.items():
        relative = target_offsets[target] - target_offsets[i] - 4
        assert 0 <= relative <= 65535 and relative % 2 == 0
        raw = bytearray(compiled[i])
        pack_into("<H", raw, 2, relative)
        compiled[i] = bytes(raw)
    header = bytearray(current[:8])
    assert end < 0x2400
    pack_into("<H", header, 4, end - 8)
    result = bytes(header) + b"".join(compiled) + bytes(-end % 4)
    installed, actual_offsets = index(result, arm, inventory)
    assert actual_offsets == target_offsets
    for i, (a, b, receipt, expected) in enumerate(zip(old, installed, receipts, compiled, strict=True)):
        at = b["offset"]
        assert a["word"] == b["word"] and result[at:target_offsets[i + 1]] == expected
        assert [target_offsets[old_rank[x]] for x in a["ancestor_0100_offsets"]] == b["ancestor_0100_offsets"]
        assert at + b["native_extent"] == target_offsets[old_rank[a["offset"] + a["native_extent"]]]
        if i in jumps:
            assert forest.jump(expected, at) == target_offsets[jumps[i]]
            receipt["target_command_index"] = jumps[i]
        receipt.update(stored=expected.hex(), stored_offset=at)
    assert current[:8] + b"".join(bytes.fromhex(r["current"]) for r in receipts) + current[old_offsets[-1]:] == current
    assert sum(row["current"] != row["stored"] for row in receipts if row["record_ids"]) == 9
    for continuation in (r for r in receipts if r["retained_continuation_of"]):
        assert continuation["current"] == continuation["stored"]
    return result, receipts, len(jumps)


def stage():
    assert not ROOT.exists()
    records, plans, binding = exact_inputs()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    source, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    before = native.files(target)
    assert native.digest(before[PATH]) == binding["current_archive_sha256"] == release["target_SC0_sha256"]
    archive = native.IlnkContainer.parse(before[PATH])
    original = archive.blocks[BLOCK]
    clean = native.IlnkContainer.parse(source.read_file(PATH)).blocks[BLOCK]
    assert native.digest(original) == binding["unchanged_block_sha256"]
    compiled, commands, relative_count = relocate(
        clean, original, source.read_file(native.ARM), before[native.ARM], records, plans, binding)
    archive.blocks[BLOCK] = compiled
    packed = archive.to_bytes()
    assert [i for i, (a, b) in enumerate(zip(native.IlnkContainer.parse(before[PATH]).blocks,
                    native.IlnkContainer.parse(packed).blocks, strict=True)) if a != b] == [BLOCK]
    target.replace_file(PATH, packed)
    final = native.files(target)
    assert final.keys() == before.keys() and {p for p in final if final[p] != before[p]} == {PATH}
    apply_guard = parent.scope["bind_registered_story_percent_guard"](parent.scope["guard_spec"]())
    guard = apply_guard(native.files(source), final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(target.rom.save())
    target.replace_file(PATH, before[PATH])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    base.save(PROOF, dict(candidate_sha256=native.digest(data), predecessor_sha256=release["candidate_sha256"],
        clean_sha256=release["clean_input_sha256"], archive_hashes={PATH: native.digest(packed)}, source25=guard,
        whole_parent_inverse=True, unchanged_ARM9_sha256=release["target_ARM9_sha256"],
        groups=[dict(route=0,file_path=PATH,block=BLOCK,commands=commands,plans=plans,after=native.digest(compiled),
             source_block_sha256=native.digest(clean),current_block_sha256=native.digest(original))],
        source_record_count=len(records), relative_commands=relative_count, exact_FE_continuations=2,
        original_block_length=len(original), installed_block_length=len(compiled),
        editorial_records=records, evidence={str(p):base.digest(p) for p in (LEDGER, REFINED, PREVIEWS, BINDING)}))
    print(f"Staged eight speeches and one choice. {relative_count} branch targets, both continuations, and the ROM inverse verified.",flush=True)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        inherited = getattr(previous.established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
