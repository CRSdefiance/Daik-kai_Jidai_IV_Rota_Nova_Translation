"""Check the revised Deck lesson through the registered progressive and system renderers."""

from PIL import Image,ImageDraw

from scripts import compile_rafael_deck_tutorial_followup_20261122 as compiled
from scripts import verify_london_guild_assignments_20261118 as renderer
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter


draft,base,native = compiled.draft,compiled.base,compiled.native
ROOT = draft.ROOT
PROOF = ROOT/"native_preflight.json"
SHEET = ROOT/"native_review.png"


def main():
    assert not PROOF.exists() and not SHEET.exists()
    source,storage,release = map(base.load,(draft.OUTPUT,compiled.PROOF,draft.current.RELEASE))
    assert base.digest(draft.OUTPUT)==storage["draft_sha256"]
    assert storage["predecessor_sha256"]==source["previous_sha256"]==release["candidate_sha256"]
    assert base.digest(compiled.TARGET)==storage["compiled_block_sha256"]
    assert storage["complete_whole_ROM_inverse"]
    ctx = native.RegisteredRuntime(draft.current.RELEASE,release["own_registered_startup"],captain=3)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    _, paint = renderer.inherited.early.prior.precedent.planners(ctx.arm)
    fe = current_fe_painter(ctx)
    names, expand = renderer.current_names(ctx), renderer.expander()
    target = compiled.TARGET.read_bytes()
    by_id = {row["id"]:row for row in source["records"]}
    renders = []
    for command in storage["commands"]:
        if not command["record_ids"] or command["stored"]==command["current"]:
            continue
        ident, = command["record_ids"]
        at = command["stored_offset"]
        stored = bytes.fromhex(command["stored"])
        assert target[at:at+len(stored)] == stored
        row, plan = by_id[ident],storage["plans"][ident]
        raw = stored[5:stored.index(0,6)]
        result = renderer.paragraph(ctx,font,paint,expand,fe,names,row,raw,plan)
        if "{MACRO:FI}" in " ".join(plan["lines"]):
            text = raw[1:].replace(b"FI",b"Rafael")
            lines = [renderer.expected(line,{"FI":"Rafael"}) for line in plan["lines"]]
            pages = renderer.raster(ctx,font,paint,text,lines,plan["expected_native_pages"])
            result["layouts"].insert(0,dict(scope="offline Rafael default",names={"FI":"Rafael"},
                expanded_hex=text.hex(),lines=lines,pages=pages))
            assert raw[:2]==b"\x06F" and raw[1:].isascii()
        renders.append(result)
    assert len(renders)==6
    samples = []
    for row in renders:
        for display in row["layouts"]:
            page, = display["pages"]
            bytes_ = bytes.fromhex(page["native_plane_hex"])
            assert len(bytes_)==216*64
            samples.append((row["id"],display["scope"],bytes_))
    sheet = Image.new("RGB",(900,142*((len(samples)+1)//2)),"#263238")
    draw = ImageDraw.Draw(sheet)
    for i,(ident,context,pixels) in enumerate(samples):
        x,y = (i%2)*450,(i//2)*142
        draw.text((x+5,y+2),f"{ident}  {context}",fill="white")
        pane = Image.frombytes("L",(216,64),bytes(0 if px else 250 for px in pixels))
        sheet.paste(pane.resize((432,128),Image.Resampling.NEAREST),(x+5,y+14))
    sheet.save(SHEET)
    base.save(PROOF,dict(proposed_ROM_sha256=storage["proposed_ROM_sha256"],
        base_ROM_sha256=release["candidate_sha256"],stored_preflight_sha256=base.digest(compiled.PROOF),
        rendering_dependencies=ctx.receipt(),full_progressive_and_FE_cases=renders,offline_pages=len(samples),
        sheet=str(SHEET),sheet_sha256=base.digest(SHEET),actual_gameplay=False,direct_visual_review_pending=True))
    print(f"Rendered {len(samples)} native pages across {len(renders)} revised Deck lesson records.",flush=True)


if __name__ == "__main__":
    main()

