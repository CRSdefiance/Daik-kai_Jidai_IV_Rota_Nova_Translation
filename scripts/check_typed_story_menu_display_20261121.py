"""Run the stored story choices through the native VM and caption painter."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace
import traceback

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE

from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from scripts import checkpoint_typed_story_text_20261121 as scout
from scripts import check_editorial_three_choice_display as precedent
from scripts import native_menu_backing_surface_v4080 as backing
from scripts import verify_ship_advice_choice_centering_20261022 as original
from scripts.source_locked_derivation_v5118 import checked_text


base, native, current = scout.base, scout.native, scout.current
ROOT = Path("work/typed_story_menu_display_20261121")
PROOF = ROOT / "native_menu_results.json"


def adapters(arm):
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data[:-48])
    assert len(payload) == 123264
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=payload)]
    executed = set()

    def machine(value):
        assert value == arm
        cpu = original.machine(value)

        def exact(u, pc, size, _):
            owner, = [s for s in owners if s.ramAddress <= pc and pc + size <= s.ramAddress + len(s.data)]
            index = pc - owner.ramAddress
            assert bytes(u.mem_read(pc, size)) == bytes(owner.data[index:index + size]), hex(pc)
            executed.add(pc)

        cpu.hook_add(UC_HOOK_CODE, exact)
        return cpu

    vm_source = base.load(precedent.PRECEDENT)["source_owned_VM_adapter"]
    vm_source = checked_text(vm_source, {
        "    assert alignment in [0,2];text+=alignment": (
            "    assert alignment in [0,2];text+=alignment\n"
            "    guard_size = len(object_bytes) + 32\n"
            "    label_length = max(map(len, object_labels(object_bytes))) + 1"
        ),
        r"b'\xA5' * 96": r"b'\xA5' * guard_size",
        "cpu.mem_read(text - 16, 96)": "cpu.mem_read(text - 16, guard_size)",
        "cpu.mem_read(pointer, 32)": "cpu.mem_read(pointer, label_length)",
    })
    vm_three = checked_text(vm_source, {
        "cpu.reg_read(UC_ARM_REG_R0) == 2": "cpu.reg_read(UC_ARM_REG_R0) == 3",
        "for index in (0, 1):": "for index in range(3):",
        "(rect, provider, maximum, 2)": "(rect, provider, maximum, 3)",
        "for selected in (0, 1, -1):": "for selected in (0, 1, 2, -1):",
    })
    proof_three = base.load(precedent.THREE_PRECEDENT)["source_derived_three_option_VM_adapter"]
    assert "for selected in (0, 1, 2, -1):" in proof_three
    vms = {}
    for count, source in ((2, vm_source), (3, vm_three)):
        namespace = vars(original) | {"machine": machine, "object_labels": labels}
        exec(compile(source, f"{__file__}::native-{count}-choice", "exec"), namespace)
        vms[count] = namespace["choice_vm"]

    paint_source = checked_text(getsource(backing.paint), {
        "'expected[(y+yy)*backing_width+x+index*6+xx]'": "'expected[(y+yy+1)*backing_width+x+index*6+xx]'",
    })
    namespace = vars(backing) | {"original": SimpleNamespace(**(vars(original) | {"machine": machine}))}
    exec(compile(paint_source, f"{__file__}::native-caption-painter", "exec"), namespace)
    return vms, namespace["paint"], executed


def sheet(previews, path):
    image = Image.new("RGB", (722, len(previews) * 54), "#263238")
    draw = ImageDraw.Draw(image)
    for i, (context, width, pixels) in enumerate(previews):
        y = i * 54
        draw.text((6, y + 2), context, fill="white")
        pic = Image.new("RGB", (width, 12))
        pic.putdata([(0, 8, 0) if point else (239, 232, 201) for point in pixels])
        image.paste(pic.resize((width * 3, 36), Image.Resampling.NEAREST), (6, y + 15))
    image.save(path)


def main():
    assert not ROOT.exists()
    source_index, release = map(base.load, (scout.OUTPUT, current.RELEASE))
    assert source_index["candidate_sha256"] == release["candidate_sha256"] == base.digest(current.ROM)
    assert source_index["clean_input_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    clean, target = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arm = target.read_file(native.ARM)
    assert native.digest(arm) == release["target_ARM9_sha256"]
    vms, paint, executed = adapters(arm)
    ROOT.mkdir()
    results, sheets = [], []
    for lead in source_index["leads"]:
        assert lead["caption_lead"] and not lead["glyph_lead"]
        source, installed = (bytes.fromhex(lead[k]) for k in ("source_object_hex", "current_object_hex"))
        ref = lead["current"]
        path, n = ref["file_path"], ref["block"]
        for image, side, raw in ((clean, "source", source), (target, "current", installed)):
            block = native.IlnkContainer.parse(image.read_file(path)).blocks[n]
            offset = lead[side]["command_offset"]
            assert block[offset:offset + len(raw)] == raw
        count = len(labels(source))
        assert count == len(labels(installed))
        key = f"{Path(path).stem}_B{n}"
        result = dict(key=key, source_reference=lead["source"], current_reference=ref, versions=[], paint=[], failures=[])
        previews = []
        for label, data in (("clean source", source), ("registered English", installed)):
            left, right = [vms[count](arm, data, alignment) for alignment in (0, 2)]
            assert left == right and left["labels"] == [option.decode("cp932") for option in labels(data)]
            assert [case["modal_selection"] for case in left["VM_cases"]] == [*range(count), -1]
            result["versions"].append(dict(version=label, object_hex=data.hex(), alignments=[0, 2], native=left))
        english = result["versions"][1]["native"]
        width = english["minimum_width_units"] * 6
        for index, label in enumerate(labels(installed)):
            for style in (1, 15):
                try:
                    pixels, proof = paint(arm, label, style, width, (0, index * 12))
                    assert proof["independent_complete_native_pixels_match"]
                    assert proof["storage_padding_all_blank"] and proof["extra_flush_stays_within_physical_backing"]
                    assert proof["visible_cell_center_twice"] == width
                except AssertionError as error:
                    frames = traceback.extract_tb(error.__traceback__)
                    result["failures"].append(dict(option=index, style=style, caption=label.decode(),
                        width_pixels=width, assertion=frames[-1].line, detail=str(error)))
                    continue
                result["paint"].append(dict(option=index, raster_sha256=sha256(pixels).hexdigest(), **proof))
                if style == 1:
                    previews.append((f"{key} | option {index + 1} | {label.decode()}", width, pixels))
        if previews:
            path = ROOT / f"{key}.png"
            sheet(previews, path)
            sheets.append(dict(file=str(path), sha256=base.digest(path)))
        results.append(result)
        print(key, "width", width, "rect", english["native_menu_rectangle"], "passed planes", len(result["paint"]),
              "findings", result["failures"], flush=True)
    base.save(PROOF, dict(candidate_sha256=release["candidate_sha256"], ARM9_sha256=release["target_ARM9_sha256"],
        source_scout_sha256=base.digest(scout.OUTPUT), cases=results, sheets=sheets,
        display_scope="Original native provider, rectangle sizing and caption painter. Modal selection and cancel are bridged. No actual gameplay.",
        executed_exact_instruction_addresses=len(executed)))


if __name__ == "__main__":
    main()

