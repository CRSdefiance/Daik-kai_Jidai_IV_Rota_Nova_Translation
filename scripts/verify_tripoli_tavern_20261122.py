"""Bind the Tripoli greeting, drink price and local lead to original gameplay."""

from types import FunctionType

from scripts import observe_tripoli_tavern_20261122 as capture
from scripts import verify_tripoli_copenhagen_20261122 as prior


stage = capture.stage
base, town, check, visual, masks = prior.base, prior.town, prior.check, prior.visual, prior.masks
ROOT = capture.ROOT
OUTPUT = ROOT / "verified_tavern.json"
captures = FunctionType(prior.captures.__code__, prior.captures.__globals__ | dict(ROOT=ROOT))
PANELS = {
    51: (4950, (), "A direct greeting leads naturally to the drink menu."),
    53: (5750, (), "This exact COMMON message gives the fixed five-coin price before the local lead."),
    823: (6150, ("Algiers",), "The Barkeep asks if the player knows the town supplied by the original substitution, then explains that it is nearby."),
}


def verify():
    assert not OUTPUT.exists()
    parent, staged = map(base.load, (stage.parent.RELEASE, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert candidate == staged["candidate_sha256"] and parent["candidate_sha256"] == staged["predecessor_sha256"]
    assert base.digest(town.CLEAN) == parent["clean_input_sha256"]
    report, requests, evidence = captures(capture.CASE, capture.schedule, candidate)
    assert [r["message_ID"] for r in requests] == [key for key in PANELS for _ in range(2)]
    frames = check.shots(report)
    old, image = map(base.NdsImage.open, (town.CLEAN, stage.ROM))
    arm, common = image.read_file(town.ARM), image.read_file(town.COMMON)
    assert stage.native.digest(arm) == parent["target_ARM9_sha256"] and stage.native.digest(common) == parent["target_COMMON_sha256"]
    clean = check.common_message_entries(old.read_file(town.COMMON), old.read_file(town.ARM))
    installed = check.owned_entries(common, arm, check.sha256(arm[check.DIRECTORY_OFFSET:check.TABLE_OFFSET]).hexdigest())
    ctx = town.RegisteredRuntime(stage.parent.RELEASE, parent["own_registered_startup"], captain=3)
    assert ctx.image.read_file(town.ARM) == arm and ctx.common == common
    cpu, _, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    names = check.GameAsciiFont.from_arm9(arm)
    renderer, _, _ = town.font_tools(ctx.image)
    font = image.read_file("/GRP/KANJI.FNT")
    decisions, pictures = [], []

    def view(frame, title):
        shot = frames[frame]
        assert base.digest(shot["path"]) == shot["PNG_sha256"]
        evidence[shot["path"]] = shot["PNG_sha256"]
        panel = check.captured(shot).convert("RGB")
        pictures.append((title, panel))
        return shot, panel

    for frame in (4000, 4950, 5350, 5750, 6150, 6550):
        key = next((k for k, v in PANELS.items() if frame == v[0]), None)
        if key is None:
            title = {4000: "Tripoli entry", 5350: "Tavern menu", 6550: "Return to the Tavern menu"}[frame]
            view(frame, title)
            continue
        first, copy = (r for r in requests if r["message_ID"] == key)
        assert [first["PC"], copy["PC"]] == [0x0205528C,0x020534F4] and first["frame"] == copy["frame"]
        assert 0 < frame-first["frame"] < 160
        at, args, note = PANELS[key]
        source, target = clean[key], installed[key]
        shot, panel = view(at, f"Tripoli Barkeep / COMMON {key}")
        formatted, lines = town.native_layout(cpu, target.text, key, args)
        pixels, checks = town.render_portrait(renderer, arm, font, formatted)
        assert town.glyph_codes(formatted) == [g["code"] for g in checks]
        assert masks.mask_check(bytes(pixels), 228, panel), (key, lines)
        ink, bounds = check.complete_mask(names, "Barkeep", panel, 16, 277, (98,97,98))
        assert (key != 53 or target.text == b"5 coins.") and all(lines)
        decisions.append(dict(message_ID=key, clean_Japanese=source.text.decode("cp932"),
            installed_English=target.text.decode("ascii"), visible_lines=lines, source_reference=check.reference(source),
            current_reference=check.reference(target), original_requests=[first,copy], capture=shot,
            nameplate=dict(text="Barkeep", pixels=ink, bounds=bounds), preserved_runtime_arguments=list(args),
            native_plane_sha256=check.sha256(bytes(pixels)).hexdigest(), localization_note=note, decision="retention",
            review=dict.fromkeys(town.GATES, True)))
    path, sha = visual.make_sheet(ROOT / "tripoli_tavern.png", pictures)
    assert all(base.digest(p)==h for p,h in evidence.items())
    base.save(OUTPUT, dict(candidate_sha256=candidate, port="Tripoli", message_ID=51, ordinary_saved_gameplay=True,
        decisions=decisions, evidence=evidence, sheets=[dict(path=path,sha256=sha)], hardware=False, new_editorial_credit=0))
    print("Verified the original greeting, five-coin price and Algiers lead.",flush=True)


if __name__ == "__main__":
    verify()
