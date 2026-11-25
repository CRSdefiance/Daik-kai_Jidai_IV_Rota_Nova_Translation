"""Use regular digits in the original Search supply and fatigue results."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from scripts import register_power_and_gold_digits_20261121 as parent
from scripts import stage_victory_reward_digits_20261121 as common
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.stage_ship_emergency_review_v1 import with_arguments
from scripts.verify_personal_gameplay_v841 import get_machine


base, shared, number = parent.base, parent.shared, common.number
ROOT = Path("work/search_supply_and_fatigue_digits_20261121")
ROM, PROOF = ROOT / "Search_Supply_And_Fatigue_Digits_STAGED.nds", ROOT / "staged.json"
FATIGUE = Path("translations/fatigue_status_contextual_final_review_v1.json")
FORAGE = Path("translations/search_reports_contextual_final_review_v1.json")
FATIGUE_SOURCE = Path("work/analysis/fatigue_status_source_v1587/source_amounts_and_original_expedition_context.json")
CALLS = (0x02079768, 0x02079784, 0x02079F3C, 0x02079F48, 0x02079FAC)
OWNED = ((0x79728, 0x797A0), (0x79EEC, 0x79FCC), (0x79FF8, 0x7A000), (0x116E80, 0x116EA0))
TABLE, ROLE = 0x02116E80, 7
FORAGE_IDS = range(2229, 2234)
NOTES = {
    308: "Keep the requested fatigue increase and its direction. Search failure can request three even near the cap.",
    309: "Keep the requested fatigue reduction even when the stored fatigue reaches zero.",
    2229: "Keep the matter-of-fact expedition report and name both barrel counts, water first.",
    2230: "Keep the familiar voice’s upbeat exclamation and both quantities.",
    2231: "Keep the short, emphatic discovery report with water before food.",
    2232: "The contraction brings out this voice’s direct report and leaves both counts clear.",
    2233: "Keep the younger voice’s inclusive “found us” and the source order of supplies.",
}


def patch(arm, clean):
    for lo, hi in OWNED:
        assert arm[lo:hi] == clean[lo:hi]
    assert unpack_from("<I", arm, 0x79FF8) == (TABLE,)
    assert unpack_from("<I", arm, 0x7979C) == (309,)
    assert unpack_from("<8i", arm, TABLE - number.BASE) == (2229, -1, 2230, -1, 2231, 2232, 2233, -1)
    itcm = next(s for s in MainCodeFile(arm, number.BASE).sections if s.ramAddress == number.ITCM)
    helper = bytes(itcm.data[number.HELPER - number.ITCM:number.END - number.ITCM])
    assert helper.hex() == base.load(common.HELPER_PROOF)["helper_hex"]
    # The two values in r5/r6 are passed to both the role portrait and the original supply update.
    assert unpack_from("<4I", arm, 0x79F64)[:3] == (0xE1A01005, 0xE1A02006, 0xE3A03001)
    assert number.target(arm, 0x79F5C) == 0x02053D44 and number.target(arm, 0x79F70) == 0x02034C98
    revised, bindings = bytearray(arm), []
    for pc in CALLS:
        at = pc - number.BASE
        assert number.target(arm, at) == number.NUMBER
        replacement = number.assemble(f"bl {number.HELPER:#x}", pc)
        assert len(replacement) == 4
        revised[at:at + 4] = replacement
        bindings.append(dict(address=pc, original_hex=arm[at:at + 4].hex(), revised_hex=replacement.hex()))
    target = bytes(revised)
    for row in bindings:
        at = row["address"] - number.BASE
        assert number.target(target, at) == number.HELPER
        revised[at:at + 4] = bytes.fromhex(row["original_hex"])
    assert bytes(revised) == arm and number.cache_plan(target) == number.cache_plan(arm)
    return target, bindings


def review_rows(jp, en):
    earlier = {r["message_id"]: r for path in (FATIGUE, FORAGE) for r in base.load(path)["records"]}
    rows = {}
    for n, reason in NOTES.items():
        source, current, row = jp[n], en[n], earlier[n]
        english = current.text.decode("ascii")
        count = 2 if n in FORAGE_IDS else 1
        assert source.text.count(b"%s") == current.text.count(b"%s") == count
        assert source.text.hex() == row["source_hex"] and english == row["english"]
        if count == 2:
            assert source.text.decode("cp932").index("水") < source.text.decode("cp932").index("食料")
        rows[n] = dict(id=f"COMMON_MESSAGE_{n}", file_path=shared.COMMON, message_ID=n,
                      speaker="Original Lookout voice" if count == 2 else "System",
                      context=row["context"], source_meaning=row["source_meaning"], clean_Japanese=source.text.decode("cp932"),
                      source_reference=shared.workflow.reference(source), current_reference=shared.workflow.reference(current),
                      source_hex=source.text.hex(), current_hex=current.text.hex(), english=english, decision="retention",
                      localization_note=reason, original_substitution_count=count, text_display_fix="ascii_decimal_digits",
                      review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True))
    return rows


def verify_native(ctx, changed, entries, rows):
    old_cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    new_cpu, _, _ = changed.machine(changed.arm, ctx.common, changed.raw, changed.plan)
    values = (0, 1, 3, 5, 10, 15, 99, 100, 105, 3875, 4650, 2147483647)
    check = FunctionType(common.prior.verify_numbers.__code__, common.prior.verify_numbers.__globals__ |
                         {"CASES": dict.fromkeys(CALLS, values)})
    allocation = check(old_cpu, new_cpu)
    assert len(allocation) == len(CALLS) * len(values) * 32
    cpu, get = get_machine(ctx.arm, ctx.raw)
    actors = {}
    for actor in range(207):
        pointer = ctx.actor_root + 4 + actor * 32
        n = get(0x53F4C, pointer, TABLE)
        if n in FORAGE_IDS:
            actors.setdefault(n, actor)
    assert set(actors) == set(FORAGE_IDS)
    assert get(0x53F4C, ctx.actor_root + 4 + 32 * 18, TABLE) == 2229
    actors[2229] = 18
    assert all(actor != 3 for actor in actors.values())
    raster, _, font = common.discovery.mixed.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    modal, portrait = common.discovery.native_reader(), with_arguments()
    cases, previews = [], []
    for n, row in rows.items():
        stored = entries[n].text
        amounts = ((0, 0), (5, 10), (105, 105), (4650, 3875), (20, 1500), (3900, 40)) if n in FORAGE_IDS else (
            (3,), (5,), (10,), (15,), (100,))
        for sample in amounts:
            args = tuple(str(value).encode("ascii") for value in sample)
            expanded = stored % args
            if n in FORAGE_IDS:
                group = dict(consumer=0x02053D44, table=TABLE, original_role_argument=ROLE)
                result = portrait(changed, row, group, stored, actors[n], args)
                formatted = result.pop("display")
                pixels, glyphs = render_portrait(raster, changed.arm, kanji, formatted)
                lines = [line.strip().decode("ascii") for line in formatted.splitlines()]
            else:
                result = modal(changed, row | {"current_copies": [{"wrapper": common.prior.WRAPPER}]},
                               tuple(value.decode("ascii") for value in args))
                formatted = bytes.fromhex(result["native_wrapper_output_hex"])
                pixels, glyphs = common.discovery.mixed.render(raster, changed.arm, kanji, formatted)
                lines = [formatted.decode("ascii")]
            changed.calls.clear()
            assert b" ".join(formatted.split()) == expanded and formatted.isascii()
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (expanded[0], expanded[-1])
            if n in FORAGE_IDS:
                assert len(lines) <= 4 and all(0 < len(line) <= 35 for line in lines)
            else:
                assert b"\n" not in formatted
            cases.append(dict(message_ID=n, amounts=sample, formatted_hex=formatted.hex(), lines=lines,
                              glyphs=len(glyphs), first_and_last_complete=True, pages=1,
                              ink_sha256=sha256(pixels).hexdigest()))
            padded = pixels.ljust(228 * 64, b"\0")
            previews.append((f"{n} {' / '.join(map(str, sample))}", padded))
    return allocation, cases, previews, font


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    ctx = common.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(shared.CLEAN)
    clean_arm = clean.read_file(shared.ARM)
    arm, bindings = patch(ctx.arm, clean_arm)
    changed = common.discovery.with_components(ctx, arm, ctx.common)
    for pc in CALLS:
        at = pc - number.BASE
        changed.raw = changed.raw[:at] + arm[at:at + 4] + changed.raw[at + 4:]
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), clean_arm)
    installed = shared.entries(ctx.image)
    rows = review_rows(source, installed)
    numbers, cases, previews, font = verify_native(ctx, changed, installed, rows)
    review = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
                  review_gates=sorted(REQUIRED_REVIEW_GATES), records=list(rows.values()))
    validate_natural_dialogue_batch(review)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(shared.ARM, arm)
    binary = bytes(image.rom.save())
    image.replace_file(shared.ARM, ctx.arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    base.save(PROOF, review | dict(candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=release["target_COMMON_sha256"],
        exact_parent_inverse=True, original_call_bindings=bindings, native_display_cases=cases,
        native_number_checks=numbers, font=font, sheets=portrait_sheets(ROOT, previews),
        water_then_food=True, emulator_and_visual_gate_pending=True,
        source_evidence={str(p): base.digest(p) for p in (parent.RELEASE, FATIGUE_SOURCE, FATIGUE, FORAGE)}))
    print(f"Verified {len(numbers)} allocation cases and {len(cases)} complete Search results.")


if __name__ == "__main__":
    main()
