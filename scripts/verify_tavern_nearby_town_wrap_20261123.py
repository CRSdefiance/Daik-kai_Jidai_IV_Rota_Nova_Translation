"""Compare both revised Tavern holds and the unchanged alternate gossip in ordinary play."""

from inspect import getsource
from types import FunctionType

from scripts import stage_tavern_nearby_town_wrap_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town = stage.base, stage.native, stage.town
observed, captures = stage.observed, stage.observed.prior_captures
check = observed.check
LIVE = stage.ROOT / "ordinary_dialogue.json"

source = checked_text(getsource(observed.check_holds), {
    'assert any(line.endswith("It\'s") for line in lines[:-1])':
        'assert lines == ["Have you heard of a nearby town", f"called {args[0]}?"]',
    'result.update(decision="wrap follow-up")':
        'result.update(decision="revision", review=dict.fromkeys(town.GATES, True))',
})
scope = vars(observed).copy()
exec(compile(source, __file__ + "::holds", "exec"), scope)


def main():
    assert not LIVE.exists()
    stored, baseline, release = map(base.load, (stage.PROOF, observed.OUT, stage.parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"]
    assert baseline["candidate_sha256"] == release["candidate_sha256"] == stored["predecessor_sha256"]
    assert base.digest(observed.OUT) == stored["inherited_observations_sha256"]
    clean, rom = map(base.NdsImage.open, (stage.CLEAN, stage.ROM))
    arm, common = (rom.read_file(path) for path in (stage.ARM, stage.COMMON))
    assert native.digest(arm) == release["target_ARM9_sha256"] == stored["target_ARM9_sha256"]
    assert native.digest(common) == stored["target_COMMON_sha256"]
    js = check.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    en = observed.prior.shared.paired.prior.entries(rom)
    ctx = town.RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    # The replay reads the revised archive. The offline formatter takes the
    # exact installed text explicitly and uses the unchanged native runtime.
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    renderer, _, _ = town.font_tools(rom)
    kanji, font = rom.read_file("/GRP/KANJI.FNT"), check.GameAsciiFont.from_arm9(arm)
    current = FunctionType(captures.__code__, captures.__globals__ | dict(ROOT=stage.PLAY))
    old = FunctionType(captures.__code__, captures.__globals__ | dict(ROOT=observed.ROOT))
    alexandria, = [row for row in stored["native_town_cases"] if row["town"] == "Alexandria"]
    observed_holds, sheets, evidence = {}, {}, {}
    for case in ("tunis", "syracuse"):
        schedule = stage.encounters.schedule
        report, requests, traces = current(case, schedule, candidate)
        older, old_requests, _ = old(case, schedule, baseline["candidate_sha256"])
        assert requests == old_requests
        frames, old_frames = map(check.shots, (report, older))
        holds, images = scope["check_holds"](case, ctx, frames, requests, js, en, cpu, renderer, kanji, font, None)
        for row, previous in zip(holds, baseline["cases"][case]["common_holds"], strict=True):
            assert row["message_ID"] == previous["message_ID"] and row["source_hex"] == previous["source_hex"]
            assert list(row["arguments"]) == previous["arguments"] and row["speaker"] == previous["speaker"]
            row["native_mask_exact"] = True
            if row["message_ID"] == stage.KEY:
                assert row["native_plane_sha256"] == alexandria["native_plane_sha256"]
                row["previous_lines"] = previous["lines"]
            else:
                assert row["installed_hex"] == previous["installed_hex"]
                assert row["native_plane_sha256"] == previous["native_plane_sha256"]
        for frame, label in ((10750, "Drink menu"), (11850, "Return to drink menu")):
            assert frames[frame]["PNG_sha256"] == old_frames[frame]["PNG_sha256"]
            traces[frames[frame]["path"]] = frames[frame]["PNG_sha256"]
            images.append((f"{case.title()} / {label}", check.captured(frames[frame]).convert("RGB")))
        for index in range(0, len(images), 4):
            path, digest = observed.visual.make_sheet(stage.ROOT / f"{case}_tavern_{1+index//4}.png", images[index:index+4])
            sheets[path] = digest
        observed_holds[case] = holds
        evidence.update(traces)
    assert sum(row["decision"] == "revision" for rows in observed_holds.values() for row in rows) == 2
    base.save(LIVE, dict(candidate_sha256=candidate, predecessor_sha256=stored["predecessor_sha256"],
        ordinary_battery_save_gameplay=True, observed=observed_holds, evidence=evidence, sheets=sheets,
        revised_holds=2, retained_holds=8, menu_transitions=4, revised_offline_only_records=[], hardware=False))
    print("Verified two revised Tunis holds, eight retained holds and four unchanged drink-menu transitions.")


if __name__ == "__main__":
    main()
