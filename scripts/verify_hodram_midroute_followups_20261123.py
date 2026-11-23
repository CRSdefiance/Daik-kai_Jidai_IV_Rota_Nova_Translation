"""Check changed panels and each retained typed object in the staged Hodram ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import stage_hodram_midroute_followups_20261123 as stage
from scripts import verify_rafael_midroute_exchanges_20261122 as previous
from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.source_locked_derivation_v5118 import checked_text

base, native = stage.base, stage.native
GLYPHS = stage.ROOT / "glyph_and_sheet_verification.json"
CHOICES = stage.ROOT / "original_choice_tables.json"
STYLES = stage.ROOT / "original_style_alternatives.json"
SPIRIT = Path("releases/all_routes_editorial_20261122_hodram_early_and_midroute_wraps_candidate/verification/unchanged_FE_pages.json")

progressive_source = checked_text(getsource(stage.established.native_display), {
    'sum(bool(r["layouts"]) for r in checked)':
        'sum(bool(r["layouts"]) or r.get("modal_consumer", False) for r in checked)',
    '            before = bytes.fromhex(row["current_hex"])[1:].decode("ascii")':
        '            if raw[5] == 254:\n'
        '                checked.append(result | dict(modal_consumer=True))\n'
        '                continue\n'
        '            before = bytes.fromhex(row["current_hex"])[1:].decode("ascii")',
})
progressive = stage.compiler_scope | globals()
exec(compile(progressive_source, __file__ + "::progressive-renderer", "exec"), progressive)

modal_source = checked_text(previous.modal_source, {
    '            page = paint(body)':
        '            before = body\n'
        '            if b"FI" in body:\n'
        '                assert (block, ident, body) == (132, "DK4_MES_B132_R0145", b"FI\x27s Spirit rose by 1! ")\n'
        '                body = body.replace(b"FI", b"Hodram")\n'
        '            page = paint(body)\n'
        '            if before != body:\n'
        '                exact = spirit_proof(ctx, body, before, paint, page)\n'
        '                pictures.append((f"SC1 {ident} / maximum FI width", bytes.fromhex(exact["cropped_hex"])))',
    'physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex()))':
        'physical_plane_sha256=native.digest(plane), physical_plane_hex=plane.hex(),\n'
        '                maximum_name=exact["receipt"] if before != body else None))',
    'assert len(records) == 17 and not any(r["second_page"] for r in records)':
        'assert len(records) == 10 and not any(r["second_page"] for r in records)',
    '== [(118, "DK4_MES_B118_R0125")]':
        '== [(135, "DK4_MES_B135_R0035"), (136, "DK4_MES_B136_R0038")]',
    'Verified all 17 modal panels, including the reflowed Colosseum award.':
        'Verified ten modal panels and the maximum-width Spirit notice.',
})


def spirit_proof(ctx, default, stored, paint, page):
    baseline = base.load(SPIRIT)
    preserved, = [row for row in baseline["records"] if row["id"] == "DK4_MES_B91_R0103"]
    prior = SPIRIT.with_name("registered_release_verification.json")
    registered = base.load(prior)
    assert registered["candidate_sha256"] == baseline["candidate_sha256"]
    image = base.NdsImage.open(registered["candidate"])
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in stage.established.display.ASSETS)
    assert bytes.fromhex(preserved["exact_command_hex"])[6:].split(b"\x00",1)[0] == stored
    assert preserved["display_body_hex"] == default.hex()
    assert preserved["physical_plane_sha256"] == native.digest(page["physical"])
    maximum = stored.replace(b"FI", b"W" * 16)
    exact = preserved["maximum_name"]
    assert exact["body_hex"] == maximum.hex()
    wide = paint(maximum)
    plane = wide["physical"]
    assert wide["complete_consumed_bytes"] == len(maximum)
    assert not any(plane[12*228:]) and native.digest(plane) == exact["physical_plane_sha256"]
    cropped = b"".join(plane[y*228:y*228+216] for y in range(64))
    return dict(receipt=exact | dict(original_dependency=str(SPIRIT), original_sha256=base.digest(SPIRIT)),
                cropped_hex=cropped.hex())


modal = previous.modal | globals()
exec(compile(modal_source, __file__ + "::modal-renderer", "exec"), modal)
choice_source = checked_text(getsource(previous.check_choices), {
    'image.read_file("/data/SC0.DK4")': 'image.read_file("/data/SC1.DK4")',
    'len(choices) == 5': 'len(choices) == 8',
    'Verified all five original choice captions, slots and complete objects.':
        'Verified all eight original choice captions, slots and complete objects.',
})
exec(compile(choice_source, __file__ + "::native-choice-binding", "exec"), globals())


def check_styles():
    editorial, proof = map(base.load, (stage.REVIEW, stage.PROOF))
    candidate = base.digest(stage.ROM)
    assert proof["candidate_sha256"] == candidate
    group, = [g for g in proof["groups"] if (g["route"], g["block"]) == (1, 123)]
    command, = [c for c in group["commands"] if c["word"] == 0x4100]
    assert command["stored"] == command["current"]
    image = base.NdsImage.open(stage.ROM)
    archive = image.read_file("/data/SC1.DK4")
    payload = native.IlnkContainer.parse(archive).blocks[123]
    raw = bytes.fromhex(command["stored"])
    start = command["stored_offset"]
    assert native.digest(payload) == group["after"] and payload[start:start + len(raw)] == raw
    original, = [c for c in group["commands"] if c["source_offset"] == 16]
    originals = {r[3][0]:r for r in text_records(bytes.fromhex(original["source"]),0x4100)}
    previous_release = base.load(stage.parent.RELEASE)
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, previous_release["own_registered_startup"], captain=3)
    display = stage.established.display
    assert all(ctx.image.read_file(p) == image.read_file(p) for p in display.ASSETS)
    paint, font = display.clipped_renderer(ctx), image.read_file("/GRP/KANJI.FNT")
    styles = {tuple(r["slots"]): r for r in editorial["retained_style_variants"]}
    records, pictures = [], []
    for rel, selector, body, slots in text_records(raw, 0x4100):
        owner = styles.pop(tuple(slots))
        old_at, old_selector, old_body, old_slots = originals[slots[0]]
        assert (old_selector, old_slots) == (selector, slots) and selector == 208
        assert original["source_offset"] + old_at == owner["source_reference"]["offset"]
        assert old_body.hex() == owner["source_reference"]["exact_body_hex"]
        assert raw.hex() == owner["current_reference"]["exact_command_hex"]
        assert body.hex() == owner["current_reference"]["exact_body_hex"] and body.decode("ascii") == owner["english"]
        lines = [display.display.expected(owner["english"], {})]
        page, = display.display.raster(ctx, font, paint, body, lines, 1)
        assert page["native_independent_plane_equal"]
        pictures.append((f"{owner['id']} / slots {','.join(map(str, slots))}", bytes.fromhex(page["native_plane_hex"])))
        ref = dict(file_path="/data/SC1.DK4", block=123, archive_sha256=native.digest(archive),
                   block_sha256=group["after"], candidate_sha256=candidate, command_offset=start,
                   offset=start + rel, exact_command_hex=raw.hex(), exact_body_hex=body.hex())
        records.append(owner | dict(registered_reference=ref, review=owner["review"] | {"formatting": True}))
    assert not styles and len(records) == 5 and sorted(s for r in records for s in r["slots"]) == list(range(8))
    make = display.display.inherited.early.contact_sheets
    root = stage.ROOT / "styles"
    root.mkdir(exist_ok=True)
    sheets = FunctionType(make.__code__, make.__globals__ | {"ROOT":root})(pictures)
    for sheet in sheets:
        path = Path(sheet["path"])
        target = path.with_name("styles_" + path.name)
        path.rename(target)
        sheet["path"] = str(target)
    base.save(STYLES, dict(candidate_sha256=candidate, records=records, sheets=sheets, stored_table_exact=True,
                           current_native_body_rendering=True, live_personality_selection=False))
    print("Verified the five physical style bodies and all eight original slot assignments.", flush=True)


def formatting():
    if not stage.NATIVE.exists():
        progressive["native_display"]()
    if not GLYPHS.exists():
        glyphs = previous.verification.glyphs
        FunctionType(glyphs.verify.__code__, vars(glyphs) | dict(stage=stage, OUTPUT=GLYPHS))()
    if not stage.FE_PROOF.exists():
        modal["check_modal"]()
    if not CHOICES.exists():
        check_choices()
    if not STYLES.exists():
        check_styles()


if __name__ == "__main__":
    formatting()
