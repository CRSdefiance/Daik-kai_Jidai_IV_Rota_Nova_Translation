from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage

SOURCE_SHA256 = "baf77c53beed5a681452517c45391cb7b3c9230ccf9a593feb82a6eede6e53ce"
SC0_SHA256 = "d968fb685460487441fd47b8d86b87f4281c4c0021524201380494e399674a98"
ARM9_LOAD_ADDRESS = 0x02000000
BLOCK_ADDRESS = 0x020D5504
LOOP_BRANCH_ADDRESS = 0x020D5804
FORBIDDEN_START = 0x02171E48
FORBIDDEN_END = 0x02172464

ORIGINAL_BLOCK = bytes.fromhex(
    "24309AE5 04009AE5 019089E2 030050E1 0510A0E1 0500A0E1 0580A0E1"
    "020000CA 0C209AE5 020053E1 0480A0B1 000058E3 0300000A 08309AE5"
    "28209AE5 020053E1 0400A0D1 000050E3 0300000A 28209AE5 10009AE5"
    "000052E1 0410A0B1 000051E3 A400001A A60000EA"
)
ZERO_CURSOR_BLOCK = bytes.fromhex(
    "24309AE5 04009AE5 019089E2 030050E1 BB0000CA 0C209AE5 020053E1"
    "B80000AA 08309AE5 28209AE5 020053E1 B40000CA 10009AE5 000052E1"
    "B10000AA AD0000EA 022059E5 0A0052E3 01205905 20005203 24309A05"
    "06005303 24508A05 E2FFFFEA 0000A0E1 0000A0E1"
)
ORIGINAL_LOOP_BRANCH = bytes.fromhex("39FFFF1A")
ZERO_CURSOR_LOOP_BRANCH = bytes.fromhex("4EFFFF1A")

SC0_PATH = "/data/SC0.DK4"
BLOCK_INDEX = 44
RECORD_INDEX = 71
RECORD_ID = "DK4_MES_B44_R0071"
SC0_RECORD_OFFSET = 0x7B4D
ORIGINAL_RECORD = (
    b"\x05She was a wreck when we got her.\n Janus helped rebuild her."
)
PHASE_SAFE_RECORD = (
    b"\x05She was a wreck when we got her. \n Janus helped repair her."
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def require_exact(data: bytes, offset: int, expected: bytes, label: str) -> None:
    actual = data[offset : offset + len(expected)]
    if actual != expected:
        raise ValueError(
            f"{label} mismatch at component offset 0x{offset:X}: "
            f"expected {expected.hex(' ')}, got {actual.hex(' ')}"
        )


def apply_arm9(arm9: bytes) -> bytes:
    if len(ORIGINAL_BLOCK) != len(ZERO_CURSOR_BLOCK):
        raise ValueError("ARM9 replacement block changes size")
    ranges = (
        (BLOCK_ADDRESS, len(ORIGINAL_BLOCK)),
        (LOOP_BRANCH_ADDRESS, len(ORIGINAL_LOOP_BRANCH)),
    )
    if any(start < FORBIDDEN_END and start + size > FORBIDDEN_START for start, size in ranges):
        raise ValueError("probe references the prohibited runtime-owned ARM9 tail")

    block_offset = BLOCK_ADDRESS - ARM9_LOAD_ADDRESS
    loop_offset = LOOP_BRANCH_ADDRESS - ARM9_LOAD_ADDRESS
    require_exact(arm9, block_offset, ORIGINAL_BLOCK, "ARM9 LF block")
    require_exact(arm9, loop_offset, ORIGINAL_LOOP_BRANCH, "ARM9 loop branch")
    rebuilt = bytearray(arm9)
    rebuilt[block_offset : block_offset + len(ORIGINAL_BLOCK)] = ZERO_CURSOR_BLOCK
    rebuilt[loop_offset : loop_offset + 4] = ZERO_CURSOR_LOOP_BRANCH

    changed = {index for index, pair in enumerate(zip(arm9, rebuilt)) if pair[0] != pair[1]}
    allowed = set(range(block_offset, block_offset + len(ORIGINAL_BLOCK))) | set(
        range(loop_offset, loop_offset + 4)
    )
    if not changed or not changed <= allowed or len(rebuilt) != len(arm9):
        raise ValueError("ARM9 changes escaped the two declared inline ranges")
    return bytes(rebuilt)


def apply_sc0(sc0: bytes) -> bytes:
    if sha256(sc0) != SC0_SHA256:
        raise ValueError("SC0 component does not match dialogue_live_safe_v3.nds")
    if len(ORIGINAL_RECORD) != len(PHASE_SAFE_RECORD):
        raise ValueError("phase-safe record must preserve its exact allocation")
    container = IlnkContainer.parse(sc0)
    segments = [block.split(b"\0") for block in container.blocks]
    header_size = 8 + (len(container.blocks) + 1) * 4
    record_offset = (
        header_size
        + sum(len(block) for block in container.blocks[:BLOCK_INDEX])
        + sum(len(record) + 1 for record in segments[BLOCK_INDEX][:RECORD_INDEX])
    )
    if record_offset != SC0_RECORD_OFFSET:
        raise ValueError(
            f"{RECORD_ID} component offset moved: expected 0x{SC0_RECORD_OFFSET:X}, "
            f"got 0x{record_offset:X}"
        )
    actual = segments[BLOCK_INDEX][RECORD_INDEX]
    if actual != ORIGINAL_RECORD:
        raise ValueError(f"{RECORD_ID} source bytes do not match")
    segments[BLOCK_INDEX][RECORD_INDEX] = PHASE_SAFE_RECORD
    container.blocks = [b"\0".join(block) for block in segments]
    rebuilt = container.to_bytes()
    if len(rebuilt) != len(sc0):
        raise ValueError("SC0 phase repair changed component size")
    return rebuilt


def component_map(image: NdsImage) -> dict[str, bytes]:
    return {
        **dict(image.iter_components()),
        **{path: data for _, path, data in image.iter_files()},
    }


def verify_output(source: NdsImage, output: NdsImage) -> list[str]:
    source_components = component_map(source)
    output_components = component_map(output)
    if source_components.keys() != output_components.keys():
        raise ValueError("output ROM component inventory changed")
    changed = sorted(
        path for path in source_components if source_components[path] != output_components[path]
    )
    if changed != ["/__arm9__.bin", SC0_PATH]:
        raise ValueError(f"unexpected changed ROM components: {changed}")
    if output.read_file("/__arm9__.bin") != apply_arm9(source.read_file("/__arm9__.bin")):
        raise ValueError("output ARM9 does not match guarded reconstruction")
    if output.read_file(SC0_PATH) != apply_sc0(source.read_file(SC0_PATH)):
        raise ValueError("output SC0 does not match guarded reconstruction")
    return changed


def build(base: Path, output: Path) -> dict[str, object]:
    source_bytes = base.read_bytes()
    if sha256(source_bytes) != SOURCE_SHA256:
        raise ValueError("source ROM does not match dialogue_live_safe_v3.nds")
    source = NdsImage.open(base)
    source.replace_file("/__arm9__.bin", apply_arm9(source.read_file("/__arm9__.bin")))
    source.replace_file(SC0_PATH, apply_sc0(source.read_file(SC0_PATH)))
    output.parent.mkdir(parents=True, exist_ok=True)
    source.save(output)

    original = NdsImage.open(base)
    rebuilt = NdsImage.open(output)
    changed = verify_output(original, rebuilt)
    output_bytes = output.read_bytes()
    manifest = {
        "format": "dk4-disposable-arm9-dialogue-probe-v1",
        "status": "experimental-cold-boot-passed",
        "output": str(output),
        "base": str(base),
        "base_sha256": SOURCE_SHA256,
        "probe_sha256": sha256(output_bytes),
        "changed_components": changed,
        "arm9_runtime_ranges": [
            [f"0x{BLOCK_ADDRESS:08X}", f"0x{BLOCK_ADDRESS + len(ORIGINAL_BLOCK):08X}"],
            [f"0x{LOOP_BRANCH_ADDRESS:08X}", f"0x{LOOP_BRANCH_ADDRESS + 4:08X}"],
        ],
        "changed_records": [RECORD_ID],
        "sc0_component_range": [
            f"0x{SC0_RECORD_OFFSET:08X}",
            f"0x{SC0_RECORD_OFFSET + len(ORIGINAL_RECORD):08X}",
        ],
        "declared_raw_rom_ranges": [
            ["0x000D9504", "0x000D956C"],
            ["0x000D9804", "0x000D9808"],
            ["0x001E8B4D", "0x001E8B89"],
        ],
        "record_change": {
            "before": ORIGINAL_RECORD.hex(" ").upper(),
            "after": PHASE_SAFE_RECORD.hex(" ").upper(),
        },
        "forbidden_runtime_tail_touched": False,
        "runtime_success_claimed": True,
        "cold_boot_result": (
            "User confirmed New Game and the target Raphael dialogue worked, "
            "including the complete Janus line."
        ),
        "note": (
            "Zero-cursor inline probe plus a one-record ASCII pair-phase repair: "
            "an invisible pre-LF space is funded by rebuild->repair."
        ),
    }
    manifest_path = output.with_suffix(output.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="Build protected-break pair-phase probe")
    parser.add_argument("--base", type=Path, default=Path("out/dialogue_live_safe_v3.nds"))
    parser.add_argument(
        "--out", type=Path, default=Path("out/dialogue_guard_pair_phase_probe.nds")
    )
    args = parser.parse_args()
    manifest = build(args.base, args.out)
    print(f"wrote {args.out}")
    print(f"wrote {args.out.with_suffix(args.out.suffix + '.manifest.json')}")
    print(f"base_sha256={manifest['base_sha256']}")
    print(f"probe_sha256={manifest['probe_sha256']}")


if __name__ == "__main__":
    main()
