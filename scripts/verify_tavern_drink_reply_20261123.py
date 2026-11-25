"""Check the accepted and declined drink flows and the ordinary Syracuse departure."""

import ast
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_tavern_drink_reply_20261123 as stage
from scripts import verify_additional_voyages_20261123 as voyages
from scripts import verify_square_and_market_reward_wraps_20261123 as shared
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
LIVE = stage.ROOT / "ordinary_dialogue.json"
REPLAY_DRIVER = stage.ROOT / "replay_driver_snapshot.py"


def rebound_replay(terminal, candidate):
    producer = Path(stage.__file__).resolve()

    def replay_function(path):
        tree = ast.parse(path.read_bytes())
        node, = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "replay"]
        return ast.dump(node)

    assert replay_function(producer) == replay_function(REPLAY_DRIVER)
    receipt = base.load(terminal)
    matching, = [path for path in receipt["evidence"] if Path(path).resolve() == producer]
    assert base.digest(REPLAY_DRIVER) == receipt["evidence"][matching]
    source = checked_text(getsource(stage.run_records), {
        'assert all(base.digest(path) == sha for path, sha in result["evidence"].items())':
            'result["evidence"][str(REPLAY_DRIVER)] = result["evidence"].pop(ORIGINAL_PRODUCER)\n'
            '    assert all(base.digest(path) == sha for path, sha in result["evidence"].items())',
    })
    scope = vars(stage) | dict(REPLAY_DRIVER=REPLAY_DRIVER, ORIGINAL_PRODUCER=matching)
    exec(compile(source, __file__ + "::source_locked_replay_rebind", "exec"), scope)
    return scope["run_records"](terminal, candidate)


def departure(stored, clean, installed, image, pending):
    root = stage.ordinary.ROOT / "village"
    terminal_path = root / "terminal.json"
    terminal = base.load(terminal_path)
    report = base.load(root / "capture/capture_report.json")
    assert terminal["ROM_sha256"] == report["ROM_sha256"] == stored["predecessor_sha256"]
    assert all(base.digest(path) == sha for path, sha in terminal["evidence"].items())
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    schedule, _, end, _, donor = stage.ordinary.schedule("village")
    assert report["scripted_input_schedule"] == schedule and report["frames"] == end
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    requests = terminal["target_COMMON_calls"]
    assert [row["message_ID"] for row in requests] == [85, 85, 86, 86]
    assert not pending.intersection(row["message_ID"] for row in requests)
    raster = voyages.font_tools(image)[0]
    arm, kanji = (image.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    frames = shared.market.shots(report)
    evidence, rows = terminal["evidence"].copy(), []
    for index, (key, frame, args) in enumerate(((85, 3800, ("38",)),
            (86, 4600, ("6", "12", "Sky: Sunny", "Syracuse")))):
        getter, copier = requests[index * 2:index * 2 + 2]
        assert (getter["PC"], copier["PC"]) == (0x0205528C, 0x020534F4)
        assert dict(getter, PC=copier["PC"]) == copier
        jp, en = clean[key], installed[key]
        history, proof = voyages.review_for(key, jp, en)
        payload = en.text.rstrip(b" ") % tuple(value.encode("ascii") for value in args)
        shot = frames[frame]
        screen = shared.market.captured(shot).convert("RGB")
        shown, digest = voyages.system_plane(raster, arm, kanji, payload, screen)
        evidence[shot["path"]] = shot["PNG_sha256"]
        rows.append(dict(message_ID=key, source_reference=stage.town.reference(jp),
            installed_reference=stage.town.reference(en), source_hex=jp.text.hex(), installed_hex=en.text.hex(),
            lines=shown.decode("ascii").splitlines(), arguments=args, native_plane_sha256=digest, screenshot=shot,
            decision="retention", source_meaning=history["source_meaning"], localization_note=voyages.NOTES[key],
            review=history["review"], prior_review=proof))
    return dict(holds=rows, village_reached=False, ordinary_gameplay=True, evidence=evidence)


def main():
    assert not LIVE.exists()
    stored, release = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    assert base.digest(stage.parent.ROM) == stored["predecessor_sha256"] == release["candidate_sha256"]
    before, original = stage.run_records(stage.BASELINE, stored["predecessor_sha256"])
    after, revision = rebound_replay(stage.PLAY / "tavern/terminal.json", stored["candidate_sha256"])
    requests = before["target_COMMON_calls"]
    assert requests == after["target_COMMON_calls"]
    for key in ("scripted_input_schedule", "core_DLL_sha256", "core_options"):
        assert original[key] == revision[key]
    assert [r["message_ID"] for r in requests[::2]] == [51, 53, 821, 55, 56, 59, 61, 827, 53, 823, 55, 57, 59, 826]
    pending = {row["message_ID"] for row in base.load(stage.parent.REVIEW)["shared_consumer_binding"]["records"]}
    assert not pending.intersection(r["message_ID"] for r in requests)
    clean = base.NdsImage.open(stage.CLEAN)
    source = stage.town.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    image = base.NdsImage.open(stage.ROM)
    installed = stage.prior.prior.parent.stage.observed.prior.shared.paired.prior.entries(image)
    ctx = stage.town.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    arm, kanji = (image.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    assert arm == ctx.arm
    raster, _, _ = stage.town.font_tools(image)
    a, b = map(shared.market.shots, (original, revision))
    scope = vars(shared) | {"stage": stage}
    hold = FunctionType(shared.display_hold.__code__, scope)
    render = FunctionType(shared.render_sheet.__code__, scope)
    rows = {row["message_ID"]: row for row in stored["records"]}
    evidence = before["evidence"] | after["evidence"]
    cases, pictures = [], []
    font = voyages.check.GameAsciiFont.from_arm9(arm)
    for frame, (key, speaker, args, _) in stage.HOLDS.items():
        row = rows[key]
        lr = row["native_request"]["caller_LR"]
        older, _ = stage.display(ctx, key, bytes.fromhex(row["current_hex"]), cpu, args, lr)
        layouts = [older, bytes.fromhex(row["display_hex"])]
        planes = [stage.town.render_portrait(raster, arm, kanji, layout)[0] for layout in layouts]
        assert stage.native.digest(planes[-1]) == row["native_plane_sha256"]
        offset = 6 if key == 59 else 0
        if offset:
            planes = [stage.town.render_portrait(raster, arm, kanji, b" " + layout)[0] for layout in layouts]
        seen, pair = hold(key, frame, a[frame], b[frame], *planes, evidence)
        ink, bounds = voyages.check.complete_mask(font, speaker, pair[-1].convert("RGB"), 16, 277, (98, 97, 98))
        cases.append(seen | dict(speaker=speaker, nameplate=dict(ink=ink, bounds=bounds), ink_origin_offset=offset))
        if key in (55, 59, 827, 826):
            pictures.append((f"Istanbul / {speaker} / COMMON {key}", pair))
    assert original["scripted_input_schedule"] == revision["scripted_input_schedule"]
    assert any(row["start"] == 9201 and row["buttons"] == ["A"] for row in revision["scripted_input_schedule"])
    assert any(row["start"] == 9601 and row["buttons"] == ["B"] for row in revision["scripted_input_schedule"])
    for frame in (9400, 10801):
        assert a[frame]["PNG_sha256"] == b[frame]["PNG_sha256"]
        for shot in (a[frame], b[frame]):
            evidence[shot["path"]] = shot["PNG_sha256"]
    sailing = departure(stored, source, installed, image, pending)
    evidence.update(sailing["evidence"])
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        observed={"Istanbul": cases}, Syracuse=sailing, revised_holds=1, retained_holds=10, menu_transitions=2,
        from_existing_battery_saves=True, ordinary_gameplay=True, hardware=False,
        revised_offline_only_records=[], pending_requested=[], evidence=evidence,
        sheets=render("istanbul_tavern", pictures)))
    print("Verified eleven Tavern holds and two Syracuse departure notices in ordinary gameplay.")


if __name__ == "__main__":
    main()
