"""Correct the single full-width letter in the original name/word confirmation."""

from dataclasses import replace
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET,TABLE_OFFSET,common_message_entries
from scripts import register_tavern_toast_and_gift_20261114 as parent
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_release_baseline import files

base=parent.base
ROOT=Path("work/name_or_words_confirmation_20261114_v1")
ROM=ROOT/"Name_or_Words_Confirmation_RESEARCH_ONLY.nds"
STORED=ROOT/"staged.json"
ARM,COMMON,CLEAN,GATES=parent.stage.ARM,parent.stage.COMMON,parent.stage.CLEAN,parent.stage.GATES
DRAFT="Is %s all right?"
ID=296


def main():
    assert not ROOT.exists()
    previous=base.load(parent.RELEASE)
    assert base.digest(parent.ROM)==previous["candidate_sha256"]
    assert base.digest(CLEAN)==previous["clean_input_sha256"]
    image,clean=map(base.NdsImage.open,(parent.ROM,CLEAN))
    old=files(image)
    arm,common=old[ARM],old[COMMON]
    digest=parent.parent.parent.source.current.assets.edit.digest
    assert digest(arm)==previous["target_ARM9_sha256"] and digest(common)==previous["target_COMMON_sha256"]
    directory=digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    polished=owned_entries(common,arm,directory)
    japanese=common_message_entries(clean.read_file(COMMON),clean.read_file(ARM))
    current,source=polished[ID],japanese[ID]
    assert current.text==b"\x82hs %s all right?" and source.text.decode("cp932")=="%sでよろしいですか？"
    body=DRAFT.encode("ascii")
    assert body.count(b"%s")==current.text.count(b"%s")==source.text.count(b"%s")==1
    lo,hi=current.block_offset,current.copy_end
    blocks=list(IlnkContainer.parse(common).blocks)
    before=blocks[current.block][lo:hi]
    assert (current.block,lo,hi)==(4,2601,2619) and before==current.text+b"\0"
    after=body.ljust(len(before),b"\0")
    blocks[current.block]=blocks[current.block][:lo]+after+blocks[current.block][hi:]
    changed=IlnkContainer(blocks).to_bytes()
    running=owned_entries(changed,arm,directory)
    for a,b in zip(polished,running,strict=True):
        index=a.record_index+(len(before)-len(body)-1 if a.block==4 and a.block_offset>=hi else 0)
        expected=replace(a,record_index=index,text=body,end=len(body)) if a.message_id==ID else replace(a,record_index=index)
        assert b==expected
    assert IlnkContainer.parse(changed).blocks==blocks
    blocks[current.block]=blocks[current.block][:lo]+before+blocks[current.block][hi:]
    assert IlnkContainer(blocks).to_bytes()==common
    image.replace_file(COMMON,changed)
    revised=files(image)
    assert revised.keys()==old.keys() and {p for p in revised if revised[p]!=old[p]}=={COMMON}
    ROOT.mkdir()
    image.save(ROM)
    image.replace_file(COMMON,common)
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    row=dict(id="COMMON_MESSAGE_296",message_id=ID,english=DRAFT,speaker="System confirmation",
        source_meaning="The game asks whether the exact entry the player submitted is acceptable.",
        context="The same Yes/No prompt confirms the string entered in the Ship Name or Promised Words keyboard. Yes accepts the entered text. No returns to entry.",
        localization_note="Retain the complete generic wording because it suits both the ship name and the password. Use the regular ASCII capital I and preserve the single verbatim text argument.",
        decision="glyph revision with prose retained",review=dict.fromkeys(GATES,True)|{"formatting":False},
        Japanese=source.text.decode("cp932"),current_English=current.text.decode("cp932"),
        source_reference=reference(source),current_reference=reference(current),staged_reference=reference(running[ID]),
        exact_clean_hex=source.text.hex(),exact_current_hex=current.text.hex(),staged_hex=body.hex(),
        argument_order=["exact_entered_ship_name_or_promised_words"])
    base.save(STORED,dict(records=[row],candidate_sha256=base.digest(ROM),previous_sha256=previous["candidate_sha256"],
        clean_sha256=previous["clean_input_sha256"],target_COMMON_sha256=digest(changed),
        target_ARM9_sha256=digest(arm),byte_allocation=dict(block=4,start=lo,end=hi,before=before.hex(),after=after.hex()),
        preserved_entries=3667,preserved_blocks=40,whole_parent_inverse=True))
    print("COMMON 296 is staged in its original 18 bytes. Only its leading I uses a different glyph.")


if __name__=="__main__":
    main()
