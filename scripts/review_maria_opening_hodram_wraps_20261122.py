"""Review Maria's opening confrontations and apply three qualified Hodram wraps."""

from collections import Counter
from inspect import getsource
from pathlib import Path

from scripts import register_maria_B18_B20_20261122 as parent
from scripts import review_maria_B18_B20_20261122 as maria
from scripts import register_hodram_B311_B324_20261122 as hodram
from scripts.source_locked_derivation_v5118 import checked_text


base, native = parent.base, parent.native
engine = parent.writer.engine
ROOT = Path("work/analysis/maria_opening_hodram_wraps_20261122")
PACKET, DRAFT, LAYOUT = [ROOT/name for name in (
    "paired_source_registered_candidate.json", "contextual_decisions_v1.json", "format_preflight_v1.json")]
FOLLOWUPS = hodram.writer.paired.ROOT/"B312_B318_B324_wrap_followup_v1.json"
HODRAM_BLOCKS = (312, 318, 324)
CONTEXTS = (
    "Maria tests whether the great powers use the Proof of Conquest to justify domination. Her advisers consider the alternative, and she decides to find it first.",
    "Yukihisa studies the Muramasa blade and describes its unsettling light.",
    "The former owner recognizes the returned object by its unchanged dull gleam. He is astonished nobody found it.",
    "Kurushima challenges Maria. Yukihisa calls out his treatment of civilians, and Maria answers Kurushima's crude proposition before he orders the attack.",
    "Maria accuses Escante of oppressing the New World. He reveals why he stocked weapons, tries to win her over, and orders a charge. Hodram arrives to join as a common enemy of Escante.",
    "Aziza rallies her crew and gives Snake, Angel and Dandy their jobs. She taunts Maria's fleet from the other side. Maria and Xien confer before preparing for battle.",
    "Alternative Aziza encounters reopen the conflict. The challenge and hostile return lines preserve their different tones.",
    "Maria corners the ship thief Yuris. He objects to the nickname and cites his birth. She answers with a dry warning about being sent to Batavia.",
    "Maria identifies Jacob, mocks the black-market trader's piracy and warns him. He replies with contempt.",
    "Maria calls Gabriel to account for violating the agreement. He taunts her back and accepts a fight.",
    "The opponent makes an animal-like cackle and repeats his threat to sink Maria. Maria's dry aside sits between those exclamations.",
    "Maria challenges Hernan Berio despite his fleet. He boasts that opponents usually flee and welcomes the chance to fight.",
    "In alternate aftermath exchanges, Lil angrily criticizes Clifford or bristles at being rescued. Camille gives thanks or chides her. Maria downplays the favor and warns of danger.",
    "Maria withdraws in this branch. Lil goes from anger or embarrassment to direct thanks or determination. Camille and Maria respond without humiliating her.",
    "Lil wonders whether her help mattered, Maria thanks her sincerely, and Lil says that pays off the earlier favor.",
    "This block has no dialogue records.",
    "Maria praises Hodram's timely help. He delays thanks until Escante has been fully defeated and warns her to stay alert when he leaves.",
    "Hodram calls the retreat, checks on Maria, and owns the mistake. She thanks him for coming, and he says to wait for a decisive victory over Escante.",
)
# Each row records the proposed paragraph, if changed, and the source/context decision.
DECISIONS = {
    0: """
4||Maria asks why the treasure matters so much that the great powers want it. The existing question gives her curiosity a clear object.
8|I don't know. It may be nothing more than a way for the Western powers to justify ruling the world.|Xien gives a tentative theory about legitimizing their existing domination. Keep it speculative and conversational.
12|You think they made up the Proof of Conquest?|Maria asks whether the story itself is fabricated. Use the approved full term when she names it.
23||The ally protests that the powers cannot fabricate this for their own ends. The forceful plain wording fits the response.
30||Yukihisa makes the counterargument that an invented symbol should be easy for its makers to claim. The conditional remains clear.
39||Yukihisa turns the lack of a discovery into evidence for a genuine Proof. His inference is tentative.
44|...I see.|The speaker gives a quiet sign of understanding before the alternate argument. The opening hesitation belongs with the response.
48||The alternate speaker draws the same tentative inference as Yukihisa in a slightly more formal cadence.
54||Maria pauses to take in the argument before deciding what to do.
58|Either way, we have to find the Proof before they get their hands on it. We can't let the great powers keep doing as they please.|Maria links the race to keep it out of their hands with resisting their continued domination.
61||Xien agrees with her decision in one beat.
""",
    1: """
5|So this is... the cursed blade Muramasa...|Yukihisa falters at seeing the named sword. The pause preserves the quiet recognition.
9||The glow feels eerie and almost draws him in. The measured two sentences convey that fascination.
""",
    2: """
5||The owner recognizes the object's same dull gleam from before the separation. Its texture and his certainty stay intact.
9|I can hardly believe no one else picked it up...|The speaker marvels that nobody picked it up in the meantime. His trailing delivery follows the physical recognition.
""",
    3: """
5|Well, FI! This is the day we settle things!|Kurushima directly challenges Maria using the original given-name substitution. The abrasive familiarity needs no invented relationship.
15|Kurushima! Stop this madness!|Yukihisa directly condemns the conduct before explaining why. Keep his stern voice in everyday English.
18||Kurushima calls a samurai who sides with foreigners a disgrace. The insult already retains both the status and accusation from source.
22|You raid the mainland coast and rob people who can't fight back. Is that how a proud samurai behaves?|Yukihisa names the actual coastal raids and defenseless victims, then turns the accusation about samurai honor back on Kurushima.
26||Kurushima mocks the reprimand and says he cannot stand that sort of character. The blunt shifts suit him.
32|Heh heh, FI! Agree to be mine and I might surrender without a fight. Yours is the only life I'll spare!|Kurushima offers to surrender himself if Maria becomes his woman. Only her life would be spared. Keep the crude condition and the original name substitution.
35||Maria names Kurushima and answers the crude proposition with a specific threat against his beard. The witty retort preserves her controlled anger.
39||Kurushima laughs before the sudden, drawn-out threat. The pause is warranted by the sharp shift.
""",
    4: """
5||Maria challenges Escante using the source's Conqueror address and demands freedom for the people he controls. No military title is supplied.
9|Ha ha ha! What's Maldonado been telling you? This wasn't what I planned at all... I expected Valdes, and I get a woman like you.|Escante blames his miscalculation on facing Maria instead of Valdes. His dismissive surprise leads to her question.
12||Maria recognizes the name and cautiously asks whether it is the officer from his country. The question leaves her uncertainty intact.
15||Escante calls his own earlier generosity softhearted. His contempt sets up the complaint about the wealth.
19||Maria's puzzled pause gives Escante room to explain.
23|The whole New World, vast as it is, and all this time I let my homeland bleed it for money. What a waste!|Escante regrets yielding the vast territory to his homeland as a source of funds. The irritable assessment keeps the focus on what he let the homeland take.
26|So that's why you've been buying up weapons. You mean to break away from your homeland.|Maria connects the sustained weapons purchases with Escante's intended independence. The inference anticipates his confirmation.
30||Escante expects her opposition to colonial rule to make his plan appealing. The boast and appeal already work together.
33||His declaration promises a country to New World residents and praises his own bold idea. Retain both sides of the claim.
37|How selfish. Only a villain would try to justify such greed.|Maria rejects his self-interest as villainous. The direct accusation follows his self-congratulation without adding a new principle.
41|You thought I'd go along with that nonsense? You've got me all wrong.|Maria is offended that he underestimated her enough to expect her support. Keep her two firm beats.
45|Hmph... No point talking anymore. If a child won't listen, it's time for a spanking! All ships, charge!|Escante condescends to Maria before ordering a charge. The threat and the fleet order must both stay.
97|Looks like I've arrived just in time.|Hodram remarks on the lucky timing as he appears during escalation.
101||Maria's surprise precedes his explanation. Keep it nonverbal.
105|He's my enemy too. Forgive me for joining the fight unasked.|Hodram says Escante is also his enemy and announces that he is joining despite not being invited. Keep his direct courtesy.
""",
    5: """
5||Aziza identifies the fleet by its original company substitution and accuses it of encroaching on her waters. Her pointed opening works.
8||The short crowd cheer answers Aziza's identification without extra words.
12||Aziza calls all hands to battle stations and orders Snake to command. Both orders already come through clearly.
15||Snake gives a short affirmative reply before Aziza assigns the maneuver.
19|Angel! Bring us around to their starboard quarter!|Aziza orders the approach to the enemy's right rear. Starboard quarter is the matching position and suits her concise deck command.
22||Angel's exuberant acceptance fits the abrupt naval order. He adds confidence without discussing a different task.
25||Aziza asks Dandy about readiness to fire, following her assignment to Angel.
28|Ready to fire.|Dandy confirms the gunnery preparations. The terse reply answers the question directly.
32||Aziza voices her excitement before addressing the crew roughly. Their cheer follows naturally.
35|Time to see who deserves to rule these waters, me or FO!|Aziza challenges the named fleet directly. The original substitution stays in order, and the comparison can be said aloud in one breath.
38||The second cheer answers Aziza's battle challenge.
42||Maria says she has not heard of this particular pirate. Keep her composed response to Aziza's spectacle.
46||Xien calls a woman pirate unusual and wonders what led her to piracy. The hesitation leaves the explanation unknown.
49|Whatever her reasons, we can't let pirates run wild. Everyone, get ready for battle!|Maria refuses to leave marauding pirates alone regardless of motive. Her command ends the brief conference.
""",
    6: """
42||Aziza announces that she has found them at last and vows to settle things this time. The threat is already spoken naturally.
45||The crew answers her discovery with a shout.
51||Aziza mocks the fleet for returning, uses its original name substitution and threatens to sink it. The existing taunt preserves all three.
""",
    7: """
4||Maria finally identifies Yuris by his nickname. The dry short line sets up his objection.
7|I resent such a cheap nickname. I'll have you know I come from one of the finest noble families.|Yuris takes offense and insists on his high-born background. The self-important turn fits his objection.
10||Maria needles him about his sensitivity, then says he can lose the nickname after being sent to Batavia. Her dry sequence works.
""",
    8: """
5||Maria identifies Jacob by his approved name, mocks the black-market trader for playing pirate and warns him against overconfidence. The sarcasm carries across the lines.
9||Jacob bristles at being lectured by Maria. His contempt answers her mocking warning.
""",
    9: """
4|You're Gabriel. You've been doing as you please and breaking the agreement. It's time you stopped.|Maria singles Gabriel out for acting unilaterally and breaking the agreement. Her demand stays controlled.
8|Doing as I please, am I? Agreements are made to be broken. Watch your mouth.|Gabriel throws Maria's own wording back at her before dismissing the agreement and warning her.
12||Maria returns his warning and asks if force is the only language he understands. The calm challenge and idiom fit.
16||Gabriel welcomes the challenge. The invitation to fight answers Maria's question.
""",
    10: """
5||The distinct high cackle precedes the taunt asking who Maria is and whether she wants to die.
8||Maria's dry uncertainty about whether her opponent is even a person answers the bizarre vocalization.
12||Keep the different cackle and all three repeated threats. The repetition is the point of the voice.
""",
    11: """
4||Maria names the pirate and his origin, then challenges his vanity about commanding a fleet. Her phrasing keeps the warning specific to him.
7|Been a while since anyone stood up to me. These days they take one look and sail off at full speed. Being this good gets old.|Hernan contrasts the unusual challenge with ships fleeing at full speed. The last boast keeps his mock complaint about being too strong.
10|Ah, well. I've been bored long enough. I'll give you a fight!|He welcomes the chance to relieve his boredom. The abrupt challenge follows his boasting.
""",
    12: """
5||Lil blames Clifford and insults the brute he sent after her. Her compressed angry delivery sounds right in the aftermath.
9|You've got your fire back. Even your face looks different from a moment ago.|Maria remarks on Lil's recovered spirit and the visible change in her expression.
12||Lil's short stammer is a surprised response to Maria's observation.
16|Come on, Lil. Thank her. You really did save us. Thank you so much.|Camille asks Lil to thank Maria outright, then voices his own gratitude. Both addresses stay distinct.
27|It's all right. They may still be nearby, so keep your guard up.|Maria brushes off the need for thanks and warns that danger may remain. Keep her calm and attentive.
31||Lil's silence belongs to the aftermath. It makes space for her reluctance or reflection.
37|There I go, getting rescued again... Ugh, I hate that.|Lil is frustrated that she needed help again. Her irritation is directed at the situation, not the person who helped.
40||Camille chides Lil by name when she dwells on being rescued.
44|It's all right. They may still be nearby, so keep your guard up.|The exact same Japanese reassurance and nearby-danger warning recur in this branch. Match Maria's wording.
48||Lil vows to repay the favor. The promise answers the rescue and keeps her determination.
""",
    13: """
4|Ugh... We'd better pull back. Retreat!|Maria recognizes the need to withdraw and then gives the order. The hesitant judgment and the urgent command both stay.
7||Lil is furious at losing to a man she despises. Her blunt phrasing fits her voice.
10|Lil... We're lucky just to be alive this time. Thank you. You really saved us.|Camille answers her anger with relief at surviving, then thanks Maria sincerely.
19|It's all right. They may still be nearby, so keep your guard up.|Maria uses the same Japanese reassurance and warning as the alternate B12 exchange. Keep the source-identical responses consistent.
23||The pause gives Lil time to respond after the warning.
28|Thanks for saving us... It really was close this time.|Lil thanks Maria directly and acknowledges how dangerous this occasion was.
31|It's all right. They may still be nearby. Be careful, okay?|This time Maria ends with the softer warning to take care. Keep it distinct from her earlier order to keep watch.
35||Lil is embarrassed at repeatedly needing rescue and vows to get stronger. The existing voice has enough indignation and hope.
39||Camille encourages Lil's determination by name.
43||Maria laughs warmly and admires Lil's positive spirit. Keep her familiar, encouraging short answer.
""",
    14: """
5|That's our Admiral FA! I guess you didn't need me to back you up, huh?|Lil praises the admiral and wonders if the support she offered was needed. Preserve the surname substitution and the light question.
9|Oh, we needed you. Thanks, really.|Maria directly denies that Lil's help was unnecessary and thanks her sincerely.
12||Lil says that helping pays off the earlier favor, then gives a playful goodbye. The light tag suits her.
""",
    16: """
5||Maria praises both the timing and Hodram's performance. Her short appreciation suits the transition from battle.
17|Thank me when we've finished off Escante. I'm pulling out for now. Stay on your guard.|Hodram asks her to save her thanks until Escante is decisively defeated and says he is leaving. Keep who is withdrawing explicit.
""",
    17: """
4||Hodram curses and calls an immediate retreat. The urgent instruction is already clear.
10||Hodram's clipped question checks whether Maria is all right after the retreat.
14|I'm... still alive, at least.|Maria hesitates before confirming she survived. Her dry understatement fits Hodram's urgent check.
18|I got the tactics wrong...|Hodram blames his own tactical judgment. The admission should sound like a man taking responsibility aloud.
22|I wouldn't say that. Thanks for coming to help, all the same.|Maria rejects the blame and then thanks him for intervening. Her second sentence answers the events they have just survived.
34|Thank me when we've finished off Escante. I'm heading out now. Stay on your guard.|This alternate exchange repeats the call to hold thanks for a decisive victory and explicitly has Hodram leaving. Keep the warning as his farewell.
""",
}


def maria_packet():
    source = checked_text(getsource(maria.pairing.source_and_current), {
        "dict(route=1, file_path=ARCHIVE": "dict(route=3, file_path=ARCHIVE",
    })
    scope = maria.pairing.source_and_current.__globals__ | {"ARCHIVE":maria.ARCHIVE, "CENSUS":maria.CENSUS}
    exec(compile(source,__file__+"::Maria-opening-pack","exec"),scope)
    return scope["source_and_current"](parent,range(18))


def localized(packet):
    history = {row["id"]:row for row in base.load(maria.HISTORICAL)["records"]}
    records, labels = [], {}
    for group in packet["groups"]:
        block = group["block"]
        decisions = {int(index):(wording,note) for index,wording,note in
                     (line.split("|",2) for line in DECISIONS.get(block,"").strip().splitlines())}
        for pair in group["records"]:
            ident, selector = pair["id"],pair["selector"]
            previous = history[ident]
            proposed, note = decisions.pop(int(ident.rsplit("R",1)[1]))
            old = " ".join(pair["current_English"].split())
            source = f"{selector:02x}"+pair["source_reference"]["exact_body_hex"]
            installed = f"{selector:02x}"+pair["current_reference"]["exact_body_hex"]
            assert previous["file_path"] == maria.ARCHIVE and previous["source_hex"] == source
            assert previous["source_reference"]["offset"] == pair["source_reference"]["offset"]
            assert all(previous["review"].values()) and pair["native_command_word"] == 0x4000
            assert labels.setdefault(selector,previous["speaker"]) == previous["speaker"]
            assert not proposed or proposed != old,(ident,proposed)
            records.append(pair | dict(kind="progressive",route=3,speaker=previous["speaker"],native_slots=[],
                source_selector=selector,source_hex=source,current_hex=installed,previous_English=old,english=proposed or old,
                protected_phrases=[],context=CONTEXTS[block],source_meaning=note,localization_note=note,
                decision="revision" if proposed else "retention",change_class="wording" if proposed else "retention",
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
        assert not decisions
    return records, labels


def wrap_followups(packet):
    rows = {row["id"]:row for row in base.load(hodram.REVIEW)["records"] if row["block"] in HODRAM_BLOCKS}
    proposals = {row["id"]:row for row in base.load(FOLLOWUPS)["records"]}
    records, approved = [], {}
    for group in packet["groups"]:
        for pair in group["records"]:
            ident = pair["id"]
            previous = rows.pop(ident)
            assert previous["source_reference"] == pair["source_reference"] and all(previous["review"].values())
            ref = previous["registered_reference"]
            prefix = f'{pair["selector"]:02x}' if pair["native_command_word"] == 0x4000 else ""
            old = prefix + pair["current_reference"]["exact_body_hex"]
            assert old == ref["exact_stored_hex"]
            for k in ("archive_sha256","block_sha256","command_offset","offset"):
                assert ref[k] == pair["current_reference"][k]
            follow = proposals.pop(ident,None)
            if follow:
                assert follow["registered_reference"] == ref and follow["current_English"] == previous["english"]
                assert follow["source_hex"] == previous["source_hex"]
                approved[ident] = follow["native_layout_preflight"]
            english = follow["proposed_English"] if follow else previous["english"]
            records.append(pair | dict(kind=previous["kind"],route=1,speaker=previous["speaker"],
                native_slots=previous["native_slots"],source_selector=previous["source_selector"],
                source_hex=previous["source_hex"],current_hex=old,previous_English=previous["english"],
                english=english,protected_phrases=follow["protected_phrases"] if follow else [],
                context=previous["context"],source_meaning=previous["source_meaning"],
                localization_note=follow["reason"] if follow else previous["localization_note"],
                decision="revision" if follow else "retention",
                change_class=("wrap-only" if english == previous["english"] else "wording") if follow else "retention",
                previous_registered_reference=ref,decision_carried=not follow,
                review=previous["review"] | {"formatting":not bool(follow)}))
    assert not rows and not proposals and len(approved) == 3 and len(records) == 70
    return records, approved


def main():
    assert not any(path.exists() for path in (PACKET,DRAFT,LAYOUT))
    starter = maria_packet()
    first,labels = localized(starter)
    hours = maria.pairing.source_and_current(parent,HODRAM_BLOCKS)
    second,approved = wrap_followups(hours)
    assert {g["block"] for g in starter["groups"] if not g["records"]} == {15}
    records = first+second
    plans = maria.preflight(records)
    assert all(plans[id]["encoded_hex"] == plan["encoded_hex"] for id,plan in approved.items())
    assert len(plans) == sum(r["decision"]=="revision" for r in records)
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET,starter | dict(groups=[*hours["groups"],*(g for g in starter["groups"] if g["records"])],
                                  Hodram_source_census_sha256=hours["census_sha256"],no_dialogue_blocks={"SC3":[15]}))
    base.save(DRAFT,dict(translation_policy="natural-dialogue-v2",target_locale="en-US",
        source_packet=str(PACKET),source_packet_sha256=base.digest(PACKET),
        records=records,Maria_names_and_roles=labels,contextual_records_revisited=len(first)+len(approved),
        contextual_decisions_reused=len(second)-len(approved),new_editorial_credit=0,
        findings=dict(Counter(row["change_class"] for row in records)),
        evidence={str(path):base.digest(path) for path in (maria.HISTORICAL,hodram.REVIEW,FOLLOWUPS)},
        status="Contextual pass and preliminary native planning complete. Stored, visual and gameplay gates pending."))
    base.save(LAYOUT,dict(candidate_sha256=starter["candidate_sha256"],draft_sha256=base.digest(DRAFT),plans=plans))
    print("Maria",len(first),dict(Counter(row["decision"] for row in first)))
    print("Hodram",len(second),dict(Counter(row["change_class"] for row in second)))
    print(len(plans),"preliminary wraps passed.")


if __name__ == "__main__":
    main()

