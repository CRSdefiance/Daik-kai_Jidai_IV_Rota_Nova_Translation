"""Bind actual early Hangzhou Square and Tavern text to clean and installed records."""

from hashlib import sha256

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import observe_hangzhou_early_actual_20261122 as run
from scripts import reconcile_shared_display_20261121 as shared
from scripts import register_maria_opening_hodram_wraps_20261122 as latest
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask


base,current=run.base,run.current
ROOT=run.ROOT/"hangzhou"
OUTPUT=run.ROOT/"observed_dialogue_and_roles.json"
SAMPLES=(
    (32750,656,"Food Shop"), (33550,658,"Spices Shop"), (34350,657,"Spices Shop"),
    (35150,658,"Luxury Shop"), (35950,704,"Luxury Shop"), (37950,51,"Tavern"),
)
WORDING={
    51:(("Welcome! What will you have?",),"Barkeep",
        "The informal welcome leads directly into asking what the customer wants, just before the drink menu."),
    656:(("We only sell retail.",),"Shopkeeper",
         "The seller explains the shop's retail policy directly without inventing a minimum quantity."),
    657:(("You're a sailor, aren't you?","Try the Market for bulk trade."),"Shopkeeper",
         "Retain the friendly question and the advice to use the Market for wholesale business. The whole question tag is visible on its first line."),
    658:(("Business? Oh, it's been all right.","I'm hoping a good deal comes along."),"Shopkeeper",
         "The seller echoes the topic, describes business as passable, and hopes a good opportunity turns up. The same valid reply is shared by two shops."),
    704:(("The Ming dynasty once thrived. Now","eunuchs do as they please, and the",
          "government sinks deeper into chaos.","It's dreadful."),"Shopkeeper",
         "Keep the contrast between Ming prosperity and the speaker's criticism of eunuch rule and growing disorder. The final reaction is personal rather than a historical claim by the narrator."),
}


def main():
    assert not OUTPUT.exists()
    inputs,_,end,origin,donor=run.schedule("hangzhou")
    terminal,log,report,release,new=map(base.load,(
        ROOT/"terminal.json",ROOT/"requests.json",ROOT/"capture/capture_report.json",current.RELEASE,latest.RELEASE))
    assert base.digest(current.ROM)==release["candidate_sha256"]==terminal["ROM_sha256"]==report["ROM_sha256"]
    assert base.digest(latest.ROM)==new["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"]==inputs and report["frames"]==end
    assert report["battery_save_preloaded"]["source_sha256"]==donor["source_sha256"]==base.digest(donor["source"])
    assert log["all_host_slots_restored_and_core_file_exact"] and not log["errors"] and not log["mismatches"]
    assert all(base.digest(path)==digest for path,digest in terminal["evidence"].items())
    assert terminal["target_COMMON_calls"]==log["source_requests"]

    clean,rom,newest=map(base.NdsImage.open,(current.native.CLEAN,current.ROM,latest.ROM))
    arm=rom.read_file(shared.ARM)
    paths=(shared.ARM,shared.COMMON,"/GRP/KANJI.FNT")
    assert all(rom.read_file(path)==newest.read_file(path) for path in paths)
    sc3="/data/SC3.DK4"
    banks=[current.native.IlnkContainer.parse(image.read_file(sc3)).blocks for image in (rom,newest)]
    assert banks[0][33]==banks[1][33]
    led=shared.workflow.common_message_entries(clean.read_file(shared.COMMON),clean.read_file(shared.ARM))
    active=shared.entries(rom)
    font=GameAsciiFont.from_arm9(arm)
    frames=shots(report)
    requests=[row for row in log["source_requests"] if row["frame"]>31000]
    assert len(requests)==2*len(SAMPLES)
    result=[]
    for (frame,ident,facility),first,second in zip(SAMPLES,requests[::2],requests[1::2],strict=True):
        assert [first["PC"],second["PC"]]==[0x0205528C,0x020534F4]
        assert first["frame"]==second["frame"]<frame
        assert ident==first["message_ID"]==second["message_ID"]
        lines,role,note=WORDING[ident]
        shot=frames[frame]
        image=captured(shot)
        body=body_mask(image,font,lines)
        pixels,bounds=complete_mask(font,role,image,16,277,(98,97,98))
        before,after=led[ident],active[ident]
        english=after.text.decode("cp932")
        assert " ".join(english.split())==" ".join(lines)
        result.append(dict(frame=frame,message_ID=ident,facility=facility,
            Japanese=before.text.decode("cp932"),installed_English=english,source_hex=before.text.hex(),current_hex=after.text.hex(),
            source_reference=reference(before),current_reference=reference(after),capture=shot,observed_lines=list(lines),
            nameplate=dict(text=role,complete_pixels=pixels,bounds=bounds),exact_body=body,request=first,
            decision="wording retained",localization_note=note))
    open_list=base.load(shared.OUTPUT)
    remaining={r["message_ID"] for r in open_list["records"]}
    assert len(remaining)==276 and not (remaining & {r["message_ID"] for r in log["source_requests"]})
    base.save(OUTPUT,dict(tested_candidate_sha256=release["candidate_sha256"],bound_current_candidate_sha256=new["candidate_sha256"],
        ordinary_facility_navigation=True,native_common_calls_total=len(log["source_requests"]),
        ordinary_city_dialogue_holds=result,distinct_records=sorted(WORDING),initialized_Hangzhou_opening_bytes_exact=True,
        settings_and_glyph_assets_exact=list(paths),existing_save_copy_for_captain_availability=True,
        new_editorial_credit=0,alternate_stored_caller_requests=[],open_display_keys_closed=0,
        wrap_followup=dict(message_ID=704,guide="Keep the transition Now with the clause it introduces if the owned shared consumer allows a fuller sentence break."),
        evidence=terminal["evidence"]))
    print(f"Verified six ordinary Hangzhou holds and five distinct records on the latest compatible assets.")


if __name__=="__main__":
    main()

