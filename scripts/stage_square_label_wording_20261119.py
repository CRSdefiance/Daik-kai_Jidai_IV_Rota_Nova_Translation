"""Source and native review for the Square's Seasonings and Textile Shop captions."""

from collections import defaultdict
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.commodity_source_repack import COUNT, TABLE as PRODUCT_NAMES
from dk4tool.patch.category_dialogue_lookup import BASE, OUTER, TABLE
from dk4tool.patch.main_pool_cache_visibility import cache_plan, target
from dk4tool.patch.square_caption_cells import assemble
from dk4tool.patch.square_font_scratch_20261027 import ENTRY as SQUARE_DRAW, OLD_BUFFER, stack_painter
from scripts import register_deck_comments_20261119 as parent
from scripts import register_square_shop_captions_20261115 as predecessor
from scripts import verify_square_shop_captions_20261115 as prior
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.probe_button_prompt_native import STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
ROOT = Path("work/square_label_wording_20261119/staged_v1")
ROM = ROOT / "Square_Label_Wording_STAGED.nds"
PROOF = ROOT / "staged.json"
SHEET = ROOT / "native_square_labels.png"
CALL, FORMAT_CALL, AFTER_FORMAT = 0x5FDA8, 0x5FDB8, 0x5FDBC
SCRATCH, SEASONINGS = 0x022A44EC, 0x0215A0A0
STUB = OLD_BUFFER
LIMIT = 0x01FFC200
WORDS = {1: "Seasonings", 8: "Textile Shop"}
NOTES = {
    1: "Seasonings names the broad family of ingredients, including salt, sugar, honey and cooking oils. The original Square menu supplies the retail context. The separate Spices Shop keeps pepper and similar goods distinct.",
    8: "Textile Shop is an idiomatic label for the trade in raw textile fiber and finished cloth. The original category includes both, so the caption keeps the broader textile trade in view.",
}


def former_scratch_references(image, objects):
    units = [(s.ramAddress, bytes(s.data)) for s in objects]
    units += [(s.ramAddress, bytes(s.data)) for s in loadOverlayTable(image.rom.arm9OverlayTable,
        lambda _, i: image.rom.files[i]).values()]
    literal, branch = [], []
    for origin, raw in units:
        for at in range(len(raw) - 3):
            word, = unpack_from("<I", raw, at)
            if STUB <= word < LIMIT:
                literal.append((origin+at, word))
            if at % 4 == 0 and word & 0x0E000000 == 0x0A000000 and word >> 28 != 15:
                displacement = word & 0xFFFFFF
                displacement -= 0x1000000 if displacement & 0x800000 else 0
                dest = origin + at + 8 + 4 * displacement
                if STUB <= dest < LIMIT:
                    branch.append((origin+at, dest))
    return literal, branch


def transform(image, arm):
    code = MainCodeFile(arm, BASE)
    saved = [(s.ramAddress, s.bssSize, bytes(s.data)) for s in code.sections]
    assert len(saved) == 6 and saved[4][:2] == (0x01FFC000, 0)
    main, itcm = code.sections[0].data, code.sections[4].data
    assert arm == bytes(code.save())
    first = STUB - code.sections[4].ramAddress
    bound = LIMIT - code.sections[4].ramAddress
    assert itcm[first:bound] == bytes(bound-first)
    existing_draw = stack_painter()
    assert itcm[SQUARE_DRAW-0x01FFC000:SQUARE_DRAW-0x01FFC000+len(existing_draw)] == existing_draw
    assert target(arm, CALL) == OUTER and target(arm, FORMAT_CALL) == BASE + 0xABFCC
    assert unpack_from("<I", arm, 0x5FDEC)[0] == SCRATCH
    assert arm[SEASONINGS-BASE:SEASONINGS-BASE+11] == b"Seasonings\0"
    assert former_scratch_references(image, code.sections) == ([], [])
    # Leave the old Square getter and its remaining format path in place.
    # Both revised captions still use the original copy into the same buffer.
    code_bytes = assemble(f"""
        cmp r0,#1
        ldreq r2,seasonings
        beq plain
        cmp r0,#8
        adreq r2,textile
        bne {OUTER}
    plain:
        ldr r0,scratch
        adr r1,format
        b {BASE+FORMAT_CALL}
    seasonings: .word {SEASONINGS}
    scratch: .word {SCRATCH}
    textile: .asciz "Textile Shop"
    format: .asciz "%s"
    .align 2
    """, STUB)
    assert len(code_bytes) <= LIMIT-STUB and b"Textile Shop\0%s\0" in code_bytes
    assert len(code_bytes) % 4 == 0
    itcm[first:first+len(code_bytes)] = code_bytes
    main[CALL:CALL+4] = assemble(f"bl {STUB}", BASE+CALL)
    after = bytes(code.save())
    assert target(after, CALL) == STUB
    assert cache_plan(arm) == cache_plan(after)
    assert arm[CALL+4:FORMAT_CALL+4] == after[CALL+4:FORMAT_CALL+4]
    main[CALL:CALL+4] = arm[CALL:CALL+4]
    itcm[first:first+len(code_bytes)] = bytes(len(code_bytes))
    assert bytes(code.save()) == arm
    assert [(s.ramAddress, s.bssSize, len(s.data)) for s in MainCodeFile(after, BASE).sections] == [
        (address, bss, len(data)) for address,bss,data in saved]
    return after, dict(original_call=BASE+CALL, caption_formatter=BASE+FORMAT_CALL,
        sole_original_call_change=[CALL, CALL+4], private_caption_selector=[STUB, STUB+len(code_bytes)],
        released_stack_painter_old_scratch=[STUB,LIMIT], original_square_painter_exact=True,
        all_absolute_aliases_and_aligned_arm_predecessor_branches_into_private_span=[],
        original_scratch_buffer=SCRATCH, staged_main_pool_and_section_extents_exact=True)


def run_caption(cpu, number):
    cpu.mem_write(SCRATCH-8, b"\xA5"*8 + bytes(12) + b"\xA5"*128)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_R0, number)
    cpu.emu_start(BASE+CALL, BASE+AFTER_FORMAT, count=100000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE+AFTER_FORMAT
    assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_R0) == SCRATCH+12
    assert bytes(cpu.mem_read(SCRATCH-8,8)) == b"\xA5"*8
    assert bytes(cpu.mem_read(SCRATCH+8,4)) == b"\x01\0\0\0"
    text, tail = bytes(cpu.mem_read(SCRATCH+12,128)).split(b"\0",1)
    assert tail == b"\xA5"*len(tail)
    return text.decode("ascii")


def source_inventory(runtime, ja):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    products = get(0xCB124) + 4
    assert ja[0x5FD9C:CALL] == runtime.arm[0x5FD9C:CALL]
    groups = defaultdict(list)
    for n in range(COUNT):
        field = PRODUCT_NAMES + n * 12
        old, = unpack_from("<I", ja, field)
        new, = unpack_from("<I", runtime.arm, field)
        obj = products + 16*n
        assert unpack_from("<I", cpu.mem_read(obj+4,4))[0] == new
        kind = cpu.mem_read(obj+12,1)[0]
        jp = ja[old-BASE:ja.index(0,old-BASE)+1]
        en = bytes(cpu.mem_read(new,64)).split(b"\0",1)[0]
        assert 0 <= kind < 18 and 1 < len(jp) < 64 and en.isascii()
        groups[kind].append(dict(product_ID=n, source_name_field_offset=field, source_name_offset=old-BASE,
            source_name_hex=jp.hex(), clean_Japanese=jp[:-1].decode("cp932"),
            registered_name_pointer=new, current_English=en.decode("ascii")))
    assert len(groups) == 18
    return groups


def verify_captions(ja, arm, after, inventory):
    old_cpu, new_cpu = map(prior.cpu_for, (arm, after))
    font = prior.GameAsciiFont.from_arm9(after)
    old_review = {r["category"]: r for r in base.load(predecessor.REVIEW)["records"]}
    assert len(old_review) == 18
    references, count = [], 0
    for return_pc in (*prior.UI_RETURNS, 0x0205FC48):
        for ident in (*range(18), -1, -2, -3, 18, 19, 255):
            a,b = (prior.getter(cpu, ident, return_pc) for cpu in (old_cpu,new_cpu))
            assert a == b
            if 0 <= ident < 18:
                assert prior.string(old_cpu,a) == prior.string(new_cpu,b)
            count += 1
    for ident in (*range(18,256), -1,-2,-3):
        assert prior.square_pointer(old_cpu, ident) == prior.square_pointer(new_cpu, ident)
    sheet = Image.new("RGB",(768,252),"#263238")
    draw = ImageDraw.Draw(sheet)
    for n in range(18):
        row = old_review[n]
        before, installed = (run_caption(cpu,n) for cpu in (old_cpu,new_cpu))
        assert before == row["english"] and installed == WORDS.get(n,before)
        old_pixels, old_context, _ = prior.native(arm,before)
        pixels, context, _ = prior.native(after,installed)
        expected = prior.expected_pixels(font,installed)
        assert all(0 <= x < 64 and 0 <= y < 12 for x,y in expected)
        assert pixels == bytes(int((i%64,i//64) in expected) for i in range(768))
        if before == installed:
            assert old_pixels == pixels and old_context == context
        source = row["source_reference"]
        index, length = source["string_offset"], len(bytes.fromhex(source["category_hex"]))
        assert ja[index:index+length].hex() == source["category_hex"]
        assert unpack_from("<I",ja,TABLE+4*n)[0] == BASE+index
        assert row["review"] == dict.fromkeys(prior.GATES,True)
        row.update(previous=before, english=installed, decision="revision" if n in WORDS else "retention",
            localization_note=NOTES.get(n,row["localization_note"]), clean_and_current_category_stock=inventory[n],
            previous_consumer=row["current_reference"],
            current_reference=dict(file_path=ARM, native_call=BASE+CALL, formatter=BASE+FORMAT_CALL,
                category=n, output_hex=installed.encode("ascii").hex(),
                linked_old_category_getter=OUTER, local_complete_caption_dispatch=n in WORDS),
            native_display=dict(single_line=True, width=64, height=12, native_plane_hex=pixels.hex(),
                ink_pixels=len(expected), complete_leading_trailing_characters=True, ink_rightmost_x=max(x for x,_ in expected)))
        img = Image.frombytes("L",(64,12),bytes(p*230 for p in pixels))
        x,y = (n%3)*256,(n//3)*42
        draw.text((x+4,y+10),f"{n:02d}",fill="white")
        sheet.paste(img.resize((192,36),Image.Resampling.NEAREST),(x+39,y+3))
        references.append(row)
    assert all(max(x for x,_ in prior.expected_pixels(font,text)) >= 64
               for text in ("Seasonings Shop","Seasoning Shop","Precious Metals Shop"))
    sheet.save(SHEET)
    return references, count


def main():
    assert not ROOT.exists()
    release, ledger = map(base.load, (parent.RELEASE, base.LEDGER))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    original = base.NdsImage.open(CLEAN).read_file(ARM)
    runtime = RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    image = runtime.image
    after, allocation = transform(image,runtime.arm)
    verify_runtime(after,release)
    ROOT.mkdir(parents=True)
    records, count = verify_captions(original,runtime.arm,after,source_inventory(runtime,original))
    image.replace_file(ARM,after)
    target_image = bytes(image.rom.save())
    ROM.write_bytes(target_image)
    image.replace_file(ARM,runtime.arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(prior.GATES), candidate_sha256=base.digest(ROM), records=records)
    validate_natural_dialogue_batch(review)
    base.save(PROOF, review | dict(parent_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        entire_parent_inverse=True, target_ARM9_sha256=native.digest(after), allocation=allocation,
        preserved_other_category_cases=count, preserved_square_fallbacks=241, visually_reviewed_pending=True,
        sheets=[dict(path=str(SHEET),sha256=base.digest(SHEET))],
        source_proofs={str(p):base.digest(p) for p in (parent.RELEASE, predecessor.REVIEW,Path(__file__))}))
    print("Reviewed 18 Square captions and all 124 sourced trade goods. Both revised labels fit the original draw.")


if __name__ == "__main__":
    main()
