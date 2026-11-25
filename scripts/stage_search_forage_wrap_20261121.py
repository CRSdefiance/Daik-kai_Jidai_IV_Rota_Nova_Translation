"""Verify source-bound foraging paragraph breaks with both original amounts."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import search_forage_wrap_v1 as selector
from scripts import register_search_supply_and_fatigue_digits_20261121 as parent
from scripts import stage_search_supply_and_fatigue_digits_20261121 as previous
from scripts.stage_mutiny_review_v1 import compile_layouts
from scripts.stage_shared_notices_storage_v1 import relocate


base, shared = parent.base, parent.shared
ROOT = Path("work/search_forage_wrap_20261121")
ROM, PROOF = ROOT / "Search_Forage_Wrap_STAGED.nds", ROOT / "staged.json"
GROUP = {"consumer": 0x02053D44, "table": selector.TABLE, "original_role_argument": previous.ROLE}
LONGEST = ("4650", "3875")
AMOUNTS = ((0, 0), (5, 10), (105, 105), (175, 140), (4650, 3875), (20, 1500), (3900, 40))


def guarded_storage(rows):
    # Compile the widest source-bound expansion, then restore the substitutions.
    # All reachable amounts occupy one to four regular-width cells.
    marked, phrases = {}, {}
    for n, row in rows.items():
        english = row["english"]
        assert english.count("%s") == 2 and "%s barrels of water and %s barrels of food" in english
        widest = english % LONGEST
        phrases[n] = (f"{LONGEST[0]} barrels of water", f"and {LONGEST[1]} barrels of food{english[-1]}")
        marked[n] = dict(english=widest)
    compile_text = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {"PHRASES": phrases})
    storage = compile_text(marked)
    for n, cooked in storage.items():
        for amount in LONGEST:
            token = amount.encode("ascii")
            assert cooked.count(token) == 1
            cooked = cooked.replace(token, b"%s", 1)
        assert b" ".join(cooked.split()).decode("ascii") == rows[n]["english"]
        lead, water, food = (line.strip() for line in cooked.split(b"\n"))
        assert lead.endswith((b"found", b"found us"))
        assert water == b"%s barrels of water" and food == b"and %s barrels of food" + cooked[-1:]
        assert cooked.startswith(b" ") and cooked.count(b"\n  ") == 2
        storage[n] = cooked
    return storage


def main():
    assert not ROOT.exists()
    release, prior = map(base.load, (parent.RELEASE, parent.REVIEW))
    assert base.digest(parent.ROM) == release["candidate_sha256"] == prior["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(shared.CLEAN) == release["clean_input_sha256"]
    ctx = previous.common.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    clean = base.NdsImage.open(shared.CLEAN)
    clean_arm = clean.read_file(shared.ARM)
    source = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), clean_arm)
    old = shared.entries(ctx.image)
    rows = {r["message_ID"]: dict(r) for r in prior["records"] if r["message_ID"] in previous.FORAGE_IDS}
    assert set(rows) == set(previous.FORAGE_IDS)
    for n, row in rows.items():
        assert row["source_hex"] == source[n].text.hex() and row["current_hex"] == old[n].text.hex()
        assert row["source_reference"] == shared.workflow.reference(source[n])
        assert row["current_reference"] == shared.workflow.reference(old[n])
        assert old[n].text.decode("ascii") == row["english"]
        row.update(decision="wrap_only", localization_note=row["localization_note"] +
                   " Keep each number, the barrel unit, and its resource together on one row.")
        row.pop("text_display_fix")
    storage = guarded_storage(rows)
    directory = sha256(ctx.arm[shared.workflow.DIRECTORY_OFFSET:shared.workflow.TABLE_OFFSET]).hexdigest()
    pack = FunctionType(relocate.__code__, relocate.__globals__ | {"DIRECTORY": directory})
    common, metadata, packed, allocation = pack(ctx.common, ctx.arm, rows, storage)
    arm, runtime = selector.transform(metadata, sha256(metadata).hexdigest())
    revised = previous.common.discovery.with_components(ctx, arm, common)
    assert allocation["changed_visible_templates"] == sorted(rows) and allocation["all_41_blocks_fit_8KiB"]
    pending = base.load(shared.OUTPUT)["records"]
    assert len(pending) == 276 and all(packed[r["message_ID"]] == old[r["message_ID"]] for r in pending)
    for n, row in rows.items():
        row.update(staged_reference=shared.workflow.reference(packed[n]), staged_hex=packed[n].text.hex())
    raster, _, font = previous.common.discovery.mixed.font_tools(ctx.image)
    kanji = ctx.image.read_file("/GRP/KANJI.FNT")
    _, get = previous.get_machine(ctx.arm, ctx.raw)
    actor_ids = {}
    for actor in range(207):
        key = get(0x53F4C, ctx.actor_root + 4 + 32 * actor, selector.TABLE)
        if key in rows:
            actor_ids.setdefault(key, actor)
    assert actor_ids.keys() == rows.keys()
    assert get(0x53F4C, ctx.actor_root + 4 + 32 * 18, selector.TABLE) == 2229
    actor_ids[2229] = 18
    portrait = previous.with_arguments()
    cases, sheets = [], []
    for n, row in rows.items():
        for water, food in AMOUNTS:
            args = (str(water).encode("ascii"), str(food).encode("ascii"))
            old_display = portrait(ctx, row, GROUP, old[n].text, actor_ids[n], args)["display"]
            formatted = portrait(revised, row, GROUP, packed[n].text, actor_ids[n], args)["display"]
            for context in (ctx, revised):
                context.calls.clear()
            assert formatted == packed[n].text % args and formatted != old_display
            body = packed[n].text % args
            lines = tuple(line.strip().decode("ascii") for line in body.split(b"\n"))
            assert " ".join(lines) == row["english"] % (water, food)
            assert lines[1:] == (f"{water} barrels of water", f"and {food} barrels of food{row['english'][-1]}")
            assert len(lines) == 3 and all(0 < len(line) <= 35 for line in lines)
            pixels, glyphs = previous.render_portrait(raster, arm, kanji, formatted)
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (ord(lines[0][0]), ord(lines[-1][-1]))
            cases.append(dict(message_ID=n, water_and_food=[water, food], lines=lines,
                              before_hex=old_display.hex(), after_hex=formatted.hex(), pages=1,
                              glyphs=len(glyphs), ink_sha256=sha256(pixels).hexdigest()))
            sheets.append((f"{n} {water} / {food}", pixels))
    bundle = {key: prior[key] for key in ("translation_policy", "encoder", "target_locale", "review_gates")}
    bundle["records"] = list(rows.values())
    validate_natural_dialogue_batch(bundle)
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(shared.ARM, arm)
    image.replace_file(shared.COMMON, common)
    result = bytes(image.rom.save())
    image.replace_file(shared.ARM, ctx.arm)
    image.replace_file(shared.COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    base.save(PROOF, bundle | dict(candidate_sha256=base.digest(ROM), parent_sha256=release["candidate_sha256"],
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        exact_parent_inverse=True, runtime=runtime, allocation=allocation, source_water_before_food=True,
        native_display_cases=cases, font=font, sheets=previous.portrait_sheets(ROOT, sheets),
        emulator_and_visual_gate_pending=True, new_editorial_credit=0,
        source_evidence={str(p): base.digest(p) for p in (parent.RELEASE, parent.REVIEW, shared.OUTPUT)}))
    print(f"Verified {len(cases)} three-row portraits with both complete quantities and the original wording.")


if __name__ == "__main__":
    main()
