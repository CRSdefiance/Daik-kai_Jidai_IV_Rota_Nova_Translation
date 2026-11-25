"""Verify Lisbon's stock quota, ship transactions, and Refit context on Ceuta."""

import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.refit_help import compile_paragraph
from scripts import observe_lisbon_stock_quota_20261124 as play
from scripts import preflight_lisbon_purser_refit_20261124 as draft
from scripts import verify_lisbon_extra_stock_20261124 as earlier
from scripts import verify_syracuse_local_purchase_20261124 as ledger
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine


OUT = earlier.OUT.with_name("lisbon_stock_quota_current_20261124.json")
scope, panels = earlier.evidence, earlier.panels
END = 68500
REFIT = {
    42500: (1285, "Lateen", "The windward benefit and the restriction about a sail behind it read distinctly."),
    42800: (1277, "Supplies", "This brief instruction names both things stored here."),
    43100: (1281, "Add Equipment", "The specific armor instruction clarifies what fits this slot."),
    43400: (1255, "Purser", "Say buy out local stock to identify a local purchase beyond the share, alongside bargaining."),
    43700: (1248, "Lumber", "The repair benefit fits the room and leaves the amount of damage open."),
    44000: (1249, "Sickbay", "The doctor treats ailments affecting officers and sailors."),
    44120: (1250, "Galley", "The current wording keeps the two supplies and the separate fatigue benefit."),
    44240: (1251, "Lounge", "Officer morale and reduced sailor fatigue remain separate effects."),
    44360: (1252, "Nursery", "The role makes the food last longer, which fits the livestock room."),
    44480: (1253, "Chapel", "The morale effect and the optional distribution in the Square remain separate."),
    44600: (1254, "Tactics", "The room enables planning at the tavern, and the text identifies the location."),
    44720: (1247, "Cabin", "The line clearly limits health and morale recovery to the officers here."),
    47300: (1283, "Figurehead", "The instructions identify the mounting point and the existing-ownership requirement."),
    47600: (1280, "Add Equipment", "The note separates the bow equipment from the larger-ship spritsail option."),
}
DIALOGUE = {
    8: ((54500, 62300), "Trader", (), ("Need help?",), "The brief greeting lets Rafael choose a service."),
    10: ((66700,), "Trader", (), ("All right. I'll cut you a break.",), "The reluctant concession leads directly into the discounted charge."),
    15: ((65500, 66100), "Julio Erneco", (), ("Will this do?",), "The restrained approval question suits Julio and covers the purchase and sale together."),
    24: ((66400,), "Julio Erneco", (), ("Sorry to trouble you, but could you", "do a bit better?"),
         "Julio apologizes before asking for a better price. The complete question reads as a polite negotiation."),
    63: ((52400,), "Innkeeper", (), ("Welcome! Come in.",), "The warm invitation suits the innkeeper's greeting."),
    265: ((50300, 60200), None, (), ("Buy this ship?",), "The short prompt names the pending action before name entry."),
    296: ((50900, 60800), None, ("Latina",), ("Is Latina all right?",), "The final question confirms the exact ship name shown by the editor."),
    758: ((37700, 55100, 62900, 67300), "Julio Erneco", (), ("It seems paying double this time", "will get us more of certain goods."),
          "Julio's measured advice distinguishes the double-price lots and limits the offer to the current visit and eligible stock."),
    786: ((50000, 59900), "Shipwright", ("2", "25"), ("Masts: 2. Durability: 25.",), "The two distinct ship stats are clear and match the selection screen."),
    1177: ((53000,), "Innkeeper", (), ("That'll be 1 gold coin.",), "The quote states exactly what the single night costs."),
    1178: ((53300,), "Innkeeper", (), ("Sleep well!",), "The brief farewell fits the one-night stay."),
    1266: ((41900, 48200), "Shipwright", (), ("Which ship would you like to refit?",), "The question asks the player to select the vessel before the Refit interface opens."),
}
SOURCE_MEANINGS = {
    8: "The trader asks whether the visitor needs anything.",
    10: "The trader relents and offers a small discount.",
    15: "The speaker asks whether the current deal is satisfactory.",
    24: "The speaker apologizes, then asks whether the price can be improved a little.",
    63: "The innkeeper welcomes the visitor.",
    265: "The prompt asks for confirmation of the selected ship purchase.",
    296: "The prompt asks whether the chosen name is acceptable.",
    758: "The speaker thinks paying twice as much will buy additional stock of some goods this time.",
    786: "The shipwright gives the ship's mast count and durability.",
    1177: "The innkeeper quotes a price of one gold coin.",
    1178: "The innkeeper bids the guest good night.",
    1247: "Officers in this cabin recover health and morale.",
    1248: "Having a ship carpenter makes it possible to repair a damaged ship.",
    1249: "Having a ship doctor makes it possible to treat ailments in officers and sailors.",
    1250: "Having a chief cook saves water and food and slows the sailors' fatigue.",
    1251: "Officers in the room recover morale and make the sailors tire less easily.",
    1252: "An animal keeper slows the loss of food supplies.",
    1253: "A missionary relieves sailors' discontent and enables distribution of trade goods in the Square.",
    1254: "A strategist makes it possible to plan schemes at the tavern.",
    1255: "A purser makes it possible to bargain and buy out the stock.",
    1266: "The shipwright asks which ship should be refitted.",
    1277: "The room stores water and food.",
    1280: "This slot accepts a ram, bow gun or, on at least a medium ship, a spritsail.",
    1281: "Extra armor can be fitted here.",
    1283: "This slot takes a figurehead the player owns.",
    1285: "A lateen sail works well against the wind, and a square sail cannot go behind it.",
}


def capture(manifest):
    root = play.ROOT / "capture"
    cap, journal = (root / file for file in ("capture_report.json", "navigation_command_journal.json"))
    run, nav, context = map(read, (cap, journal, play.ROOT / "stock_quota_runner.json"))
    assert context["source"] == reference(play.__file__) and context["controller"] == reference(play.CONTROLLER)
    assert run["ROM_sha256"] == nav["ROM_sha256"] == context["rom_sha256"] == manifest["candidate_sha256"]
    assert run["frames"] == nav["last_command_frame"] == END
    assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
    assert [key for key, result in run.items() if key.startswith("synthetic_") and result] == ["synthetic_market_finance_prerequisite"]
    controller = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert controller[:len(play.OPENING)] == list(play.OPENING) and controller[-1] == {"stop": True}
    assert controller == [row["command"] for row in nav["commands_received"]]
    assert all(row["validation_passed"] for row in nav["commands_received"])
    prior_packet = read(earlier.OUT)
    fixture, = run["synthetic_market_finance_prerequisite"]
    assert not run["earned_finance_prerequisite_verified"]
    state_keys = {"full_RAM_before_sha256", "full_RAM_after_sha256"}
    assert {k: v for k, v in fixture.items() if k not in state_keys} == {
        k: v for k, v in prior_packet["focused_prerequisite"].items() if k not in state_keys}
    snapshot, = (r for r in run["read_only_pause_RAM_snapshots"] if r["frame"] == fixture["frame"])
    before = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(before).hexdigest() == snapshot["sha256"] == fixture["full_RAM_before_sha256"]
    after = bytearray(before)
    for change in fixture["changes"]:
        offset = change["address"] - play.stock.BASE
        assert after[offset] == change["before"]
        after[offset] = change["after"]
    assert sha256(after).hexdigest() == fixture["full_RAM_after_sha256"]
    stock_capture = play.stock.ROOT / "capture/capture_report.json"
    prior = read(stock_capture)
    donor = run["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and donor["source_sha256"] == digest(donor["source"])
    assert donor["source_sha256"] == prior["battery_save_preloaded"]["source_sha256"]
    frames, former = [panels.shots(data, "_navigation.png") for data in (run, prior)]
    matches = (37300, 37700, 38100, 38500, 38900)
    assert all(frames[n]["framebuffer_sha256"] == former[n]["framebuffer_sha256"] for n in matches)
    return run, frames, fixture, controller, list(map(reference, (cap, journal, stock_capture, earlier.OUT, play.CONTROLLER,
                                                                     play.ROOT / "stock_quota_runner.json", donor["source"])))


def records(source, installed, font, frames, screens):
    def record(key, context, rationale, decision):
        a, b = source[key], installed[key]
        return dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON, context=context, source_meaning=SOURCE_MEANINGS[key],
            english=" ".join(b.text.decode("ascii").split()), clean_Japanese=a.text.decode("cp932"),
            source_reference=scope.source_ref(a), current_reference=scope.source_ref(b), installed_reference=scope.source_ref(b),
            decision=decision, localization_note=rationale, review=dict.fromkeys(GATES, True))

    completed = []
    for key, (sample, speaker, arguments, lines, rationale) in DIALOGUE.items():
        context = "The Lisbon purchase, refit, lodging and six-lot Guns deal after Julio's Finance prerequisite is supplied."
        item = record(key, context, rationale, "retention")
        assert item["english"] % arguments == " ".join(lines)
        assert installed[key].text.count(b"%s") == source[key].text.count(b"%s") == len(arguments)
        item.update(speaker=speaker, holds=[dict(capture=frames[n], exact_body=panels.exact_body(font, lines, screens[n]),
            nameplate=panels.nameplate(font, speaker, screens[n]), lines=lines, arguments=arguments) for n in sample])
        completed.append(item)
    proposed = None
    for frame, (key, label, rationale) in REFIT.items():
        item = record(key, f"The {label} panel in the Lisbon shipwright's Refit view.", rationale, "retention")
        text = installed[key].text
        assert b"%" not in source[key].text + text
        compiled, _ = compile_paragraph(item["english"])
        stored_lines = text.decode("ascii").splitlines()
        lines = [line.rstrip() for line in stored_lines]
        assert " ".join(lines) == item["english"]
        assert all(0 < len(line) <= 27 for line in lines)
        assert len(lines) <= 5 and all(len(line) % 2 == 0 for line in stored_lines[:-1])
        screen = screens[frame]
        masks = [panels.find_mask(font, line, screen, (60, 76 + 12 * i, 236, 94 + 12 * i)) for i, line in enumerate(lines)]
        item.update(speaker="Refit help", standard_formatter_reproduces_stored_bytes=(compiled == text + b"\0"),
            holds=[dict(capture=frames[frame], lines=lines, exact_masks=masks,
            title=panels.find_mask(font, label, screen, (59, 27, 236, 50)))])
        if key == draft.KEY:
            proposed = item | dict(decision="revision_proposed", review=dict.fromkeys(GATES, True) | {"formatting": False},
                                   proposed_english=draft.ENGLISH, native_preflight=reference(draft.OUT))
        else:
            completed.append(item)
    assert proposed is not None
    return completed, proposed


def trades(run, arm, font, frames, screens):
    initial, sale, unit = 21794, 211, 1277
    costs = {63200: 0, 63400: 0, 63800: unit, 64000: 2 * unit, 64400: 3 * unit, 64600: 4 * unit,
             65000: 5 * unit, 65200: 7 * unit, 65500: 7 * unit, 65800: 7 * unit, 66100: 7 * unit}
    states = {n: ledger.exact_ledger(font, screens[n], (initial, sale if n > 63200 else 0, spent,
              initial + (sale if n > 63200 else 0) - spent)) for n, spent in costs.items()}
    assert screens[38900].tobytes() == screens[39200].tobytes()
    assert screens[65500].tobytes() == screens[66100].tobytes()
    difference = ImageChops.difference(screens[65200], screens[65800])
    blinking = [(20, 197, 44, 219), (212, 197, 236, 219), (210, 284, 238, 312)]
    for rect in blinking:
        assert difference.crop(rect).getbbox()
        difference.paste((0, 0, 0), rect)
    assert difference.getbbox() is None
    assert panels.find_mask(font, "26052", screens[39800], (60, 84, 117, 99))
    assert panels.find_mask(font, "26995", screens[40100], (55, 348, 139, 366))
    price = panels.find_line(font, "2554", screens[65000], range(209, 224), range(309, 318), (246, 246, 0))
    choice = {n: [panels.find_mask(font, word, screens[n], rect) for word, rect in
                (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))] for n in (65500, 66100)}
    after = 13341
    assert after - (initial + sale - 7 * unit) == 275
    cleared = {n: ledger.exact_ledger(font, screens[n], (after, 0, 0, after)) for n in (67600, 67900, 68200)}
    assert panels.find_mask(font, str(after), screens[67000], (55, 348, 139, 366))
    snapshot, = [r for r in run["read_only_pause_RAM_snapshots"] if r["frame"] == 68200]
    ram = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(ram).hexdigest() == snapshot["sha256"]
    cpu, get = get_machine(arm, ram)
    fleet = get(0xCB1A8) + 4 + get(0x2E58C) * 0x84
    ships = [get(0x36C94, fleet + 12 + i * 8) for i in range(3)]
    names = [bytes(cpu.mem_read(ship + 8, 20)).split(b"\0")[0].decode("ascii") for ship in ships]
    assert names == ["Carteira", "Latina", "Latina"]
    cargo = [list(bytes(cpu.mem_read(ship + 0x50, 60))[::12]) for ship in ships]
    gun = cargo[0][0]
    assert gun not in (14, 125) and cargo == [[gun, gun, 125, 125, 125]] * 3
    return dict(regular_unit_price=unit, regular_lots=5, additional_unit_price=2 * unit, additional_lots=1,
                yellow_price_mask=price, cargo_room_sale=211, quote=initial + sale - 7 * unit,
                bargain_discount=275, settlement=after, pending_ledgers=states, cleared_ledgers=cleared,
                declined_return_except_blinking_arrows_and_cursor=blinking, repeated_confirmation_exact=True,
                choices=choice, returned_to_market=frames[END], settled_gun_ID=gun,
                settled_ships=names, settled_cargo=cargo, cargo_snapshot=snapshot)


def sheets(screens):
    groups = (
        ((37700, "Julio announces the option"), (38900, "One Salt with one free hold"), (39800, "Two Salt after staging a sale"),
         (43400, "Current Purser help"), (49700, "Standard Latina quote"), (50900, "Confirm the Latina name")),
        ((64600, "Four regular-price lots"), (65000, "Five lots. Extra price appears."), (65200, "Six lots staged"),
         (66100, "Julio asks for approval"), (66400, "Julio asks for a better price"), (66700, "Trader agrees")),
        ((67000, "Settled balance"), (67300, "Julio repeats the advice"), (67600, "Carteira cargo"),
         (67900, "First Latina cargo"), (68200, "Second Latina cargo"), (68500, "Return to Market")),
    )
    results = []
    for number, group in enumerate(groups, 1):
        canvas = Image.new("RGB", (768, 808), "#263238")
        draw = ImageDraw.Draw(canvas)
        for index, (frame, label) in enumerate(group):
            x, y = index % 3 * 256, index // 3 * 404
            canvas.paste(screens[frame], (x, y + 20))
            draw.text((x + 4, y + 4), label, fill="white")
        path = OUT.with_name(f"lisbon_stock_quota_current_{number}_20261124.png")
        canvas.save(path)
        results.append(reference(path))
    return results


def main():
    current = play.current
    manifest = read(current.RELEASE)
    assert digest(CLEAN) == manifest["clean_input_sha256"] and digest(REGISTRY) == manifest["registry_sha256"]
    assert digest(current.ROM) == manifest["candidate_sha256"]
    run, frames, fixture, controller, refs = capture(manifest)
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    arm, archive = image.read_file(current.ARM), image.read_file(current.COMMON)
    assert sha256(arm).hexdigest() == manifest["target_ARM9_sha256"] and sha256(archive).hexdigest() == manifest["target_COMMON_sha256"]
    source = scope.base.common_message_entries(clean.read_file(current.COMMON), clean.read_file(current.ARM))
    installed = scope.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {n: panels.picture(row) for n, row in frames.items()}
    completed, proposed = records(source, installed, font, frames, screens)
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), candidate_sha256=manifest["candidate_sha256"], records=completed, proposed_revision=proposed,
        isolated_finance_fixture=fixture, ordinary_inputs_after_fixture=True, ordinary_gameplay=False, controller=controller,
        trade=trades(run, arm, font, frames, screens), evidence=refs, new_editorial_credit=0, ROM_changed=False,
        unvisited=["Naturally earned Finance 160", "Other eligible goods and adviser voices", "Physical hardware"])
    validate_natural_dialogue_batch(result)
    result["contact_sheets"] = sheets(screens)
    write(OUT, result)
    print(f"Verified the regular and extra quota, six delivered lots, {len(completed)} retentions and the Refit revision proposal.")


if __name__ == "__main__":
    main()
