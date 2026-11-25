"""Bind the large harbor and ship paintings to the early Rafael sequence."""
from pathlib import Path
from types import SimpleNamespace

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from scripts import checkpoint_story_still_commands_20261120 as still
from scripts import observe_rafael_early_harbor_20261121 as run
from scripts import reconcile_shared_display_20261121 as worklist
from scripts import research_graphics_file_open_v301 as movie


base,native = run.base,run.active.native
ROOT = run.ROOT/"rafael"
REPORT = ROOT/"capture/capture_report.json"
TRACE = ROOT/"requests.json"
OUTPUT = worklist.OUTPUT.with_name("rafael_harbor_shared_artwork_20261121_v1.json")
ARCHIVE = "/data/SC0.DK4"
OLDER = worklist.OUTPUT.with_name("opening_scene_labels_20261115_v1.json")
TARGETS = {
    3394:(20,"/FLS/M20.fls","港町２（大）","Port Town 2 (Large)",26,3000),
    3397:(21,"/FLS/m21.fls","３人と船（大）","Three People and a Ship (Large)",0,7021),
}


def upper(frame):
    assert base.digest(frame["path"]) == frame["PNG_sha256"]
    with Image.open(frame["path"]) as image:
        return image.convert("RGB").crop((0,0,256,192))


def main():
    assert not OUTPUT.exists()
    release,report,trace = map(base.load,(run.active.RELEASE,REPORT,TRACE))
    assert base.digest(run.active.ROM)==release["candidate_sha256"]==report["ROM_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(native.CLEAN)==release["clean_input_sha256"]
    assert report["frames"]==run.END and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not report.get("battery_save_preloaded")
    assert not any(value for key,value in report.items() if key.startswith("synthetic_"))
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert [(r["message_ID"],r["PC"]) for r in trace["source_requests"]]==[(120,0x0205528C),(120,0x020534F4)]
    clean,current = map(base.NdsImage.open,(native.CLEAN,run.active.ROM))
    arms = [im.read_file(native.ARM) for im in (clean,current)]
    assert native.digest(arms[1])==release["target_ARM9_sha256"]
    source = worklist.workflow.common_message_entries(clean.read_file(worklist.COMMON),arms[0])
    installed = worklist.entries(current)
    earlier = base.load(worklist.OUTPUT)
    retain = {r["message_ID"]:r for r in earlier["records"]}
    for ident,row in retain.items():
        assert source[ident].text.hex()==row["source_hex"] and installed[ident].text.hex()==row["current_hex"]
        assert worklist.workflow.reference(source[ident])==row["source_reference"]
        assert worklist.workflow.reference(installed[ident])==row["current_reference"]
    assert len(retain)==276
    decode = still.explicit_walk()
    frames = {r["frame"]:r for r in report["frames_captured"]}
    baseline = {r["frame"]:r for r in base.load(OLDER)["ordinary_emulator_runs"]["rafael"]["held_frames"]}
    actual, associations, panels = {}, [], []
    for side,image,arm in zip(("clean","current"),(clean,current),arms,strict=True):
        data = image.read_file(ARCHIVE)
        scene = native.IlnkContainer.parse(data).blocks[44]
        analyzed = decode(arm,scene)
        assert analyzed["error"] is None
        actual[side]={}
        for number,(movie_id,path,_,_,_,_) in TARGETS.items():
            request, = [x for x in analyzed["native_movie_requests"] if x["args"]==[movie_id,0,1,0]]
            at = request["source_offset"]
            assert any(c["offset"]==at and c["word"]==0x4900|(movie_id-20) and c["native_extent"]==2
                       for c in analyzed["rows"])
            hit, = movie.generated(image,arm,movie_id)["SDK_open_events"]
            assert hit["actual_path"]==path and hit["file_sha256"]==native.digest(image.read_file(path))
            actual[side][number]=dict(original_movie_request=request,block=44,path=ARCHIVE,command_offset=at,
                exact_command_hex=scene[at:at+2].hex(),archive_sha256=native.digest(data),block_sha256=native.digest(scene),
                file_open=hit)
    for number,(_,path,jp,english,index,frame) in TARGETS.items():
        data,b = [im.read_file(path) for im in (clean,current)]
        old,new = [FlsArchive(raw).texture(index) for raw in (data,b)]
        assert old==new and (old.width,old.height)==(256,256)
        row=retain[number]
        assert source[number].text.decode("cp932")==jp and row["draft"]["english"]==english
        assert not row["draft"]["review"]["formatting"]
        shot=frames[frame]
        picture=upper(shot)
        earlier_match=None
        if number==3394:
            past=baseline[frame]
            assert past["match"] and upper(past["current"]).tobytes()==picture.tobytes()
            earlier_match=past["current"]
        else:
            quant=bytes(x>>3 for x in range(256))
            expected=old.render().convert("RGB").crop((0,0,256,192))
            assert picture.tobytes().translate(quant)==expected.tobytes().translate(quant)
        panels.append((english,picture))
        associations.append(dict(message_ID=number,Japanese=jp,English=english,editorial_decision="retain draft",
            localization_note=("Keep the specific second port view and its large format." if number==3394 else
                                "Keep the three figures and ship in the large harbor scene."),
            source_reference=row["source_reference"],current_reference=row["current_reference"],current_hex=row["current_hex"],
            art=dict(path=path,index=index,clean_sha256=native.digest(data),installed_sha256=native.digest(b),
                     unchanged_texture_sha256=native.digest(old.indices)),
            original_story_proof={side:actual[side][number] for side in actual},observed=shot,
            reused_earlier_exact_upper=earlier_match,
            full_texture_view_matched_at_native_rgb_precision=number==3397,
            stored_label_used_as_text=False,other_possible_display_owners="open"))
    sheet=ROOT/"harbor_artwork_holds.png"
    canvas=Image.new("RGB",(1024,421),"#263238")
    draw=ImageDraw.Draw(canvas)
    for i,(tag,image) in enumerate(panels):
        x=i*512
        draw.text((x+7,6),tag,fill="white")
        canvas.paste(image.resize((512,384),Image.Resampling.NEAREST),(x,25))
    canvas.save(sheet)
    receipts = {str(p):base.digest(p) for p in (REPORT,TRACE,OLDER,worklist.OUTPUT)}
    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],clean_sha256=release["clean_input_sha256"],
        ordinary_New_Game_gameplay=True,hardware=False,observed_stored_label_requests=0,
        anchored_shared_description_count=2,open_stored_COMMON_display_references=len(retain),new_editorial_credit=0,
        records=associations,sheet=dict(path=str(sheet),sha256=base.digest(sheet)),evidence=receipts))
    print("Verified two independent early harbor artwork paths and rebound all 276 stored records.")


if __name__=="__main__":
    main()
