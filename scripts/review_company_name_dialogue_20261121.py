"""Review complete beats around the company name and preserve its original substitution."""

from collections import Counter
from pathlib import Path

from scripts import prepare_company_name_dialogue_20261121 as paired
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical


base, ROOT, parent = paired.precedent.base, paired.ROOT, paired.parent
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v3.json"
ACTORS = Path("translations/editorial_checkpoints/SharedText_20261110_v1/actor_name_inventory_current_v1.json")

CONTEXTS = """
0 37|Julio encourages Rafael to stand his ground. Rafael clears his throat, announces his company and identifies himself before the applause.
0 44|Julio makes Rafael captain and entrusts him with the loan. Rafael protests in surprise before Julio explains all three responsibilities.
0 70|Rafael's party has reached the Far East. A stranger recognizes its leader. Clau comments on his appearance, is shushed, and Rafael answers for himself.
0 292|A local recognizes Rafael as belonging to the company and tells him the Genoa guild is looking for him.
1 153|A guard recognizes the player's group and permits entry. A benefactor presents a gift, then answers Hodram's questions about resisting Ottoman rule and helping Sera.
2 54|Kuhn and his subordinate discuss Lil's suspicions. They plan a false-flag attack with an excuse to strike the Li family or a staged accidental death if Lil survives.
2 60|The speaker reflects on Maldonado's defeat, the player's company and what each version of the independence plan now requires.
2 138|Lil asks what happened. The man reports the Nagarpur Company's absorption and explains why it amounts to being ruined.
2 151|The man dismisses the first answer. Lil objects to how he addresses her and supplies her name. He begins to recognize her affiliation, and she guesses that he is Maldonado.
2 282|The same local gives Lil the same message from the Genoa guild as in Rafael's route.
3 113|Maria and Nagarpur exchange insults. Nagarpur recognizes Maria's clan and challenges her means and resolve before threatening a lesson about money.
3 118|The same guard recognizes the player's group and allows entry before the benefactor presents a gift.
3 139|Maria's crew decide to recruit the learned stranger despite his manners. After the invitation he explains why he refuses.
"""

# Each row gives the source meaning and a specific editorial reason.
REVIEWS = """
0 37 81|Julio warns that this proud man may prey on anyone who looks ready to run.|Keep his practical caution as the reason for Rafael's display of confidence.
0 37 84|Rafael questions the advice, steels himself and clears his throat.|The hesitation makes his public declaration a deliberate change of register.
0 37 89|Rafael begins a declaration of Portuguese voyages under the banner of defeating Spain and reviving Portugal.|The long declaration deliberately stops before supplying the company name.
0 37 94|Rafael emphatically names the company.|Retain the standalone name because the previous turn builds toward the reveal.
0 37 99|Rafael identifies himself as the admiral.|Keep the explicit rank and rhetorical continuation after the company reveal.
0 37 103|Julio calls the declaration splendid.|The brief delighted reaction fits the applause that follows.
0 37 107|The others voice approval and applaud.|Retain the audible reaction before the next exchange.
0 44 308|Julio tells Rafael he is the ship's captain.|The short announcement leaves room for Rafael's surprise.
0 44 312|Rafael asks why he is captain when Janus and Clau rebuilt the ship.|The interruption and their contribution remain explicit.
0 44 316|Julio trusts Rafael as the company's head and gives him responsibility for the loan.|Keep the name and company substitutions and the duty attached to the loan.
0 44 320|Rafael incredulously repeats the company name and questions becoming its leader.|Keep the interrupted repeat after Julio's announcement.
0 44 324|Julio encourages Rafael to make his name alongside the greatest sailors.|The question and encouragement establish the level of ambition Julio expects.
0 44 327|Julio distinguishes the ship captain, fleet admiral and company leader roles.|The assigned responsibilities remain separate and intelligible.
0 44 330|Julio jokes that making Claudio responsible could leave him working for free forever.|Keep the hypothetical consequence and the comic threat.
0 70 5|Rafael marvels at the far-eastern edge of the world.|The brief thought belongs at the start of the crew's observations.
0 70 18|Janus notices the buildings look different from those in the Arab lands and India.|The observations preserve the travelers' perspective and named places.
0 70 25|Clau is excited by the adventure and notices someone approaching.|His subject changes naturally as the stranger arrives.
0 70 29|The stranger excuses the interruption and identifies Rafael by surname as the head of the company.|Keep his careful supposition and the company leadership in a complete question.
0 70 32|Clau thinks the older man looks like an Eastern military commander.|This is Clau's impression and explains the reprimand.
0 70 43|A crewmate hushes Clau for being rude.|The interruption acknowledges that Clau spoke aloud.
0 70 50|Rafael confirms his identity by giving his name.|Keep the direct confirmation before the stranger continues.
0 292 6|A local confirms the affiliation and says the Genoa guild has been looking for the player.|Keep the local's familiar recognition and ongoing search. Reflow the short question as one unit across both routes.
1 153 6|The guard recognizes the company's member and grants passage.|Match the same guard and Japanese in Maria's route. Keep the permission as a complete short sentence.
1 153 9|The benefactor addresses the ruler of the Mediterranean and offers the gift.|Retain the ceremonial address and gift announcement.
1 153 12|Hodram hesitantly asks the benefactor's identity.|The short question lets the benefactor choose how much to disclose.
1 153 16|The benefactor has resisted Ottoman rule for a long time.|The reply provides a history of resistance instead of a personal name.
1 153 27|Hodram asks whether he helped Sera and the others.|The tentative question links the resistance account to their earlier encounter.
1 153 34|The benefactor advises him to solve the gift's secret and find the Proof quickly.|Keep the reluctance to discuss details and the urgency of the instruction.
1 153 45|Other people have escaped Ottoman rule too. The next lead is ruins in Turkey.|Keep the specific directions after the disclosure about the resistance.
2 54 5|The subordinate calls to Kuhn with respect.|Keep the established address for his superior.
2 54 9|Kuhn tersely asks what he wants.|His clipped response gives the subordinate the floor.
2 54 13|Lil has made contact with the Li family and seems suspicious of Kuhn.|Retain the uncertainty that precedes the report about his son.
2 54 16|She has apparently been asking about Kuhn's son in secret.|The subordinate is reporting suspicions and preserves the relationship.
2 54 20|Kuhn thinks Lil is still useful but considers disposing of her and admits how much she helped.|The apparent praise gives his decision its cold tone.
2 54 24|The subordinate agrees to proceed with the earlier plan.|The trailing thought invites Kuhn to give the order.
2 54 27|Kuhn orders a fleet disguised as Li ships to attack while their own fleet waits nearby.|Preserve the distinction between the attacking fleet and the fleet standing by.
2 54 31|If the disguised attackers win, they can claim to avenge their ally and have a pretext to strike the Li family.|Separate the planned pretext from the condition. Keep the alliance and the transition to the alternative.
2 54 34|If Lil survives, their fleet will attack her tired ships and arrange for her to be hit by a stray shot.|The ironic twist on luck is deliberate and belongs to the subordinate's plan.
2 54 38|If Lil disappears, no evidence remains. The subordinate praises the plot.|The praise explains Kuhn's brusque response.
2 54 42|Kuhn rejects the flattery and entrusts the job to him.|The direct order ends their plotting.
2 54 45|The subordinate takes responsibility.|Keep the understated answer after Kuhn's order.
2 60 11|The speaker reacts privately to Maldonado's defeat.|The trailing reaction conveys surprise without declaring that Maldonado died.
2 60 15|The speaker has heard of a company recently entering the area.|Retain the report as hearsay before the assessment.
2 60 20|The speaker is surprised by Maldonado's defeat and thinks the company has accomplished more than expected.|Keep the pause and private assessment while giving the entire company name a clear place in the sentence.
2 60 34|With Clifford absent, the speaker thought the independence plan would be easy.|Retain the original circumstance in this branch.
2 60 39|The speaker thought using Maldonado and defeating Clifford would make the independence plan easy.|Retain the two means and the plan in this alternate branch.
2 60 46|Given the outcome, the speaker concludes they must use all their strength to defeat the company.|Keep the escalation and put the name before the verb's particle to prevent doubled terminal punctuation.
2 138 11|Lil asks the man what's wrong.|Her short opening gives him room for the news.
2 138 23|The man reports that the Nagarpur Company has been absorbed by the player's company.|Give the excited man an active sentence that preserves who took over whom.
2 138 27|He has heard that the company is as good as ruined.|Keep hearsay as his interpretation of the takeover.
2 151 90|The man eagerly starts giving his background in Paris.|Keep his long-winded answer as the setup for the interruption.
2 151 93|The hostile speaker cuts him off.|The abrupt rebuke belongs before Lil objects to the form of address.
2 151 100|Lil objects to being called woman and introduces herself by name.|The short retort gives him the clue he needs.
2 151 103|He repeats her given name and wonders whether she belongs to the company.|Keep recognition as an uncertain question and make the name part of that question.
2 151 107|Lil asks whether he knows her and whether he is Vasquez Maldonado.|Retain her surprise and his full name.
2 151 125|A crewmate thinks that this is Maldonado.|Keep the measured reaction as a separate observed alternative.
2 151 134|A crewmate thinks that this is Maldonado.|Keep the sharper alternate reaction and his name.
2 282 6|A local confirms the affiliation and says the Genoa guild has been looking for the player.|Match the familiar wording in Rafael's route for the same line and speaker.
3 113 74|A crewmate remarks that the man fails to understand.|The dry private reaction leads into Nagarpur's display of confidence.
3 113 81|Nagarpur asks if they are new and threatens a demonstration of his company's strength.|Retain the rhetorical challenge, with the company's name made explicit.
3 113 85|Maria identifies Nagarpur and calls out the company's greed.|Keep her cool delivery of the reputation, which provokes the next line.
3 113 89|Nagarpur identifies Maria's faction and challenges her resolve and financial means after being insulted.|Make the affiliation natural in English and keep both parts of the challenge.
3 113 92|Nagarpur promises to teach them to appreciate money and laughs.|Retain his gleeful threat without adding an outcome.
3 113 97|Maria considers him a potentially troublesome opponent.|The restrained assessment lets the exchange end without predicting the result.
3 118 5|The guard recognizes the company's member and grants passage.|Match the same guard and Japanese in Hodram's route.
3 118 8|The benefactor addresses the ruler of the Mediterranean and offers the gift.|The formal address works after the guard's brief directions.
3 139 108|A crewmate suggests recruiting the learned stranger despite his manners.|Keep the contrast that motivates the invitation.
3 139 112|Maria tentatively agrees.|The pause preserves her hesitation.
3 139 116|The stranger splutters and asks who they are.|Keep his startled demand before the proposal.
3 139 120|The crewmate compliments the stranger's knowledge and asks him to lend their company his help.|Make the invitation sound like an invitation to join, as the stranger understands it in the next turn.
3 139 124|He refuses to leave town and particularly refuses an invitation from a man.|Retain both objections and the distinction between them.
3 139 128|The crewmate still asks him to lend his help.|The short plea follows through after his refusal.
3 139 131|The stranger is unmoved at first, then suddenly reacts.|Keep the interrupted response that points into the next scene.
"""

REVISIONS = {
    (0, 70, 29): ("Excuse me. FO is under your command, isn't it, FA?", ("under your command", "isn't it, FA?")),
    (0, 292, 6): ("You with FO? The Genoa guild's been looking for you.", ("You with FO?", "The Genoa guild's", "been looking for you.")),
    (1, 153, 6): ("You're with FO? Go on through.", ("Go on through.",)),
    (2, 54, 31): ("If the disguised fleet wins, we can attack the Li family. We'll claim we're avenging FO, our ally...",
                  ("If the disguised fleet wins,", "the Li family.", "FO, our ally...")),
    (2, 60, 20): ("Maldonado lost... FO has done more than I expected.", ("Maldonado lost...", "more than I expected.")),
    (2, 60, 46): ("We'll have to go all out to bring FO down.", ("go all out", "to bring FO down.")),
    (2, 138, 23): ("Bad news! FO has taken over the Nagarpur Company!", ("the Nagarpur Company!",)),
    (2, 151, 103): ("FI...? Wait. Are you with FO, by any chance?", ("with FO", "by any chance?")),
    (2, 282, 6): ("You with FO? The Genoa guild's been looking for you.", ("You with FO?", "The Genoa guild's", "been looking for you.")),
    (3, 113, 89): ("You're with FO? I trust you've got the nerve and the money to back up those insults!",
                   ("You're with FO?", "the nerve and the money", "back up those insults!")),
    (3, 118, 5): ("You're with FO? Go on through.", ("Go on through.",)),
    (3, 139, 120): ("I admire your knowledge. Please give FO a hand.", ("I admire your knowledge.", "give FO a hand.")),
}


def main():
    assert not OUTPUT.exists()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    actors = base.load(ACTORS)["records"]
    contexts = {}
    for line in CONTEXTS.strip().splitlines():
        ref, text = line.split("|", 1)
        contexts[tuple(map(int, ref.split()))] = text
    notes = {}
    for line in REVIEWS.strip().splitlines():
        ref, meaning, reason = line.split("|", 2)
        notes[tuple(map(int, ref.split()))] = (meaning, reason)
    records = []
    for group in packet["groups"]:
        route, block, path = (group[k] for k in ("route", "block", "file_path"))
        for data in group["records"]:
            index = data["source_record_index"]
            ref = (route, block, index)
            if ref not in notes:
                continue
            selector = data["selector"]
            assert data["native_command_word"] == 0x4000 and data["slots"] == []
            previous = logical(data["current_English"])
            english, phrases = REVISIONS.get(ref, (previous, ()))
            meaning, reason = notes[ref]
            assert (ref in REVISIONS) == (english != previous)
            assert TOKEN.findall(english) == TOKEN.findall(previous) == TOKEN.findall(data["Japanese"])
            source, current = (dict(file_path=path, block=block, offset=data[f"{side}_offset"],
                command_offset=data[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
                exact_stored_hex=bytes([selector]).hex() + data[f"{side}_body_hex"]) for side in ("source", "current"))
            source["record_index"] = index
            records.append(dict(id=f"DK4_MES_B{block}_R{index:04}", file_path=path, route=route, block=block,
                kind="progressive", native_command_word=0x4000, source_selector=selector, native_slots=[],
                source_reference=source, current_reference=current, source_hex=source["exact_stored_hex"],
                current_hex=current["exact_stored_hex"], Japanese=data["Japanese"], english=english,
                previous_English=previous, context=contexts[route, block], speaker=actors[selector]["current_consumers"][0]["text"],
                source_meaning=meaning, localization_note=reason, protected_phrases=list(phrases),
                finding="prose" if ref in REVISIONS else "retention", decision="revision" if ref in REVISIONS else "retention",
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(records) == len(notes)
    assert sum(r["decision"] == "revision" for r in records) == len(REVISIONS)
    matches = {(r["route"], r["block"]): r for r in records if r["decision"] == "revision"}
    for a, b in (((1, 153), (3, 118)), ((0, 292), (2, 282))):
        other = matches[a] if a in matches else next(r for r in records if (r["route"], r["block"]) == a)
        assert other["source_hex"] == matches[b]["source_hex"] and other["english"] == matches[b]["english"]
    counts = dict(Counter(r["decision"] for r in records))
    base.save(OUTPUT, dict(previous_sha256=release["candidate_sha256"], previous_registry_sha256=release["registry_sha256"],
        source_packet_sha256=base.digest(SOURCE), records=records, decisions=counts, translation_policy="natural-dialogue-v2",
        encoder="dialogue-relocatable-v1", target_locale="en-US", review_gates=GATES, new_coverage_credit=0,
        formatting_and_registration_pending=True))
    print(f"{len(records)} contextual decisions: {counts}", flush=True)


if __name__ == "__main__":
    main()
