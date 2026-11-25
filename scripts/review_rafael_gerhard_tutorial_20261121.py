"""Review Gerhard's recruitment, its branches, menus and sea-battle lessons."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_spain_london_20261121 as parent
from scripts.review_rafael_east_asia_followup_20261121 import TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/analysis/rafael_tutorial_B84_followup_20261121")
SOURCE, OUTPUT = ROOT / "paired_source_registered_parent.json", ROOT / "gerhard_contextual_review_v3.json"
PRIOR = Path("translations/rafael_B81_B84_contextual_final_review_v1.json")
GATES = ("source", "context", "localization", "naturalness", "formatting")
SPEAKERS = {0: "Rafael Castor", 4: "Janus Pasar", 5: "Claudio Manaus", 16: "Gerhard Adernkatz",
            82: "Shopkeeper", 162: "Boy", 254: "System panel", None: "Player choice"}

# Empty English preserves the installed wording. A pair of paragraphs marks original FE pages.
DECISIONS = """
0005|||Rafael opens with a practical question about finding a navigator in town.
0010|||Claudio answers confidently about sailors, a wider group than navigators.
0014|||Claudio logically turns from a general assurance to sending Janus to ask around.
0017|||Janus grumbles about being given the errand in his familiar rueful voice.
0021|Excuse me. I'm looking for someone who knows a lot about ships...||Janus approaches politely and breaks off before the shopkeeper answers.
0024|||The shopkeeper recognizes a seafarer and starts to mention Mr. Adernkatz before thinking better of it.
0027|||The odd chuckle and dismissal explain why Janus considers the man unsettling.
0030|What a creepy fellow. Adern... Adernkatz, was it? Might as well look for him.||Janus tries the unfamiliar name aloud and decides to follow up on the lead.
0034|||Janus addresses his admiral and reports only as much of the name as he recalls.
0037|What?! Adernkatz?! You're sure, Janus?|You're sure, Janus?|Claudio's shock and quick confirmation question show he recognizes the name.
0040|||Janus pushes back at the implied doubt instead of supplying new proof.
0044|||Claudio's sudden decision leads straight into Rafael calling after him.
0048|||Rafael uses Claudio's established nickname as he hurries after him.
0053|||Claudio addresses the boy informally and asks for Gerhard by full name.
0057|You mean Admiral Adernkatz? His house is that way.||The boy supplies the title which Claudio notices next. House leaves the scale of the residence open.
0060|Admiral... I thought so. Thanks, kid. That way, right? Hurry up, FI!|Hurry up, FI!|Claudio confirms his own hunch, checks the direction and keeps the given-name substitution.
0064|...You're usually not this eager, Clau.||Rafael notices that Claudio's enthusiasm is unusual for him.
0068|That's not why... Never mind. You'll see when we get there.||Claudio backs away from explaining his unusual behavior and lets the meeting speak for itself.
0071|||The brief question fits arriving at the house.
0076|...Looks like it.||Claudio answers tentatively before the knock.
0080|||The speakerless cue stays on the original FE panel and represents the knock at the door.
0085|||Gerhard's cautious pause and question fit the unexpected visit.
0089||with FO,|Rafael begins a polite introduction that Claudio interrupts. Allow the full faction substitution and its company suffix.
0093||FI FA.;I'm Claudio Manaus,|Claudio finishes Rafael's introduction and introduces himself as a navigator. Give both substitutions room at the supported maximum widths.
0097|||Gerhard registers Claudio's profession and asks why the group came.
0100|We heard you're an excellent navigator. We were hoping to speak with you...||Janus explains what they heard and starts a courteous request.
0103|That was a long time ago. I live ashore now, as you can see.||Gerhard puts his former profession in the past and points to his life ashore.
0106|Would you consider going back to sea?||Rafael opens with an invitation and leaves the decision to Gerhard.
0110|||Gerhard's blunt refusal sets up Claudio's insistence.
0114|You can't brush us off that easily. You know Vels, don't you?||Claudio challenges the dismissal and names the man he came to ask about.
0117|||Gerhard's silence carries recognition before Claudio presses him.
0121|||Claudio pointedly calls Vels the man Gerhard let go. Gerhard's later account supplies the circumstances.
0125|What?! W-what are you talking about?||Rafael stammers at the unexpected accusation.
0130|||Gerhard lets the accusation stand without answering yet.
0134|Clau! What are you talking about?!||Janus demands an explanation in a direct voice.
0137|This is Admiral Gerhard Adernkatz. He commanded the strongest private fleet ever put together to hunt pirates.||Claudio identifies Gerhard and distinguishes the private pirate-hunting fleet from a national navy.
0140|For a while, pirates kept their heads down from the North Sea to the Mediterranean. That was Gerhard's fleet at work.|North Sea;to the Mediterranean.|Keep the two geographic boundaries, limited period and Claudio's credit to Gerhard's fleet.
0143|He did all that?!||Rafael's surprise responds to the scale of the fleet's accomplishments.
0147|His fleet once captured a big gang of pirates. Vels was one of them.||Claudio connects the capture to Vels without implying that Gerhard commanded a state navy.
0151|||Janus's short interruption shows surprise at the connection.
0155|That's enough. Manaus, isn't it? I'll tell the rest. Come in, Admiral. The rest of you, too.|Come in, Admiral.|Gerhard takes over, checks Claudio's surname and invites the full party inside.
0160|||Gerhard explains that Vels was young and promising. Taking him in and training him are separate actions.
0164|Vels the pirate... an admiral's pupil?!||Janus voices the paradox prompted by learning who trained Vels.
0167|||Gerhard makes the timing explicit. Vels mutinied as soon as he got the ship, and Gerhard chose to resign.
0171|Why didn't you go after him then?||Claudio asks why Gerhard did not pursue Vels at the time.
0175|Some of my crew had fought beside me for years. The promise of freedom and money drew them after him.||Gerhard remembers experienced subordinates and names what drew them away.
0179|...I believed in strict discipline and living frugally. Maybe I was wrong. I lost faith in my own command.||Gerhard questions his values after the betrayal and admits that he lost confidence in himself.
0182|||Claudio listens in silence instead of interrupting the admission.
0186|I turned my back on the sea!||Gerhard insists on the decision he made and speaks more forcefully than in the following lines.
0190|I have a good life here. People leave me in peace. The days go by, quiet and uneventful...||Gerhard depicts a comfortable but unchanging life before Rafael challenges him.
0193||settled it, has it?|Rafael asks the original gentle challenge and keeps its question tag readable.
0197|FI, was it? What are you getting at? Go on. Say it plainly.|What are you getting at?;Say it plainly.|Gerhard checks Rafael's given name and invites him to make the point openly.
0201|Vels nearly wiped out our fleet. We need your help.||Rafael explains why their own force needs him, then states the request directly.
0206|My help? What good would an old man's advice do? He took everything from me.||Gerhard dismisses his own advice after the loss. This moment needs his vulnerability more than an ornate voice.
0210|That's not true.||Rafael answers the self-doubt immediately before Gerhard presses him for specifics.
0215|||Gerhard asks what Rafael expects him to do and uses the same given-name substitution.
0218|||Rafael pauses before the player chooses how to answer.
3114_0|||The first answer proposes tackling Vels together and leads into Rafael's matching invitation.
3114_1|Our fleet needs you.||The second reply asks him to join for the fleet's sake. The branch says that defeating Vels is only part of the reason.
0234|Just come aboard as you are. That's all we ask. Let's defeat Vels together!|Let's defeat Vels together!|Rafael says Gerhard need bring only himself and invites him to help face Vels.
0244|Please don't take offense. Even with my help, I can't see you holding your own against Vels.||Gerhard tempers a frank assessment with courtesy.
0248|You don't think we're ready...?||Rafael checks whether their current ability is Gerhard's objection.
0253|||Gerhard asks for time and leaves his answer open.
0257|Of course. I hope you'll have decided by the time we meet again. Excuse us.||Rafael waits for an answer on a later visit and excuses the party politely.
0262|||Keep Gerhard's silent response as the visit ends.
0272|Forgive me if I spoke out of turn.||Rafael acknowledges that he may have sounded presumptuous.
0277|But you built a fleet they called the strongest. I can't believe you were wrong to lead it your way.||Rafael supports Gerhard's leadership using the fleet's reputation as evidence.
0281|||Gerhard's surprise is shown without supplying an unspoken answer.
0285|Vels was in the wrong. Greed blinded him, and he betrayed you. I can't forgive that!||Rafael takes a clear moral position about the betrayal.
0290|||Gerhard pauses before raising the practical issue of finding Vels.
0294|But Vels is cautious. He won't be easy to draw out.||Gerhard shifts from the betrayal to the difficulty of luring Vels into the open.
0297|He's gotten cocky. Spread the word that you're back at sea, and he'll come out on his own.||Rafael's confidence rests on Vels's overconfidence and the rumor that Gerhard has returned.
0302|||Gerhard considers the plan because Vels likely believes he is dead.
0306|||Rafael's unfinished question gives Gerhard room to make his own decision.
0311|Very well. I set this in motion. I ought to see it through.||Gerhard accepts responsibility and resolves to settle the matter himself.
0314|Thank you! Train us, too. We're ready for it.||Rafael thanks him and volunteers the crew for demanding training.
0319|||Gerhard responds with the warning that his training will be hard.
0327|||The second branch says defeating Vels is one reason for the invitation and leaves room for other goals.
0332|What do you mean?||Gerhard asks Rafael to explain the broader invitation.
0336|Come aboard for our fleet's sake! With you along, we could do something worth remembering.||Rafael wants to accomplish something historic with Gerhard's help but does not promise success.
0340|||Gerhard weighs the appeal in silence.
0350|Please don't take offense. Fine words from someone your age can't persuade me to put my life in your hands.||Gerhard acknowledges the speech before refusing to commit his life on its strength.
0353|You don't think we're ready...?||Keep Rafael's matching response in both branches.
0358|I've left the sea behind. For today, I'd like you to go.||Gerhard repeats his decision to live ashore and asks them to leave for the day.
0361|Of course. I hope you'll have decided by the time we meet again. Excuse us.||Use the same polite exit in this branch.
0366|||Gerhard's silence mirrors the end of the other initial conversation.
0376|Forgive me if I spoke out of turn.||Keep Rafael's renewed approach consistent across the two follow-ups.
0381|But you built a fleet they called the strongest. I can't believe you were wrong to lead it your way.||Rafael gives the same reason for trusting Gerhard's methods in this branch.
0385|||Gerhard is visibly surprised before Rafael states what he wants to learn.
0389|||Rafael asks directly to be taught and adds an earnest plea.
0394|||Leave Gerhard a beat before his warning.
0398|||Gerhard's short warning echoes his response in the Vels branch.
0402|||Rafael hears a possible agreement and lets Gerhard finish.
0407|All right. But you'd better be ready.||Gerhard agrees and makes clear that Rafael must be prepared.
0417|Before I go back to sea, there's something I'd like to teach you. Are you up for some special training?||Gerhard offers a choice before he returns to sea and asks how far Rafael wants to go.
5298_0|Take the tough training.||A direct caption for the full practical course. It stays in the original first slot.
5298_1|||The short answer clearly chooses to hear the explanation without the practical course.
5298_2|Stick with my own style.||The third caption selects learning on the ship in Rafael's own way and does not imply that he declined Gerhard's company.
0439|You've got nerve. Don't give up halfway through.||Gerhard approves of the resolve and warns Rafael that the course is demanding.
0443|Now you're looking the part. Show me to your ship.||Gerhard gives restrained praise after training and asks to be shown the ship.
0446|I'll explain naval combat on the way.||Gerhard offers instruction as they walk to the ship.
0449|||Rafael accepts the lesson politely before Gerhard begins.
0454|Let's start with naval gunfire. I'll show you a classic tactic called crossing the T.||Keep the specific named tactic and let Gerhard introduce it to a novice.
0458|Stay clear of their broadside. Pass ahead of the bow or behind the stern, then turn your broadside toward them and fire.|of their broadside.;turn your broadside;and fire.|Keep the side to avoid, both positions and the player's firing orientation.
0461|||Rafael's hesitant acknowledgment lets Gerhard finish the example.
0466|Steer and let your gunners fire. To improve their fire, assign an officer with high Aim to a Gun Battery.|let your gunners fire.;To improve their fire,;high Aim;a Gun Battery.|Retain the automatic gunners and both installed English equipment and stat labels.
0470|Steer and adjust the sails as usual during naval battles.~Your ship fires automatically when an enemy ship comes within range.||Use one complete instruction per existing FE panel, with the automatic fire rule on the continuation.
0473|If you prefer boarding, go to the shipyard and refit a hold into Quarters.||Keep the shipyard refit action and exact Quarters label.
0476|Hire plenty of sailors. Then assign an officer with high Swords to the Quarters as Boarding Leader. That will make boarding more effective.||Explain the headcount, skill, assigned job and expected effect in order.
0480|||This panel gives a clear single action with the actual Swords and Quarters labels.
0483|Boarding starts automatically when ships touch. Your Boarding Leader should make a difference.||Preserve the actual contact trigger and qualified benefit of an assigned Boarding Leader.
0487|||Gerhard's compact close leaves Rafael to draw the next step.
0491|Understood. Now we need experience in a real battle. Thank you.||Rafael thanks Gerhard and recognizes that practice must follow instruction.
0507|||Keep the name substitution and the three exact stat names and their increase.
0511|Very well.||Gerhard accepts the request for a spoken lesson without judging the other route.
0515|Then I'll explain naval combat.||Gerhard starts the spoken lesson after Rafael chooses to listen.
0518|||Rafael's brief polite acceptance mirrors the other tutorial route.
0523|Let's start with naval gunfire. I'll show you a classic tactic called crossing the T.||Use the same gunfire lesson in both tutorial branches.
0527|Stay clear of their broadside. Pass ahead of the bow or behind the stern, then turn your broadside toward them and fire.|of their broadside.;turn your broadside;and fire.|Match the full training branch exactly so the same tactic means the same thing.
0530|||Rafael's tentative acknowledgment mirrors his response in the full course.
0535|Steer and let your gunners fire. To improve their fire, assign an officer with high Aim to a Gun Battery.|let your gunners fire.;To improve their fire,;high Aim;a Gun Battery.|Use the same division of responsibilities and exact labels as the other branch.
0539|Steer and adjust the sails as usual during naval battles.~Your ship fires automatically when an enemy ship comes within range.||Mirror the same two FE instructions and keep each complete sentence on its own panel.
0542|If you prefer boarding, go to the shipyard and refit a hold into Quarters.||Keep the same refit action and Quarters label in the spoken lesson.
0545|Hire plenty of sailors. Then assign an officer with high Swords to the Quarters as Boarding Leader. That will make boarding more effective.||Mirror the full course instructions and labels in the spoken lesson.
0549|||The duplicate panel gives the same usable assignment instruction as the full course.
0552|Boarding starts automatically when ships touch. Your Boarding Leader should make a difference.||Match the ordinary contact trigger and the qualified benefit in the full course.
0556|That's all. Is that clear?||Gerhard checks whether the lesson made sense at the end of the spoken route.
0560|Yes. Now we need experience in a real battle. Thank you.||Rafael acknowledges the answer and connects the lesson to real experience.
0566|||Keep the given-name substitution and the exact Wits increase.
0571|...I see. You'd rather learn aboard ship. Very well.||Gerhard accepts that Rafael prefers to learn in practice.
0577|||Keep the given-name substitution and the exact Luck increase for this choice.
"""


def context(ident):
    if ident.startswith("3114") or ident == "0218":
        return "Gerhard asks what Rafael expects from him. The player chooses between making the case for facing Vels and asking him to join for the fleet's sake."
    if ident.startswith("5298") or ident == "0417":
        return "Rafael can attempt the full training, hear Gerhard's explanation, or learn in practice aboard ship."
    number = int(ident)
    if number < 122:
        return "Janus follows a local lead and Claudio recognizes Gerhard's name. The crew asks the retired admiral to go back to sea before Claudio mentions Vels."
    if number < 218:
        return "Gerhard explains the mutiny, the crew he lost and his retirement. Rafael asks him for help."
    if number < 327:
        return "Rafael asks Gerhard to face Vels with them. On the follow-up visit he defends Gerhard's command and gives him a reason to come out of retirement."
    if number < 417:
        return "Rafael asks Gerhard to join for the fleet's future. He later asks Gerhard to teach them to fight."
    if number < 511:
        return "Gerhard challenges Rafael to finish the full training, teaches naval fire and boarding, and awards the three physical stat increases."
    if number < 571:
        return "Gerhard gives the spoken-only lesson. The same combat instructions finish with a Wits increase."
    return "Rafael chooses his own way of learning. Gerhard accepts that decision and Rafael's Luck rises."


def main():
    assert not OUTPUT.exists()
    packet, previous, parent_release = map(base.load, (SOURCE, PRIOR, parent.RELEASE))
    candidate = base.digest(parent.ROM)
    assert packet["candidate_sha256"] == parent_release["candidate_sha256"] == candidate
    assert base.digest(base.REGISTRY) == parent_release["registry_sha256"]
    old = {r["id"]: r for r in previous["records"] if r["block"] == 84}
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        ident, english, phrases, note = line.split("|")
        assert ident not in decisions
        decisions[ident] = english, tuple(phrases.split(";")) if phrases else (), note
    records = []
    for entry in packet["records"]:
        ident, selector = entry["id"], entry["source_selector"]
        row = old.pop(ident)
        key = ident.split("_CHOICE_")[-1] if selector is None else ident.rsplit("_R", 1)[-1]
        replacement, phrases, note = decisions.pop(key)
        pages = entry["installed_pages"]
        current = " ".join(logical(p["text"]) for p in pages)
        logical_pages = replacement.split("~") if "~" in replacement else [replacement] if replacement else [
            logical(p["text"]) for p in pages]
        english = " ".join(logical_pages)
        assert len(logical_pages) == len(pages)
        assert english.isascii() and logical(english) == english
        assert all(phrase in english for phrase in phrases)
        macro = TOKEN.findall(entry["Japanese"])
        assert TOKEN.findall(current) == TOKEN.findall(english) == macro
        changed = bool(replacement and replacement.replace("~", " ") != current or phrases)
        body = entry["source_body_hex"]
        prefix = "" if selector is None else f"{selector:02x}"
        kind = "typed-choice-label" if selector is None else "system-FE" if selector == 254 else "progressive"
        assert row["source_hex"] == prefix + body and row["kind"] == kind
        records.append(dict(id=ident, block=84, route=0, file_path=packet["file_path"], kind=kind,
            speaker=SPEAKERS[selector], context=context(key), source_meaning=row["source_meaning"],
            localization_note=note, english=english, previous_English=current, editable_FE_pages=logical_pages if selector == 254 else [],
            protected_phrases=list(phrases), decision="revision" if changed else "retention",
            finding="wording" if replacement and english != current else "wrap" if changed else "retention",
            source_selector=selector, native_command_word=entry["native_command_word"], native_slots=entry["source_slots"],
            source_hex=prefix + body, current_hex=prefix + pages[0]["body_hex"], Japanese=entry["Japanese"],
            source_reference=dict(file_path=packet["file_path"], block=84, offset=entry["source_offset"],
                command_offset=entry["source_command_offset"], archive_sha256=packet["clean_archive_sha256"],
                block_sha256=packet["clean_block_sha256"], exact_hex=prefix + body),
            current_reference=dict(file_path=packet["file_path"], block=84, offset=pages[0]["body_offset"],
                command_offset=pages[0]["command_offset"], archive_sha256=packet["current_archive_sha256"],
                block_sha256=packet["current_block_sha256"], exact_hex=prefix + pages[0]["body_hex"],
                installed_pages=pages), review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(records) == 131 and not old and not decisions
    assert sum(r["kind"] == "typed-choice-label" for r in records) == 5
    assert sum(len(r["editable_FE_pages"]) == 2 for r in records) == 2
    findings = dict(Counter(r["finding"] for r in records))
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), status="Contextual review complete. Native formatting and release pending.",
        records=records, findings=findings, previous_sha256=candidate, previous_registry_sha256=parent_release["registry_sha256"],
        source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)}, new_editorial_credit=0))
    print(f"Reviewed {len(records)} source records. {findings}")


if __name__ == "__main__":
    main()
