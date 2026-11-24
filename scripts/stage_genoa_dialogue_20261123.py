"""Install and verify the three reviewed Genoa story changes in their current allocations."""

from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as release_checks
from scripts import register_cartridge_title_20261123 as registration
from scripts import register_price_info_descriptions_20261123 as parent
from scripts import verify_genoa_copenhagen_town_20261123 as gameplay
from scripts.checkpoint_story_still_commands_20261120 import explicit_walk
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_current_story_wraps_20261122 import native
from scripts.verify_moonlit_violin_20261121 import bytes_for


ROOT = Path(".codex-release-work/genoa_dialogue_20261123")
ROM = ROOT / "Genoa_Dialogue_STAGED.nds"
STORED = ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
ARM, COMMON, STORY = parent.ARM, parent.COMMON, gameplay.STORY
IDS = ("DK4_MES_B170_R0090", "DK4_MES_B170_R0125", "DK4_MES_B181_R0012")


def apply_block(clean, current, arm, rows, renderer, font, walk):
    updated = bytearray(current)
    edited = []
    for row in rows:
        source, ref = row["source_reference"], row["installed_reference"]
        original, before = gameplay.exact_command(clean, source), gameplay.exact_command(current, ref)
        offset = ref["command_offset"]
        draft = row["offline_preflight"]
        plan = draft["formatter_plan"]
        compiled = bytes.fromhex(plan["encoded_hex"])
        assert original[:6] == before[:6] == b"\x00\x40\xFF\xFF\x00" + compiled[:1]
        assert compiled[0] == draft["physical_source_and_installed_selectors"]
        assert all(token not in raw for token in (b"FI", b"FA", b"FO", b"FU", b"%")
                   for raw in (bytes_for(original), bytes_for(before), compiled[1:]))
        assert " ".join(compiled[1:].decode("ascii").split()) == row["proposed_English"]
        end = before.index(0, 6)
        assert len(compiled) - 1 <= end - 6 and not any(before[end:])
        body = compiled[1:].ljust(end - 6, b" ")
        command = before[:6] + body + before[end:]
        assert command != before and len(command) == len(before) and command.index(0, 6) == end
        updated[offset:offset + len(command)] = command
        before_layout = renderer(arm, font, bytes_for(before))
        after_layout = renderer(arm, font, body)
        page, = after_layout["pages"]
        assert len(before_layout["pages"]) == 1 and page["native_independent_plane_equal"]
        plane = bytes.fromhex(page["native_plane_hex"])
        assert sha256(plane).hexdigest() == draft["native_plane_sha256"]
        assert after_layout["complete_consumed_bytes"] == len(body) and 1 <= len(plan["lines"]) <= 4
        edited.append(dict(id=row["id"], block=row["block"], command_offset=offset, selector=compiled[0],
                           source_reference=source, before_hex=before.hex(), after_hex=command.hex(),
                           lines=plan["lines"], page_sha256=sha256(plane).hexdigest(), body_allocation=end - 6,
                           single_page=True, allocation_and_termination_preserved=True,
                           native_inputs_preserved=True))

    natives = [walk(arm, data) for data in (current, bytes(updated))]
    for result in natives:
        assert result["error"] is None
    assert natives[0]["rows"] == natives[1]["rows"]
    extents = {row["offset"]: row for row in natives[1]["rows"]}
    for row in edited:
        native_row = extents[row["command_offset"]]
        assert native_row["word"] == 0x4000 and native_row["native_extent"] == len(bytes.fromhex(row["after_hex"]))
    inverse = updated.copy()
    for row in edited:
        offset, original_hex = row["command_offset"], row["before_hex"]
        data = bytes.fromhex(original_hex)
        inverse[offset:offset + len(data)] = data
    assert bytes(inverse) == current
    return bytes(updated), edited, len(extents)


def stage():
    assert not (STORED.exists() or ROM.exists())
    release, packet = map(read, (parent.RELEASE, gameplay.OUT))
    assert digest(parent.ROM) == release["candidate_sha256"] == packet["candidate_sha256"]
    assert packet["release"] == reference(parent.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    genoa = packet["ordinary_gameplay"]["genoa"]
    assert packet["draft_findings"] == 3
    assert len(genoa["proposed_native_sheets"]) == 1
    assert all(reference(row["path"]) == row for row in genoa["proposed_native_sheets"])
    proposals = defaultdict(list)
    for row in genoa["story"]:
        if row["proposed_English"]:
            proposals[row["block"]].append(row)
    assert sorted(row["id"] for rows in proposals.values() for row in rows) == list(IDS)

    clean, image = map(NdsImage.open, (CLEAN, parent.ROM))
    original, before = map(native.files, (clean, image))
    arm = before[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(before[STORY]).hexdigest() == release["target_SC1_sha256"]
    assert registration.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    source, prior = map(IlnkContainer.parse, (original[STORY], before[STORY]))
    bank = IlnkContainer(prior.blocks.copy())
    font = image.read_file("/GRP/KANJI.FNT")
    renderer = gameplay.town.clipped_renderer(SimpleNamespace(arm=arm, image=image))
    walk = explicit_walk()
    edits, blocks = [], {}
    for block, rows in sorted(proposals.items()):
        current = prior.blocks[block]
        result, entries, count = apply_block(source.blocks[block], current, arm, rows, renderer, font, walk)
        bank.blocks[block] = result
        edits.extend(entries)
        blocks[block] = dict(before_sha256=sha256(current).hexdigest(), after_sha256=sha256(result).hexdigest(),
                             exact_native_command_extents=count)
    updated = bank.to_bytes()
    directory_end = 8 + (len(bank.blocks) + 1) * 4
    assert updated[:directory_end] == before[STORY][:directory_end]
    assert {i for i, (a, b) in enumerate(zip(prior.blocks, bank.blocks, strict=True)) if a != b} == proposals.keys()
    image.replace_file(STORY, updated)
    final = native.files(image)
    assert final.keys() == before.keys() and {p for p in final if before[p] != final[p]} == {STORY}
    guard = bind_registered_story_percent_guard(registration.previous.guard_spec())(original, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    output = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(output)
    assert native.files(NdsImage.open(ROM)) == final
    write(STORED, dict(staged=reference(ROM), clean=reference(CLEAN), predecessor=reference(parent.ROM),
        target_SC1_sha256=sha256(updated).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=release["target_COMMON_sha256"], blocks=blocks, changed=edits,
        source25_guard=guard, whole_parent_inverse=True, unchanged_archive_directory=True,
        editorial_and_preflight=reference(gameplay.OUT), stored_rendering_matches_reviewed_previews=True))
    print(f"Staged and verified {len(edits)} fixed allocations. {digest(ROM)}", flush=True)


def check(action):
    stored = read(STORED)
    proof = dict(candidate=str(ROM), candidate_sha256=stored["staged"]["sha256"],
                 predecessor_sha256=stored["predecessor"]["sha256"], clean_input_sha256=stored["clean"]["sha256"])
    scope = vars(release_checks) | dict(RELEASE=parent.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(release_checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    stage() if action == "stage" else check(action)
