"""Verify the legacy memory-card status templates and their immediate-return sink."""

from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0

from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.reconcile_editorial_acceptance_20261123 import ARM, OUT, digest, read, reference


RELEASE = Path("releases/all_routes_editorial_20261123_sound_play_stop_candidate/verification/registered_release_verification.json")
RESULT = OUT.with_name("legacy_card_status_text_20261123.json")
ENTRY, SINK, FORMATTER = 0xEEFD0, 0xEF068, 0xD7720
TABLES = {"outcome": (0xEF054, 3), "subject": (0xEF058, 4), "action": (0xEF05C, 7)}
FORMATS = {"completed": (0xEF060, 3), "in_progress": (0xEF064, 2)}


def word(arm, offset):
    return unpack_from("<I", arm, offset)[0]


def string_at(arm, address):
    start = address - BASE
    assert 0 <= start < len(arm)
    end = arm.index(b"\0", start, min(len(arm), start + 128))
    raw = arm[start:end]
    return dict(address=address, hex=raw.hex(), text=raw.decode("cp932"))


def original_strings(arm):
    result = {}
    for name, (reference_offset, size) in TABLES.items():
        table = word(arm, reference_offset) - BASE
        result[name] = [string_at(arm, word(arm, table + index * 4)) | dict(pointer_address=BASE + table + index * 4)
                        for index in range(size)]
    for name, (reference_offset, arity) in FORMATS.items():
        row = string_at(arm, word(arm, reference_offset))
        assert bytes.fromhex(row["hex"]).count(b"%s") == arity
        result[name] = row | dict(pointer_address=BASE + reference_offset, placeholder_count=arity)
    return result


def execute(arm, strings):
    cpu = machine(arm)
    calls, tests = [], []

    def observe(core, _address, _size, _data):
        pointer = core.reg_read(UC_ARM_REG_R0)
        raw = bytes(core.mem_read(pointer, 128))
        body, end, _ = raw.partition(b"\0")
        assert end and core.reg_read(UC_ARM_REG_LR) == BASE + 0xEF04C
        calls.append(body)

    def raw(row):
        return bytes.fromhex(row["hex"])

    handle = cpu.hook_add(UC_HOOK_CODE, observe, begin=BASE + SINK, end=BASE + SINK)
    try:
        for outcome, status in enumerate(strings["outcome"]):
            for subject, topic in enumerate(strings["subject"]):
                for action, activity in enumerate(strings["action"]):
                    value = (outcome << 8) | (action << 4) | subject
                    if outcome:
                        expected = raw(strings["completed"]) % (raw(topic), raw(activity), raw(status))
                    else:
                        expected = raw(strings["in_progress"]) % (raw(topic), raw(activity))
                    calls.clear()
                    visited = call(cpu, ENTRY, (value,), instruction_limit=250000)
                    assert {BASE + FRAME for FRAME in (SINK, FORMATTER, 0xEF048, 0xEF04C, 0xEF050)} <= visited
                    assert calls == [expected] and len(expected) < 128
                    tests.append(dict(status_word=value, bytes=len(expected), formatted_hex=expected.hex()))
    finally:
        cpu.hook_del(handle)
    assert len(tests) == 84
    return tests


def main():
    import json

    assert not RESULT.exists()
    receipt = read(RELEASE)
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"]
    assert digest("translations/release_stack.json") == receipt["registry_sha256"]
    assert digest("work/clean.nds") == receipt["clean_input_sha256"]
    clean, current = (NdsImage.open(path).read_file(ARM) for path in ("work/clean.nds", receipt["candidate"]))
    assert clean[ENTRY:SINK + 4] == current[ENTRY:SINK + 4]
    assert current[SINK:SINK + 4] == bytes.fromhex("1eff2fe1")
    original, installed = (original_strings(arm) for arm in (clean, current))
    assert all(original[key] == installed[key] for key in TABLES)
    assert sum(bool(row["hex"]) for key in TABLES for row in original[key]) == 11
    tests = dict(clean=execute(clean, original), current=execute(current, installed))
    result = dict(candidate_sha256=receipt["candidate_sha256"], clean_sha256=receipt["clean_input_sha256"],
        verified_release=reference(RELEASE), original_entry=BASE + ENTRY, original_sprintf=BASE + FORMATTER,
        formatter_to_sink=BASE + 0xEF048, display_sink=BASE + SINK, sink_hex=current[SINK:SINK + 4].hex(),
        exact_clean_and_current_function_hex=current[ENTRY:SINK + 4].hex(),
        exact_legacy_tokens={key: installed[key] for key in TABLES},
        clean_formats={key: original[key] for key in FORMATS}, current_formats={key: installed[key] for key in FORMATS},
        combinations=tests, ordinary_gameplay=False,
        disposition="All eleven nonempty tokens format through the original status helper. Its terminal routine immediately returns, so this caller never displays the assembled text.",
        other_indirect_consumers_unverified=True, registered_ROM_changed=False, new_editorial_credit=0)
    RESULT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("Verified all 84 clean and 84 current legacy memory-card status combinations and their no-op sink.")


if __name__ == "__main__":
    main()
