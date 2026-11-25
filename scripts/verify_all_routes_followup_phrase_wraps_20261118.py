"""Verify all stored revisions and retentions in the original renderer."""

from types import FunctionType

from scripts import stage_all_routes_followup_phrase_wraps_20261118 as build
from scripts import verify_all_routes_next_phrase_wraps_20261118 as prior

base, native, ASSETS = build.base, build.native, prior.ASSETS
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def verify():
    assert not ROOT.exists()
    stored, draft, released = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert draft["previous_sha256"] == released["candidate_sha256"] == base.digest(build.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT) and stored["whole_parent_inverse"]
    image = base.NdsImage.open(build.ROM)
    # This initializes the same four exact name contexts already verified in the preceding release.
    contexts = prior.native_routes(base.load(build.parent.parent.RELEASE))
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for ctx in contexts.values() for asset in ASSETS)
    expand = prior.original_expander()
    names = prior.route_names(contexts, expand)
    assert {str(route): data for route, data in names.items()} == base.load(build.parent.display.PROOF)["default_name_macros"]
    arm, font = (image.read_file(asset) for asset in (ASSETS[0], ASSETS[2]))
    paint, paint_cp932 = prior.clipped_renderer(contexts[0]), prior.prior.original_cp932_renderer(arm)
    paragraph = FunctionType(prior.display.paragraph.__code__, vars(prior.display) | {"build": build})
    banks = {route: native.IlnkContainer.parse(image.read_file(f"/data/SC{route}.DK4")) for route in contexts}
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    modified, retained, pictures = [], [], []
    for group in stored["groups"]:
        route, path, number = (group[k] for k in ("route", "file_path", "block"))
        block = banks[route].blocks[number]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = rows[path, ident]
            raw, at = bytes.fromhex(cmd["stored"]), cmd["stored_offset"]
            assert block[at:at + len(raw)] == raw and cmd["word"] == row["native_command_word"]
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"] < 207
            if row["decision"] == "retention":
                assert cmd["stored"] == cmd["current"] and value.hex() == row["current_hex"]
                body = prior.prior.default_text(value[1:], names[route])
                rendered = (paint if body.isascii() else paint_cp932)(arm, font, body)
                assert rendered["complete_consumed_bytes"] == len(body)
                assert all(p["native_independent_plane_equal"] for p in rendered["pages"])
                retained.append(dict(id=ident, file_path=path, stored_hex=value.hex(),
                    pages=[dict(page=p["page"], native_plane_sha256=native.digest(bytes.fromhex(p["native_plane_hex"])))
                           for p in rendered["pages"]]))
                continue
            plan = group["plans"][ident]
            assert not build.review.TOKEN.findall(row["english"])
            entry = paragraph(contexts[route], font, paint, expand, None, names[route], row, value, plan)
            diagnostics = plan["diagnostics"]
            assert all(d["severity"] == "warning" and d["code"] == "line-break-count" for d in diagnostics)
            layout, = entry["layouts"]
            page, = layout["pages"]
            pictures.append((f"SC{route} {ident}", bytes.fromhex(page["native_plane_hex"])))
            modified.append(entry | {"informational_source_row_differences": diagnostics})
    assert {(r["file_path"], r["id"]) for r in modified + retained} == rows.keys()
    assert len(modified) == 18 and len(retained) == 151 and len(pictures) == 18
    contact = prior.display.inherited.early.contact_sheets
    ROOT.mkdir()
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_assets_byte_identical=True, default_name_macros=names, renderer_assets=ASSETS,
        revision_count=len(modified), fresh_page_count=len(pictures), retention_count=len(retained), 
        checked_records=modified, retained_records=retained, contact_sheets=sheets, actual_gameplay=False))
    print("Verified 18 revised pages and 151 exact retentions.")


if __name__ == "__main__":
    verify()
