"""Stage the London Guild pitch, buy quote, and empty sale reply after native checks."""

from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from
from textwrap import wrap

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ascii_glyph_right_bounds import assemble
from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, ITCM, NUMBER, compact_helper
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_london_guild_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts import verify_yard_numerals_native_20261124 as native
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference as text_reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_inn_numerals_native_20261119 import RING, RING_SIZE, normalize


ARM, COMMON = play.active.ARM, play.active.COMMON
PITCH, SIZE, PITCH_ID = 0x143D20, 88, 0xFFFFFFFF
BUY_CALL, BUY_WRAPPER, PITCH_WRAPPER = 0x0205C2A0, 0x02053F9C, 0x02054020
PITCH_ENGLISH = "You're in luck! I've got an old map said to lead to legendary treasure."
EDIT = {1073: "Want to buy it for %s coins?", 1084: "Wait. You've got nothing to sell."}
CONTEXT = "The Guildmaster pitches an old map and describes the dagger. Hodram sees the item choices, declines the Loom, buys the map, then opens Sell Items."
PITCH_PRIOR = Path("translations/editorial_checkpoints/SharedText_20261110_v1/ancient_map_rumors_context_v2.json")
PRICE = Path("work/analysis/guild_price_domain_v2245/original_item_prices_skill_clamp_and_English_unit_contract.json")
OUT = panels.OUT.with_name("london_guild_display_preflight_20261124.json")
ROOT = Path(".codex-release-work/london_guild_display_20261124")
ROM = ROOT / "London_Guild_Display_STAGED.nds"


def layout_function():
    source = checked_text(getsource(native.formatters.layout), {
        "else 0x02053FCC if n in YESNO else 0x02054014":
            "else 0x02053FCC if n in GUILD_CHOICES else PITCH_PARENT if n == PITCH_ID else 0x02054014",
    })
    scope = vars(native.formatters) | dict(GUILD_CHOICES=(1073,), PITCH_PARENT=PITCH_WRAPPER + 0x28, PITCH_ID=PITCH_ID)
    exec(compile(source, __file__ + "::Guild-native-layout", "exec"), scope)
    return scope["layout"]


def propose_arm9(clean, arm):
    assert clean[0x5C188:0x5C1D0].hex() == read(PITCH_PRIOR)["original_native_selection_code_hex"]
    assert arm[0x5C188:0x5C1D0] == clean[0x5C188:0x5C1D0]
    assert unpack_from("<I", arm, 0x5C458)[0] == BASE + PITCH
    assert arm[0x5C1BC:0x5C1C0] == assemble(f"bl {PITCH_WRAPPER}", 0x0205C1BC)
    assert arm[0x5C29C:0x5C2B4] == clean[0x5C29C:0x5C2B4]
    assert unpack_from("<I", arm, 0x5C468)[0] == 1073
    assert arm[0x5C2B0:0x5C2B4] == assemble(f"bl {BUY_WRAPPER}", 0x0205C2B0)
    code = native.patch.MainCodeFile(arm, BASE)
    helper = compact_helper()
    itcm = code.sections[4]
    assert itcm.ramAddress == ITCM and bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    assert clean[NUMBER - BASE:NUMBER - BASE + 0x7C] == arm[NUMBER - BASE:NUMBER - BASE + 0x7C]

    reference = read(PITCH_PRIOR)
    source, previous = (blob[PITCH:PITCH + SIZE] for blob in (clean, arm))
    source_body, previous_body = (data.split(b"\0")[0] for data in (source, previous))
    assert source_body.decode("cp932") == reference["original_preamble_Japanese"]
    assert previous_body.decode("ascii") == reference["current_preamble_English"]
    lines = wrap(PITCH_ENGLISH, width=35, break_long_words=False, break_on_hyphens=False)
    compiled = "\n ".join(lines).encode("ascii")
    assert len(lines) == 2 and len(compiled) < SIZE and max(map(len, lines)) <= 35
    applied = compiled.ljust(SIZE, b"\0")
    offset = BUY_CALL - BASE
    old = assemble(f"bl {NUMBER}", BUY_CALL)
    new = assemble(f"bl {HELPER}", BUY_CALL)
    assert arm[offset:offset + 4] == old
    target = bytearray(arm)
    target[PITCH:PITCH + SIZE] = applied
    target[offset:offset + 4] = new
    target = bytes(target)
    assert native.patch.cache_plan(target) == native.patch.cache_plan(arm)
    edits = [dict(offset=PITCH, source_hex=source.hex(), previous_hex=previous.hex(), installed_hex=applied.hex()),
             dict(offset=offset, address=BUY_CALL, source_hex=old.hex(), previous_hex=old.hex(), installed_hex=new.hex())]
    return target, edits, (source_body, previous_body, compiled), lines


def number_cases(runtime, arm):
    raw = bytearray(runtime.raw)
    offset = BUY_CALL - BASE
    assert raw[offset:offset + 4] == runtime.arm[offset:offset + 4]
    raw[offset:offset + 4] = arm[offset:offset + 4]
    cpus = native.get_machine(runtime.arm, runtime.raw)[0], native.get_machine(arm, bytes(raw))[0]
    initial = bytes(cpus[0].mem_read(RING, RING_SIZE))
    assert initial == bytes(cpus[1].mem_read(RING, RING_SIZE))
    audited = read(PRICE)
    assert all(sha256(runtime.arm[a:b]).hexdigest() == row["sha256"] for row in audited["source_clean_exact_spans"] for a, b in (row["span"],))
    bounds = audited["source_native_price_ranges"]
    minimum = min(r["buy_min"] for r in bounds)
    maximum = max(r["buy_max"] for r in bounds)
    assert (minimum, maximum) == (90, 420000)
    values = sorted({3000, 11000, 99, 100, 999, 1000, 9999, 10000, 99999, 100000}
                    | {r[key] for r in bounds for key in ("buy_min", "buy_max")})
    replacements = {}
    for index, value in enumerate(values):
        for cpu in cpus:
            cpu.mem_write(RING, initial[:8] + pack("<I", index % 32) + initial[12:])
        (old_ptr, previous), (new_ptr, installed) = (native.call_number(cpu, BUY_CALL, value) for cpu in cpus)
        assert new_ptr == old_ptr and normalize(previous) == installed == str(value).encode("ascii")
        old_ring, new_ring = (bytes(cpu.mem_read(RING, RING_SIZE)) for cpu in cpus)
        a, b = old_ptr - RING, old_ptr - RING + len(previous) + 1
        assert 12 <= a < b <= RING_SIZE and old_ring[:a] == new_ring[:a] and old_ring[b:] == new_ring[b:]
        replacements[value] = (previous, installed)
    return cpus[1], replacements, [minimum, maximum]


def exact_row(row):
    return text_reference(row) | {"exact_stored_hex": row.text.hex()}


def main():
    active = play.active
    release = read(active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    runtime = RegisteredRuntime(active.RELEASE, release["own_registered_startup"], captain=3)
    clean = NdsImage.open(CLEAN)
    original_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), original_arm)
    before = native.yard.common_rows(runtime.common, runtime.arm)
    arm, edits, pitch, pitch_lines = propose_arm9(original_arm, runtime.arm)
    assert active.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    payloads = {key: (b" " + english.encode("ascii")).ljust(len(before[key].text), b" ") for key, english in EDIT.items()}
    for key, data in payloads.items():
        assert len(data) == len(before[key].text) and b"\n" not in data and b"\0" not in data
        assert data.count(b"%s") == before[key].text.count(b"%s") == source[key].text.count(b"%s")
    common, after, allocations = owned_deployment(runtime.common, arm, before, payloads)
    assert [b.message_id for a, b in zip(before, after, strict=True) if a != b] == sorted(EDIT)

    cpu, numbers, bounds = number_cases(runtime, arm)
    layout = layout_function()
    previous_pitch = layout(cpu, pitch[1], PITCH_ID, ())
    revised_pitch = layout(cpu, pitch[2], PITCH_ID, ())
    assert previous_pitch["lines"] == ["You're in luck!", "This old map may lead", "to legendary treasure."]
    assert revised_pitch["lines"] == pitch_lines and not revised_pitch["findings"]
    previous_sale = layout(cpu, before[1084].text, 1084, ())
    revised_sale = layout(cpu, after[1084].text, 1084, ())
    assert previous_sale["lines"] == ["Hold on. You don't have", "anything to sell."]
    assert revised_sale["lines"] == [EDIT[1084]] and not revised_sale["findings"]
    layouts = {n: layout(cpu, after[1073].text, 1073, (compact,)) for n, (_, compact) in numbers.items()}
    assert all(row["lines"] == [EDIT[1073] % n] and not row["findings"] for n, row in layouts.items())
    prior_quotes = {n: layout(cpu, before[1073].text, 1073, (numbers[n][0],)) for n in (3000, 11000)}
    assert all(row["lines"][-1] == "to buy it?" for row in prior_quotes.values())

    raster, _, _ = native.portraits.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    pages = []
    for label, row in (("Old map pitch", revised_pitch), ("Nothing to sell", revised_sale),
                       *[(f"Buy quote {n}", layouts[n]) for n in (90, 3000, 11000, 420000)]):
        page = bytes.fromhex(row["formatted_hex"])
        plane, positions = native.portraits.render_portrait(raster, arm, kanji, page)
        assert all(0 <= item["x"] < 228 and 0 <= item["y"] < 48 for item in positions)
        pages.append((label, plane))

    source_row = dict(id="ARM9_GUILD_TREASURE_PITCH", file_path=ARM, speaker="Guildmaster", context=CONTEXT,
        source_meaning="The player is in luck. The Guildmaster has an old map said to show where a legendary treasure lies.",
        localization_note="Restore the Guildmaster's possession of the map and keep the claim as hearsay. The native literal profile packs the sentence into two complete rows.",
        english=PITCH_ENGLISH, clean_Japanese=pitch[0].decode("cp932"), previous_English=pitch[1].decode("ascii"),
        source_reference=dict(offset=PITCH, exact_hex=pitch[0].hex()), current_reference=dict(offset=PITCH, exact_hex=pitch[1].hex()),
        staged_reference=dict(offset=PITCH, exact_hex=pitch[2].hex()), decision="revision", review=dict.fromkeys(GATES, True))
    records = [source_row]
    notes = {
        1073: ("The Guildmaster gives the selected price and asks if the player will buy the item.",
               "The price and buy question stay together across the proven item-price range. Use the existing ordinary digits and preserve the original argument."),
        1084: ("The Guildmaster stops the player and says there is nothing eligible to sell.",
               "Wait keeps the interruption. Nothing to sell refers to this Guild list, and the complete reply fits a line."),
    }
    for key, english in EDIT.items():
        meaning, rationale = notes[key]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_ID=key, speaker="Guildmaster", context=CONTEXT,
            source_meaning=meaning, localization_note=rationale, english=english,
            clean_Japanese=source[key].text.decode("cp932"), previous_English=before[key].text.decode("ascii").strip(),
            source_reference=exact_row(source[key]), current_reference=exact_row(before[key]), staged_reference=exact_row(after[key]),
            decision="revision", review=dict.fromkeys(GATES, True)))
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                      review_gates=list(GATES), records=records)
    validate_natural_dialogue_batch(manuscript)

    image = NdsImage.open(active.ROM)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    staged = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release["candidate_sha256"]
    ROOT.mkdir()
    ROM.write_bytes(staged)
    final = NdsImage.open(ROM)
    assert final.read_file(ARM) == arm and final.read_file(COMMON) == common
    visual_root = OUT.with_suffix("")
    visual_root.mkdir(exist_ok=True)
    sheets = native.portraits.portrait_sheets(visual_root, pages)
    write(OUT, manuscript | dict(candidate=reference(ROM), predecessor=reference(active.ROM), clean_input=reference(CLEAN),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        whole_parent_inverse=True, exact_ARM9_edits=edits, allocations=allocations, price_domain=bounds,
        quote_cases=layouts, quote_before=prior_quotes, price_source=reference(PRICE), pitch_before=previous_pitch,
        pitch_after=revised_pitch, empty_sale_before=previous_sale, empty_sale_after=revised_sale, sheets=sheets,
        paired_ordinary_gameplay_pending=True, registered=False, new_editorial_credit=0))
    print(f"Staged three Guild display fixes after {len(layouts)} native buy quote checks. {digest(ROM)}")


if __name__ == "__main__":
    main()
