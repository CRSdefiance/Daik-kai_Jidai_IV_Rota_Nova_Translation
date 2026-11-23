"""Verify each changed line against the two initialized native story consumers."""

from types import FunctionType

from scripts import stage_maria_opening_hodram_wraps_20261122 as stage
from scripts import verify_hodram_B311_B324_20261122 as inherited
from scripts import verify_rafael_B161_B169_20261121 as rafael


base, native, parent = stage.base, stage.native, stage.parent
display = inherited.scope["display"]
ROOT = stage.ROOT/"native_display"
PROOF = ROOT/"native_display.json"


def runtime_contexts(image):
    release = base.load(parent.RELEASE)
    routes = {
        1: inherited.scope["current_runtime"](image),
        3: native.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3),
    }
    assert all(ctx.image.read_file(path)==image.read_file(path)
               for ctx in routes.values() for path in display.ASSETS)
    return routes


def read_settings_binding(image):
    from pathlib import Path

    path = Path("work/analysis/shared_settings_20261122/sailing_help_state_transitions.json")
    proof = base.load(path)
    assert proof["candidate_sha256"] == base.digest(parent.ROM)
    previous = base.NdsImage.open(parent.ROM)
    assert all(previous.read_file(asset)==image.read_file(asset) for asset in display.ASSETS)
    assert proof["native_common_request_count"]==0 and all(proof["review"].values())
    return dict(path=str(path),sha256=base.digest(path),runtime_assets_exact=list(display.ASSETS))


def main():
    assert not PROOF.exists()
    stored,draft = map(base.load,(stage.PROOF,stage.MANUSCRIPT))
    candidate = base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"] and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"]==base.digest(parent.ROM)
    assert stored["manuscript_sha256"]==base.digest(stage.MANUSCRIPT)
    active = base.NdsImage.open(stage.ROM)
    contexts = runtime_contexts(active)
    font,expand = active.read_file("/GRP/KANJI.FNT"),display.original_expander()
    audit = inherited.scope["audit_macro_widths"]()
    original = inherited.scope["check_progressive"]
    prepared,names = {},{}
    for route,ctx in contexts.items():
        defaults = {}
        for macro in ("FI","FA","FO","FU"):
            four = ctx.execute(expand,macro.encode("ascii"),route)["cases"]
            out, = {case["output_hex"] for case in four}
            assert len(four)==4
            defaults[macro]=bytes.fromhex(out).decode("ascii")
        names[route]=defaults
        checked = FunctionType(original.__code__, original.__globals__ | {"DEFAULT_NAMES":defaults})
        prepared[route]=(ctx, display.clipped_renderer(ctx), checked)
    assert names[1]==inherited.scope["DEFAULT_NAMES"]
    assert names[3]=={"FI":"Maria","FA":"Li","FO":"Li Clan","FU":"Maria Huamei Li"}
    archives = {f"/data/SC{route}.DK4": native.IlnkContainer.parse(active.read_file(f"/data/SC{route}.DK4")).blocks
                for route in contexts}
    pending = {(r["route"],r["id"]):r for r in draft["records"]}
    rows,pictures = [],[]
    revised,alternates = 0,0
    for group in stored["groups"]:
        route,n,path = group["route"],group["block"],group["file_path"]
        block=archives[path][n]
        assert native.digest(block)==group["after"]
        for cmd in group["commands"]:
            offset = cmd["stored_offset"]
            raw, prior, jp = [bytes.fromhex(cmd[key]) for key in ("stored","current","source")]
            assert block[offset:offset+len(raw)]==raw
            if not cmd["record_ids"]:
                continue
            for ident in cmd["record_ids"]:
                row = pending.pop((route,ident))
                entry = dict(id=ident,route=route,block=n,stored_pages=[cmd],layouts=[])
                if row["kind"]=="actor-style":
                    remembered = row["previous_registered_reference"]
                    assert row["decision"]=="retention" and raw==prior==bytes.fromhex(remembered["exact_command_hex"])
                    delta = remembered["offset"]-remembered["command_offset"]
                    span = bytes.fromhex(remembered["exact_stored_hex"])
                    assert raw[delta:delta+len(span)+1]==span+b"\0"
                else:
                    delta,selector=5,row["source_selector"]
                    assert raw[:6]==prior[:6]==jp[:6]==b"\x00\x40\xff\xff\x00"+bytes([selector])
                    span=raw[5:raw.index(0,6)]
                    assert not any(raw[5+len(span):])
                    assert prior[5:prior.index(0,6)].hex()==row["current_hex"]
                    assert jp[5:jp.index(0,6)].hex()==row["source_hex"]
                    changed=row["decision"]=="revision"
                    assert (raw != prior)==changed
                    if changed:
                        ctx,paint,check = prepared[route]
                        plan = group["plans"][ident]
                        try:
                            layouts,alignment = check(ctx,font,paint,expand,audit,row,span[1:],plan)
                        except (AssertionError,ValueError) as error:
                            raise AssertionError((ident,plan["lines"],span)) from error
                        for layout in layouts:
                            default=layout["scope"]=="registered default"
                            pages=layout["pages"]
                            assert len(pages)==plan["expected_native_pages"]
                            for ix,page in enumerate(pages,1):
                                assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                                pictures.append((f"SC{route} {ident} {layout['scope']} {ix}/{len(pages)}",bytes.fromhex(page["native_plane_hex"])))
                            revised+=len(pages) if default else 0
                            alternates+=len(pages) if not default else 0
                        entry.update(layouts=layouts,original_expansion=alignment)
                entry.update(body_offset=offset+delta,body_hex=span.hex())
                rows.append(entry)
    assert not pending and len(rows)==171
    assert sum(bool(row["layouts"]) for row in rows)==46
    ROOT.mkdir(exist_ok=True)
    sheet=rafael.prior.precedent.prior.sheet
    render=FunctionType(sheet.__code__,sheet.__globals__|{"ROOT":ROOT})
    sheets=render(pictures,"maria_opening_hodram_native",216)
    base.save(PROOF,dict(candidate_sha256=candidate,stage_proof_sha256=base.digest(stage.PROOF),
        records=rows,sheets=sheets,revised_speech_pages=revised,alternate_name_pages=alternates,default_names=names,
        initialized_dependencies={route:ctx.receipt() for route,ctx in contexts.items()},
        exact_shared_prompt_consumer=read_settings_binding(active),offline_native_only=True))
    print(f"Native formatting passed for {revised} changed pages and {alternates} alternate-name pages.")


if __name__=="__main__":
    main()

