"""Stage the Istanbul barkeep's reviewed influence rumor in its existing slot."""

from dataclasses import replace
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_about_extras_20261114 as parent
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_release_baseline import files

base = parent.base
ROOT = Path("work/tavern_influence_20261114_v1")
ROM = ROOT / "Tavern_Influence_RESEARCH_ONLY.nds"
STORED = ROOT / "staged.json"
DRAFT = "%s from %s is a %s with real pull here."
ARM, COMMON = "/__arm9__.bin", "/COMMON/MESFILE.DK4"
CLEAN = parent.parent.parent.stage.CLEAN
GATES = ("source", "context", "localization", "naturalness", "formatting")


def stage():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    rom, clean = map(base.NdsImage.open, (parent.ROM, CLEAN))
    original = files(rom)
    before = original[COMMON]
    arm = original[ARM]
    digest = parent.source.current.assets.edit.digest
    directory = digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    assert digest(arm) == release["target_ARM9_sha256"] and digest(before) == release["target_COMMON_sha256"]
    ja = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    active = owned_entries(before, arm, directory)
    target, source = active[821], ja[821]
    assert target.text == b" %s of %s is an influential %s around here."
    assert source.text.decode("cp932") == "この辺じゃ\n%sっていう\n%sの%sが\n幅を利かせてるぜ"
    english = DRAFT
    raw = b" " + english.encode("ascii")
    assert raw.count(b"%s") == source.text.count(b"%s") == 3
    assert b"\n" not in raw and raw[0] == target.text[0] == 32
    row = dict(id="COMMON_MESSAGE_821", message_id=821, speaker="Barkeep", english=english+"{PAD}",
        source_meaning="The named person from the named town wields influence in this area in their profession.",
        context="The barkeep gives local gossip after the player orders a drink. This casual influence report is an alternative to the formal reputation line, a nearby-town tip or no news. The order of arguments is person, town, role.",
        localization_note="Use the barkeep's conversational 'real pull' to express his appraisal of the person's local influence. The port association and native role keep their source slots.",
        review=dict.fromkeys(GATES, True) | {"formatting":False},
        source_reference=reference(source), current_reference=reference(target),
        Japanese=source.text.decode("cp932"), current_English=target.text.decode("ascii"),
        argument_order=["person_full_name", "town_name", "localized_force_profession"],
        exact_clean_hex=source.text.hex(), exact_current_hex=target.text.hex())
    container = IlnkContainer.parse(before)
    rows = list(container.blocks)
    assert target.block == 10
    lo,hi = target.block_offset,target.copy_end
    old = rows[target.block][lo:hi]
    assert old == target.text+b"\0" and len(raw)+1 <= len(old)
    replacement = raw.ljust(len(old), b"\0")
    rows[target.block] = rows[target.block][:lo]+replacement+rows[target.block][hi:]
    deployed = IlnkContainer(rows).to_bytes()
    after = owned_entries(deployed, arm, directory)
    assert after[821].text == raw and reference(after[821])["copy_end"] == hi
    padding = len(old)-len(raw)-1
    for a,b in zip(active,after,strict=True):
        if a.message_id != 821:
            # The parser counts NUL-separated fields. Extra terminators inside
            # this slot shift its diagnostic ordinals only.
            index = a.record_index + (padding if a.block == target.block and a.block_offset >= hi else 0)
            assert replace(a, record_index=index) == b
    row["staged_reference"] = reference(after[821])
    row["staged_hex"] = raw.hex()
    assert IlnkContainer.parse(deployed).blocks == rows
    inverse = list(rows)
    inverse[target.block] = inverse[target.block][:lo]+old+inverse[target.block][hi:]
    assert IlnkContainer(inverse).to_bytes() == before
    rom.replace_file(COMMON, deployed)
    reconstructed = files(rom)
    assert original.keys() == reconstructed.keys()
    assert {path for path in original if original[path] != reconstructed[path]} == {COMMON}
    ROOT.mkdir()
    rom.save(ROM)
    rom.replace_file(COMMON, before)
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    base.save(STORED, dict(translation_policy="natural-dialogue-v2",target_locale="en-US",
        encoder="dialogue-relocatable-v1",candidate_sha256=base.digest(ROM),
        previous_sha256=release["candidate_sha256"],target_COMMON_sha256=digest(deployed),
        target_ARM9_sha256=digest(arm), records=[row], native_control=raw[0],
        byte_allocation=dict(block=target.block,start=lo,end=hi,before=old.hex(),after=replacement.hex()),
        preserved_entries=len(active)-1,preserved_blocks=len(rows)-1, whole_parent_inverse=True))
    print(f"Staged COMMON 821 in {len(old)} bytes, with all other entries and ARM9 exact.")


if __name__ == "__main__":
    stage()
