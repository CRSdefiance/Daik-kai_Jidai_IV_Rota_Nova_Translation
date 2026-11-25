"""Replay the Lure Fleet picker for each revised destination question."""

from argparse import ArgumentParser
from io import StringIO
from json import dumps
from struct import pack, unpack_from
from types import FunctionType
import sys

from dk4tool.formats.ilnk import IlnkContainer
from scripts import preflight_fleet_diversion_questions_20261125 as draft
from scripts import replay_tavern_strategist_followup_20261119 as historical
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, sha256, write
from unicorn.arm_const import UC_ARM_REG_R0


ROOT = draft.current.ROM.parent.with_name("editorial_20261125_fleet_diversion_replay")
ROM = ROOT / "Fleet_Diversion_STAGED.nds"
PROOF = ROOT / "unregistered_replay_manifest.json"
FRAMES = 18000
CAPTURES = (3200, 15200, 16000, 16400, 16800, 17200, 17600, 18000)


def stage():
    parent, packet = map(read, (draft.current.RELEASE, draft.OUT))
    assert packet["candidate_sha256"] == parent["candidate_sha256"] == digest(draft.current.ROM)
    original = NdsImage.open(draft.current.ROM)
    common = original.read_file(draft.current.COMMON)
    assert sha256(common).hexdigest() == parent["target_COMMON_sha256"]
    archive = IlnkContainer.parse(common)
    blocks = list(archive.blocks)
    assert set(map(int, packet["allocations"])) == draft.DRAFTS.keys()
    for slot in packet["allocations"].values():
        block, lo, hi = (slot[k] for k in ("block", "start", "end"))
        before, after = (bytes.fromhex(slot[k]) for k in ("before", "after"))
        assert blocks[block][lo:hi] == before and len(after) == len(before) == hi - lo
        blocks[block] = blocks[block][:lo] + after + blocks[block][hi:]
    proposed = IlnkContainer(blocks).to_bytes()
    assert sha256(proposed).hexdigest() == packet["proposed_COMMON_sha256"]
    original.replace_file(draft.current.COMMON, proposed)
    ROOT.mkdir()
    original.save(ROM)
    original.replace_file(draft.current.COMMON, common)
    assert sha256(original.rom.save()).hexdigest() == parent["candidate_sha256"]
    write(PROOF, dict(parent=reference(draft.current.ROM), candidate=reference(ROM),
                      preflight=reference(draft.OUT), target_COMMON_sha256=packet["proposed_COMMON_sha256"],
                      exact_parent_inverse=True, unregistered_staged_replay=True))
    print("Staged both dialogue changes and verified the whole-parent inverse.")


def fixture(arm, raw, request, message, expected_digest):
    assert sha256(arm).hexdigest() == expected_digest
    assign = FunctionType(historical.assignment.assign.__code__, vars(historical.assignment) | {"BASELINE": expected_digest})
    expert = FunctionType(historical.expert.assign_expert.__code__, vars(historical.expert) | {"assign": assign})
    after, proof = expert(arm, raw, request)
    cpu = draft.schemes.machine(arm)
    cpu.mem_write(draft.BASE, after)
    from scripts.native_call_abi_v764 import call

    def get(offset, args):
        call(cpu, offset, args)
        return cpu.reg_read(UC_ARM_REG_R0)

    clean = NdsImage.open(CLEAN).read_file(draft.current.ARM)
    for lo, hi in ((0x7E988, 0x7E9A0), (0x53F4C, 0x53F84)):
        assert clean[lo:hi] == arm[lo:hi]
    voice = get(0x7E988, (proof["actor"],))
    assert voice == 1 and get(0x53F4C, (proof["actor"], draft.TABLE)) == 921
    start = draft.TABLE - draft.BASE
    menu = (921, -1, 922, -1, 923, 924, 925, 926)
    assert all(unpack_from("<8i", source, start) == menu for source in (clean, arm, after))
    assert message in (923, 926) and message in menu

    # Use a RAM copy of the destination prompt table only. The crew member,
    # voiced confirmations and the game logic remain identical between runs.
    slot = start + voice * 4
    word = pack("<i", message)
    result = after[:slot] + word + after[slot + 4:]
    cpu.mem_write(draft.BASE + slot, word)
    assert get(0x53F4C, (proof["actor"], draft.TABLE)) == message
    touched = [dict(address=draft.BASE + slot + i, before=old, after=new)
               for i, (old, new) in enumerate(zip(after[slot:slot + 4], word, strict=True)) if old != new]
    proof.update(after_RAM_sha256=sha256(result).hexdigest(), prompt_message_ID=message, native_actor_voice=voice,
                 prior_prompt_selection=921, prompt_selector_slot=draft.BASE + slot,
                 all_other4MiB_bytes_exact=True, only_three_assignment_bytes_one_XP_word_one_calendar_word_owned=False,
                 only_previous_eligibility_fixture_and_one_prompt_table_word_owned=True,
                 changes=proof["changes"] + touched)
    return result, proof


def capture(version, message):
    parent, staged, prior = map(read, (draft.current.RELEASE, PROOF, historical.HISTORICAL))
    path = draft.current.ROM if version == "current" else ROM
    assert reference(path) == staged["parent" if version == "current" else "candidate"]
    assert staged["exact_parent_inverse"]
    arm = NdsImage.open(path).read_file(draft.current.ARM)
    assert sha256(arm).hexdigest() == parent["target_ARM9_sha256"]
    donor = prior["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    inputs = ROOT / f"{version}_{message}_inputs.json"
    schedule = [row for row in prior["scripted_input_schedule"] if row["start"] <= FRAMES]
    write(inputs, schedule)
    folder = ROOT / f"{version}_{message}"
    harness = historical.runner.HARNESS
    assert digest(harness) == prior["controlled_strategist_adapter"]["original_harness_sha256"]
    source = checked_text(harness.read_text(encoding="utf-8"), {
        "from scripts.native_strategist_fixture_v624 import assign, assign_expert": "assign, assign_expert = ACTIVE_FIXTURE, ACTIVE_FIXTURE",
    })

    def apply(arm, raw, request):
        return fixture(arm, raw, request, message, parent["target_ARM9_sha256"])

    previous = sys.argv, sys.stdin
    try:
        sys.argv = [str(harness), "--rom", str(path), "--out", str(folder), "--battery-save", donor["source"],
                    "--frames", str(FRAMES), "--inputs-json", str(inputs), "--touchscreen", "--allow-strategist-fixtures",
                    "--pause-at", "3200", "--dump-pause-ram", "--capture-every", "999999",
                    "--capture-at", *map(str, CAPTURES), "--dump-capture-ram"]
        sys.stdin = StringIO(dumps({"strategist_expert_fixture": True, "until": FRAMES, "buttons": []}) + "\n"
                             + dumps({"stop": True}) + "\n")
        exec(compile(source, str(harness), "exec"),
             {"__name__": "__main__", "__file__": str(harness.resolve()), "ACTIVE_FIXTURE": apply})
    finally:
        sys.argv, sys.stdin = previous
    report_path = folder / "capture_report.json"
    report = read(report_path)
    assert report["frames"] == FRAMES and report["ROM_sha256"] == digest(path)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == schedule and digest(donor["source"]) == donor["source_sha256"]
    write(folder / "terminal.json", dict(capture=reference(report_path), inputs=reference(inputs),
          candidate=reference(path), message_ID=message, fixture_gameplay=True, ordinary_gameplay=False,
          harness=reference(harness), effective_harness_sha256=sha256(source.encode()).hexdigest()))
    print(f"Completed {version} fixture replay for COMMON {message}.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(required=True, dest="action")
    commands.add_parser("stage")
    run = commands.add_parser("capture")
    run.add_argument("version", choices=("current", "proposed"))
    run.add_argument("message", type=int, choices=draft.DRAFTS)
    args = parser.parse_args()
    if args.action == "stage":
        stage()
    else:
        capture(args.version, args.message)
