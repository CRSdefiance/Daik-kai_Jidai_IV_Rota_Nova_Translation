"""Verify the corrected surrender line and the complete natural Kurushima encounter."""

from pathlib import Path

from PIL import Image,ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_rafael_deck_after_trade_20261119 as display_tools
from scripts import stage_kurushima_surrender_20261122 as staged
from scripts.verify_captain_biographies_v1 import captured,shots


base,native = staged.base,staged.native
ROOT=staged.ROOT/"checked"
NATIVE,LIVE=ROOT/"native.json",ROOT/"ordinary_gameplay.json"
SHEET,PLAY_SHEET=ROOT/"native_pages.png",ROOT/"encounter_comparison.png"
BASELINE=staged.voyage.ROOT/"capture/capture_report.json"
REPORT=staged.ROOT/"gameplay/capture/capture_report.json"


def verify():
    assert not ROOT.exists()
    stored,review,prior=map(base.load,(staged.PROOF,staged.MANUSCRIPT,staged.parent.RELEASE))
    sha=base.digest(staged.ROM)
    assert sha==stored["candidate_sha256"]
    assert base.digest(staged.MANUSCRIPT)==stored["manuscript_sha256"] and stored["whole_parent_inverse"]
    assert stored["predecessor_sha256"]==prior["candidate_sha256"]==base.digest(staged.parent.ROM)
    ctx=native.RegisteredRuntime(staged.parent.RELEASE,prior["own_registered_startup"],captain=3)
    painter=staged.renderer.inherited.early.prior.precedent.planners(ctx.arm)[1]
    font=ctx.image.read_file("/GRP/KANJI.FNT")
    bitmap_font=GameAsciiFont.from_arm9(ctx.arm)
    names,expand=staged.renderer.current_names(ctx),staged.renderer.expander()
    commands=[row for row in stored["commands"] if row["record_ids"]]
    assert len(commands)==len(review["records"])==8
    revised=next(row for row in review["records"] if row["id"]==staged.ID)
    change=next(cmd for cmd in commands if cmd["record_ids"]==[staged.ID])
    def raw(cmd,key):
        command=bytes.fromhex(cmd[key])
        return command[5:command.index(0,6)]
    native_proof=staged.renderer.paragraph(ctx,font,painter,expand,None,names,revised,raw(change,"stored"),
        stored["plans"][staged.ID])
    assert len(native_proof["layouts"])==4 and native_proof["layouts"][0]["names"]=={"FI":"Maria"}
    assert all(len(x["pages"])==1 for x in native_proof["layouts"])

    original,replayed=map(base.load,(BASELINE,REPORT))
    assert original["ROM_sha256"]==prior["candidate_sha256"] and replayed["ROM_sha256"]==sha
    for report in (original,replayed):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
        donor=report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    assert original["core_options"]==replayed["core_options"]
    assert replayed["scripted_input_schedule"]==[r for r in original["scripted_input_schedule"] if r["start"]<=11801]
    assert replayed["frames"]==11851
    assert original["battery_save_preloaded"]["source_sha256"]==replayed["battery_save_preloaded"]["source_sha256"]
    old,new=map(shots,(original,replayed))
    controls=(8550,9020,11620,11850)
    for number in controls:
        assert old[number]["framebuffer_sha256"]==new[number]["framebuffer_sha256"]
        assert base.digest(old[number]["path"])==old[number]["PNG_sha256"]
        assert base.digest(new[number]["path"])==new[number]["PNG_sha256"]
    target=native.IlnkContainer.parse(base.NdsImage.open(staged.ROM).read_file(staged.ARCHIVE)).blocks[3]
    assert native.digest(target)==stored["compiled_block_sha256"]

    evidence={str(p):base.digest(p) for p in (REPORT,BASELINE,staged.PROOF,staged.MANUSCRIPT)}
    panels=[]
    for frame,row,command in zip(staged.FRAMES[2:10],review["records"],commands,strict=True):
        ident=row["id"]
        assert command["record_ids"]==[ident]
        assert bytes.fromhex(command["stored"])==target[command["stored_offset"]:command["stored_offset"]+len(bytes.fromhex(command["stored"]))]
        captures=[]
        for side,frames,cmdkey in (("before",old,"current"),("after",new,"stored")):
            image=captured(frames[frame])
            payload=raw(command,cmdkey)[1:].replace(b"FI",b"Maria")
            plan=painter(ctx.arm,font,payload)
            page,=plan["pages"]
            assert plan["complete_consumed_bytes"]==len(payload) and page["native_independent_plane_equal"]
            plane=bytes.fromhex(page["native_plane_hex"])
            assert display_tools.TOOL.body_masks(image)==display_tools.TOOL.prior.masks(plane),(ident,frame,side)
            count,bounds=display_tools.complete_mask(bitmap_font,row["speaker"],image,16,277,(98,97,98))
            captures.append(dict(frame=frame,path=frames[frame]["path"],PNG_sha256=frames[frame]["PNG_sha256"],
                complete_body_plane_sha256=native.digest(plane),name=row["speaker"],name_pixels=count,name_bounds=bounds))
            evidence[frames[frame]["path"]]=frames[frame]["PNG_sha256"]
        assert (old[frame]["framebuffer_sha256"]==new[frame]["framebuffer_sha256"])==(ident!=staged.ID)
        panels.append(dict(id=ident,decision=row["decision"],before=captures[0],after=captures[1]))
    revised_frame=10720
    assert next(r for r in panels if r["id"]==staged.ID)["after"]["frame"]==revised_frame
    assert b"I'll let you surrender" in b" ".join(raw(change,"stored")[1:].split())
    for n in controls:
        for group in (old,new):
            evidence[group[n]["path"]]=group[n]["PNG_sha256"]

    ROOT.mkdir()
    sheet=Image.new("RGB",(900,142*2),"#263238")
    labels=ImageDraw.Draw(sheet)
    for i,c in enumerate(native_proof["layouts"]):
        x,y=i%2*450,i//2*142
        labels.text((x+5,y+2),c["scope"],fill="white")
        pane=Image.frombytes("L",(216,64),bytes(0 if px else 250 for px in
            bytes.fromhex(c["pages"][0]["native_plane_hex"])))
        sheet.paste(pane.resize((432,128),Image.Resampling.NEAREST),(x+5,y+14))
    sheet.save(SHEET)
    actual=Image.new("RGB",(1024,408),"#263238")
    labels=ImageDraw.Draw(actual)
    for i,(group,label) in enumerate(((old,"Previous"),(new,"Corrected"))):
        labels.text((i*512+5,3),label,fill="white")
        pane=captured(group[revised_frame]).crop((0,192,256,384))
        actual.paste(pane.resize((512,384),Image.Resampling.NEAREST),(i*512,20))
    actual.save(PLAY_SHEET)
    base.save(NATIVE,dict(candidate_sha256=sha,stored_proof_sha256=base.digest(staged.PROOF),native=native_proof,
        sheet=str(SHEET),sheet_sha256=base.digest(SHEET),all_four_name_width_pages=True))
    base.save(LIVE,dict(candidate_sha256=sha,baseline_sha256=prior["candidate_sha256"],ordinary_Nagasaki_voyage=True,
        complete_panels=panels,retained_exact_panels=7,corrected_frame=revised_frame,matched_controls=list(controls),
        observed_postdialogue_sea_transition=True,Osaka_arrival=False,hardware=False,
        sheet=str(PLAY_SHEET),sheet_sha256=base.digest(PLAY_SHEET),evidence=evidence))
    print("Verified the eight-panel encounter, corrected surrender and exact sea transition.",flush=True)


if __name__=="__main__":
    verify()

