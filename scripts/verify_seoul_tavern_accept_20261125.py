"""Bind the ordinary Seoul Tavern choices and rumor to exact source records."""

from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_seoul_tavern_accept_20261125 as play
from scripts import verify_riga_trade_deck_20261124 as review
from scripts import verify_seoul_tavern_decline_20261123 as previous
from scripts.stage_azores_wording_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = review.OUT.with_name("seoul_tavern_accept_current_20261125.json")
PANELS = review.panels
HOLDS = {
    59: ((15130, 17410), "Reika", (), ("How about one more drink?",),
         "Reika invites Maria to have another glass.",
         "The friendly offer gives Maria a simple choice and keeps the invitation light."),
    61: ((15350,), "Barkeep", (), ("Ten coins.",),
         "The barkeep sets the price at ten gold coins.",
         "The brisk price quote fits the barkeep and matches the next deduction."),
    991: ((15560,), "Reika", (), ("Are you rich? I'm jealous! I hope I", "find someone nice soon. I want",
                                  "to be happy, too."),
          "Reika wonders if Maria is wealthy, envies her, and longs to meet someone nice and be happy soon.",
          "The current wrap splits both expressions of hope. A revised paragraph should keep her teasing envy and genuine wish together."),
    855: ((16360, 18460), "Sailor", ("196",), ("Looks like it'll cost 196 gold.", "Okay with you?"),
          "The sailor estimates the cost of the round and checks that the captain agrees.",
          "The wording makes the price an estimate and gives the full question its own line."),
    53: ((16780,), "Barkeep", (), ("5 coins.",),
         "The barkeep charges five gold coins.",
         "The clipped price fits his brief replies and matches the actual charge."),
    55: ((16990,), "Barkeep", ("Reika",), ("Hey, Reika! We've got a customer!",),
         "The barkeep calls Reika over for a customer.",
         "The familiar call sounds natural across a busy Tavern and names the person who responds."),
    57: ((17200,), "Reika", (), ("Welcome!",),
         "Reika welcomes the guest.",
         "The warm greeting follows her summons without adding recognition or a relationship."),
    826: ((17620,), "Reika", (), ("Oh, can't handle another drink?",),
          "Reika is surprised that Maria turns down another drink and lightly teases her tolerance.",
          "The teasing question fits the refusal and preserves the mild surprise."),
    867: ((18670,), "Maria Li", (), ("Barkeep, serve everyone", "a drink, please."),
          "Maria politely asks the barkeep to give everyone a drink.",
          "The direct request and final please preserve Maria's settled, courteous delivery."),
    872: ((18880,), "Barkeep", ("Li",), ("This round's on Li. Enjoy!",),
          "The barkeep tells the room who is treating them and invites them to enjoy it.",
          "The familiar announcement uses the established surname substitution and keeps the toast together."),
    874: ((19090,), "Patron", (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
          "The patron reacts with delighted disbelief, thanks Maria, and praises her generosity.",
          "The surprise and colloquial thanks earn the informality of the following tip."),
    870: ((19300,), "Patron", ("Ma'am", "Pink Apron", "East Asia"),
          ("Ma'am, a tip about a rare treasure.", "They say Pink Apron is stashed", "in East Asia."),
          "The patron addresses Maria and passes along hearsay about the hiding place of a rare treasure.",
          "Ma'am fits the respectful approach, and They say preserves uncertainty while keeping the item and region clear."),
}
BALANCES = {15130: 38781, 15350: 38781, 15560: 38771, 15770: 38771, 16360: 38771, 16570: 38771,
            16780: 38771, 17830: 38766, 18460: 38766, 18670: 38766, 18880: 38766, 19510: 38570, 19720: 38570}


def sheet(screens, frames, suffix):
    image = Image.new("RGB", (804, 222 * ((len(frames) + 2) // 3)), "#263238")
    paint = ImageDraw.Draw(image)
    for index, (frame, label) in enumerate(frames):
        x, y = 6 + index % 3 * 268, index // 3 * 222
        paint.text((x, y + 6), f"{frame}  {label}", fill="white")
        image.paste(screens[frame].crop((0, 192, 256, 384)), (x, y + 23))
    path = OUT.with_name(f"seoul_tavern_accept_{suffix}_20261125.png")
    image.save(path)
    return reference(path)


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    scope = vars(PANELS) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(PANELS.capture.__code__, scope)(play.ROOT.name, release)
    run, nav = (read(refs[key]["path"]) for key in ("capture", "journal"))
    earlier = read(play.HISTORY)
    prefix = earlier["scripted_input_schedule"]
    assert run["scripted_input_schedule"][:len(prefix)] == prefix
    assert nav["commands_received"][0]["command"] == play.OPENING
    assert refs["donor"] == read(play.DECLINE)["donor"]
    start, stop = play.FIRST_PAUSE, max(frames)
    assert stop == 19720
    original_frame = previous.frame_map(earlier)[start]
    screens = {frame: previous.captured(item) for frame, item in frames.items()}
    assert screens[start].tobytes() == previous.captured(original_frame).tobytes()
    assert screens[16360].tobytes() == screens[18460].tobytes()

    clean, current = (NdsImage.open(p) for p in (CLEAN, play.current.ROM))
    arm = current.read_file(play.current.ARM)
    archive = current.read_file(play.current.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(play.current.COMMON), clean.read_file(play.current.ARM))
    installed = common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    snapshots = {row["frame"]: row for row in run["read_only_pause_RAM_snapshots"]}
    for frame, amount in BALANCES.items():
        assert previous.cash_state(arm, snapshots[frame]) == (3, 3, amount)

    records, verified_calls, dialogue = [], [], []
    for key, (holds, speaker, args, lines, meaning, note) in HOLDS.items():
        ja, en = source[key], installed[key]
        text = " ".join(en.text.decode("ascii").split())
        assert text.count("%s") == len(args) and ja.text.count(b"%s") == len(args) + (key == 872)
        assert " ".join(lines) == text % args
        observations = []
        for frame in holds:
            raw = previous.read_ram(snapshots[frame])
            live = previous.text_at(raw, unpack_from("<I", raw, 0x54450)[0]).decode("ascii")
            assert " ".join(live.split()) == " ".join(lines), (key, frame, live)
            getter, copier = [row for row in calls if row["message_ID"] == key and 0 < frame - row["frame"] < 210]
            assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
            verified_calls.extend((getter, copier))
            observations.append(dict(frame=frames[frame], arguments=args, lines=lines, native_requests=[getter, copier],
                complete_body=PANELS.exact_body(font, lines, screens[frame]),
                complete_nameplate=PANELS.nameplate(font, speaker, screens[frame])))
            dialogue.append((frame, f"COMMON {key} / {speaker}"))
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON,
            speaker=speaker, clean_Japanese=ja.text.decode("cp932"), english=text, source_meaning=meaning,
            localization_note=note, decision="revision_needed" if key == 991 else "retention",
            source_reference=review.source_ref(ja), current_reference=review.source_ref(en),
            installed_reference=review.source_ref(en), observations=observations,
            review=dict.fromkeys(GATES, True) | {"formatting": key != 991}))
    assert sorted((row["frame"], row["PC"]) for row in verified_calls if row["frame"] > start) == sorted(
        (row["frame"], row["PC"]) for row in calls if row["frame"] > start)
    transitions = ((15770, "Return after Yes"), (16570, "Return after round declined"),
                   (17830, "Return after drink declined"), (19510, "Round settled"),
                   (19720, "Seoul town return"))
    sheets = [sheet(screens, sorted(dialogue)[:7], "dialogue_1"),
              sheet(screens, sorted(dialogue)[7:], "dialogue_2"), sheet(screens, transitions, "transitions")]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, evidence=refs,
        previous_decline=reference(play.DECLINE), exact_previous_invitation_frame=True,
        context="Ordinary Seoul controls reach both second-drink choices, both round choices and a treasure rumor.",
        records=records, finance=dict(second_drink_charged=10, first_drink_charged=5, round_estimate=196, round_paid=196,
                                     verified_balances=BALANCES),
        choice_frames={n: frames[n] for n in (15130, 16360, 17410, 18460)},
        transitions={n: frames[n] for n, _ in transitions}, sheets=sheets,
        remaining="Other Reika responses and other rumor variants were not sampled. COMMON 991 needs a verified reflow.",
        new_editorial_credit=0, ROM_changed=False))
    print(f"Verified {len(dialogue)} Seoul holds across {len(records)} COMMON records and the observed gold balances.")


if __name__ == "__main__":
    main()
