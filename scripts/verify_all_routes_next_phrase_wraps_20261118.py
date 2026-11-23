"""Check revised pages and all four native name contexts."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import generic_name_macro_owned_v5886b as macro
from scripts import stage_all_routes_next_phrase_wraps_20261118 as build
from scripts import verify_london_guild_assignments_20261118 as display
from scripts import verify_rafael_next_phrase_wraps_20261118 as prior
from scripts import verify_story_phrase_continuity_20261118 as contexts
from scripts.source_locked_derivation_v5118 import checked_text

base, native, ASSETS = build.base, build.native, prior.ASSETS
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def original_expander():
    source = checked_text(getsource(macro.expand), {
        "assert identity==prefix and captain==2": "assert identity == prefix and captain in range(4)",
    })
    scope = vars(macro).copy()
    exec(compile(source, __file__ + "::original-name-processor", "exec"), scope)
    return scope["expand"]


def native_routes(release):
    earlier = base.load(build.parent.display.PROOF)["previous_initialized_rafael_context"]
    boot, identity = map(Path, (earlier["path"], earlier["identity"]))
    assert base.digest(boot) == earlier["sha256"] and base.digest(identity) == earlier["identity_sha256"]
    return {
        0: native.RegisteredRuntime(identity, boot, captain=0),
        1: contexts.hodram_context(),
        2: contexts.routes.lil_context(),
        3: native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3),
    }


def route_names(routes, expand):
    named = {}
    for route, expected in enumerate(("Rafael", "Hodram", "Lil", "Maria")):
        out = routes[route].execute(expand, b"FI FA FO", route)["cases"]
        assert len(out) == 4
        result, = {case["output_hex"] for case in out}
        given, surname, company = bytes.fromhex(result).decode("ascii").split(" ", 2)
        assert given == expected and 1 <= len(surname) <= 16 and 1 <= len(company) <= 20
        named[route] = {"FI": given, "FA": surname, "FO": company}
    return named


def clipped_renderer(ctx):
    return display.inherited.early.prior.precedent.planners(ctx.arm)[1]


def verify():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert stored["candidate_sha256"] == base.digest(build.ROM)
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(build.parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT) and stored["whole_parent_inverse"]
    image = base.NdsImage.open(build.ROM)
    routes = native_routes(release)
    assert all(ctx.image.read_file(asset) == image.read_file(asset) for ctx in routes.values() for asset in ASSETS)
    expand = original_expander()
    names = route_names(routes, expand)
    arm, font = (image.read_file(asset) for asset in (ASSETS[0], ASSETS[2]))
    paint = clipped_renderer(routes[0])
    earlier = build.ROOT.with_name("research_v1")
    earlier_proof = earlier / ROOT.name / PROOF.name
    earlier_stored = earlier / build.PROOF.name
    first, previous = map(base.load, (earlier_proof, earlier_stored))
    earlier_rom = earlier / build.ROM.name
    assert first["candidate_sha256"] == previous["candidate_sha256"] == base.digest(earlier_rom)
    assert first["stage_proof_sha256"] == base.digest(earlier_stored)
    assert previous["predecessor_sha256"] == stored["predecessor_sha256"]
    old_image = base.NdsImage.open(earlier_rom)
    assert all(old_image.read_file(asset) == image.read_file(asset) for asset in ASSETS)
    assert first["default_name_macros"] == {str(i): value for i, value in names.items()}
    previous_groups = {(g["file_path"], g["block"]): g for g in previous["groups"]}
    renders = {(entry["file_path"], entry["id"]): entry
               for entry in first["checked_records"] + first["retained_records"]}
    punctuation_fixes = {("/data/SC2.DK4", "DK4_MES_B12_R0060"), ("/data/SC3.DK4", "DK4_MES_B19_R0059")}
    paragraph_source = checked_text(getsource(display.paragraph), {
        "{macro: example for macro in tokens}":
            '{macro: example + " Co." if macro == "FO" else example for macro in tokens}',
    })
    scope = vars(display) | {"build": build}
    exec(compile(paragraph_source, __file__ + "::original-renderer-and-20-cell-company-names", "exec"), scope)
    paragraph = scope["paragraph"]

    banks = {i: native.IlnkContainer.parse(image.read_file(f"/data/SC{i}.DK4")) for i in routes}
    rows = {(r["file_path"], r["id"]):r for r in draft["records"]}
    modified, retained, pictures, rendered_fresh = [], [], [], set()
    for group in stored["groups"]:
        route, path, number = (group[k] for k in ("route", "file_path", "block"))
        block = banks[route].blocks[number]
        assert native.digest(block) == group["after"]
        before = previous_groups[path, number]
        commands = {cmd["record_ids"][0]: cmd for cmd in before["commands"] if cmd["record_ids"]}
        for command in group["commands"]:
            if not command["record_ids"]:
                continue
            ident, = command["record_ids"]
            row = rows[path, ident]
            raw, offset = bytes.fromhex(command["stored"]), command["stored_offset"]
            assert block[offset:offset + len(raw)] == raw and command["word"] == row["native_command_word"]
            value = raw[5:raw.index(0, 6)]
            assert value[0] == row["source_selector"] < 207
            plan = group["plans"].get(ident)
            if (path, ident) in punctuation_fixes:
                assert row["decision"] == "revision" and command["stored"] != commands[ident]["stored"]
                assert plan["maximum_expanded_FO_length"] == 20
                entry = paragraph(routes[route], font, paint, expand, None, names[route], row, value, plan)
                assert all(b".." not in bytes.fromhex(layout["expanded_hex"]) for layout in entry["layouts"])
                diagnostics = plan["diagnostics"]
                assert all(d["severity"] == "warning" and d["code"] == "line-break-count" for d in diagnostics)
                entry["informational_source_row_differences"] = diagnostics
                rendered_fresh.add((path, ident))
            else:
                assert command["stored"] == commands[ident]["stored"] and plan == before["plans"].get(ident)
                entry = renders[path, ident]
                assert entry["stored_hex"] == value.hex()
            if row["decision"] == "retention":
                assert command["stored"] == command["current"] and value.hex() == row["current_hex"]
                retained.append(entry)
                continue
            modified.append(entry)
            for layout in entry["layouts"]:
                page, = layout["pages"]
                pictures.append((f"SC{route} {ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))

    assert {(r["file_path"], r["id"]) for r in modified + retained} == rows.keys()
    assert len(modified) == 15 and len(retained) == 136 and len(pictures) == 21
    assert rendered_fresh == punctuation_fixes
    contact = display.inherited.early.contact_sheets
    ROOT.mkdir()
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_assets_byte_identical=True, default_name_macros=names, renderer_assets=ASSETS,
        revision_count=len(modified), fresh_page_count=len(pictures), retention_count=len(retained),
        checked_records=modified, retained_records=retained, contact_sheets=sheets, actual_gameplay=False,
        dependency_exact_reuse=dict(path=str(earlier_proof), sha256=base.digest(earlier_proof),
                                    revised_pages=13, retained_records=136),
        refreshed_punctuation_records=sorted(rendered_fresh)))
    print("Verified 15 revised paragraphs, six additional company-width pages, and 136 exact retentions.")


if __name__ == "__main__":
    verify()
