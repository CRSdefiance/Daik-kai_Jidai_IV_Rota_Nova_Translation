"""Compare complete observed voyage panels with clean source and native glyphs."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import observe_additional_voyages_20261123 as replay
from scripts import verify_current_shared_encounters_20261123 as prior
from scripts.preflight_shared_dynamic_notice_wrap_v1 import render as render_system, font_tools


base, current, ROOT = replay.base, replay.current, replay.ROOT
native, check, town, masks, visual = prior.native, prior.check, prior.town, prior.masks, prior.visual
OUTPUT = Path("translations/editorial_checkpoints/shared_display_20261123/additional_voyages_20261123.json")
REVIEWS = {
    85: "20261119_departure_numerals",
    86: "20261119_departure_numerals",
    297: "20261111_discovery_rewards",
    601: "20261122_ceuta_supply_alerts",
    1296: "20261111_sea_approach_village",
    2397: "20261119_sea_hazard_dialogue",
}
NOTES = {
    85: "The concise notice distinguishes an approximate range from a fixed deadline.",
    86: "The three rows distinguish date, weather and departure. The place name completes the last row.",
    297: "The separate system line names Crete after the lookout reports sighting a port.",
    601: "Keep the urgent warning and its food and water alternatives in the First Mate's voice.",
    1296: "Manuel's report preserves the port sighting and the Japanese address before the system names the place.",
    2397: "The groan and broken first syllable carry the cold reaction in Manuel's delivery.",
}
# Earlier route names identify the input schedule. The holds below identify the current outcomes.
HOLDS = {
    "tripoli_arrival": ((3920, 85, "", ("38",)), (4280, 86, "", ("9", "22", "Sky: Sunny", "Athens")),
        (7880, 1296, "Manuel Almeida", ()), (8120, 297, "", ("Crete",)),
        (9080, 601, "Charles Rochefort", ("food",)), (9320, 601, "Charles Rochefort", ("water",))),
    "ceuta_leg": ((3680, 85, "", ("38",)), (4040, 86, "", ("2", "18", "Sky: Sunny", "Ceuta")),
        (9080, 601, "Charles Rochefort", ("water",)), (9200, 601, "Charles Rochefort", ("food",))),
    "crew_conditions": ((7520, 2397, "Manuel Almeida", ()),),
}


def review_for(key, source, current_entry):
    package = Path(f"releases/all_routes_editorial_{REVIEWS[key]}_candidate")
    path = package / "verification/registered_review.json"
    assert base.digest(path) == base.load(package / "checksums.json")[path.relative_to(package).as_posix()]
    row, = [r for r in base.load(path)["records"] if r["id"] == f"COMMON_MESSAGE_{key}"]
    assert row["source_hex"] == source.text.hex()
    assert row["source_reference"] == town.reference(source) and all(row["review"].values())
    actual = current_entry.text.decode("ascii").strip()
    reviewed = row["english"].replace("{LB}", " ").removesuffix("{PAD}")
    assert actual.split() == reviewed.split(), (key, actual, reviewed)
    return row, dict(path=str(path), sha256=base.digest(path))


def system_plane(raster, arm, kanji, raw, picture):
    # These status notices use the separately verified renderer. The candidate
    # line may start at the ordinary inset or one ASCII cell farther in.
    matches = []
    actual = bytes(pixel == (0, 8, 0) for pixel in picture.crop((16, 296, 244, 344)).get_flattened_data())
    for candidate in (raw, b" " + raw) if not raw.startswith(b" ") else (raw,):
        pixels, _ = render_system(raster, arm, kanji, candidate)
        if bytes(pixel == 1 for pixel in pixels) == actual:
            matches.append((candidate, native.digest(bytes(pixels))))
    assert len(matches) == 1, (raw, len(matches))
    matched, = matches
    return matched


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert release["candidate_sha256"] == candidate and release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    ctx = town.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    clean, rom = base.NdsImage.open(native.CLEAN), ctx.image
    source = town.common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))
    installed = current.stage.observed.prior.shared.paired.prior.entries(rom)
    assert native.digest(ctx.arm) == release["target_ARM9_sha256"]
    assert native.digest(ctx.common) == release["target_COMMON_sha256"]
    renderer, _, _ = town.font_tools(rom)
    font = check.GameAsciiFont.from_arm9(ctx.arm)
    system = font_tools(rom)[0]
    kanji = rom.read_file("/GRP/KANJI.FNT")
    pending = {row["message_ID"] for row in base.load(current.REVIEW)["shared_consumer_binding"]["records"]}
    capture = FunctionType(prior.prior_captures.__code__, prior.prior_captures.__globals__ | dict(ROOT=ROOT))
    cases = {}
    for case, samples in HOLDS.items():
        report, trace, evidence = capture(case, replay.schedule, candidate)
        frames, observed, pictures = check.shots(report), [], []
        for frame, key, speaker, arguments in samples:
            recent = [row for row in trace if row["message_ID"] == key and 0 < frame - row["frame"] <= 220]
            latest = max(row["frame"] for row in recent)
            getter, copier = [row for row in recent if row["frame"] == latest]
            assert (getter["PC"], copier["PC"]) == (0x0205528C, 0x020534F4)
            assert dict(getter, PC=copier["PC"]) == copier
            jp, en = source[key], installed[key]
            assert en.text.count(b"%s") == len(arguments)
            history, history_reference = review_for(key, jp, en)
            image = check.captured(frames[frame]).convert("RGB")
            nameplate = None
            if speaker:
                data, lines = town.native_layout(cpu, en.text, key, arguments, parent=getter["caller_LR"] + 0x1C)
                plane, glyphs = town.render_portrait(renderer, ctx.arm, kanji, data)
                assert [g["code"] for g in glyphs] == town.glyph_codes(data)
                digest = native.digest(bytes(plane))
                if not masks.mask_check(bytes(plane), 228, image):
                    assert len(lines) == 1, (case, key, frame, lines)
                    # Short portrait alerts can keep an extra leading cell.
                    data, digest = system_plane(system, ctx.arm, kanji, lines[0].encode("ascii"), image)
                ink, bounds = check.complete_mask(font, speaker, image, 16, 277, (98, 97, 98))
                nameplate = dict(ink=ink, bounds=bounds)
            else:
                payload = en.text.rstrip(b" ") % tuple(value.encode("ascii") for value in arguments)
                data, digest = system_plane(system, ctx.arm, kanji, payload, image)
                lines = data.decode("ascii").splitlines()
            observed.append(dict(message_ID=key, source_reference=town.reference(jp),
                installed_reference=town.reference(en), source_hex=jp.text.hex(), installed_hex=en.text.hex(),
                clean_Japanese=jp.text.decode("cp932"), english=history["english"],
                observed_speaker=speaker or "System", arguments=arguments, observed_lines=lines, nameplate=nameplate,
                complete_glyph_plane_sha256=digest, localization_note=NOTES[key],
                context=history["context"], source_meaning=history["source_meaning"],
                decision="retention", review=history["review"], prior_review=history_reference,
                screenshot=frames[frame], requests=[getter, copier]))
            pictures.append((f"{speaker or 'System'} / COMMON {key} / {frame}", image))
        sheets = []
        for index in range(0, len(pictures), 4):
            path, digest = visual.make_sheet(OUTPUT.parent / f"{case}_voyage_{1+index//4}.png", pictures[index:index + 4])
            sheets.append(dict(path=path, sha256=digest))
        counts = Counter(row["message_ID"] for row in trace if row["PC"] == 0x0205528C)
        cases[case] = dict(ordinary_input_only_saved_gameplay=True, requests_by_id=dict(counts),
            pending_requests=sorted(pending & counts.keys()), holds=observed, sheets=sheets, evidence=evidence)
    assert all(not case["pending_requests"] for case in cases.values())
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        cases=cases, cases_used_for_context=3, exact_gameplay_holds=sum(len(case["holds"]) for case in cases.values()),
        distinct_reviewed_messages=len(REVIEWS), hardware=False, new_editorial_credit=0,
        scope="Input-only cold boots from exact existing saves. Historical trajectories were not asserted. The Athens replay visibly discovers Crete."))
    print("Verified eleven ordinary holds for six shared records, including the cold reaction and Crete discovery.")


if __name__ == "__main__":
    main()
