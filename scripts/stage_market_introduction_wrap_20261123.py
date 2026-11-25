"""Check and stage the Market's ordinary letter-of-introduction offer."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from textwrap import dedent
from types import FunctionType, SimpleNamespace

from scripts import observe_recommendation_v4984c as observer
from scripts import register_title_reports_label_20261123 as parent
from scripts import stage_square_and_market_reward_wraps_20261123 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town, market = prior.base, prior.native, prior.town, prior.market
ARM, COMMON, CLEAN = prior.ARM, prior.COMMON, prior.CLEAN
ROOT = Path(".codex-release-work/market_intro_wrap_20261123/staged")
ROM, PROOF = ROOT / "Market_Introduction_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
EDITS = {774: "Here's a letter of introduction. Thanks for the popular goods!"}
EXPECTED_LINES = ("Here's a letter of introduction.", "Thanks for the popular goods!")
BRANCH_INPUT = 12
CHAIN = [774, 779, 766]


def display(ctx, data, key, cpu):
    return market.native_layout(cpu, data, key, (), parent=0x02054014)


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
    original_branches = market.original_branches(clean_arm, ctx.arm)
    assert CHAIN in [row["IDs"] for row in original_branches["chains"]]
    branch_span = slice(0xBBCA4, 0xBBCBC)
    assert clean_arm[branch_span] == ctx.arm[branch_span]
    compile_market = FunctionType(market.compile_layouts.__code__, market.compile_layouts.__globals__ |
        {"PHRASES": {774: ("a letter of introduction.", "Thanks for the popular goods!")}})
    encoded = compile_market({774: {"english": EDITS[774]}})
    assert len(encoded[774]) <= len(before[774].text)
    encoded[774] = encoded[774].ljust(len(before[774].text), b" ")
    deployed, after, slots = town.owned_deployment(ctx.common, ctx.arm, before, encoded)
    assert {old.message_id for old, new in zip(before, after, strict=True) if old != new} == EDITS.keys()
    assert slots[774]["new_null_fields"] == 0
    target = market.with_components(ctx, ctx.arm, deployed)
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    raster, _, _ = town.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    history = base.load(parent.parent.REVIEW)
    historical = {row["message_ID"]: row for row in history["records"] if row["message_ID"] in prior.MARKET_KEYS}
    assert set(historical) == set(prior.MARKET_KEYS)
    rows, previews = [], []
    for key, earlier in historical.items():
        jp, old, new = source[key], before[key], after[key]
        assert (earlier["source_reference"], earlier["source_hex"]) == (town.reference(jp), jp.text.hex())
        assert earlier["installed_hex"] == old.text.hex()
        assert all(earlier["review"].values()) and b"%" not in jp.text + old.text + new.text
        address = get(0x5528C, key)
        assert bytes(cpu.mem_read(address, len(new.text) + 1)) == new.text + b"\0"
        former_bytes, former = display(ctx, old.text, key, cpu)
        complete, lines = display(ctx, new.text, key, cpu)
        english = EDITS.get(key, earlier["english"])
        assert " ".join(lines) == english and 0 < len(lines) <= 4 and all(0 < len(item) <= 36 for item in lines)
        plane, glyphs = town.render_portrait(raster, ctx.arm, kanji, complete)
        assert [row["code"] for row in glyphs] == town.glyph_codes(complete)
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(english[0]), ord(english[-1]))
        note = earlier["localization_note"]
        if key == 774:
            assert tuple(lines) == EXPECTED_LINES and len(former) == 4, (former, lines)
            old_plane, _ = town.render_portrait(raster, ctx.arm, kanji, former_bytes)
            previews.extend(((f"{key} previous", old_plane), (f"{key} revised", plane)))
            note = ("The trader offers the letter on the spot and thanks the player for the popular goods. "
                    "The next panel keeps the small-town restriction. The introduction and thanks each fit on one row.")
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker=earlier["speaker"],
            context=earlier["context"], source_meaning=earlier["source_meaning"], clean_Japanese=jp.text.decode("cp932"),
            localization_note=note, decision="revision" if key == 774 else "retention",
            source_reference=town.reference(jp), current_reference=town.reference(old), registered_reference=town.reference(new),
            source_hex=jp.text.hex(), current_hex=old.text.hex(), installed_hex=new.text.hex(),
            previous_English=earlier["english"], english=english, previous_lines=former, installed_lines=lines,
            display_hex=complete.hex(), native_plane_sha256=native.digest(plane),
            prior_review=dict(path=str(parent.parent.REVIEW), sha256=base.digest(parent.parent.REVIEW)),
            review=dict.fromkeys(town.GATES, True)))
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
        source25=guard, allocations=slots, market_reward_selectors=original_branches,
        introduction_threshold_window_sha256=native.digest(ctx.arm[branch_span]), introduction_quantity_input=BRANCH_INPUT,
        sheets={row["path"]: row["sha256"] for row in town.portrait_sheets(ROOT, previews)},
        translation_policy="natural-dialogue-v2", target_locale="en-US", gates=town.GATES))
    print(f"Staged {candidate}. Reconciled {len(rows)} Market records and verified the revised native page.")


def market_replay(action):
    previous = base.load(parent.RELEASE)
    proof = base.load(PROOF) if action == "new_market" else None
    expected = proof["candidate_sha256"] if proof else previous["candidate_sha256"]
    target = ROM if proof else parent.ROM
    outputs = ROOT / action
    outputs.mkdir(exist_ok=True)
    receipt = outputs / "replay_contract.json"
    base.save(receipt, dict(previous_sha256=expected, candidate_sha256=expected,
        target_ARM9_sha256=previous["target_ARM9_sha256"]))
    settings = SimpleNamespace(base=base, ROOT=outputs, ROM=target, STORED=receipt, ARM=ARM, digest=native.digest)
    run = FunctionType(prior.marketplace.reward.__code__,
        vars(prior.marketplace) | dict(stage=settings, __file__=__file__))
    init = checked_text(dedent(getsource(observer.Observer.__init__)), {
        "value=16": f"value={BRANCH_INPUT}",
        "supplied_reward_quantity_input=16": f"supplied_reward_quantity_input={BRANCH_INPUT}",
    })
    scope = vars(observer).copy()
    exec(compile(init, __file__ + "::introduction_observer", "exec"), scope)
    original = observer.Observer.__init__
    observer.Observer.__init__ = FunctionType(scope["__init__"].__code__, vars(observer))
    case = "reviewed" if proof else "current"
    try:
        run(case, target)
    finally:
        observer.Observer.__init__ = original
    path = outputs / case / "run_plan.json"
    plan = base.load(path)
    assert plan.pop("synthetic_qualification2_reward_quantity16_and_bonus1_inputs_at_original_BBCA4")
    plan["synthetic_qualification2_quantity12_and_bonus1_inputs_at_original_BBCA4"] = True
    base.save(path, plan)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup", "old_market", "new_market"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    elif action.endswith("_market"):
        market_replay(action)
    else:
        step = getattr(prior.parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
