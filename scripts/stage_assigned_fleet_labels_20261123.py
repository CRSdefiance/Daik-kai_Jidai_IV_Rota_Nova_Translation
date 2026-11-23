"""Stage and replay the two stock Fleet Info formats found in ordinary play."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack, unpack_from

from scripts import observe_assigned_fleet_detail_20261123 as baseline
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, write

ARM = "/__arm9__.bin"
BASE = 0x02000000
TRIAL = baseline.ROOT / "fixed_slots"
ROM = TRIAL / "Assigned_Fleet_Info_STAGED.nds"
EDITS = (
    (0x021370F8, 0x0203767C, 12, "目標街：%s", "To: %s"),
    (0x02137118, 0x02038E00, 32, "収入額%8lu支出額%8lu投資額%8lu", "Income%8luCosts%8luInvested%8lu"),
)


# The stock Report paints a horizontal 252px strip and composites three 84px slices.
# Reserve nineteen 6px cells per row and round the canvas width up to 344.
ALIGNED = (
    (0x021370F8, 12, "目標街：%s".encode("cp932") + b"\0", b"To: %s\0"),
    (0x0213710C, 44, b"Level %4d\0\0\0" +
     "収入額%8lu支出額%8lu投資額%8lu".encode("cp932") + b"\0",
     b"Income   %10luExpenses %10luInvested %10lu\0"),
)
WORDS = (
    (0x02037E88, 0x0213710C, 0x02137904),  # Reuse the byte-identical Level caption.
    (0x02038E00, 0x02137118, 0x0213710C),  # Report template in the merged caption slots.
    (0x02038D30, 0xE3A030FC, 0xE3A03F56),  # mov r3, #344
    (0x021151E4, 182, 212),               # Report frame right edge.
    (0x02115210, 84, 114),                # Width of income slice.
    (0x02115224, 84, 114),                # X origin of expenses slice.
    (0x0211522C, 84, 114),                # Width of expenses slice.
    (0x02115240, 168, 228),               # X origin of invested slice.
    (0x02115248, 84, 114),                # Width of invested slice.
)


ROWS_TEMPLATE = b"Income  %11lu\nExpenses%11lu\nInvested%11lu\0"
ROWS = (
    ALIGNED[0],
    (ALIGNED[1][0], ALIGNED[1][1], ALIGNED[1][2], ROWS_TEMPLATE),
)
ROW_WORDS = (
    WORDS[0], WORDS[1],
    (0x02038D30, 0xE3A030FC, 0xE3A03078),  # 120px source width.
    (0x02038D38, 0xE3A0300C, 0xE3A03024),  # 36px source height.
    WORDS[3], WORDS[4],
    (0x02115224, 84, 0),                   # Row 2 source X.
    (0x02115228, 0, 12),                  # Row 2 source Y.
    WORDS[6],
    (0x02115240, 168, 0),                  # Row 3 source X.
    (0x02115244, 0, 24),                   # Row 3 source Y.
    WORDS[8],
)

PACKED_TEMPLATE = b"Income  %11luExpenses%11lu\nInvested%11lu\0"
PACKED = (
    ALIGNED[0],
    (ALIGNED[1][0], ALIGNED[1][1], ALIGNED[1][2], PACKED_TEMPLATE),
)
PACKED_WORDS = (
    WORDS[0], WORDS[1],
    (0x02038D30, 0xE3A030FC, 0xE3A030F0),  # 240px source width.
    (0x02038D38, 0xE3A0300C, 0xE3A03018),  # 24px source height.
    WORDS[3], WORDS[4], WORDS[5], WORDS[6],
    (0x02115240, 168, 0),                   # Row 3 source X.
    (0x02115244, 0, 12),                   # Row 3 source Y.
    WORDS[8],
)

def stage(variant):
    release = read(baseline.RELEASE)
    parent = Path(release["candidate"])
    assert digest(REGISTRY) == release["registry_sha256"]
    assert digest(parent) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    stock, current = (NdsImage.open(path).read_file(ARM) for path in (CLEAN, parent))
    blob = parent.read_bytes()
    arm_begin, _, arm_load, arm_size = unpack_from("<4I", blob, 0x20)
    assert arm_load == BASE and arm_size == len(current)
    assert blob[arm_begin:arm_begin + arm_size] == current
    staged = bytearray(blob)
    rows = []
    if variant != "fixed_slots":
        assert stock[0x1151DC:0x115250] == current[0x1151DC:0x115250]
        assert current[0x137904:0x137910] == current[0x13710C:0x137118] == b"Level %4d\0\0\0"
        for value, pointers in ((0x0213710C, [0x02037E88]), (0x02137118, [0x02038E00]),
                                (0x021151DC, [0x02038E04]), (0x021151FC, [0x02038D24])):
            literal = pack("<I", value)
            assert [BASE+i for i in range(0, len(current)-3, 4) if current[i:i+4] == literal] == pointers
        texts, words = {
            "stacked_report": (ROWS, ROW_WORDS),
            "packed_report": (PACKED, PACKED_WORDS),
            "aligned_report": (ALIGNED, WORDS),
        }[variant]
        changes = list(texts) + [(addr, 4, pack("<I", old), pack("<I", revised)) for addr, old, revised in words]
    else:
        changes = [(address, length, japanese.encode("cp932") + b"\0", english.encode("ascii") + b"\0")
                   for address, _, length, japanese, english in EDITS]
    owned = set()
    for address, length, original, replacement in changes:
        offset = address - BASE
        original, replacement = original.ljust(length, b"\0"), replacement.ljust(length, b"\0")
        assert len(original) == len(replacement) == length
        assert current[offset:offset + length] == original
        if address != 0x0213710C:
            assert stock[offset:offset + length] == original
        target = set(range(offset, offset + length))
        assert not owned & target
        owned.update(target)
        start = arm_begin + offset
        staged[start:start + length] = replacement
        rows.append(dict(clean_offset=offset, current_offset=offset, staged_offset=offset, address=address,
                         clean_hex=stock[offset:offset + length].hex(), current_hex=original.hex(),
                         staged_hex=replacement.hex(), rom_offset=start))
    TRIAL.mkdir(parents=True, exist_ok=True)
    with ROM.open("xb") as f:
        f.write(staged)
    for row in rows:
        before = bytes.fromhex(row["current_hex"])
        start = row["rom_offset"]
        staged[start:start + len(before)] = before
    assert staged == blob
    write(TRIAL / "stage.json", dict(registered_predecessor=reference(parent), clean=reference(CLEAN),
        staged=reference(ROM), records=rows, exact_inverse=True, staging_only=True))


def replay():
    stage_data = read(TRIAL / "stage.json")
    assert digest(ROM) == stage_data["staged"]["sha256"]
    source_commands = (baseline.ROOT / "controller.jsonl").read_text(encoding="utf-8").splitlines()
    assert source_commands[-1] == '{"stop":true}'
    commands = source_commands[:-1] + [
        '{"until":12600,"buttons":["B"],"duration":8}',
        '{"until":12800,"buttons":["B"],"duration":8}',
        '{"stop":true}',
    ]
    parent_reader = baseline.read

    def read_trial(path):
        data = parent_reader(path)
        if path == baseline.RELEASE:
            return data | dict(candidate=str(ROM), candidate_sha256=stage_data["staged"]["sha256"])
        return data

    source = checked_text(getsource(baseline.main), {
        'assert not controller.stat().st_size and not (ROOT / "capture").exists()':
            'assert not controller.stat().st_size and not (ROOT / "capture").exists()\n'
            '    controller.write_text("\\n".join(COMMANDS) + "\\n", encoding="utf-8")',
        "CONTROLLER=controller, current=current, __file__=__file__)":
            "CONTROLLER=controller, current=current, __file__=__file__, base=TRIAL_BASE)",
    })
    from types import SimpleNamespace

    original_base = baseline.replay.base

    def load_trial(path):
        return read_trial(path) if path == baseline.RELEASE else original_base.load(path)

    trial_base = SimpleNamespace(load=load_trial, digest=original_base.digest, save=original_base.save,
                                 REGISTRY=original_base.REGISTRY)
    namespace = vars(baseline) | dict(ROOT=baseline.ROOT.with_name("fleet_info_" + TRIAL.name + "_replay"), COMMANDS=commands, read=read_trial,
                                      TRIAL_BASE=trial_base, __file__=__file__)
    exec(compile(source, __file__ + "::staged_fleet_replay", "exec"), namespace)
    namespace["main"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("fixed_slots", "aligned_report", "stacked_report", "packed_report"))
    parser.add_argument("--replay-only", action="store_true")
    args = parser.parse_args()
    TRIAL = baseline.ROOT / args.variant
    ROM = TRIAL / "Assigned_Fleet_Info_STAGED.nds"
    if not args.replay_only:
        stage(args.variant)
    replay()
