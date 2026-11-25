"""Record the contextual B166 review before native layout verification."""

from collections import Counter
from pathlib import Path

from scripts import register_rafael_homeland_and_maps_20261121 as parent


ROOT = Path("work/analysis/rafael_B161_B169_followup_20261121")
PACKET = ROOT / "paired_source_final_candidate.json"
OUTPUT = ROOT / "B166_contextual_decisions_v4_final_candidate.json"
CATALOGUE = parent.stage.review.CATALOGUE
SOURCE_REVIEW = Path("translations/rafael_B166_B167_integrated_final_review_v1.json")

CONTEXTS = {
    "arrival": "Claudio chooses to wait outside the royal audience. Rafael wants him there for the occasion but respects his decision. Claudio asks to hear what happened and teases him about getting a reward.",
    "audience": "The king reports what the seven Proofs could accomplish with the Pope and appoints Rafael viceroy over the overseas Estado. Alternate companions react in asides. The king invites Rafael to appear before the public.",
    "eirene": "Outside, Claudio and Eirene discuss the distinction she may receive and the prospect of her going back to Athens. He admits he is worried about their lives taking different courses. Her questions give him room to say what he wants.",
    "overhearing": "The crew watches from a distance and speculates about Claudio and Eirene. They cannot make out the entire exchange, and the joke proceeds to their discovery before anyone announces a definite outcome.",
    "expedition": "After being discovered, the crew learns that Rafael turned down the viceroyalty. He explains Albuquerque's loyalty to the sovereign at the time and his own decision to survey uncharted waters. The crew rallies around the expedition.",
    "letter": "Eirene gives Rafael a letter from Charlotte. The game presents his name, her hesitant Portuguese with pronunciation aids and a signature, then an English reading. The companions defend the effort Charlotte put into learning and writing it.",
    "departure": "Claudio suggests their first destination in light of the letter. Julio and Janus back the New World expedition while leaving Rafael to give the order. The crew responds together.",
}

# A blank replacement preserves the installed words. Layout notes never supply authored linebreaks.
DECISIONS = """
6|||Janus announces the return to Portugal and keeps his excited address to Rafael.
9|Mr. FA, His Majesty is waiting for you.|Mr. FA;His Majesty|The attendant announces the audience formally. The surname and its runtime substitution remain intact.
20|What?! We're going before the king? I-I'm getting awfully nervous!|awfully nervous!|Cesare's emphatic stammer carries his fear of the audience.
27|||Claudio makes a quiet request to speak with Rafael before they go in.
30|||Rafael's reply uses his familiar nickname for Claudio.
35|I'm no good with all that ceremony. Mind if I wait out here?|wait out here?|Claudio asks to wait outside because the formal setting unsettles him.
39|It's a big moment. I'd like you beside me, Clau. But if you'd rather stay out here, that's all right.|beside me, Clau.|Rafael says he wants Claudio there and accepts Claudio's preference without insisting.
44|||Claudio asks Rafael to tell him what happens after the audience.
48|||Rafael promises to come back as soon as he is done.
52|And don't let them get away without giving you a reward!|giving you a reward!|Claudio jokes about making sure Rafael gets something for his trouble.
55|||Rafael gives a casual farewell before leaving for the audience.
60|||Claudio sees him off in the same casual register.
64|||Janus invites the party to go in, ending the exchange outside.
69|||The king greets Rafael by his runtime surname and calls him the pride of Portugal.
72|I'm FU, and I've returned to my homeland, Portugal.|my homeland, Portugal.|Rafael introduces himself by full name and formally names the country he has returned to.
85|If we show the Pope the seven Proofs of Conquest you gathered, I hear he'll press for recognition of the Portuguese Crown's authority again.|seven Proofs of Conquest;Portuguese Crown's authority|The king reports the expected support. The wording preserves the condition and the king's uncertainty about the outcome.
88|||Rafael is startled by the news about the Proofs.
96|||The king calls Rafael a treasure of the seafaring country, which leads into the appointment.
100|In the name of the King of Portugal, I appoint you viceroy over the Estado, all our overseas trading territories!|King of Portugal;overseas trading territories!|The formal appointment preserves the exact title and the explanation of Estado.
103|||Rafael stammers at the unexpected rank and addresses the king respectfully.
107|||Janus admires Rafael in a private aside with the name substitution.
118|||Yifa keeps her enthusiastic repetition on hearing the appointment.
132|Heh. I'd say a rank like that is only fitting.|only fitting.|The aside treats the rank as expected in a matter-of-fact voice. Its speaking owner and private presentation stay intact.
146|||Emilio thinks the word sounds tasty even though he doesn't know what it means. The joke belongs to his aside.
152|||The king urges Rafael out to the square to show him to the crowd, with his repeated invitation intact.
155|...||Rafael's pause after the announcement reads in the surrounding dialogue font.
170|||Rafael returns and greets Claudio by his nickname.
175|||Claudio notices how quickly Rafael is back.
183|||Eirene recognizes Claudio hesitantly. Retain the embedded Eirene heading and pause.
187|||Claudio starts to use the old name before correcting himself.
190|||Eirene wonders why Claudio is outside. Preserve the heading.
193|I never did much like all that ceremony...|all that ceremony...|Claudio gives Eirene the same discomfort he described to Rafael.
196|||Eirene's laugh acknowledges that Claudio is uncomfortable in formal settings. Preserve the heading.
201|What about you? Aren't they going to give you some grand title as a scholar?|grand title|Claudio asks about academic recognition without inventing the exact rank she is to receive.
205|Eirene: It looks that way. But I haven't made any great discoveries. I'm not sure I've earned it.|great discoveries;I'm not sure I've earned it.|Eirene doubts she has done enough to merit the distinction. The label remains its own native heading and her concluding doubt reads as one line.
208|||A higher rank means more funding, and Eirene's joke about her poverty keeps her practical attitude distinct from her doubts.
211|||Claudio mutters that she will be gone. Eirene's next line establishes that she cannot make out what he said.
215|||Eirene asks what she missed instead of acting as if she heard the remark. Preserve the heading.
219|Nothing... You'll be going back to Athens for your research, right?|back to Athens;research, right?|Claudio avoids repeating himself and asks whether she will return to Athens for her work.
222|||Eirene thinks she probably will and tries again to find out what Claudio said. Preserve the heading.
225|...||Claudio pauses before acknowledging what he was thinking.
229|You looked like a scholar again back there. Once you leave the ship...|a scholar again|Claudio describes a side of Eirene he has seen before and leaves his thought unfinished for the next panel.
233|You'll be off to a whole different world. Damn. Listen to me. Since when do I worry about things like that?|a whole different world.|Claudio finally explains his worry, then tries to take the seriousness out of it with a joke at his own expense.
237|||Eirene says Claudio's name gently after his admission. Preserve the heading.
240|Ha! What's gotten into me today? Must be the weather. Or this palace, I bet.|this palace, I bet.|Claudio avoids the subject by blaming something outside himself.
245|||Eirene asks what Claudio wants from her. Preserve the left-side and vertical presentation of this exchange.
249|||Claudio's stammer shows he is unprepared for the question. Preserve his right-side presentation.
253|||Eirene asks directly if he wants her to give up her research. Preserve the left-side presentation.
257|||Claudio objects without supplying a clear answer. Preserve his right-side presentation.
261|||Eirene tries another possibility and names Athens. Preserve the left-side presentation.
265|||Claudio's right-side silence is the answer here. Keep the deliberate leading blanks and pause glyph.
269|||Eirene lets the other possibility go unsaid. Preserve the left-side presentation.
273|||Claudio falls silent again. Keep the deliberate alignment and pause.
278|||Janus quietly asks for a report, revealing that the crew is watching.
282|||Rafael cannot see enough to draw a conclusion from where they are.
294|||The short complaint identifies the jostling in the group.
308|||Another watcher complains that he cannot see much either.
323|||The objection breaks into the sound of eating. The two parts together make the joke.
337|||The cheer encourages Claudio without telling the player what he should ask or do.
352|||The warning reminds the others that they can be discovered if they make noise.
359|||Rafael begins with Eirene's public alias and corrects himself. He sees a nod, without claiming to hear what she said.
371|||Another watcher asks what happened, continuing the crew's incomplete version of events.
378|||Janus asks whether Claudio is blushing and says he has never seen him like this.
381|||Julio jokes that Claudio is already under Eirene's thumb without establishing their relationship as a fact.
392|I can't stand it. I'm getting all itchy just watching this.|just watching this.|The crew member's physical discomfort shows embarrassment at watching, though the next reply calls out his grin.
413|||The retort answers the watcher who complains about the scene while grinning.
422|||The alternate speaker makes the same retort. Preserve the original actor selection.
435|||Janus sees the pair coming toward the group and warns them abruptly.
440|||The alternate speaker gives the same warning. Preserve the original actor selection.
446|||Rafael stumbles as the others push. The line preserves his interrupted protest and cry.
452|||Claudio immediately recognizes Rafael and confronts the whole group.
455|Well, uh... the audience was over, so I came looking for you. I didn't mean to eavesdrop, but...|came looking for you.|Rafael explains why he came and trails off in embarrassment when he gets to watching and listening.
459|||Claudio objects as if the others had been watching a show, preserving the stammer.
471|||The crew member admits that the situation was too entertaining to ignore.
478|||Janus defensively notes that he asked them to stop.
489|Honestly, the lot of you! That was rude!|That was rude!|Cristina reproaches the watchers directly in a conversational register.
504|||The reply points out that everyone joined in anyway.
519|...||The silent reaction uses the normal dialogue punctuation without changing the actor.
526|||Eirene realizes the others now know she is a woman. It reads as her observation, without ascribing a reaction to everyone.
529|||Janus stammers because he does not know how to respond.
533|I thought it would be all right by now. I'm sorry. I didn't think I could keep pretending I didn't know.|keep pretending|Rafael apologizes and explains why he felt he could no longer keep up the pretense.
538|Heh, it's fine. I heard the news. Congratulations, FI. Oh, I suppose I shouldn't call you that now.|Congratulations, FI.;call you that|Eirene reassures him, congratulates Rafael, then jokes that his appointment changes how she should address him. The shorter reassurance lets the full congratulations fit beside a 16-character given name.
541|R-right! And you, FI! What are you doing standing around out here?!|standing around out here?!|Claudio seizes the announcement as a new subject and challenges Rafael about lingering outside.
550|||Rafael's short question invites Claudio to explain what he thinks should be happening.
555|||Claudio expects a public appearance because of the appointment. His loose phrasing shows he has secondhand details.
559|||Janus laughs before Rafael lets Claudio in on the change of plan.
564|||Rafael hesitates before giving the surprising reply. Preserve the speakerless presentation.
568|||Claudio's question marks register bewilderment without adding a spoken sentence.
572|||Rafael reveals his decision in as few words as the source. Preserve the speakerless presentation.
584|||Arcadius reacts to the refusal in understandable surprise.
591|||Claudio echoes the unexpected decision with a stammer.
595|||Rafael distinguishes Albuquerque's established naval command from the viceroyalty and his own position as a sailor. The sentence carries all three facts.
606|||Claudio's accusation calls back to the fleet's alignment with Spain. He assumes Rafael yielded the office to Albuquerque.
610|||Rafael rejects the accusation of betrayal and explains allegiance to the king who was their sovereign at that time.
617|Ah, for crying out loud! You can be too nice, you know! Why do you have to be so...|too nice, you know!|Claudio expresses frustration with Rafael's generosity, then trails off before reconsidering it.
621|||Claudio recognizes that the same quality might explain why the crew follows Rafael.
625|||Julio quietly agrees with Claudio's softened judgment.
629|I offered to survey uncharted waters instead. I want to help Portugal expand its shipping.|survey uncharted waters|Rafael proposes exploration as a practical contribution to Portuguese seafaring.
633|||Claudio laughs at the idea of exchanging the viceroyalty for an expedition and approves.
638|||Claudio checks that Rafael will still need him. The question echoes the earlier discussion of parting.
642|||Rafael assures Claudio that he is counting on him.
646|||Claudio eagerly promises to help.
658|||Eirene sees the expedition as a chance to find something new to research. Her interest follows naturally from the earlier conversation.
680|||The threat about flirting aboard ship keeps the teasing conditional, without establishing that a romance has begun.
683|||Claudio stammers in his embarrassed protest.
695|||The watcher is delighted by the prospect of more scenes to observe and plays off the earlier eavesdropping.
714|||Cristina sees that Eirene looks happy and tentatively considers going back to London. Neither thought is inflated into a firm decision.
723|||Julio suggests preparing the expedition once their decision is made.
726|||Rafael says they can let the tired crew rest before they leave.
731|What are you talking about? If we drag our feet, another country's expedition will beat us there!|another country's expedition|Claudio urges them to hurry or another country's expedition will beat them to the destination.
742|||The crew member rejects the idea of losing in his own blunt terms.
756|||The next speaker agrees that being first is what counts in a competition.
770|||Eirene remembers the object she has for Rafael and asks him to guess what it is.
774|||Rafael asks whether it is a letter after a moment of uncertainty.
779|||Eirene confirms it and invites him to read it.
782|||Rafael wonders who wrote it, then recognizes the letter's origin without announcing it yet.
787|||The letter's address is the runtime given name alone. Preserve its exact presentation.
791|||Keep Charlotte's beginner Portuguese and the separate pronunciation aid. The spelling is part of the characterization and sets up the crew's comments about the letter.
794|||Keep Charlotte's second Portuguese line, its separate pronunciation aid, and her signature at its original anchor.
797|||The English reading keeps Rafael's substituted name, both thoughts in the letter and Charlotte's signature. It belongs to the reading panel, following the two Portuguese panels.
807|||Cesare carefully calls the writing awkward. It leads directly into the others defending Charlotte's effort.
818|||The reply concedes that the intended meaning is clear, prompting the rebuke.
832|||The sharp reply tells the others to keep their criticism to themselves.
846|||Cristina says that Charlotte put her heart into the letter and calls out the rude reaction.
860|||The second rebuke asks how the speakers can miss what the letter means to Charlotte.
869|||Janus recognizes that she studied Portuguese and worked hard to write it. The tentative phrasing stays.
873|||Rafael responds only with Charlotte's name after reading.
877|||Claudio connects the letter to the expedition by saying he knows the first destination.
880|||Rafael stammers in surprise before Claudio teases him.
884|Aw, you're just shy. Come on, get ready!|Come on, get ready!|Claudio teases him for being embarrassed and tells him to get ready. The source gives no additional visible reaction here.
887|||Julio says nobody objects and supports beginning the expedition in the New World.
891|||Rafael's quiet use of Julio's name acknowledges his support.
899|||Janus asks the admiral to give the order as he normally does.
902|||Rafael agrees after a short pause.
908|||Rafael gives the command to leave. Preserve the final collective exchange's original speakerless placement.
912|||The crew answers together. Preserve the existing final-panel placement.
"""


def context_for(index):
    if index <= 64:
        return "arrival"
    if index <= 155:
        return "audience"
    if index <= 273:
        return "eirene"
    if index <= 519:
        return "overhearing"
    if index <= 756:
        return "expedition"
    if index <= 873:
        return "letter"
    return "departure"


def source_reference(row, group, side):
    return {
        "command_offset": row[f"{side}_command_offset"],
        "offset": row[f"{side}_offset"],
        "exact_body_hex": row[f"{side}_body_hex"],
        "block_sha256": group[f"{side}_block_sha256"],
        "archive_sha256": group[f"{side}_archive_sha256"],
    }


def main():
    base = parent.base
    packet = base.load(PACKET)
    assert packet["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["candidate_sha256"] == base.load(parent.RELEASE)["candidate_sha256"]
    group, = [g for g in packet["groups"] if g["block"] == 166]
    entries = [line.split("|", 3) for line in DECISIONS.strip().splitlines()]
    assert [int(line[0]) for line in entries] == [r["source_record_index"] for r in group["records"]]
    names = {
        r["actor_ID"]: r["progressive_nameplate"]
        for r in base.load(CATALOGUE)["source_and_current_default_name_fields"]
    }
    names[254] = "System panel"
    glosses = {
        r["source_record_index"]: r for r in base.load(SOURCE_REVIEW)["records"] if r["block"] == 166
    }
    token, logical = parent.stage.review.TOKEN, parent.stage.review.logical
    records = []
    for row, (index, replacement, protected, note) in zip(group["records"], entries, strict=True):
        number = int(index)
        source_gloss = glosses.pop(number)
        assert source_gloss["source_hex"] == f"{row['selector']:02x}" + row["source_body_hex"]
        assert source_gloss["source_Japanese"] == row["Japanese"]
        current = logical(row["current_English"])
        english = replacement or current
        assert token.findall(english) == token.findall(row["Japanese"])
        if replacement:
            assert replacement.isascii()
        phrases = protected.split(";") if protected else []
        assert english and note and all(phrase.casefold() in english.casefold() for phrase in phrases)
        modal = row["selector"] == 254
        records.append({
            "id": f"DK4_MES_B166_R{number:04d}",
            "block": 166,
            "file_path": group["file_path"],
            "source_record_index": number,
            "source_reference": source_reference(row, group, "source"),
            "current_reference": source_reference(row, group, "current"),
            "source_selector": row["selector"],
            "speaker": names[row["selector"]],
            "contextual_speaker": source_gloss["speaker"],
            "Japanese": row["Japanese"],
            "source_meaning": source_gloss["source_meaning"],
            "context": CONTEXTS[context_for(number)],
            "previous_English": current,
            "english": english,
            "protected_phrases": phrases,
            "localization_note": note,
            "decision": "revision" if english != current else "retention",
            "formatting_scope": "native specialized FE consumer" if modal else "native progressive dialogue",
            "expected_embedded_heading": "Eirene" if row["Japanese"].startswith("＜エイレネ＞") else None,
            "review": {
                "source": True, "context": True, "localization": True, "naturalness": True, "formatting": False
            },
        })
    assert len(records) == 136 and not glosses
    assert sum(r["source_selector"] == 254 for r in records) == 29
    assert not OUTPUT.exists()
    base.save(OUTPUT, {
        "translation_policy": "natural-dialogue-v2",
        "target_locale": "en-US",
        "candidate_sha256": packet["candidate_sha256"],
        "paired_source": str(PACKET),
        "paired_source_sha256": base.digest(PACKET),
        "prior_source_glosses": str(SOURCE_REVIEW),
        "prior_source_glosses_sha256": base.digest(SOURCE_REVIEW),
        "status": "Contextual review complete. Native formatting, gameplay and registration pending.",
        "records": records,
    })
    print(f"Reviewed {len(records)} records over seven exchanges. {dict(Counter(r['decision'] for r in records))}")


if __name__ == "__main__":
    main()
