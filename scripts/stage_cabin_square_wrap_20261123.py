"""Review the Auto Move and Square giveaway conversations on the Port Fleet ROM."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from scripts import checkpoint_navigation_prerequisite_review_v1 as navigation
from scripts import register_port_fleet_wrap_20261123 as parent
from scripts import stage_market_introduction_wrap_20261123 as commerce
from scripts import stage_mutiny_review_v1 as portraits
from scripts import stage_square_and_market_reward_wraps_20261123 as prior
from scripts import stage_square_samples_wraps_20261115 as square


base, native, town, market = prior.base, prior.native, prior.town, prior.market
ARM, COMMON, CLEAN = prior.ARM, prior.COMMON, prior.CLEAN
ROOT = Path(".codex-release-work/cabin_square_wrap_20261123/staged")
ROM, PROOF = ROOT / "Cabin_Square_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
NAV_REVIEW = Path("releases/all_routes_editorial_20261111_navigation_prerequisites_candidate/verification/registered_review.json")
NAV_REFLOW = Path("releases/all_routes_editorial_20261121_final_early_wrap_leads_candidate/verification/registered_review.json")
SQUARE_REVIEW = commerce.parent.parent.REVIEW
NAV_IDS = tuple(range(629, 653))
SQUARE_IDS = prior.SQUARE_KEYS
EDITS = {
    649: "Admiral, use the Captain's Cabin. Give the order there.",
    664: "Give these to the locals for free?",
}
EXPECTED = {
    649: ("Admiral, use the Captain's Cabin.", "Give the order there."),
    664: ("Give these to the locals for free?",),
}
NOTES = {
    649: "The Surveyor speaks bluntly after the cabin requirement blocks Auto Move. "
         "Keep the direct address and give the room and the order two short, complete commands.",
    664: "The goods have already been selected in the Square. These refers to that selection. "
         "The quick question preserves this speaker's casual tone and confirms both the recipients and the free offer.",
}


def history():
    records = {}
    for path, keys in ((NAV_REVIEW, NAV_IDS), (NAV_REFLOW, (640,)), (SQUARE_REVIEW, SQUARE_IDS)):
        manifest = base.load(path.parent.parent / "checksums.json")
        sha = base.digest(path)
        assert manifest["verification/registered_review.json"] == sha
        for row in base.load(path)["records"]:
            if row["message_ID"] in keys:
                records[row["message_ID"]] = row, dict(path=str(path), sha256=sha)
    assert set(records) == set(NAV_IDS + SQUARE_IDS)
    return records


def display(ctx, key, raw, group=None, cpu=None):
    if key in SQUARE_IDS:
        parent_pc, table, body, lines = square.layout(ctx.arm, cpu, key, raw)
        return body, lines, dict(parent=parent_pc, table=table)
    actor, _, _ = next(case for case in group["original_voice_choices"] if case[2] == key)
    native_case = portraits.portrait_case(ctx, {"message_ID": key}, group, raw, actor)
    body = native_case.pop("display")
    lines = [part.strip().decode("ascii") for part in body.split(b"\n")]
    return body, lines, native_case


def stage():
    assert not PROOF.exists() and not ROM.exists()
    release = base.load(parent.RELEASE)
    previous = base.digest(parent.ROM)
    assert release["candidate_sha256"] == previous and release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(CLEAN)
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    clean_arm = clean.read_file(ARM)
    ctx = town.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert native.digest(ctx.arm) == release["target_ARM9_sha256"]
    assert native.digest(ctx.common) == release["target_COMMON_sha256"]
    source = town.common_message_entries(clean.read_file(COMMON), clean_arm)
    before = prior.parent.stage.observed.prior.shared.paired.prior.entries(image)
    assert all(ctx.arm[start:end] == clean_arm[start:end] for start, end in square.SOURCE_RANGES)
    square_tables = square.table_selection(ctx.arm)
    assert square_tables == square.table_selection(clean_arm)
    nav_cases = navigation.bind_predicate(clean_arm, ctx.arm)
    nav_groups = navigation.bind_voices(ctx, clean_arm)
    assert len(nav_cases["focused_dependency_results"]) == 32
    assert len(nav_groups) == 3
    nav_owners = {key: group for group in nav_groups for key in range(group["first_ID"], group["last_ID"] + 1)}
    assert set(nav_owners) == set(NAV_IDS)
    compiler = FunctionType(market.compile_layouts.__code__, market.compile_layouts.__globals__ |
        {"PHRASES": {649: EXPECTED[649]}})
    encoded = compiler({key: {"english": prose} for key, prose in EDITS.items()})
    assert all(len(raw) <= len(before[key].text) for key, raw in encoded.items())
    encoded = {key: raw.ljust(len(before[key].text), b" ") for key, raw in encoded.items()}
    deployed, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, encoded)
    assert {old.message_id for old, new in zip(before, after, strict=True) if old != new} == EDITS.keys()
    assert all(slot["new_null_fields"] == 0 for slot in slots.values())
    target = market.with_components(ctx, ctx.arm, deployed)
    old_cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, previews = [], []
    for key, (earlier, receipt) in history().items():
        jp, old, new = source[key], before[key], after[key]
        assert (earlier["source_reference"], earlier["source_hex"]) == (town.reference(jp), jp.text.hex())
        if key == 640:
            earlier_stored = earlier["staged_hex"]
        elif key in NAV_IDS:
            earlier_stored = earlier["registered_reference"]["exact_stored_hex"]
        else:
            earlier_stored = earlier["installed_hex"]
        assert earlier_stored == old.text.hex(), key
        assert all(earlier["review"].values()) and b"%" not in jp.text + old.text + new.text
        address = get(0x5528C, key)
        assert bytes(cpu.mem_read(address, len(new.text) + 1)) == new.text + b"\0"
        group = nav_owners.get(key)
        former_bytes, former, _ = display(ctx, key, old.text, group, old_cpu)
        complete, lines, consumer = display(target, key, new.text, group, cpu)
        english = EDITS.get(key, earlier["english"])
        assert " ".join(lines) == english and 0 < len(lines) <= 4 and all(0 < len(item) <= 36 for item in lines)
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, complete)
        assert [row["code"] for row in glyphs] == town.glyph_codes(complete)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(english[0]), ord(english[-1]))
        if key in EDITS:
            assert tuple(lines) == EXPECTED[key] and former != lines, (key, former, lines)
            old_plane, _ = town.render_portrait(raster, ctx.arm, kanji, former_bytes)
            previews.extend(((f"{key} previous", old_plane), (f"{key} revised", plane)))
        else:
            assert former_bytes == complete
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=earlier["speaker"],
            context=earlier["context"], source_meaning=earlier["source_meaning"], clean_Japanese=jp.text.decode("cp932"),
            localization_note=NOTES.get(key, earlier["localization_note"]), decision="revision" if key in EDITS else "retention",
            source_reference=town.reference(jp), current_reference=town.reference(old), registered_reference=town.reference(new),
            source_hex=jp.text.hex(), current_hex=old.text.hex(), installed_hex=new.text.hex(),
            previous_English=earlier["english"], english=english, previous_lines=former, installed_lines=lines,
            display_hex=complete.hex(), native_plane_sha256=native.digest(plane), consumer=consumer,
            prior_review=receipt, review=dict.fromkeys(town.GATES, True)))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    first = native.files(image)
    image.replace_file(COMMON, deployed)
    final = native.files(image)
    assert first.keys() == final.keys() and {name for name in first if first[name] != final[name]} == {COMMON}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(clean), final)
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(image.rom.save())
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    candidate = base.digest(ROM)
    for row in rows:
        row["registered_reference"].update(candidate_sha256=candidate, file_path=COMMON,
            archive_sha256=native.digest(deployed), exact_stored_hex=row["installed_hex"])
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=previous,
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(ctx.arm),
        target_COMMON_sha256=native.digest(deployed), records=rows, whole_parent_inverse=True,
        source25=guard, allocations=slots, square_voice_tables=square_tables,
        auto_move_cases=nav_cases, auto_move_owners=nav_groups,
        sheets={row["path"]: row["sha256"] for row in town.portrait_sheets(ROOT, previews)},
        translation_policy="natural-dialogue-v2", target_locale="en-US", gates=town.GATES))
    print(f"Staged {candidate}. Checked all {len(rows)} Auto Move and Square texts.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    else:
        step = getattr(prior.parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
