"""Verify Yard numeric substitutions, ring storage, and complete native pages."""

from inspect import getsource
from itertools import product
from struct import pack, unpack_from

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_SP

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_shipyard_runtime_v759 as formatters
from scripts import stage_recruit_crew_20261120 as portraits
from scripts import stage_yard_numerals_20261124 as stage
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_inn_numerals_native_20261119 import RING, RING_SIZE, normalize, read_cstring
from scripts.verify_personal_gameplay_v841 import get_machine


patch, yard = stage.patch, stage.yard
BASE, STACK = patch.BASE, formatters.STACK
OUT = stage.ROOT / "native_yard_numerals.json"
REFIT_QUOTE, REFUND_PARENT, REFUND_ID = 1246, 0x02054048, 0xFFFFFFFF
CALLEE = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
AMOUNTS = (*range(11), 30, 50, 99, 100, 123, 255, 999, 1000, 1880, 7500, 50000, 65535, 1000000, 2147483647)
FORMATTING_OWNERS = {
    786: "The Shipwright reports the selected ship's mast count and hull durability before purchase confirmation.",
    789: "The Shipwright makes an offer for the selected ship and waits for a decision.",
    798: "A crew member offers to help. The Shipwright quotes the resulting repair discount as a percentage.",
    799: "The Shipwright explains that funds do not cover the quoted repair price.",
    800: "The Shipwright quotes the price for repairs and waits for confirmation.",
    802: "The Shipwright offers full repairs at the quoted price and asks whether to proceed.",
    803: "Duplicating a ship's design takes the quoted price and the stated number of days.",
    804: "The requested design needs no remodeling. The Shipwright asks the player to confirm the purchase price.",
    1245: "The amount is stated before refusing a special build or equipment work for lack of funds.",
    1246: "The Shipwright quotes the equipment cost in gold before the player confirms.",
    1263: "The Shipwright states the helper's discount and starts calculating the refit cost.",
    1267: "After confirmation, the Shipwright gives the time needed to finish the refit.",
    patch.REFUND: "Removing equipment returns the exact displayed amount in coins.",
}


def call_number(cpu, address, value):
    marks = tuple(0x76543000 + i for i in range(len(CALLEE)))
    for register, marker in zip(CALLEE, marks, strict=True):
        cpu.reg_write(register, marker)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R0, value)
    cpu.emu_start(address, address + 4, count=3000)
    assert cpu.reg_read(UC_ARM_REG_PC) == address + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert tuple(cpu.reg_read(register) for register in CALLEE) == marks
    pointer = cpu.reg_read(UC_ARM_REG_R0)
    return pointer, read_cstring(cpu, pointer)


def quantity_census(ctx, arm, stored):
    raw = bytearray(ctx.raw)
    for span in stored["instruction_changes"]:
        address = span["address"] - BASE
        old, new = bytes.fromhex(span["before_hex"]), bytes.fromhex(span["after_hex"])
        assert ctx.arm[address:address + 4] == raw[address:address + 4] == old and arm[address:address + 4] == new
        raw[address:address + 4] = new
    cpus = (get_machine(ctx.arm, ctx.raw)[0], get_machine(arm, bytes(raw))[0])
    initial = bytes(cpus[0].mem_read(RING, RING_SIZE))
    assert bytes(cpus[1].mem_read(RING, RING_SIZE)) == initial and unpack_from("<I", arm, 0xABFC0)[0] == RING
    native, rows = {}, []
    sites = patch.BARE_CALLS | patch.SUFFIX_CALLS
    for address, key in sorted(sites.items()):
        duration = address in patch.DURATION_CALLS
        suffix = address in patch.SUFFIX_CALLS
        amounts = range(256) if duration else (*AMOUNTS, *([1, 10, 7500, 30, 65535, 50, 2147483647] * 2))
        cases = []
        for index, value in enumerate(amounts):
            slot = index % 32
            for cpu in cpus:
                cpu.mem_write(RING, initial[:8] + pack("<I", slot) + initial[12:])
            (old_at, previous), (new_at, current) = (call_number(cpu, address, value) for cpu in cpus)
            unit = (" day" if value == 1 else " days") if duration else (" gold coin" if value == 1 else " gold coins")
            expected = (str(value) + (unit if suffix else "")).encode("ascii")
            assert old_at == new_at and normalize(previous) == current == expected
            limit = RING + 12 + 128 * (slot + 1)
            assert limit - 128 <= new_at and new_at + len(previous) < limit
            old_ring, new_ring = (bytes(cpu.mem_read(RING, RING_SIZE)) for cpu in cpus)
            lower, upper = new_at - RING, new_at - RING + len(previous) + 1
            assert old_ring[:lower] == new_ring[:lower] and old_ring[upper:] == new_ring[upper:]
            native[address, value] = current
            if index < len(AMOUNTS) or duration:
                cases.append(dict(value=value, ring_slot=slot, original_hex=previous.hex(), compact_hex=current.hex()))
        rows.append(dict(call=address, message_ID=key, ring_slots=32, cases=len(amounts), transitions=cases,
            protected_buffer_outside_original_payload_unchanged=True, return_pointer_and_callee_saved_registers_match=True))
    return cpus[1], native, rows


def layout_function():
    source = checked_text(getsource(formatters.layout), {
        '    assert bytes(u.mem_read(output, len(expected) + 1))': '    expected = expected.replace(b"%%", b"%")\n    assert bytes(u.mem_read(output, len(expected) + 1))',
        'else 0x02053FCC if n in YESNO else 0x02054014': 'else 0x02053FCC if n in YESNO or n == REFIT_QUOTE else REFUND_PARENT if n == REFUND_ID else 0x02054014',
    })
    scope = vars(formatters) | dict(REFIT_QUOTE=REFIT_QUOTE, REFUND_PARENT=REFUND_PARENT, REFUND_ID=REFUND_ID)
    exec(compile(source, __file__ + "::exact-percent-and-literal-wrapper", "exec"), scope)
    return scope["layout"]


def form_cases(native):
    many = (1, 9, 99, 1000, 7500, 65535, 1000000, 2147483647)
    readers = {key: site for site, key in (patch.BARE_CALLS | patch.SUFFIX_CALLS).items() if key not in (786, 803)}
    forms = {key: [(native[site, value],) for value in many] for key, site in readers.items() if key not in (798, 1263, 1267)}
    forms[786] = [(native[0x0206347C, masts], native[0x0206348C, hull])
                  for masts, hull in product((0, 1, 3), (0, 30, 99, 255, 65535))]
    for key in (798, 1263):
        forms[key] = [(native[readers[key], value],) for value in (1, 9, 30, 50)]
    forms[1267] = [(native[readers[1267], value],) for value in (0, 1, 2, 99, 255)]
    names = ("Chun", *formatters.NAMES)
    forms[803] = [(name.encode("ascii"), native[0x02063174, price], native[0x02063180, day])
                  for name, price, day in product(names, (1, 7500, 2147483647), (1, 2, 16))]
    forms[804] = [(name.encode("ascii"), native[0x02063140, price]) for name, price in product(names, (1, 7500, 2147483647))]
    assert set(forms) == set(FORMATTING_OWNERS)
    return forms


def check_pages(ctx, image, target, cpu, forms):
    fmt = layout_function()
    source_image = NdsImage.open(CLEAN)
    original_arm = source_image.read_file(stage.ARM)
    source = yard.common_message_entries(source_image.read_file(stage.COMMON), original_arm)
    common = yard.common_rows(ctx.common, ctx.arm)
    raster, _, _ = portraits.font_tools(image)
    kanji = image.read_file("/GRP/KANJI.FNT")
    rows, pages = [], []
    live_english = dict(stage.LIVE.values())
    for key, inputs in forms.items():
        if key == patch.REFUND:
            label = REFUND_ID
            source_at, installed_at = (unpack_from("<I", arm, 0x17FA0)[0] - BASE for arm in (original_arm, target))
            prior_literal = original_arm[source_at:source_at + 80].split(b"\0")[0]
            template = target[installed_at:installed_at + 80].split(b"\0")[0]
            assert prior_literal.count(b"%s") == template.count(b"%s") == 1 and template == b"Refund %s coins."
            source_ref = dict(offset=source_at, exact_hex=prior_literal.hex())
            installed_ref = dict(offset=installed_at, exact_hex=template.hex())
        else:
            label = key
            prior_literal, template = source[key].text, common[key].text
            assert prior_literal.count(b"%s") == template.count(b"%s") == len(inputs[0])
            source_ref, installed_ref = map(yard.panels.text_reference, (source[key], common[key]))
        context = FORMATTING_OWNERS[key]
        cases, sample_cases = [], []
        for args in inputs:
            result = fmt(cpu, template, label, args)
            assert not (set(result["findings"]) & {"four_row_whole_word_bound"}), (key, result)
            assert all(result["lines"]) and result["lines"][-1][-1] in ".?", (key, result)
            formatted = bytes.fromhex(result["formatted_hex"])
            assert formatted.isascii() and b"%s" not in formatted
            cases.append(result)
            if result["lines"] == [live_english.get(key)]:
                sample_cases.append(result)
        widest = max(cases, key=lambda row: (len(row["lines"]), sum(map(len, row["lines"])), max(map(len, row["lines"]))))
        visible = [widest, *(r for r in sample_cases if r != widest)]
        for result in visible:
            formatted = bytes.fromhex(result["formatted_hex"])
            plane, events = portraits.render_portrait(raster, target, kanji, formatted)
            codes = [glyph["code"] for glyph in events]
            assert codes == portraits.glyph_codes(formatted)
            assert codes[0] == ord(result["lines"][0][0]) and codes[-1] == ord(result["lines"][-1][-1])
            result["complete_native_plane_sha256"] = sha256(bytes(plane)).hexdigest()
            pages.append((f"{key} / {' '.join(bytes.fromhex(arg).decode('ascii') for arg in result['values_hex'])}", plane))
        if key in live_english:
            assert len(sample_cases) == 1
        rows.append(dict(id=f"COMMON_MESSAGE_{key}" if isinstance(key, int) else key, message_ID=key,
            file_path=stage.COMMON if isinstance(key, int) else stage.ARM, speaker="Shipwright", context=context,
            source_meaning=context, english=template.decode("ascii").strip(), clean_Japanese=prior_literal.decode("cp932"),
            source_reference=source_ref, current_reference=installed_ref, registered_reference=installed_ref, decision="retention",
            localization_note="Keep the existing wording and all numeric values, units, argument order, and interaction prompts. The digits use the same narrower glyphs as the adjacent English.",
            review=dict.fromkeys(GATES, True), native_argument_cases=len(cases), longest_checked=widest, ordinary_amount_fixtures=sample_cases,
            review_flags=sorted({finding for r in cases for finding in r["findings"]})))
    return rows, portraits.portrait_sheets(stage.ROOT, pages)


def main():
    release, staged = map(read, (stage.parent.RELEASE, stage.STORED))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(stage.ROM) == staged["candidate"]["sha256"] and staged["previous"]["sha256"] == release["candidate_sha256"]
    ctx = RegisteredRuntime(stage.parent.RELEASE, release["own_registered_startup"], captain=3)
    image = NdsImage.open(stage.ROM)
    arm, common = [image.read_file(path) for path in (stage.ARM, stage.COMMON)]
    assert common == ctx.common and sha256(arm).hexdigest() == staged["target_ARM9_sha256"]
    cpu, native, numbers = quantity_census(ctx, arm, staged)
    records, sheets = check_pages(ctx, image, arm, cpu, form_cases(native))
    policy = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=records)
    validate_natural_dialogue_batch(policy)
    write(OUT, policy | dict(candidate_sha256=staged["candidate"]["sha256"], predecessor_sha256=release["candidate_sha256"],
        patch_input=reference(stage.STORED), number_callers=numbers, unique_number_cases=sum(row["cases"] for row in numbers),
        layout_cases=sum(row["native_argument_cases"] for row in records), sheets=sheets, ordinary_gameplay=False,
        native_input=ctx.receipt() | {"captain": 3}, sources=list(map(reference, (stage.parent.RELEASE, yard.OUT)))))
    print(f"Verified {len(numbers)} numeric call sites and {sum(row['native_argument_cases'] for row in records)} guarded text layouts.")


if __name__ == "__main__":
    main()
