"""Verify the Lisbon Guild uses the earned Purser and settles both prices."""

import json
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R7, UC_ARM_REG_R8

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, NUMBER
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_lisbon_guild_bargaining_20261125 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.stage_sound_bgm_titles_v1 import get_raster
from scripts.verify_personal_gameplay_v841 import get_machine, machine


OUT = panels.OUT.with_name("lisbon_guild_bargaining_current_20261125.json")
PREFLIGHT = OUT.with_name("guild_trade_numerals_preflight_20261124.json")
BUY = (0x0205C308, 0x0205C334, UC_ARM_REG_R8, 0x0205C340, 0x02118160, 1083)
SALE = (0x0205BF68, 0x0205BF94, UC_ARM_REG_R7, 0x0205BFA0, 0x02118140, 1095)
END = 43060
GROWTH = 336
CONTEXT = "After Julio earns the Purser assignment in Lisbon, Rafael buys and then resells Travels of Marco Polo at the Guild."
HOLDS = (
    (62, "Guildmaster", [(38020, (), ("Need something?",))],
     "The Guildmaster asks if the customer needs anything.", "The relaxed opening gives Rafael the floor before the service menu."),
    (3665, "Guildmaster", [(38740, (), ("It's supposed to be a twisted horn.", "Some say it came from a dragon.",
                                          "Word is, you can turn it into", "medicine that cures any illness."))],
     "The Guildmaster repeats rumors about the horn, a possible dragon origin and a cure.",
     "The hearsay cues preserve the uncertainty as he encourages Rafael to consider the map."),
    (1071, "Guildmaster", [(n, (), ("Which one would you like?",)) for n in (38980, 40180)],
     "The Guildmaster asks which item Rafael wants.", "The invitation fits the initial list and the renewed choice after completing the purchase."),
    (1073, "Guildmaster", [(39460, ("10000",), ("Want to buy it for 10000 coins?",))],
     "The Guildmaster gives the price and asks whether Rafael will buy.",
     "The whole price and decision stay on one line. The selection already identifies the book."),
    (1080, "Julio Erneco", [(39700, (), ("That's a steep price. Surely you", "can lower it?"))],
     "Julio says the price is high and urges the Guildmaster to lower it.",
     "The question currently breaks after Surely you. Keep the seasoned challenge and put the complete question together."),
    (1083, "Guildmaster", [(39940, ("9800",), ("Fine. 9800 coins it is.",))],
     "The Guildmaster reluctantly accepts the revised purchase price.",
     "Fine marks the concession and the complete price makes clear why the bill differs from the initial quote."),
    (1085, "Guildmaster", [(41140, (), ("What would you like to sell?",))],
     "The Guildmaster asks which item Rafael wants to sell.", "The plain question changes the direction of the deal before the stock list opens."),
    (1086, "Guildmaster", [(41620, ("8000",), ("Hmm... How about 8000 coins?",))],
     "The Guildmaster pauses to appraise the book and offers a price to buy it from Rafael.",
     "The appraisal pause and direct offer fit the moment before Rafael decides whether to sell."),
    (1092, "Julio Erneco", [(41860, (), ("Eh? You don't know what this is", "worth. Take a closer look!"))],
     "Julio is incredulous that the Guildmaster has undervalued the item and tells him to look closer.",
     "The current break separates is from worth. Keep Julio's disbelief and the instruction in two complete thoughts."),
    (1095, "Guildmaster", [(42100, ("8200",), ("All right... I'll pay 8200 coins.",))],
     "The Guildmaster relents and says what he will pay.",
     "The pause keeps his reluctance. I'll pay makes the direction of the revised offer clear."),
    (335, "System", [(42340, ("Julio",), ("Julio leveled up!",))],
     "The notice says Julio has gained a level.", "The player sees who leveled up immediately after the negotiation."),
    (GROWTH, "System", [(42580, ("Luck", "2"), ("Luck increased by 2!",))],
     "The notice identifies the ability and amount of the increase.",
     "The line calls out the actual stat and increase and keeps both readable together."),
)


def snapshot(report, frame, arm):
    row, = [row for row in report["read_only_pause_RAM_snapshots"] if row["frame"] == frame]
    raw = Path(row["path"]).read_bytes()
    assert row["read_only_export"] and row["bytes"] == len(raw) == 0x400000
    assert sha256(raw).hexdigest() == row["sha256"]
    cpu, get = get_machine(arm, raw)
    assert get(0xB65E4) == 11
    controller = get(0xCB1A8) + 0x2090
    model = get(0x82E04, controller)
    slot, = [i for i in range(31) if (get(0x132C0, model, i), get(0x82BC4, controller, i)) == (20, 6)]
    assert get(0x825E4, controller, 3) == 6
    actor = get(0xCB184) + 4 + 6 * 32
    vtable, = unpack_from("<I", raw, actor - BASE)
    name_getter, = unpack_from("<I", raw, vtable - BASE + 0x20)
    name = get(name_getter - BASE, actor)
    assert bytes(cpu.mem_read(name, 24)).split(b"\0")[0] == b"Julio"
    companies = get(0xCB160)
    company = companies + 4 + 76 * get(0x397D8, companies)
    return dict(frame=frame, reference=row, captain_id=get(0x7F244), purser="Julio Erneco",
                actor=6, office_slot=slot, finance=get(0x7DCC8, actor, 4), voice=get(0x7E988, actor),
                wallet=get(0x3CCC8, company))


def price_fragment(clean, arm, proof, spec, skill, base):
    start, stop, register, call, voice_table, answer = spec
    spans = []
    for lo, hi in ((start, stop), (voice_table, voice_table + 32), (call + 4, call + 20)):
        raw = arm[lo - BASE:hi - BASE]
        assert raw == clean[lo - BASE:hi - BASE]
        spans.append(dict(start=lo, end=hi, sha256=sha256(raw).hexdigest()))
    case, = [row for row in proof["exact_ARM9_edits"] if row["message_ID"] == answer]
    assert case["address"] == call
    assert clean[call - BASE:call - BASE + 4] == assemble(f"bl {NUMBER}", call)
    assert arm[call - BASE:call - BASE + 4] == assemble(f"bl {HELPER}", call) == bytes.fromhex(case["installed_hex"])
    cpu = machine(arm)
    cpu.reg_write(UC_ARM_REG_R0, skill)
    cpu.reg_write(register, base)
    cpu.emu_start(start, stop, count=40)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop
    return dict(native_price=cpu.reg_read(register), item_base_price=base, finance=skill, answer=answer,
                checked_spans=spans, installed_numeral_call=case,
                voice_table=unpack_from("<8i", arm, voice_table - BASE))


def growth_display(report, image, arm, screen):
    frame = 42580
    snapshot, = [row for row in report["read_only_pause_RAM_snapshots"] if row["frame"] == frame]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(raw).hexdigest() == snapshot["sha256"]
    expanded, formatted = (unpack_from("<I", arm, offset)[0] - BASE for offset in (0x5444C, 0x54450))
    values = [raw[at:at + 256].split(b"\0", 1)[0] for at in (expanded, formatted)]
    assert values == [b" Luck increased by \x82Q!"] * 2
    plane, consumed = get_raster(image)(arm, values[1], 0x01FFCE40 - BASE, size=(228, 64),
                                        complete=False, instruction_limit=2000000)
    seen = bytes(pixel == (0, 8, 0) for pixel in screen.crop((16, 296, 244, 360)).get_flattened_data())
    assert seen == bytes(ink == 1 for ink in plane) and consumed == len(values[1])
    return dict(snapshot=snapshot, expansion_hex=values[0].hex(), formatted_hex=values[1].hex(),
                mixed_width_visible=values[1].decode("cp932").strip(), mixed_native_ink_pixels=sum(seen),
                full_width_amount_hex="8251", separate_glyph_fix_pending=True)


def contextual_record(ja, en, key, speaker, context, meaning, reason, holds, reference_frames, screens, trace, font, growth):
    displays = []
    for frame, arguments, lines in holds:
        values = tuple(a.encode("ascii") for a in arguments)
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(values)
        assert (en.text % values).decode("ascii").split() == " ".join(lines).split()
        first, second = [row for row in trace if row["message_ID"] == key and 0 < frame - row["frame"] <= 240]
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        glyphs = growth if key == GROWTH else panels.exact_body(font, lines, screens[frame])
        displays.append(dict(capture=reference_frames[frame], lines=lines, arguments=arguments, requests=[first, second],
                             glyphs=glyphs,
                             nameplate=panels.nameplate(font, speaker, screens[frame]) if speaker != "System" else None))
    installed = panels.text_reference(en) | {"exact_hex": en.text.hex()}
    return dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker=speaker, context=context, source_meaning=meaning,
        clean_Japanese=ja.text.decode("cp932"), english=en.text.decode("ascii").strip(), localization_note=reason,
        source_reference=panels.text_reference(ja) | {"exact_hex": ja.text.hex()}, current_reference=installed,
        installed_reference=installed, decision="retention", review=dict.fromkeys(GATES, True), observations=displays)


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    assert max(frames) == END
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands[:len(play.OPENING)] == list(play.OPENING)
    historical = read(play.prior.BOOK)
    old = read(historical["evidence"]["capture"]["path"])
    report = read(refs["capture"]["path"])
    assert report["scripted_input_schedule"][:len(old["scripted_input_schedule"])] == old["scripted_input_schedule"]
    assert refs["donor"]["sha256"] == historical["evidence"]["donor"]["sha256"]
    prior_held = panels.shots(old, "_navigation.png")[play.FIRST_PAUSE]
    assert prior_held["framebuffer_sha256"] == frames[play.FIRST_PAUSE]["framebuffer_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    clean_arm, arm = (rom.read_file(active.ARM) for rom in (clean, image))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(active.COMMON), clean_arm)
    installed = panels.common_rows(image.read_file(active.COMMON), arm)
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    state = {frame: snapshot(report, frame, arm) for frame in (37300, 39460, 40660, 41620, 42820, END)}
    assert all(row["office_slot"] == historical["assigned_purser"]["room_slot"] and row["captain_id"] == 0
               for row in state.values())
    assert [row["wallet"] for row in state.values()] == [26995, 26995, 17195, 17195, 25395, 25395]
    before_guild = read(PREFLIGHT)
    buy = price_fragment(clean_arm, arm, before_guild, BUY, state[39460]["finance"], 10000)
    sale = price_fragment(clean_arm, arm, before_guild, SALE, state[41620]["finance"], 10000)
    assert buy["native_price"] == state[39460]["wallet"] - state[40660]["wallet"] == 9800
    assert sale["native_price"] == state[42820]["wallet"] - state[41620]["wallet"] == 8200
    assert buy["voice_table"][state[39460]["voice"]] == 1080
    assert sale["voice_table"][state[41620]["voice"]] == 1092

    growth = growth_display(report, image, arm, screens[42580])
    records = []
    for key, speaker, holds, meaning, reason in HOLDS:
        row = contextual_record(source[key], installed[key], key, speaker, CONTEXT, meaning, reason, holds,
                                frames, screens, calls, font, growth)
        if key in (1080, 1092):
            row.update(decision="revision needed", review=dict.fromkeys(GATES, True) | {"formatting": False})
        if key == GROWTH:
            row.update(decision="wording retained, glyph revision needed",
                       review=dict.fromkeys(GATES, True) | {"formatting": False})
        records.append(row)
    batch = dict(candidate_sha256=release["candidate_sha256"], translation_policy="natural-dialogue-v2",
                 target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(GATES))
    validate_natural_dialogue_batch(batch | {"records": [row for row in records if row["decision"] == "retention"]})
    title = panels.find_mask(font, "Lisbon", screens[END], (51, 13, 108, 34))
    choices = {n: [panels.find_mask(font, word, screens[n], bounds) for word, bounds in (
        ("No", (127, 359, 172, 377)), ("Yes", (193, 359, 238, 377)))] for n in (39460, 41620)}
    figures = [(f"{n} / {speaker} / {key}", screens[n]) for key, speaker, holds, _, _ in HOLDS
               for n, _, _ in holds]
    figures.append(("Lisbon return", screens[END]))
    sheets = panels.sheets_for("lisbon_guild_bargaining_current_20261125", figures, crop=(0, 192, 256, 384))
    write(OUT, batch | dict(records=records, ordinary_gameplay=True, native_calculations=[buy, sale], state=state,
        source_replay=refs, earlier_earned_assignment=reference(play.prior.BOOK), commands=commands, native_requests=calls,
        purchased="Travels of Marco Polo", sold="Travels of Marco Polo", buy_list_price=10000, sale_first_quote=8000,
        item_and_stat_frames=[frames[n] for n in (39220, 40420, 41380, 42340, 42580, END)], verified_offer_choices=choices,
        stat_growth_glyph_lead=growth,
        archived_display_ids_requested=sorted({row["message_ID"] for row in calls} & {284, 318, 750, 751, 752}),
        returned_to_Lisbon=title, sheets=sheets, ROM_changed=False, new_editorial_credit=0))
    print("Verified the earned Purser, both original bargains and two phrase breaks.")


if __name__ == "__main__":
    main()
