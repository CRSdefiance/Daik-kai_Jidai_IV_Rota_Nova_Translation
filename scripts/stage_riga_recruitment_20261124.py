"""Stage the Riga crew wording and regular numerals with the original portrait formatter."""

from argparse import ArgumentParser
from struct import pack
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile

from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, ITCM, NUMBER, assemble, cache_plan, compact_helper
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts import observe_riga_tavern_20261124 as play
from scripts import stage_recruit_crew_20261120 as recruit
from scripts import stage_recruitment_capacity_wraps_20261123 as capacity
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_inn_numerals_native_20261119 import RING, RING_SIZE, normalize
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_riga_tavern_20261124 import OUT as ORDINARY
from scripts.verify_yard_numerals_native_20261124 import call_number

parent = play.current
ARM, COMMON = parent.ARM, parent.COMMON
ROOT = play.ROOT.with_name("editorial_20261124_riga_recruitment")
ROM = ROOT / "Riga_Recruitment_STAGED.nds"
OUT = ROOT / "riga_recruitment_native.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=parent.RELEASE)
ASSIGN, CALLS = 0x02117460, (0x0201DD20, 0x0201E120)
COUNTS = sorted(set(capacity.COUNTS) | {15, 49, 56, 64, 120, 139})
WIDE = str.maketrans("0123456789", "０１２３４５６７８９")
DRAFTS = {
    71: ("Is leaving %s of our sailors unassigned all right?",
         "Gerhard asks permission with the same number unassigned. The noun phrase stays together."),
    72: (None, "The statement and simple follow-up suit the conversational question about the unassigned sailors."),
    73: ("Go ahead with %s of our sailors still unassigned?",
         "Keep the direct question about proceeding and the still-unresolved assignments."),
    74: ("Can we leave %s of our sailors unassigned?",
         "The plain question preserves the casual concern about the extra sailors."),
    75: ("May we leave %s of our sailors unassigned?",
         "May preserves the courteous request concerning the same unassigned sailors."),
    1042: ("There's room aboard for %s more. Shall I keep looking?",
           "Gerhard states the precise capacity and politely offers to continue."),
    1043: ("Still room aboard for %s more. Should I keep looking?",
           "The clipped observation and direct question keep the practical, familiar voice."),
    1044: ("There's room aboard for %s more. Would you like me to keep looking?",
           "The courteous offer leaves the choice to the captain."),
    1045: (None, "The existing short offer fits the familiar voice and already avoids repeating more."),
    1046: ("Seems we can fit %s more aboard. Shall I see who else might join?",
           "The estimate stays tentative, and the question keeps the measured offer."),
    1047: ("Looks like we can take %s more. Should I keep looking?",
           "The casual inference and familiar offer preserve the voice and precise spare capacity."),
    1048: (None, "The current count and polite offer to keep recruiting read naturally as two complete sentences."),
}


def number_edits(ctx, clean_arm, release):
    for start, end in ((0x1DCF4, 0x1DD38), (0x1E0F4, 0x1E138), (0x53CB0, 0x53D60)):
        assert ctx.arm[start:end] == clean_arm[start:end] == ctx.raw[start:end]
    for offset in (0x1DD4C, 0x1E17C):
        assert ctx.arm[offset:offset + 4] == clean_arm[offset:offset + 4] == pack("<I", ASSIGN)
    itcm = MainCodeFile(ctx.arm, BASE).sections[4]
    helper = compact_helper()
    assert itcm.ramAddress == ITCM and bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    arm, raw = bytearray(ctx.arm), bytearray(ctx.raw)
    changes = []
    for address in CALLS:
        off = address - BASE
        old, new = assemble(f"bl {NUMBER}", address), assemble(f"bl {HELPER}", address)
        assert arm[off:off + 4] == old
        arm[off:off + 4] = raw[off:off + 4] = new
        changes.append(dict(address=address, before_hex=old.hex(), after_hex=new.hex()))
    inverse = bytearray(arm)
    for row in changes:
        offset = row["address"] - BASE
        inverse[offset:offset + 4] = bytes.fromhex(row["before_hex"])
    arm, raw = bytes(arm), bytes(raw)
    assert inverse == ctx.arm and cache_plan(ctx.arm) == cache_plan(arm)
    check = parent.template.right_bound
    assert check(ctx.arm, release["right_bound_configuration"]) == check(arm, release["right_bound_configuration"])
    cpus = [get_machine(a, snap)[0] for a, snap in ((ctx.arm, ctx.raw), (arm, raw))]
    initial = bytes(cpus[0].mem_read(RING, RING_SIZE))
    assert bytes(cpus[1].mem_read(RING, RING_SIZE)) == initial
    cases = []
    for address in CALLS:
        for slot in range(32):
            value = COUNTS[slot % len(COUNTS)]
            for cpu in cpus:
                cpu.mem_write(RING, initial[:8] + pack("<I", slot) + initial[12:])
            (p, old), (q, new) = (call_number(cpu, address, value) for cpu in cpus)
            lower = RING + 12 + 128 * slot
            assert lower <= p == q and p + len(old) < lower + 128
            assert old != new and normalize(old) == new == str(value).encode("ascii")
            lo, hi = p - RING, p - RING + len(old) + 1
            before, after = [bytes(cpu.mem_read(RING, RING_SIZE)) for cpu in cpus]
            assert before[:lo] == after[:lo] and before[hi:] == after[hi:]
            cases.append(dict(call=address, slot=slot, count=value, before_hex=old.hex(), after_hex=new.hex()))
    return arm, raw, changes, cases


def review_text(ctx, arm, raw, common, clean, prior, installed):
    src = recruit.batch.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    target = with_components(ctx, arm, common)
    native, get, provider = target.machine(arm, common, target.raw, target.plan)
    cpu, _ = get_machine(arm, raw)
    original = capacity.native_formatter()
    fmt = FunctionType(original.__code__, original.__globals__ | dict(SHORTFALL=ASSIGN))
    raster, _, _ = recruit.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    rows, pages = [], []
    for key, (draft, reason) in DRAFTS.items():
        jp, old, new = (book[key] for book in (src, prior, installed))
        assert all(row.text.count(b"%") == row.text.count(b"%s") == 1 for row in (jp, old, new))
        assert old.copy_end == new.copy_end and len(old.text) == len(new.text)
        assert bytes(native.mem_read(get(0x5528C, key), len(new.text) + 1)) == new.text + bytes(1)
        english = new.text.decode("ascii").strip()
        assignment = key < 80
        context = "Confirm whether to leave the stated number of sailors unassigned." if assignment else (
            "After the first call for volunteers, give the remaining capacity and offer to keep recruiting.")
        row = dict(id=f"COMMON_MESSAGE_{key}", message_id=key, file_path=COMMON, speaker="First mate",
                   english=english, English_argument_source_indices=[0], context=context,
                   source_meaning=context if assignment else recruit.semantics(key),
                   localization_note=reason, clean_Japanese=jp.text.decode("cp932"),
                   decision="revision" if draft or assignment else "retention",
                   wording_decision="revision" if draft else "retention", cases=[],
                   review=dict.fromkeys(GATES, True) | dict(formatting=False))
        for label, entry in (("source", jp), ("current", old), ("installed", new)):
            row[f"{label}_reference"] = recruit.batch.reference(entry) | dict(exact_hex=entry.text.hex())
        for count in COUNTS:
            value = str(count)
            prior_arg = value.translate(WIDE).encode("cp932") if assignment else value.encode("ascii")
            previous = fmt(cpu, row, (prior_arg,), old.text)
            result = fmt(cpu, row, (value.encode("ascii"),), new.text)
            lines = result["lines"]
            assert " ".join(lines) == english % value and lines[-1].endswith("?") and not result["findings"], (key, count, lines)
            if assignment:
                assert any(f"{count} of our sailors" in line for line in lines), (key, count, lines)
                assert len(lines) <= 3
            else:
                assert len(lines) == 2 and lines[0].endswith(".") and len(lines[1]) >= 15, (key, count, lines)
            formatted = bytes.fromhex(result["formatted_hex"])
            plane, glyphs = recruit.render_portrait(raster, arm, kanji, formatted)
            codes = [g["code"] for g in glyphs]
            assert codes == recruit.glyph_codes(formatted) and (codes[0], codes[-1]) == (ord(english[0]), ord("?"))
            row["cases"].append(result | dict(count=count, prior_lines=previous["lines"],
                                              native_plane_sha256=sha256(bytes(plane)).hexdigest()))
            if assignment or draft:
                pages.append((f"{key} / {count}", plane))
        rows.append(row)
    assert provider.reads
    return rows, pages


def main():
    release, ordinary = map(read, (parent.RELEASE, ORDINARY))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(parent.ROM) == release["candidate_sha256"] == ordinary["candidate_sha256"]
    assert ordinary["ordinary_gameplay"] and ordinary["volunteers"] == [56, 64]
    starter = read(release["own_registered_startup"])
    ctx = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=starter["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    for address, expected in ((ASSIGN, (71, -1, 72, -1, -1, 73, 74, 75)),
                              (capacity.CAPACITY, recruit.TABLES[capacity.CAPACITY])):
        off = address - BASE
        assert clean_arm[off:off + 32] == ctx.arm[off:off + 32] == pack("<8i", *expected)
    arm, raw, changes, cases = number_edits(ctx, clean_arm, release)
    prior = recruit.catalogue(ctx.arm, ctx.common)
    edited = {key: (" " + draft).encode("ascii").ljust(len(prior[key].text), b" ")
              for key, (draft, _) in DRAFTS.items() if draft}
    assert all(len(data) == len(prior[key].text) for key, data in edited.items())
    common, installed, allocations = owned_deployment(ctx.common, arm, prior, edited)
    assert {b.message_id for a, b in zip(prior, installed, strict=True) if a != b} == set(edited)
    rows, pages = review_text(ctx, arm, raw, common, clean, prior, installed)
    ctx.image.replace_file(ARM, arm)
    ctx.image.replace_file(COMMON, common)
    candidate = bytes(ctx.image.rom.save())
    ctx.image.replace_file(ARM, ctx.arm)
    ctx.image.replace_file(COMMON, ctx.common)
    assert sha256(ctx.image.rom.save()).hexdigest() == release["candidate_sha256"]
    ROOT.mkdir(exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        with ROM.open("xb") as output:
            output.write(candidate)
    sheets = recruit.portrait_sheets(ROOT, pages)
    write(OUT, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
                    clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=sha256(arm).hexdigest(),
                    target_COMMON_sha256=sha256(common).hexdigest(), allocations=allocations, records=rows,
                    instruction_changes=changes, regular_digit_cases=cases, sheets=sheets, native_pages=len(pages),
                    exact_parent_reserialize=True, translation_policy="natural-dialogue-v2", target_locale="en-US",
                    encoder="dialogue-relocatable-v1", review_gates=list(GATES), paired_gameplay_complete=False,
                    visual_review_complete=False, registered=False))
    print(f"Staged {len(edited)} text edits and {len(changes)} number calls. Verified {len(cases)} number cases and "
          f"{len(rows) * len(COUNTS)} native layouts.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", choices=("stage", "patch", "startup"), default="stage")
    action = parser.parse_args().action
    if action == "stage":
        main()
    else:
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(OUT), action)
