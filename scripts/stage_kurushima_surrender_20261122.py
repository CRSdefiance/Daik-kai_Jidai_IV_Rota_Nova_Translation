"""Repair the speaker of the surrender clause in Maria's Kurushima exchange."""

from argparse import ArgumentParser
from inspect import getsource
import sys
from types import FunctionType

from dk4tool.patch.xdelta import apply_xdelta,make_xdelta
from scripts import observe_osaka_town_20261122 as voyage
from scripts import register_rafael_deck_tutorial_followup_20261122 as parent
from scripts import stage_rafael_deck_tutorial_followup_20261122 as earlier
from scripts import stage_london_guild_assignments_20261118 as compiler
from scripts import verify_london_guild_assignments_20261118 as renderer
from scripts.source_locked_derivation_v5118 import checked_text


base,native=parent.base,parent.native
ROOT=voyage.ROOT/"kurushima_staged"
ROM=ROOT/"Maria_Kurushima_Surrender_STAGED.nds"
PROOF,MANUSCRIPT=ROOT/"stored_proof.json",ROOT/"manuscript.json"
PATCH, REBUILT = ROOT/"translation.xdelta",ROOT/"clean_rebuilt.nds"
STARTUP_CAPTURE=ROOT/"startup/capture/capture_report.json"
ARCHIVE="/data/SC3.DK4"
BLOCK=3
ID="DK4_MES_B3_R0032"
TARGET="Heh heh, FI! Agree to be mine and I'll let you surrender without a fight. Yours is the only life I'll spare!"
FRAMES=(8550,9020,9230,9520,9820,10120,10420,10720,11020,11320,11620,11850)
PREVIOUS="releases/all_routes_editorial_20261122_maria_opening_hodram_wraps_candidate/verification/registered_review.json"
NOTES=(
    ("Kurushima taunts Maria by name and demands a decisive fight today.",
     "The taunt and declaration open the confrontation. Keep the original given-name token."),
    ("Yukihisa calls out to Kurushima and tells him to stop his foolish conduct.",
     "The blunt rebuke sounds right as Yukihisa interrupts his challenge."),
    ("Kurushima accuses a fellow samurai of siding with foreigners and disgracing his class.",
     "Keep the contemptuous question and accusation in Kurushima's voice."),
    ("Yukihisa challenges Kurushima to justify raiding the mainland coast and robbing defenseless people as a proud samurai.",
     "The direct charges and rhetorical question answer Kurushima's appeal to samurai honor."),
    ("Kurushima mocks Yukihisa's stiff manner and says that is the kind of person he hates.",
     "The mocking aside shifts from talking about honor to insulting Yukihisa personally."),
    ("Kurushima says Maria can surrender without resisting if she agrees to be his woman. He will spare only her.",
     "The offer is permission for Maria to surrender on his terms. Correct the English subject while retaining the threat, coercion, and native given-name substitution."),
    ("Maria says she will pluck Kurushima's imposing beard if he keeps talking nonsense.",
     "The insulting threat ridicules his pretension and rejects his offer in Maria's voice."),
    ("Kurushima laughs, pauses, then threatens to kill her.",
     "The bitter turn from laughter to an explicit threat closes the exchange."),
)
CONTEXT="Kurushima confronts Maria's fleet. Yukihisa speaks up, Kurushima tries to intimidate Maria, and she answers him with ridicule before he threatens her." 


def stage():
    assert not ROOT.exists()
    previous=base.load(parent.RELEASE)
    candidate=base.digest(parent.ROM)
    assert candidate==previous["candidate_sha256"] and base.digest(base.REGISTRY)==previous["registry_sha256"]
    assert base.digest(parent.MANIFEST)==previous["manifest_sha256"]
    assert base.digest(native.CLEAN)==previous["clean_input_sha256"]
    source,image=map(base.NdsImage.open,(native.CLEAN,parent.ROM))
    before=native.files(image)
    arm,clean_arm=before[native.ARM],source.read_file(native.ARM)
    assert native.digest(arm)==previous["target_ARM9_sha256"]
    jp=native.IlnkContainer.parse(source.read_file(ARCHIVE)).blocks[BLOCK]
    bank=native.IlnkContainer.parse(before[ARCHIVE])
    en=bank.blocks[BLOCK]
    prior=[r for r in base.load(PREVIOUS)["records"] if r["block"]==BLOCK and r["file_path"]==ARCHIVE]
    inv,_,_=native.scoped_inventory()
    clean,current=[native.references(*native.raw_speeches(a,b,inv)) for a,b in ((clean_arm,jp),(arm,en))]
    assert len(clean)==len(current)==len(prior)==len(NOTES)==8
    rows=[]
    for j,e,past,(meaning,note) in zip(clean,current,prior,NOTES,strict=True):
        assert j["raw_hex"]==past["source_hex"] and e["raw_hex"]==past["registered_reference"]["exact_stored_hex"]
        selector=j["selector"]
        assert selector==e["selector"]==past["source_selector"]
        assert j["complete_preamble_hex"]==e["complete_preamble_hex"]
        ja=bytes.fromhex(j["raw_hex"])[1:].decode("cp932")
        old=" ".join(bytes.fromhex(e["raw_hex"])[1:].decode("ascii").split())
        assert old==past["english"] and all(past["review"].values())
        changed=past["id"]==ID
        english=TARGET if changed else old
        if changed:
            assert "I'll let you surrender" in english and "I might surrender" in old
            assert "俺の女になるなら" in ja and "おとなしく降参" in ja
        assert compiler.review.TOKEN.findall(ja)==compiler.review.TOKEN.findall(old)==compiler.review.TOKEN.findall(english)
        rows.append(dict(id=past["id"],file_path=ARCHIVE,block=BLOCK,route=3,source_selector=selector,
            kind="progressive",native_command_word=0x4000,speaker=past["speaker"],context=CONTEXT,
            Japanese=ja,source_meaning=meaning,english=english,previous_English=old,localization_note=note,
            source_hex=j["raw_hex"],current_hex=e["raw_hex"],source_reference=j,current_reference=e,
            protected_phrases=["surrender without a fight.","Yours is the only life I'll spare!"] if changed else [],
            decision="revision" if changed else "retention",
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    updated,commands,plans=compiler.rebuild_function()(rows,jp,en,inv,clean_arm,arm,None)
    assert set(plans)=={ID} and plans[ID]["expected_native_pages"]==1
    changed=[c for c in commands if c["record_ids"] and c["stored"]!=c["current"]]
    edited,=changed
    assert edited["record_ids"]==[ID] and updated!=en
    bank.blocks[BLOCK]=updated
    packed=bank.to_bytes()
    actual=native.IlnkContainer.parse(packed)
    bank.blocks[BLOCK]=en
    assert bank.to_bytes()==before[ARCHIVE]
    assert [i for i,(a,b) in enumerate(zip(bank.blocks,actual.blocks,strict=True)) if a!=b]==[BLOCK]
    image.replace_file(ARCHIVE,packed)
    after=native.files(image)
    assert {p for p in before if before[p]!=after[p]}=={ARCHIVE} and before.keys()==after.keys()
    data=bytes(image.rom.save())
    image.replace_file(ARCHIVE,before[ARCHIVE])
    assert bytes(image.rom.save())==parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(data)
    base.save(MANUSCRIPT,dict(translation_policy="natural-dialogue-v2",encoder="dialogue-relocatable-v1",
        target_locale="en-US",review_gates=["source","context","localization","naturalness","formatting"],records=rows,
        previous_sha256=candidate,previous_registry_sha256=previous["registry_sha256"],
        earlier_decisions=PREVIOUS,earlier_decisions_sha256=base.digest(PREVIOUS),new_contextual_records=0))
    base.save(PROOF,dict(candidate_sha256=base.digest(ROM),predecessor_sha256=candidate,
        source_block_sha256=native.digest(jp),previous_block_sha256=native.digest(en),
        compiled_block_sha256=native.digest(updated),compiled_archive_sha256=native.digest(packed),
        whole_parent_inverse=True,commands=commands,plans=plans,manuscript_sha256=base.digest(MANUSCRIPT)))
    print("Restored the surrender subject, preserving the complete original encounter commands.",flush=True)


def patch():
    FunctionType(earlier.patch.__code__,earlier.patch.__globals__|globals())()


def startup():
    FunctionType(earlier.startup.__code__,earlier.startup.__globals__|globals())()


def replay():
    baseline=voyage.ROOT/"capture/capture_report.json"
    report=base.load(baseline)
    assert report["ROM_sha256"]==base.digest(parent.ROM) and not report["callback_errors"]
    assert report["cold_boot"] and not report["savestate_loaded"]
    assert not any(v for k,v in report.items() if k.startswith("synthetic_"))
    donor=report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"])==donor["source_sha256"]
    out=ROOT/"gameplay"
    out.mkdir()
    inputs=out/"inputs.json"
    base.save(inputs,[r for r in report["scripted_input_schedule"] if r["start"]<=11801])
    before_argv=sys.argv
    try:
        sys.argv=["headless_desmume_v193.py","--rom",str(ROM),"--out",str(out/"capture"),
            "--frames","11851","--inputs-json",str(inputs),"--press-start","-1","--touchscreen",
            "--battery-save",donor["source"],"--capture-every","999999","--capture-at",*map(str,FRAMES)]
        voyage.harness.main()
    finally:
        sys.argv=before_argv
    assert base.digest(donor["source"])==donor["source_sha256"]


if __name__=="__main__":
    parser=ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("stage","patch","startup","replay"))
    globals()[parser.parse_args().action]()

