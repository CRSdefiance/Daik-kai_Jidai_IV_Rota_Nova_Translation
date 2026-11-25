"""Preserve the individual clean-first editorial decisions; no ROM writes or credit."""
import json
import re
from collections import Counter
from hashlib import sha256
from pathlib import Path

PACKET = Path('work/analysis/Hodram_B71_B80_current_20261101/current_effective.json')
DEST = Path('translations/hodram_B71_B80_editorial_manuscript_v1.json')

# Each entry is an individual editorial decision, not a generated paraphrase.
# None retains the effective predecessor template after whitespace normalization.
DECISIONS = {
71: [
(7, 'Admiral {MACRO:FA}.', 'Restore the respectful summons. Admiral is established explicitly in the linked Maria exchange; do not invent a noble title.'),
(11, None, 'Retain the brief, natural response to being addressed; his next reaction follows the unexpected invitation.'),
(15, None, 'Retain the messenger\'s formal, clear invitation, Maria Li\'s established rank, and Hangzhou.'),
(18, '?', 'Use the ordinary question-mark glyph for the same wordless surprise; no spoken words are added.'),
],
72: [
(6, None, 'Retain Xien Yan\'s welcoming summons and clear direction to Admiral Li; it leads naturally into her congratulations.'),
(10, "I hear you've finally defeated Kuhn. Congratulations.", 'Restore the reported news and finally, in Maria\'s composed conversational voice.'),
(13, None, 'Retain the deliberate wordless pause: it motivates her question about his expression.'),
(17, "What's wrong? Why the gloomy face?", 'Restore her initial inquiry and connect the concern to his suspicious reply.'),
(21, 'What are you planning to use me for this time?', 'Make his recurring suspicion conversational rather than a terse literal future question.'),
(25, "My, aren't you suspicious.", 'Preserve Maria\'s lightly teasing response without making it an accusation or romance.'),
(29, "Well, never mind. At least we've gained a foothold in Southeast Asia.", 'Restore the dismissal before he acknowledges their practical gain; do not imply the entire regional campaign is over.'),
(33, None, 'Retain her pointed question about aligned interests; it answers his practical assessment naturally.'),
(36, None, 'Retain his guarded one-word concession, which allows her to introduce the next offer.'),
(40, "Good. While we're on the subject, I have one more proposal.", 'Keep her opportunistic conversational pivot and additional proposal, without stiff transcript phrasing.'),
(44, '...I thought as much.', 'Preserve his preceding suspicion and dry recognition with a natural spoken response.'),
(48, None, 'Retain the clear Wako question; the next turn explains the culturally specific term.'),
(51, '?', 'Keep his wordless lack of understanding while using the normal question-mark glyph.'),
(55, "Ming's policy of closing itself off has left it without a navy. Japanese pirates take advantage of that to raid and plunder the mainland coast. They're called the Wako.", 'Express Maria\'s source explanation in natural sentences. Preserve her in-story claim about Ming without adding historical corrections, a trade ban, or a broader claim about all Japanese people.'),
(58, 'Their leader is Sojin Kurushima. I formed my private fleet to protect people from his raids...', 'Restore her stated reason for forming the fleet and the trailing pause; retain the native catalogue spelling of Kurushima.'),
(62, None, 'Retain his concise inference about defeating Kurushima; it follows her explanation without adding a mission detail.'),
(65, "Of course, there'll be a reward. Besides, I think Japan has something you're looking for.", 'Keep the reward unnamed and the sought object tentative, using a natural offer rather than an impersonal fragment.'),
(69, "Something I'm looking for? Heh... You underestimate me. Do you take me for your hunting dog?", 'Restore his first-person echo and the hunting-dog image behind his objection to being used.'),
(73, "That's a rather cynical way to look at it. I'm offering you trading rights with Japan.", 'Remove the unsupported exclusive restriction. Preserve her offer of trading rights and composed rebuttal.'),
(77, None, 'Retain the sarcastic How generous of you: it conveys his objection to her acting as though she is doing him a favor.'),
(81, '...Would you rather turn me down?', 'Turn the abrupt Refuse into her cool challenge, leading into his threat to choose another target.'),
(85, "I haven't come all the way to the eastern edge of the world for nothing. But Japan doesn't have to be my target.", 'Preserve his resolve and implied alternative target without inventing a new destination or an actual declaration of war.'),
(88, "...If you'd rather take me on, that's fine.", 'Let Maria explicitly accept the implied challenge in controlled, natural dialogue.'),
(91, "I'm curious whether that's confidence or a bluff. But I have no reason to quarrel with you for now. Don't get so worked up.", 'Preserve his interest, temporary lack of conflict, and deliberately provocative reassurance; no enduring friendship is promised.'),
(94, None, 'Retain Maria\'s silent reaction between the provocation and his acknowledgment that her offer benefits him.'),
(98, "I don't need to think about it. Taking your offer is clearly in my best interest.", 'Keep his practical acknowledgment, without narrowing his advantage to immediate monetary profit.'),
(102, "What a formidable woman... So this is what it means to dance to someone else's tune.", 'Localize the palm-dancing idiom by its effect: he knows she has maneuvered him, without adding romance.'),
(106, "Just sit back and watch. You won't need to lift a finger while I clear out those pirates.", 'Preserve his boast that no intervention is needed, in idiomatic speech; do not promise a particular allied reinforcement.'),
(110, 'Oh, will I now?', 'Restore her skepticism about his claim that she can simply watch, keeping the exchange teasing and competitive.'),
(114, "With that fearless smile of yours backing me up, I can make all the bold speeches I like. How reassuring.", 'Keep his sarcastic connection between her fearless smile behind him and his bravado; this is no specific military-support commitment.'),
(117, 'You and your sarcasm.', 'Retain her recognition of his irony in an idiomatic, lightly exasperated reply.'),
(121, "'So straightforward. So easy to handle.' That's what you're thinking, isn't it? Just wait for the good news.", 'Restore his imagined quotation of her thoughts as an explicit guess, followed by his confident farewell; do not turn it into actual Maria narration.'),
],
73: [
(28, 'Impressive work, Admiral {MACRO:FA}.', 'Restore the explicit admiral title while keeping her praise lightly pointed.'),
(31, "...Don't make me any angrier.", 'Preserve his irritation and pause in natural speech rather than a formal prohibition.'),
(35, None, 'Retain her dry apology and clear handover of the promised reward. The reward remains unnamed; Here is conveys the offer to take it.'),
(56, 'It seems I must acknowledge you as the master of these waters. Take this.', 'Preserve her acknowledgment and the separate conditional handover; do not merge the two reward branches or name either item.'),
],
74: [
(58, "The Ottoman Empire is making some troubling moves in the Mediterranean. Once you've found that treasure, why not head back?", 'Remove the added order to seek the treasure. Restore the conditional return suggestion and her troubling report.'),
(62, "You're well informed. I'll keep that in mind.", 'Restore his acknowledgment of her information and his future intention, rather than telegraphic Useful. Noted.'),
],
75: [
(25, 'Well, well, {MACRO:FA}.', 'Localize familiar -kun through teasing cadence, paired with his final objection to her tone. Preserve the surname macro; invent no dear, nickname, age, or relationship.'),
(29, 'Maria?! What brings you all the way out here?', 'Keep his surprise at her presence and the distance implied, in a natural greeting.'),
(32, 'The Ottoman navy has launched a major offensive to seize control of the Mediterranean.', 'Restore the scale and begun offensive, without claiming the sea has already been conquered.'),
(35, None, 'Retain his natural sudden alarm, existing idiomatic punctuation, and no added event.'),
(39, "I can't imagine my homeland being drawn into the war, but... Did you come all this way to warn me?", 'Preserve his expectation rather than a guarantee of safety, the hesitation, and surprise that she made this journey for him.'),
(43, 'Well, I do owe you.', 'Make Maria\'s understated admission of indebtedness sound conversational; do not invent the debt\'s terms.'),
(47, "I'm glad you did. Thank you.", 'Let his sincere, straightforward thanks motivate her surprised internal reaction.'),
(51, '(Oh? That was surprisingly straightforward...)', 'Preserve the parenthetical thought and her surprise at his unguarded thanks; honest here concerns manner, not an allegation of lying.'),
(55, "But don't say '{MACRO:FA}' in that tone...", 'Complete the paired -kun adaptation: he objects to her familiar way of addressing him, not to an invented dear. Both FA occurrences remain runtime substitutions.'),
],
76: [
(6, None, 'Retain the clear anonymous system notice that a letter has arrived from Escante; it does not identify a messenger.'),
(9, None, 'Retain the unambiguous declaration-of-war system notice and urgency; do not merge it with the letter notice.'),
(27, 'That man... I knew he was up to something.', 'Render the ulterior-motive idiom as spoken suspicion, without specifying the still-unrevealed plan.'),
(40, "So Escante has betrayed us after all.", 'Retain Gerhard\'s considered conclusion in a natural perfect tense after the declaration.'),
(43, "I expected this ever since we heard what he was really like at that tavern... But this puts us at a serious disadvantage.", 'Restore that they heard his nature at an unspecified tavern; a tavern itself did not warn them. Preserve the contrast and current disadvantage.'),
(46, 'What do you mean?', 'Use Gerhard\'s natural request for explanation rather than an isolated Meaning fragment.'),
(50, 'While we were fighting Maldonado, Escante was stockpiling money and strength for his real objective.', 'Keep the contrast in preparation and unnamed objective, with the native catalogue spellings; do not fill in the later empire revelation.'),
(53, 'His objective? What is it?', 'Keep Gerhard\'s echo and specific request for the withheld purpose in a natural turn.'),
(56, 'Well, I can guess...', 'Restore Hodram\'s first-person, unfinished inference without supplying the answer.'),
],
77: [
(12, 'Admiral, a request to take the field has arrived from His Majesty.', 'Restore the king\'s request for action, rather than generic royal orders; retain Gerhard\'s formality.'),
(17, "Admiral, His Majesty has sent a request for us to take the field.", 'Keep the same royal request in Charles\'s slightly more conversational delivery. This is an alternate messenger, not a second consecutive letter.'),
(23, 'From His Majesty? What does it say?', 'Make his surprised question refer naturally to the letter without inventing a named monarch.'),
(33, "Allow me... 'The Ottoman Empire's great offensive has placed the Christian nations in unprecedented danger.'", 'Restore the unprecedented scale and the nations addressed, preserving the formal quoted letter and Gerhard\'s introduction.'),
(36, "'For the honor of our armed forces, meet the enemy and fight to preserve peace in Europe and safe commerce in the Mediterranean.' That is all.", 'Restore the national military honor and instruction to fight. Do not invent a specifically naval oath or a crusade; keep the closing as Gerhard\'s report.'),
(42, "Let me read it... 'The Ottoman Empire's great offensive has placed the Christian nations in unprecedented danger.'", 'Keep the king\'s wording identical in the alternate reading, with Charles\'s conversational lead-in.'),
(45, "'For the honor of our armed forces, meet the enemy and fight to preserve peace in Europe and safe commerce in the Mediterranean.' That's all.", 'Keep the royal instruction identical across alternatives; let only Charles\'s closing be less formal.'),
(52, "...So northern Europe is finally feeling the heat!", 'Localize the fire-at-one\'s-rear idiom as mounting pressure, not literal fire or an unsupported northern invasion.'),
],
78: [
(13, None, 'Retain the localized wordless growl and null-speaker FE presentation; it introduces the angry opening without identifying an unseen speaker.'),
(17, '!', 'Preserve Hodram\'s startled reaction with an ordinary exclamation glyph.'),
(21, "I was so close... My empire could have ruled the New World! If it weren't for you...!", 'Preserve Escante\'s thwarted ambition and blame, rather than presenting an already-established empire as having almost seized the continent.'),
(24, None, 'Retain the natural recognition of Escante at the confrontation.'),
(28, "You, of all people... I'll never hand my empire over to you! Die!", 'Restore the personal emphasis and attack cry without inventing a weapon or who delivers the later injury.'),
(34, 'Well, well, {MACRO:FA}.', 'Restore the feigned courteous greeting in the alternate opening. The honorific does not grant Hodram a noble Lord title.'),
(37, None, 'Retain the restrained recognition in the alternate opening, distinct from the first branch\'s exclamation.'),
(41, None, 'Retain Escante\'s feigned gracious concession, which makes the shift into resentment and attack intelligible.'),
(44, None, 'Retain Hodram\'s guarded silence before Escante\'s facade breaks.'),
(48, "Heh... Hehehe... I was so close... My empire could have ruled the New World...", 'Restore the strained laughter and unfinished imperial ambition in the courteous-opening branch; do not collapse it into the other opening.'),
(51, "If it weren't for you...!", 'Keep the resentful accusation as a natural unfinished outburst; its speaker remains Escante.'),
(55, '!!', 'Preserve the sharper startled reaction with normal exclamation glyphs.'),
(62, 'Admiral, look out!', 'Preserve Gerhard\'s urgent danger warning without inventing the specific ducking action.'),
(66, '!!', 'Preserve Escante\'s abrupt reaction without adding a description of the opaque action.'),
(70, 'Guhhh!!', 'Localize the choking cry as a readable vocalization without naming a wound or attacker.'),
(74, 'G-guh... Am I... dying here?', 'Restore the complete frightened question within the broken, choking delivery; avoid the old ungrammatical Am... Dying fragment.'),
(77, None, 'Retain the readable final choking cry and its existing ordinary exclamation glyphs.'),
(81, None, 'Retain Hodram\'s wordless response after the cry; it separates the action from the concern for his safety.'),
(85, 'Admiral, are you all right? Are you hurt?!', 'Restore both Gerhard\'s safety check and explicit question about injury, with urgent but clear speech.'),
(89, "I'm all right...", 'Restore the calm first-person reassurance and trailing pause; do not add a specific injury diagnosis.'),
(93, None, 'Retain Hodram\'s cold pity and skeptical question about acceptance as king. It neither confirms that acceptance nor invents a completed conquest.'),
(96, "Hm? Escante has something tucked inside his clothes.", 'Keep Gerhard\'s discovery unnamed. 懐 locates it inside clothing but does not establish the old draft\'s specific coat.'),
],
79: [
(5, '…?', 'Retain the puzzled pause while replacing only the full-width question mark with its normal glyph.'),
(10, "...What's all this commotion?", 'Turn the literal So hectic observation into an idiomatic reaction to the unsettled port, leading to the worker\'s explanation.'),
(14, "They say Hayreddin the pirate took a terrible beating from the Ottoman navy. The remnants of his force have come back, and the place is in an uproar.", 'Restore hearsay and the uproar caused by the returning remnants; do not report total annihilation or certain news.'),
(17, None, 'Retain his incredulous echo of the report; the missing verb is supplied naturally by the previous turn.'),
(21, None, 'Retain the concise anonymous order to move and the original FE null-speaker consumer.'),
(26, 'Ah!! H-Hayreddin!', 'Keep the alarm and stammer while removing the unsupported noble Lord title; the respectful shock is conveyed by delivery.'),
(29, '!!', 'Preserve Hodram\'s surprised recognition with normal exclamation glyphs.'),
(33, None, 'Retain Hayreddin\'s longer wordless pause before their exchange; do not supply an invented thought.'),
(37, None, 'Retain Hodram\'s answering silence, preserving the awkward recognition rather than inventing banter.'),
(42, None, 'Retain the natural, wounded challenge about laughing at his disgrace; it motivates Hodram\'s denial.'),
(45, "...You think rather highly of yourself. I'm here on the king's orders to fight the Ottoman Empire.", 'Preserve the rebuke for imagining himself the reason for the visit; fool adds an unnecessary insult and the old draft loses I came.'),
(49, "Hah. Bad luck for you. If you're going up against them, be ready to die.", 'Preserve the gruff personal warning as preparedness, rather than a prediction that their enemies will die.'),
(53, "Wasn't your fleet allied with the Ottoman Empire?", 'Localize pirate 一家 as his outfit/fleet, without implying blood kinship through clan. Keep the previous alliance as Hodram\'s question.'),
(57, None, 'Retain the reluctant silence before Hayreddin explains how the alliance broke down.'),
(61, "Pasha, commander in chief of the Ottoman navy, wanted to fold our pirate fleet into his offensive. We were allies, but he demanded that I pay homage as his vassal.", 'Restore Pasha\'s role and the crucial ally-to-subordinate demand. Do not invent a specific ceremony or an oath already sworn.'),
(64, "My father and I worked hard to build that fleet. I wasn't about to let it be swallowed up by the military. I rebelled against the Ottoman Empire without a second thought...", 'The paired personal backstory and cannot-face-親父 line support my father here. Preserve his own immediate refusal and rebellion; do not borrow a father\'s identity, death, or biography from history.'),
(67, "That was all well and good. We were outmatched, but I meant to hold out for two or three years and show them the pride of the Algiers pirates.", 'Restore the exact intended two or three years and localized pride. The resistance was a plan, not completed years of success.'),
(71, "Then a subordinate I trusted betrayed me. Pasha's forces caught us by surprise, and this is how I ended up. Damn it... I can't face my father.", 'Restore shame rather than literal physical impossibility. Keep the traitor unnamed and do not imply that his father is dead.'),
(75, None, 'Retain Hodram\'s quiet response to the humiliating betrayal rather than inventing sympathy or a new alliance.'),
(79, None, 'Retain the gruff, natural dismissal of the value of telling this story to Hodram.'),
(83, "Here, take it. That bastard Pasha sent it as a token of my subordination. I can't stand the sight of it!", 'Preserve the gruff insult, intended vassal token, disgust and unnamed handover. The demand and refusal above prevent interpreting the token as an oath he accepted.'),
(90, None, 'Retain the curt warning not to lose disgracefully; it ends the exchange without adding allegiance or reconciliation.'),
],
80: [
(6, None, 'Retain the startled recognition of Sera and existing emphatic punctuation.'),
(10, '{MACRO:FI}!!', 'Retain the name call and intensity while replacing full-width exclamation marks with normal glyphs.'),
(14, None, 'Retain the natural question about Sera\'s unexpected presence.'),
(18, 'I heard you were in danger, {MACRO:FI}. I came with others from my homeland to help the king of legend.', 'Correct the reversed comitative: her companions came WITH her; they are not another group she came to rescue. Use clear, simple English and preserve the king as her belief.'),
(22, "You saved my life. Everyone... I'm sorry.", 'Restore his life being saved and apology to everyone, without implying everyone needed the same rescue or inventing his offense.'),
(26, None, 'Retain FI and the exact undecoded ○×○× utterance, including source punctuation. This is intentional opaque language, not full-width Latin contamination.'),
(29, "Yes, thank you. Truly. Now, all of you, get away as quickly as you can. The Ottoman forces won't stand idly by.", 'Keep the sincere thanks, urgent escape instruction and expectation of Ottoman action in idiomatic speech; do not invent a specific pursuit.'),
(33, None, 'Retain Sera\'s clear affirmative before she speaks to her companions.'),
(37, None, 'Retain the exact opaque ○××○○ and its source punctuation; the exchange does not decode it.'),
(41, None, 'Retain Sirwood\'s exact opaque reply ××○ and source punctuation; do not invent its meaning.'),
(45, "Everyone's leaving.", 'Restore Sera\'s report that the others are escaping, rather than turning it into another command.'),
(49, 'You should get away too.', 'Keep his instruction that she also escape, in direct conversational language.'),
(53, None, 'Retain her deliberate silence as she chooses to stay; it motivates his question.'),
(57, None, 'Retain his natural concern and urgent instruction when she does not move.'),
(61, "I'm not going.", 'Give Sera a simple complete refusal, preserving her determination without caricatured broken grammar.'),
(65, None, 'Retain the short puzzled response to her refusal; it invites her explanation.'),
(69, "I'm staying with {MACRO:FI}.", 'Restore the complete decision to remain with FI without making it romance or an oath of service.'),
(72, 'What are you talking about?', 'Restore his explicit incredulity at her choice, rather than the vague What is this.'),
(76, "I'm coming aboard.", 'Give her concrete decision to board the ship a clear, short sentence; no crew rank is assigned.'),
(80, "I still have work to do. It's dangerous. Go home.", 'Preserve his remaining work and safety-based refusal in natural direct speech.'),
(83, "{MACRO:FI}, I want to see you become king of the seas.", 'Restore the prospective kingship and her commitment to witness it in simple English. This expresses her motivation, not a completed or guaranteed outcome.'),
(86, '...No. Go home.', 'Restore the hesitant pause while retaining his firm refusal.'),
(90, "I've made up my mind.", 'Give Sera\'s already-made decision an idiomatic short sentence that carries her stubbornness.'),
(94, None, 'Retain Hodram\'s longer silent beat before he relents.'),
(98, "You're stubborn... Do as you please.", 'Restore his exasperated concession; do not add a relationship or formal permission to join a named crew position.'),
(101, None, 'Retain the unadorned FI call: it naturally reopens the conversation before her request.'),
(105, None, 'Retain his terse but natural prompt for her to continue.'),
(109, "When you've defeated Pasha, come back to this town.", 'Restore the condition before returning and this town, without inventing a location name or an immediate separate order to attack.'),
(112, 'This town?', 'Keep his echo tied to her return request with consistent local terminology.'),
(116, "Yes. To the king's tomb...", 'Restore her confirmation and direction toward the tomb, leaving the thought unfinished for Hodram\'s question.'),
(119, None, 'Retain his natural question about whether the tomb means the pyramid and why she asks; the identification remains a question.'),
(123, "Go there... and you'll understand.", 'Give her hesitant invitation a natural conditional explanation rather than the telegraphic Go... then see.'),
],
}

CONTEXTS = {
71: 'A respectful sailor summons Hodram to meet Admiral Maria Li in Hangzhou; his surprise leads into B72.',
72: 'After Kuhn\'s defeat, Maria and Hodram test each other\'s motives. Her Wako explanation leads to trading rights, his implied threat, mutual challenge, practical acceptance and sarcastic confidence. Review all 32 turns together.',
73: 'Maria rewards Hodram. The promised-reward conversation and the later acknowledgment of regional mastery have distinct conditional handovers; they are not one continuous double reward.',
74: 'Maria warns of troubling Ottoman activity and suggests returning after the treasure is found. Hodram acknowledges her information.',
75: 'Maria unexpectedly comes to warn Hodram of the Ottoman offensive. Teasing familiar address frames his surprise, her debt, his sincere thanks, her private surprise and his objection to her tone. Both FA calls form one localization choice.',
76: 'Conditional Escante letter/war notices lead to Hodram and Gerhard discussing betrayal, unequal preparation and a still-withheld objective. Do not supply the later answer here.',
77: 'Gerhard OR Charles delivers and reads the same royal request. Preserve the two alternative readings and their voices, rather than staging two consecutive letters. Hodram reacts to northern Europe feeling pressure.',
78: 'Escante\'s angry opening OR feigned courtesy collapses into thwarted imperial ambition and attack, followed by choking, a safety check, cold pity and an unnamed discovery. Preserve branch alternatives; opaque actions do not identify a weapon or killer.',
79: 'A port worker reports Hayreddin\'s defeat; the pirate then recounts Pasha\'s demand to turn an ally into a vassal, refusal, planned resistance, betrayal and shame. He gives an unwanted unnamed token and a gruff warning, without pledging alliance.',
80: 'Sera and companions from her homeland rescue Hodram. She sends the others away, stubbornly stays aboard to witness his prospective sea kingship, and asks him to return after Pasha\'s defeat. The tomb/pyramid remains a question. Keep her simple voice clear, not broken; opaque language remains undecoded.',
}

NAMES = {1:'Hodram',3:'Maria',10:'Xien Yan',16:'Gerhard',18:'Charles',24:'Sera',
         34:'Barbarossa Hayreddin',43:'Diogo Escante',78:'Sirwood',115:'Port Worker',156:'Sailor',254:'System (no speaker)'}

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def digest(path):
    return sha256(Path(path).read_bytes()).hexdigest()

def markup(text):
    return re.sub(r'\b(FI|FA|FO)\b', lambda m:'{MACRO:'+m[1]+'}', text)

def main():
    assert not DEST.exists(), 'Preserve earlier manuscript; create a successor.'
    packet = load(PACKET)
    rows = []
    for group in packet['groups']:
        block = group['block']
        choices = {index:(english,note) for index,english,note in DECISIONS[block]}
        assert len(choices) == len(group['records'])
        for source in group['records']:
            index = source['source_reference']['record_index']
            proposed, note = choices.pop(index)
            prior = markup(source['current_comparison_paragraph'])
            english = prior if proposed is None else proposed
            retained = english == prior
            assert (proposed is None) == retained, (block,index,'Unnecessary duplicate revision')
            macros = {key:english.count('{MACRO:'+key+'}') for key in ('FI','FA','FO')}
            assert macros == source['source_macros'], (block,index,macros,source['source_macros'])
            assert english.strip() == english and '\n' not in english and '  ' not in english
            assert not any(token in english for token in ('{LB','{PAD','{ALIGN'))
            assert all(source['source_hex'] and source['current_hex'] for _ in [0])
            selector = source['source_selector']
            row = {key:source[key] for key in (
                'id','file_path','block','source_selector','source_hex','source_complete_preamble_hex',
                'source_reference','source_Japanese','source_decode_error','source_0100_ancestors',
                'source_macros','current_hex','current_reference','current_record_index',
                'current_effective_hex','current_catalogue_selected','selected_native_pointer')}
            row.update(source_record_index=index,source_native_extent=source['native_extent'],
                kind='system-FE' if selector==254 else 'progressive',
                current_raw_storage_English=source['current_stored_text'],
                prior_effective_paragraph_preserved=source['current_comparison_paragraph'],
                prior_macro_normalized_comparison=prior,english=english,logical_English=english,
                planned_English_markup='{SPEAKER:'+format(selector,'02X')+'}'+english,
                speaker=NAMES[selector],context=f'B{block}: '+CONTEXTS[block],
                context_reference=f'#/complete_exchange_contexts/{block}',
                source_meaning=source['source_meaning_gloss'],
                source_meaning_gloss=source['source_meaning_gloss'],
                localization_note=note,finding=note,
                decision='retention' if retained else 'revision',retention_reason=note if retained else None,
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
                whole_clean_exchange_andcadence_emotional_progression_reviewed=True,
                no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
                name_reference='#/identity_review',
                formatting_native_stored_actual_andregistered_release_pending=True)
            rows.append(row)
        assert not choices
    assert len(rows)==144 and len({r['id'] for r in rows})==144
    evidence = [PACKET,Path('work/analysis/Hodram_B71_B80_clean_20261101/all144_clean_meanings_before_English.json'),
        Path('work/analysis/Hodram_B71_B80_identity_20261101/native_names.json'),
        Path('work/analysis/Hodram_B71_B80_identity_20261101/clean_names.json'),Path(__file__)]
    counts = Counter(r['decision'] for r in rows)
    doc = dict(format='hodram-complete-exchange-editorial-manuscript-v1',
        translation_policy='natural-dialogue-v2',target_locale='en-US',
        file_path=packet['file_path'],blocks=list(CONTEXTS),
        current_ROM=packet['current_ROM'],current_ROM_sha256=packet['current_ROM_sha256'],
        current_archive_sha256=packet['current_archive_sha256'],
        current_packet=str(PACKET),current_packet_sha256=digest(PACKET),
        complete_exchange_contexts=CONTEXTS,records=rows,total_editorial_objects=len(rows),
        revised=counts['revision'],retained=counts['retention'],
        source_macro_counts={key:sum(r['source_macros'][key] for r in rows) for key in ('FI','FA','FO')},
        source_FE_panels=sum(r['source_selector']==254 for r in rows),
        identity_review=dict(
            progressive_names=NAMES,
            proper_name_references=['Hardum Pasha','Sojin Kurushima','Vasquez Maldonado','Diogo Escante','Barbarossa Hayreddin'],
            basis='Current native progressive/full getters are bound to clean getters in the identity evidence. Preserve current name spellings, without historical biography. Actor 33 Pasha is distinct from Janus Pasar.',
            father_context='B79R64 builds the fleet with 親父 and R71 cannot face 親父. The same personal backstory supports my father; neither death nor identity is supplied. This does not generalize familiar address into kinship elsewhere.',
            familiar_address='B75R25/R55 pair Well, well, FA with the objection to that tone. This preserves familiar -kun pragmatics without dear, a false relationship, or a fixed replacement for the macro.',
            separate_consumers='Actor156 Sailor in progressive display and Retainer in full catalogue are distinct consumers. No global relabeling is authorized by this scene.',
            open_full_catalogue_findings=['Actor34 full-name Fazul contains a full-width F.', 'Actors42/43 full names retain untranslated デ middle fields; inspect shared ownership before patching.'],
            no_shared_name_ROM_changes_orall207_approval=True),
        all_individual_four_prose_gates_true_formatting_false=True,
        ordinary_wrapping_owned_by_formatter=True,no_manual_breaks=True,
        structure_inventory_reference=str(PACKET)+'#/groups',
        conditional_membership_not_claimed_as_actual_gameplay=True,
        no_ROM_changes_no_new_completion_credit=True,new_credit=0,full_goal_complete=False,
        evidence={str(path):digest(path) for path in evidence})
    DEST.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(manuscript=str(DEST),records=len(rows),decisions=counts,source_macros=doc['source_macro_counts'],FE=doc['source_FE_panels'],formatting_approved=0,new_credit=0)))

if __name__=='__main__':
    main()
