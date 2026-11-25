"""Review and stage the six displayed About Extras pages as one sequence."""

import argparse
from dataclasses import replace
from inspect import getsource
from pathlib import Path
from struct import pack_into, unpack_from
import sys

from PIL import Image, ImageChops

from dk4tool.dialogue import layout
from dk4tool.dialogue.codec import DialogueToken, parse_markup, tokens_to_bytes
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.grand_race_help import PROFILE as validated_help
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_gallery_options_legacy_20261114 as controls
from scripts import headless_desmume_v193 as harness
from scripts import observe_extras_tie_in_common_20261114 as original
from scripts.checkpoint_market_shared_consumers_20261114 import ARM, COMMON, font_mask
from scripts.materialize_extras_menu_v1 import ARM9_RECORDS
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


parent,base=original.parent,original.parent.base
ROOT=original.ROOT/"revision_v2"
ROM=ROOT/"About_Extras_RESEARCH_ONLY.nds"
STORED=ROOT/"staged.json"
LIVE=ROOT/"live.json"
REVIEW=Path("translations/editorial_checkpoints/SharedText_20261110_v1/extras_tie_in_review_20261114_v2.json")
PROFILE=replace(validated_help,name="about-extras-32-cell-12-pixel-rows",window_width_px=192,max_lines=6)
TABLE=0x16DA40
GATES=("source","context","localization","naturalness","formatting")
PAGES=(
    (2099,0x16DE74,0x16DE74,0x16DEFC,None,
     "Introduces the tie-in with the PC game Uncharted Waters Online. Playing both games expands what you can do in Rota Nova.",
     "The introduction already identifies the other game and makes clear that the tie-in adds something to this game."),
    (2599,0x16DD70,0x16DD70,0x16DDEC,
     "Play Uncharted Waters Online. A certain character will tell you a village name and its Promised Words.",
     "Play the Online game and learn the village name and its password by speaking with a particular character.",
     "The paired name and password lead directly into Step 2. Use Promised Words, the name shown by the village interface."),
    (3099,0x16DCF4,0x16DCF4,0x16DD70,
     "Find that village in Rota Nova and enter its Promised Words. You can then trade for valuable new goods.",
     "Find that village in this game and use the password to trade with the village. Valuable trade goods become available.",
     "Identify Rota Nova as the game the player returns to, preserve the password term, and keep the new goods as trade goods."),
    (3599,0x16DDEC,0x16DDEC,0x16DE68,
     "There are 24 villages, each with its own trade goods. Visit them to see what they sell.",
     "There are 24 villages in all, and the trade goods that appear differ by village. The text invites the player to see them in person.",
     "Keep all 24 villages and their different goods. This refers to commodities for sale and the invitation to explore."),
    (4099,0x16DC48,0x16DC94,0x16DCE8,
     "Visit the official Uncharted Waters Online site and set sail again!",
     "The closing invitation directs players to the official website of Uncharted Waters Online to continue their voyages.",
     "Restore the word official and the full game title. Treat the invitation as the original game’s copy."),
    (4599,0x16DC94,0x16DC48,0x16DC80,
     "Please note that online services may change or end.",
     "Depending on circumstances, network content services may change or end. The message asks players to keep that in mind.",
     "Keep the service caveat. The Japanese does not say changes will happen without notice."),
)


def encode(english, step):
    source=checked_text(getsource(layout._balanced_wrap),{
        'final = end + 1 == count': '''final = end + 1 == count
            if not final and (labels[end].rstrip(".,!?"), labels[end+1].rstrip(".,!?")) in PROTECTED:
                continue''',
        "len(\" \".join(labels[start:end + 1])) <= 8":"len(\" \".join(labels[start:end + 1])) <= 11",
    })
    env=vars(layout) | dict(PROTECTED={("Uncharted","Waters"),("Waters","Online"),("Promised","Words"),("Rota","Nova"),("trade","goods"),("new","goods")})
    exec(compile(source,__file__+"::existing-balancing-with-components-of-names-protected","exec"),env)
    # The STEP line is a source heading. The body still receives automatic breaks.
    tokens=env["_balanced_wrap"](parse_markup(english),replace(PROFILE,max_lines=5 if step else 6))
    assert tokens is not None
    if step:
        tokens=[*parse_markup(f"STEP {step}"),DialogueToken("line_break","",b"\n"),*tokens]
    raw=tokens_to_bytes(tokens,guard_linebreaks=True,pair_phase_safe_breaks=True)
    lines=[part.strip() for part in raw.decode("ascii").split("\n")]
    assert ' '.join(lines)==(f"STEP {step} " if step else "")+english
    assert all(0<len(line)<=32 for line in lines) and len(lines)<=6
    return raw+b"\0",lines


def check_page(shot,font,lines):
    counts=[]
    for i,line in enumerate(lines):
        y=245+12*i
        counts.append(font_mask(shot,font,line,40,y,(38,y-1,228,y+11),(0,8,0)))
    assert all(shot.getpixel((x,y))!=(0,8,0)
        for x in range(38,228) for y in range(244+12*len(lines),321))
    return counts


def stage():
    assert not ROOT.exists() and not REVIEW.exists()
    release=base.load(parent.RELEASE)
    assert base.digest(parent.ROM)==release["candidate_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    assert base.digest(parent.parent.stage.CLEAN)==release["clean_input_sha256"]
    current,clean=map(base.NdsImage.open,(parent.ROM,parent.parent.stage.CLEAN))
    all_before=files(current)
    arm,ja=all_before[ARM],clean.read_file(ARM)
    assert parent.source.current.assets.edit.digest(arm)==release["target_ARM9_sha256"]
    for start,end in ((0x1040DC,0x104218),(0x10537C,0x1053EC),(0x1045A0,0x1045A4),(TABLE,TABLE+24)):
        assert arm[start:end]==ja[start:end]
    assert unpack_from("<I",arm,0x1045A0)[0]==0x0216DA40
    context,calls,screens=controls.verify_report(original,"tie_in_advance",release)
    assert not context["target_COMMON_calls"] and not calls
    old_rows={offset:(ident,japanese) for ident,offset,japanese,_,_ in ARM9_RECORDS}
    font=GameAsciiFont.from_arm9(arm)
    result=bytearray(arm)
    records,owned,expected_pointers,after_pointers=[],[],{},{}
    for index,(frame,source,replacement,end,english,meaning,note) in enumerate(PAGES):
        ident,jp=old_rows[source]
        jp_raw=jp.encode("cp932")+b"\0"
        saved=arm[source:arm.index(0,source)+1]
        field=TABLE+4*index
        assert ja[source:source+len(jp_raw)]==jp_raw
        assert unpack_from("<I",arm,field)[0]==source+0x02000000
        old_lines=[part.strip() for part in saved[:-1].decode("ascii").split("\n")]
        before_mask=check_page(controls.screen(screens[frame]),font,old_lines)
        documentation=dict(id=ident,speaker="About Extras",file_path=ARM,full_sequence_order=index+1,
            context="About Extras leads from the PC connection through the village password instructions to the closing invitation and service notice.",
            source_Japanese=jp,source_hex=jp_raw.hex(),source_meaning=meaning,localization_note=note,
            current_English=" ".join(old_lines),current_page=screens[frame],current_glyph_counts=before_mask,
            current_reference=dict(pointer_field=field,ARM9_offset=source,exact_stored_hex=saved.hex()),
            decision="revision" if english else "retention",review=dict.fromkeys(GATES,True)|{"formatting":False})
        if english:
            step=index if index in (1,2) else None
            encoded,lines=encode(english,step)
            assert len(encoded)<=end-replacement,(ident,len(encoded),end-replacement,lines)
            start_of_current_record=replacement
            null=arm.index(0,start_of_current_record)
            assert arm[null:end]==bytes(end-null)
            owned.append((replacement,end))
            expected_pointers[field]=source
            after_pointers[field]=replacement
            result[replacement:end]=encoded.ljust(end-replacement,b"\0")
            pack_into("<I",result,field,0x02000000+replacement)
            documentation.update(english=f"STEP {step}{{LB}}{english}" if step else english,lines=lines,
                revised_reference=dict(pointer_field=field,ARM9_offset=replacement,capacity=end-replacement,exact_stored_hex=encoded.hex()))
            if step:
                documentation["manual_break_reason"]="The original screen sets the numbered step heading on its own line."
        else:
            documentation.update(english=" ".join(old_lines),lines=old_lines)
        records.append(documentation)
    assert byte_pointer_references(arm,owned)==expected_pointers
    assert byte_pointer_references(result,owned)==after_pointers
    owned_fields=[(k,k+4)for k in expected_pointers]
    for left,right in ((0x16DC80,0x16DC94),(0x16DCE8,0x16DCF4),(0x16DE68,0x16DE74),(0x16DE74,0x16DF10)):
        assert arm[left:right]==result[left:right]
    verify_runtime(result,release)
    target=bytes(result)
    assert all(any(left<=at<right for left,right in [*owned,*owned_fields])
               for at,(before,after) in enumerate(zip(arm,target,strict=True)) if before!=after)
    current.replace_file(ARM,target)
    after=files(current)
    assert after.keys()==all_before.keys() and {p for p in all_before if all_before[p]!=after[p]}=={ARM}
    ROOT.mkdir()
    current.save(ROM)
    current.replace_file(ARM,arm)
    assert bytes(current.rom.save())==parent.ROM.read_bytes()
    native_source=common_message_entries(clean.read_file(COMMON),ja)
    native_current=owned_entries(all_before[COMMON],arm,parent.source.current.assets.edit.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    pending=[]
    for ident in (3317,3318,3319):
        a,b=native_source[ident],native_current[ident]
        assert a.text==b.text
        pending.append(dict(message_ID=ident,Japanese=a.text.decode("cp932"),source_reference=reference(a),current_reference=reference(b),
            exact_hex=a.text.hex(),other_consumer_pending=True))
    base.save(REVIEW,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=list(GATES),candidate_sha256=release["candidate_sha256"],records=records,actual_COMMON_requests=calls,
        legacy_tie_in_records=pending,initial_evidence=context["evidence"],zero_duplicate_credit=True,full_goal_complete=False))
    base.save(STORED,dict(parent_sha256=release["candidate_sha256"],target_sha256=base.digest(ROM),
        target_ARM9_sha256=parent.source.current.assets.edit.digest(target),owned_body_and_pointer_spans=owned+owned_fields,
        exact_parent_inverse=True,review_sha256=base.digest(REVIEW)))
    base.save(ROOT/"inputs.json",original.schedule("tie_in_advance")[0])
    print([(r["id"],r["lines"]) for r in records])


def capture():
    assert base.digest(ROM)==base.load(STORED)["target_sha256"]
    events,frames,end,_,_=original.schedule("tie_in_advance")
    assert events==base.load(ROOT/"inputs.json")
    old=sys.argv
    try:
        sys.argv=[*old[:1],"--rom",str(ROM),"--out",str(ROOT/"capture"),"--inputs-json",str(ROOT/"inputs.json"),
                  "--frames",str(end),"--capture-every","999999","--capture-at",*map(str,frames)]
        harness.main()
    finally:
        sys.argv=old


def verify():
    assert not LIVE.exists()
    data=base.load(REVIEW)
    s=base.load(STORED)
    path=ROOT/"capture/capture_report.json"
    report=base.load(path)
    assert report["ROM_sha256"]==s["target_sha256"]==base.digest(ROM)
    assert report["cold_boot"] and not report.get("battery_save_preloaded") and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"]==base.load(ROOT/"inputs.json")
    assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
    assert base.digest(REVIEW)==s["review_sha256"]
    shot={p["frame"]:p for p in report["frames_captured"]}
    img=base.NdsImage.open(ROM)
    font=GameAsciiFont.from_arm9(img.read_file(ARM))
    evidence={}
    rows=[]
    sheet=Image.new("RGB",(768,2*110),"#263238")
    for index,row in enumerate(data["records"]):
        frame=row["current_page"]["frame"]
        a,b=[controls.screen(q) for q in (row["current_page"],shot[frame])]
        diff=ImageChops.difference(a,b).getbbox()
        if row["decision"]=="retention":
            assert diff is None
        else:
            assert diff and 38<=diff[0]<diff[2]<=228 and 244<=diff[1]<diff[3]<=321
        glyphs=check_page(b,font,row["lines"])
        evidence[shot[frame]["path"]]=shot[frame]["PNG_sha256"]
        rows.append(row | dict(review=row["review"]|{"formatting":True},candidate_page=shot[frame],
            candidate_glyph_counts=glyphs,changed_pixels_bounding_box=diff))
        sheet.paste(b.crop((0,225,256,335)),(index%3*256,index//3*110))
    parent_report=base.load(original.ROOT/"tie_in_advance/capture/capture_report.json")
    baseline={p["frame"]:p for p in parent_report["frames_captured"]}
    returns=[1419,5099,5599]
    assert all(shot[n]["framebuffer_sha256"]==baseline[n]["framebuffer_sha256"] for n in returns)
    path_view=ROOT/"all_revised_panels.png"
    sheet.save(path_view)
    base.save(LIVE,data | dict(records=rows,target_ROM_sha256=s["target_sha256"],complete_revised_and_retained_masks=True,
        exact_navigation_control_frames=returns,actual_visual_review_pending=True,sheet=str(path_view),sheet_sha256=base.digest(path_view),
        live_evidence=evidence | {str(p):base.digest(p) for p in (path,STORED,REVIEW,Path(__file__))}))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step",choices=("stage","capture","verify"))
    globals()[parser.parse_args().step]()

