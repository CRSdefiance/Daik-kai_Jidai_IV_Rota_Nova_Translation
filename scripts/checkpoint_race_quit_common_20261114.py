"""Review the Grand Race rules and bind the original Quit Game and graphics paths."""

from pathlib import Path
from struct import unpack_from

from PIL import Image
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.grand_race_help import format_page
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import checkpoint_gallery_options_legacy_20261114 as checks
from scripts import observe_race_quit_common_20261114 as run
from scripts.checkpoint_market_shared_consumers_20261114 import ARM, COMMON, font_mask
from scripts.probe_button_prompt_native import machine
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_grand_race_native_v576 import PAGE_FRAMES


base,current=run.base,run.current
CHECKPOINT=Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT=CHECKPOINT/"grand_race_rules_and_quit_review_20261114_v1.json"
MANUSCRIPT=Path("translations/grand_race_rules_manuscript_v2.json")
TITLE_NOTES={
    "About the Race": "Retain the four-player limit, DS wireless connection, and distinction between host and joining players.",
    "Basic Rules": "The existing text explains the Touch Screen restriction, all seven checkpoints in any order, the first finisher and continued play for the others.",
    "Your Ship": "The save selection determines the flagship. Keep the clear distinction between its basic performance and the equipment, crew and items that have no effect.",
    "Race Area": "The existing text identifies four areas, the host's choice and the limit shown by the red border.",
    "Prizes": "Keep the two separate facts: finishing position determines prize money, and the prize goes into the player's saved funds.",
    "Map": "Keep the meaning of each symbol, the color order and the fact that passed checkpoints vanish from the player's map.",
    "Supplies": "Keep the barrel icon and its location, the slowing at zero food, and how to resupply.",
    "Time Limit": "The rule distinguishes each late player's disqualification and loss of prize money from the race being void if everyone is late.",
    "Stopping a Race": "Use 'drop out on your own' to make the individual withdrawal rule clear. Preserve the original instruction to turn off the DS and the result for every player.",
}
STOPPING = ("You can't drop out on your own mid-race. To stop playing, turn off your DS. "
            "If any player turns off their DS, the race ends for everyone.")
GATES = ("source","context","localization","naturalness","formatting")


def native_graphics_index(clean, arm):
    start, end, target = 0xF56AC,0xF56B4,0x692D4
    for lo,hi in ((start,end),(target,target+28),(0xF57A4,0xF57A8),(0x145E94,0x145E98)):
        assert clean[lo:hi] == arm[lo:hi]
    assert [offset for offset in range(0,len(clean)-3,4) if clean[offset:offset+4] == b"\x3e\x01\0\0"] == [0xF57A4]
    assert unpack_from("<I",arm,0xF57A4)[0] == 318
    table,hardware_register=unpack_from("<2I",arm,0x692E8)
    assert (table,hardware_register) == (0x0214599C,0x04000488)
    entry=table+4*318
    value=unpack_from("<I",arm,entry-0x02000000)[0]
    assert value == 0x06001000
    results=[]
    for label,data in (("clean",clean),("registered",arm)):
        cpu=machine(data)
        cpu.mem_map(0x04000000,0x1000)
        writes=[]
        def collect(u,access,address,size,word,opaque):
            writes.append((address,size,word))
        cpu.hook_add(UC_HOOK_MEM_WRITE,collect)
        stack=cpu.reg_read(UC_ARM_REG_SP)
        cpu.emu_start(0x02000000+start,0x02000000+end,count=12)
        assert cpu.reg_read(UC_ARM_REG_PC)==0x02000000+end and cpu.reg_read(UC_ARM_REG_SP)==stack
        assert writes == [(hardware_register,4,value)]
        results.append(dict(version=label,observed_isolated_writes=writes))
    return dict(message_id_lookalike=318,source_word_offset=0xF57A4,caller=0x020F56AC,callee=0x020692D4,
        graphics_table=table,graphics_entry=entry,native_port=hardware_register,value=value,original_CPU_fragment_runs=results,
        narrower_finding="This numeric reference selects a graphics register value. It supplies no COMMON string.")


def native_help_pages(arm, clean, frame_rows):
    font=GameAsciiFont.from_arm9(arm)
    loaded=machine(arm)
    original=base.load(MANUSCRIPT)
    assert current.assets.edit.digest(clean)==original["source_arm9_sha256"]
    results=[]
    for row in original["records"]:
        title=row["draft_english_title"]
        descriptor=row["descriptor_offset"]
        old_at=row["source_offset"]
        old=bytes.fromhex(row["source_hex"])
        assert clean[old_at:old_at+len(old)]==old
        title_ptr,body_ptr=unpack_from("<2I",bytes(loaded.mem_read(0x02000000+descriptor,8)))
        assert bytes(loaded.mem_read(title_ptr,len(title)+1))==title.encode("ascii")+b"\0"
        _,body,lines,_=format_page(row["english"])
        assert bytes(loaded.mem_read(body_ptr,len(body)+1))==body+b"\0"
        actual=frame_rows[PAGE_FRAMES[descriptor]]
        shot=checks.screen(actual).point(lambda n:n >> 3)
        header, head_bounds=complete_mask(font,title,shot,4,193,(0,31,0))
        plane=Image.new("1",(252,128))
        captures=[]
        for index,line in enumerate(lines):
            y=217+16*index
            count,bounds=complete_mask(font,line,shot,4,y,(28,28,28))
            assert bounds[2] <= 256 and bounds[3] < 364
            captures.append(dict(text=line,bounds=bounds,pixels=count))
            for col,char in enumerate(line):
                plane.paste(font.decode(char),(col*6,index*16+1))
        pixels=shot.load()
        assert all((pixels[x+4,y+216]==(28,28,28))==bool(plane.getpixel((x,y))) for y in range(128) for x in range(252))
        changed=title=="Stopping a Race"
        decision=dict(id=row["id"],title=title,speaker=row["speaker"],source_meaning=row["source_meaning"],
            context="The player opens this page from Grand Race, reads it alongside the related rules and can return to the menu.",
            localization_note=TITLE_NOTES[title],english=STOPPING if changed else row["english"],current_English=row["english"],
            Japanese=row["japanese"],decision="revision" if changed else "retention",
            review=dict.fromkeys(GATES,True) | {"formatting":not changed},
            source_reference=dict(ARM9_offset=old_at,exact_hex=old.hex()),current_reference=dict(
                descriptor_offset=descriptor,title_pointer=title_ptr,body_pointer=body_ptr,exact_hex=(body+b"\0").hex()),
            existing_live_page=dict(frame=actual, title_ink_pixels=header, title_bounds=head_bounds,
                line_pitch=16,complete_body_ink_and_spacing=True,lines=captures))
        if changed:
            _,draft,proposed_lines,_=format_page(STOPPING)
            assert len(draft)<=len(body) and b"  " not in STOPPING.encode("ascii")
            rendered=Image.new("RGB",(252,128),"#eee6d4")
            for index,line in enumerate(proposed_lines):
                assert 0<len(line)<=42
                for col,char in enumerate(line):
                    rendered.paste("#221810",(col*6,index*16,col*6+6,index*16+11),font.decode(char))
            preview=run.ROOT/"stopping_a_race_draft.png"
            rendered.resize((504,256),Image.Resampling.NEAREST).save(preview)
            decision.update(proposed_lines=proposed_lines,proposed_hex=(draft+b"\0").hex(),
                existing_body_slot_bytes=len(body)+1,proposed_body_bytes=len(draft)+1,
                offline_automatic_layout_preview=str(preview),preview_sha256=base.digest(preview))
        results.append(decision)
    assert len(results)==9
    return results


def main():
    assert not OUTPUT.exists()
    release=base.load(current.RELEASE)
    assert base.digest(current.ROM)==release["candidate_sha256"]
    assert base.digest(current.stage.CLEAN)==release["clean_input_sha256"]
    target,source=map(base.NdsImage.open,(current.ROM,current.stage.CLEAN))
    arm,clean=[im.read_file(ARM) for im in (target,source)]
    assert current.assets.edit.digest(arm)==release["target_ARM9_sha256"]
    original=common_message_entries(source.read_file(COMMON),clean)
    active=owned_entries(target.read_file(COMMON),arm,current.assets.edit.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    quit_trace,quit,quit_frames=checks.verify_report(run,"quit",release)
    race_trace,race,race_frames=checks.verify_report(run,"race",release)
    assert [r["message_ID"] for r in quit]==[319,319] and [r["PC"] for r in quit]==[0x0205528C,0x020534F4]
    assert all(r["caller_LR"]==0x02054680 for r in quit) and not race
    assert arm[0x3FC08:0x3FC40]==clean[0x3FC08:0x3FC40] and unpack_from("<I",arm,0x3FC3C)[0]==319
    assert active[319].text.decode("ascii").strip()=="Quit the game?"
    sample=quit_frames[5800]
    font=GameAsciiFont.from_arm9(arm)
    ink=font_mask(checks.screen(sample),font,"Quit the game?",16,297,(16,296,237,350),(0,8,0))
    pages=native_help_pages(arm,clean,race_frames)
    src,current_text=original[318],active[318]
    ledger=base.load(base.LEDGER)
    assert ledger["current_integrated_candidate"]["sha256"]==release["candidate_sha256"]
    assert 318 in ledger["pending_shared_consumer_checkpoint_20261114"]["remaining_legacy_keys"]
    evidence=dict(quit=quit_trace["evidence"],race=race_trace["evidence"])
    for case,expected in (
        ("quit","e7b70504bcbb28434d48cc46453663891769fa601efdb7c2da798b6e19e590ce"),
        ("race","6cb5b3b0e5aef4a11538474cf64f5f21b59c16cc924154d8385f46473dd6ca32"),
    ):
        path=run.ROOT/case/"review_sheet.png"
        assert base.digest(path)==expected
        evidence[str(path)]=expected
    base.save(OUTPUT,dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",target_locale="en-US",
        review_gates=list(GATES),candidate_sha256=release["candidate_sha256"],clean_sha256=release["clean_input_sha256"],
        records=pages,actual_quit=dict(common_ID=319,source_reference=reference(original[319]),
            current_reference=reference(active[319]),complete_glyph_ink=ink,confirmation=sample,cancelled=quit_frames[6200],
            trace=quit,source_caller=0x0203FC08),
        actual_race_scope=dict(actual_saved_game=True,original_ordinary_donor_save=True,help_pages=9,
            load_question=race_frames[11000],host_wait=race_frames[11800],title_return=race_frames[12190],
            race_started=False,hardware=False,COMMON_requests=race),
        legacy318=dict(Japanese=src.text.decode("cp932"),English=current_text.text.decode("cp932"),
            source_reference=reference(src),current_reference=reference(current_text),
            clean_hex=src.text.hex(),current_hex=current_text.text.hex(),
            rejected_numeric_lead=native_graphics_index(clean,arm),other_possible_callers_pending=True),
        evidence=evidence,new_dialogue_credit=0,full_goal_complete=False))
    print("All nine actual rule pages and the ordinary 319 confirmation pass. The 318 graphic index is ruled out; the stopping-page revision is staged for preview.")


if __name__ == "__main__":
    main()

