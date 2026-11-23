"""Verify Maria's compiled dialogue against the registered native renderer."""

from types import FunctionType

from scripts import stage_maria_B18_B20_20261122 as stage
from scripts import verify_rafael_B161_B169_20261121 as rafael
from scripts import verify_hodram_B311_B324_20261122 as inherited


base, native, parent = stage.base, stage.native, stage.parent
display = inherited.scope["display"]
ROOT = stage.ROOT / "native_display"
PROOF = ROOT / "native_display.json"


def main():
    assert not PROOF.exists()
    stored, draft, release = map(base.load, (stage.PROOF, stage.MANUSCRIPT, parent.RELEASE))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert stored["manuscript_sha256"] == base.digest(stage.MANUSCRIPT)
    active = base.NdsImage.open(stage.ROM)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    assert all(ctx.image.read_file(path) == active.read_file(path) for path in display.ASSETS)
    expand = display.original_expander()
    defaults = {}
    for macro in ("FI", "FA", "FO", "FU"):
        cases = ctx.execute(expand, macro.encode("ascii"), 3)["cases"]
        expanded, = {case["output_hex"] for case in cases}
        assert len(cases) == 4
        defaults[macro] = bytes.fromhex(expanded).decode("ascii")
    assert defaults["FI"] == "Maria" and defaults["FA"] == "Li" and defaults["FO"] == "Li Clan"
    original = inherited.scope["check_progressive"]
    check = FunctionType(original.__code__, original.__globals__ | {"DEFAULT_NAMES":defaults})
    audit = inherited.scope["audit_macro_widths"]()
    font = active.read_file("/GRP/KANJI.FNT")
    paint = display.clipped_renderer(ctx)
    blocks = native.IlnkContainer.parse(active.read_file(stage.review.ARCHIVE)).blocks
    prior_proof = stage.FIRST_ROOT / "native_display/native_display.json"
    first = base.load(prior_proof)
    first_rom = stage.FIRST_ROOT / stage.ROM.name
    first_stored = base.load(stage.FIRST_ROOT / stage.PROOF.name)
    assert first["candidate_sha256"] == first_stored["candidate_sha256"] == base.digest(first_rom)
    assert first["runtime_assets"] == list(display.ASSETS)
    earlier = base.NdsImage.open(first_rom)
    assert all(earlier.read_file(path) == active.read_file(path) for path in display.ASSETS)
    assert first["default_name_macros"] == defaults and first["initialized_dependencies"] == ctx.receipt()
    earlier_records = {row["id"]:row for row in first["records"]}
    earlier_plans = {key:plan for group in first_stored["groups"] for key,plan in group["plans"].items()}
    checked_again = set()
    pending = {row["id"]:row for row in draft["records"]}
    entries, pictures = [], []
    changed, alternate = 0, 0
    for group in stored["groups"]:
        n = group["block"]
        block = blocks[n]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            raw, before, source = [bytes.fromhex(cmd[key]) for key in ("stored","current","source")]
            at = cmd["stored_offset"]
            assert block[at:at+len(raw)] == raw
            if not cmd["record_ids"]:
                continue
            ident, = cmd["record_ids"]
            row = pending.pop(ident)
            plan = group["plans"].get(ident)
            selector = row["source_selector"]
            assert raw[:6] == before[:6] == source[:6] == b"\x00\x40\xff\xff\x00"+bytes([selector])
            assert (raw != before) == bool(plan) == (row["decision"] == "revision")
            span = raw[5:raw.index(0,6)]
            assert before[5:before.index(0,6)].hex() == row["current_hex"]
            assert source[5:source.index(0,6)].hex() == row["source_hex"]
            assert not any(raw[5+len(span):])
            entry = dict(id=ident,block=n,stored_pages=[cmd],body_offset=at+5,body_hex=span.hex(),layouts=[])
            if plan:
                former = earlier_records[ident]
                reused = span.hex() == former["body_hex"] and plan == earlier_plans[ident]
                if reused:
                    layouts, cases = former["layouts"], former["original_expansion"]
                else:
                    assert ident in stage.review.VISUAL_REFINEMENTS
                    checked_again.add(ident)
                    try:
                        layouts, cases = check(ctx,font,paint,expand,audit,row,span[1:],plan)
                    except (AssertionError, ValueError) as error:
                        raise AssertionError((ident, plan["lines"],span)) from error
                for layout in layouts:
                    registered = layout["scope"] == "registered default"
                    for i,page in enumerate(layout["pages"],1):
                        if not reused:
                            pictures.append((f"{ident} {layout['scope']} {i}/{len(layout['pages'])}",bytes.fromhex(page["native_plane_hex"])))
                    changed += len(layout["pages"]) if registered else 0
                    alternate += len(layout["pages"]) if not registered else 0
                entry.update(layouts=layouts,original_expansion=cases)
            entries.append(entry)
    assert not pending and len(entries) == 88
    assert sum(bool(row["layouts"]) for row in entries) == 43
    assert changed == 43 and alternate == 3
    assert checked_again == set(stage.review.VISUAL_REFINEMENTS) and len(pictures) == 2
    ROOT.mkdir(exist_ok=True)
    sheet = rafael.prior.precedent.prior.sheet
    make_sheets = FunctionType(sheet.__code__, sheet.__globals__ | {"ROOT":ROOT})
    sheets = make_sheets(pictures, "maria_B18_B20_progressive", 216)
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in first["sheets"])
    base.save(PROOF,dict(candidate_sha256=candidate, records=entries, sheets=first["sheets"] + sheets,
        exact_predecessor_pages_reused=41, independently_reformatted=sorted(checked_again),
        earlier_visual_proof=str(prior_proof), earlier_visual_sha256=base.digest(prior_proof),
        revised_speech_pages=changed,alternate_name_pages=alternate,
        default_name_macros=defaults,initialized_dependencies=ctx.receipt(),
        runtime_assets=list(display.ASSETS),offline_native_only=True))
    print(f"Verified {changed} changed pages and {alternate} alternate-name pages.")


if __name__ == "__main__":
    main()

