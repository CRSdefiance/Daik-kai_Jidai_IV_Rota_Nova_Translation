"""Review both decisions and the complete Rafael–Pereira exchange in SC0 B60."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_north_sea_africa_20261121 as parent
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical
from scripts.stage_hodram_alexandria_tutorial_20261121 import plan_progressive


base, native = parent.base, parent.native
ROOT = parent.stage.review.ROOT / "spain_B60"
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v4.json"
PRIOR = Path("translations/rafael_B51_B60_contextual_final_review_v1.json")
BLOCKS = ((60,), (), (), ())

CONTEXTS = (
    "Pereira asks what Rafael found and explains his official position. He presses Rafael on who his real enemy is.",
    "Pereira tests Rafael's resolve against Spain, then hands him the key and asks what their agreement against Kuhn should accomplish.",
    "In the Kuhn-first plan, Rafael wants to test his company's strength before challenging Valdes. Pereira agrees to stay as Portugal's last line of defense.",
    "In the Europe-first plan, Rafael entrusts the region and Kuhn to Pereira, who invokes free competition and holds Rafael to his promise to defeat Valdes.",
    "Pereira ties control of the Spice Islands to global military power. He explains why he cannot risk an all-out fight with Kuhn and sends Rafael to face Valdes.",
)

# An empty replacement with named phrases retains the wording and tests a reflow.
DECISIONS = """
6|||Pereira's surprised call preserves Rafael's surname substitution.
17|||His blunt question uses Proof as the source does and leads to two different answers.
21|We found the key we need to look for the Proof of Conquest.|the key we need;look for;the Proof of Conquest.|Rafael reports finding a search key in this branch. He has not found the Proof itself.
25|||Pereira's brief acknowledgment leaves the alternative discovery to the other branch.
31|||Keep the promised Proof itself and East Asia in this distinct report.
35|||Pereira recognizes the real object after a brief inspection.
41|||The blunt invitation moves the meeting along.
44|I know I've said it before, but in my position I can't help you out in the open.|I've said it before,;in my position;out in the open.|Keep Pereira's impatience and public constraint in the same breath.
48|||Rafael's silence gives Pereira room to explain their shared interests.
53|But you and I both want to take down Kuhn and Spain. We've got the same enemies.|take down;Kuhn and Spain.;We've got the same enemies.|Pereira speaks plainly about a shared objective without offering formal help yet.
57||Isn't that reason enough?;Can't we;make an agreement;Kuhn and Spain together?|Keep both steps of Rafael's earnest proposal together.
62|||Pereira's clipped response challenges Rafael's assumption that the decision is simple.
66|||Rafael asks for the reason plainly before Pereira changes the question.
71|Then tell me straight. Who's your real enemy? Think hard before you answer.|tell me straight.;Who's your real enemy?;before you answer.|Let Pereira's direct questions sound spoken while retaining his insistence on thinking it through.
75|Huh? My real enemy...|My real enemy...|Rafael repeats the question's key words while trying to make sense of it.
99|Spain. They seized Portugal.||State the player's answer plainly and keep Portugal's seizure as the reason for naming Spain.
101|...I'm not sure.||Keep the pause and Rafael's willingness to admit uncertainty.
111|Well, well. You'd really take on Spain's Invincible Armada? Even Albuquerque's sided with them, you know.|take on;Spain's Invincible Armada?;sided with them,|Let Pereira test the consequences of Rafael's resolve. Keep Albuquerque's side and the full Armada name.
114|||Rafael's emphatic reply answers whether he really means it.
119||And if I refuse to help?;Would you still do it?|Pereira probes whether their commitment depends on him. Keep both questions whole.
123|Then we'll have to do it ourselves. However long it takes, we'll defeat Spain and rebuild Portugal.|Then we'll have to;do it ourselves.;However long it takes,;rebuild Portugal.|Keep Rafael's reluctant acceptance and the vow to prevail even without Pereira.
127|||Pereira lets the answer sit before deciding Rafael can be trusted.
131|||The abrupt turn makes sense once Pereira explains what he was testing.
135|||Rafael's wordless confusion sets up Pereira's explanation.
140|Too many hypocrites wave the flag when it suits them. Throw in with their kind and a dozen lives wouldn't be enough.|when it suits them.;Throw in with their kind;a dozen lives|Keep the attack on shallow patriotism and Pereira's colorful warning about trusting those men.
143||worrying over nothing.;You'll do just fine.|Pereira withdraws his doubt once Rafael shows conviction.
147|Come on! We'd better finish off Kuhn and get back to Portugal!|finish off Kuhn;back to Portugal!|Restore Pereira's reference to their homeland and his sudden urgency.
150|||Rafael's surprised address fits Pereira's swing from skepticism to resolve.
155|||Pereira's short offer puts the object at the center of the next beat.
160|||Rafael's question leaves the object unidentified until Pereira explains it.
165|They say this is the key that deciphers a Proof of Conquest map. Show me you're worthy of the Proof.|They say this is the key;a Proof of Conquest map.;Show me;worthy of the Proof.|Keep the hearsay, the key's purpose, and Pereira's challenge about the Proof.
169|||Claudio's surprised question sounds natural and lets Pereira dismiss the task of collecting.
173|Yeah. I'm not interested. Who's got time to collect all seven? It's yours now.|Who's got time;collect all seven?;It's yours now.|Keep Pereira's curt disinterest, the count of seven and the unconditional gift.
177|...All right. Then let's make our agreement against Kuhn, here and now.|make our agreement;against Kuhn,;here and now.|Once the gift is accepted, Rafael asks for an explicit agreement against their common target.
182|What do you propose?||Keep Pereira's terse invitation to choose their next move.
188|||The direct proposal matches the first original plan to defeat Kuhn together.
190|||The second choice gives Pereira responsibility for Kuhn and preserves its distinct strategy.
201||work together;defeat Kuhn first.|Rafael spells out the cooperative option in his own words.
205|Cover our rear, eh? Even I'd have a hell of a time taking him on alone.|Cover our rear, eh?;have a hell of a time;taking him on alone.|Pereira hears the strategy and admits that even he would have trouble facing Kuhn by himself.
208|As Spain's king, I'd do all I could to strip Portugal's royal family of its claim to the throne for good. We're running out of time.|As Spain's king,;do all I could;Portugal's royal family;claim to the throne for good.;We're running out of time.|Preserve Rafael's hypothetical and the urgency it explains. This speech repeats in the other strategy.
212|Taking down Kuhn would give us the strength to face Spain's Valdes on our own.|Taking down Kuhn;face Spain's Valdes;on our own.|Rafael explains why he wants this fight first and keeps the later confrontation independent.
217|||Pereira's incredulous repetition challenges Rafael's plan to go alone.
220|You're in charge of these waters, Pereira. You can't just walk away from your post.|in charge of these waters,;walk away from your post.|Rafael insists on Pereira's regional responsibility after Pereira doubts him.
225|What are you talking about? We're about to rebel against the king of Spain! To hell with my post!|What are you talking about?;the king of Spain!;To hell with my post!|Restore the direct challenge and the king. Keep Pereira's blunt rejection as a separate beat.
229|...If this plan fails, you'll lose your post as governor of Indochina for good.|If this plan fails,;governor of Indochina;for good.|Keep Rafael's specific warning about the governorship and its permanent loss.
234|Ha ha ha! Is that what you're getting at? I know that full well!|what you're getting at?;full well!|Pereira laughs at a risk he already understands before Rafael explains the larger responsibility.
238||If we aren't strong enough,;entrust Portugal's future to!|Keep Rafael's correction and his need for a person he can trust with the country's future.
242|||Pereira's wordless surprise gives Rafael room to explain why the region matters.
246|All Europe's powers want these Spice Islands. Hold on to them, and one day we can face Spain on equal terms.|these Spice Islands.;Hold on to them,;Spain on equal terms.|Use the established place name and preserve Rafael's argument that control can eventually let Portugal match Spain.
250|If you'll be Portugal's last line of defense, we can give this fight everything we've got.|last line of defense,;everything we've got.|Rafael asks Pereira to stand as Portugal's safeguard so his own crew can commit fully to the fight.
255|||Pereira's quiet chuckle registers the unexpected argument before his outburst.
259|Ha ha ha! You're a piece of work! I'll give you that!|You're a piece of work!;I'll give you that!|Let Pereira's laughter turn admiration into a grudging, affectionate compliment.
263|All right! I'm betting on you. Leave the rest to me!|I'm betting on you.;Leave the rest to me!|Pereira gives his assent and takes responsibility in short, confident phrases.
267|||Rafael answers with clear gratitude and trust.
273|||This branch opens with Pereira asking what Rafael means by leaving Kuhn to him.
277|||Rafael states that they will leave Southeast Asia immediately.
281|And then?||Pereira prompts Rafael to state his destination.
285||Spain's Valdes.|The order of destination and objective is natural in English. Keep Valdes attached to Spain.
289|Wait, what did you say?||Recover Pereira's startled interruption before Rafael explains the urgency.
293|As Spain's king, I'd do all I could to strip Portugal's royal family of its claim to the throne for good. We're running out of time.|As Spain's king,;do all I could;Portugal's royal family;claim to the throne for good.;We're running out of time.|Use the same hypothetical as the Kuhn-first branch. It explains the same urgency.
297||leaving Kuhn for later?|Pereira grants the premise, then asks what the immediate change of plan means for Kuhn.
301|No. You're the governor of Indochina. These waters are your responsibility, so I'm leaving it all to you.|governor of Indochina.;your responsibility,;leaving it all to you.|Rafael invokes Pereira's original title and regional remit before handing him responsibility.
306|Ah... So you want me to cover your rear.|cover your rear.|Keep the nautical strategy in Pereira's everyday voice.
309||With you protecting this sea,;with all our strength.|Rafael accepts the rear-guard plan and says the crew can concentrate on Valdes.
314|Ha! You really are something. So I'm already a piece on your board, am I?|You really are something.;a piece on your board,;am I?|Keep Pereira's amusement that he is already a piece in Rafael's strategy.
318||Leave it to me.;drive Kuhn out myself?|Pereira accepts, then tests whether Rafael really means to leave the consequences to him.
322|You've given me the key to the Proof of Conquest. I've got no problem letting you have the trading rights here.|the Proof of Conquest.;no problem;the trading rights here.|Rafael distinguishes the key he has received from the commercial rights he can give up.
327|Ha ha! Is that out of pity? Don't worry about me. You can take over Southeast Asia later, and me with it!|Is that out of pity?;take over Southeast Asia;and me with it!|Keep Pereira's swagger and explicit willingness to face Rafael as a competitor in the region.
330|||Rafael's stammer answers the unexpected permission to compete.
335|Business is supposed to be fair, right? Free competition and all that?|fair, right?;Free competition and all that?|Pereira needles Rafael with the principle of free competition. Keep the tag together.
338|||Rafael agrees but is still trying to qualify the answer.
343|Then make sure you take down Valdes. Got it?|take down Valdes.;Got it?|Keep this reciprocal promise in Pereira's direct voice.
346|||Rafael accepts without hesitation after Pereira makes the terms plain.
354|||Pereira's repetition shows growing belief in this particular crew.
362|||The pause gives Pereira time to change the perspective of the question.
366|Another question, FA. Who's the strongest power in the world right now?|Another question, FA.;Who's the strongest power;in the world right now?|Keep the surname substitution and give Pereira an easy transition to his new question.
370|Whichever company has the biggest trading network, right? Ours, maybe, or...|trading network, right?;Ours, maybe, or...|Restore Claudio's casual certainty and his unfinished guess. He is thinking about commerce.
374|No. I mean, if someone set out to conquer the world, who'd have the best shot?|to conquer the world,;the best shot?|Let Pereira state what he means quickly after dismissing Claudio's trade-network answer.
377|||Rafael's tentative answer invokes the fleet he thinks could decide the question.
382|Fair answer. FA, you know the Spice Islands, right?|Fair answer.;the Spice Islands, right?|Pereira concedes the logic and turns to the named islands with the original surname address.
386|||Rafael identifies the islands as nearby and confirms familiarity.
391|That's right. To Europe right now, the Spice Islands are a treasure. You see?|right now,;the Spice Islands;are a treasure.;You see?|Keep the timing, the place name and Pereira's comparison before he explains the money involved.
394|...Yes.||Restore Rafael's hesitation as he starts to see where Pereira is going.
399|And it's not just spices. The goods here bring in a fortune. Whoever controls this region could use that money to start conquering...|not just spices.;bring in a fortune.;controls this region;to start conquering...|Pereira's premise is control of the region's wealth. Leave the consequence for Rafael to finish.
402|||Rafael lands on the consequence and speaks it with the source's growing dread.
407|||Pereira confirms Rafael has understood what is at stake.
411||Antony Kuhn...;King of the world?;Not a chance in hell!|Claudio moves from disbelief to outright refusal in his own blunt voice.
423|||Jam's emphatic defiance and invocation are distinct from Claudio's.
430|So whoever rules the Spice Islands could end up ruling the world...|rules the Spice Islands;ruling the world...|Rafael draws the larger conclusion tentatively and uses the established place name.
442|You don't get that far on luck alone.||Fernando pushes back in plain speech against treating Kuhn's power as luck.
448||starting to get the picture.|Pereira recognizes that Rafael sees the larger stakes before disclosing his restraint.
451|I'm holding back from an all-out fight with Kuhn. If he beats me, there'll be no one left to stop him.|an all-out fight;If he beats me,;no one left to stop him.|Pereira gives his practical reason for holding back. The danger follows only if he loses.
454|||Rafael's silence gives Pereira's admission time to sink in.
459|I want to see Portugal restored, too. But if that's all we think about, we could hand him the world.|see Portugal restored,;all we think about,;hand him the world.|Keep Portugal's restoration as worthy in Pereira's eyes and its risk if it absorbs their attention.
462|||Rafael's short question lets Pereira give a concrete instruction.
467|Go beat Spain's Valdes! Once you've honed your skills against him, we'll stand a chance against Kuhn together!|Spain's Valdes!;honed your skills;against Kuhn together!|Keep Pereira's objective and the experience he expects them to gain before returning.
470|||Two short fragments show Rafael weighing Valdes and the Armada.
474|As Spain's king, I'd do all I could to strip Portugal's royal family of its claim to the throne for good. There's no time to waste.|As Spain's king,;do all I could;Portugal's royal family;claim to the throne for good.;There's no time to waste.|Pereira makes the same hypothetical in his own terms and drives home the urgency.
477||Portugal's restored,;give you my full support.|Pereira makes his full support contingent on both original outcomes.
481|||The quiet agreement signals Rafael accepts the logic.
486|Valdes should know where the Mediterranean Proof of Conquest is. Can't even beat that little mustached bastard? You won't beat Kuhn in a hundred years!|Mediterranean Proof of Conquest is.;Can't even beat;that little mustached bastard?;You won't beat Kuhn;in a hundred years!|Keep the clue, complete insult, and hyperbole. Pereira's rhetorical question closes the first page and his answer opens the second.
489|...All right. We'll beat Valdes and come back. I promise.|We'll beat Valdes;I promise.|Rafael accepts the charge and promises to return after defeating Valdes.
493|||Pereira's direct vote of confidence keeps the admiral address and surname substitution.
"""


def scene(number):
    return CONTEXTS[sum(number >= start for start in (111, 201, 273, 354))]


def main():
    assert not OUTPUT.exists()
    packet, release, previous_review = map(base.load, (SOURCE, parent.RELEASE, PRIOR))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    group, = packet["groups"]
    assert group["block"] == 60
    decisions = {}
    for line in DECISIONS.strip().splitlines():
        number, text, phrases, reason = line.split("|")
        assert int(number) not in decisions
        decisions[int(number)] = text, tuple(phrases.split(";")) if phrases else (), reason
    prior = {r["source_reference"]["offset"]: r for r in previous_review["records"] if r["block"] == 60}
    rows, plans, failures = [], {}, []
    for entry in group["records"]:
        n, selector = entry["source_record_index"], entry["selector"]
        old = prior.pop(entry["source_offset"])
        assert entry["Japanese"] == old["source_Japanese"] and all(old["review"].values())
        jp, current = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
        choice = entry["native_command_word"] == 0x2100
        assert choice == (selector is None)
        prefix = b"" if choice else bytes([selector])
        if not choice:
            assert selector == old["source_selector"] and (prefix + jp).hex() == old["source_hex"]
        replacement, phrases, reason = decisions.pop(n)
        old_english = logical(entry["current_English"])
        english = replacement or old_english
        assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(old_english) == TOKEN.findall(english)
        refs = {side: dict(file_path=group["file_path"], block=60, offset=entry[f"{side}_offset"],
                           command_offset=entry[f"{side}_command_offset"],
                           archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                           exact_hex=(prefix + value).hex())
                for side, value in (("source", jp), ("current", current))}
        changed = bool(replacement or phrases)
        row = dict(id=old["id"], file_path=group["file_path"], route=0, block=60, source_record_index=n,
                   native_command_word=entry["native_command_word"], native_slots=entry["slots"],
                   source_selector=selector, kind="typed-choice-label" if choice else "progressive",
                   source_reference=refs["source"], current_reference=refs["current"],
                   source_hex=refs["source"]["exact_hex"], current_hex=refs["current"]["exact_hex"],
                   Japanese=entry["Japanese"], previous_English=old_english, english=english,
                   speaker=old["speaker"], context=scene(n), source_meaning=old["source_meaning"],
                   localization_note=reason, protected_phrases=list(phrases),
                   decision="revision" if changed else "retention",
                   finding="choice caption" if choice and changed else "prose and wrap" if replacement else
                           "wrap" if phrases else "retention",
                   review=dict.fromkeys(GATES, True) | {"formatting": not changed and not choice})
        if changed and not choice:
            assert all(phrase in english for phrase in phrases), (n, english, phrases)
            try:
                body, plan = plan_progressive(row, selector, current, jp)
            except (ValueError, AssertionError) as error:
                failures.append((n, english, phrases, str(error)))
            else:
                if body.rstrip(b" ") == current.rstrip(b" "):
                    assert not replacement, row["id"]
                    row.update(decision="retention", finding="retention")
                    row["review"]["formatting"] = True
                else:
                    plans[row["id"]] = plan
        rows.append(row)
    assert not prior and not decisions and len(rows) == 103 and not failures, failures
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
                         target_locale="en-US", review_gates=GATES, previous_sha256=packet["candidate_sha256"],
                         previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
                         source_packet_sha256=base.digest(SOURCE), earlier_contextual_reviews={str(PRIOR): base.digest(PRIOR)},
                         records=rows, plans=plans, decisions=dict(Counter(r["decision"] for r in rows)),
                         findings=dict(Counter(r["finding"] for r in rows)), new_editorial_credit=0,
                         status="Contextual review complete. Changed speech and both menus await native formatting approval."))
    print(f"Reviewed {len(rows)} records. {dict(Counter(r['finding'] for r in rows))}.")


if __name__ == "__main__":
    main()
