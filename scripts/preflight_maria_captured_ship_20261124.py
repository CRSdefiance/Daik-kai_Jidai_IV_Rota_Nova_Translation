"""Review the Nagasaki voyage and preserve the captured ship name on one line."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_nagasaki_voyage_20261124 as played
from scripts import stage_square_trend_dialogue_20261115 as trend
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts import verify_ezo_voyage_20261123 as prior_story
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


OUT = panels.OUT.with_name("maria_captured_ship_preflight_20261124.json")
KEY, END, RESULT_FRAME = 2086, 21300, 20300
TABLE = 0x02117B00
PROPOSAL = "We took %s from the enemy!"
HISTORY = Path("work/analysis/ship_name_bound_v1335b/original_ship_rename_capacity.json")
STORY = Path("releases/all_routes_editorial_20261123_kurushima_confrontation_wraps_candidate/verification/registered_review.json")
STORY_FRAMES = (13900, 14700, 15100, 15500, 15900, 16300, 16700, 17100)
HOLDS = {
    7200: (815, "Port Worker", (), ("You have no cargo.",),
           "The port worker observes that the fleet has no freight.",
           "The operator selected Cargo Setup with empty holds. The direct reply explains why the editor does not open."),
    8000: (85, "System", ("26",), ("Sailing days left: about 26.",),
           "The provisions permit about the displayed number of days at sea.",
           "About preserves the estimate before the departure-mode choice."),
    10400: (641, "Sailor", (), ("No route to that port.",),
            "The sailor says their port has no connected sailing route to the destination.",
            "The terse line suits this sailor's voice and explains the map refusal for Osaka."),
    13200: (86, "System", ("3", "12", "Sky: Sunny", "Nagasaki"), ("3/12", "Sky: Sunny", "Departed Nagasaki."),
            "The log lists the date, weather and port just departed.",
            "The three unchanged rows separate the original facts and preserve all four substitutions."),
    13600: (618, "Sailor", ("to the east", "Kurushima"),
            ("We've got company to the east!", "They're with Kurushima! Get ready", "for a fight!"),
            "The lookout identifies the bearing and faction of a fleet and calls the crew to prepare for battle.",
            "The familiar idiom and urgent final command suit the sailor. The fleet name stays intact and the final phrase occupies one line."),
    RESULT_FRAME: (KEY, "Sailor", ("War Ironclad",), ("We took the enemy ship War", "Ironclad!"),
            "The sailor exclaims that their side took the named enemy ship.",
            "Keep the sailor's blunt took and the capture from the enemy. Move the ship name before the longer phrase so it can stay together."),
    20700: (2011, "Sailor", (), ("We've defeated the enemy flagship's", "entire crew and captured the ship!"),
          "The sailor reports defeating the enemy flagship's entire crew and capturing the ship.",
          "The later notice states why the flagship was captured and keeps the crew and ship outcomes distinct."),
}


def observed_dialogue(source, current, installed, frames, calls, screens, font):
    records, holds = [], []
    for frame, (key, speaker, args, lines, meaning, note) in HOLDS.items():
        got, copied = [row for row in calls if row["message_ID"] == key and 0 < frame - row["frame"] <= 400]
        assert got["PC"] == 0x0205528C and copied == got | {"PC": 0x020534F4}
        ja, before, after = source[key], current[key], installed[key]
        assert ja.text.count(b"%s") == before.text.count(b"%s") == after.text.count(b"%s") == len(args)
        assert (before.text.decode("ascii") % args).split() == " ".join(lines).split()
        make_ref = lambda row: panels.text_reference(row) | dict(exact_hex=row.text.hex())
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=trend.COMMON, speaker=speaker,
            Japanese=ja.text.decode("cp932"), english=" ".join(after.text.decode("ascii").split()),
            source_reference=make_ref(ja), current_reference=make_ref(before),
            proposed_reference=panels.text_reference(after), source_hex=ja.text.hex(), current_hex=before.text.hex(),
            proposed_hex=after.text.hex(), source_meaning=meaning,
            context="Ordinary Nagasaki departure, the Kurushima encounter, and the named prize from the boarding duel.",
            localization_note=note, decision="revision" if key == KEY else "retention", review=dict.fromkeys(GATES, True)))
        holds.append(dict(frame=frame, message_ID=key, speaker=speaker, arguments=args, lines=lines, capture=frames[frame],
            ink=panels.exact_body(font, lines, screens[frame]),
            nameplate=panels.nameplate(font, "" if speaker == "System" else speaker, screens[frame]), requests=[got, copied]))
    assert next(row for row in holds if row["message_ID"] == KEY)["requests"][0]["caller_LR"] == 0x02053F24
    return records, holds


def layouts(runtime, revised, original, proposed):
    cpu, get, _ = machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    root = get(0xCB184)
    actor = next(root + 4 + n * 32 for n in range(207) if get(0x53F4C, root + 4 + n * 32, TABLE) == KEY)
    assert get(0x53F4C, actor, TABLE) == KEY
    assert read(HISTORY)["max_name_bytes_excluding_NUL"] == 18
    samples = ("War Ironclad", "Hanse Cog", "The Southern Cross", "This Ship Is Ours", "FALCON", "ICARUS",
               "FIFOFOFU", "Santa Maria", "F's Hope", "長崎丸" * 3, "ＦＡＬＣＯＮ")
    names = [b"F" + b"A" * n for n in range(18)] + [name.encode("cp932") for name in samples]
    assert len(names) == len(set(names)) and all(1 <= len(name) <= 18 for name in names)
    painter, _, _ = trend.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    cases, figures = [], []
    def test(label, archive, template, name):
        native = consumer(runtime.arm, archive, runtime.raw, runtime.plan, 0x53F0C, actor, TABLE, name)
        expected = template.replace(b"%s", name)
        raw = bytes.fromhex(native["formatted_hex"])
        assert native["input_hex"] == expected.hex() and b" ".join(raw.split()) == expected
        assert native["parent"] == 0x02053F40 and native["selector"] == TABLE and native["file_reads"]
        lines = [line.strip() for line in raw.split(b"\n")]
        assert 1 <= len(lines) <= 4 and all(0 < len(line) <= 38 for line in lines)
        plane, events = trend.render_portrait(painter, runtime.arm, kanji, raw)
        assert len(plane) == 228 * 64 and (events[0]["code"], events[-1]["code"]) == (ord("W"), ord("!"))
        complete = any(name in line for line in lines)
        assert complete == (label == "Proposed")
        name_text = name.decode("cp932")
        cases.append(dict(label=label, name=name_text, name_hex=name.hex(), layout=dict(lines=[line.decode("cp932") for line in lines],
            formatted_hex=raw.hex(), complete_runtime_name_on_one_line=complete), font_sha256=trend.digest(plane), native=native))
        figures.append((label + " / " + name.hex(), plane))
    test("Current", runtime.common, original, b"War Ironclad")
    assert cases[0]["layout"]["lines"] == list(HOLDS[RESULT_FRAME][3])
    for name in names:
        test("Proposed", revised, proposed, name)
    assert next(row for row in cases[1:] if row["name"] == "War Ironclad")["layout"]["lines"] == [
        "We took War Ironclad", "from the enemy!"]
    return cases, figures, actor


def main():
    release = read(played.prior.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    capture = FunctionType(panels.capture.__code__, vars(panels) | dict(observed=SimpleNamespace(ROOT=played.ROOT.parent)))
    frames, calls, evidence = capture(played.ROOT.name, release)
    assert max(frames) == END
    assert {284, 318, 750, 751, 752}.isdisjoint(row["message_ID"] for row in calls)
    runtime = trend.RegisteredRuntime(played.prior.RELEASE, release["own_registered_startup"], captain=3)
    assert trend.digest(runtime.arm) == release["target_ARM9_sha256"]
    clean = NdsImage.open(CLEAN)
    source = trend.common_message_entries(clean.read_file(trend.COMMON), clean.read_file(trend.ARM))
    current = trend.owned_entries(runtime.common, runtime.arm, trend.digest(runtime.arm[trend.DIRECTORY_OFFSET:trend.TABLE_OFFSET]))
    old = current[KEY].text
    assert old == b"We took the enemy ship %s!" and len(old) == len(PROPOSAL.encode("ascii"))
    assert source[KEY].text.decode("cp932") == "敵艦%sを\n奪ったぜ！"
    proposed = PROPOSAL.encode("ascii")
    revised, installed, allocation = trend.owned_deployment(runtime.common, runtime.arm, current, {KEY: proposed})
    font = GameAsciiFont.from_arm9(runtime.arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    records, holds = observed_dialogue(source, current, installed, frames, calls, screens, font)
    lineage = SimpleNamespace(RELEASE=STORY.with_name("registered_release_verification.json"), REVIEW=STORY)
    prove_story = FunctionType(prior_story.confrontation.__code__, vars(prior_story) | dict(earlier=lineage, STORY_FRAMES=STORY_FRAMES))
    story, story_figures = prove_story(clean, runtime.image, release, font, frames)
    cases, figures, actor = layouts(runtime, revised, old, proposed)
    root = OUT.with_suffix("")
    root.mkdir(parents=True, exist_ok=True)
    sheets = trend.portrait_sheets(root, figures)
    sheet = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=OUT), argdefs=panels.sheets_for.__defaults__)
    controls = sheet("maria_nagasaki_voyage", [(f"COMMON {row['message_ID']}", screens[row["frame"]]) for row in holds])
    controls += sheet("maria_kurushima_voyage", story_figures)
    data = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=records, candidate_sha256=release["candidate_sha256"],
        source_sha256=release["clean_input_sha256"], unchanged_ARM9_sha256=trend.digest(runtime.arm),
        proposed_COMMON_sha256=trend.digest(revised), allocation=allocation[KEY], native_cases=cases, proposed_sheets=sheets,
        ordinary_gameplay=dict(holds=holds, prior_story=story, evidence=evidence, requests=calls,
            offline_actor=hex(actor), called_duel_barks=[row for row in calls[::2] if 1931 <= row["message_ID"] <= 1960],
            duel_frames=[frames[f] for f in (19100, 19500, 19900)], osaka_docking=False,
            donor_provenance=reference("docs/nagasaki_shiraki_v518_checkpoint.md"), sheets=controls),
        current_ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(data)
    write(OUT, data)
    print(f"Verified {len(holds)} shared pages, {len(story)} story pages, and {len(cases) - 1} proposed name cases.")


if __name__ == "__main__":
    main()
