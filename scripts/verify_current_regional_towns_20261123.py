"""Verify observed regional dialogue, the Seoul event, and the Tunis shop labels."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import bind_shared_display_after_hodram_20261123 as shared
from scripts import observe_current_regional_towns_20261123 as runs
from scripts import verify_ceuta_and_lisbon_20261122 as previous
from scripts.verify_tripoli_copenhagen_20261122 import captures as prior_captures


base, current, ROOT = runs.base, runs.current, runs.ROOT
native = current.native
check, masks, town, visual = previous.check, previous.masks, previous.town, previous.visual
OUT = shared.OUTPUT.parent / "regional_towns_current_20261123.json"
YIFA = Path("releases/all_routes_editorial_20261115_seoul_recruitment_candidate/verification/registered_review.json")
LABELS = {
    0: ("Charles Rochefort", (), "Charles reports a gathering without claiming to know its cause."),
    51: ("Barkeep", (), "The welcome leads directly to the choice to order a drink."),
    654: ("Shopkeeper", ("Whale Meat",), "The stock recommendation stays conditional and names the Market."),
    656: ("Shopkeeper", (), "The short answer explains that the shop sells at retail."),
    657: ("Shopkeeper", (), "The sailor's question tag fits with the question before the referral to the Market."),
    658: ("Shopkeeper", (), "The casual echo and modest report suit the answer about business."),
    714: ("Shopkeeper", (), "The two sentences preserve Valdes, Spain's navy and its reported name."),
    715: ("Shopkeeper", (), "The active verb preserves the company's past reach and the speaker's figurative comparison."),
    732: ("Shopkeeper", (), "The tentative forecast fits on one line without splitting a phrase."),
}


def observed_frame(frames, request):
    next_hold = min(frame for frame in frames if frame > request["frame"])
    assert next_hold - request["frame"] < 160 or (request["message_ID"] == 0 and next_hold == 3200)
    return frames[next_hold]


def compare_tunis(candidate_report, sheets):
    clean_report = ROOT / "tunis_clean/capture/capture_report.json"
    clean = base.load(clean_report)
    installed = base.load(candidate_report)
    assert clean["ROM_sha256"] == base.digest(native.CLEAN)
    assert clean["cold_boot"] and not clean["savestate_loaded"] and not clean["callback_errors"]
    assert clean["scripted_input_schedule"] == [row for row in installed["scripted_input_schedule"] if row["start"] < 5600]
    assert clean["battery_save_preloaded"]["source_sha256"] == installed["battery_save_preloaded"]["source_sha256"]
    left, right = [check.shots(report)[5150] for report in (clean, installed)]
    path, digest = visual.make_sheet(OUT.parent / "tunis_shop_labels_clean_current.png", [
        ("Clean Japanese / Tunis", check.captured(left).convert("RGB")),
        ("Latest candidate / Tunis", check.captured(right).convert("RGB")),
    ])
    sheets.append(dict(path=path, sha256=digest))
    return dict(clean=left, installed=right, clean_report_sha256=base.digest(clean_report),
        same_donor_and_input_prefix=True, three_identical_shop_categories_in_clean=True,
        observed_clean_label="珍味店", observed_installed_label="Delicacy Shop")


def observe_seoul(current_rom, clean_rom, frames, font, painter, sheets):
    row, = [r for r in base.load(YIFA)["records"] if r["id"] == "DK4_MES_B140_R0059"]
    path = row["file_path"]
    refs = []
    for image, name in ((clean_rom, "source_reference"), (current_rom, "registered_reference")):
        data = image.read_file(path)
        block = native.IlnkContainer.parse(data).blocks[140]
        ref = row[name]
        at = ref["offset"] - 5
        expected = bytes.fromhex(ref["complete_preamble_hex"]) + bytes.fromhex(ref["raw_hex"])[1:] + b"\0"
        assert block[at:at + len(expected)] == expected
        refs.append(ref | dict(archive_sha256=native.digest(data), block_sha256=native.digest(block)))
    assert all(row["review"].values())
    hold = frames[10350]
    picture = check.captured(hold).convert("RGB")
    page, = painter(row["english"])
    assert masks.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, picture)
    ink, bounds = check.complete_mask(font, row["speaker"], picture, 16, 277, (98, 97, 98))
    path, digest = visual.make_sheet(OUT.parent / "seoul_ordinary_recruitment_current.png", [
        ("Seoul / town entry", check.captured(frames[3720]).convert("RGB")),
        ("Seoul / Yifa recruitment", picture),
    ])
    sheets.append(dict(path=path, sha256=digest))
    return dict(id=row["id"], file_path=row["file_path"], source_reference=refs[0], installed_reference=refs[1],
        capture=hold, English=row["english"], speaker=row["speaker"], complete_native_body=True,
        nameplate=dict(ink=ink, bounds=bounds), earlier_full_exchange=dict(path=str(YIFA), sha256=base.digest(YIFA)))


def main():
    assert not OUT.exists()
    release, worklist = map(base.load, (current.RELEASE, shared.SOURCE))
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arm, common = [rom.read_file(path) for path in (town.ARM, town.COMMON)]
    assert native.digest(arm) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = check.common_message_entries(clean.read_file(town.COMMON), clean.read_file(town.ARM))
    installed = shared.paired.prior.entries(rom)
    ctx = town.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    renderer, _, _ = town.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    font = check.GameAsciiFont.from_arm9(arm)
    capture = FunctionType(prior_captures.__code__, prior_captures.__globals__ | dict(ROOT=ROOT))
    pending = {row["message_ID"] for row in worklist["records"]}
    results, sheets, cases = {}, [], Counter()
    for city in runs.regional.HISTORY:
        report, requests, evidence = capture(city, runs.regional.schedule, candidate)
        frames = check.shots(report)
        paired, pictures = [], [(city.title() + " / town entry", check.captured(frames[3720]).convert("RGB"))]
        for getter, copier in zip(requests[::2], requests[1::2], strict=True):
            assert (getter["PC"], copier["PC"]) == (0x0205528C, 0x020534F4)
            assert dict(getter, PC=copier["PC"]) == copier
            key = getter["message_ID"]
            role, args, note = LABELS[key]
            jp, en = source[key], installed[key]
            assert jp.text.count(b"%s") == en.text.count(b"%s") == len(args)
            hold = observed_frame(frames, getter)
            picture = check.captured(hold).convert("RGB")
            raw, lines = town.native_layout(cpu, en.text, key, args)
            pixels, glyphs = town.render_portrait(renderer, arm, kanji, raw)
            assert [g["code"] for g in glyphs] == town.glyph_codes(raw)
            assert masks.mask_check(bytes(pixels), 228, picture), (city, key, hold["frame"], lines)
            ink, bounds = check.complete_mask(font, role, picture, 16, 277, (98, 97, 98))
            evidence[hold["path"]] = hold["PNG_sha256"]
            paired.append(dict(message_ID=key, speaker=role, source_reference=check.reference(jp), installed_reference=check.reference(en),
                source_hex=jp.text.hex(), installed_hex=en.text.hex(), Japanese=jp.text.decode("cp932"),
                English=en.text.decode("ascii"), arguments=args, lines=lines, capture=hold,
                requests=(getter, copier), body_plane_sha256=native.digest(bytes(pixels)), nameplate=dict(ink=ink,bounds=bounds),
                decision="retention", localization_note=note, review=dict.fromkeys(town.GATES, True)))
            cases[key] += 1
            pictures.append((f"{city.title()} / {role} / COMMON {key}", picture))
        if paired:
            for i in range(0, len(pictures), 5):
                path, digest = visual.make_sheet(OUT.parent / f"{city}_ordinary_current_{1+i//5}.png", pictures[i:i+5])
                sheets.append(dict(path=path, sha256=digest))
        assert all(base.digest(file) == digest for file, digest in evidence.items())
        results[city] = dict(verified_common=paired, evidence=evidence,
            open_shared_hits=sorted(pending & {entry["message_ID"] for entry in requests}),
            donor_sha256=report["battery_save_preloaded"]["source_sha256"])
        if city == "seoul":
            painter = current.stage.scope["compiler"].display.clipped_renderer(ctx)
            def yifa_painter(line):
                plan = painter(arm, kanji, line.encode("ascii"))
                assert plan["complete_consumed_bytes"] == len(line)
                return plan["pages"]
            results[city]["event_hold"] = observe_seoul(rom, clean, frames, font, yifa_painter, sheets)
    assert set(cases) == LABELS.keys() and sum(cases.values()) == 19
    comparison = compare_tunis(ROOT / "tunis/capture/capture_report.json", sheets)
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        town_visits=results, common_holds=19, distinct_common_keys=dict(cases), clean_tunis_comparison=comparison,
        ordinary_battery_save_gameplay=True, hardware=False, new_editorial_credit=0, sheets=sheets))
    print(dict(cases))


if __name__ == "__main__":
    main()
