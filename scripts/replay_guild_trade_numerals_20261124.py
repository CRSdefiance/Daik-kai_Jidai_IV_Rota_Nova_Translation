"""Verify both ordinary Seoul sale decisions after the four Guild text changes."""

from argparse import ArgumentParser
from inspect import getsource

from PIL import ImageChops

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_london_guild_display_20261124 as replay_base
from scripts import stage_guild_trade_numerals_20261124 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import NdsImage, digest, read, reference, write


BEFORE = stage.play.ROOT / stage.play.CASE / "capture/capture_report.json"
REPLAY = stage.ROOT / "ordinary_replay"
AFTER = REPLAY / "capture_report.json"
OUT = stage.OUT.with_name("guild_trade_numerals_paired_20261124.json")
SHEET = OUT.with_name("seoul_guild_sale_paired_1_20261123.png")
CHANGED = {12400, 13600}
AMOUNT = 6160
RETAINS = {
    7200: (1071, ["Which one would you like?"], "The Guildmaster opens the purchase list with a brief selection question."),
    8000: (1073, ["Want to buy it for 7700 coins?"], "The already corrected buy question keeps the price and choice together."),
    9600: (1074, ["Thanks for your business!"], "The Guildmaster thanks Maria after the purchase is accepted."),
    11600: (1085, ["What would you like to sell?"], "The question states the action and leads to a list of eligible items."),
    14000: (1096, ["Thanks!"], "The casual close follows agreement and distinguishes payment from the preceding offer."),
}


def replay():
    source = checked_text(getsource(replay_base.replay), {'"_navigation.png"': '"_cold_boot.png"'})
    scope = vars(replay_base) | dict(stage=stage, BEFORE=BEFORE, REPLAY=REPLAY, __file__=__file__)
    exec(compile(source, __file__ + "::Seoul-Guild-replay", "exec"), scope)
    scope["replay"]()


def verify():
    panels = stage.panels
    before, after, preflight = map(read, (BEFORE, AFTER, stage.OUT))
    assert before["ROM_sha256"] == preflight["predecessor"]["sha256"]
    assert after["ROM_sha256"] == preflight["candidate"]["sha256"] == digest(stage.ROM)
    assert before["frames"] == after["frames"] == 15601
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule"):
        assert before[key] == after[key]
    for run in (before, after):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
        donor = run["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert before["battery_save_preloaded"]["source_sha256"] == after["battery_save_preloaded"]["source_sha256"]
    old, new = (panels.shots(run, "_cold_boot.png") for run in (before, after))
    assert set(old) == set(new) and CHANGED < set(new)
    unchanged = sorted(set(old) - CHANGED)
    assert all(old[frame]["framebuffer_sha256"] == new[frame]["framebuffer_sha256"] for frame in unchanged)

    rom = NdsImage.open(stage.ROM)
    arm, common = (rom.read_file(asset) for asset in (stage.ARM, stage.COMMON))
    font = GameAsciiFont.from_arm9(arm)
    revised, figures = [], []
    result = preflight["quote_cases"]["1086"][str(AMOUNT)]
    for frame in sorted(CHANGED):
        prior, target = (panels.picture(bank[frame]) for bank in (old, new))
        bbox = ImageChops.difference(prior, target).getbbox()
        assert bbox and 16 <= bbox[0] < bbox[2] <= 245 and 296 <= bbox[1] < bbox[3] < 360, (frame, bbox)
        ink = panels.exact_body(font, result["lines"], target)
        nameplate = panels.nameplate(font, "Guildmaster", target)
        revised.append(dict(frame=frame, message_ID=1086, amount=AMOUNT, lines=result["lines"], changed_box=bbox,
                            complete_body_ink=ink, nameplate=nameplate, previous=old[frame], installed=new[frame]))
        figures.extend(((f"{frame} / Before", prior), (f"{frame} / After", target)))
    sheets = panels.sheets_for("seoul_guild_sale_paired", figures)
    assert sheets == [reference(SHEET)]

    source = NdsImage.open(stage.CLEAN)
    clean = stage.london.common_message_entries(source.read_file(stage.COMMON), source.read_file(stage.ARM))
    current = stage.native.yard.common_rows(common, arm)
    trace_path = BEFORE.parent.parent / "requests.json"
    trace = read(trace_path)
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert [r["message_ID"] for r in trace["source_requests"] if r["message_ID"] in stage.PROSE] == [1086] * 4
    retentions = []
    for frame, (key, lines, reason) in RETAINS.items():
        getter, copier = [r for r in trace["source_requests"] if r["message_ID"] == key and 0 < frame - r["frame"] < 400]
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        args = (b"7700",) if key == 1073 else ()
        assert (current[key].text % args).decode("ascii").split() == " ".join(lines).split()
        screen = panels.picture(new[frame])
        retentions.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=stage.COMMON, speaker="Guildmaster", context=stage.CONTEXT,
            english=current[key].text.decode("ascii").strip(), clean_Japanese=clean[key].text.decode("cp932"),
            source_reference=stage.london.exact_row(clean[key]), current_reference=stage.london.exact_row(current[key]),
            staged_reference=stage.london.exact_row(current[key]), decision="retention", source_meaning=reason,
            localization_note=reason, review=dict.fromkeys(stage.GATES, True), capture=new[frame],
            complete_body_ink=panels.exact_body(font, lines, screen), nameplate=panels.nameplate(font, "Guildmaster", screen),
            requests=[getter, copier]))
    funds = [dict(frame=frame, **panels.find_mask(font, amount, panels.picture(new[frame]), (52, 344, 137, 367)))
             for frame, amount in ((3200, "38816"), (10800, "31116"), (11200, "31116"), (14400, "37276"), (15600, "37276"))]
    town = panels.find_mask(font, "Seoul", panels.picture(new[15600]), (10, 13, 123, 31))
    write(OUT, dict(candidate_sha256=after["ROM_sha256"], predecessor_sha256=before["ROM_sha256"], ordinary_gameplay=True,
                    revised=revised, unchanged_frames=unchanged, retentions=retentions, balances=funds,
                    return_to_town=town, sheets=sheets, ordinary_message_IDs=[1086], offline_conditionals=[1072, 1083, 1095],
                    evidence=list(map(reference, (BEFORE, AFTER, stage.OUT, trace_path))), new_editorial_credit=0, registered=False))
    print(f"Verified both revised Seoul sale holds and {len(unchanged)} unchanged surrounding frames in ordinary play.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    (replay if args.replay else verify)()
