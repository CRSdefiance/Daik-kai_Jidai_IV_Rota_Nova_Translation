"""Review recruitment voices and compile the seven spare-capacity replies."""

from inspect import getsource
from pathlib import Path
from struct import pack

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_tavern_continuation_layout_v768 as formatter
from scripts import register_azores_return_20261123 as parent
from scripts import stage_recruit_crew_20261120 as recruitment
from scripts.observe_azores_return_20261123 import VISIT, VISIT_SHA
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_lisbon_azores_voyage_20261123 import load_exact
from scripts.verify_personal_gameplay_v841 import get_machine


ARM, COMMON, CLEAN, BASE = recruitment.ARM, recruitment.COMMON, recruitment.CLEAN, recruitment.BASE
ROOT = Path(".codex-release-work/recruitment_capacity_20261123")
ROM, PROOF = ROOT / "Recruitment_Capacity_STAGED.nds", ROOT / "stored_proof.json"
base, batch = recruitment.base, recruitment.batch
CAPACITY = 0x02118180
SHORTFALL = 0x021181A0
PARENT = 0x02053D24
WRAP_ENTRY = 0x01FFCF3C
COUNTS = (1, 9, 10, 67, 99, 100, 324, 999, 1000, 9999, 10000, 65535)
DRAFTS = {
    1042: ("There's room for %s more aboard. Shall I recruit more?",
           "The neutral first mate states the available room and asks a direct, polite question."),
    1043: ("Still room for %s more aboard. Should I recruit more?",
           "The brief first sentence preserves the practical, familiar voice and its sense of remaining room."),
    1044: ("There's room for %s more aboard. Would you like me to recruit more?",
           "The courteous offer remains intact, with its own line after the count."),
    1045: ("There's space aboard for %s more. Want me to round up more?",
           "The blunt question keeps the officer's casual round up and the exact remaining room."),
    1046: ("Seems we can fit %s more aboard. Shall I recruit some more?",
           "Seems preserves the tentative estimate and Shall I keeps the measured offer."),
    1047: ("Looks like we can take %s more. Should I find some more?",
           "The casual inference introduces the number of additional volunteers the ship can take."),
    1048: ("We have room for %s more aboard. Shall I keep recruiting?",
           "Manuel states the spare room plainly. His courteous follow-up fits together on the next line."),
}


def native_formatter():
    source = checked_text(getsource(formatter.format_case), {
        "raw = b' ' + row['english'].removesuffix('{PAD}').encode('ascii')": "raw = payload",
        "source_values):": "source_values, payload):",
        "    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)": """    key = row['message_id']
    table = CAPACITY if key >= 1042 else SHORTFALL
    for offset, value in ((0x264, PARENT), (0x270, 0), (0x274, key), (0x27C, table)):
        u.mem_write(STACK + offset, struct.pack('<I', value))
    for pointer, value in zip(pointers, values):
        assert bytes(u.mem_read(pointer, len(value) + 1)) == value + bytes(1)
    call(u, WRAP_ENTRY - BASE, (wrapped, output, 0), instruction_limit=2000000)""",
    })
    scope = vars(formatter) | dict(CAPACITY=CAPACITY, SHORTFALL=SHORTFALL, PARENT=PARENT, WRAP_ENTRY=WRAP_ENTRY)
    exec(compile(source, __file__ + "::voice-table-formatter", "exec"), scope)
    return scope["format_case"]


def compare(ctx, source, baseline, installed, deployed, snapshot):
    cpu, _ = get_machine(ctx.arm, snapshot)
    target = with_components(ctx, ctx.arm, deployed)
    loader, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    original = recruitment.catalogue(ctx.arm, ctx.common)
    assert original == baseline
    layout = native_formatter()
    raster, _, _ = recruitment.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    records, pages = [], []
    for key in range(1035, 1049):
        src, old, final = (book[key] for book in (source, original, installed))
        assert all(x.text.count(b"%s") == x.text.count(b"%") == 1 for x in (src, old, final))
        assert final.text.startswith(b" ") and b"\n" not in final.text and final.copy_end == old.copy_end
        assert bytes(loader.mem_read(get(0x5528C, key), len(final.text) + 1)) == final.text + b"\0"
        english, note = DRAFTS[key] if key in DRAFTS else recruitment.EDITS[key]
        assert english == final.text.decode("ascii").strip()
        decision = "revision" if key in DRAFTS else "retention"
        if key == 1039:
            decision, note = "wrap lead", "The original voice is gentle. At common headcounts the current formatter splits round up."
        elif key == 1041:
            decision, note = "wrap lead", "The original offer is measured. At common headcounts recruiting? sits alone."
        row = dict(message_id=key, id=f"COMMON_MESSAGE_{key}", file_path=COMMON,
            context="After the first recruiting attempt, the first mate reports the remaining required crew or the extra room aboard and asks whether to continue.",
            speaker="Recruiting first mate", source_meaning=recruitment.semantics(key), localization_note=note,
            decision=decision, english=english, English_argument_source_indices=[0],
            source_Japanese=src.text.decode("cp932"), source_reference=batch.reference(src), source_hex=src.text.hex(),
            current_reference=batch.reference(old), current_hex=old.text.hex(),
            registered_reference=batch.reference(final), installed_hex=final.text.hex(),
            review=dict.fromkeys(batch.GATES, True))
        row["review"]["formatting"] = decision != "wrap lead"
        samples = []
        for value in COUNTS:
            args = (str(value).encode("ascii"),)
            current = layout(cpu, row, args, old.text)
            result = layout(cpu, row, args, final.text)
            expected = english % str(value)
            assert " ".join(result["lines"]) == expected
            assert all(result["lines"]) and not set(result["findings"]) & {"four_row_width_bound"}
            if key in DRAFTS:
                lines = result["lines"]
                assert len(lines) == 2 and len(lines[-1]) >= 15
                assert lines[0].endswith((".", "Want")) or value >= 10000, (key, value, lines)
                assert lines[-1].endswith("?") and str(value) in lines[0]
                text = bytes.fromhex(result["formatted_hex"])
                plane, glyphs = recruitment.render_portrait(raster, ctx.arm, kanji, text)
                codes = [item["code"] for item in glyphs]
                assert codes == recruitment.glyph_codes(text)
                assert (codes[0], codes[-1]) == (ord(expected[0]), ord("?"))
                result["native_plane_sha256"] = batch.digest(bytes(plane))
                if value in (1, 67, 65535):
                    pages.append((f"{key} / {value} spare", plane))
            samples.append(result | dict(count=value, previous_lines=current["lines"]))
        row["cases"] = samples
        records.append(row)
    assert provider.reads
    return records, pages


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    ctx = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert batch.digest(ctx.arm) == release["target_ARM9_sha256"]
    assert batch.digest(ctx.common) == release["target_COMMON_sha256"]
    clean = base.NdsImage.open(CLEAN)
    assert all(ctx.arm[at - BASE:at - BASE + 32] == clean.read_file(ARM)[at - BASE:at - BASE + 32] == pack("<8i", *table)
               for at, table in recruitment.TABLES.items())
    source = batch.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    prior = recruitment.catalogue(ctx.arm, ctx.common)
    edited = {key: (" " + english).encode("ascii").ljust(len(prior[key].text), b" ")
              for key, (english, _) in DRAFTS.items()}
    assert all(len(data) == len(prior[key].text) for key, data in edited.items())
    deployed, after, allocations = owned_deployment(ctx.common, ctx.arm, prior, edited)
    assert {row.message_id for row, old in zip(after, prior, strict=True) if row != old} == set(DRAFTS)
    assert all(not slot["new_null_fields"] for slot in allocations.values())
    assert base.digest(VISIT) == VISIT_SHA
    visit = base.load(VISIT)
    assert visit["ROM_sha256"] == base.load(parent.parent.RELEASE)["candidate_sha256"]
    snapshot_ref, = [row for row in visit["read_only_pause_RAM_snapshots"] if row["frame"] == 18080]
    snapshot = load_exact(snapshot_ref)
    for start, end in ((0x5762C, 0x576A0), (0x53CB0, 0x53E4C), (0x53F4C, 0x53F9C),
                       (0xD7720, 0xD7740), (CAPACITY - BASE, SHORTFALL - BASE + 32)):
        assert ctx.arm[start:end] == snapshot[start:end]
    records, pages = compare(ctx, source, prior, after, deployed, snapshot)
    proof_1048 = records[-1]["cases"][3]
    assert proof_1048["count"] == 67 and proof_1048["previous_lines"] == [
        "There's still room for 67 more", "aboard. Shall I try", "recruiting more?"]
    image = ctx.image
    image.replace_file(COMMON, deployed)
    data = bytes(image.rom.save())
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == Path(release["candidate"]).read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(data)
    sheets = recruitment.portrait_sheets(ROOT, pages)
    for row in records:
        row["registered_reference"].update(candidate_sha256=base.digest(ROM), archive_sha256=batch.digest(deployed))
    proof = dict(candidate=str(ROM), candidate_sha256=base.digest(ROM), verified_predecessor_sha256=release["candidate_sha256"],
        clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=release["target_ARM9_sha256"],
        target_COMMON_sha256=batch.digest(deployed), whole_parent_inverse=True, allocations=allocations,
        original_voice_table=CAPACITY, snapshot=snapshot_ref, sheets=sheets, records=records,
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=batch.GATES)
    validate_natural_dialogue_batch(proof | {"records": [row for row in records if row["decision"] != "wrap lead"]})
    base.save(PROOF, proof)
    print(f"Staged seven capacity prompts and checked {len(records) * len(COUNTS)} original formatter cases.")


if __name__ == "__main__":
    main()
