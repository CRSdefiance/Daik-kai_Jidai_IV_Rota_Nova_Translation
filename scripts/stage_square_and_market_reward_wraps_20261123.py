"""Reflow the Square sample pitch and the Market recommendation offer."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_tavern_nearby_town_wrap_20261123 as parent
from scripts import replay_market_reward_dialogue_20261115 as marketplace
from scripts import stage_market_reward_dialogue_20261115 as market
from scripts import stage_square_samples_wraps_20261115 as square


base, native, town = parent.base, parent.native, parent.stage.town
ARM, COMMON, CLEAN = parent.ARM, parent.COMMON, native.CLEAN
ROOT = Path(".codex-release-work/square_and_market_reward_wraps_20261123/staged")
ROM, PROOF = ROOT / "Square_Market_Reward_Wraps_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
SQUARE_REVIEW = Path("releases/all_routes_editorial_20261115_square_samples_wraps_candidate/verification/registered_review.json")
MARKET_REVIEW = Path("releases/all_routes_editorial_20261119_market_followup_candidate/verification/registered_review.json")
SQUARE_KEYS = tuple(range(659, 675))
MARKET_KEYS = (766, *range(774, 784))
EDITS = {
    671: "Try a sample! It's free right now!",
    775: "Here's a letter of recommendation. Thanks for all those popular goods!",
}
NOTES = {
    671: "Give the invitation and temporary free offer two short beats. The whole shout fits without a break after It's.",
    775: "This branch delivers an extra reward after the sale. The trader offers the letter directly, and all those keeps the quantity that earns it. The offer and the thanks each fit on a complete row.",
}


def histories():
    records = {}
    for path, keys in ((SQUARE_REVIEW, SQUARE_KEYS), (MARKET_REVIEW, MARKET_KEYS)):
        checksums = base.load(path.parent.parent / "checksums.json")
        assert base.digest(path) == checksums["verification/registered_review.json"]
        for row in base.load(path)["records"]:
            if row["message_ID"] in keys:
                records[row["message_ID"]] = (row, path)
    assert set(records) == set(SQUARE_KEYS + MARKET_KEYS)
    return records


def display(ctx, en, key, cpu):
    if key in SQUARE_KEYS:
        _, _, data, visible = square.layout(ctx.arm, cpu, key, en)
    else:
        data, visible = market.native_layout(cpu, en, key, (), parent=0x02054014)
    return data, visible


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
    get_records = parent.stage.observed.prior.shared.paired.prior.entries
    before = get_records(image)
    assert all(clean_arm[a:b] == ctx.arm[a:b] for a, b in square.SOURCE_RANGES)
    original_giveaway = square.table_selection(ctx.arm)
    assert original_giveaway == square.table_selection(clean_arm) and len(original_giveaway) == 16
    original_reward = market.original_branches(clean_arm, ctx.arm)
    compile_market = FunctionType(market.compile_layouts.__code__, market.compile_layouts.__globals__ |
        {"PHRASES": {775: tuple(EDITS[775].removesuffix("!").split(". "))}})
    encoded = {671: EDITS[671].encode("ascii"), **compile_market({775: {"english": EDITS[775]}})}
    for key, raw in encoded.items():
        assert len(raw) <= len(before[key].text)
        encoded[key] = raw.ljust(len(before[key].text), b" ")
    deployed, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, encoded)
    assert {old.message_id for old, new in zip(before, after, strict=True) if old != new} == EDITS.keys()
    assert all(slots[key]["new_null_fields"] == 0 for key in EDITS)
    target = market.with_components(ctx, ctx.arm, deployed)
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, previews = [], []
    for key, (prior, path) in histories().items():
        jp, old, new = source[key], before[key], after[key]
        assert prior["source_hex"] == jp.text.hex() and prior["source_reference"] == town.reference(jp)
        assert all(prior["review"].values()) and b"%" not in jp.text + old.text + new.text
        assert " ".join(old.text.decode("ascii").split()) == prior["english"]
        address = get(0x5528C, key)
        assert bytes(cpu.mem_read(address, len(new.text) + 1)) == new.text + b"\0"
        former_bytes, former = display(ctx, old.text, key, cpu)
        complete, lines = display(ctx, new.text, key, cpu)
        english = EDITS.get(key, prior["english"])
        assert " ".join(lines) == english and 0 < len(lines) <= 4 and all(0 < len(item) <= 36 for item in lines)
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, complete)
        assert [row["code"] for row in glyphs] == town.glyph_codes(complete)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(english[0]), ord(english[-1]))
        if key in EDITS:
            old_plane, _ = town.render_portrait(raster, ctx.arm, kanji, former_bytes)
            assert old_plane != plane and len(lines) < len(former)
            previews.extend(((f"{key} previous", old_plane), (f"{key} revised", plane)))
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=prior["speaker"],
            context=prior["context"], source_meaning=prior["source_meaning"], clean_Japanese=jp.text.decode("cp932"),
            localization_note=NOTES.get(key, prior["localization_note"]), decision="revision" if key in EDITS else "retention",
            source_reference=town.reference(jp), current_reference=town.reference(old), registered_reference=town.reference(new),
            source_hex=jp.text.hex(), current_hex=old.text.hex(), installed_hex=new.text.hex(),
            previous_English=prior["english"], english=english, previous_lines=former, installed_lines=lines,
            display_hex=complete.hex(), native_plane_sha256=native.digest(plane),
            prior_review=dict(path=str(path), sha256=base.digest(path)), review=dict.fromkeys(town.GATES, True)))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    first = native.files(image)
    image.replace_file(COMMON, deployed)
    final = native.files(image)
    assert first.keys() == final.keys() and {p for p in first if first[p] != final[p]} == {COMMON}
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
    base.save(PROOF, dict(candidate_sha256=candidate, predecessor_sha256=previous, clean_sha256=release["clean_input_sha256"],
        target_ARM9_sha256=native.digest(ctx.arm), target_COMMON_sha256=native.digest(deployed), records=rows,
        whole_parent_inverse=True, source25=guard, allocations=slots,
        square_giveaway_selectors=original_giveaway, market_reward_selectors=original_reward,
        sheets={row["path"]:row["sha256"] for row in town.portrait_sheets(ROOT, previews)},
        translation_policy="natural-dialogue-v2", target_locale="en-US", gates=town.GATES))
    print(f"Staged {candidate}. Reconciled {len(rows)} records and verified both revised native pages.")


def market_replay(action):
    previous = base.load(parent.RELEASE)
    proof = base.load(PROOF) if action == "new_market" else None
    arm = previous["target_ARM9_sha256"]
    expected = proof["candidate_sha256"] if proof else previous["candidate_sha256"]
    target = ROM if proof else parent.ROM
    ROOT.mkdir(parents=True, exist_ok=True)
    outputs = ROOT / action
    outputs.mkdir()
    receipt = outputs / "replay_contract.json"
    base.save(receipt, dict(previous_sha256=expected, candidate_sha256=expected, target_ARM9_sha256=arm))
    settings = SimpleNamespace(base=base, ROOT=outputs, ROM=target, STORED=receipt, ARM=ARM, digest=native.digest)
    run = FunctionType(marketplace.reward.__code__, vars(marketplace) | dict(stage=settings, __file__=__file__))
    run("reviewed" if proof else "current", target)


if __name__ == "__main__":
    options = ArgumentParser(description=__doc__)
    options.add_argument("action", choices=("stage", "patch", "startup", "old_market", "new_market"))
    action = options.parse_args().action
    if action == "stage":
        stage()
    elif action.endswith("_market"):
        market_replay(action)
    else:
        step = getattr(parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
