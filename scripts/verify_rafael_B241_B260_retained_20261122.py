"""Verify all retained letter alternatives and choice captions in B241–260."""

from pathlib import Path
from types import FunctionType

from scripts import review_rafael_B241_B260_20261122 as review
from scripts import verify_rafael_B221_B240_20261122 as precedent
from scripts.verify_rafael_gerhard_tutorial_20261121 import menu, verify_menu


base, native = review.base, review.paired.native
ROOT = review.paired.ROOT / "retained_display"
PROOF = ROOT / "native_display.json"
draft_path = review.OUTPUT


def main():
    assert not PROOF.exists()
    draft = base.load(draft_path)
    current = review.paired.parent.ROM
    assert draft["previous_sha256"] == base.digest(current)
    assert draft["source_packet_sha256"] == base.digest(review.paired.PAIRED)
    images = [base.NdsImage.open(path) for path in (native.CLEAN, current)]
    ctx = precedent.scope["current_runtime"](images[1])
    arms = [image.read_file(native.ARM) for image in images]
    banks = [native.IlnkContainer.parse(image.read_file(precedent.PATH)).blocks for image in images]
    renderer = precedent.display.clipped_renderer(ctx)
    font = images[1].read_file("/GRP/KANJI.FNT")
    inventory, _, _ = native.scoped_inventory()
    check_menu = FunctionType(verify_menu.__code__, verify_menu.__globals__ | {"ROOT": ROOT})
    adapters = menu.adapters(arms[1])

    panels, menus, entries = [], [], []
    ROOT.mkdir(exist_ok=True)
    for block in review.DECISIONS:
        rows = [r for r in draft["records"] if r["block"] == block]
        originals, installed = [{r["offset"]: r for r in inventory(arm, selected[block])[0]}
                                for arm, selected in zip(arms, banks, strict=True)]
        first = rows[0]
        left, right = first["source_reference"]["command_offset"], first["current_reference"]["command_offset"]
        if first["kind"] == "typed-choice-label":
            record = dict(source_offset=left, stored_offset=right, current=installed[right]["whole_command_hex"],
                stored=installed[right]["whole_command_hex"], record_ids=[r["id"] for r in rows])
            menu_record = check_menu(ctx.arm, originals, record, rows, adapters)
            menus.append(menu_record | {"block": block})
            entries.extend(dict(id=r["id"], block=block, exact_menu_command=record["stored"], slots=r["native_slots"]) for r in rows)
            continue
        source, stored = [bytes.fromhex(obj["whole_command_hex"]) for obj in (originals[left], installed[right])]
        for row, offset, jp, current_body, same in precedent.styles.parts(source, stored, stored, rows):
            assert current_body == same and jp.hex() == row["source_hex"] and same.hex() == row["current_hex"]
            assert right + offset == row["current_reference"]["offset"]
            lines = [line.strip() for line in same.decode("ascii").splitlines()]
            assert " ".join(lines) == row["english"]
            page, = precedent.display.display.raster(ctx, font, renderer, same, lines, 1)
            assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
            plane = bytes.fromhex(page["native_plane_hex"])
            panels.append((row["id"], plane))
            entries.append(dict(id=row["id"], block=block, source_ref=row["source_reference"],
                current_ref=row["current_reference"], slots=row["native_slots"], lines=lines, plane_sha256=native.digest(plane)))
    assert len(entries) == 20 and len(panels) == 14 and [m["count"] for m in menus] == [2, 2, 2]
    make_sheets = precedent.scope["prior"].precedent.prior.sheet
    sheet = FunctionType(make_sheets.__code__, make_sheets.__globals__ | {"ROOT": ROOT})
    visuals = sheet(panels, "retained_letter_variants", 216) + [m["sheet"] for m in menus]
    base.save(PROOF, dict(candidate_sha256=draft["previous_sha256"], draft=str(draft_path), draft_sha256=base.digest(draft_path),
        verified_records=entries, native_menu_cases=menus, sheets=visuals, unchanged_installed_text=True,
        initialized_dependencies=ctx.receipt(), offline_native_only=True))
    print("Verified 14 letter variants and the six original choice captions on the published ROM.")


if __name__ == "__main__":
    main()
