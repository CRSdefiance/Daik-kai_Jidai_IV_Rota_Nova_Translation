"""Review specific reading defects in Maria's ship-buying, coin and refit exchanges."""

from inspect import getsource

from scripts import reconcile_maria_later_release_decisions_20261122 as earlier
from scripts import register_maria_B51_B70_20261122 as parent
from scripts import review_maria_opening_hodram_wraps_20261122 as pairing
from scripts.source_locked_derivation_v5118 import checked_text


base,native=parent.base,parent.native
ROOT=earlier.ROOT/"tutorial_and_coin_followup"
PACKET,DRAFT,PLANS=(ROOT/name for name in ("source_current.json","manuscript_replay_scope.json","preflight_replay_scope.json"))
BLOCKS=(135,136,138)
DECISIONS={
    "DK4_MES_B135_R0325":("You can add towns to your trade routes without buying ships. A one percent share lets you buy just one to five units of goods.",
        ("trade routes","one percent share","one to five units of goods."),
        "Cesare explains that opening up trade through more towns takes no new ship purchases yet. The one percent share and one-to-five-unit limit follow as a complete example."),
    "DK4_MES_B135_R0332":("Check the size and price first.",(),
        "Cesare has just said when to buy a ship. His next instruction names the two things to check first in one complete line."),
    "DK4_MES_B135_R0348":("Medium ships have 2 or 3 masts. Three make the ship faster, but you'll need more sail handlers.",
        ("2 or 3 masts.","more sail handlers."),
        "Lead with the two rig options on a complete line. Keep the higher speed and additional sail handlers attached to the three-mast option."),
    "DK4_MES_B136_R0143":("Sure. With an eye like mine, I can read my opponent's next move.",
        ("With an eye like mine,","my opponent's next move."),
        "Fernando boasts about his own ability to read a move, following the exact clues he noticed. Keep his confidence before he credits his luck."),
    "DK4_MES_B138_R0113":("At sea, shipwrights like me can repair damage in the Lumber Room. At the shipyard, we help with refits and repairs.",
        ("in the Lumber Room.","refits and repairs."),
        "Manuel identifies the Lumber Room as the work location for repairs at sea. His next sentence gives the work a shipwright can do at a shipyard."),
    "DK4_MES_B138_R0125":("I see. I'll leave it to you, then.",(),
        "Keep Manuel's courteous response when Maria declines the explanation. The complete phrase stays on one line."),
}
RETAINED={
    "DK4_MES_B135_R0328":"Keep the trigger for buying a ship tied to how much traders can buy as their share grows.",
    "DK4_MES_B135_R0335":"The budget and market share both matter. The example shows why a ship too large to fill still costs sailors.",
    "DK4_MES_B136_R0139":"Maria's surprise acknowledges the details Fernando caught and sets up his boast about reading people.",
    "DK4_MES_B136_R0146":"Fernando gives luck the last word after explaining the skill he uses to read an opponent.",
    "DK4_MES_B138_R0116":"Manuel acknowledges his quick explanation and checks whether Maria found it useful.",
    "DK4_MES_B138_R0119":"Manuel closes the advice by putting responsibility for the fleet and careful refits in the admiral's hands.",
}


def main():
    assert not DRAFT.exists() and not PLANS.exists()
    old=base.load(earlier.OUTPUT)
    release=base.load(parent.RELEASE)
    assert old["candidate_sha256"]==release["candidate_sha256"]==base.digest(parent.ROM)
    assert not old["pending"] and old["latest_total_exact"]==3839
    program=checked_text(getsource(pairing.maria_packet),{
        'return scope["source_and_current"](parent,range(18))':'return scope["source_and_current"](parent,BLOCKS)',
    })
    namespace=pairing.maria_packet.__globals__|{"parent":parent,"BLOCKS":BLOCKS}
    exec(compile(program,__file__+"::tutorial-pairing","exec"),namespace)
    packet=namespace["maria_packet"]()
    assert packet["candidate_sha256"]==old["candidate_sha256"]
    records,plans=[],{}
    documents={}
    matches={r["id"]:r for r in old["records"]}
    planner=parent.writer.engine.assemble({}).__globals__["plan_progressive"]
    for group in packet["groups"]:
        for pair in group["records"]:
            ident=pair["id"]
            if ident not in DECISIONS and ident not in RETAINED:
                continue
            previous=matches[ident]
            path=previous["prior_native_and_contextual_review"]
            if path not in documents:
                assert base.digest(path)==old["qualified_release_receipts"][path]["manuscript_hash"]
                documents[path]={r["id"]:r for r in base.load(path)["records"] if r.get("file_path")=="/data/SC3.DK4"}
            prior=documents[path][ident]
            source,current=[f'{pair["selector"]:02x}'+pair[f"{key}_reference"]["exact_body_hex"] for key in ("source","current")]
            assert source==previous["exact_previous_source_hex"] and current==previous["installed_body_hex"]
            assert pair["current_reference"]["command_offset"]==previous["installed_command_offset"]
            before=" ".join(pair["current_English"].split())
            revised=ident in DECISIONS
            if revised:
                english,protected,note=DECISIONS[ident]
                assert before!=english
            else:
                english,protected,note=before,(),RETAINED[ident]
            assert pair["native_command_word"]==0x4000
            row=pair|dict(route=3,kind="progressive",source_selector=pair["selector"],speaker=prior["speaker"],
                native_slots=[],source_hex=source,current_hex=current,previous_English=before,
                english=english,protected_phrases=list(protected),decision="revision" if revised else "retention",change_class="wording" if revised else "retention",
                source_meaning=prior["source_meaning"],context=prior["context"],localization_note=note,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
            if revised:
                _,plan=planner(row,pair["selector"],bytes.fromhex(current)[1:],bytes.fromhex(source)[1:])
                assert plan["expected_native_pages"]==1
                plans[ident]=plan
                print(ident,plan["lines"])
            records.append(row)
    assert plans.keys()==DECISIONS.keys()
    assert base.load(PACKET)==packet
    base.save(DRAFT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(PACKET),source_packet_sha256=base.digest(PACKET),exact_historical_review=str(earlier.OUTPUT),
        exact_historical_review_sha256=base.digest(earlier.OUTPUT),contextual_records_revisited=len(records),
        contextual_decisions_reused=3839-len(records),new_editorial_credit=0,records=records,findings={"wording":6,"retention":6},planned_FE={}))
    base.save(PLANS,dict(draft_sha256=base.digest(DRAFT),plans=plans))


if __name__=="__main__":
    main()

