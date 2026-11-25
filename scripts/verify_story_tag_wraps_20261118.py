"""Check revised question tags and names through the registered native renderer."""

from inspect import getsource
from types import FunctionType

from scripts import stage_story_tag_wraps_20261118 as build
from scripts import verify_late_trade_exchanges_20261118 as routes
from scripts import verify_london_guild_assignments_20261118 as display
from scripts.source_locked_derivation_v5118 import checked_text

base, native = build.base, build.native
ROOT = build.ROOT / "native_display_v1"
PROOF = ROOT / "native_display.json"


def main():
    assert not ROOT.exists()
    stored, draft, release = map(base.load, (build.PROOF, build.review.OUTPUT, build.parent.RELEASE))
    assert base.digest(build.ROM) == stored["candidate_sha256"]
    assert stored["manuscript_sha256"] == base.digest(build.review.OUTPUT) and stored["whole_parent_inverse"]
    assert release["candidate_sha256"] == stored["predecessor_sha256"] == base.digest(build.parent.ROM)
    image = base.NdsImage.open(build.ROM)
    lil = routes.lil_context()
    maria = native.RegisteredRuntime(build.parent.RELEASE, release["own_registered_startup"], captain=3)
    assets = (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT")
    assert all(image.read_file(p) == lil.image.read_file(p) == maria.image.read_file(p) for p in assets)
    names = {2: routes.current_names(lil), 3: display.current_names(maria)}
    font = image.read_file(assets[2])
    _, paint = display.inherited.early.prior.precedent.planners(maria.arm)
    expand = routes.expander()
    paragraph_source = checked_text(getsource(display.paragraph), {
        'assert compiled[:1] == raw[:1] and raw in (compiled, compiled + b" ")':
            'assert compiled[:1] == raw[:1] and raw == compiled.ljust(len(raw), b" ")\n'
            '    assert len(raw) - len(compiled) <= plan.get("original_allocation_right_padded", 1)',
    })
    scope = vars(display) | {"build": build}
    exec(compile(paragraph_source, __file__ + "::verified-original-consumer", "exec"), scope)
    rows = {(r["file_path"], r["id"]): r for r in draft["records"]}
    verified, pictures = [], []
    for group in stored["groups"]:
        route, path, n = (group[k] for k in ("route", "file_path", "block"))
        block = native.IlnkContainer.parse(image.read_file(path)).blocks[n]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            raw = bytes.fromhex(cmd["stored"])
            pos = cmd["stored_offset"]
            assert cmd["word"] == 0x4000 and block[pos:pos + len(raw)] == raw
            value = raw[5:raw.index(0, 6)]
            row = rows[path, ident]
            assert value[0] == row["source_selector"] < 207
            assert route in (2, 3) or not build.review.TOKEN.search(row["english"])
            context = lil if route == 2 else maria
            plan = group["plans"][ident]
            result = scope["paragraph"](context, font, paint, expand, None, names.get(route, {}), row, value, plan)
            verified.append(result)
            for layout in result["layouts"]:
                for page in layout["pages"]:
                    pictures.append((f"SC{route} {ident} {layout['scope']}", bytes.fromhex(page["native_plane_hex"])))
    assert {(r["file_path"], r["id"]) for r in verified} == rows.keys() and len(verified) == 17
    assert len(pictures) == 26
    ROOT.mkdir()
    contact = display.inherited.early.contact_sheets
    sheets = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": ROOT})(pictures)
    base.save(PROOF, dict(candidate_sha256=stored["candidate_sha256"], stage_proof_sha256=base.digest(build.PROOF),
        native_runtime_data_matches_registered_route_contexts=True, default_name_macros=names,
        revision_count=len(verified), fresh_page_count=len(pictures), checked_records=verified,
        contact_sheets=sheets, actual_gameplay=False, visual_review_pending=True))
    print(f"Native and allocation checks passed for {len(verified)} revised records and {len(pictures)} pages.")


if __name__ == "__main__":
    main()
