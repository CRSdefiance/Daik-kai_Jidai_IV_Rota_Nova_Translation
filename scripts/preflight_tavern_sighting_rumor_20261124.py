"""Review the witnessed-treasure rumor and its original patron follow-up."""

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import preflight_istanbul_tavern_rumor_20261124 as earlier
from scripts import register_istanbul_tavern_rumor_20261124 as parent
from scripts.probe_button_prompt_native import STACK
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
from unicorn.arm_const import UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP


ARM, COMMON = earlier.ARM, earlier.COMMON
trend, panels = earlier.athens.town, earlier.PANELS
KEY, REPLY = 863, 868
OUT = earlier.OUT.with_name("tavern_sighting_rumor_preflight_20261124.json")
RELEASE = parent.RELEASE
PROPOSAL = "Heard the rumor about a rare item? They say %s was seen in %s..."
SAMPLES = ("Black Rapier", "Red-Haired Pirate Sword", "Saladin's Silver Armor")
CONTEXT = ("A Tavern patron relays a rumor that someone saw a rare item. In the optional next panel, "
           "he doubts the drunk's word and suggests the listener may be able to make sense of the story.")


def stock_calls(runtime):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    names, _ = earlier.providers(cpu, get)
    first_item = get(0xCB190) + 4
    stock = [(row, first_item + 20 * row["index"]) for row in names]
    items = [(row, address, get(0x4A3F0, address)) for row, address in stock]
    events, cases = [], []

    def collect(u, address, size, unused):
        events.append(tuple(u.reg_read(reg) for reg in (
            UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        )))
        u.emu_stop()

    def text_at(pointer):
        return bytes(cpu.mem_read(pointer, 64)).split(b"\0", 1)[0].decode("ascii")

    hook = cpu.hook_add(UC_HOOK_CODE, collect, begin=0x02053FE4, end=0x02053FE4)
    try:
        for item, address, region in items:
            if region >= len(earlier.REGIONS):
                assert region == 8
                continue
            events.clear()
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.reg_write(UC_ARM_REG_R5, region)
            cpu.reg_write(UC_ARM_REG_R6, address)
            cpu.emu_start(0x02059950, 0x02059994, count=50000)
            (actor, receiver, name, area), = events
            assert receiver == KEY and text_at(name) == item["name"] and text_at(area) == earlier.REGIONS[region]
            cases.append(dict(item_index=item["index"], item_object=address, region_index=region, speaker_object=actor,
                              pointers=[name, area], arguments=[text_at(name), text_at(area)]))
        speaker, = {row["speaker_object"] for row in cases}
        events.clear()
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_R4, speaker)
        cpu.emu_start(0x020599BC, 0x020599C8, count=50000)
        (actor, receiver, _, _), = events
        assert actor == speaker and receiver == REPLY
    finally:
        cpu.hook_del(hook)
    assert len(cases) == 121 and text_at(get(0x7EB0C, speaker)) == "Patron"
    return cases, dict(message_ID=REPLY, same_original_speaker_object=speaker, source_call_site=0x020599C4)


def layout(cpu, template, key, args=()):
    assert template.startswith(b" ") and template.count(b"%s") == len(args)
    out = earlier.format_case(cpu, dict(message_id=key, english=template[1:].decode("ascii")),
                              [value.encode("ascii") for value in args])
    assert 1 <= len(out["lines"]) <= 4
    assert all(0 < len(line) <= 35 for line in out["lines"])
    assert "four_row_width_bound" not in out["findings"]
    return out


def record(key, source, old, new, meaning, reason):
    return dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=COMMON, speaker="Patron",
        clean_Japanese=source.text.decode("cp932"), context=CONTEXT,
        english=new.text.decode("ascii").strip(), source_meaning=meaning, localization_note=reason,
        source_hex=source.text.hex(), current_hex=old.text.hex(), proposed_hex=new.text.hex(),
        source_reference=earlier.exact_entry(source), current_reference=earlier.exact_entry(old),
        proposed_reference=panels.text_reference(new), decision="revision" if key == KEY else "retention",
        review=dict.fromkeys(earlier.GATES, True))


def main():
    release = earlier.read(RELEASE)
    assert earlier.digest(earlier.REGISTRY) == release["registry_sha256"]
    assert earlier.digest(earlier.CLEAN) == release["clean_input_sha256"]
    ctx = earlier.RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    assert earlier.sha256(ctx.arm).hexdigest() == release["target_ARM9_sha256"]
    assert earlier.sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    clean = earlier.NdsImage.open(earlier.CLEAN)
    before = earlier.athens.common_rows(ctx.common, ctx.arm)
    source = earlier.guild.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    del clean
    old = before[KEY].text
    assert old == b" Have you heard? Someone may have spotted a rare item called %s in %s..."
    proposed = (b" " + PROPOSAL.encode("ascii")).ljust(len(old), b" ")
    assert len(proposed) == len(old) and old.count(b"%s") == source[KEY].text.count(b"%s") == proposed.count(b"%s") == 2
    revised, installed, allocation = earlier.guild.owned_deployment(ctx.common, ctx.arm, before, {KEY: proposed})
    assert [b.message_id for a, b in zip(before, installed, strict=True) if a != b] == [KEY]

    cases, followup = stock_calls(ctx)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    split_count = 0
    for case in cases:
        args = case["arguments"]
        case["previous"] = layout(cpu, old, KEY, args)
        case["proposed"] = layout(cpu, proposed, KEY, args)
        split_count += not any(args[0] in line for line in case["previous"]["lines"])
        assert all(any(term in line for line in case["proposed"]["lines"]) for term in (*args, "rare item", "They say"))
    assert split_count == 89
    followup["layout"] = layout(cpu, before[REPLY].text, REPLY)
    records = [
        record(KEY, source[KEY], before[KEY], installed[KEY],
               "The patron asks if the listener heard a rumor that someone saw a rare item with this name in this region.",
               "They say keeps the report tentative and leads into the patron's optional warning. The first question stands alone, so the following line can keep the item name together."),
        record(REPLY, source[REPLY], before[REPLY], installed[REPLY],
               "The patron says the source is a drunk whose report cannot be trusted. The listener may understand what to make of it.",
               "The present voice shifts from distrust to qualified respect for the listener and preserves both ideas. Trust it reads as a complete verb phrase at the start of the second line."),
    ]
    paint, _, _ = trend.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    sample_rows = [(f"{label} / {case['arguments'][0]}", case[field]) for case in cases if case["arguments"][0] in SAMPLES
                   for label, field in (("Previous", "previous"), ("Proposed", "proposed"))]
    sample_rows.append(("Optional follow-up retained", followup["layout"]))
    figures = []
    for title, row in sample_rows:
        raw = bytes.fromhex(row["formatted_hex"])
        plane, events = trend.render_portrait(paint, ctx.arm, kanji, raw)
        assert [event["code"] for event in events] == trend.glyph_codes(raw)
        assert all(0 <= event["x"] < 228 and 0 <= event["y"] < 64 for event in events)
        figures.append((title, plane))
    preview = OUT.with_suffix("")
    preview.mkdir(exist_ok=True)
    result = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(earlier.GATES), records=records, candidate_sha256=release["candidate_sha256"],
        source_sha256=release["clean_input_sha256"], unchanged_ARM9_sha256=release["target_ARM9_sha256"],
        proposed_COMMON_sha256=earlier.sha256(revised).hexdigest(), proposed_sheets=trend.portrait_sheets(preview, figures),
        allocation=allocation[KEY], native_cases=cases, optional_same_speaker_followup=followup,
        previous_item_names_split=split_count, proposed_item_names_split=0,
        coverage="Native caller fragments and complete offline dialogue layouts; ordinary selection unobserved.",
        ordinary_representative_consumer=earlier.reference(parent.REVIEW), new_editorial_credit=0)
    validate_natural_dialogue_batch(result)
    earlier.write(OUT, result)
    print(f"Verified {len(cases)} native item/region bindings and layouts. Split item names fall from {split_count} to zero.")


if __name__ == "__main__":
    main()
