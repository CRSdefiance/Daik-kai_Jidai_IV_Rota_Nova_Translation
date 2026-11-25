"""Review the Maria lines whose installed bodies changed after their earlier contextual passes."""

from collections import Counter
from pathlib import Path

from scripts import register_maria_B21_B32_20261122 as parent


base = parent.base
ROOT = Path("work/analysis/maria_B33_B49_followup_20261122")
SOURCE = ROOT / "paired_source_registered_candidate.json"
HISTORY = ROOT / "prior_contextual_decisions_reuse.json"
NAMES = parent.writer.ROOT.parent / "name_width_followups.json"
DRAFT = ROOT / "maria_followup_manuscript_v4.json"
PLANS = ROOT / "maria_followup_preflight_v4.json"

# Empty replacement fields record an individual editorial retention.
DECISIONS = {
    "B33_R0080": ("", (), "Jam balances fear with admiration. Keep the two spoken beats so his affectionate punch line lands after the others praise Maria."),
    "B35_R0006": ("Pardon the sudden interruption...", (), "Hodram approaches politely and acknowledges how unexpected it is. His brief apology fits Maria's brisk reply and keeps his initial reserve."),
    "B35_R0025": ("", (), "Maria turns Hodram's question back on him. The break at her pause keeps her answer cool and lets his silence follow."),
    "B36_R0041": ("", ("running China's underworld,",), "Lil first defends her own part, then throws the accusation back at Maria. Keep all her words and keep the accusation about China's underworld together."),
    "B38_R0005": ("", (), "Making waves suits Uddin's conversational recognition and retains the recent stir in the Indian Ocean. Carry the original surname substitution and 25 actor selector."),
    "B38_R0022": ("", (), "Uddin says that expelling the Europeans occupies him for the moment. His unfinished 'So...' hands off naturally to the next turn's joint-front proposal."),
    "B39_R0008": ("", (), "Xien recognizes Nagarpur and then wonders why he's still here. The pause separates recognition from surprise without implying he was hiding."),
    "B41_R0049": ("", (), "Maria answers the suggestion that she stay in Ming. She gives practical reasons for leaving in her own voice before the report about the government."),
    "B43_R0018": ("", (), "Maria calls the completed trading post real progress but only a first step. Xien follows with advice on reinvesting the profits."),
    "B47_R0060": ("They took so many from my village! They're forcing them to work all over, with barely enough to eat!", ("barely enough to eat!",),
                "Keep the villager's outraged testimony in the present where she describes the forced labor, away from home and with barely enough food."),
    "B47_R0140": ("Espinosa had this. He'd long sought Africa's Proof of Conquest, too. We prayed he'd never get his hands on it...", ("Proof of Conquest, too.","get his hands on it..."),
                "Keep the former possession distinct from the Proof and preserve the shopkeeper's fear that it would fall into Espinosa's hands."),
    "B47_R0211": ("", (), "Maria's short return question follows Jam's unexpected declaration of loyalty. Keep her puzzled tone and what she heard from him aloud."),
    "B48_R0083": ("I had no idea you were so lovely... Clau, those rumors have to be made up.", ("you were so lovely...",),
                "Rafael's surprised compliment leads into his reassurance to Clau. It keeps his sincerity distinct from Clau's nervous flattery in the reply."),
    "B48_R0142": ("", (), "Rafael states that Spain rules Portugal and voices his hope for a seafaring revival. Keep that hope separate from Maria's question about ruling the world."),
    "B48_R0178": ("", (), "Rafael mistakes Maria's thoughtful praise for criticism and apologizes for sounding presumptuous. Her next line reassures him."),
    "B48_R0257": ("Of course! We'll join you in a heartbeat. Especially against those Spanish bastards! Right?", ("Spanish bastards!","in a heartbeat."),
                "Clau agrees to help generally and especially against the Spanish. Keep his rough insult and quick appeal to Rafael."),
    "B49_R0139": ("...That's a flimsy excuse. You're just exploiting the locals' feelings, aren't you?", ("the locals' feelings,","aren't you?"),
                "Keep Maria's skepticism about using the villagers' feelings. Repeating 'exploiting' lets the pirate seize on her own word in his reply."),
}


def build_manuscript():
    packet, receipt, release = map(base.load, (SOURCE, HISTORY, parent.RELEASE))
    assert receipt["packet_sha256"] == base.digest(SOURCE)
    assert receipt["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    differences = {rec["id"]:rec for rec in receipt["records"] if rec["decision"] == "display-review-followup"}
    assert len(differences) == len(DECISIONS) == 17 and receipt["findings"]["exact-stored"] == 343
    reviews, records = {}, []
    for group in packet["groups"]:
        for pair in group["records"]:
            ident = pair["id"]
            if ident not in differences:
                continue
            dependency = differences.pop(ident)
            path = dependency["prior_review"]
            if path not in reviews:
                assert base.digest(path) == dependency["prior_review_sha256"]
                reviews[path] = {row["id"]:row for row in base.load(path)["records"]}
            prior = reviews[path][ident]
            selector = pair["selector"]
            source_hex = f"{selector:02x}" + pair["source_reference"]["exact_body_hex"]
            current_hex = f"{selector:02x}" + pair["current_reference"]["exact_body_hex"]
            assert prior["source_hex"] == source_hex and all(prior["review"].values())
            assert pair["native_command_word"] == 0x4000
            english, phrases, note = DECISIONS[ident.removeprefix("DK4_MES_")]
            current = " ".join(pair["current_English"].split())
            change = "wording" if english else "wrap-only" if phrases else "retention"
            context = prior.get("whole_exchange_context") or prior.get("full_clean_exchange_context") or prior["context"]
            meaning = prior.get("source_meaning") or prior["source_gloss"]
            records.append(pair | dict(route=3,kind="progressive",speaker=prior["speaker"],
                source_selector=selector,native_slots=[],source_hex=source_hex,current_hex=current_hex,
                previous_English=current,english=english or current,protected_phrases=list(phrases),
                context=context,source_meaning=meaning,localization_note=note,change_class=change,
                decision="retention" if change=="retention" else "revision",prior_decision_dependency=dependency,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    assert not differences
    named = base.load(NAMES)
    assert named["candidate_sha256"] == release["candidate_sha256"]
    for proposal in named["records"]:
        row = proposal["record"].copy()
        row.update(previous_English=proposal["installed"]["english"],change_class="wording",
                   localization_note=row["followup_reason"])
        records.append(row)
    records.sort(key=lambda row:(row["block"],row["source_reference"]["offset"]))
    return dict(translation_policy="natural-dialogue-v2",target_locale="en-US",encoder="dialogue-relocatable-v1",
        previous_sha256=release["candidate_sha256"],previous_registry_sha256=release["registry_sha256"],
        source_packet=str(SOURCE),source_packet_sha256=base.digest(SOURCE),prior_exact_343=str(HISTORY),
        prior_exact_343_sha256=base.digest(HISTORY),paired_name_wrap_proposals=str(NAMES),
        paired_name_wrap_proposals_sha256=base.digest(NAMES), contextual_records_revisited=19,
        contextual_decisions_reused=343,findings=dict(Counter(row["change_class"] for row in records)),
        new_editorial_credit=0,records=records,planned_FE={})


def main():
    assert not DRAFT.exists() and not PLANS.exists()
    draft = build_manuscript()
    planner = parent.writer.engine.assemble({}).__globals__["plan_progressive"]
    plans = {}
    for row in draft["records"]:
        if row["decision"] == "retention":
            continue
        obsolete, original = (bytes.fromhex(row[key])[1:] for key in ("current_hex","source_hex"))
        _, plan = planner(row, row["source_selector"], obsolete, original)
        plans[row["id"]] = plan
        print(row["id"],plan["lines"],plan["expected_native_pages"])
    print(draft["findings"])
    base.save(DRAFT,draft)
    base.save(PLANS,dict(draft_sha256=base.digest(DRAFT),plans=plans))


if __name__ == "__main__":
    main()

