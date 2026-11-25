"""Check every revised harbor page plus live name, movie and dialogue transitions."""
from pathlib import Path
from types import FunctionType

from PIL import ImageChops

from scripts import replay_rafael_harbor_exchange_20261121 as run
from scripts import verify_all_routes_next_phrase_wraps_20261118 as native_display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


stage,base,native = run.stage,run.base,run.stage.native
ROOT=stage.ROOT/"native_display"
PROOF=ROOT/"native_display.json"
LIVE=run.ROOT/"verified_harbor.json"


def runtime(rom,report,candidate):
    snapshot=report["read_only_RAM_snapshot"]
    assert snapshot["read_only_export"] and base.digest(snapshot["path"])==snapshot["sha256"]
    arm=rom.read_file(native.ARM)
    cpu,get=panel.town.get_machine(arm,Path(snapshot["path"]).read_bytes())
    assert get(0x7F244)==0
    release=ROOT/"research_exact_ROM.json"
    startup=ROOT/"own_Rafael_read_only_snapshot.json"
    base.save(release,dict(candidate=str(stage.ROM),candidate_sha256=candidate,
        own_registered_startup_pending=False,clean_input_patch_byte_exact=True,research_only=True))
    base.save(startup,dict(candidate_sha256=candidate,cold_boot=True,savestate=False,
                          actual_captain_getter=0,read_only_snapshot=snapshot))
    return native.RegisteredRuntime(release,startup,captain=0)


def main():
    assert not LIVE.exists()
    stored,review,report,prior=map(base.load,(stage.PROOF,stage.review.OUTPUT,run.REPORT,run.harbor.REPORT))
    candidate=base.digest(stage.ROM)
    assert candidate==stored["candidate_sha256"]==report["ROM_sha256"]
    assert stored["predecessor_sha256"]==base.digest(stage.parent.ROM)==prior["ROM_sha256"]
    assert base.digest(stage.review.OUTPUT)==stored["manuscript_sha256"]
    assert base.digest(run.harbor.REPORT)==review["previous_gameplay_report_sha256"]
    assert stored["whole_parent_inverse"] and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"]==prior["scripted_input_schedule"]==base.load(run.PLAN)
    assert report["core_options"]==prior["core_options"] and report["frames"]==prior["frames"]
    assert base.digest(stage.ROOT/"clean_rebuilt.nds")==candidate
    before,after=map(base.NdsImage.open,(stage.parent.ROM,stage.ROM))
    assert all(before.read_file(p)==after.read_file(p) for p in (*native_display.ASSETS,
        "/FLS/M20.fls","/FLS/m21.fls"))
    ROOT.mkdir(exist_ok=True)
    ctx=runtime(after,report,candidate)
    font=after.read_file("/GRP/KANJI.FNT")
    paint=native_display.clipped_renderer(ctx)
    if PROOF.exists():
        offline=base.load(PROOF)
        assert offline["candidate_sha256"]==candidate and offline["stage_proof_sha256"]==base.digest(stage.PROOF)
        assert len(offline["records"])==117 and all(base.digest(x["path"])==x["sha256"] for x in offline["sheets"])
        revisions={x["id"]:x for x in offline["records"] if x["decision"]=="revision"}
        assert len(revisions)==30
    else:
        expander=native_display.original_expander()
        names={"FI":"Rafael","FA":"Castor","FO":"Castor Co."}
        actual=ctx.execute(expander,b"FI FA",0)["cases"]
        assert len(actual)==4 and {case["output_hex"] for case in actual}=={b"Rafael Castor".hex()}
        validate=native_display.display.paragraph
        validate=FunctionType(validate.__code__,validate.__globals__|{"build":stage})
        group,=stored["groups"]
        path=group["file_path"]
        data=native.IlnkContainer.parse(after.read_file(path)).blocks[44]
        assert native.digest(data)==group["after"]
        rows={r["id"]:r for r in review["records"]}
        revisions,retained,previews={},[],[]
        for c in group["commands"]:
            original,compiled=(bytes.fromhex(c[k]) for k in ("current","stored"))
            at=c["stored_offset"]
            assert data[at:at+len(compiled)]==compiled
            for ident in c["record_ids"]:
                row=rows.pop(ident)
                common=dict(id=ident,file_path=path,block=44,decision=row["decision"],
                            stored_offset=at,stored_command_hex=compiled.hex())
                if row["decision"]=="retention":
                    assert original==compiled
                    retained.append(common)
                    continue
                assert c["word"]==0x4000 and original[:6]==compiled[:6]==b"\0\x40\xff\xff\0"+bytes([row["source_selector"]])
                last=compiled.index(0,6)
                raw=compiled[5:last]
                assert raw[1:].isascii() and not any(compiled[last:])
                assert stage.review.TOKEN.findall(raw[1:].decode())==stage.review.TOKEN.findall(original[6:original.index(0,6)].decode())
                verified=validate(ctx,font,paint,expander,None,names,row,raw,group["plans"][ident])
                cases=[]
                for check in verified["layouts"]:
                    one,=check["pages"]
                    assert one["native_independent_plane_equal"]
                    pixels=bytes.fromhex(one["native_plane_hex"])
                    previews.append((ident+" "+check["scope"],pixels))
                    cases.append(dict(scope=check["scope"],lines=check["lines"],expanded_hex=check["expanded_hex"],
                                      plane_sha256=native.digest(pixels)))
                revisions[ident]=common|dict(native_pages=1,layouts=cases,original_processor=verified["macro_alignment_checks"])
        assert not rows and len(revisions)==30 and len(retained)==87
        contact=native_display.display.inherited.early.contact_sheets
        sheets=FunctionType(contact.__code__,contact.__globals__|{"ROOT":ROOT})(previews)
        base.save(PROOF,dict(candidate_sha256=candidate,stage_proof_sha256=base.digest(stage.PROOF),
            records=[*revisions.values(),*retained],sheets=sheets,offline_native_only=True,newly_rendered_pages=len(previews),
            native_given_and_surname_names=names,original_captain_from_ordinary_snapshot=0,source_name_cases=actual))

    actual_frames={r["frame"]:r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    before_frames={r["frame"]:r for r in prior["frames_captured"]}
    checks,unchanged,pairs=[],[],[]
    name_font=panel.GameAsciiFont.from_arm9(ctx.arm)
    for row in review["records"]:
        if row["previous_capture"] is None:
            continue
        ident=row["id"]
        old=row["previous_capture"]
        frame=old["frame"]
        shot,picture=panel.town.read_frame(actual_frames,frame)
        if row["decision"]=="retention":
            assert old["framebuffer_sha256"]==shot["framebuffer_sha256"], (ident,frame)
            unchanged.append(shot)
            continue
        result=revisions[ident]["layouts"][0]
        expanded=bytes.fromhex(result["expanded_hex"])
        rendered=paint(ctx.arm,font,expanded)
        native_page,=rendered["pages"]
        assert rendered["complete_consumed_bytes"]==len(expanded)
        raw=bytes.fromhex(native_page["native_plane_hex"])
        assert native.digest(raw)==result["plane_sha256"] and panel.mask_check(raw,216,picture), ident
        speaker={0:"Rafael Castor",5:"Claudio Manaus"}[row["source_selector"]]
        panel.complete_mask(name_font,speaker,picture,16,277,panel.town.INKS[1])
        _,past=panel.town.read_frame({frame:old},frame)
        diff=ImageChops.difference(past,picture)
        diff.paste((0,0,0),(16,296,232,360))
        assert diff.getbbox() is None, ident
        pairs.extend(((ident+" before",past),(ident+" revised",picture)))
        checks.append(dict(id=ident,file_path=row["file_path"],frame=frame,previous=old,revised=shot,speaker=speaker))
    extra=[]
    for f in (3000,6920,7021,8020):
        shot,picture=panel.town.read_frame(actual_frames,f)
        same=shot["framebuffer_sha256"]==before_frames[f]["framebuffer_sha256"]
        if f==8020:
            _,prior_picture=panel.town.read_frame(before_frames,f)
            assert picture.crop((0,0,256,192)).tobytes()==prior_picture.crop((0,0,256,192)).tobytes()
        else:
            assert same,f
        extra.append(shot|{"whole_frame_exact":same,"upper_RGB_exact":True})
    assert len(checks)==7 and len(unchanged)==11
    comparison=[]
    for pos in range(0,len(pairs),6):
        p=run.ROOT/f"harbor_before_after_{pos//6+1}.png"
        panel.town.sheet(pairs[pos:pos+6],p)
        comparison.append(dict(path=str(p),sha256=base.digest(p)))
    base.save(LIVE,dict(candidate_sha256=candidate,holds=checks,unchanged_controls=unchanged,movie_transition_holds=extra,
        natural_activation=True,exact_native_glyph_matches=True,hardware_verified=False,sheets=comparison,
        evidence={str(p):base.digest(p) for p in (run.REPORT,run.PLAN,run.harbor.OUTPUT,PROOF)}))
    print("Verified 45 native pages, seven revised gameplay panels and fourteen unchanged holds. The ship art also matches during a changed line.")


if __name__=="__main__":
    main()
