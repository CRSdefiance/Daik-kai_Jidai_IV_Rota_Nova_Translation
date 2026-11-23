"""Stage the source-bound Hodram elegy using the registered story compiler."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as release_checks
from scripts import preview_hodram_B16_elegy_20261123 as editorial
from scripts import register_assigned_fleet_info_20261123 as parent
from scripts import register_cartridge_title_20261123 as registration
from scripts import stage_current_story_wraps_20261122 as compiler
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


ROOT = Path("E:/Rota Nova translations/Generated/work/hodram_B16_elegy_20261123")
ROM = ROOT / "Translation_DS_Hodram_Elegy_20261123_candidate.nds"
STORED = ROOT / "elegy_stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
PATCH_PROOF = ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
ARM, STORY = editorial.outcome.ARM, editorial.outcome.STORY
native = compiler.native


def bind_records(packet, observed, earlier, parent_rom):
    proposals = {row["id"]: row for row in packet["records"]}
    evidence = {row["id"]: row for row in observed["story"]}
    records = []
    for old in (row for row in earlier["records"] if row["block"] == 16):
        key = old["id"]
        actual = evidence.pop(key)
        assert actual["installed"]["candidate_sha256"] == parent_rom
        assert old["source_hex"] == actual["source"]["exact_stored_hex"]
        original, current = actual["source"], actual["installed"]
        row = old | dict(route=1, source_reference=original, current_reference=current,
                         current_hex=current["exact_stored_hex"], decision="retention")
        if key in proposals:
            new = proposals[key]
            assert original == new["exact_source"] and current == new["exact_current"]
            row |= new | dict(source_reference=original, current_reference=current)
        elif "retention_reason" in actual:
            row["localization_note"] = actual["retention_reason"]
        records.append(row)
    assert not evidence and len(records) == 14
    return records, proposals


def stage():
    assert not STORED.exists() and not ROM.exists()
    release = read(parent.RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    packet, observed, earlier = map(read, (editorial.OUT, editorial.outcome.OUT, editorial.outcome.STORY_REVIEW))
    validate_natural_dialogue_batch(packet)
    assert packet["registered_release"] == reference(parent.RELEASE)
    assert packet["preview"] == reference(editorial.SHEET)
    assert packet["gameplay"] == reference(editorial.outcome.OUT)
    assert observed["candidate_sha256"] == release["candidate_sha256"]
    rows, proposals = bind_records(packet, observed, earlier, release["candidate_sha256"])

    clean, image = map(NdsImage.open, (CLEAN, release["candidate"]))
    predecessor = native.files(image)
    source_tables = native.files(clean)
    arm = predecessor[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(predecessor[STORY]).hexdigest() == release["target_SC1_sha256"]
    assert registration.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    before, source = (native.IlnkContainer.parse(tables[STORY]) for tables in (predecessor, source_tables))
    original, current = source.blocks[16], before.blocks[16]
    rebuild, _ = compiler.compilers()
    inventory, _, _ = native.scoped_inventory()
    revised, commands, plans = rebuild(rows, original, current, inventory, source_tables[ARM], arm, None)
    assert revised != current and plans.keys() == proposals.keys()
    owned = set()
    for command in commands:
        old, new = (bytes.fromhex(command[key]) for key in ("current", "stored"))
        if old == new:
            continue
        ident, = command["record_ids"]
        proposal = proposals[ident]
        expected = bytes.fromhex(proposal["candidate_body_hex"])
        assert old[:6] == new[:6] and expected[0] == new[5]
        payload_end = new.index(0, 6)
        assert new[5:payload_end].rstrip(b" ") == expected.rstrip(b" ")
        assert plans[ident]["lines"] == proposal["native_layout"]["lines"]
        assert not any(new[payload_end:])
        owned.add(ident)
    assert owned == proposals.keys()
    before.blocks[16] = revised
    updated = before.to_bytes()
    image.replace_file(STORY, updated)
    final = native.files(image)
    assert predecessor.keys() == final.keys() and {p for p in final if predecessor[p] != final[p]} == {STORY}
    guard = bind_registered_story_percent_guard(registration.previous.guard_spec())(source_tables, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    output = bytes(image.rom.save())
    image.replace_file(STORY, predecessor[STORY])
    assert bytes(image.rom.save()) == Path(release["candidate"]).read_bytes()
    ROOT.mkdir(exist_ok=True)
    ROM.write_bytes(output)
    assert digest(ROM) == sha256(output).hexdigest()
    installed = NdsImage.open(ROM)
    final_blocks = native.IlnkContainer.parse(installed.read_file(STORY)).blocks
    earlier_blocks = native.IlnkContainer.parse(predecessor[STORY]).blocks
    assert {i for i, (old, new) in enumerate(zip(earlier_blocks, final_blocks, strict=True)) if old != new} == {16}
    assert all(installed.read_file(path) == value for path, value in final.items())
    write(STORED, dict(staged=reference(ROM), clean=reference(CLEAN), predecessor=reference(release["candidate"]),
                       target_ARM9_sha256=release["target_ARM9_sha256"], target_SC1_sha256=sha256(updated).hexdigest(),
                       block_sha256=sha256(revised).hexdigest(), previous_block_sha256=sha256(current).hexdigest(),
                       owned_ids=sorted(owned), commands=commands, plans=plans, records=rows,
                       source25_guard=guard, whole_parent_inverse=True, proposal=reference(editorial.OUT)))
    print(f"Staged two B16 changes. {digest(ROM)}")


def check(action):
    detail = read(STORED)
    config = vars(release_checks) | dict(RELEASE=parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT,
                                         STARTUP_CAPTURE=STARTUP_CAPTURE)
    proof = dict(candidate=str(ROM), candidate_sha256=detail["staged"]["sha256"],
                 clean_input_sha256=detail["clean"]["sha256"], predecessor_sha256=detail["predecessor"]["sha256"])
    worker = getattr(release_checks, action)
    FunctionType(worker.__code__, config)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        check(action)
