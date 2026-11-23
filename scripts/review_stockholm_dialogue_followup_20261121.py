"""Review the complete Stockholm fur exchanges and recruitment tutorial."""
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_seville_stockholm_trends_20261121 as previous
from scripts import stage_story_short_phrase_wraps_20261119 as compiler
from scripts import verify_stockholm_december_20261121 as live
from scripts.review_company_name_dialogue_20261121 import GATES, logical
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = live.base, live.native, live.replay.active
ROOT = Path("work/stockholm_dialogue_followup_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = live.town.events.BOOK / "stockholm_dialogue_followup_20261121_v2.json"
STORY = Path("translations/hodram_B131_B150_contextual_final_review_v1.json")
BLOCKS = ((197,), (134,189), (185,), (158,))
CONTEXT = ("Stockholm Square and Tavern.",) * 4
SQUARE = "Two Stockholm townspeople agree that the cold is unusually sharp. She wishes for a fur coat, and he connects the cold to rising sales and prices. Her last line returns to the coat before the trade forecast."
TAVERN = "Hodram checks in with Gerhard after men were wounded. Gerhard asks for orders on recruiting. The player can hear how to recruit efficiently or let Gerhard handle it. The lesson balances boarding crew against cruising range."
TABLE = {
    "DK4_MES_B134_R0005": "Hodram's familiar greeting makes sense with an officer he knows well.",
    "DK4_MES_B134_R0009": "The address comes from the source. Gerhard connects the injuries to recruitment and asks for instructions.",
    "SC1_B134_CHOICE_134_0": "The brief assent accepts Gerhard's offer to explain recruiting.",
    "SC1_B134_CHOICE_134_1": "The player delegates recruitment to Gerhard.",
    "DK4_MES_B134_R0025": "Buying a round draws people looking for work and speeds up recruiting. The wording keeps the actions in order.",
    "DK4_MES_B134_R0033": "Gerhard's short acknowledgment fits the branch that delegates the job.",
}
REVISIONS = {
    "DK4_MES_B189_R0006": ("It's freezing. The cold goes right through you.", ("The cold goes right through you.",),
        "Use Rafael's reviewed wording for the same speaker and source line. The emphatic second sentence sounds spoken and leads into the reply.", "dialogue"),
    "DK4_MES_B189_R0013": (None, ("I wish I had a fur coat.","I'm going to freeze at this rate!"),
        "Keep the wish followed by the threat of freezing. Let each clause sit together and avoid breaking going to freeze.", "wrap"),
    "DK4_MES_B134_R0028": ("Relying on boarding battles? Hire plenty of sailors. Just remember, a larger crew reduces your fleet's cruising range.",
        ("boarding battles?","Hire plenty of sailors.","Just remember,","cruising range."),
        "Lead with the player's chosen tactic. Keep the crew advice and the drawback as separate thoughts, and keep both gameplay terms together.", "dialogue and wrap"),
}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__,vars(pairing)|globals())()
    packet, event, release = map(base.load,(SOURCE,live.OUTPUT,parent.RELEASE))
    assert packet["candidate_sha256"] == event["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    shelf = base.load(previous.REVIEW)["records"]
    story = [r for r in base.load(STORY)["records"] if r["block"]==134]
    prior_rows = {(r["file_path"],r["id"]):r for r in shelf+story}
    squ = {r["id"]:r["observed"] for r in event["complete_fur_exchange"]}
    tav = dict(zip(("DK4_MES_B134_R0005","DK4_MES_B134_R0009","SC1_B134_CHOICE_134_0",
                    "DK4_MES_B134_R0025","DK4_MES_B134_R0028"),event["separate_Tavern_tutorial_frames"]))
    tav["SC1_B134_CHOICE_134_1"] = tav["SC1_B134_CHOICE_134_0"]
    rom = base.NdsImage.open(parent.ROM)
    system = live.town.current_fe_painter(SimpleNamespace(image=rom,arm=rom.read_file(native.ARM)))
    fe = compiler.stage.plan_fe
    source = checked_text(getsource(fe),{"phrases(paragraph)":'tuple(row["protected_phrases"])'})
    scope = fe.__globals__.copy()
    exec(compile(source,__file__+"::FE","exec"),scope)

    results, plans = [], {}
    for group in packet["groups"]:
        path, block, route = (group[k] for k in ("file_path","block","route"))
        for row in group["records"]:
            selector = row["selector"]
            if selector is None:
                assert block==134
                ident = f"SC1_B134_CHOICE_134_{row['slots'][0]}"
            else:
                ident = f"DK4_MES_B{block}_R{row['source_record_index']:04}"
                assert not row["slots"]
            before = prior_rows[path,ident]
            assert before.get("Japanese",before.get("source_Japanese")) == row["Japanese"]
            jp, en = (bytes.fromhex(row[f"{side}_body_hex"]) for side in ("source","current"))
            prefix = b"" if selector is None else bytes([selector])
            assert before["source_hex"].lower() == (prefix+jp).hex()
            prior_english = logical(row["current_English"])
            assert prior_english == before["english"]
            original, phrases, note, finding = REVISIONS.get(ident,(None,(),
                TABLE.get(ident,before["localization_note"]),"retention"))
            english = prior_english if original is None else original
            refs = {s: dict(file_path=path,block=block,offset=row[f"{s}_offset"],
                command_offset=row[f"{s}_command_offset"],archive_sha256=group[f"{s}_archive_sha256"],
                block_sha256=group[f"{s}_block_sha256"],exact_hex=(prefix+b).hex())
                    for s,b in (("source",jp),("current",en))}
            updated = dict(id=ident,route=route,file_path=path,block=block,kind=before.get("kind","progressive"),
                source_selector=selector,native_command_word=row["native_command_word"],native_slots=row["slots"],
                source_reference=refs["source"],current_reference=refs["current"],source_hex=(prefix+jp).hex(),
                current_hex=(prefix+en).hex(),Japanese=row["Japanese"],english=english,previous_English=prior_english,
                source_meaning=before["source_meaning"],speaker=before["speaker"],context=TAVERN if block==134 else SQUARE,
                localization_note=note,protected_phrases=list(phrases),finding=finding,
                decision="revision" if ident in REVISIONS else "retention",
                previous_capture=(squ|tav).get(ident),review=dict.fromkeys(GATES,True)|{"formatting":ident not in REVISIONS})
            if ident in REVISIONS:
                if selector==254:
                    body, plan = scope["plan_fe"](updated,system)
                else:
                    body, plan = compiler.workflow.plan_progressive(updated,selector,en,jp)
                assert body.rstrip(b" ") != en.rstrip(b" ") and logical(body.decode("ascii")) == english
                assert plan["expected_native_pages"] == 1
                plans[f"{path}:{ident}"] = plan
            results.append(updated)
    assert len(results) == 39 and len(plans)==3
    base.save(OUTPUT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",review_gates=GATES,
        previous_sha256=packet["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE),source_packet_sha256=base.digest(SOURCE),
        decisions=dict(Counter(r["decision"] for r in results)),records=results,plans=plans,
        ordinary_gameplay_sha256=base.digest(live.OUTPUT),new_editorial_credit=0,
        status="Three revisions planned. Stored-Rom checks and changed-candidate visual verification pending."))
    for name,plan in plans.items():
        print(name,plan["lines"])


if __name__ == "__main__":
    main()
