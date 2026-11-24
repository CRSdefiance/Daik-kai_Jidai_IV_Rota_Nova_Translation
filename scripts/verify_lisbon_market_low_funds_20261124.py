"""Verify the funded investment and rejected purchase in ordinary Lisbon play."""

import json

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_lisbon_market_low_funds_20261124 as play
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = evidence.OUT.with_name("lisbon_market_low_funds_current_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 17081
panels = evidence.panels
HOLDS = (
    (12681, 763, ("You're going to invest?", "I knew you weren't like the others!", "How much will you put in?"),
     "The trader is surprised that Rafael will invest, says he seemed different from the others, and asks how much.",
     "The quick turn from surprise to flattery to a price question sounds like the same trader trying to close the deal."),
    (13881, 747, ("Thanks. We'll put it to good use.",),
     "The trader thanks Rafael and says the money will be put to good use.",
     "The short, appreciative answer fits the payment and preserves the promise to use the investment."),
    (15881, 753, ("You don't have enough money.",),
     "The trader tells Rafael he is short of money for the pending deal.",
     "The direct objection fits the trader and makes clear why the player is still in Trade."),
)


def capture(release):
    report_path = play.ROOT / "capture/capture_report.json"
    journal_path = report_path.with_name("navigation_command_journal.json")
    report, journal = map(read, (report_path, journal_path))
    schedule, prior_donor = play.schedule()
    donor = report["battery_save_preloaded"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["ROM_sha256"] == journal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == journal["last_command_frame"] == END
    assert donor["copied_byte_exact_before_cold_boot"] and not donor["savestate_loaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == prior_donor["source_sha256"]
    assert report["scripted_input_schedule"][:len(schedule)] == schedule
    assert list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines())) == list(play.ACTIONS)
    assert [row["command"] for row in journal["commands_received"]] == list(play.ACTIONS)
    assert all(row["validation_passed"] for row in journal["commands_received"])
    frames = panels.shots(report, "_navigation.png")
    last = read(play.BOOK)["state_and_panel_captures"]["back_11881"]
    assert frames[play.FIRST]["PNG_sha256"] == last["PNG_sha256"]
    assert frames[play.FIRST]["framebuffer_sha256"] == last["framebuffer_sha256"]
    refs = (report_path, journal_path, play.CONTROLLER, play.BOOK, play.HISTORY, donor["source"])
    return frames, list(map(reference, refs))


def stock_finish(clean_arm, arm):
    """Bind the displayed refusal to the original unsigned treasury branch."""
    base = 0x02000000
    cpu = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    probes = (
        (0x020BB410, "beq", "#0x20bc244"),
        (0x020BB440, "cmp", "r0, r4"),
        (0x020BB444, "blo", "#0x20bc22c"),
        (0x020BB450, "bl", "#0x2053cb0"),
        (0x020BC22C, "ldr", "r1, [pc, #0x78]"),
        (0x020BC234, "bl", "#0x2053fe4"),
        (0x020BC248, "bl", "#0x2053fe4"),
        (0x020C2B58, "bge", "#0x20c2b7c"),
        (0x020C2B70, "bl", "#0x2053fe4"),
    )
    instructions = []
    for address, mnemonic, operands in probes:
        start = address - base
        raw = arm[start:start + 4]
        assert raw == clean_arm[start:start + 4]
        insn, = cpu.disasm(raw, address)
        assert (insn.mnemonic, insn.op_str) == (mnemonic, operands), (hex(address), insn.mnemonic, insn.op_str)
        instructions.append(dict(address=hex(address), bytes=raw.hex(), mnemonic=mnemonic, operands=operands))
    literals = []
    for address, key in ((0x020BC2AC, 753), (0x020BC2B0, 746), (0x020C2B98, 749)):
        start = address - base
        raw = key.to_bytes(4, "little")
        assert arm[start:start + 4] == clean_arm[start:start + 4] == raw
        literals.append(dict(address=hex(address), COMMON=key, bytes=raw.hex()))
    return dict(method="offline original ARM9 instruction and ID comparison", instructions=instructions, literals=literals)


def check_purchases(font, screens):
    investment = {
        frame: [panels.find_mask(font, str(value), screens[frame], rect) for value, rect in zip(
            amounts, ((134, 327, 192, 348), (134, 346, 192, 364)), strict=True)]
        for frame, amounts in ((13081, (3000, 24400)), (13481, (27000, 400)))
    }
    market = {frame: panels.find_mask(font, str(value), screens[frame], (55, 348, 139, 366))
              for frame, value in ((11881, 27400), (14281, 400), (16681, 400))}
    ledger = {}
    for frame, spending, total in ((14681, 0, 400), (15481, 1144, -744), (16281, 1144, -744), (END, 0, 400)):
        screen = screens[frame]
        white = [panels.find_mask(font, str(value), screen, (62, y, 117, y + 14))
                 for y, value in zip((36, 52, 68), (400, 0, spending), strict=True)]
        rect = (62, 84, 117, 98)
        if total >= 0:
            total_glyphs = panels.find_mask(font, str(total), screen, rect)
        else:
            red = (213, 64, 16)
            sign = {(x, y) for y in range(84, 98) for x in range(62, 92) if screen.getpixel((x, y)) == red}
            assert sign == {(x, 91) for x in range(66, 73)}
            digits = evidence.glyph_mask(font, str(abs(total)), screen, (92, 84, 117, 98), red,
                                         range(92, 99), range(84, 90))
            total_glyphs = dict(native_separate_minus=list(sorted(sign)), digits=digits)
        ledger[frame] = dict(funds=400, income=0, spent=spending, sum=total, white_glyphs=white, sum_glyphs=total_glyphs)
    assert 27400 - 27000 == 400 and 2 * 572 == 1144 and 400 - 1144 == -744
    assert screens[15481].tobytes() == screens[16281].tobytes()
    assert screens[14681].tobytes() == screens[END].tobytes()
    return dict(initial_gold=27400, investment_gold=27000, settled_gold=400, quote=572, staged_units=2,
                staged_total=1144, projected_gold=-744, investment=investment, market_wallets=market,
                ledger=ledger, dismissed_refusal_restores_exact_pending_trade=True, back_restores_exact_empty_trade=True)


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    frames, refs = capture(release)
    screens = {frame: panels.picture(row) for frame, row in frames.items()}
    clean, installed = map(NdsImage.open, (CLEAN, play.current.ROM))
    clean_arm, arm = (rom.read_file(play.current.ARM) for rom in (clean, installed))
    path = play.current.COMMON
    archive = installed.read_file(path)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = evidence.base.common_message_entries(clean.read_file(path), clean_arm)
    current = evidence.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    records = []
    context = ("After investing in Lisbon, Rafael tries to buy two units of Salt for more than he has. "
               "The trader refuses, dismissing the warning restores the pending deal, and Back clears it.")
    for frame, key, lines, gloss, reason in HOLDS:
        ja, en = source[key], current[key]
        english = " ".join(lines)
        assert " ".join(en.text.decode("ascii").split()) == english and b"%" not in ja.text + en.text
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=path, speaker="Trader",
            english=english, clean_Japanese=ja.text.decode("cp932"), source_meaning=gloss, context=context,
            localization_note=reason, decision="retention", review=dict.fromkeys(GATES, True),
            source_reference=evidence.source_ref(ja), current_reference=evidence.source_ref(en),
            installed_reference=evidence.source_ref(en),
            hold=dict(frame=frames[frame], body=panels.exact_body(font, lines, screens[frame]),
                      nameplate=panels.nameplate(font, "Trader", screens[frame]))))
    purchases = check_purchases(font, screens)
    offline = stock_finish(clean_arm, arm)
    labels = ((12681, "Trader asks how much"), (13481, "Invest 27,000"), (13881, "Trader accepts the investment"),
              (15481, "Two Salt units exceed the balance"), (15881, "Finish refuses the deal"),
              (16281, "Dismissal restores the pending deal"), (16681, "Back returns to Market"),
              (END, "Reopened Trade is clear"))
    sheet = Image.new("RGB", (1024, 808), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(labels):
        x, y = (index % 4) * 256, (index // 4) * 404
        draw.text((x + 4, y + 4), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    receipt = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=records, clean_rom_sha256=release["clean_input_sha256"],
        candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, fixture_or_state_load=False,
        original_lisbon_checkpoint_matches=True, transactions=purchases, stock_finish_scope=offline,
        evidence=refs + [reference(play.current.RELEASE)], contact_sheet=str(SHEET),
        unvisited=["Double-price stock offer", "Other indirect owners of archived COMMON records", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(receipt)
    sheet.save(SHEET)
    receipt["contact_sheet"] = reference(SHEET)
    write(OUT, receipt)
    print("Verified the 27,000-gold investment, 1,144-gold refusal, intact pending trade and restored 400-gold balance.")


if __name__ == "__main__":
    main()
