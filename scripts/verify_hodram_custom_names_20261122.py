"""Verify the ordinary deletion correction and bind the separate literal-name rendering defect."""

from pathlib import Path
from struct import unpack_from

from PIL import Image,ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_hodram_name_delete_20261122 as replay
from scripts import stage_captain_name_delete_20261122 as stage
from scripts.audit_captain_name_latin_20261119 import BODY_COLOR,EDITOR_COLOR,glyphs
from scripts.verify_captain_name_storage_20261119 import FIELDS
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_rafael_custom_name_20261119 import BASE,require_string,snapshot


base,native=stage.base,stage.native
ROOT=stage.run.ROOT
REVIEW=Path("releases/all_routes_editorial_20261122_hodram_B24_B53_candidate/verification/registered_review.json")
LIVE=stage.ROOT/"verified_editor.json"
SHEET=stage.ROOT/"ordinary_editor_comparison.png"
DEFECT=ROOT/"first_mate_surname_expansion_finding.json"
DEFECT_SHEET=ROOT/"surname_expansion_witness.png"
MAX=b"HodramFIFIFIFIFI"
BASE_DELETED=MAX[:-2]
REENTERED_BASE=BASE_DELETED+b"I"
EXPECTED_FIELDS=(b"JoakimFI",b"BergstromFIFAFOF",b"Bergstrom FleetFIF")
SOURCE_ID="DK4_MES_B42_R0113"


def hold(report,frame,navigation=False):
    snapshot_key="read_only_pause_RAM_snapshots" if navigation else "read_only_capture_RAM_snapshots"
    report_row,= [r for r in report["frames_captured"] if r["frame"]==frame and r["path"].endswith(
        "_navigation.png" if navigation else "_cold_boot.png")]
    assert base.digest(report_row["path"])==report_row["PNG_sha256"]
    raw,receipt=snapshot(report[snapshot_key],frame,"sha256")
    with Image.open(report_row["path"]) as frame_image:
        image=frame_image.convert("RGB")
    return raw,image,dict(frame=frame,image=report_row,read_only_RAM=receipt)


def confirm_fields(raw,first):
    start=0x02192E8C
    return [require_string(raw,start+at,value) for at,value in zip((0,17,34,51),(first,*EXPECTED_FIELDS),strict=True)]


def verify_editor():
    assert not LIVE.exists()
    old,new=map(base.load,(stage.BASELINE,replay.REPORT))
    candidate=base.digest(stage.ROM)
    proof=base.load(stage.PROOF)
    assert new["ROM_sha256"]==candidate==proof["candidate_sha256"]
    assert old["ROM_sha256"]==proof["predecessor_sha256"]==base.digest(stage.parent.ROM)
    assert new["scripted_input_schedule"]==[e for e in old["scripted_input_schedule"] if e["start"]<replay.END]
    assert new["frames"]==replay.END
    for report in (old,new):
        assert report["cold_boot"] and not report.get("battery_save_preloaded") and not report["savestate_loaded"]
        assert not report["callback_errors"] and not any(v for k,v in report.items() if k.startswith("synthetic_"))

    a,b=map(base.NdsImage.open,(stage.parent.ROM,stage.ROM))
    arm=a.read_file(native.ARM)
    font=GameAsciiFont.from_arm9(arm)
    assert font==GameAsciiFont.from_arm9(b.read_file(native.ARM))
    assert a.read_file("/GRP/KANJI.FNT")==b.read_file("/GRP/KANJI.FNT")
    rows,pictures=[],[]
    for frame,old_name,new_name in (
        (3870,b"HodramFI",b"HodramFI"),
        (6270,MAX,MAX),(6570,MAX,MAX),
        (6690,BASE_DELETED,MAX[:-1]),(7170,REENTERED_BASE,MAX),
        (8900,EXPECTED_FIELDS[0],EXPECTED_FIELDS[0]),
        (12260,EXPECTED_FIELDS[1],EXPECTED_FIELDS[1]),
        (14300,EXPECTED_FIELDS[2],EXPECTED_FIELDS[2]),
    ):
        sources=[]
        for nav,run,wanted in ((True,old,old_name),(False,new,new_name)):
            raw,im,witness=hold(run,frame,nav)
            assert unpack_from("<I",raw,stage.CHILD+0xA0-BASE)[0]==(
                18 if frame==14300 else 16)
            widget=require_string(raw,stage.FIELD,wanted)
            px=glyphs(font,im,wanted.decode("ascii"),(60,245),EDITOR_COLOR,200)
            sources.append(dict(name=widget,complete_glyphs=px,evidence=witness))
            if frame in (6570,6690,7170):
                pictures.append((f"{'Before' if nav else 'After'} {frame} / {wanted.decode()}",im))
        rows.append(dict(frame=frame,before=sources[0],after=sources[1]))

    accepted=[]
    for nav,run,first in ((True,old,REENTERED_BASE),(False,new,MAX)):
        raw,im,witness=hold(run,14520,nav)
        fields=confirm_fields(raw,first)
        for value,y in zip((first,*EXPECTED_FIELDS),(221,243,265,287),strict=True):
            glyphs(font,im,value.decode("ascii"),(89,y),EDITOR_COLOR,202)
        accepted.append(dict(fields=fields,evidence=witness))
        pictures.append((f"{'Before' if nav else 'After'} / confirmed native fields",im))

    canvas=Image.new("RGB",(1024,412*4),"#263238")
    labels=ImageDraw.Draw(canvas)
    for i,(caption,image) in enumerate(pictures):
        x,y=(i%2)*512,(i//2)*412
        labels.text((x+4,y+2),caption,fill="white")
        canvas.paste(image.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+19))
    canvas.save(SHEET)
    base.save(LIVE,dict(candidate_sha256=candidate,predecessor_sha256=old["ROM_sha256"],ordinary_controls_only=True,
        editable_results=rows,confirmation=accepted,sheet=str(SHEET),sheet_sha256=base.digest(SHEET),
        deletion_before_characters=2,deletion_after_characters=1,over_capacity_input_rejected=True,
        new_dialogue_credit=0,hardware=False,
        evidence={str(p):base.digest(p) for p in (stage.BASELINE,replay.REPORT,stage.PROOF)}))


def bind_second_defect():
    assert not DEFECT.exists()
    report=base.load(stage.BASELINE)
    assert report["ROM_sha256"]==base.digest(stage.parent.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k,v in report.items() if k.startswith("synthetic_"))
    clean,current=map(base.NdsImage.open,(native.CLEAN,stage.parent.ROM))
    arm=current.read_file(native.ARM)
    font=GameAsciiFont.from_arm9(arm)
    raw,im,bad=hold(report,24320,True)
    cpu,get=get_machine(arm,raw)
    captain=get(0xCB184)+0x19E4
    assert get(0x7F244)==1
    source=current.read_file("/data/SC1.DK4")
    lookup={r["id"]:r for r in base.load(REVIEW)["records"] if r["block"]==42}
    jp=clean.read_file("/data/SC1.DK4")
    clean_block,current_block=[native.IlnkContainer.parse(archive).blocks[42] for archive in (jp,source)]
    refs=[]
    for ident in ("DK4_MES_B42_R0015",SOURCE_ID,"DK4_MES_B42_R0116"):
        prior=lookup[ident]
        assert all(prior["review"].values())
        a,b=prior["source_reference"],prior["registered_reference"]
        source_body=bytes.fromhex(prior["source_hex"])
        current_body=bytes.fromhex(b["exact_stored_hex"])
        assert clean_block[a["offset"]:a["offset"]+len(source_body)]==source_body
        assert current_block[b["offset"]:b["offset"]+len(current_body)]==current_body
        refs.append(dict(id=ident,Japanese=prior["Japanese"],source_meaning=prior["source_meaning"],
            English=prior["english"],speaker=prior["speaker"],review=prior["review"],
            retention_reason=prior["localization_note"],source_hex=source_body.hex(),
            source_ref=a,current_ref=b|{"candidate_sha256":report["ROM_sha256"],
                "archive_sha256":native.digest(source),"block_sha256":native.digest(current_block)}))
    first,middle,last,company=REENTERED_BASE,EXPECTED_FIELDS[0],EXPECTED_FIELDS[1],EXPECTED_FIELDS[2]
    values={"first":first,"middle":middle,"last":last,"company":company}
    actor=[]
    for field,offset,_,cap,*_ in FIELDS:
        value=values[field]
        assert len(value)<cap
        addr=captain+offset
        stored=bytes(cpu.mem_read(addr,cap))
        assert stored.split(b"\0",1)[0]==value
        actor.append(dict(field=field,original_offset=offset,native_byte_capacity=cap,
                          address=addr,loaded_hex=stored.hex(),exact_value=value.decode("ascii")))
    installed=bytes.fromhex(refs[1]["current_ref"]["exact_stored_hex"])[1:]
    assert installed.count(b"FA")==1 and installed.count(b"FI")==installed.count(b"FO")==0
    expanded=installed.replace(b"FA",last)
    require_string(raw,0x0218EDC8,expanded)
    corrupted=b"Bergstrom"+first+last+company+b"F"
    assert last==b"BergstromFIFAFOF"
    bad_rows=("One of your speeches,",
        "Admiral "+corrupted[:28].decode(),
        corrupted[28:].decode()+",",
        "was the first thing that ever made")
    masks=[glyphs(font,im,text,(16,y),BODY_COLOR,232) for text,y in zip(bad_rows,(297,313,329,345),strict=True)]
    later, outro, after=hold(report,24670,True)
    require_string(later,0x0218EDC8,expanded)
    glyphs(font,outro,"me shake with eagerness for battle.",(22,297),BODY_COLOR,232)
    name_raw,headed,name_witness=hold(report,25020,True)
    joined=first+b" "+last
    require_string(name_raw,0x022A4F78,joined)
    glyphs(font,headed,joined.decode(),(16,277),(98,97,98),215)
    sheet=Image.new("RGB",(1024,820),"#263238")
    caption=ImageDraw.Draw(sheet)
    for i,(meaning,image) in enumerate((("Rendered extra text in Charles's first page",im),
        ("Extra page for the end of his sentence",outro),("Literal spelling in Hodram's nameplate",headed))):
        x,y=(i%2)*512,(i//2)*410
        caption.text((x+4,y+2),meaning,fill="white")
        sheet.paste(image.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+19))
    sheet.save(DEFECT_SHEET)
    base.save(DEFECT,dict(candidate_sha256=report["ROM_sha256"],exact_record=refs[1],nameplate_and_neighbor_refs=[refs[0],refs[2]],
        all_four_actor_fields=actor,first_expanded_buffer_address=0x0218EDC8,first_expanded_hex=expanded.hex(),
        expected_name=last.decode(),visible_nested_expansion_hex=corrupted.hex(),visible_complete_first_page_masks=masks,
        first_page=bad,incorrect_extra_page=after,correct_literal_nameplate=name_witness,
        observed_in_ordinary_opening=True,engine_consumer_fix_pending=True,new_editorial_credit=0,
        sheet=str(DEFECT_SHEET),sheet_sha256=base.digest(DEFECT_SHEET),
        evidence={str(p):base.digest(p) for p in (REVIEW,stage.BASELINE)}))


if __name__=="__main__":
    bind_second_defect()
    verify_editor()

