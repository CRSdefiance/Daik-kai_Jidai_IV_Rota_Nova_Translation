"""Stage the three canonical room-name corrections in their current text owners."""

from inspect import getsource
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.crew_equipment_item_cards_v1 import compile_item
from dk4tool.patch.reviewed_item_cards import BASE, POOL, STAGE, item_table
from scripts import register_maria_tutorial_followup_20261122 as parent
from scripts import stage_square_country_briefings_20261115 as common
from scripts.physical_fatigue_layout_v960 import compiled as fatigue
from scripts.source_locked_derivation_v5118 import checked_text


base,native=parent.base,parent.native
ARM,COMMON=common.ARM,common.COMMON
INTAKE=Path("work/analysis/ship_room_terms_20261122/next_terminology_decisions.json")
ROOT=INTAKE.parent/"staged"
ROM,PROOF,MANUSCRIPT=[ROOT/name for name in ("Ship_Room_Terms_STAGED.nds","stored_proof.json","manuscript.json")]
IDS=(1784,2919,2920)
SOURCE_MEANING={
    1784:"The tired speaker says she is worn out and trails off about going to the lounge.",
    2919:"A small mask designed to block foul smells from the animal-keeping room. Each mask is made carefully by hand.",
    2920:"Stylish rubber boots made with a great deal of precious rubber because feet inevitably get dirty in the animal-keeping room.",
}
CONTEXT={
    1784:"Cristina's independent Deck response when the original selector finds physical fatigue.",
    2919:"The mask's catalogue description appears in both item views. The room name is the same as the one on the crew assignment menu.",
    2920:"The boots' catalogue description appears in both item views. The Nursery explains why they are useful aboard ship.",
}


def qualified_item_table(arm):
    sections=MainCodeFile(arm,BASE).sections
    assert len(sections)==7 and sections[6].ramAddress==0x1FFB860
    script=checked_text(getsource(item_table),{
        "assert len(sections) == 6 and sections[3].ramAddress == STAGE":
            "assert len(sections) == 7 and sections[3].ramAddress == STAGE",
    })
    scope=item_table.__globals__.copy()
    exec(compile(script,__file__+"::current-item-sections","exec"),scope)
    return scope["item_table"](arm)


def make_projections(arm, proposals):
    code=MainCodeFile(arm,BASE)
    assert bytes(code.save())==arm
    payload,table,pointers=qualified_item_table(arm)
    section=code.sections[3]
    original=bytes(section.data)
    assert section.ramAddress==STAGE and original[:-48]==payload
    edited=bytearray(original)
    edits=[]
    for number in IDS[1:]:
        row=proposals[number]
        item=row["projected_item_index"]
        assert item==number-2815 and row["description_table_address"]==table
        pointer=pointers[item]
        assert pointer==row["description_pointer"]
        assert pointers.count(pointer)==1
        current=bytes.fromhex(row["projected_before_hex"])
        lines,renewed=compile_item(row["new_English"])
        assert lines==row["proposed_lines"] and renewed.hex()==row["proposed_projection_hex"]
        start=pointer-POOL
        limit=start+len(current)
        assert 0<=start<limit<len(payload)
        assert current==original[start:limit] and current.endswith(b"\0\0") and len(renewed)<len(current)
        after=renewed.ljust(len(current),b"\0")
        edited[start:limit]=after
        edits.append(dict(message_ID=number,item_ID=item,pointer=pointer,offset=start,before=current.hex(),after=after.hex(),
            compiled_rows=lines,compiled_hex=renewed.hex()))
    section.data=bytearray(edited)
    target=bytes(code.save())
    assert len(target)==len(arm)
    inverse=MainCodeFile(target,BASE)
    assert bytes(inverse.save())==target
    for row in edits:
        start=row["offset"]
        before,after=map(bytes.fromhex,(row["before"],row["after"]))
        assert bytes(inverse.sections[3].data[start:start+len(after)])==after
        inverse.sections[3].data[start:start+len(before)]=before
    assert bytes(inverse.save())==arm
    check,after_table,after_pointers=qualified_item_table(target)
    assert (after_table,after_pointers)==(table,pointers) and len(payload)==len(check)==123264
    assert all(bytes(a.data)==bytes(b.data) for i,(a,b) in enumerate(zip(code.sections,inverse.sections,strict=True)) if i!=3)
    return target,edits


def main():
    assert not ROOT.exists()
    intake,release=map(base.load,(INTAKE,parent.RELEASE))
    assert intake["candidate_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    assert release["registry_sha256"]==base.digest(base.REGISTRY)
    assert release["clean_input_sha256"]==base.digest(native.CLEAN)
    clean,target=map(base.NdsImage.open,(native.CLEAN,parent.ROM))
    original=native.files(target)
    arm,shared=original[ARM],original[COMMON]
    assert native.digest(arm)==release["target_ARM9_sha256"] and native.digest(shared)==release["target_COMMON_sha256"]
    for name,offsets in intake["installed_arm9_ui_label_locations"].items():
        for offset in offsets:
            assert arm[offset:offset+len(name)+1]==name.encode("ascii")+b"\0"
    lookup=common.owned_entries(shared,arm,native.digest(arm[common.DIRECTORY_OFFSET:common.TABLE_OFFSET]))
    japanese=common.common_message_entries(clean.read_file(COMMON),clean.read_file(ARM))
    proposals={row["message_ID"]:row for row in intake["records"]}
    assert tuple(proposals)==IDS
    assert intake["storage_deployment_pending"] and intake["native_draw_and_gameplay_pending"]
    target_arm,private=make_projections(arm,proposals)
    assert target_arm[common.DIRECTORY_OFFSET:common.TABLE_OFFSET]==arm[common.DIRECTORY_OFFSET:common.TABLE_OFFSET]
    repl={n:row["new_English"].encode("ascii") for n,row in proposals.items()}
    repl[1784]=fatigue({"english":proposals[1784]["new_English"]})
    assert repl[1784].hex()==proposals[1784]["proposed_hex"]
    target_common,rebound,slots=common.owned_deployment(shared,target_arm,lookup,repl)
    rows=[]
    for n in IDS:
        p=proposals[n]
        src,cur=japanese[n],lookup[n]
        assert src.text.hex()==p["source_ref"]["source_hex"] and src.text.decode("cp932")==p["original"]
        assert cur.text.hex()==p["installed_hex"] and rebound[n].text==repl[n]
        assert cur.block==p["block"] and cur.block_offset==p["offset"]
        assert b'%' not in src.text and b'%' not in repl[n]
        rows.append(dict(id=f"COMMON_MESSAGE_{n}",message_ID=n,file_path=COMMON,speaker="Cristina" if n==1784 else "Item catalogue",
            clean_Japanese=p["original"],source_meaning=SOURCE_MEANING[n],context=CONTEXT[n],
            localization_note=p["localization_note"],english=p["new_English"],previous_English=" ".join(p["body"].split()),
            decision="revision",change_class="terminology",source_reference=common.reference(src),
            current_reference=common.reference(cur),source_hex=src.text.hex(),current_hex=cur.text.hex(),
            installed_reference=common.reference(rebound[n]),installed_hex=repl[n].hex(),
            expected_lines=p["proposed_lines"],review=dict.fromkeys(common.GATES,True)|{"formatting":False}))
    assert [old.message_id for old,new in zip(lookup,rebound,strict=True) if old.text!=new.text]==list(IDS)
    target.replace_file(ARM,target_arm)
    target.replace_file(COMMON,target_common)
    final=native.files(target)
    assert {p for p in original if original[p]!=final[p]}=={ARM,COMMON}
    result=bytes(target.rom.save())
    for name in (ARM,COMMON):
        target.replace_file(name,original[name])
    assert bytes(target.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(result)
    base.save(MANUSCRIPT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        review_gates=list(common.GATES),candidate_sha256=base.digest(ROM),parent=release["candidate_sha256"],
        source_preflight=str(INTAKE),source_preflight_sha256=base.digest(INTAKE),records=rows,new_editorial_credit=0))
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),predecessor_sha256=release["candidate_sha256"],
        whole_parent_inverse=True,stored_components={ARM:native.digest(target_arm),COMMON:native.digest(target_common)},
        manuscript_sha256=base.digest(MANUSCRIPT),common_fixed_slots=slots,private_item_allocations=private,
        copied_payload_bytes=123264,item_pointers_exact=True,preserved_COMMON_entries=len(lookup)-len(IDS)))
    print("Staged the three shared records and verified both private item paragraphs, unchanged pointers, and the whole-ROM inverse.")


if __name__=="__main__":
    main()

