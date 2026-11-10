"""Clean-first whole-exchange review of 82 Hodram utterances; no layout approval."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B54_B60_prose_v8800')
DOC = Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
CURRENT = Path('work/analysis/Hodram_B54_B60_current_v8799/current_effective.json')
GLOSS = Path('work/analysis/Hodram_next_clean_gloss_v8787/82_qualified_clean_glosses_no_unbound_gender_orFA_type.json')
VIEW = Path('work/analysis/Hodram_B54_B60_source_review_v8798b/source_context_names_display_review_before_current_English.json')
PATHS = Path('work/analysis/Hodram_B58_source_paths_v8796/all64_structural_paths_49utterance_memberships_unforced_opening_reference.json')
NAMES = Path('translations/hodram_B54_B60_speaker_name_review_v1.json')
CITY_TERMS = Path('translations/common_native_prefix_repairs_v100.json')
PROOF_TERMS = Path('translations/common_japanese_b36_advice_manuscript_v1.json')
RULER_TERMS = Path('translations/common_japanese_b34_manuscript_v1.json')

# Each tuple is authored against the complete Japanese exchange, then compared
# with the separately preserved predecessor. Retention is computed, never assumed.
LINES = {
54: {
6: ("You new around here?", 'The informal newcomer check already works.', 'The casual dropped auxiliary is idiomatic for this Port Worker. It asks whether the captain is new without inventing a career, faction or prior relationship.'),
10: ("Hm? Yes.", 'The puzzled acknowledgment already works.', 'The short puzzled response followed by assent preserves both parts of the Japanese and lets the worker continue without adding an explanation.'),
14: ("So you're new. Well, good luck. Heh heh.", 'The acknowledgment, encouragement and low chuckle already work together.', 'The worker acknowledges the answer, offers a potentially unsettling good wish, and chuckles. The natural English repetition preserves that progression without turning the speaker into a confirmed villain or explaining the laugh.'),
18: ('？', 'The isolated puzzled reaction is already faithful.', 'Keep the language-neutral question reaction as a reaction, rather than inventing a spoken sentence or a motive. Its full-width glyph is source-compatible; final English display remains to be checked.'),
},
55: {
6: ("You're {MACRO:FA}, the military man, right? The guildmaster in Veracruz was asking for you.", 'Officer asserts a particular rank; the Japanese says military person. Wants you loses the reported past request.', 'The Port Worker checks the identity informally and relays the guild contact\'s request. Military man preserves the source role without assigning a commission or naval rank. Guildmaster renders the familiar guild address as its established functional English role, not a father relationship. Was asking for you retains the reported request without adding urgency or an order. Preserve the surname substitution and established Veracruz spelling.'),
},
56: {
7: ("...And you? Won't you go with them?", 'The question about her plans and the departing group already works.', 'Read after the release of captives and before her silence: the captain asks what she will do and whether she will go with the others. The natural two-question English carries both ideas without adding an order or a destination.'),
10: ('Foreign Girl: ...', 'Strange girl can suggest bizarre behavior; 異国 identifies foreign origin.', 'Keep the caption and silence together as the FE system-panel body. Foreign Girl localizes the descriptive caption without giving her a new name or creating an actor254 nameplate. The colon performs the caption function; ordinary layout belongs to the distinct panel formatter.'),
13: ("I see. You're from a different ethnic group than the other captives. You should let the people here look after you for a while.", 'The predecessor loses the explicit comparison with the other captives and the temporary recommendation.', 'The matter-of-fact captain recalls her differing ethnic identity and proposes temporary care in this town. Different ethnic group preserves 民族 without substituting nationality, religion or race. The people here look after you expresses local protection in natural speech without inventing a shelter institution, a guarantee of safety or permanent residence.'),
},
57: {
7: ('Ah... {MACRO:FI}.', 'The opening hesitant attempt to address the captain was omitted.', 'Keep the small hesitant opening and the given-name call. This begins her attempt at newly learned speech; it does not imply a new intimacy or a different name.'),
11: ('Hm? What is it?', 'Bare What? makes the response more abrupt than the attentive source.', 'The captain notices her addressing him and asks what she wants to say. The complete conversational response preserves his brief, direct voice without adding impatience.'),
15: ('...Thank... you.', 'The predecessor omits the hesitation within the newly learned expression.', 'A pause between familiar English words conveys her effort respectfully. Do not invent a phonetic accent, imply an inability to think, or turn language learning into a joke.'),
19: ("You've learned the language?!", 'Our speech sounds translated and weakens the surprise.', 'Express the captain\'s surprise at her learning the language in idiomatic English. Do not name the language or imply she was previously unable to speak any language.'),
23: ('(Nods) ...A little.', 'The nod, pause and modest learner reply already work.', 'The written nod is in the source, and A little is a natural short learner response. The pause carries hesitation without reproducing syllable breaks as a caricature.'),
27: ("You're a quick learner.", 'The captain\'s praise already works.', 'The concise praise naturally acknowledges her answer and ability. No added age label, pet name, relationship or change of subject is needed.'),
31: ('{MACRO:FI}. Thank... you.', 'The repeated name and halting gratitude already work.', 'Her second thank-you follows his praise. Preserve the effort and earnest repetition without exaggerating an accent or treating it as a romantic confession. Macro notation is serialization only.'),
35: ("Ah... Don't mention it.", 'Never mind can dismiss her effort; 気にするな is his modest response to thanks.', 'The small hesitation followed by the idiomatic response to gratitude conveys his awkward warmth. Do not add romance or tell her to stop speaking.'),
},
58: {
6: ('W-what are you doing?!', 'The frightened stammer and protest already work.', 'The captured man protests the group\'s actions. English you naturally addresses more than one person; no extra scene action or attacker needs to be invented.'),
10: ('Get over here!', 'The rough command already works.', 'Keep the worker\'s forceful ordinary command, with no added threat or official authority.'),
14: ('What? Espinosa?!', 'The captain\'s startled recognition already works.', 'The surprise and established surname identify the man in the exchange without adding a rank, biography or a new accusation.'),
18: ("Well done, {MACRO:FA}! You've defeated this scoundrel.", 'The predecessor omits the explicit praise in よくぞ.', 'The respectful local speaker praises the captain for defeating the scoundrel. Polite phrasing carries the honorific without inventing Sir or a rank. Scoundrel preserves the moral insult; the surname macro remains exact.'),
21: ('Y-you think you can get away with this?!', 'A definite promise of punishment replaces the source\'s frightened rhetorical protest.', 'The stammering question is an angry attempt to intimidate his captors. It does not establish a future punishment, a court or a guaranteed rescuer.'),
24: ('Shut up!', 'The rough imperative already works.', 'This blunt interruption answers his protest in the worker\'s angry voice. It needs no additional insult or authority.'),
28: ('Gah! That hurts!', 'The cry and pain already work.', 'Preserve the audible pain without inventing a specific blow, weapon, attacker or animation from surrounding opaque commands.'),
32: ("You've been doing whatever you please all this time!", 'The predecessor changes a complaint about past conduct into a promise that cruelty now ends.', 'The angry worker accuses him of prolonged unchecked conduct. The following confused denial leads into concrete accusations; do not anticipate a punishment or guarantee the end of abuse.'),
35: ('W-what are you talking about?', 'The nervous hesitation and complete defensive question were lost.', 'The captured man feigns confusion before the accusations become specific. Preserve his nervous delivery rather than giving him a detached fragment.'),
39: ("Don't pretend you've forgotten! You cheated my father out of his house and farmland! He and the rest of my family are missing!", 'The predecessor omits the fraud and farmland and blurs the father\'s disappearance.', 'Restore the explicit actual father, deception, house, farmland and missing family. Missing does not mean confirmed dead. The rough force comes from the accusation and exclamation, not an invented slur or additional crime.'),
42: ('My friend tried to report your corruption back home. You killed them and made it look like an accident!', 'The predecessor loses the report to the home country and the staged accident.', 'Keep both the attempted report and the killing disguised as an accident. Singular them avoids assigning the friend an unsupported gender. Back home preserves 本国 without naming a country or inventing a specific official recipient.'),
46: ("Lots of villagers back home have been taken away and forced to work all over the place, with barely enough to eat!", 'The predecessor loses dispersal and hunger, and replaces them with an unsupported nearly-to-death claim.', 'The innkeeper describes many villagers taken from her home and made to work in various places while barely fed. The conversational phrasing preserves those concrete abuses without inventing deaths, one destination or a governmental role.'),
58: ('A devil in human skin...', 'The companion\'s grave condemnation already works.', 'This is a natural English rendering of the demon-in-human-skin image. It is moral condemnation, not a literal species claim. Review as an optional companion reaction, not as an unconditional speaker turn.'),
64: ("I-I know nothing about it! Those fools under me did it all on their own!", 'The predecessor drops claimed ignorance and contempt for the blamed subordinates.', 'Restore the frightened denial and scapegoating. Under me is natural in his speech and preserves the subordinate relationship without assigning every subordinate a gender. His claim is dialogue, not a verified account of innocence.'),
68: ('You bastard...!', 'The worker\'s angry interrupted insult already works.', 'Use the idiomatic angry insult for the outburst. It makes no literal assertion about parentage and adds no specific threat.'),
80: ("Rotten to the core... There's no excuse for him.", 'You deserve no mercy can imply harsher punishment than the source\'s refusal of mitigating grounds.', 'Fernando\'s rough optional aside condemns complete corruption and rejects excuses. It does not specify execution or a legal sentence. The third-person aside fits the surrounding denial and reactions.'),
93: ('Sera, do you know this man?', 'The captain\'s direct question already works.', 'In the conditional Sera exchange, the captain asks about recognition without presuming their history. The established short name is supported by the earlier full introduction.'),
97: ('...Yes.', 'The quiet pause before her answer was lost.', 'Preserve the subdued recognition before Espinosa reacts. This quiet answer begins the emotional escalation toward her accusation.'),
101: ('Y-you?!', 'His shocked recognition already works.', 'The brief startled stammer conveys the source\'s shock without supplying a new relationship or explaining how they met.'),
105: ('This man... said... sell me. For a high price. Send me... to his country.', 'The predecessor changes an order into a completed sale and misreads the destination as Sera\'s own home.', 'Her halting accusation reports his order to sell her for a high price and send her to the home country associated with that order. His country preserves the deictic home-country reference without naming Portugal or claiming the transport happened. Use simple fragments and pauses respectfully; do not invent a comic accent or a homecoming.'),
108: ('W-what...?!', 'Lies! makes an explicit accusation absent from his interrupted protest.', 'Keep the alarmed unfinished protest. His full false-accusation defense comes after the captain\'s silence, so do not move it into this turn.'),
112: ('…', 'The captain\'s silence already works.', 'Keep the silent reaction between the interrupted protest and the attempted denial. An invented spoken judgment would change the pacing and the captain\'s role.'),
116: ("Wait! You've got the wrong man! That's a false accusation!", 'The predecessor loses Wait and uses stiff legal-sounding slander.', 'The frightened man interrupts and claims mistaken identity and a false accusation. Ordinary spoken English keeps the denial without adding a judicial process or a separate allegation.'),
120: ('My younger brother... the others with me... He killed them all! This man!', 'The predecessor loses younger and all, and broadens companions into an entire people.', 'Keep the explicit younger brother and the companions\' shared fate without asserting close friendship, ethnicity or the destruction of a whole population. The others with me is concrete, simple learner speech for 仲間. The repeated This man and escalating punctuation retain distress rather than polishing it into a formal testimony.'),
124: ("S-stop! You... Damn it! I should've killed you with the others back then... Ugh!", 'The predecessor omits the incriminating with-the-others admission.', 'Restore the admission that undermines his denial and his contemptuous failed interruption. You... carries the hostile address without adding a sexual slur. The final pain cry does not establish a specific blow or punishment.'),
127: ("...Looks like you can't talk your way out of this.", 'No escape can imply physical confinement rather than failed excuses.', 'The captain draws an apparent conclusion after the man\'s own admission. Looks like preserves the qualification; talk your way out preserves verbal evasion rather than inventing an escape attempt.'),
137: ("You monster! {MACRO:FA}, what are you going to do with him?", 'The predecessor drops the condemnation and changes the captain\'s intended action into a collective we.', 'The local witness condemns Espinosa, then asks what the captain intends. Retain that agency so the captain\'s next decision to leave the matter to the locals is coherent. Monster is a moral insult, not a literal creature claim.'),
141: ('You decide his fate.', 'The captain\'s delegation already works.', 'The plural locals decide the man\'s disposition. Fate is a natural concise expression for this delegation and does not itself specify death or any particular sentence.'),
145: ("You heard him! Come on! We'll make you pay for what you've done!", 'The predecessor reduces the full reckoning to an abstract every crime and blurs the worker\'s forceful lead-in.', 'The worker addresses the group, orders Espinosa along, and promises a full reckoning. We naturally refers to the locals just entrusted with his disposition; do not add execution, enslavement or an official court.'),
148: ('P-please, help me!', 'The panicked plea already works.', 'The stammer and plea follow the locals taking charge. Do not invent whom he expects to rescue him or whether the plea succeeds.'),
152: ('…', 'The captain\'s silent response already works.', 'Silence answers the plea without adding approval of a specific punishment or an explanation of his feelings.'),
164: ('…', 'Sera\'s optional silence already works.', 'Keep her silence as its own conditional turn after the handover. Do not turn it into gratitude, forgiveness or a romantic statement.'),
168: ('Sera... Remember this. There are still Westerners like him throwing their weight around all over the world.', 'The predecessor removes the explicit Western colonial-cultural reference.', 'Retain Westerners like him and the continuing worldwide abuse of power. The source criticizes that kind of Westerner, not every Westerner. Throwing their weight around is natural American English for the contemptuous idiom without weakening its power imbalance.'),
172: ("...Then again, maybe I'm not so different from them myself.", 'We changes the captain\'s explicit self-criticism into a group comparison.', 'Preserve the individual I, self-emphasis and uncertainty before Sera objects. The captain questions his own difference; he does not confess to the same specific crimes or implicate all his companions.'),
175: ('No... {MACRO:FI}... different.', 'The halting objection already works.', 'Her short learner speech rejects his self-comparison. Preserve the given-name call and hesitation without inventing a romance or replacing her voice with polished adult testimony.'),
179: ("Don't trust people blindly.", 'The practical warning against overtrust already works.', 'Blindly limits the warning to excessive trust. It does not tell her never to trust anyone or import additional language from her later departure scene.'),
186: ('{MACRO:FA}.', 'The respectful attention call already works.', 'The surname call turns the conversation toward the request. The following polite language conveys respect without adding a rank or a relationship. Macro notation is serialization only.'),
190: ("I'm sorry to put you to the test, but there's something I'd really like you to find and bring back.", 'The predecessor loses the polite personal wish, strength of desire and return request.', 'Keep the speaker\'s regret at testing the group and the request to find and bring back an object. The sentence is conversational and polite, with no invented emergency, ownership or reward yet.'),
194: ('？', 'The captain\'s puzzled reaction already works.', 'Keep the language-neutral puzzled beat before the explanation. Do not insert a question with new content.'),
198: ('Admiral, have you heard the legends about King Solomon?', 'The clipped predecessor loses the polite conversational question.', 'Retain the source\'s explicit Admiral address and legendary framing. This is a question about the tale, not a historical assertion or evidence of a new rank.'),
202: ('Legend has it that long ago, the great King Solomon could command even the demon king.', 'The predecessor pluralizes the demon king and weakens the explicit old account.', 'Preserve the singular demon king and the claim as legend. Do not identify a specific demon, equate the reference with a named religious figure, or assert the supernatural account as external historical fact.'),
206: ('Rumor has it that a weapon linked to that demon king was sealed away on an icy island far to the northwest of here.', 'The predecessor weakens the same-demon reference and omits the explicit rumor framing and here.', 'Keep the weapon associated with that same demon king, the report that it was sealed away, and the direction relative to here. Linked to does not invent ownership, a precise item identity or a confirmed location.'),
210: ("They say only someone worthy of being a conqueror can possess it. If you can bring it back...", 'True ruler and wield replace the source\'s qualification and possession; Return with it makes a conditional into an imperative.', 'Use the established conqueror vocabulary for 覇王 while retaining worthiness, hearsay and possession. If you can preserves the conditional offer and leads naturally to Then what? Do not invent a magical test, required kingship, combat use or guaranteed success.'),
213: ('Then what?', 'The short follow-up to the conditional already works.', 'The immediately preceding bring-it-back condition supplies the omitted clause in natural English. The captain asks what follows without inventing a reward or accepting the task yet.'),
217: ("Then there's something I'd like to give you.", 'The predecessor replaces an intended gift with categorical future ownership.', 'The speaker expresses an intention to give an unnamed object. Keep the object unspecified until the later offer rather than naming a weapon, map or Proof prematurely.'),
220: ('What is it?', 'The captain\'s direct question already works.', 'The brief question refers naturally to the unnamed intended gift and maintains his direct voice.'),
224: ("I can't tell you yet. Let's keep it a surprise until you return safely.", 'The predecessor loses the anticipation in お楽しみ and sounds brusque.', 'The polite speaker withholds the information and suggests leaving something to look forward to on their safe return. The wording does not promise that they will return or explain the reason for withholding it.'),
228: ("Hm... The demon king's weapon...", 'Demon arms obscures the singular weapon and king.', 'The captain thoughtfully echoes the object just described. Keep the singular weapon and demon king without assigning a specific item name or confirming the legend.'),
239: ('An icy island far to the northwest... Could that be Iceland?', 'The predecessor loses the explicit Iceland suggestion.', 'Manuel repeats the clue and tentatively proposes Iceland. Could that be preserves uncertainty; do not announce a confirmed destination or add sailing directions.'),
},
59: {
5: ('You found it?', 'The surprised question already works.', 'The question naturally expresses the speaker\'s pleased surprise at the discovery without needing a literal extra interjection or an invented item name.'),
9: ("Hmm... There's no mistaking it. In that case, I'll entrust you with this.", 'The predecessor loses recognition and changes the personal entrusting intention into we.', 'The speaker identifies the returned object, then entrusts a different object that the next turn names as a map fragment. Do not imply the weapon is being returned or invent a counterfeit test.'),
13: ('Please accept this piece of the map.', 'The polite offer of a map fragment already works.', 'The complete polite sentence preserves the fragment rather than a whole map. Its function is clear between entrusting this and the captain\'s question.'),
19: ("What's this?", 'This? is unnecessarily clipped for the source question about the offered object.', 'The captain asks about the fragment he has just been offered. A short complete conversational question keeps his directness without adding a demand or disbelief.'),
23: ("Espinosa had it. He'd been searching for Africa's Proof of Conquest for a long time, too. We'd been praying it would never fall into his hands...", 'The predecessor loses the long search and the distinction between possessing the fragment and seeking the Proof.', 'It first refers to the map fragment; the later it refers to the named Proof. Restore long-term search, too, and the wish that the Proof stay out of his hands. Preserve the established item term and the group\'s prayer without inventing a religious denomination or a successful search.'),
26: ("You are the one who should rule these waters. I hope you'll find the treasure marked on the map as soon as you can and bring peace and prosperity to this land.", 'The predecessor loses the map, urgency, prosperity and the expressed wish.', 'The respectful speaker asserts the captain\'s worthiness and wishes for prompt discovery and peace and prosperity. This land stays as local deixis rather than expanding automatically to all Africa. Preserve the aspiration without promising success or changing the map into the treasure.'),
30: ("That's a lot to expect of me... Still, thank you. I'll take it.", 'Expect little turns the captain\'s awkward response to high expectations into dismissiveness and loses explicit gratitude.', 'His wry discomfort with the expectations leads into grateful acceptance. The conversational response preserves both emotions without predicting failure or rejecting the task.'),
},
60: {
5: ('Admiral, no one is more vile than a slave trader.', 'Manuel\'s strong moral condemnation already works.', 'The formal address and forceful judgment naturally express his view that slave traders are unforgivable. Do not add a particular punishment or convert his opinion into a legal ruling.'),
8: ('？', 'The captain\'s puzzled reaction already works.', 'The silent question invites Manuel\'s explanation without adding an objection or changing the speaker relationship.'),
12: ("I once stopped in Sao Jorge as a ship's carpenter with a Portuguese fleet bound for India. I came down with an illness that was going around and had to leave the ship.", 'The predecessor omits his occupation, Portuguese fleet, India and the circulating illness.', 'Restore the complete recollection: his ship\'s-carpenter work, the fleet\'s affiliation and destination, the Sao Jorge stop and departure after illness. Illness that was going around renders はやり病 without diagnosing a named disease. A Portuguese fleet does not assert Manuel\'s nationality. Keep the established city spelling.'),
15: ('The local people saved me. They cared for me with extraordinary kindness.', 'The rescue and generous nursing already work in the illness context.', 'With the preceding illness restored, cared for clearly includes their attentive nursing. The complete sentences convey his sincere gratitude without inventing payment, a cure or a family relationship.'),
19: ('I heard the Portuguese had treated them terribly. But to them, a sick person was a sick person. They cared for me as if I were family...', 'The predecessor replaces reported mistreatment by Portuguese people with an unsupported under-Portugal political condition and drops their care for the sick regardless.', 'Keep the reported status, the Portuguese people as the agents of mistreatment, and the residents\' compassionate treatment of a sick person. As if I were family is explicitly a simile, not actual kinship. Do not invent a quoted conversation, a government or a named occupation.'),
22: ('Oh...', 'The captain\'s understated interested response already works.', 'The brief reaction gives Manuel room to continue and preserves the reserved captain\'s voice without adding a judgment or sympathy speech.'),
26: ("That's when the Lord's teaching, 'Love your neighbor,' really sank in. This place has been my second home ever since.", 'Became real sounds supernatural rather than a deeply felt personal understanding.', 'Retain the Christian reference and familiar American wording of the teaching, his personal realization and this place becoming a second home from that time onward. Do not invent a conversion, miracle, denomination or actual family tie.'),
29: ("And I swore that someday I'd fight the vile traders carrying out slave raids in Africa.", 'The predecessor loses the personal and future vow and can suggest hunting already enslaved fugitives.', 'Keep Manuel\'s own vow, someday, the unscrupulous traders and the African raids to capture people for slavery. Slave raids is precise natural English and does not turn the victims into fugitives or specify every trader\'s gender.'),
33: ('Admiral, we must defeat Espinosa!', 'The determined appeal already works.', 'The strong appeal follows his personal history and vow. Must conveys determination without asserting a guaranteed victory or naming an additional enemy.'),
36: ('Yes. Of course.', 'The captain\'s firm assent already works.', 'His concise agreement completes the exchange in his direct voice without adding an oath, operational plan or new promise.'),
},
}

CONTEXTS = {
54: 'A Port Worker asks whether the captain is a newcomer; the puzzled captain assents, the worker repeats the acknowledgment and chuckles after wishing him luck, and the captain remains puzzled. The source does not disclose the worker\'s motive.',
55: 'A Port Worker checks the captain\'s surname and military identity, then relays the guild contact\'s request from Veracruz. This is one complete message, not a proven immediate continuation of B54.',
56: 'After the linked release-of-captives context, the captain asks whether the foreign girl will leave with the others. The FE caption records her silence. He recalls that she differs ethnically from the other captives and recommends temporary local care. B15/37/142 supply source context, not fresh completed localization or observed natural activation.',
57: 'Sera cautiously tries newly learned words to thank the captain. He notices, is surprised at her learning, praises her, then responds awkwardly to the repeated thanks. Preserve her halting speech respectfully and his reserved warmth. The full introduction in B142 supports the short name; the later B65 departure does not establish a romance here.',
58: 'Locals bring Espinosa before the captain, protest his abuses, reject his excuses and ask the captain what to do. Conditional companion reactions and the conditional Sera recognition/accusation/admission/self-doubt exchange are reviewed only on their mapped structural paths. Locals take charge of Espinosa, then the Shopkeeper asks the group to recover a rumored weapon and offers an unspecified object in return. Manuel may tentatively suggest Iceland. None of the 64 structural path models proves native event eligibility or real future state; opaque effects remain unclaimed.',
59: 'The Shopkeeper recognizes the recovered object and entrusts a map fragment to the group. He explains Espinosa\'s possession of the fragment and search for the Proof, expresses hope for this land\'s peace and prosperity, and receives the captain\'s wry but grateful acceptance. Do not conflate the returned weapon, fragment, Proof and mapped treasure.',
60: 'Manuel explains his condemnation of slave traders through a personal account of illness, local care despite Portuguese mistreatment, deeply felt neighbor-love and a vow to fight slave raids. The captain listens briefly and agrees to oppose Espinosa. Preserve hearsay, place, occupation, fleet destination, religious reference and family simile.',
}
SPEAKERS = {1: 'Hodram', 20: 'Fernando', 23: 'Manuel', 24: 'Sera', 36: 'Geronimo Espinosa', 84: 'Shopkeeper', 113: 'Port Worker', 114: 'Port Worker', 119: 'Port Worker', 141: 'Innkeeper', 254: 'System panel caption: Foreign Girl'}

def normalized_previous(text):
    return re.sub(r'\b(FI|FA|FO)\b', lambda m: '{MACRO:'+m[1]+'}', text)

if __name__ == '__main__':
    assert not ROOT.exists() and not DOC.exists()
    current, gloss, view, paths, names = map(read, [CURRENT, GLOSS, VIEW, PATHS, NAMES])
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger_before = ledger_path.read_bytes(); ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 7237 and ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert current['source_first_glosses_andcomplete_native_page_view_precede_current_English'] and current['all82_source_units_uncredited_in_current_ledger']
    assert view['all82_source_native_pages_and11_sheets_directly_viewed']
    assert len(names['records']) == 10 and len(paths['models']) == 64
    completed = {historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not completed & {historical_key(r) for r in current['records']}
    city = read(CITY_TERMS); proof = read(PROOF_TERMS); ruler = read(RULER_TERMS)
    term_rows = [next(r for r in city['records'] if r['id'] == ident) for ident in ['DK4_MES_B36_R0001', 'DK4_MES_B36_R0007']]
    assert 'Sao Jorge' in term_rows[0]['english'] and 'Veracruz' in term_rows[1]['english']
    proof_row = next(r for r in proof['records'] if r['id'] == 'COMMON_MESSAGE_3209')
    ruler_row = next(r for r in ruler['records'] if r['id'] == 'COMMON_MESSAGE_3105')
    assert '覇者の証' in proof_row['japanese'] and "Africa's Proof of Conquest" in proof_row['english']
    assert '覇王' in ruler_row['japanese'] and 'conqueror' in ruler_row['english']
    membership = {r['id']: r for r in paths['utterance_membership']}
    rows = []; macro_counts = dict(FI=0, FA=0, FO=0)
    for original in current['records']:
        row = deepcopy(original); text, finding, reason = LINES[row['block']][row['source_record_index']]
        assert text == text.strip() and not any(v in text for v in ['\n', '\r', '{LB', '{ALIGN', '{PAD', '  ', '%'])
        text.encode('cp932')
        old = normalized_previous(row['effective_predecessor_paragraph'])
        decision = 'retention' if text == old else 'revision'
        for macro in macro_counts:
            source_n = bytes.fromhex(row['source_hex'])[1:].count(macro.encode('ascii'))
            assert text.count('{MACRO:'+macro+'}') == source_n
            macro_counts[macro] += source_n
        path_neighbors = []
        models = paths['models'] if row['block'] == 58 else [dict(model=None, source_speech_IDs=[r['id'] for r in current['records'] if r['block'] == row['block']])]
        for model in models:
            ids = model['source_speech_IDs']
            if row['id'] not in ids: continue
            at = ids.index(row['id'])
            pair = dict(previous=ids[at-1] if at else None, following=ids[at+1] if at+1 < len(ids) else None)
            found = next((v for v in path_neighbors if v['previous'] == pair['previous'] and v['following'] == pair['following']), None)
            if found: found['structural_models'].append(model['model'])
            else: path_neighbors.append(dict(**pair, structural_models=[model['model']]))
        assert path_neighbors
        row.update(english=text, logical_English=text, speaker=SPEAKERS[row['source_selector']], source_meaning=row['first_clean_source_gloss'],
            context=CONTEXTS[row['block']], localization_note=reason, finding=finding, decision=decision,
            retention_reason=reason if decision == 'retention' else None,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            whole_clean_utterance_andalternate_branches_read=True, read_aloud_cadence_andemotional_progression_reviewed=True,
            exact_structural_neighbor_pairs=path_neighbors, structural_membership=membership.get(row['id']),
            structural_neighbors_not_actual_reachability_orcontinuous_event_chronology=True,
            prior_raw_storage_preserved=row['current_raw_storage_English'], prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],
            prior_macro_normalized_comparison=old, planned_English_markup='{SPEAKER:'+format(row['source_selector'], '02X')+'}'+text,
            no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
            source_controls_andruntime_substitutions_must_remain_exact=True,
            formatting_native_stored_actual_policy_atomic_andregistered_integration_pending=True,
            source_meaning_only_not_localized_orformatting_approval=False,
            prior_source_only_andpending_flags_preserved_in_immutable_current_packet=True,
            no_source_prose_counter_orcompletion_credit=True, source_prose_orcompletion_credit_added=False)
        rows.append(row)
    assert len(rows) == sum(map(len, LINES.values())) == 82
    assert macro_counts == dict(FI=3, FA=4, FO=0)
    revisions = sum(r['decision'] == 'revision' for r in rows); retentions = len(rows)-revisions
    evidence_paths = [CURRENT, GLOSS, VIEW, PATHS, NAMES, CITY_TERMS, PROOF_TERMS, RULER_TERMS, Path(__file__)]
    save(DOC, dict(format='dk4-whole-exchange-editorial-manuscript-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'], current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'], current_archive_sha256=current['current_archive_sha256'],
        file_path='/data/SC1.DK4', blocks=list(LINES), records=rows, typed_choice_records=[], total_editorial_objects=82,
        physical_speech_objects=82, typed_choice_objects=0, revised=revisions, retained=retentions, names_packet=str(NAMES), names_packet_sha256=sha(NAMES.read_bytes()),
        source_context=str(GLOSS), source_context_sha256=sha(GLOSS.read_bytes()), current_packet=str(CURRENT), current_packet_sha256=sha(CURRENT.read_bytes()),
        source_native_view=str(VIEW), source_native_view_sha256=sha(VIEW.read_bytes()), source_macro_counts=macro_counts,
        source_FE_panels=1, source_relative_sites=24, source_query_sites=6, source_commands=152,
        approved_term_references=dict(city_rows=term_rows, proof_row=proof_row, conqueror_vocabulary_row=ruler_row,
            city_source_spellings_in_this_batch=['ヴェラクルス', 'サン＝ジョルジェ'],
            city_reference_is_existing_terminology_not_clean_dialogue_translation_authority=True),
        all82_clean_first_glossed_andnative_viewed_before_current_English=True, whole_exchange_andalternate_branch_context_reviewed=True,
        all_four_prose_gates_true_all_formatting_gates_false=True, ordinary_wrapping_owned_by_formatter=True,
        FE_body_caption_is_not_actor254_nameplate=True, Geronimo_Alonso_fullname_de_shared_field_still_open=True,
        no_all207_fullcatalogue_customname_ornew_actual_gameplay_approval=True,
        no_new_ROM_registered_integration_orcompletion_credit=True, new_credit=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in evidence_paths}))
    ROOT.mkdir(parents=True)
    save(ROOT/'contextual_review.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()),
        records=[{k:r[k] for k in ['id','source_reference','source_hex','source_Japanese','current_reference','current_hex','prior_effective_paragraph_preserved','english','decision','finding','localization_note','retention_reason','exact_structural_neighbor_pairs','review']} for r in rows],
        revisions=revisions, retentions=retentions, source_macro_counts=macro_counts,
        all82_individual_prose_decisions_recorded=True, all_four_prose_gates_true_all_formatting_gates_false=True,
        names_ten_progressive_retentions_andopen_fullname_lead_reused_not_recredited=True,
        formatting_stored_native_actual_andregistered_integration_still_pending=True,
        no_ROM_registry_orcompletion_credit_change=True, new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in evidence_paths+[DOC]}))
    assert ledger_path.read_bytes() == ledger_before
    print(f'82 contextual decisions: {revisions} revisions / {retentions} justified retentions. FI3/FA4/FO0. Formatting pending; zero credit.')
