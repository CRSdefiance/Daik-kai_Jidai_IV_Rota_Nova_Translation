"""Verify current native layout for ten later body variants whose wording is retained."""

from types import FunctionType

from scripts import verify_maria_B51_B70_20261122 as changed


base,native,stage,display=changed.base,changed.native,changed.stage,changed.display
ROOT=changed.ROOT
PROOF=ROOT/"retained_display.json"


def main():
    display_proof, release, draft=map(base.load,(changed.PROOF,stage.parent.RELEASE,stage.MANUSCRIPT))
    candidate=base.digest(stage.ROM)
    assert display_proof["candidate_sha256"]==candidate and not PROOF.exists()
    ctx=native.RegisteredRuntime(stage.parent.RELEASE,release["own_registered_startup"],captain=3)
    image=base.NdsImage.open(stage.ROM)
    assert all(ctx.image.read_file(path)==image.read_file(path) for path in display.ASSETS)
    font=image.read_file("/GRP/KANJI.FNT")
    paint,expand=display.clipped_renderer(ctx),display.original_expander()
    references={row["id"]:row for row in display_proof["records"]}
    pictures,records=[],[]
    for row in draft["records"]:
        if row["decision"]!="retention":
            continue
        ident=row["id"]
        native_row=references[ident]
        prefix,*_=bytes.fromhex(native_row["body_hex"])
        assert native_row["body_hex"]==row["current_hex"] and not native_row["layouts"]
        body=bytes.fromhex(native_row["body_hex"])[1:]
        cases=ctx.execute(expand,body,prefix)["cases"]
        assert len(cases)==4 and {case["output_hex"] for case in cases}=={body.hex()}
        lines=[" ".join(line.split()) for line in body.decode("ascii").splitlines()]
        assert " ".join(lines)==row["english"]
        page,=display.display.raster(ctx,font,paint,body,lines,1)
        assert page["native_independent_plane_equal"] and page["all_bitmap_header_input_canaries_exact"]
        plane=bytes.fromhex(page["native_plane_hex"])
        pictures.append((f"{ident} retained",plane))
        records.append(dict(id=ident,body_hex=native_row["body_hex"],lines=lines,pages=1,plane_sha256=native.digest(plane)))
    assert len(records)==10
    template=changed.previous.rafael.prior.precedent.prior.sheet
    sheet=FunctionType(template.__code__,template.__globals__|{"ROOT":ROOT})
    sheets=sheet(pictures,"maria_B51_B70_retained_native",216)
    base.save(PROOF,dict(candidate_sha256=candidate,source_proof_sha256=base.digest(changed.PROOF),
        records=records,sheets=sheets,new_gameplay=False))
    print("Verified all ten retained bodies against the current native renderer.")


if __name__=="__main__":
    main()

