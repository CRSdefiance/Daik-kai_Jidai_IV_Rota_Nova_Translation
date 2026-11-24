"""Verify ordinary refit, Purser assignment, bargaining and the roster crop lead."""

from inspect import getsource
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.roster_role_crop import DESCRIPTOR
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_ordinary_lisbon_purser_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts import verify_nagasaki_shipyard_20261124 as shipyard
from scripts.record_navigation_v327 import dark_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, digest, read, reference, sha256, write
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact
from scripts.verify_personal_gameplay_v841 import get_machine


OUT = panels.OUT.with_name("lisbon_ordinary_purser_20261124.json")
ARM, COMMON = play.current.ARM, play.current.COMMON
SQUARE, YARD, MARKET = "Lisbon Square", "Lisbon Yard", "Lisbon Market"
HOLDS = {
    18100: (136, SQUARE, "", (), ("Choose a shop sign to ask about", "trends and other local news."),
            "Select a retail sign to hear about trends and other information.",
            "The instruction gives the exact action and explains what the player can learn."),
    19100: (657, SQUARE, "Shopkeeper", (), ("You're a sailor, aren't you?", "Try the Market for bulk trade."),
            "The shopkeeper recognizes a sailor and points them to the Market for wholesale.",
            "The short question tag stays intact and the response points to the actual Market."),
    19900: (656, SQUARE, "Shopkeeper", (), ("We only sell retail.",),
            "This shop sells only at retail.", "The brisk reply explains why the shop offers information instead of a cargo sale."),
    20600: (658, SQUARE, "Shopkeeper", (), ("Business? Oh, it's been all right.", "I'm hoping a good deal comes along."),
            "The shopkeeper says business is satisfactory and hopes for a valuable opportunity.",
            "The hesitation and modest optimism give the shopkeeper a distinct voice."),
    21300: (656, SQUARE, "Shopkeeper", (), ("We only sell retail.",),
            "This shop sells only at retail.", "The same short reply fits another retailer in the shared shop pool."),
    23700: (1266, YARD, "Shipwright", (), ("Which ship would you like to refit?",),
            "The shipwright asks the player to choose a ship for refitting.",
            "The whole question fits one line and leads into the original ship list."),
    27600: (1267, YARD, "Shipwright", ("2 days",), ("The refit will take 2 days.",),
            "The shipwright states the time for the accepted refit.",
            "The line keeps the game-supplied two-day duration and confirms the accepted job."),
    33700: (8, MARKET, "Trader", (), ("Need help?",),
            "The trader asks what the visitor needs.", "The brief greeting gives the player the floor."),
    36100: (15, MARKET, "Julio Erneco", (), ("Will this do?",),
            "Julio politely asks the captain to approve the deal.",
            "The concise, courteous question gives both answers room."),
    36500: (24, MARKET, "Julio Erneco", (), ("Sorry to trouble you, but could you", "do a bit better?"),
            "Julio apologetically requests slightly better terms.",
            "The deferential request fits his voice and keeps the modest size of the favor."),
    36900: (10, MARKET, "Trader", (), ("All right. I'll cut you a break.",),
            "The trader agrees to give the buyer a concession.",
            "The friendly concession answers Julio's request plainly and precedes settlement."),
}
REFIT_HOLDS = {
    24500: (1285, "The wind advantage and the square-sail mounting restriction remain distinct."),
    24800: (1247, "The Cabin help names both health and morale as benefits for officers."),
    25100: (1249, "The doctor's help applies both to officers and to sailors."),
    25280: (1250, "The chief cook conserves both supplies and slows crew fatigue. Keep food and water together in the next layout."),
    25460: (1251, "The Lounge distinguishes recovery of morale and slower fatigue."),
    25640: (1252, "The animal keeper's benefit is longer-lasting food supplies."),
    25820: (1253, "The Chapel help carries both the morale effect and the Square action."),
    26000: (1254, "The Tactics help names the strategist, schemes, and the Tavern."),
    26180: (1255, "The help explains both Purser functions and the replay demonstrates bargaining."),
}


def request(trace, frame, key):
    nearby = [row for row in trace if row["PC"] == 0x0205528C and row["message_ID"] == key and 0 < frame - row["frame"] <= 900]
    event = nearby[-1]
    assert event | {"PC": 0x020534F4} in trace
    return event


def record(ja, en, key, english, reason, meaning, scene, speaker, **proof):
    return dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, clean_Japanese=ja.text.decode("cp932"),
        source_reference=panels.text_reference(ja) | dict(exact_hex=ja.text.hex()),
        current_reference=panels.text_reference(en) | dict(exact_hex=en.text.hex()),
        installed_reference=panels.text_reference(en) | dict(exact_hex=en.text.hex()),
        speaker=speaker or "System", english=english, source_meaning=meaning, message_ID=key,
        localization_note=reason, context=scene, review=dict.fromkeys(GATES, True), decision="retention", **proof)


def dialogue(source, installed, frames, trace, font):
    rows = {}
    for frame, (key, scene, speaker, args, lines, gloss, reason) in HOLDS.items():
        ja, en = source[key], installed[key]
        english = " ".join(en.text.decode("ascii").split())
        assert english % args == " ".join(lines), (key, english, args)
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(args)
        screen = panels.picture(frames[frame])
        hold = dict(frame=frame, capture=frames[frame], request=request(trace, frame, key),
                    lines=lines, ink=panels.exact_body(font, lines, screen), nameplate=panels.nameplate(font, speaker, screen))
        if key not in rows:
            rows[key] = record(ja, en, key, english, reason, gloss, scene, speaker, holds=[])
        rows[key]["holds"].append(hold)
    return list(rows.values())


def refit(source, installed, frames, trace, font):
    path = panels.Path("releases/all_routes_editorial_20261115_refit_help_wraps_candidate/verification/registered_review.json")
    earlier = {r["message_id"]: r for r in read(path)["records"]}
    rows = []
    for frame, (key, note) in REFIT_HOLDS.items():
        ja, en = source[key], installed[key]
        old = earlier[key]
        assert ja.text.hex() == old["exact_clean_hex"]
        lines, ink = shipyard.exact_refit(font, en.text.rstrip(), panels.picture(frames[frame]))
        row = record(ja, en, key, " ".join(en.text.decode("ascii").split()), note, old["source_meaning"],
            "Rafael inspects each room and its crew effect before choosing a Purser.", "", lines=lines,
            ink=ink, capture=frames[frame], request=request(trace, frame, key))
        if key == 1250:
            row["decision"] = "prose retention, wrap follow-up"
            row["review"]["formatting"] = False
        rows.append(row)
    return rows


def deck(source, installed, clean, arm, frames, trace, font):
    key, frame = 1464, 32000
    en, ja = installed[key], source[key]
    english = "What's selling well now?"
    assert en.text.decode("ascii").strip() == english
    screen = panels.picture(frames[frame])
    row = record(ja, en, key, english, "Julio's quick question sounds natural as he takes up his new buying and selling duties.",
        "The newly assigned purser asks what goods are selling well now.",
        "Julio is placed in the Purser room and comments on the market.", "Julio Erneco",
        capture=frames[frame], request=request(trace, frame, key),
        complete_body=dark_text(font, english, screen, (6, 105, 250, 131)))
    loc = panels.Path("translations/deck_view_arm9_v2.json")
    config = read(loc)
    item, = [r for r in config["records"] if r["id"] == "DK4_DECK_CONFIRM_ASSIGNMENT_V2"]
    start = item["offset"]
    original = bytes.fromhex(item["source_hex"])
    assert clean[start:start + len(original)] == original
    text = item["english"]
    raw = arm[start:start + len(original)]
    assert raw.split(bytes(1))[0].decode("ascii") == text
    ref = dict(file_path=ARM, ARM9_file_offset=start, exact_hex=raw.hex())
    return [row, dict(id=item["id"], file_path=ARM, speaker="System", english=text,
        source_reference=ref | dict(exact_hex=original.hex()), current_reference=ref, installed_reference=ref,
        clean_Japanese=original.rstrip(bytes(1)).decode("cp932"),
        source_meaning="Ask the player to confirm the current assignments.", context=item["context"],
        localization_note="The concise question applies to all pending changes and leaves both answers open.",
        review=dict.fromkeys(GATES, True), decision="retention", capture=frames[32400],
        complete_body=dark_text(font, text, panels.picture(frames[32400]), (5, 290, 248, 326)))]


def roster(font, clean, arm, frames):
    shot = frames[30800]
    screen = panels.picture(shot)
    profile = panels.find_mask(font, "Finance 115", screen, (72, 126, 174, 143))
    summary = panels.find_mask(font, "Finance 11", screen, (5, 326, 130, 345))
    assert summary["bounds"] == [12, 333, 72, 344] and summary["ink_pixels"] == 104
    assert profile["ink_pixels"] == 122
    assert all(screen.getpixel((x, y)) == (16, 16, 16) for x in range(72, 78) for y in range(333, 344))
    second = DESCRIPTOR + 28
    shape = unpack_from("<7i", arm, second)
    assert shape == unpack_from("<7i", clean, second) == (-1, 12, 108, 0, 12, 60, 12)
    assert unpack_from("<I", arm, 0x9C1D4)[0] == unpack_from("<I", clean, 0x9C1D4)[0] == 0x02000000 + DESCRIPTOR
    name_row = unpack_from("<7i", arm, second + 28)
    assert name_row[5] == 204
    return dict(actual=summary, expected=profile, screenshot=shot, native_descriptor=shape,
                descriptor_file_offset=second, width_file_offset=second + 20, existing_name_bitmap_width=name_row[5],
                final_digit_cells_completely_blank=True, positive_match_to_original_60_pixel_crop=True)


def assignment(arm, report):
    snapshot = report["read_only_RAM_snapshot"]
    ram = load_exact(snapshot)
    _, get = get_machine(arm, ram)
    controller = get(0xCB1A8) + 0x2090
    model = get(0x82E04, controller)
    assert get(0x7B60, 3) == 20 and get(0x825E4, controller, 3) == 6
    slot, = [i for i in range(31) if (get(0x132C0, model, i), get(0x82BC4, controller, i)) == (20, 6)]
    actor = get(0xCB184) + 4 + 6 * 32
    assert get(0x7DD38, actor, 4, 20) == 115
    return dict(read_only_snapshot=snapshot, room_slot=slot, assigned_room_type=20, assigned_actor=6,
                finance=115, getters=[0x825E4, 0x132C0, 0x82BC4, 0x7DD38])


def main():
    active = read(play.current.RELEASE)
    assert digest(active["candidate"]) == active["candidate_sha256"]
    rom, clean = (NdsImage.open(path) for path in (active["candidate"], CLEAN))
    arm, clean_arm = [image.read_file(ARM) for image in (rom, clean)]
    common = rom.read_file(COMMON)
    assert sha256(arm).hexdigest() == active["target_ARM9_sha256"]
    assert sha256(common).hexdigest() == active["target_COMMON_sha256"] and digest(CLEAN) == active["clean_input_sha256"]
    font = panels.GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    installed = panels.common_rows(common, arm)
    capture = play.ROOT / "capture/capture_report.json"
    source_code = checked_text(getsource(panels.capture), {'(root / "controller.jsonl")': "CONTROLLER"})
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent), CONTROLLER=play.CONTROLLER)
    exec(compile(source_code, __file__ + "::verify-controller-path", "exec"), scope)
    frames, trace, evidence = scope["capture"](play.ROOT.name, active)
    assert max(frames) == 37300
    rows = dialogue(source, installed, frames, trace, font) + refit(source, installed, frames, trace, font)
    rows.extend(deck(source, installed, clean_arm, arm, frames, trace, font))
    crop = roster(font, clean_arm, arm, frames)
    final = read(capture)
    role = assignment(arm, final)
    balance = {str(frame): panels.find_mask(font, amount, panels.picture(frames[frame]), (65, 344, 140, 369))
        for frame, amount in ((34100, "27400"), (37300, "26995"))}
    trade = {label: panels.find_mask(font, expected, panels.picture(frames[35700]), bounds)
        for label, expected, bounds in (("pending_cost", "418", (58, 67, 128, 85)),
                                        ("pending_total", "26982", (58, 83, 128, 100)))}
    assert 27400 - 26995 == 405 and 418 - 405 == 13
    figures = [(label, panels.picture(frames[frame])) for label, frame in (
        ("Julio roster Finance crop", 30800), ("Yard settlement duration", 27600),
        ("Assigned Purser", 32000), ("Confirmed trade after bargaining", 37300))]
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=OUT), argdefs=panels.sheets_for.__defaults__)
    sheets = draw("lisbon_purser_ordinary", figures[1:])
    sheets += draw("lisbon_purser_roster", figures[:1], crop=(0, 300, 256, 376))
    archived = {284, 318, 750, 751, 752}
    assert not archived.intersection(event["message_ID"] for event in trace)
    proof = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=[r for r in rows if r["decision"] == "retention"])
    validate_natural_dialogue_batch(proof)
    write(OUT, proof | dict(candidate_sha256=active["candidate_sha256"], original_cold_boot_and_ordinary_controller_inputs=True,
        evidence=evidence | dict(controller=reference(play.CONTROLLER)), roster_finance_crop=crop,
        full_body_refit_wrap_followups=[r for r in rows if r["decision"] != "retention"],
        assigned_purser=role, balances=balance, initial_quote=trade,
        settled_olive_oil_cost=405, observed_discount=13, archived_ids_idle=sorted(archived),
        sheets=sheets, new_editorial_credit=0))
    print(f"Verified {len(rows)} current records, ordinary Purser assignment and the 60-pixel roster crop.")


if __name__ == "__main__":
    main()
