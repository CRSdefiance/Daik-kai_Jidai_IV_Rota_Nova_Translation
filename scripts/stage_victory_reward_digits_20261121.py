"""Use the regular English digits in the three original victory reward notices."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from ndspy.code import MainCodeFile

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.patch import inn_numerals_20261119 as number
from scripts import check_departure_numerals_native_20261119 as prior
from scripts import reconcile_shared_display_20261121 as shared
from scripts import register_clifford_declaration_wrap_20261121 as parent
from scripts import stage_discovery_rewards_v1 as discovery
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_madeira_resupply_numerals_20261120 import HELPER_PROOF


base, native = parent.base, parent.native
ROOT = Path("work/victory_reward_digits_20261121")
ROM, PROOF = ROOT / "Victory_Reward_Digits_STAGED.nds", ROOT / "staged.json"
ORIGINAL = Path("releases/all_routes_editorial_20261111_discovery_rewards_candidate/verification/registered_review.json")
BASE = number.BASE
GROUPS = {
    301: ((0x020722AC,), 0x020722B8, 0x7235C),
    303: ((0x020721A0, 0x020721AC), 0x020721BC, 0x72350),
    305: ((0x0207230C,), 0x02072318, 0x72364),
}
SAMPLES = {
    301: ((1,), (6055,), (2147483647,)),
    303: ((20, 29), (109, 103), (1000, 20), (20, 1000), (2147483647, 2147483647)),
    305: ((1,), (400,), (2147483647,)),
}
REASONS = {
    301: "Keep the recovered gold distinct from the later national award. 'Captured ships' identifies the source without specifying a count.",
    303: "Keep the source heading and one row per resource. Read the food and water totals in that order, with barrels explicit for both.",
    305: "Keep the nation as the source of this separate award and use the same gold term as the capture notice.",
}


def patch(arm, clean):
    for lo, hi in ((0x72174, 0x72368), (0xABF50, 0xABFD0)):
        assert arm[lo:hi] == clean[lo:hi]
    itcm = next(section for section in MainCodeFile(arm, BASE).sections if section.ramAddress == number.ITCM)
    helper = itcm.data[number.HELPER - number.ITCM:number.END - number.ITCM]
    assert helper.hex() == base.load(HELPER_PROOF)["helper_hex"]
    revised = bytearray(arm)
    bindings = []
    for n, (calls, notice, key_offset) in GROUPS.items():
        assert unpack_from("<I", arm, key_offset) == (n,)
        assert number.target(arm, notice - BASE) == prior.WRAPPER
        for pc in calls:
            assert number.target(arm, pc - BASE) == number.NUMBER
            at = pc - BASE
            before = arm[at:at + 4]
            after = number.assemble(f"bl {number.HELPER:#x}", pc)
            assert len(after) == 4
            revised[at:at + 4] = after
            bindings.append(dict(message_ID=n, number_call=pc, original_hex=before.hex(),
                                 revised_hex=after.hex(), modal_call=notice, key_address=key_offset + BASE))
    target = bytes(revised)
    for binding in bindings:
        at = binding["number_call"] - BASE
        assert number.target(target, at) == number.HELPER
        revised[at:at + 4] = bytes.fromhex(binding["original_hex"])
    assert bytes(revised) == arm and number.cache_plan(arm) == number.cache_plan(target)
    return target, bindings


def main():
    assert not ROOT.exists()
    previous, registered = map(base.load, (parent.RELEASE, ORIGINAL))
    assert base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(shared.CLEAN) == previous["clean_input_sha256"]
    ctx = RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"], captain=3)
    jp = base.NdsImage.open(shared.CLEAN)
    clean_arm = jp.read_file(shared.ARM)
    arm, common = ctx.arm, ctx.common
    new_arm, calls = patch(arm, clean_arm)
    target = discovery.with_components(ctx, new_arm, common)
    for call in calls:
        at = call["number_call"] - BASE
        target.raw = target.raw[:at] + new_arm[at:at + 4] + target.raw[at + 4:]
    old_cpu, _, _ = ctx.machine(arm, common, ctx.raw, ctx.plan)
    new_cpu, _, _ = target.machine(new_arm, common, target.raw, target.plan)
    values = (0, 1, 9, 10, 20, 29, 99, 100, 103, 109, 999, 1000, 6055, 2147483647)
    check_numbers = FunctionType(prior.verify_numbers.__code__, prior.verify_numbers.__globals__ |
                                 {"CASES": {binding["number_call"]: values for binding in calls}})
    allocations = check_numbers(old_cpu, new_cpu)
    assert len(allocations) == len(calls) * 32 * len(values)

    sources = shared.workflow.common_message_entries(jp.read_file(shared.COMMON), clean_arm)
    current = shared.entries(ctx.image)
    old_review = {r["message_ID"]: r for r in registered["records"]}
    raster, _, font = discovery.mixed.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    run = discovery.native_reader()
    records, cases, planes = [], [], []
    for n, choices in SAMPLES.items():
        source, installed = sources[n], current[n]
        prev = old_review[n]
        english = " ".join(installed.text.decode("ascii").split())
        assert prev["english"] == english and prev["source_hex"] == source.text.hex()
        assert prev["native_substitution_count"] == source.text.count(b"%s") == installed.text.count(b"%s")
        row = dict(id=f"COMMON_MESSAGE_{n}", file_path=shared.COMMON, message_ID=n, speaker="System",
                   source_reference=shared.workflow.reference(source), current_reference=shared.workflow.reference(installed),
                   source_hex=source.text.hex(), current_hex=installed.text.hex(), clean_Japanese=source.text.decode("cp932"),
                   english=english, decision="retention", text_display_fix="ascii_decimal_digits",
                   context=prev["context"], source_meaning=prev["source_meaning"], localization_note=REASONS[n],
                   original_substitution_count=prev["native_substitution_count"],
                   review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True))
        records.append(row)
        for amounts in choices:
            args = tuple(str(v) for v in amounts)
            markup = row | dict(english=installed.text.decode("ascii").replace("\n", "{LB}"),
                                 current_copies=[dict(wrapper=prior.WRAPPER)])
            result = run(target, markup, args)
            target.calls.clear()
            formatted = bytes.fromhex(result["native_wrapper_output_hex"])
            assert formatted.isascii() and b" ".join(formatted.split()).decode() == english % args
            pixels, glyphs = discovery.mixed.render(raster, new_arm, kanji, formatted)
            assert glyphs[0]["code"] == ord(english[0]) and glyphs[-1]["code"] == ord(english[-1])
            assert formatted.count(b"\n") <= 2 and all(g["code"] < 128 for g in glyphs)
            if n == 303:
                assert formatted.count(b"\n") == 2
            lines = [line.strip().decode("ascii") for line in formatted.splitlines()]
            cases.append(result | dict(lines=lines, pages=1, ink_sha256=sha256(pixels).hexdigest()))
            planes.append(pixels)

    verified = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                    target_locale="en-US", review_gates=sorted(REQUIRED_REVIEW_GATES), records=records)
    validate_natural_dialogue_batch(verified)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(shared.ARM, new_arm)
    binary = bytes(image.rom.save())
    image.replace_file(shared.ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    sheets = FunctionType(discovery.save_sheets.__code__, discovery.save_sheets.__globals__ | {"ROOT": ROOT})
    base.save(PROOF, verified | dict(candidate_sha256=base.digest(ROM), parent_sha256=previous["candidate_sha256"],
        target_ARM9_sha256=native.digest(new_arm), target_COMMON_sha256=previous["target_COMMON_sha256"],
        original_call_bindings=calls, exact_parent_inverse=True, native_number_checks=allocations,
        native_display_cases=cases, font=font, sheets=sheets(cases, planes), emulator_and_visual_gate_pending=True,
        evidence={str(p): base.digest(p) for p in (parent.RELEASE, ORIGINAL, HELPER_PROOF)}))
    print(f"Verified {len(allocations)} ring-slot checks and {len(cases)} complete victory reward pages.")


if __name__ == "__main__":
    main()
