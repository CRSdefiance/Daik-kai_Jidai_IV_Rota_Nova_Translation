"""Review Maria's naval victory, Manuel's poem, and Aziza's mutiny."""

from collections import Counter
from inspect import getsource
from pathlib import Path

from scripts import pair_hodram_opening_20261122 as pairing
from scripts import register_hodram_B311_B324_20261122 as build
from scripts.source_locked_derivation_v5118 import checked_text


base, native = build.base, build.native
ARCHIVE = "/data/SC3.DK4"
CENSUS = Path("work/story_source_coverage_20261110_SC3_v17/coverage.json")
HISTORICAL = Path("translations/maria301_integrated_final_review_v1.json")
ROOT = Path("work/analysis/maria_B18_B20_followup_20261122")
PACKET = ROOT / "paired_source_registered_candidate.json"
DRAFT = ROOT / "contextual_decisions_v1.json"
LAYOUT = ROOT / "format_preflight_v1.json"
CONTEXTS = {
    18: "Maria's victory prompts Xien's praise. Manuel mourns those who fell and recites a poem on the sea and motherhood. Jam's celebration gives Xien a brief dry aside before Manuel returns to his original thought.",
    19: "Aziza's repeated losses bring the crew to mutiny. Maria's party intervenes, pays for her release, and hears why her father's blade mattered. Aziza decides to give up piracy, and Maria invites her aboard.",
    20: "Separate defeat and withdrawal outcomes preserve Aziza's two distinct threats and Maria's two short responses.",
}
DECISIONS = {
    18: """
5||Maria registers the victory in a composed voice before Xien comments on her performance.
9|You're getting the hang of commanding a fleet in battle.|Xien explicitly praises her handling of fleet combat, which is what Maria credits him for in reply.
13||Maria credits Xien directly and warmly. The short answer has the right modesty.
17|Heh. What are you talking about? I hardly have anything left to teach you.|Xien's amused dismissal leads into praise that she has almost nothing left to learn from him. Keep his measured confidence without the archaic cadence.
21|So many lives lost at sea... Or maybe I should say they've gone back to the sea, their mother...|Manuel uses an image of people scattered on the sea and then changes his terms to describe a return to a mother. This anticipates the poem.
25||Maria answers with his name while he grieves. Let the silence follow her address.
29|Let's offer some comfort to the souls of the fallen.|He proposes comforting the souls of the dead. This invites the poem and gives the act more purpose than a general statement of respect.
32||The question marker is Maria's puzzled reaction before she knows what Manuel will do.
36||The verse opens the quotation, compares the sea with a mother, and hears her distant heartbeat in the returning waves. Its cadence and images work aloud.
39||The repeated opening keeps the verse recognizable. The next line reports a rumor about how the words can be expressed in some lands, without claiming a particular language.
43||The final verse completes the three-part refrain with a bond that lasts throughout life, then closes the quotation.
46|Well, Manuel... I didn't know you recited poetry.|Xien is surprised to hear Manuel reciting a poem. Let his slow recognition follow the last verse.
49|I never would have guessed... I thought all you cared about was ships.|Maria's tentative pause leads into the contrast with Manuel's usual focus on ships.
53||Xien's correction keeps the given-name substitution. The poetic streak conveys the original romantic sensibility and sets up his exception when Jam bursts in.
64||Jam's boisterous victory feast and cheer interrupt the reflective exchange. The burst supplies the joke's setup.
68||Xien's brief, wry exception refers to Jam. The timing and delivery already work.
75|...The sea takes everything in. I hope we can be that way, too.|Manuel returns to his image of the sea's capacity to receive everything and wishes for the same generosity in people.
78||Maria pauses at the end of his thought. Preserve the silent beat.
""",
    19: """
5|Damn it, we lost again... But next time, I'll...!|Aziza acknowledges another loss and starts a vow before the abrupt interruption. Her sudden realization cuts the vow short.
8||Angel plays on Aziza's claim that there will be a next time. The short two-beat threat works.
11||Snake's quiet, malicious laugh supports Angel's threat without a new statement.
15||Aziza immediately challenges the threat. The two short exclamations fit her anger.
19||Angel answers her challenge with a taunting question. The contraction suits him.
23|I'm saying there's nobody left here who'll take orders from you!|Angel spells out that nobody here will obey her anymore. Keep the rejection of her authority and his colloquial delivery.
26||Aziza calls the crew traitors after their refusal to obey. The sharp curse fits her voice.
29|Something's happening aboard that ship.|Maria sees the disturbance before she knows what the dispute is about. The plain alert keeps the ship explicit.
33|Something's wrong. Sounds like they're having it out.|Xien notices that the situation feels wrong and identifies an apparent quarrel without claiming to know its cause.
36||Maria asks the crew to bring the ship alongside. Her immediate decision and politeness both read clearly.
40|We've been losing every fight lately, and we haven't made a coin. You're going to answer for that.|Angel ties Aziza's responsibility to their recent losing streak and lack of earnings. The direct speech lets the accusation build.
44|Answer for it...?|Aziza repeats the charge of responsibility in disbelief before Dandy brings up the pursuit.
48||Dandy asks why Aziza keeps pursuing the player's company. Keep the company substitution and persistent pursuit.
52|Heh. There's a reason you can't tell the rest of us, isn't there?|Snake presses Aziza on her private motive. The question remains a taunt and the tag belongs with it.
55||Aziza is shocked before Snake names the blade. The punctuation carries the interruption.
59|You only want to get the Bloodstained Shamshir back from FO. It was your old man's, wasn't it?|Snake reveals the motive and the blade's origin to the group. Keep the company substitution and his derisive way of referring to her father.
63|That's... that's not why...|Aziza tries to deny the accusation and falters. Keep her hesitation.
67||Angel's accusation leads straight into a threat. The three beats retain Aziza's decline, the money motive, and the coming attack.
71|...At this rate, they'll kill her.|Maria concludes that Aziza is in mortal danger if the confrontation continues. The pause gives weight to her decision.
74|But this isn't the sort of thing outsiders should meddle in...|Xien objects to a third party getting involved. His unfinished warning leaves room for Al to intervene.
77||Al volunteers tersely before Maria calls out to him.
81||Maria calls Al's name immediately in surprise.
85|Huh? Butt out. This has nothing to do with you!|Snake challenges a newcomer and tells him to stay out in a blunt voice.
88|...Don't get ahead of yourselves, small fry.|Al rebukes the low-ranking pirates for getting carried away. His pause and dismissive address distinguish him from Snake.
92|Stay out of it! You know what? Get rid of both of them. Him and Aziza!|Angel moves from rebuffing Al to ordering both of them attacked. Keep the escalation and both targets explicit.
96||Yukihisa offers to fight alongside Al. His measured promise also conveys respect without putting a new title in his mouth.
100|Count me in! Any man who'll only fight when he's got the numbers is pathetic!|Cristina volunteers and condemns men who rely on numbers. Keep her scorn and the reference to numerical advantage.
103|Woo-hoo! Come on, I'll take you on!|Jam's gleeful challenge keeps his loud, self-assured entry into the fight.
107||Al's brief challenge names the pirates and calls them forward. His words already fit the immediacy.
110||Aziza is bewildered at being defended by people she was just fighting. The trailing thought preserves the emotional reversal.
114|D-damn it, we're outmatched! Why are they sticking their necks out for Aziza?|Angel stammers when the odds turn and cannot understand why they are taking Aziza's side so strongly.
118||Maria gets everyone's attention decisively before confronting the pirates herself.
122||Snake asks whether Maria is there to rescue Aziza as well. The wording picks up the intervention already under way.
126||Maria confirms that and threatens consequences if they harm Aziza. The understated delivery suits her authority in this turn.
130||Aziza recognizes Maria and says her full live name. Preserve both substitutions and the pause.
134|...Doesn't look like we're getting away.|Dandy assesses that they will likely be unable to escape. He then shifts to bargaining.
138|I can pay you something if you let her go without a fuss.|Maria offers payment if they release Aziza peacefully. The condition remains explicit and the amount is still open.
141|What if we ask for a million? That's how badly we want to get even with her.|Dandy demands exactly one million and uses the size of the grudge to justify it. The reply keeps the provocation.
144|...You've got to be kidding!|Al reacts to the exorbitant demand with anger and disbelief before Maria asks him to stand down.
148||Maria uses Al's name and asks him to stand down because Aziza's safety comes first. The tradeoff is already explicit.
151||Aziza is stunned that someone would spend that much to save her. The two pauses carry her disbelief.
156||Maria checks that the pirates are satisfied and then calls Aziza over. Her address remains polite without a new rank.
159||Aziza hesitates in silence as she is released.
163||Angel says their business is finished and leaves abruptly. The short farewell suits him.
169|I never thought my own crew would turn on me. Look how far I've fallen... Anyway, why did you save me?|Aziza begins in disbelief, sees how far she has fallen, and turns the conversation to why Maria helped her.
173|I remember what happened at that tavern. I've been curious about you ever since.|Maria recalls a specific earlier meeting and dates her interest to it. The wording avoids adding a motive that she has not yet explained.
176|Something's been on my mind... Why would someone of your ability stoop to piracy?|Yukihisa asks why someone he respects chose what he calls a fall into piracy. His choice of verb sets up Aziza's answer.
180||Aziza disputes the compliment and the premise that she fell into piracy. The repetition of pirate underscores that this is her family background.
184||Xien gives a brief sign of interest and lets Aziza continue.
188|Those men were my father's crew. I grew up watching them. That's how I learned to handle a sword and live as a pirate.|Aziza learned by watching and copying during childhood. The account keeps her father's crew, swordsmanship, and the trade without the stiff narration.
191|And your father now...?|Maria asks after his fate indirectly. The unfinished question fits her delicacy as Aziza prepares to explain.
195|He died in an accident. That sword was his most prized possession. It disappeared with him...|Aziza describes the accident and the blade she associates with her father. The final sentence keeps their disappearance together.
199||Al names the Bloodstained Shamshir as he realizes which sword she means. The trailing delivery fits the revelation.
202||Aziza wanted to be as great a pirate as her father and imitated everything he did. The line leads directly to why the sword mattered.
206||When Aziza heard they had the sword, she wanted it back at any cost. Her unfinished conditional invites Maria's reply.
209||Maria repeats Aziza's unfinished condition as a question. Their phrasing matches.
213|I'd have something to show I was getting closer to being like him... Heh. But you know what?|Aziza recalls what she once thought the blade would prove, then laughs quietly before changing the subject toward her present realization.
217|Turns out I didn't really want to be a great pirate. I just wanted something to remember my father by...|Aziza distinguishes her stated ambition from what she now recognizes as her true motive. The second sentence carries the personal admission.
220||Aziza explains why she thinks the crew abandoned her. The existing wording keeps the distinction between her own priorities and the crew's profit.
224|...Do you still want to be a pirate?|Al asks directly whether she has any lingering wish to stay in piracy. His short question gives Aziza room to answer.
228||Aziza says her real pursuit was her father and resolves to give up piracy. The parallel sentences make the connection clear.
232||Al addresses Maria by her role and leaves the invitation unspoken.
236|I know, Al. That's what I had in mind when I saved her. People with her kind of ability are rare. Will you come with us?|Maria understands Al's cue, explains why she acted, and directly invites Aziza to join. Keep the shift from third-person explanation to the invitation.
239|Thanks... If you'll take me aboard, I'll give it everything I've got. You saved my life, after all.|Aziza's hesitant thanks becomes a plain promise to put in her full effort. The reason is her debt to the people who saved her.
243||Aziza asks them to use her given name. This follows Maria's more formal address without implying any new relationship.
246|All right. I'm looking forward to seeing what you can do.|Maria acknowledges the request and says she expects to see Aziza's contribution. The composed reply sounds welcoming and practical.
""",
    20: """
17|We're pulling out for now! I'll settle this next time!|Aziza orders the immediate retreat and promises to settle things at their next encounter.
20|You're all talk.|Maria's blunt dismissal responds to the threat just made. The short retort fits the moment.
26|Tch. I'll pull back for now, but I'll never bow to you! Remember the name Aziza Nurennahar!|Aziza uses a proud, emphatic refusal to submit in this version and announces her full approved name.
30||Maria observes that Aziza will not give up. The plain idiom catches both persistence and exasperation.
""",
}


def pair():
    source = checked_text(getsource(pairing.source_and_current), {
        "dict(route=1, file_path=ARCHIVE": "dict(route=3, file_path=ARCHIVE",
    })
    scope = pairing.source_and_current.__globals__ | {"ARCHIVE": ARCHIVE, "CENSUS": CENSUS}
    exec(compile(source, __file__ + "::registered-Maria-pairs", "exec"), scope)
    return scope["source_and_current"](build, DECISIONS)


def manuscript(packet):
    historical = {row["id"]: row for row in base.load(HISTORICAL)["records"]}
    labels = {}
    records = []
    for group in packet["groups"]:
        block = group["block"]
        decisions = {int(index): (wording, reason) for index, wording, reason in
                     (line.split("|", 2) for line in DECISIONS[block].strip().splitlines())}
        for pair in group["records"]:
            ident = pair["id"]
            proposed, reason = decisions.pop(int(ident.rsplit("R", 1)[1]))
            old = historical[ident]
            selector = pair["selector"]
            prefix = f"{selector:02x}"
            assert old["file_path"] == ARCHIVE and all(old["review"].values())
            assert pair["native_command_word"] == 0x4000 and pair["source_reference"]["offset"] == old["source_reference"]["offset"]
            assert prefix + pair["source_reference"]["exact_body_hex"] == old["source_hex"]
            assert labels.setdefault(selector, old["speaker"]) == old["speaker"]
            current = " ".join(pair["current_English"].split())
            revision = bool(proposed)
            assert not revision or proposed != current, (ident, proposed)
            english = proposed or current
            records.append(pair | dict(kind="progressive", route=3, speaker=old["speaker"],
                native_slots=[], source_selector=selector, source_hex=old["source_hex"],
                current_hex=prefix + pair["current_reference"]["exact_body_hex"],
                previous_English=current, english=english, protected_phrases=[],
                context=CONTEXTS[block], source_meaning=reason, localization_note=reason,
                decision="revision" if revision else "retention",
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
        assert not decisions
    assert len(records) == 88 and all(isinstance(label, str) and label for label in labels.values())
    return records, labels


def preflight(records):
    stage = build.writer
    planner = stage.engine.assemble({}).__globals__["plan_progressive"]
    output = {}
    for row in records:
        if row["decision"] == "retention":
            continue
        old, jp = (bytes.fromhex(row[key])[1:] for key in ("current_hex", "source_hex"))
        try:
            _, output[row["id"]] = planner(row, row["source_selector"], old, jp)
        except (AssertionError, ValueError) as error:
            raise ValueError(row["id"]) from error
    return output


def main():
    assert not any(path.exists() for path in (PACKET, DRAFT, LAYOUT))
    packet = pair()
    records, labels = manuscript(packet)
    plans = preflight(records)
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET, packet)
    base.save(DRAFT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(PACKET), source_packet_sha256=base.digest(PACKET),
        prior_review=str(HISTORICAL), prior_review_sha256=base.digest(HISTORICAL),
        records=records, current_names_and_roles=labels, new_editorial_credit=0,
        status="Context and prose complete. Fresh native, visual, focused and release gates pending."))
    base.save(LAYOUT, dict(candidate_sha256=packet["candidate_sha256"],
        draft_sha256=base.digest(DRAFT), plans=plans, gameplay_observed=False))
    print(dict(Counter(row["decision"] for row in records)))
    print(f"{len(plans)} preliminary wraps passed. {len(labels)} existing name and role bindings retained.")


FINAL_DRAFT = ROOT / "contextual_decisions_v2.json"
FINAL_LAYOUT = ROOT / "format_preflight_v2.json"
VISUAL_REFINEMENTS = {
    "DK4_MES_B19_R0005": ("Damn it, we lost again... But next time... Huh?!", ["next time..."],
        "Restore the audible gasp as Aziza realizes what is happening. Angel immediately picks up and mocks the words 'next time'."),
    "DK4_MES_B19_R0195": ("He died in an accident. He treasured that sword. It disappeared with him...", [],
        "Preserve the accident, his attachment to the sword, and their disappearance together. The Japanese gives no superlative."),
}


def refine():
    assert not FINAL_DRAFT.exists() and not FINAL_LAYOUT.exists()
    original, earlier_layout = map(base.load, (DRAFT, LAYOUT))
    assert earlier_layout["draft_sha256"] == base.digest(DRAFT)
    records = {row["id"]: row for row in original["records"]}
    for ident, (wording, phrases, reason) in VISUAL_REFINEMENTS.items():
        row = records[ident]
        assert row["decision"] == "revision" and row["english"] != wording
        row.update(english=wording, protected_phrases=phrases, layout_review_refinement=reason,
                   localization_note=reason, previous_draft_comparison_sha256=base.digest(DRAFT))
    fresh = preflight([records[ident] for ident in VISUAL_REFINEMENTS])
    plans = earlier_layout["plans"] | fresh
    assert len(plans) == 43 and all(plans[ident]["expected_native_pages"] == 1 for ident in fresh)
    base.save(FINAL_DRAFT, original | dict(prior_draft=str(DRAFT), prior_draft_sha256=base.digest(DRAFT)))
    base.save(FINAL_LAYOUT, earlier_layout | dict(draft_sha256=base.digest(FINAL_DRAFT), plans=plans,
        prior_layout=str(LAYOUT), newly_planned_ids=sorted(fresh)))
    print(f"Replanned {len(fresh)} refinements after the visual review. The other 41 plans carry forward.")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--refine", action="store_true")
    (refine if parser.parse_args().refine else main)()
