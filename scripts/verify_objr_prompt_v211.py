"""Verify registered inheritance, full prompt pixels and native file-read spans."""

import json
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.obj_banked_sync import apply_banked_sync
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_objr_prompt_v211 import decode
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/objr_prompt_v211")
CANDIDATE = Path("out/all_routes_combined_v211_candidate.nds")
BUFFER = 0x02460020
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    batch = json.loads(Path("translations/objr_start_prompt_embedded_sync_v1.json").read_text(encoding="utf-8"))
    prior, candidate = NdsImage.open("out/all_routes_combined_v205_candidate.nds"), NdsImage.open(CANDIDATE)
    assert sha(prior.source.read_bytes()) == "88444cb34139aada935f81b39b478fa81b5f54a32ef7c88a7e08b2b3dfe1dfa0"
    assert sha((ROOT / "v205_builder_reproduction.nds").read_bytes()) == sha(prior.source.read_bytes())
    a = {p: bytes(v) for _, p, v in prior.iter_files()}
    b = {p: bytes(v) for _, p, v in candidate.iter_files()}
    changed = [p for p in a if a[p] != b[p]]
    assert a.keys() == b.keys() and changed == ["/GRP/DSOBJR.DK4"]
    assert bytes(prior.rom.arm9) == bytes(candidate.rom.arm9)
    assert bytes(prior.rom.arm7) == bytes(candidate.rom.arm7)
    reference = candidate.read_file(batch["source_image_path"])
    raw = candidate.read_file(batch["file_path"])
    expected, _ = apply_banked_sync(batch, prior.read_file(batch["file_path"]), reference)
    assert raw == expected and raw[:5920] == a[batch["file_path"]][:5920]
    image = PxlImage.from_bytes(reference)
    indices = decode(raw[5920:])
    assert indices == bytes(image.indices) + bytes(768)
    ink = [(i % 256, i // 256) for i, v in enumerate(indices) if v == 15]
    bounds = [min(x for x, y in ink), min(y for x, y in ink), max(x for x, y in ink) + 1, max(y for x, y in ink) + 1]
    assert bounds[0] >= 0 and bounds[2] <= 256 and bounds[1] >= 0 and bounds[3] <= 29
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    prior_manifest = json.loads(prior.source.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    assert manifest["profile"] == "all-routes-unified-v211" and len(manifest["batches"]) == 467
    assert manifest["batches"][:-1] == prior_manifest["batches"]
    assert manifest["required_batches"] == prior_manifest["required_batches"]
    assert manifest["base_sha256"] == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert manifest["candidate_sha256"] == sha(CANDIDATE.read_bytes())
    assert manifest["release_stack_sha256"] == sha(Path("translations/release_stack.json").read_bytes())
    arm = candidate.read_file("/__arm9__.bin")
    u = machine(arm)
    handles, events = {}, []

    def bridge(uc, address, size, _):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = uc.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_R1), 64)).split(b"\0")[0].decode("ascii").replace("\\", "/")
            assert name == "/GRP/DSOBJR.DK4" and not handles
            handles[obj] = 0
            value = 1
            events.append({"operation": "open", "path": name})
        elif address == SEEK:
            offset = uc.reg_read(UC_ARM_REG_R1)
            assert uc.reg_read(UC_ARM_REG_R2) == 0 and offset == 5920
            handles[obj] = offset
            value = 1
            events.append({"operation": "seek", "offset": offset})
        elif address == READ:
            target, count = uc.reg_read(UC_ARM_REG_R1), uc.reg_read(UC_ARM_REG_R2)
            offset = handles[obj]
            assert target == BUFFER and offset + count <= len(raw)
            uc.mem_write(target, raw[offset:offset + count])
            handles[obj] += count
            value = count
            events.append({"operation": "read", "offset": offset, "bytes": count})
        else:
            handles.pop(obj)
            value = 1
            events.append({"operation": "close"})
        uc.reg_write(UC_ARM_REG_R0, value)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    try:
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R4, BUFFER)
        for start, stop, size, offset in ((0x02000D70, 0x02000D8C, 5408, 0),
                                           (0x02000D9C, 0x02000DBC, 4096, 5920)):
            u.mem_write(BUFFER - 16, b"\xa5" * (size + 32))
            u.emu_start(start, stop, count=1000)
            assert u.reg_read(UC_ARM_REG_PC) == stop and u.reg_read(UC_ARM_REG_SP) == STACK
            assert bytes(u.mem_read(BUFFER, size)) == raw[offset:offset + size]
            assert bytes(u.mem_read(BUFFER - 16, 16)) == b"\xa5" * 16
            assert bytes(u.mem_read(BUFFER + size, 16)) == b"\xa5" * 16
        u.emu_start(0x02000DCC, 0x02000DD4, count=1000)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02000DD4 and not handles
    finally:
        u.hook_del(hook)
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = ROOT / "patch_reconstruction.nds"
    clean = Path("work/clean.nds")
    assert sha(clean.read_bytes()) == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == CANDIDATE.read_bytes()
    proof = {"format": "dk4-embedded-OBJR-prompt-proof-v1", "candidate": CANDIDATE.as_posix(),
             "candidate_sha256": sha(CANDIDATE.read_bytes()), "profile": manifest["profile"],
             "base_sha256": manifest["base_sha256"], "active_batches": 467,
             "all_V205_batches_required_layers_components_and_other_files_retained": True,
             "full_prior_builder_reproduction_exact": True, "only_changed_path_vs_V205": changed[0],
             "protected_prefix_and_palette_bytes": 5920, "full_DSOBJR_size": len(raw),
             "reference_pixels_copied_exact": len(image.indices), "transparent_padding_pixels": 768,
             "complete_source_first_last_letters_and_blank_pixels_exact": True,
             "complete_foreground_pixels": len(ink), "foreground_bounds": bounds,
             "native_file_read_spans": events, "native_read_guards_exact": True,
             "native_read_scope": "Original startup open/read/seek/read/close spans with explicit preceding R4/stack fixture; graphics/DMA transfers between spans are not executed.",
             "patch": patch.as_posix(), "patch_sha256": sha(patch.read_bytes()),
             "exact_clean_ROM_patch_reconstruction": True, "cold_boot_and_GPU_followup_pending": True,
             "experimental_user_acceptance_pending": True, "full_goal_complete": False}
    (ROOT / "saved_proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate_sha256": proof["candidate_sha256"], "patch_sha256": proof["patch_sha256"],
                      "complete_foreground_pixels": len(ink), "native_read_spans": 2, "exact_patch": True}))


if __name__ == "__main__":
    main()
