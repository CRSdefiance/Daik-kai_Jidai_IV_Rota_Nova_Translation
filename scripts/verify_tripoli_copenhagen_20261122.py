"""Verify ordinary Square and Tavern panels against the exact COMMON records."""

from pathlib import Path

from scripts import checkpoint_regional_town_dialogue_20261115 as check
from scripts import observe_tripoli_copenhagen_20261122 as visits
from scripts import observe_tripoli_square_20261122 as tripoli
from scripts import verify_story_literal_names_20261122 as visual
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as masks
from scripts.stage_square_rumors_20261115 import template as town


stage = visits.stage
base = stage.base
ROOT = visits.ROOT
OUTPUT = ROOT / "verified_visits.json"
LABELS = {
    51: ("Barkeep", "The invitation to order gives the player a clear handoff to the drink menu."),
    656: ("Shopkeeper", "The shopkeeper's brief answer identifies retail sales in the Square."),
    657: ("Shopkeeper", "The question tag stays intact, followed by a referral to the Market for bulk trade."),
    658: ("Shopkeeper", "The casual echo and hope for a deal preserve the shopkeeper's modest assessment."),
    718: ("Shopkeeper", "Keep the relationship in the shopkeeper's words, including the distinction between a man he called his father and a claimed birth relationship."),
}
RUNS = {
    "copenhagen": ("copenhagen", visits.schedule, 3720),
    "tripoli": ("tripoli_square", tripoli.schedule, 4000),
}


def captures(case, schedule, candidate):
    folder = ROOT / case
    paths = [folder / p for p in ("capture/capture_report.json", "requests.json", "terminal.json")]
    report, trace, terminal = map(base.load, paths)
    inputs, _, end, source, donor = schedule(case)
    assert candidate == report["ROM_sha256"] == terminal["ROM_sha256"] and report["frames"] == end
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == inputs and not any(v for k,v in report.items() if k.startswith("synthetic_"))
    battery = report["battery_save_preloaded"]
    assert battery["copied_byte_exact_before_cold_boot"] and battery["source_sha256"] == donor["source_sha256"] == base.digest(donor["source"])
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_requests"] == terminal["target_COMMON_calls"]
    evidence = {str(p): base.digest(p) for p in paths}
    for name, expected in terminal["evidence"].items():
        path = Path(name)
        if case == "copenhagen" and path.name == Path(visits.__file__).name:
            path = ROOT / "copenhagen_observer_original.py"
        assert base.digest(path) == expected
        evidence[str(path)] = expected
    return report, trace["source_requests"], evidence


def verify():
    assert not OUTPUT.exists()
    parent = base.load(stage.parent.RELEASE)
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and parent["candidate_sha256"] == proof["predecessor_sha256"]
    assert base.digest(town.CLEAN) == parent["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (town.CLEAN, stage.ROM))
    arm, common = (rom.read_file(path) for path in (town.ARM, town.COMMON))
    assert stage.native.digest(arm) == parent["target_ARM9_sha256"] and stage.native.digest(common) == parent["target_COMMON_sha256"]
    src = check.common_message_entries(clean.read_file(town.COMMON), clean.read_file(town.ARM))
    installed = check.owned_entries(common, arm, check.sha256(arm[check.DIRECTORY_OFFSET:check.TABLE_OFFSET]).hexdigest())
    ctx = town.RegisteredRuntime(stage.parent.RELEASE, parent["own_registered_startup"], captain=3)
    assert ctx.image.read_file(town.ARM) == arm and ctx.common == common
    cpu, _, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    font = check.GameAsciiFont.from_arm9(arm)
    renderer, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    results, sheets, all_evidence = {}, [], {}
    for name, (case, schedule, entry) in RUNS.items():
        report, requests, evidence = captures(case, schedule, candidate)
        frames = check.shots(report)
        upcoming = [r for r in requests if r["frame"] > entry and r["message_ID"] in LABELS]
        observations, seen = [], set()
        pictures = [(f"{name.title()} / town entry", check.captured(frames[entry]).convert("RGB"))]
        evidence[frames[entry]["path"]] = frames[entry]["PNG_sha256"]
        for direct, copied in zip(upcoming[::2], upcoming[1::2], strict=True):
            assert [r["PC"] for r in (direct, copied)] == [0x0205528C, 0x020534F4]
            assert {k:v for k,v in direct.items() if k!="PC"} == {k:v for k,v in copied.items() if k!="PC"}
            key = direct["message_ID"]
            if key in seen:
                continue
            t = next((n for n in frames if 0 < n-direct["frame"] <= 160), None)
            if t is None:
                continue
            held = frames[t]
            assert base.digest(held["path"]) == held["PNG_sha256"]
            image = check.captured(held).convert("RGB")
            target, clean_text = installed[key], src[key]
            assert b"%" not in target.text and b"%" not in clean_text.text
            formatted, lines = town.native_layout(cpu, target.text, key, ())
            assert 1 <= len(lines) <= 4 and " ".join(lines) == " ".join(target.text.decode("ascii").split())
            pixels, glyphs = town.render_portrait(renderer, arm, kanji, formatted)
            assert [g["code"] for g in glyphs] == town.glyph_codes(formatted)
            assert masks.mask_check(bytes(pixels), 228, image), (name, key, t, lines)
            body = dict(lines=lines, full_plane_sha256=check.sha256(bytes(pixels)).hexdigest())
            label, note = LABELS[key]
            total, bounds = check.complete_mask(font, label, image, 16, 277, (98, 97, 98))
            evidence[held["path"]] = held["PNG_sha256"]
            observations.append(dict(message_ID=key, capture=held, original_requests=[direct, copied],
                Japanese=clean_text.text.decode("cp932"), English=target.text.decode("ascii"),
                source_reference=check.reference(clean_text), current_reference=check.reference(target),
                complete_body=body, nameplate=dict(text=label, pixels=total, bounds=bounds), localization_note=note,
                decision="retention", review=dict.fromkeys(town.GATES, True), new_editorial_credit=0))
            pictures.append((f"{name.title()} / {label} / COMMON {key}", image))
            seen.add(key)
        assert seen == ({51, 656, 657, 658} if name == "copenhagen" else {656, 657, 658, 718})
        last = frames[max(frames)]
        evidence[last["path"]] = last["PNG_sha256"]
        pictures.append((f"{name.title()} / after leaving the dialogue", check.captured(last).convert("RGB")))
        path, sha = visual.make_sheet(ROOT / f"{name}_ordinary.png", pictures)
        sheets.append(dict(path=path, sha256=sha))
        results[name] = dict(case=case, panels=observations, entry=frames[entry], closing=last,
                             donor_sha256=report["battery_save_preloaded"]["source_sha256"])
        all_evidence.update(evidence)
    assert all(base.digest(path) == sha for path, sha in all_evidence.items())
    base.save(OUTPUT, dict(candidate_sha256=candidate, visits=results, evidence=all_evidence, sheets=sheets,
        ordinary_saved_gameplay=True, original_controller_and_touch=True, hardware=False, new_editorial_credit=0))
    print({name: [r["message_ID"] for r in result["panels"]] for name,result in results.items()},flush=True)


if __name__ == "__main__":
    verify()
