"""Check complete Maria render planes, menu behavior and retained lookout slots."""

from types import FunctionType

from scripts import stage_maria_B21_B32_20261122 as stage
from scripts import verify_maria_opening_hodram_wraps_20261122 as previous
from scripts import verify_hodram_B311_B324_20261122 as inherited


base,native,parent=stage.base,stage.native,stage.parent
display=previous.display
ROOT=stage.ROOT/"native_display"
PROOF=ROOT/"native_display.json"


def owned_slice(row,command,side):
    ref=row[side+"_reference"]
    offset=ref["offset"]-ref["command_offset"]
    expected=bytes.fromhex(ref["exact_body_hex"])
    assert command[offset:offset+len(expected)]==expected
    return offset,expected


def main():
    assert not PROOF.exists()
    saved,draft,release=map(base.load,(stage.PROOF,stage.MANUSCRIPT,parent.RELEASE))
    candidate=base.digest(stage.ROM)
    assert candidate==saved["candidate_sha256"] and saved["whole_parent_inverse"]
    assert saved["predecessor_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    assert saved["manuscript_sha256"]==base.digest(stage.MANUSCRIPT)
    image=base.NdsImage.open(stage.ROM)
    ctx=native.RegisteredRuntime(parent.RELEASE,release["own_registered_startup"],captain=3)
    assert all(ctx.image.read_file(asset)==image.read_file(asset) for asset in display.ASSETS)
    font=image.read_file("/GRP/KANJI.FNT")
    expand,paint=display.original_expander(),display.clipped_renderer(ctx)
    names={}
    for macro in ("FI","FA","FO","FU"):
        responses=ctx.execute(expand,macro.encode("ascii"),3)["cases"]
        out,={r["output_hex"] for r in responses}
        assert len(responses)==4
        names[macro]=bytes.fromhex(out).decode("ascii")
    assert names==previous.base.load(parent.display.PROOF)["default_names"]["3"]
    original=inherited.scope["check_progressive"]
    check=FunctionType(original.__code__,original.__globals__|{"DEFAULT_NAMES":names})
    audit=inherited.scope["audit_macro_widths"]()
    library=inherited.scope["menus"]
    menu=FunctionType(library.verify_menu.__code__,library.verify_menu.__globals__|{"ROOT":ROOT})
    menu_adapters=library.menu.adapters(ctx.arm)
    ROOT.mkdir(exist_ok=True)
    banks=native.IlnkContainer.parse(image.read_file(stage.review.ARCHIVE)).blocks
    wanted={row["id"]:row for row in draft["records"]}
    entries,pictures,menus,voice_owners=[],[],[],[]
    revised,alternate=0,0
    for group in saved["groups"]:
        block=group["block"]
        installed=banks[block]
        assert group["route"]==3 and native.digest(installed)==group["after"]
        for cmd in group["commands"]:
            at=cmd["stored_offset"]
            target,old,source=[bytes.fromhex(cmd[key]) for key in ("stored","current","source")]
            assert installed[at:at+len(target)]==target
            members=[wanted.pop(i) for i in cmd["record_ids"]]
            if cmd["word"]==0x2100 and members:
                assert target==old
                originals={cmd["source_offset"]:{"offset":cmd["source_offset"],"whole_command_hex":cmd["source"]}}
                menus.append(menu(ctx.arm,originals,cmd,members,menu_adapters)|{"block":block})
            for row in members:
                ident=row["id"]
                entry=dict(id=ident,block=block,route=3,stored_pages=[cmd],layouts=[])
                if row["kind"] in ("actor-style","typed-choice-label"):
                    assert target==old and row["decision"]=="retention"
                    offset,body=owned_slice(row,old,"current")
                    owned_slice(row,source,"source")
                    assert body.hex()==row["current_hex"]
                    if row["kind"]=="actor-style":
                        plan=group["plans"][ident]
                        assert plan["encoded_hex"]==(bytes([row["source_selector"]])+body).hex()
                        native_style=paint(ctx.arm,font,body)
                        assert native_style["complete_consumed_bytes"]==len(body)
                        page,=native_style["pages"]
                        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                        pixels=bytes.fromhex(page["native_plane_hex"])
                        voice_owners.append(dict(id=ident,slots=row["native_slots"],glyph_plane_sha256=native.digest(pixels)))
                        pictures.append((f"{ident} retained lookout",pixels))
                else:
                    selector=row["source_selector"]
                    offset=5
                    assert target[:6]==old[:6]==source[:6]==b"\x00\x40\xff\xff\x00"+bytes([selector])
                    body=target[5:target.index(0,6)]
                    assert not any(target[5+len(body):])
                    assert old[5:old.index(0,6)].hex()==row["current_hex"]
                    assert source[5:source.index(0,6)].hex()==row["source_hex"]
                    changed=row["decision"]=="revision"
                    assert (target!=old)==changed
                    if changed:
                        plan=group["plans"][ident]
                        try:
                            layouts,four_alignments=check(ctx,font,paint,expand,audit,row,body[1:],plan)
                        except (AssertionError,ValueError) as error:
                            raise AssertionError((ident,plan["lines"],body)) from error
                        for layout in layouts:
                            regular=layout["scope"]=="registered default"
                            pages=layout["pages"]
                            assert len(pages)==plan["expected_native_pages"]
                            revised+=len(pages) if regular else 0
                            alternate+=len(pages) if not regular else 0
                            for idx,page in enumerate(pages,1):
                                assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
                                pictures.append((f"{ident} {layout['scope']} {idx}/{len(pages)}",bytes.fromhex(page["native_plane_hex"])))
                        entry.update(layouts=layouts,original_expansion=four_alignments)
                entry.update(body_offset=at+offset,body_hex=body.hex())
                entries.append(entry)
    assert not wanted and len(entries)==132
    assert sum(bool(row["layouts"]) for row in entries)==40
    assert len(menus)==1 and menus[0]["count"]==2 and menus[0]["block"]==29
    assert len(voice_owners)==7 and sorted(i for row in voice_owners for i in row["slots"])==list(range(8))
    sheet=previous.rafael.prior.precedent.prior.sheet
    render=FunctionType(sheet.__code__,sheet.__globals__|{"ROOT":ROOT})
    sheets=render(pictures,"maria_B21_B32_native",216)
    base.save(PROOF,dict(candidate_sha256=candidate,stage_proof_sha256=base.digest(stage.PROOF),records=entries,
        sheets=sheets+[m["sheet"] for m in menus],menus=menus,lookout_voice_owners=voice_owners,
        revised_speech_pages=revised,alternate_name_pages=alternate,default_names={"3":names},
        initialized_dependencies=ctx.receipt(),offline_native_only=True))
    print(f"Verified {revised} changed pages, {alternate} alternate-name pages, seven lookout bodies and two choice labels.")


if __name__=="__main__":
    main()

