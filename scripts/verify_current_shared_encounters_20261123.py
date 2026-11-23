"""Bind Tavern and sailing holds to clean source and current executable display paths."""

from collections import Counter
from types import FunctionType

from scripts import observe_current_shared_encounters_20261123 as runs
from scripts import probe_tavern_conversations_v764 as tavern
from scripts import register_kurushima_surrender_20261122 as kurushima
from scripts import stage_voyage_rat_and_search_dialogue_20261115 as rat_search
from scripts import verify_current_regional_towns_20261123 as prior
from scripts.probe_sighting_layout_v1070 import native_layout as sighting_layout
from scripts.verify_tripoli_copenhagen_20261122 import captures as prior_captures


base, current, ROOT = runs.base, runs.current, runs.ROOT
native, check, masks, town, visual = current.native, prior.check, prior.masks, prior.town, prior.visual
OUT = prior.OUT.with_name("ordinary_shared_encounters_20261123.json")
SAMPLES = {
    "voyage": {
        4075: (408, "Manuel Almeida", (), "The first line warns of rats and the second explains the danger to food."),
        4535: (2221, "Manuel Almeida", (), "The return and tentative result remain two clear thoughts."),
        4735: (608, "Manuel Almeida", ("food",), "Food is the depleted resource and the alarm remains direct."),
        4955: (608, "Manuel Almeida", ("water",), "The same alarm keeps its separate water substitution."),
        6400: (609, "Sailor", (), "Dizziness, hunger and exhaustion escalate in the sailor's voice."),
        13400: (609, "Sailor", (), "The parallel exhaustion hold preserves the same three complaints."),
    },
    "osaka": {
        5200: (618, "Sailor", ("to the east", "Kurushima"), "The direction, fleet affiliation and alert remain clear and distinct."),
    },
    "tunis": {
        10350: (51, "Barkeep", (), "The invitation leads to the original drink menu."),
        11050: (53, "Barkeep", (), "The barkeep gives the exact charge before delivering a tip."),
        11450: (823, "Barkeep", ("Alexandria",), "The rumor names a town and says it is nearby. The live wrap breaks after 'It's'."),
        12250: (53, "Barkeep", (), "The second visit charges the same amount."),
        12650: (823, "Barkeep", ("Alexandria",), "The second hold confirms the same awkward break in the ordinary town hint."),
    },
    "syracuse": {
        10350: (51, "Barkeep", (), "The invitation leads to the original drink menu."),
        11050: (53, "Barkeep", (), "The barkeep gives the exact charge before the gossip."),
        11450: (821, "Barkeep", ("Pasha", "Istanbul", "soldier"), "The person, home town and role remain distinct in this informal influence report."),
        12250: (53, "Barkeep", (), "The second visit charges the same amount."),
        12650: (821, "Barkeep", ("Hayreddin", "Alexandria", "pirate"), "The next drink yields a different person, town and profession with the same natural phrasing."),
    },
}


def verify_encounter(rom, ctx, frames, font):
    review = base.load(kurushima.REVIEW)
    previous = base.load(kurushima.RELEASE)
    assert review["candidate_sha256"] == previous["candidate_sha256"] == base.digest(kurushima.ROM)
    archive = kurushima.stage.ARCHIVE
    block = native.IlnkContainer.parse(rom.read_file(archive)).blocks[3]
    earlier = base.NdsImage.open(kurushima.ROM)
    assert block == native.IlnkContainer.parse(earlier.read_file(archive)).blocks[3]
    formatter = kurushima.stage.renderer.inherited.early.prior.precedent.planners(ctx.arm)[1]
    kanji = rom.read_file("/GRP/KANJI.FNT")
    stored = base.load(kurushima.VERIFY / "stored_proof.json")
    commands = [cmd for cmd in stored["commands"] if cmd["record_ids"]]
    evidence, pictures = [], []
    for frame, row, cmd in zip(range(5360, 6761, 200), review["records"], commands, strict=True):
        assert cmd["record_ids"] == [row["id"]] and all(row["review"].values())
        at = cmd["stored_offset"]
        command = bytes.fromhex(cmd["stored"])
        assert block[at:at + len(command)] == command
        body = command[6:command.index(0, 6)].replace(b"FI", b"Maria")
        result = formatter(ctx.arm, kanji, body)
        page, = result["pages"]
        assert result["complete_consumed_bytes"] == len(body) and page["native_independent_plane_equal"]
        held = frames[frame]
        image = check.captured(held).convert("RGB")
        assert masks.mask_check(bytes.fromhex(page["native_plane_hex"]), 216, image), (row["id"], frame)
        ink, bounds = check.complete_mask(font, row["speaker"], image, 16, 277, (98, 97, 98))
        evidence.append(dict(id=row["id"], file_path=archive, block=3, capture=held,
            source_reference=row["source_reference"], installed_command_offset=at, installed_command_hex=command.hex(),
            complete_mask=True, speaker=row["speaker"], nameplate=dict(ink=ink, bounds=bounds)))
        pictures.append(("Nagasaki / " + row["id"], image))
    return evidence, pictures


def check_holds(case, ctx, frames, requests, js, en, cpu, renderer, kanji, font, shore_search_group):
    results, pictures = [], []
    for frame, (key, role, args, reason) in SAMPLES[case].items():
        selected = [r for r in requests if r["message_ID"] == key and 0 < frame - r["frame"] <= 220]
        a, b = selected
        assert (a["PC"], b["PC"]) == (0x0205528C, 0x020534F4) and dict(a, PC=b["PC"]) == b
        source, installed = js[key], en[key]
        assert source.text.count(b"%s") == installed.text.count(b"%s") == len(args)
        if key in (821, 823):
            formatted = tavern.format_case(cpu, dict(message_id=key, english=installed.text.decode("ascii").strip()),
                                           tuple(arg.encode("ascii") for arg in args))
            lines, data = formatted["lines"], bytes.fromhex(formatted["formatted_hex"])
        elif key == 2221:
            layout = rat_search.portrait_case(ctx, dict(message_ID=key), shore_search_group, installed.text, 23)
            data = layout["display"]
            lines = [line.strip().decode("ascii") for line in data.split(b"\n")]
        elif key == 618:
            data, lines = sighting_layout(cpu, installed.text, key, *(arg.encode("ascii") for arg in args))
        else:
            data, lines = town.native_layout(cpu, installed.text, key, args, parent=a["caller_LR"] + 0x1C)
        plane, glyphs = town.render_portrait(renderer, ctx.arm, kanji, data)
        assert [g["code"] for g in glyphs] == town.glyph_codes(data)
        held = frames[frame]
        image = check.captured(held).convert("RGB")
        if key == 608:
            body_positions = check.body_mask(image, font, lines)
            assert not any(pixel == (0, 8, 0) for pixel in image.crop((16, 344, 244, 360)).get_flattened_data())
        else:
            assert masks.mask_check(bytes(plane), 228, image), (case, key, frame, lines)
            body_positions = None
        ink, bounds = check.complete_mask(font, role, image, 16, 277, (98, 97, 98))
        result = dict(message_ID=key, speaker=role, source_reference=check.reference(source),
            installed_reference=check.reference(installed), source_hex=source.text.hex(), installed_hex=installed.text.hex(),
            Japanese=source.text.decode("cp932"), English=installed.text.decode("ascii"), arguments=args,
            lines=lines, capture=held, original_requests=selected, native_plane_sha256=native.digest(bytes(plane)),
            nameplate=dict(ink=ink, bounds=bounds), measured_body_rows=body_positions, localization_note=reason)
        if key == 823:
            assert any(line.endswith("It's") for line in lines[:-1])
            result.update(decision="wrap follow-up")
        else:
            result.update(decision="retention", review=dict.fromkeys(town.GATES, True))
        results.append(result)
        pictures.append((f"{case.title()} / {role} / COMMON {key}", image))
    return results, pictures


def main():
    assert not OUT.exists()
    release = base.load(current.RELEASE)
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    js = check.common_message_entries(clean.read_file(town.COMMON), clean.read_file(town.ARM))
    en = prior.shared.paired.prior.entries(rom)
    ctx = town.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    _, shore_search_group = rat_search.original_groups(clean.read_file(town.ARM), ctx.arm)
    assert native.digest(ctx.arm) == release["target_ARM9_sha256"] and native.digest(ctx.common) == release["target_COMMON_sha256"]
    renderer, _, _ = town.font_tools(rom)
    kanji, font = rom.read_file("/GRP/KANJI.FNT"), check.GameAsciiFont.from_arm9(ctx.arm)
    capture = FunctionType(prior_captures.__code__, prior_captures.__globals__ | dict(ROOT=ROOT))
    shared = base.load(current.REVIEW)["shared_consumer_binding"]["records"]
    pending = {row["message_ID"] for row in shared}
    all_cases, sheets = {}, []
    for case in SAMPLES:
        report, requests, evidence = capture(case, runs.schedule, candidate)
        frames = check.shots(report)
        holds, images = check_holds(case, ctx, frames, requests, js, en, cpu, renderer, kanji, font, shore_search_group)
        cases = dict(common_holds=holds, all_getter_counts=dict(Counter(x["message_ID"] for x in requests if x["PC"] == 0x0205528C)),
            open_shared_hits=sorted(pending & {x["message_ID"] for x in requests}), evidence=evidence)
        if case == "osaka":
            extra, pictures = verify_encounter(rom, ctx, frames, font)
            cases["ordinary_Nagasaki_Kurushima_encounter"] = extra
            images.extend(pictures)
        for i in range(0, len(images), 5):
            path, digest = visual.make_sheet(OUT.parent / f"{case}_shared_encounters_{1+i//5}.png", images[i:i+5])
            sheets.append(dict(path=path, sha256=digest))
        all_cases[case] = cases
    held = sum(len(case["common_holds"]) for case in all_cases.values())
    assert held == 17 and all(not case["open_shared_hits"] for case in all_cases.values())
    base.save(OUT, dict(candidate_sha256=candidate, cases=all_cases,
        common_holds=held, story_holds=8, ordinary_battery_save_gameplay=True,
        natural_encounters_observed=True, unvisited_variants="Other Tavern rumors, disease, storms, dolphins and sea outcomes.",
        unresolved_actual_wraps=[823], hardware=False, new_editorial_credit=0, sheets=sheets))
    print("Verified 17 ordinary shared holds, eight Kurushima panels and one repeatable Tavern wrap issue.")


if __name__ == "__main__":
    main()
