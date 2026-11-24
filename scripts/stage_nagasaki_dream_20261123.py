"""Relocate the four reviewed Nagasaki lines with the registered story compiler."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_supply_ratio_release_inputs_20261123 as checks
from scripts import stage_forest_expeditions_20261118 as compiler
from scripts import verify_nagasaki_dream_20261123 as discovery
from scripts import register_cartridge_title_20261123 as registration
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_current_story_wraps_20261122 import native
from scripts.verify_moonlit_violin_20261121 import bytes_for


ROOT = Path(".codex-release-work/nagasaki_dream_20261123")
ROM, STORED = ROOT / "Nagasaki_Dream_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PARENT = discovery.run.current
ARM, COMMON, STORY, BLOCK = PARENT.ARM, PARENT.COMMON, discovery.STORY, discovery.BLOCK


def stage():
    assert not ROOT.exists()
    packet, release = map(read, (discovery.OUT, PARENT.RELEASE))
    assert digest(PARENT.ROM) == release["candidate_sha256"] == packet["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert packet["observed_story_holds"] == 15
    assert all(digest(row["path"]) == row["sha256"] for row in packet["offline_proposed_pages"])
    clean, image = map(NdsImage.open, (CLEAN, PARENT.ROM))
    before, original = map(native.files, (image, clean))
    arm = before[ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(before[STORY]).hexdigest() == release["target_SC3_sha256"]
    bounds = registration.right_bound(arm, release["right_bound_configuration"])
    assert bounds["matched_repair_spans"] == 8
    bank, japanese = (IlnkContainer.parse(data[STORY]) for data in (before, original))
    context = SimpleNamespace(image=image, arm=arm)
    paint = discovery.panels.town.clipped_renderer(context)
    kanji = image.read_file("/GRP/KANJI.FNT")
    records, revised = [], {}
    for row in packet["story"]:
        src, ref = row["source_reference"], row["installed_reference"]
        a = discovery.panels.exact_command(japanese.blocks[BLOCK], src)
        b = discovery.panels.exact_command(bank.blocks[BLOCK], ref)
        key = int(row["id"].rsplit("_R", 1)[1])
        change = discovery.PROPOSALS.get(key)
        english, phrases = (change[0], change[1]) if change else (" ".join(row["installed_English"].split()), ())
        record = row | dict(file_path=STORY, english=english, protected_phrases=phrases,
            current_reference=dict(command_offset=ref["command_offset"], offset=ref["command_offset"] + 5),
            source_hex=(a[5:6] + bytes_for(a)).hex(), current_hex=(b[5:6] + bytes_for(b)).hex(),
            decision="revision" if change else "retention")
        if change:
            assert set(row["review"]) == set(discovery.GATES) and row["review"]["formatting"] is False
            revised[row["id"]] = row["offline_preflight"]
        records.append(record)
    inventory, _, _ = native.scoped_inventory()
    env = vars(compiler) | dict(plan_progressive=discovery.panels.layout.plan_progressive)
    env["changed_speech"] = FunctionType(compiler.changed_speech.__code__, env)
    rebuild = FunctionType(compiler.rebuild.__code__, env)
    target, commands, plans = rebuild(records, japanese.blocks[BLOCK], bank.blocks[BLOCK], inventory,
                                      original[ARM], arm, None)
    assert plans.keys() == revised.keys() and len(revised) == 4
    stored_visuals = {}
    for binding in commands:
        for key in binding["record_ids"]:
            source, old, new = (bytes.fromhex(binding[col]) for col in ("source", "current", "stored"))
            assert source[:6] == old[:6] == new[:6]
            if key not in revised:
                assert old == new
                continue
            data = bytes_for(new)
            result = paint(arm, kanji, data)
            page, = result["pages"]
            assert page["native_independent_plane_equal"] and result["complete_consumed_bytes"] == len(data)
            actual = sha256(bytes.fromhex(page["native_plane_hex"])).hexdigest()
            assert actual == revised[key]["native_plane_sha256"]
            stored_visuals[key] = dict(page_sha256=actual, lines=plans[key]["lines"], content_hex=data.hex())
    old_block = bank.blocks[BLOCK]
    bank.blocks[BLOCK] = target
    image.replace_file(STORY, bank.to_bytes())
    final = native.files(image)
    assert final.keys() == before.keys() and {path for path in final if before[path] != final[path]} == {STORY}
    after = IlnkContainer.parse(final[STORY]).blocks
    assert {i for i, (a, b) in enumerate(zip(IlnkContainer.parse(before[STORY]).blocks, after, strict=True)) if a != b} == {BLOCK}
    assert after[BLOCK] == target
    guard = bind_registered_story_percent_guard(registration.previous.guard_spec())(original, final)
    assert guard["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(guard["source_bound_new_command_counts"].values())
    content = bytes(image.rom.save())
    image.replace_file(STORY, before[STORY])
    assert bytes(image.rom.save()) == PARENT.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(content)
    assert native.files(NdsImage.open(ROM)) == final
    write(STORED, dict(candidate=reference(ROM), previous=reference(PARENT.ROM), clean=reference(CLEAN),
        source_review=reference(discovery.OUT), changed_file=STORY, changed_block=BLOCK,
        target_SC3_sha256=sha256(final[STORY]).hexdigest(), target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=release["target_COMMON_sha256"], before_block_sha256=sha256(old_block).hexdigest(),
        target_block_sha256=sha256(target).hexdigest(), previous_logical_size=compiler.logical_end(old_block),
        target_logical_size=compiler.logical_end(target), commands=commands, records=records,
        stored_native_pages=stored_visuals, whole_parent_inverse=True, source25=guard))
    print(f"Staged four reviewed lines and verified the complete scene and ROM inverses. {digest(ROM)}")


def check(action):
    stored = read(STORED)
    proof = dict(candidate=str(ROM), candidate_sha256=stored["candidate"]["sha256"],
                 predecessor_sha256=stored["previous"]["sha256"], clean_input_sha256=stored["clean"]["sha256"])
    scope = vars(checks) | dict(RELEASE=PARENT.RELEASE, PATCH=PATCH, REBUILT=REBUILT, STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(getattr(checks, action).__code__, scope)(proof)
    if action == "patch":
        write(PATCH_PROOF, dict(clean_input_sha256=proof["clean_input_sha256"], candidate=reference(ROM),
                               patch=reference(PATCH), rebuilt=reference(REBUILT), byte_exact=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    stage() if action == "stage" else check(action)
