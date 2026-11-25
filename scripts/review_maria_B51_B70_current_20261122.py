"""Review the changed Maria B51–70 records against the clean exchange and exact installed text."""

from collections import Counter
from pathlib import Path

from scripts import register_maria_hangzhou_followup_20261122 as parent


base, native = parent.base, parent.native
ROOT = Path("work/analysis/maria_B50_B70_current_20261122")
PACKET = ROOT / "B51_B70_source_current.json"
HISTORY = ROOT / "B51_B70_prior_decisions.json"
DRAFT = ROOT / "B51_B70_manuscript_v4.json"
PLANS = ROOT / "B51_B70_preflight_v4.json"

CLAIMS = {
    "summary": ("", (), "Maria counts the completed set aloud. The tentative pause leaves room for Xien to observe that nothing happens."),
    "relics": ("", ("Who knows if they're even genuine?",),
        "Maria questions authenticity after describing what each region revered. Keep the uncertainty on a complete line before she turns to the power of belief."),
    "agency": ("", (), "Ian respectfully agrees while putting responsibility on what they do as holders of the Proofs. His words lead directly into Xien's joke about postponing retirement."),
}
DECISIONS = {
    "B53_R0006": CLAIMS["summary"],
    "B53_R0069": CLAIMS["relics"],
    "B53_R0144": CLAIMS["agency"],
    "B54_R0012": CLAIMS["summary"],
    "B54_R0074": CLAIMS["relics"],
    "B54_R0150": CLAIMS["agency"],
    "B54_R0448": ("Oh! We're finally going out there in front of all those people! I-I'm getting awfully nervous!",
        ("all those people!","I-I'm getting awfully nervous!"), "Cesare realizes the wait is over and the whole group must face the crowd. Keep his alarm and nervous stammer before Maria's brisk order."),
    "B55_R0062": ("", (), "Angelo thinks he had been aboard a ship. His quiet decision to let the inconsistency go rests on Bianca being beside him. Keep the parentheses for his private thought."),
    "B55_R0152": ("", (), "Angelo pleads with Bianca and tries to dismiss the farewell as a cruel joke. The three short beats preserve his denial before the more desperate plea."),
    "B57_R0079": ("", (), "Mivor stumbles over his own name and overdoes the formal courtesy. His full name and enthusiastic introduction play against Cristina's lack of interest."),
    "B58_R0314": ("Oh, will you pipe down? Let's set sail already. He's driving me crazy!",
        ("set sail already.","He's driving me crazy!"), "Cristina snaps at the noisy Mivor, then urges the group to leave before he can keep at it. The change makes both addressees clear."),
    "B60_R0036": ("Yes. I like machinery. I'm good at handling ships. I can fix them, too.",
        ("I'm good at handling ships.","I can fix them, too."), "Janus answers Maria's general question with his interest in machinery and both specific skills he brings. He can handle ships and make repairs."),
    "B60_R0094": ("", (), "Richard rebukes Janus for presuming on the admiral's good will. The sharp spoken question carries his indignation without assigning a new rank."),
    "B61_R0063": ("Oh, it's you. I'm busy. Can we talk later? I've almost proved my theory...",
        ("Can we talk later?","I've almost proved my theory..."), "Charles recognizes his visitor without suggesting kinship and tries to put him off. His sudden enthusiasm about being close to proof explains the hurry."),
    "B61_R0087": ("", (), "Xien says Charles can be forgiven for doubting the offer before he knows who is making it. The familiar wording sets up the introduction of Maria."),
    "B61_R0094": ("Her accomplishments include... (list abridged) ...and I could go on all day! Well? Impressed?",
        ("(list abridged)","I could go on all day!"), "Xien starts listing Maria's achievements, the source cuts away from the middle, and he says the list could go on. Restore the comic abridgment before Charles reacts."),
    "B61_R0112": ("", (), "Charles is delighted and introduces himself with his complete spoken name. This is a personal introduction following Maria's and Xien's exchange about being elderly."),
    "B64_R0060": ("I call out as each ship comes in. You're the hundredth I've asked.",
        ("as each ship comes in.","You're the hundredth I've asked."), "The sailor says he has been approaching arriving sailors here to find a captain who believes in miracles. Keep the repeated effort and the exact count without inventing its duration."),
}


def main():
    assert not DRAFT.exists() and not PLANS.exists()
    packet, sources, release = map(base.load, (PACKET,HISTORY,parent.RELEASE))
    assert release["registry_sha256"]==base.digest(base.REGISTRY)
    assert release["candidate_sha256"]==packet["candidate_sha256"]==sources["candidate_sha256"]==base.digest(parent.ROM)
    assert sources["source_packet_sha256"]==base.digest(PACKET)
    assert sources["findings"]=={"exact-stored":595,"display-review-followup":18}
    matched={r["id"]:r for r in sources["records"] if r["decision"]=="display-review-followup"}
    history={}
    for path, digest in sources["previous_reviews"].items():
        assert base.digest(path)==digest
        history[path]={r["id"]:r for r in base.load(path)["records"]}
    records=[]
    plans={}
    planner=parent.writer.engine.assemble({}).__globals__["plan_progressive"]
    for group in packet["groups"]:
        for pair in group["records"]:
            ident=pair["id"]
            if ident not in matched:
                continue
            ref=matched.pop(ident)
            old=history[ref["review_path"]][ident]
            assert old["kind"]=="progressive" and pair["native_command_word"]==0x4000
            selector=pair["selector"]
            src,installed=[f"{selector:02x}"+pair[key+"_reference"]["exact_body_hex"] for key in ("source","current")]
            assert src==old["source_hex"] and all(old["review"].values())
            assert pair["source_reference"]==ref["source_reference"] and pair["current_reference"]==ref["current_reference"]
            english,phrases,note=DECISIONS[ident.removeprefix("DK4_MES_")]
            live=" ".join(pair["current_English"].split())
            finding="wording" if english else "wrap-only" if phrases else "retention"
            row=pair | dict(route=3,kind=old["kind"],speaker=old["speaker"],source_selector=selector,native_slots=[],
                source_hex=src,current_hex=installed,previous_English=live,english=english or live,
                protected_phrases=list(phrases),source_meaning=old["source_meaning"],context=old["whole_exchange_context"],
                localization_note=note,prior_decision_dependency=ref,change_class=finding,
                decision="retention" if finding=="retention" else "revision",
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False))
            if finding!="retention":
                body,plan=planner(row,selector,bytes.fromhex(installed)[1:],bytes.fromhex(src)[1:])
                assert body!=bytes.fromhex(installed)[1:]
                plans[ident]=plan
                print(ident,plan["lines"],plan["expected_native_pages"])
            records.append(row)
    assert not matched and len(records)==18
    findings=dict(Counter(r["change_class"] for r in records))
    assert len(plans)==8 and findings=={"wording":6,"wrap-only":2,"retention":10}
    draft=dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(PACKET),source_packet_sha256=base.digest(PACKET),prior_exact_595=str(HISTORY),
        prior_exact_595_sha256=base.digest(HISTORY), findings=findings,contextual_records_revisited=18,
        contextual_decisions_reused=595,new_editorial_credit=0,records=records,planned_FE={})
    base.save(DRAFT,draft)
    base.save(PLANS,dict(draft_sha256=base.digest(DRAFT),plans=plans))
    print(findings)


if __name__=="__main__":
    main()

