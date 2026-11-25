"""Stage the Lisbon roster stat crop and the Galley help reflow."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.ascii_glyph_right_bounds import BASE
from dk4tool.patch.roster_role_crop import DESCRIPTOR
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_village_article_wraps_20261124 as parent
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts import verify_ordinary_lisbon_purser_20261124 as observed
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact
from scripts.verify_personal_gameplay_v841 import get_machine


ARM, COMMON, RELEASE = parent.ARM, parent.COMMON, parent.RELEASE
ROOT = Path("E:/Rota Nova translations/Generated/work/editorial_20261124_lisbon_roster_galley")
ROM = ROOT / "Lisbon_Roster_Galley_STAGED.nds"
STORED, OUT = ROOT / "stored_proof.json", ROOT / "lisbon_roster_galley_review.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
NATIVE = ROOT / "native_refit"
MANUSCRIPT = ROOT / "native_refit_input.json"
played = SimpleNamespace(RELEASE=RELEASE)
KEY, WIDTH = 1250, 72
WIDTH_AT = DESCRIPTOR + 28 + 20
FIELD_ID = "DK4_ROSTER_STAT_COMPLETE_CROP"


def stat_raster(cpu, font, text, mode, color):
    header_at, origin_at, text_at = 0x02450000, 0x02460000, 0x02460100
    pitch = WIDTH if mode == 16 else WIDTH // 4
    stride, height = pitch * 2, 12
    header = pack("<5I", mode, pitch, height, 0x2000, 20)
    size = stride * height
    canary = b"\xA5" * 16
    initial = b"\x99" * size
    cpu.mem_write(header_at - 16, canary + header + initial + canary)
    cpu.mem_write(origin_at, bytes(8))
    cpu.mem_write(text_at, text.encode("ascii") + b"\0")
    cpu.mem_write(STACK, pack("<I", 1))
    call(cpu, 0xD1604, (0, header_at, origin_at, text_at))

    expected = bytearray(initial)
    for i, char in enumerate(text):
        glyph = font.decode(char)
        for y in range(11):
            for x in range(6):
                ink = bool(glyph.getpixel((x, y)))
                px, py = i * 6 + x, y + 1
                if mode == 16 and ink:
                    expected[py * stride + px * 2:py * stride + px * 2 + 2] = color
                if mode == 4:
                    at, shift = py * stride + px // 2, px % 2 * 4
                    expected[at] = expected[at] & ~(15 << shift) | (int(ink) << shift)
    assert bytes(cpu.mem_read(header_at - 16, size + 52)) == canary + header + expected + canary, (text, mode)


def roster(arm, clean, packet):
    field = packet["roster_finance_crop"]
    assert field["width_file_offset"] == WIDTH_AT
    assert unpack_from("<21i", arm, DESCRIPTOR) == (
        -1, 12, 92, 0, 0, 204, 12, -1, 12, 108, 0, 12, 60, 12, -1, 12, 124, 0, 24, 204, 12)
    assert arm[DESCRIPTOR + 28:DESCRIPTOR + 84] == clean[DESCRIPTOR + 28:DESCRIPTOR + 84]
    assert arm[0x9C0CC:0x9C110] == clean[0x9C0CC:0x9C110]
    assert arm[0x9C1D4:0x9C1D8] == clean[0x9C1D4:0x9C1D8] == pack("<I", 0x02000000 + DESCRIPTOR)
    assert arm[0x9C324:0x9C39C] == clean[0x9C324:0x9C39C]
    assert 12 + WIDTH <= 12 + 204 <= 256
    target = arm[:WIDTH_AT] + pack("<I", WIDTH) + arm[WIDTH_AT + 4:]
    assert target[:WIDTH_AT] + pack("<I", 60) + target[WIDTH_AT + 4:] == arm
    raw = load_exact(packet["assigned_purser"]["read_only_snapshot"])
    state, get = get_machine(arm, raw)

    def read_label(i):
        pointer = get(0x7EEB0, i)
        name = raw[pointer - BASE:pointer - BASE + 24].split(b"\0")[0].decode("ascii")
        return name, pointer

    entries = [read_label(i) for i in range(10)]
    labels = {label for label, _ in entries}
    assert len(labels) == 10 and "Finance" in labels and all(label.isalpha() for label in labels)
    assert arm[0x14FBB4:0x14FBB4 + 6] == b"%s%4d\0"
    assert arm[0x14FBA8:0x14FBA8 + 10] == b"Level %4d\0"
    font = GameAsciiFont.from_arm9(target)
    palette = unpack_from("<I", target, 0xD181C)[0] - BASE
    color = target[palette + 2:palette + 4]
    raster = machine(target)
    formatted = 0x02440020
    cases = []
    for label, pointer in [*entries, ("Level ", None)]:
        for value in (0, 99, 115, 255, 9999):
            text = "%s%4d" % (label, value)
            args = (formatted, BASE + 0x14FBB4, pointer, value) if pointer else (formatted, BASE + 0x14FBA8, value)
            state.mem_write(formatted - 4, b"\xA5" * 24)
            call(state, 0xD7720, args)
            assert bytes(state.mem_read(formatted - 4, 24)) == b"\xA5" * 4 + (text.encode("ascii") + b"\0").ljust(20, b"\xA5")
            padded = text + (" " if len(text) % 2 else "")
            assert len(padded) * 6 <= WIDTH
            for mode in (4, 16):
                stat_raster(raster, font, padded, mode, color)
            cases.append(dict(label=label, value=value, text=text, native_final_x=len(padded) * 6, complete_4_and_16_bit=True))
    ref = dict(file_path=ARM, width_file_offset=WIDTH_AT, exact_width_hex=pack("<I", 60).hex(), descriptor=DESCRIPTOR,
               source_level_format="Level %4d", source_ability_format="%s%4d")
    row = dict(id=FIELD_ID, file_path=ARM, english="Finance 115", speaker="Crew roster",
        context="The lower roster card summarizes the selected officer's relevant ability while assigning a crew role.",
        source_meaning="Display the complete native ability name and the current officer's numeric value.",
        localization_note="The roster needs the full Finance value shown in the detailed profile. Expand its existing stat-row crop to 72 pixels.",
        source_reference=ref, current_reference=ref, installed_reference=ref | dict(exact_width_hex=pack("<I", WIDTH).hex()),
        decision="revision", review=dict.fromkeys(GATES, True))
    return target, row, cases


def galley(arm, clean, image, packet):
    source = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))[KEY]
    common = image.read_file(COMMON)
    rows = parent.parent.parent.trend.owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    current = rows[KEY]
    row, = packet["full_body_refit_wrap_followups"]
    assert row["message_ID"] == KEY and row["source_reference"]["exact_hex"] == source.text.hex()
    assert row["installed_reference"]["exact_hex"] == current.text.hex()
    text = " ".join(current.text.decode("ascii").split())
    assert text == row["english"] and text.count("food and water") == 1
    compiled, lines = compile_paragraph(text.replace("food and water", "food_and_water"))
    compiled = compiled[:-1].replace(b"_", b" ").ljust(len(current.text))
    lines = [line.replace("_", " ") for line in lines]
    assert " ".join(lines) == text and len(lines) == 3 and "food and water" in lines[1]
    assert len(compiled) == len(current.text) and max(map(len, compiled.split(b"\n"))) <= 28
    revised, entries, allocation = owned_deployment(common, arm, rows, {KEY: compiled})
    assert [after.message_id for before, after in zip(rows, entries, strict=True) if before != after] == [KEY]
    ref = observed.panels.text_reference(entries[KEY]) | dict(exact_hex=compiled.hex())
    row.update(installed_reference=ref, decision="revision", review=dict.fromkeys(GATES, True),
               localization_note="Keep the cook's conservation and fatigue effects. The phrase food and water now occupies one row.",
               editorial_decision="wrap", message_id=KEY, payload_hex=compiled.hex(), compiled_lines=lines)
    return revised, row, allocation[KEY]


def verify_native_help(row, candidate):
    source = Path("scripts/verify_refit_editorial_v830.py").read_text(encoding="utf-8")
    code = checked_text(source, {
        "from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT": "",
        "compiled, lines = compile_paragraph(record['english'])":
            "compiled, lines = bytes.fromhex(record['payload_hex']) + bytes(1), record['compiled_lines']",
        "(line_index * 12 + y) * 168": "(line_index * 12 + y + 1) * 168",
    })
    ROOT.mkdir(exist_ok=True)
    NATIVE.mkdir(exist_ok=True)
    write(MANUSCRIPT, dict(current_candidate_sha256=candidate, records=[row]))
    scope = dict(__name__="__main__", __file__=__file__, ROM=ROM, ROOT=NATIVE, MANUSCRIPT=MANUSCRIPT)
    exec(compile(code, __file__ + "::original-refit-font", "exec"), scope)
    return read(NATIVE / "native_font_verification.json")


def stage():
    previous, packet = read(RELEASE), read(observed.OUT)
    assert digest(previous["candidate"]) == previous["candidate_sha256"]
    assert digest(CLEAN) == previous["clean_input_sha256"] and digest(REGISTRY) == previous["registry_sha256"]
    assert packet["original_cold_boot_and_ordinary_controller_inputs"]
    image, clean = (NdsImage.open(path) for path in (previous["candidate"], CLEAN))
    files = parent.parent.parent.trend.files
    before = files(image)
    arm = before[ARM]
    assert sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    assert sha256(before[COMMON]).hexdigest() == previous["target_COMMON_sha256"]
    updated_arm, field, matrix = roster(arm, clean.read_file(ARM), packet)
    updated_common, row, allocation = galley(arm, clean, image, packet)
    assert parent.template.right_bound(updated_arm, previous["right_bound_configuration"])["matched_repair_spans"] == 8
    assert parent.build.former.cache_plan(arm) == parent.build.former.cache_plan(updated_arm)
    image.replace_file(ARM, updated_arm)
    image.replace_file(COMMON, updated_common)
    after = files(image)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {ARM, COMMON}
    binary = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, before[COMMON])
    assert sha256(image.rom.save()).hexdigest() == previous["candidate_sha256"]
    ROOT.mkdir(exist_ok=True)
    if ROM.is_file():
        assert ROM.read_bytes() == binary
    else:
        with ROM.open("xb") as rom:
            rom.write(binary)
    cand = digest(ROM)
    assert cand == sha256(binary).hexdigest()
    native = verify_native_help(row, cand)
    proof = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=[field, row], contextual_lisbon_review=reference(observed.OUT),
        candidate_sha256=cand, previous_sha256=previous["candidate_sha256"],
        all_native_stat_names=matrix, allocation=allocation, native_galley=native)
    validate_natural_dialogue_batch(proof)
    write(OUT, proof)
    write(STORED, dict(candidate=str(ROM), candidate_sha256=cand, predecessor_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"], target_ARM9_sha256=sha256(updated_arm).hexdigest(),
        target_COMMON_sha256=sha256(updated_common).hexdigest(), whole_parent_inverse=True,
        source_preflight=reference(OUT), changed_files=[ARM, COMMON], changed_common_slot=allocation))
    print(f"Staged one roster crop and COMMON {KEY}. Candidate {cand}.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(STORED), action)
