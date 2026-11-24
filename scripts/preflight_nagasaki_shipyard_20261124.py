"""Check the three revised Yard paragraphs through their original consumers."""

from pathlib import Path

from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import probe_shipyard_runtime_v759 as shipyard
from scripts import stage_recruit_crew_20261120 as portraits
from scripts import verify_nagasaki_shipyard_20261124 as yard
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.verify_personal_gameplay_v841 import get_machine


OUT = yard.OUT.with_name("nagasaki_yard_preflight_20261124.json")
ROOT = OUT.with_suffix("")
NATIVE_ROOT = ROOT / "refit"
NATIVE_MANUSCRIPT = ROOT / "refit_manuscript.json"
ROM = yard.play.current.ROM


def refit_font():
    verifier = Path("scripts/verify_refit_editorial_v830.py")
    source = checked_text(verifier.read_text(encoding="utf-8"), {
        "from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT":
            "from scripts.preflight_nagasaki_shipyard_20261124 import NATIVE_MANUSCRIPT as MANUSCRIPT, ROM, NATIVE_ROOT as ROOT",
        "        compiled, lines = compile_paragraph(record['english'])":
            "        compiled, lines = compile_paragraph(record['english'])\n"
            "        assert compiled[:-1] == bytes.fromhex(record['payload_hex']).rstrip(b' ')\n"
            "        compiled = bytes.fromhex(record['payload_hex']) + b'\\0'",
        "(line_index * 12 + y) * 168": "(line_index * 12 + y + 1) * 168",
        "assert actual == expected": "assert actual == expected, (record['message_id'], lines)",
        "All31 current native fonts/independent complete planes/guards pass;four sheets await visual review.":
            "Both revised Refit sail pages passed the native font and padding check.",
    })
    scope = dict(__name__="__main__", __file__=__file__)
    exec(compile(source, __file__ + "::verified-Refit-font", "exec"), scope)
    return reference(NATIVE_ROOT / "native_font_verification.json")


def rename_font(ctx, current, proposed, actual_lines):
    cpu, _ = get_machine(ctx.arm, ctx.raw)
    before, after = [shipyard.layout(cpu, text, 1264, ()) for text in (current, proposed)]
    assert before["lines"] == actual_lines and after["lines"] == [yard.PROPOSALS[1264]]
    assert not after["findings"]
    raster, _, _ = portraits.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    text = bytes.fromhex(after["formatted_hex"])
    plane, glyphs = portraits.render_portrait(raster, ctx.arm, kanji, text)
    codes = [glyph["code"] for glyph in glyphs]
    assert codes == portraits.glyph_codes(text) and codes[0] == ord("W") and codes[-1] == ord("?")
    return dict(previous=before, revised=after, full_plane_sha256=sha256(bytes(plane)).hexdigest(),
                sheets=portraits.portrait_sheets(ROOT, [("1264 / rename prompt", plane)]))


def main():
    current = yard.play.current
    receipt, packet = map(read, (current.RELEASE, yard.OUT))
    assert packet["ordinary_gameplay"] and packet["candidate_sha256"] == receipt["candidate_sha256"]
    assert digest(REGISTRY) == receipt["registry_sha256"] and digest(CLEAN) == receipt["clean_input_sha256"]
    ctx = RegisteredRuntime(current.RELEASE, receipt["own_registered_startup"], captain=3)
    assert sha256(ctx.arm).hexdigest() == receipt["target_ARM9_sha256"] and sha256(ctx.common).hexdigest() == receipt["target_COMMON_sha256"]
    stock = NdsImage.open(CLEAN)
    source = yard.common_message_entries(stock.read_file(current.COMMON), stock.read_file(current.ARM))
    before = yard.common_rows(ctx.common, ctx.arm)
    observations = {row["message_ID"]: row for row in packet["records"]}
    edits, reviews = {}, []
    for key, english in yard.PROPOSALS.items():
        row, old = observations[key], before[key]
        assert yard.panels.text_reference(source[key]) == row["source"]
        assert yard.panels.text_reference(old) == row["installed"] and english == row["proposed_english"]
        assert b"%" not in source[key].text + old.text and "%" not in english
        if key == 1264:
            body = b" " + english.encode("ascii")
            assert len(english) <= 35
            context = "The shipwright asks Maria which existing ship to rename before opening the selection list."
            meaning = "Which ship do you want to rename?"
        else:
            body = compile_paragraph(english)[0][:-1]
            assert max(map(len, body.split(b"\n"))) <= 28
            context = "The player compares the adjacent sails in Refit equipment."
            meaning = ("Lateen sails perform well upwind. A square sail cannot be fitted behind a lateen sail." if key == 1285
                       else "Square sails perform well in a following wind. A lateen sail cannot be fitted ahead of a square sail.")
        edits[key] = body.ljust(len(old.text), b" ")
        assert len(edits[key]) == len(old.text)
        if key != 1264:
            assert len(edits[key].split(b"\n")[-1]) <= 28
        reviews.append(dict(id=f"COMMON_MESSAGE_{key}", message_id=key, english=english,
            speaker=row["speaker"] or "Refit equipment help", context=context, source_meaning=meaning,
            localization_note=row["rationale"], review=dict.fromkeys(GATES, True), editorial_decision="revision",
            source_reference=row["source"], current_reference=row["installed"], payload_hex=edits[key].hex()))
    archive, final, slots = owned_deployment(ctx.common, ctx.arm, before, edits)
    assert [a.message_id for a, b in zip(before, final, strict=True) if a != b] == sorted(edits)
    assert all(not slot["new_null_fields"] for slot in slots.values())
    policy = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                  review_gates=list(GATES), records=reviews)
    validate_natural_dialogue_batch(policy)
    NATIVE_ROOT.mkdir(parents=True)
    write(NATIVE_MANUSCRIPT, policy | dict(current_candidate_sha256=receipt["candidate_sha256"], records=reviews[1:]))
    checked_help = refit_font()
    checked_rename = rename_font(ctx, before[1264].text, edits[1264], observations[1264]["actual_lines"])
    write(OUT, policy | dict(candidate_sha256=receipt["candidate_sha256"], gameplay=reference(yard.OUT),
        exact_storage_slots=slots, proposed_archive_sha256=sha256(archive).hexdigest(), old_archive_recovers_byte_exactly=True,
        checked_refit_pages=checked_help, checked_rename_prompt=checked_rename,
        native_input=ctx.receipt() | {"captain": 3}, new_gameplay=False, ROM_changed=False))
    print("Verified original formatting and fixed-slot storage for all three Yard revisions.")


if __name__ == "__main__":
    main()
