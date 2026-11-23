"""Check progressive dialogue and Charlotte's five FE picture panels."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_rafael_tradehouse_festival_20261121 as stage
from scripts import verify_rafael_pereira_village_20261121 as prior
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows
from scripts.source_locked_derivation_v5118 import checked_text


base, native, town, display = stage.base, stage.native, prior.town, prior.display
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def festival_panel(ctx, expand, fe, names, row, body, group):
    tokens = stage.review.TOKEN.findall(row["english"])
    expanded = body
    bindings = None
    if tokens:
        assert row["decision"] == "retention" and tokens == ["FI"]
        bindings = ctx.execute(expand, body, 0)
        expanded = body.replace(b"FI", names["FI"].encode("ascii"))
        assert {case["output_hex"] for case in bindings["cases"]} == {expanded.hex()}
    result = fe(expanded)
    assert result["complete_consumed_bytes"] == len(expanded)
    membership = check_FE_rows(expanded, result)
    if row["decision"] == "revision":
        plan = group["plans"][row["id"]]
        encoded = bytes.fromhex(plan["encoded_hex"])
        assert b"\xfe" + body in (encoded, encoded + b" ")
        assert plan["expected_native_pages"] == 1 and membership["actual_rows"] == plan["lines"]
        assert stage.review.logical(body.decode("ascii")) == row["english"]
    plane = result["physical"]
    assert len(plane) == 228 * 64
    return plane, dict(festival_FE=True, native_pages=1, expanded_hex=expanded.hex(),
                       panel_mask_sha256=native.digest(plane), native_rows=membership, original_expansion=bindings)


def festival_sheet(previews, contact):
    source = checked_text(getsource(contact), {
        "(888,": "(936,",
        "index % 2 * 444": "index % 2 * 468",
        "(216,64)": "(228,64)",
        "(432,128)": "(456,128)",
        "before_after_": "festival_fe_",
    })
    scope = contact.__globals__ | {"ROOT": ROOT}
    exec(compile(source, __file__ + "::FE-contact-sheet", "exec"), scope)
    return scope["contact_sheets"](previews)


source = checked_text(getsource(prior.main), {
    "    records, previews = [], []": "    records, previews, fe_sheets = [], [], []",
    '    for group in stored["groups"]:': '    for group in sorted(stored["groups"], key=lambda g: g["block"] != 69):',
    '''            if row["decision"] == "retention":
                assert old == new and new[5:end].hex() == row["current_hex"]
                if selector == 254:
                    result = fe(body)
                    assert result["complete_consumed_bytes"] == len(body)
                    entry.update(retained_system_panel=True, native_pages=1,
                                 panel_mask_sha256=native.digest(result["physical"]))
            else:''':
        '''            if selector == 254:
                assert block == 69
                assert (old == new) == (row["decision"] == "retention")
                plane, proof = festival_panel(ctx, expand, fe, names, row, body, group)
                entry.update(proof)
                fe_sheets.append((ident, plane))
            elif row["decision"] == "retention":
                assert old == new and new[5:end].hex() == row["current_hex"]
            else:''',
    "    assert len(records) == 197 and not rows and revised_pages == 110":
        "    assert len(records) == 200 and not rows and revised_pages == 92",
    '    assert sum(bool(r.get("retained_system_panel")) for r in records) == 1':
        '    assert len(fe_sheets) == 5 and sum(r.get("festival_FE", False) and r["decision"] == "revision" for r in records) == 2',
    '    base.save(PROOF,': '    sheets.extend(festival_sheet(fe_sheets, contact))\n    base.save(PROOF,',
    'revised_pages=revised_pages, name_stress_pages=': 'revised_pages=revised_pages + 2, festival_FE_panels=5, name_stress_pages=',
    'print(f"Verified {revised_pages} native pages, {len(previews) - revised_pages} name-width cases, and the retained FE notice.")':
        'print(f"Verified {revised_pages} progressive revisions, five FE panels including two revisions, and {len(previews) - revised_pages} name-width cases.")',
})
scope = vars(prior) | globals()
exec(compile(source, __file__ + "::native-festival-pages", "exec"), scope)


def refresh_regional_reference():
    """Carry forward only exact command/plan pairs with identical renderer assets."""
    assert not ROOT.exists()
    earlier = stage.ROOT.with_name("staged_v2")
    prior_receipt = earlier / "native_display/native_display.json"
    old, previous, final, review = map(base.load, (prior_receipt, earlier / stage.PROOF.name, stage.PROOF, stage.OUTPUT))
    predecessor_rom = earlier / stage.ROM.name
    assert old["candidate_sha256"] == previous["candidate_sha256"] == base.digest(predecessor_rom)
    assert old["stage_proof_sha256"] == base.digest(earlier / stage.PROOF.name)
    assert final["candidate_sha256"] == base.digest(stage.ROM) and final["manuscript_sha256"] == base.digest(stage.OUTPUT)
    assert previous["predecessor_sha256"] == final["predecessor_sha256"]
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in old["sheets"])
    before, image = map(base.NdsImage.open, (predecessor_rom, stage.ROM))
    assert all(before.read_file(asset) == image.read_file(asset) for asset in display.ASSETS)
    bank = native.IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks
    arm, font = (image.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    context = SimpleNamespace(arm=arm, image=image)
    paint = display.clipped_renderer(context)
    old_rows = {r["id"]: r for r in old["records"]}
    old_plans = {k: value for group in previous["groups"] for k, value in group["plans"].items()}
    new_rows = {r["id"]: r for r in review["records"]}
    records, previews, refreshed = [], [], []
    for group in final["groups"]:
        block = group["block"]
        assert native.digest(bank[block]) == group["after"]
        for cmd in group["commands"]:
            at, raw = cmd["stored_offset"], bytes.fromhex(cmd["stored"])
            assert bank[block][at:at + len(raw)] == raw
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            older, row = old_rows.pop(ident), new_rows.pop(ident)
            entry = older | dict(stored_offset=at, stored_command_hex=raw.hex())
            plan = group["plans"].get(ident)
            if older["stored_command_hex"] != raw.hex() or old_plans.get(ident) != plan:
                assert ident == "DK4_MES_B70_R0018" and plan["expected_native_pages"] == 1
                end = raw.index(0, 6)
                encoded = bytes.fromhex(plan["encoded_hex"])
                assert raw[5:end] in (encoded, encoded + b" ") and not any(raw[end:])
                assert raw[6:end].isascii() and not stage.review.TOKEN.findall(row["english"])
                body = raw[6:end]
                assert stage.review.logical(body.decode("ascii")) == row["english"]
                page, = display.display.raster(context, font, paint, body, plan["lines"], 1)
                assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                pixels = bytes.fromhex(page["native_plane_hex"])
                entry["layouts"] = [dict(scope="registered default", expanded_hex=body.hex(),
                                         plane_sha256=native.digest(pixels), lines=plan["lines"])]
                refreshed.append(ident)
                previews.append((ident, pixels))
            records.append(entry)
    assert not old_rows and not new_rows and refreshed == ["DK4_MES_B70_R0018"]
    ROOT.mkdir()
    contact = display.display.inherited.early.contact_sheets
    fresh = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(previews)
    base.save(PROOF, old | dict(candidate_sha256=final["candidate_sha256"], stage_proof_sha256=base.digest(stage.PROOF),
                               records=records, sheets=old["sheets"] + fresh, refreshed=refreshed,
                               earlier_native_receipt=str(prior_receipt), earlier_native_sha256=base.digest(prior_receipt)))
    print("Verified the corrected regional reference and rebound exact native evidence for the other 199 records.")


if __name__ == "__main__":
    if stage.ROOT.name == "staged_v2":
        scope["main"]()
    else:
        refresh_regional_reference()
