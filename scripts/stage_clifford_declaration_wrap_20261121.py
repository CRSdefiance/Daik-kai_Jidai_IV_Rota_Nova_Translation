"""Validate a wrap-only correction in the original declaration portrait consumer."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.patch import clifford_declaration_wrap_v1 as selector
from scripts import checkpoint_fleet_attack_shared_20261121 as gameplay
from scripts import stage_bubble_portrait_wraps_20261120 as portrait
from scripts.stage_shared_notices_storage_v1 import relocate


base, parent, shared = gameplay.base, gameplay.replay.current, gameplay.shared
ROOT = Path("work/clifford_declaration_wrap_20261121")
ROM, PROOF = ROOT / "Clifford_Declaration_Wrap_STAGED.nds", ROOT / "staged.json"
PRIOR = Path("translations/declaration_responses_contextual_final_review_v1.json")
N = 2205
GROUP = {"consumer": 0x02053F0C, "table": selector.TABLE, "original_role_argument": None}
LINES = ("What?! They've declared war on me?!", "Ha! Do they really think", "they can beat me?")


def digest(data):
    return sha256(data).hexdigest()


def main():
    assert not ROOT.exists()
    release, original, actual = map(base.load, (parent.RELEASE, PRIOR, gameplay.OUTPUT))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == actual["candidate_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    ctx = portrait.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(shared.CLEAN)
    clean_arm = clean.read_file(shared.ARM)
    keys = tuple(range(2201, 2209))
    directory = digest(ctx.arm[portrait.DIRECTORY_OFFSET:portrait.TABLE_OFFSET])
    source = portrait.common_message_entries(clean.read_file(shared.COMMON), clean_arm)
    current = shared.entries(ctx.image)
    before_records = {row["message_id"]: row for row in original["records"]}
    assert before_records.keys() == set(keys)
    row = next(r for r in actual["records"] if r["message_ID"] == N)
    original_choice = before_records[N]
    native_proof = Path(original_choice["current_native_declaration_responses_font_proof"])
    original_native = {row["message_ID"]: row for row in base.load(native_proof)["all8_complete_native_cases"]}
    english = " ".join(LINES)
    assert row["speaker"] == "James Clifford" and original_native[N]["existing_actor_ID"] == 28
    assert row["source_hex"] == source[N].text.hex() == original_choice["source_hex"]
    assert row["current_hex"] == current[N].text.hex()
    assert english == portrait.unwrapped(current[N].text) == original_choice["english"]
    assert b"%" not in source[N].text and b"%" not in current[N].text
    row.update(english=english, previous_English=english, id=f"COMMON_MESSAGE_{N}",
               file_path=shared.COMMON, context=original_choice["context"], source_meaning=original_choice["source_meaning"],
               decision="wrap_only", original_substitution_count=0,
               review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True))

    compiler = portrait.compile_layouts
    wrap = FunctionType(compiler.__code__, compiler.__globals__ | {
        "PHRASES": {N: (LINES[0], LINES[2])},
    })
    storage = wrap({N: row})
    pack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    common, metadata, packed, allocation = pack(ctx.common, ctx.arm, {N: row}, storage)
    arm, runtime = selector.transform(metadata, digest(metadata))
    target = portrait.with_components(ctx, arm, common)
    assert allocation["changed_visible_templates"] == [N] and allocation["all_41_blocks_fit_8KiB"]
    assert all(portrait.reference(packed[n]) == portrait.reference(current[n])
               for n in (r["message_ID"] for r in base.load(shared.OUTPUT)["records"]))
    raster, _, font = portrait.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")

    views, sheets = [], []
    for n in keys:
        old_record = before_records[n]
        assert old_record["source_hex"] == source[n].text.hex()
        assert old_record["english"] == portrait.unwrapped(current[n].text)
        actor = original_native[n]["existing_actor_ID"]
        assert (actor == 28) == (n == N)
        old = portrait.portrait_case(ctx, {"message_ID": n}, GROUP, current[n].text, actor).pop("display")
        assert old.hex() == original_native[n]["native_pipeline"]["formatted_hex"]
        new = portrait.portrait_case(target, {"message_ID": n}, GROUP, packed[n].text, actor).pop("display")
        assert (old != new) == (n == N)
        pixels, glyphs = portrait.render_portrait(raster, arm, kanji, new)
        old_pixels, _ = portrait.render_portrait(raster, ctx.arm, kanji, old)
        codes = [g["code"] for g in glyphs]
        assert codes == portrait.glyph_codes(new) and codes[0] == new.strip()[0] and codes[-1] == new.strip()[-1]
        assert (pixels != old_pixels) == (n == N)
        lines = tuple(line.strip() for line in new.decode("ascii").splitlines())
        assert " ".join(lines) == old_record["english"] and 1 <= len(lines) <= 4
        assert all(0 < len(line) <= 36 for line in lines)
        if n == N:
            assert lines == LINES
            sheets.extend((("Clifford before", old_pixels), ("Clifford corrected", pixels)))
        views.append(dict(message_ID=n, original_actor=actor, before_hex=old.hex(), after_hex=new.hex(),
                          lines=lines, ink_sha256=digest(pixels), glyph_count=len(glyphs)))
    row.update(staged_reference=portrait.reference(packed[N]), staged_hex=packed[N].text.hex())
    review = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
                  encoder="dialogue-relocatable-v1", review_gates=sorted(REQUIRED_REVIEW_GATES), records=[row])
    validate_natural_dialogue_batch(review)

    image = base.NdsImage.open(parent.ROM)
    image.replace_file(shared.ARM, arm)
    image.replace_file(shared.COMMON, common)
    binary = bytes(image.rom.save())
    image.replace_file(shared.ARM, ctx.arm)
    image.replace_file(shared.COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(binary)
    base.save(PROOF, review | dict(candidate_sha256=digest(binary), parent_sha256=release["candidate_sha256"],
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(common), all_parent_bytes_restored=True,
        allocation=allocation, runtime=runtime, native_views=views, font=font, new_editorial_credit=0,
        sheets=portrait.portrait_sheets(ROOT, sheets), emulator_and_visual_gate_pending=True,
        source_evidence={str(path): base.digest(path) for path in (parent.RELEASE, PRIOR, gameplay.OUTPUT, native_proof)}))
    print("Validated all eight original declaration portraits. Only Clifford's wrap changed.")


if __name__ == "__main__":
    main()
