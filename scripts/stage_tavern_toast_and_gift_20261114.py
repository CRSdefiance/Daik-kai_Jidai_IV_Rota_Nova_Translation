"""Stage the toast and Hodram’s item identification reply in COMMON."""

from dataclasses import replace
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_tavern_influence_20261114 as parent
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_release_baseline import files

base = parent.base
ROOT = Path("work/tavern_toast_and_gift_20261114_v2")
ROM = ROOT/"Tavern_Toast_and_Gift_RESEARCH_ONLY.nds"
STORED = ROOT/"staged.json"
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
REVISIONS = {
    827: ("Ah, %s? Here's to meeting you!", "Faticia", "Hmm... %s, right? Here's to our new friendship!",
        "The barmaid confirms the captain's name and raises a toast to getting acquainted.",
        "The toast follows the paid follow-up drink. The barmaid answers the introduction by repeating the name with a questioning inflection.",
        "Keep the name check and the warm invitation to toast the meeting. The Japanese establishes a new acquaintance."),
    831: ("It's called %s.", "Hodram", "This? It's called %s.",
        "Hodram echoes the barmaid's question and identifies the object directly by its name.",
        "The barmaid notices a present. Hodram names it directly. She admires it, and he asks whether she likes it before her request.",
        "Hodram answers plainly and briefly. The previous repeat question works in the more conversational variants. Hodram answers immediately here. 'It's called' is grammatical for both named treasures and ordinary item labels."),

}


def main():
    assert not ROOT.exists()
    released = base.load(parent.RELEASE)
    assert base.digest(parent.ROM)==released["candidate_sha256"] and base.digest(CLEAN)==released["clean_input_sha256"]
    rom,clean = map(base.NdsImage.open,(parent.ROM,CLEAN))
    before = files(rom)
    common,arm = before[COMMON],before[ARM]
    digest = parent.parent.source.current.assets.edit.digest
    assert digest(common)==released["target_COMMON_sha256"] and digest(arm)==released["target_ARM9_sha256"]
    directory = digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    current = owned_entries(common,arm,directory)
    source = common_message_entries(clean.read_file(COMMON),clean.read_file(ARM))
    old_blocks = IlnkContainer.parse(common).blocks
    blocks = list(old_blocks)
    staged, payloads, proof = [], {}, []
    for number,(english,speaker,old,meaning,context,note) in REVISIONS.items():
        native,ja = current[number],source[number]
        raw = b" "+english.encode("ascii")
        assert native.text == b" "+old.encode("ascii")
        assert raw.count(b"%s")==native.text.count(b"%s")==ja.text.count(b"%s")==1
        assert b"\n" not in raw and native.block == 10
        lo,hi = native.block_offset,native.copy_end
        original = blocks[native.block][lo:hi]
        assert original==native.text+b"\0" and len(raw)+1<=len(original)
        replacement = raw.ljust(len(original),b"\0")
        blocks[native.block] = blocks[native.block][:lo]+replacement+blocks[native.block][hi:]
        payloads[number]=raw
        proof.append(dict(block=native.block,start=lo,end=hi,before=original.hex(),after=replacement.hex(),
                          extra_terminators=len(original)-len(raw)-1))
        staged.append(dict(id=f"COMMON_MESSAGE_{number}",message_id=number,speaker=speaker,english=english,
            source_meaning=meaning,context=context,localization_note=note,decision="revision",
            review=dict.fromkeys(GATES,True)|{"formatting":False},
            source_reference=reference(ja),current_reference=reference(native),Japanese=ja.text.decode("cp932"),
            current_English=old,exact_clean_hex=ja.text.hex(),exact_current_hex=native.text.hex(),
            argument_order=["admiral_short_name" if number==827 else "item_name"],staged_hex=raw.hex()))
    deployed = IlnkContainer(blocks).to_bytes()
    after = owned_entries(deployed,arm,directory)
    for a,b in zip(current,after,strict=True):
        extra = sum(row["extra_terminators"] for row in proof if a.block==row["block"] and a.block_offset>=row["end"])
        text = payloads.get(a.message_id,a.text)
        assert replace(a,record_index=a.record_index+extra,text=text,end=a.start+len(text)) == b
    for row in staged:
        row["staged_reference"] = reference(after[row["message_id"]])
    assert {i for i,(a,b) in enumerate(zip(old_blocks,blocks,strict=True)) if a!=b}=={10}
    inverse = list(blocks)
    for a in proof:
        i,lo,hi = a["block"],a["start"],a["end"]
        inverse[i] = inverse[i][:lo]+bytes.fromhex(a["before"])+inverse[i][hi:]
    assert IlnkContainer(inverse).to_bytes()==common
    rom.replace_file(COMMON,deployed)
    target = files(rom)
    assert before.keys()==target.keys() and {p for p in target if before[p]!=target[p]}=={COMMON}
    ROOT.mkdir()
    rom.save(ROM)
    rom.replace_file(COMMON,common)
    assert bytes(rom.rom.save())==parent.ROM.read_bytes()
    base.save(STORED,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",
        encoder="dialogue-relocatable-v1",candidate_sha256=base.digest(ROM),previous_sha256=released["candidate_sha256"],
        target_COMMON_sha256=digest(deployed),target_ARM9_sha256=digest(arm),clean_sha256=released["clean_input_sha256"],
        records=staged,byte_allocation=proof,preserved_entries=len(current)-len(REVISIONS),preserved_blocks=40,
        whole_parent_inverse=True))
    print("Staged the toast and Hodram’s item reply in their original allocations.")


if __name__=="__main__":
    main()
