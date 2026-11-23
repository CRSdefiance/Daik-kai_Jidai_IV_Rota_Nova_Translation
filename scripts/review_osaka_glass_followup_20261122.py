"""Reconcile Osaka's glass exchange on all four routes and check two proposed replies."""

from types import SimpleNamespace

from PIL import Image, ImageDraw

from scripts import observe_osaka_town_20261122 as voyage
from scripts.checkpoint_flagged_phrase_and_julio_20261119 import native
from scripts import stage_london_guild_assignments_20261118 as compiler
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts.verify_all_routes_next_phrase_wraps_20261118 import clipped_renderer


base,current = voyage.base,voyage.current
ROOT = voyage.ROOT/"editorial"
BLOCKS = (200,192,188,161)
REVIEW = ROOT/"contextual_review.json"
PROOF = ROOT/"stored_and_native_preflight.json"
SHEET = ROOT/"revised_dialogue.png"
PREVIOUS = "releases/all_routes_editorial_20261121_sofala_malacca_osaka_trends_candidate/verification/registered_review.json"
LATER = "releases/all_routes_editorial_20261122_hodram_B181_B200_candidate/verification/registered_review.json"
CONTEXT = "In the Osaka Square, a daimyo admires a piece of glass. The guildmaster agrees politely and explains its name. The daimyo orders him to gather more, then the game forecasts a glass trend."
NOTES = (
    ("He praises the object as a work of art.","The enthusiastic opening gives the guildmaster a cue to agree."),
    ("The guildmaster respectfully agrees with the daimyo.","As you say fits the courtly tone and leaves the next thought to the daimyo."),
    ("He guesses that a well-known artisan must have made something this fine.","The wording links his inference to the object's quality and leaves the maker unnamed."),
    ("The guildmaster politely agrees with the daimyo's inference.","Indeed answers the thought with the source's assent."),
    ("He didn't realize things like this had become fashionable.","The opening pause and admission turn his admiration into curiosity."),
    ("He asks what the object is called.","The brief, direct question cues the unfamiliar word."),
    ("The guildmaster explains that the object is called giyaman. The source glosses it as glass.","Keep the Japanese term and its gloss because the title repeats the term and the notice names the trade good."),
    ("He repeats the unfamiliar word as he considers it.","The pause and repetition give him time to take in the word before he gives an order."),
    ("He decides to keep the piece and orders the guildmaster to gather all the giyaman in town.","Keep his delight turning into an extravagant command and preserve the scope of the order."),
    ("The guildmaster respectfully accepts the order.","The acknowledgment ends the exchange with the order accepted and the collection still to come."),
    ("The notice forecasts a possible glass fashion in Osaka.","The forecast keeps the commodity, the town and the original uncertainty."),
)
CHANGES = {
    1: ("So it seems.","Indeed, my lord.","The source agrees formally. So it seems sounds like the guildmaster is qualifying the daimyo's judgment."),
    3: ("Indeed it is.","Indeed, my lord.","The daimyo has inferred who made the piece. An unqualified assent answers that claim naturally and keeps the respectful register."),
}


def main():
    assert not ROOT.exists()
    live=base.load(current.RELEASE)
    identity=base.digest(current.ROM)
    assert identity==live["candidate_sha256"] and base.digest(base.REGISTRY)==live["registry_sha256"]
    assert base.digest(native.CLEAN)==live["clean_input_sha256"]
    assert base.digest(current.MANIFEST)==live["manifest_sha256"]
    source,candidate=map(base.NdsImage.open,(native.CLEAN,current.ROM))
    clean_arm,arm=[rom.read_file(native.ARM) for rom in (source,candidate)]
    assert native.digest(arm)==live["target_ARM9_sha256"]
    ctx=SimpleNamespace(image=candidate,arm=arm)
    font=candidate.read_file("/GRP/KANJI.FNT")
    paint,fe=clipped_renderer(ctx),current_fe_painter(ctx)
    inv,_,_=native.scoped_inventory()
    rebuild=compiler.rebuild_function()
    prior=base.load(PREVIOUS)
    later={row["id"]:row for row in base.load(LATER)["records"] if row["id"] in {"DK4_MES_B192_R0014","DK4_MES_B192_R0030"}}
    assert len(later)==2
    rebound=set()
    manuscript,integrity,raster=[],[],[]
    proposed={}
    for route,no in enumerate(BLOCKS):
        file=f"/data/SC{route}.DK4"
        arj,are=(rom.read_file(file) for rom in (source,candidate))
        assert native.digest(are)==live[f"target_SC{route}_sha256"]
        ja,eng=[native.IlnkContainer.parse(bank).blocks[no] for bank in (arj,are)]
        j,e=[native.references(*native.raw_speeches(a,block,inv)) for a,block in ((clean_arm,ja),(arm,eng))]
        known=[row for row in prior["records"] if row["file_path"]==file and row["block"]==no]
        assert len(known)==len(j)==len(e)==len(NOTES)==11
        rows=[]
        for ordinal,(src,old,past,(meaning,reason)) in enumerate(zip(j,e,known,NOTES,strict=True)):
            selector=src["selector"]
            assert selector==old["selector"]==past["source_selector"]
            assert selector in (130,150,254) and src["complete_preamble_hex"]==old["complete_preamble_hex"]
            reviewed=PREVIOUS
            assert src["raw_hex"]==past["source_hex"]
            if past["registered_reference"]["exact_stored_hex"]!=old["raw_hex"]:
                past=later[past["id"]]
                reviewed=LATER
                rebound.add(past["id"])
            assert src["raw_hex"]==past["source_hex"]
            assert past["registered_reference"]["exact_stored_hex"]==old["raw_hex"]
            assert all(past["review"].values())
            japanese=bytes.fromhex(src["raw_hex"])[1:].decode("cp932")
            prev=" ".join(bytes.fromhex(old["raw_hex"])[1:].decode("ascii").split())
            assert prev==past["english"]
            revised=ordinal==3 and route in CHANGES
            if revised:
                baseline,english,reason=CHANGES[route]
                assert prev==baseline and japanese=="さようでございます"
            else:
                english=prev
            cols=dict(id=past["id"],route=route,block=no,file_path=file,
                source_selector=selector,kind="system-FE" if selector==254 else "progressive",
                native_command_word=0x4000,speaker=past["speaker"],context=CONTEXT,
                source_meaning=meaning,localization_note=reason,Japanese=japanese,
                source_hex=src["raw_hex"],current_hex=old["raw_hex"],previous_English=prev,english=english,
                source_reference=src|{"file_path":file,"block":no,"block_sha256":native.digest(ja)},
                current_reference=old|{"file_path":file,"block":no,"block_sha256":native.digest(eng)},
                decision="revision" if revised else "retention",protected_phrases=[],
                earlier_approved_reference=past["registered_reference"],prior_editorial_review=reviewed,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
            rows.append(cols)
        manuscript.extend(rows)
        target,commands,plans=rebuild(rows,ja,eng,inv,clean_arm,arm,fe)
        changed = [r for r in rows if r["decision"]=="revision"]
        assert len(changed)==len(plans)==int(route in CHANGES)
        assert (target!=eng)==bool(changed)
        if changed:
            row,=changed
            command,=[c for c in commands if c["record_ids"]==[row["id"]]]
            raw=bytes.fromhex(command["stored"])
            start=command["stored_offset"]
            assert target[start:start+len(raw)]==raw and raw[5]==150
            body=raw[6:raw.index(0,6)]
            assert body.decode("ascii").rstrip()==row["english"]
            checked=paint(arm,font,body)
            page,=checked["pages"]
            assert checked["complete_consumed_bytes"]==len(body) and page["native_independent_plane_equal"]
            pixels=bytes.fromhex(page["native_plane_hex"])
            raster.append(dict(id=row["id"],route=route,english=row["english"],plan=plans[row["id"]],
                native_complete_plane_hex=pixels.hex(),exact_consumer_sha256=native.digest(arm),
                complete_original_body_bytes=body.hex(),complete_original_body_glyphs_and_bounds=True))
            bank=native.IlnkContainer.parse(are)
            bank.blocks[no]=target
            archived=bank.to_bytes()
            proposed[file]=archived
            bank.blocks[no]=eng
            assert bank.to_bytes()==are
            integrity.append(dict(file_path=file,block=no,predecessor_sha256=native.digest(are),
                compiled_archive_sha256=native.digest(archived),compiled_block_hex=target.hex(),
                compiled_block_sha256=native.digest(target),command_map=commands,captured_gameplay_pending=True))
    before=native.files(candidate)
    for path,data in proposed.items():
        candidate.replace_file(path,data)
    after=native.files(candidate)
    assert before.keys()==after.keys() and {path for path in before if before[path]!=after[path]}=={"/data/SC1.DK4","/data/SC3.DK4"}
    proposed_sha=native.digest(candidate.rom.save())
    for path in proposed:
        candidate.replace_file(path,before[path])
    assert bytes(candidate.rom.save())==current.ROM.read_bytes()
    assert len(manuscript)==44 and len(raster)==2 and rebound==set(later)
    ROOT.mkdir()
    base.save(REVIEW,dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",
        target_locale="en-US",review_gates=["source","context","localization","naturalness","formatting"],
        records=manuscript,prior_review=PREVIOUS,prior_review_sha256=base.digest(PREVIOUS),
        later_review=LATER,later_review_sha256=base.digest(LATER),later_matched_ids=sorted(rebound),
        prior_ROM=identity,proposed_changes=2,justified_retentions=42,new_editorial_credit=0,full_goal_complete=False))
    canvas=Image.new("RGB",(892,157),"#263238")
    labels=ImageDraw.Draw(canvas)
    for i,row in enumerate(raster):
        x=i*446
        labels.text((x+6,4),row["id"],fill="white")
        ink=bytes(0 if n else 250 for n in bytes.fromhex(row["native_complete_plane_hex"]))
        canvas.paste(Image.frombytes("L",(216,64),ink).resize((432,128),Image.Resampling.NEAREST),(x+6,21))
    canvas.save(SHEET)
    base.save(PROOF,dict(prior_ROM=identity,proposed_ROM_sha256=proposed_sha,compiled_blocks=integrity,
        exact_whole_ROM_inverse=True,native_pages=raster,sheet=str(SHEET),sheet_sha256=base.digest(SHEET),
        manuscript=str(REVIEW),manuscript_sha256=base.digest(REVIEW),direct_visual_pending=True,ROM_written=False))
    print("Reviewed the 44 Osaka turns and compiled two translated replies with complete native page checks.",flush=True)


if __name__=="__main__":
    main()

