"""Record complete-exchange decisions after all400 independent source drafts were sealed."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.draft_hodram_B311_B324_clean_v1 import ROOT, OUT as DRAFTS, MEANINGS
from scripts.review_hodram_B231_B250_contextual_v1 import mark_macros

CURRENT = ROOT / 'current_v1/current_effective.json'
OBJECTS = ROOT / 'current_objects_v1/current_objects.json'
OUT = Path('translations/hodram_B311_B324_contextual_review_v1.json')

RETAIN = {
311: {
113: 'The frightened cry is natural and exactly matches the independent draft.',
117: 'The urgent inclusive run order is natural and exactly matches the independent draft.',
156: 'The immediate jump-into-the-brush order is natural and preserves the escape action without inventing a side.',
176: 'The clipped welfare question is idiomatic immediately after escaping danger and addresses everyone.',
180: 'Aye naturally answers the captain’s welfare question in the sailor’s informal nautical voice.',
189: 'The alternate urgent welfare check is natural and addresses the whole group.',
193: 'The sailor’s alternate affirmative naturally answers the group welfare check.',
239: 'The urgent questioning exclamation naturally asks what caused the companion’s scream.',
270: 'The panicked flight shout preserves the sailor’s alarm without requiring a phonetic scream.',
278: 'The short distressed refusal is natural after the frantic run and conveys having had enough.',
327: 'The complete exclamation naturally expresses how frightening the escape was.'},
312: {13: 'The interested echo and complete map-location question naturally prompt Silvia’s admission that she does not know.'},
313: {
68: 'The startled cry naturally conveys the sailor’s shock; a written stammer is unnecessary.',
96: 'The nervous hesitation and short what-now question naturally ask the captain’s plan.',
242: 'The quiet-retreat order and warning not to provoke the scorpions are complete and natural.',
275: 'The conventional sound effect exactly matches the draft and connects to dropped baggage.',
331: 'The urgent run-through command is idiomatic and preserves the requested quick dash.',
355: 'The excited but qualified arrival judgment is natural and preserves the source uncertainty.'},
314: {
6: 'The simple greeting naturally welcomes the visitor.',
30: 'The noncommittal reaction naturally conveys Rafael’s mild interest without inventing enthusiasm.',
35: 'In the exchange, the short recollection marker naturally introduces the additional pirate warning.',
47: 'The casual farewell is natural for Verisa and adds no relationship.'},
315: {6: 'The warm welcome naturally introduces the grateful follow-up visit.'},
316: {
104: 'The tentative onward suggestion is natural after the fog choice and preserves trying to advance.',
254: 'The conventional system notice exactly preserves one elapsed day.'},
317: {
93: 'Sir is a natural respectful address to the established admiral; it creates no new rank or participant.',
108: 'The restrained dismissal and onward decision are natural for Hodram in the dark cave.',
147: 'The disoriented location question exactly matches the independent draft.',
180: 'The startled identification and swarm observation are natural during the bat encounter.',
206: 'The brisk dismissal and continued-advance order naturally preserve ignoring the bats.'},
318: {
12: 'The natural map-first request includes returning with it; it does not claim a gift or ownership transfer.',
48: 'The emphatic surprised question naturally answers the revelation that the ruins are off-island.',
54: 'The complete necessity statement naturally explains the sea crossing.',
59: 'The direct return-to-port proposal is idiomatic for Hodram’s practical response to the required crossing.',
66: 'The guide’s complete qualification claim and secrecy requirement are natural, without a new eligibility rule.',
75: 'The conventional system notice exactly preserves one elapsed day.',
79: 'The arrival statement and overland continuation are complete and natural.',
82: 'The stammered surprised reaction is natural for Rafael’s unexpected encounter.',
125: 'Hodram’s restrained acceptance and shared-search proposal are complete and natural.',
128: 'The brief agreement exactly matches the independent draft.',
136: 'The excited pointing call naturally identifies the ruins as one destination; English need not use a plural here.'},
319: {
5: 'The friendly greeting naturally welcomes the visitor.',
9: 'The complete village question naturally opens the rumored-monk exchange.',
17: 'The preceding customer attribution supplies hearsay; this natural follow-up preserves finding the village, disappearance and concern.'},
320: {
16: 'The resident’s deduction and confirmation question naturally introduce the useful sextant without naming the return gift.',
20: 'The surprised question exactly matches the independent draft.',
35: 'The natural short challenge keeps the return gift a surprise until the sextant is brought.'},
321: {6: 'The acknowledgment and natural exchange offer preserve the requested instrument and unnamed return gift.'},
322: {83: 'The professional survey-start announcement and Sofala-guild report request are complete and natural; no result or deadline is added.'},
323: {
6: 'The solemn confirmation question naturally asks whether this is the object sought without naming it.',
13: 'The measured trust declaration and invitation to accept are natural and preserve the solemn handover.'},
324: {
5: 'The surprised recognition question naturally establishes the shared topic of the monk.',
9: 'The brief echo naturally confirms that the resident knows of the monk; it invents no personal relationship.',
16: 'The witness’s natural account conveys the medicine rapidly stopping the illness and his sense of a miracle.',
20: 'The complete medical-knowledge question exactly matches the independent draft.',
28: 'The gesture and complete authorship statement naturally introduce the book.',
39: 'Lil’s incomplete recognition is natural before the conditional book-identification response.',
58: 'The excited recognition and discovery exclamations naturally preserve Charles’s earlier mention of the book.',
69: 'The concerned surprise question is idiomatic after Charles’s excited outburst.',
77: 'The research report and trailing reservation naturally preserve the learned prerequisite without claiming a new material was obtained.',
84: 'The clipped apology and lack-of-time explanation are natural for Hodram interrupting the rambling explanation.',
90: 'The direct location question naturally returns the exchange to the missing monk.',
102: 'The resident’s conversational comparison naturally links the monk’s illness to drinking the same local water.',
105: 'The emotional account naturally preserves concealment and giving every dose to the villagers.',
109: 'Passed away is a natural, unambiguous death euphemism in the grieving witness’s voice; messenger of God preserves his praise without canonization.',
116: 'The complete respectful entrustment request is natural after the grief pause.',
123: 'The complete book-description sentence naturally preserves an ore no one has seen.',
126: 'The measured statement preserves the resident’s conviction that the ore must be buried somewhere in the world.',
129: 'The complete research-succession request naturally asks the party to find the ore without inventing a named metal.',
133: 'Hodram’s complete sincere promise is natural and needs no extra pause marker.',
144: 'Charles’s emphatic agreement and thorough-investigation pledge are natural; the collective promise does not invent a new participant.'},
}

FIND = {
311: {
84: 'Replace the full-width question mark with an idiomatic voiced questioning reaction; native glyph checking remains.',
172: 'Preserve companion silence with consistent ASCII periods rather than a mixed full-width ellipsis.',
185: 'Preserve the alternate companion silence with consistent ASCII periods.',
274: 'Use breath sounds, not the spoken stage direction Pant.',
284: 'Restore apparent fatigue rather than definite exhaustion.',
290: 'Restore the stern instruction not to lose heart or complain, rather than substituting a generic onward command.',
323: 'Express collective relief naturally rather than the isolated label Safe; no rescuer is invented.'},
312: {
6: 'Give the forgotten message a complete conversational lead-in rather than the clipped almost-forgot phrase.',
10: 'Restore recent discovery, pictorial-map description and reported uncertainty; the old text asserts the location as narrator-certified fact.',
16: 'Preserve the apology, lack of map-location knowledge and conditional suggestion if interested, rather than a bare searching instruction.'},
313: {
65: 'Make the desert-heat acknowledgment and onward decision sound like speech rather than a terse informational label.',
92: 'Use the calming command Calm down, not the isolated adjective Calm.',
115: 'Leave it to me reassures the party; My turn introduces an unsupported turn-taking implication.',
139: 'Restore the complete promise to drive the scorpions off; standalone Drive is incomplete and ambiguous.',
162: 'A strained pain sound does not introduce the old explicit curse.',
189: 'Keep the explicit source curse and restore the natural admission of letting his guard down.',
228: 'Make the one-day treatment stay a complete system notice while preserving FI and avoiding a promise of recovery.',
236: 'Replace the disconnected Better fragment with Hodram’s complete reassurance that he is now all right.',
279: 'Use the sailor’s mistake exclamation and falling baggage without adding profanity or a permanent cargo-loss claim.',
303: 'Use a pain/alarm cry suited to the apparent injury, rather than the milder surprise Whoa.',
336: 'Preserve apparent sailor injury rather than asserting it as confirmed.'},
314: {
10: 'Restore the conversational have-you-heard question, use the registered Goryeo Incense Burner item title and explicitly preserve celadon and reported East Asian location.',
14: 'The claim is more accurate fortune-telling, not exact or infallible divination. Restore Verisa’s personal wish to try it.',
39: 'Preserve the reported nearby pirate activity and make the equipment advice conversational.',
43: 'Give Rafael a natural surprised response, complete danger assessment, thanks and personal promise of caution.'},
315: {
10: 'Make the gratitude and offered reading conversational and explicitly connect improved readings to the burner the visitor gave her.',
14: 'Use a warm natural invitation to sit rather than the stiff Come, sit there.',
18: 'Preserve the diviner’s silence with consistent ASCII periods.',
22: 'Preserve the captain-role silence with consistent ASCII periods.',
26: 'Restore the far-inland location and the diviner’s confident prediction; do not turn her description into an unexplained travel order or a narrator-certified reward.'},
316: {
144: 'Preserve the resolve to advance even if cutting through trees is necessary, not only an isolated cutting order.',
174: 'Restore apparent fatigue rather than definite exhaustion.',
179: 'A way around the dead end is more specific than an unspecified path.',
214: 'Wait for this fog to clear, not for unspecified clear skies. Keep the danger judgment and waiting decision as speech.',
243: 'Preserve the first shorter wordless pause using consistent ASCII punctuation.',
247: 'Preserve the following longer wordless pause using ASCII punctuation, without manual line breaks.',
258: 'Restore seems clear and a natural departure call rather than the labels Clear now and Depart.'},
317: {
63: 'Make Hodram’s breath, humidity observation and concern for the exhausted party natural spoken English without assigning every party member a gender.',
89: 'Restore the darker-than-expected comparison, not only darkness.',
113: 'Preserve tactile recognition and its unfinished reveal rather than replacing it with a generic object question.',
116: 'The interrupted warning concerns a party member, not specifically a sailor. Do not finish it with a bite or death.',
127: 'Preserve Samwell’s specific Indian-python identification and self-doubting comic aside.',
133: 'Use an urgent danger assessment and general retreat order without adding the old curse.',
141: 'Preserve apparent injury rather than confirmed injury.',
176: 'Make Hodram’s choice to light a fire complete and natural without adding a torch.',
214: 'Restore apparent fatigue rather than definite exhaustion.'},
318: {
44: 'Restore the guide’s hesitant disclosure and qualified off-island conclusion.',
63: 'Preserve the prepared small boat and planned continuation without inventing oars or a rowboat.',
94: 'Restore the company identity and recognition question; Castor is not a new location or rank.',
100: 'Use a natural question addressed to the unknown person rather than the isolated Who.',
109: 'Restore Rafael’s complete account of the accompanying guide’s request and getting lost, without inventing a friend or gender.',
114: 'Restore the indiscriminate-recruitment callback to clean B287R104; sent everywhere changes the meaning.',
117: 'Restore no news from the searchers and the personal decision to accompany this expedition, rather than addressing only Rafael or implying deaths.',
121: 'Make Rafael’s self-blame natural rather than a stiff declaration of physical weakness.',
132: 'Make Rafael’s agreement and invitation to search together complete and natural.',
165: 'Keep the immediate coming response and complete its punctuation.'},
319: {
13: 'Restore the customer’s complete historical account, the monk’s respected status and journey to the northern continent long ago, without an invented clerical rank.',
21: 'Use a restrained uncertain answer suited to Hodram rather than the unusually casual Dunno.',
25: 'Preserve the hope that the people he preached to grew fond of him; new flock implies a congregation not established by the source.',
28: 'Preserve the conditional request if the captain goes north, rather than ordering a new trip.'},
320: {
5: 'Make the unfamiliar-face observation a natural personal question without adding ethnicity or a chief title.',
8: 'Preserve Sweden in northern Europe, not only the vague up north.',
12: 'Keep the resident’s inference of a distant origin rather than an unqualified travel fact.',
24: 'Use a natural personal hearsay report and preserve sea positioning without landmarks.',
28: 'Make the barter offer sound like a resident speaking, not a quest-reward announcement, and keep the gift unnamed.',
31: 'The echo follows something good; it should not reintroduce a reward label after the barter wording changes.'},
321: {14: 'Use a complete, directionally clear notice that the player handed over the Sextant.'},
322: {
71: 'Make the player’s provision of all money for initial expenses explicit; the passive label can obscure spending versus income.',
76: 'Preserve exactly 1,000 gold coins and the outward funding direction in a complete notice.'},
323: {10: 'Give the long wait and day finally arriving complete, solemn English rather than At last, today.'},
324: {
13: 'Restore the monk’s compassion and tireless care as the reason the village escaped being wiped out, without implying confirmed contagion.',
24: 'Preserve the witness’s vague secondhand account of alchemy removing mineral poison; do not assert a named toxin or new medical explanation.',
65: 'Use the existing Alchemy Book title and a natural excited reaction without a literal To find fragment.',
73: 'Give Charles a natural first-person account of recently hearing the discovery rumor; keep it reported.',
81: 'Preserve the clue to precious metal and rambling interest using actual hesitation, not the spoken stage direction Mutter.',
94: 'Preserve the grieving witness’s silence with consistent ASCII punctuation.',
98: 'Use a voiced questioning reaction rather than a full-width question glyph in otherwise ASCII dialogue.',
112: 'Preserve the captain-role silence with consistent ASCII punctuation.',
119: 'Echo the entrustment of the book clearly rather than the different and ambiguous standalone Trust.',
148: 'Preserve finding the ore, a fleet command in that region and freedom to research. The source does not require bringing the ore back or make him ruler/admiral of a whole region.'},
}

# Individually selected physical offsets; all exact-equal drafts are also retained.
STYLE_RETAIN = {
(311,24): ({0,82,132,182,220,270,324}, 'The map requirement and route uncertainty are idiomatic for this voice; no embellishment is needed.'),
(311,436): ({0,28,46,74,118,140,172}, 'The brief spoken observation naturally conveys this variant’s forest darkness or density.'),
(311,654): ({0,28,52,78,102}, 'The hesitant attention call naturally alerts the admiral to the audible sound.'),
(311,838): ({44,96}, 'The urgent rock-behind-us warning is natural; a phonetic opening cry is unnecessary.'),
(311,1124): ({0,46,70,88,114}, 'The short alarm naturally announces a dead end in an urgent escape.'),
(311,1500): ({18}, 'The long nonlexical scream naturally preserves fear; phonetic vowel choice need not change.'),
(311,1578): ({0,14,28,46,68,80,96}, 'The immediate snake alarm is idiomatic; a literal phonetic stammer is unnecessary.'),
(311,1918): ({34,68,104,130,190}, 'The relieved directional report naturally conveys the rock taking the left route, without giving it deliberate agency.'),
(311,2220): ({0,24,50,74}, 'The natural pointing call preserves the admiral address and discovery without naming it prematurely.'),
(313,24): ({226}, 'The complete map warning naturally fits the youthful concern without requiring elongated spelling.'),
(313,376): ({34,60}, 'The short heat complaint is natural for the blunt or groaning voice.'),
(313,546): ({28,54,80,140}, 'The alarm naturally identifies the scorpions and the variant’s fear or quantity emphasis.'),
(313,856): ({56,136,234,278}, 'The natural praise preserves flight and this variant’s admiration or dependability remark.'),
(313,1252): ({56,136,234,278}, 'The alternate successful branch naturally preserves flight and this variant’s admiration or dependability remark.'),
(313,1624): ({0,28,50,74}, 'The urgent welfare question or admiral-only cry is idiomatic immediately after the captain’s injury.'),
(313,2118): ({40}, 'The direct move-out order and quiet instruction are natural for this decisive voice.'),
(313,2472): ({16}, 'The short startled interjection naturally reacts to the fallen baggage.'),
(316,24): ({36,68,140,176,214}, 'The map warning or request is natural for this direct, casual or older-register voice.'),
(316,348): ({0,22,40,56,80,100,124}, 'The complete departure call naturally preserves this voice’s politeness or energy without inventing a train.'),
(316,520): ({56,76}, 'The natural fog observation preserves the weather change or emphatic thickness of this source variant.'),
(316,754): ({0,66,82,132}, 'The natural dead-end observation preserves this variant’s qualification, pause or mild surprise.'),
(316,1010): ({0,14,32,152}, 'The natural attempt response preserves this variant’s agreement, skepticism or renewed resolve after the cutting order.'),
(316,1310): ({0,30,58,94,122,182,210}, 'The natural discovery call preserves the fork, alternate path or pointing gesture in this variant.'),
(316,1634): ({0,28,42,56,78,104}, 'The natural agreement preserves this variant’s assessment and acceptance of waiting for the fog.'),
(316,1916): ({18,32}, 'The immediate sighting call naturally reports the destination coming into view.'),
(317,446): ({0,16,36,62,84,100}, 'The concise departure call is natural and preserves this variant’s register without added characterization.'),
(317,654): ({0,24}, 'The short surprised cave discovery is natural, without naming new landmarks.'),
(317,1114): ({0,46,76,180,230}, 'The natural location response preserves uncertainty about emerging near the ruins, without placing the party inside them.'),
(317,1648): ({0,18,82,100,170}, 'The urgent bat reaction naturally preserves excessive numbers, inability to advance or revulsion, as this source variant requires.'),
(317,1974): ({0,44,66,102,132,168,202}, 'The natural relieved celebration preserves escaping the jungle, without inventing an additional success.'),
(317,2252): ({28,50,70,120}, 'The brief recognition call naturally identifies the ruins for this non-tentative source variant.'),
(318,96): ({56,92,128,166,208,310}, 'The natural observation or trailing wonder preserves the ancient city once standing here; no expanded historical detail is needed.'),
(318,1420): ({134}, 'The complete pointing statement naturally identifies the ruins for the youthful voice.'),
(322,8): ({26,48,90}, 'The immediate going-ashore announcement is idiomatic and does not prematurely declare the party already landed.'),
}

STYLE_FIND = {
(311,24): 'Restore the explicit recklessness judgment instead of only inability to proceed.',
(311,436): 'Use an actual spoken darkness observation rather than the label Dark woods.',
(311,654): 'Preserve the youthful speaker hearing something and trailing off, without flattening every voice to the same question.',
(311,838): 'Restore this variant’s natural warning and the rock’s source direction or falling motion; chasing can imply agency absent from the Japanese.',
(311,1124): 'Keep the source dead-end alarm idiomatic in the complete escape.',
(311,1460): 'Preserve the brief questioning reaction.',
(311,1500): 'Preserve the frightened nonlexical scream.',
(311,1578): 'This time the threat is a snake; Another snake incorrectly implies an earlier snake encounter in this exchange.',
(311,1918): 'Make the directional report complete and preserve the rock rolling down the left path.',
(311,2220): 'Preserve the urgent pointing call.',
(313,24): 'Restore complete natural map warnings and this physical voice’s register instead of flattening most alternatives to the same clipped No map phrase.',
(313,376): 'Use a natural spoken heat complaint suited to this voice rather than a terse descriptive label.',
(313,546): 'Preserve this variant’s explicit scorpion swarm and urgent admiral address.',
(313,856): 'Restore the specific reassurance that the admiral can be relied upon, not only generic impressive ability.',
(313,1252): 'In the alternate successful branch, restore the specific reassurance that the admiral can be relied upon.',
(313,1624): 'Preserve the urgent welfare reaction.',
(313,1756): 'Give the injured captain a clear urgent-treatment response and preserve the physical voice’s register instead of treating him as an unspecified it.',
(313,2118): 'Preserve the quiet repeated caution and the variant’s gentle, casual or youthful movement call rather than flattening all voices to a military move-out order.',
(313,2472): 'Use an idiomatic alarm or dismayed realization rather than the label Bad or an unnecessary curse.',
(313,2556): 'Preserve the welfare question and encouragement to hang on without suggesting an unstated loss of consciousness.',
(316,24): 'Restore this variant’s qualified risk or formal warning, rather than flattening every voice to a definite getting-lost statement.',
(316,348): 'Preserve the departure suggestion.',
(316,520): 'Make the developing fog a natural observation, without adding heavy fog to a variant that only reports its arrival.',
(316,754): 'Preserve the disappointed dead-end discovery in this conversational or youthful voice.',
(316,1010): 'Restore this variant’s personal commitment, determination to go all the way or natural complaint that too much is being asked.',
(316,1310): 'Preserve the older voice’s qualified judgment that this way seems passable.',
(316,1634): 'Preserve the safety assessment without strengthening it into a superlative guarantee.',
(316,1916): 'Make the sighting a natural observation or question instead of Now in view or the awkward question There it is?',
(317,24): 'Preserve wandering aimlessly, the variant’s danger or inability judgment, and the blunt voice’s explicit refusal; retain the actual map reference only where spoken.',
(317,446): 'Preserve the departure call.',
(317,654): 'Preserve the cave discovery.',
(317,1114): 'Give the uncertain emergence a natural location response. Near the ruins is not these look like ruins.',
(317,1648): 'Preserve the surprised concern that this number of bats is abnormal, not merely an enormous swarm.',
(317,1974): 'Preserve the relieved jungle-exit celebration.',
(317,2252): 'Restore apparent arrival or completed reaching of the ruins, rather than only pointing at them or putting them ahead.',
(318,96): 'Restore explicit disbelief in this physical voice, or give the youthful town-once-here observation natural word order.',
(318,1420): 'Use natural complete discovery reports and retain qualified seems-found variants rather than making every discovery definite.',
(322,8): 'Announce putting the survey party ashore; do not turn the speaker’s intended action into an order or report a completed landing prematurely.',
}

CHOICE_RETAIN = {(311,1086,0), (311,1086,1), (313,782,2), (316,674,0), (316,934,0)}
CHOICE_FIND = {
(311,1306): 'Explicitly identify the brush on each side, distinguishing this hiding choice from the earlier left/right path choice.',
(313,782): 'Fight does not promise killing scorpions; Drive them off expresses expulsion and avoids standalone Drive’s steering ambiguity.',
(316,674): 'Specify waiting for the fog to clear; Wait for clear is incomplete English.',
(316,934): 'Find a way around preserves an alternate route around the obstacle, rather than an unspecified path.',
(317,764): 'Use natural action captions and preserve feeling the way or lighting a fire, without adding a torch.'}

FINAL = {
(317,63): "Whew. It's humid here. I'm concerned about how worn out the party is getting...",
(318,114): 'So you were asked "at random," too.',
(318,165): 'Coming!',
}

def main():
    assert not OUT.exists()
    draft, current, objects = map(load, [DRAFTS, CURRENT, OBJECTS])
    assert current['runtime'] == objects['runtime']
    assert current['records'] == 151 and objects['native_style_getter_cases'] == 304
    bound = {r['id']: r for g in current['groups'] for r in g['records']}
    bound.update({r['id']: r for r in objects['style_records'] + objects['choice_records']})
    assert len(bound) == len(draft['records']) == 400
    rows, glyphs, used_retentions, used_findings = [], [], set(), set()
    for original in draft['records']:
        row = deepcopy(original)
        old = bound[row['id']]
        assert all(row[k] == old[k] for k in ['source_reference', 'source_hex', 'source_Japanese'])
        for key, value in old.items():
            if key.startswith('current_') or key == 'selected_native_pointer':
                row[key] = deepcopy(value)
        prior = mark_macros(old['current_comparison_paragraph'], row)
        english = row['english']
        kind = row.get('kind')
        if kind == 'actor-style-alternative':
            key = (row['block'], row['source_command_offset'])
            physical = int(row['id'].rsplit('_', 1)[1])
            offsets, retention = STYLE_RETAIN.get(key, (set(), None))
            if physical in offsets:
                english = prior
                reason = retention + ' Individual source requirement: ' + row['source_meaning']
                used_retentions.add((key, physical))
            else:
                reason = STYLE_FIND[key] + ' Individual source requirement: ' + row['source_meaning']
        elif kind == 'typed-choice-label':
            key = (row['block'], row['source_command_offset'], row['source_index'])
            if key in CHOICE_RETAIN:
                english = prior
                reason = 'The existing caption naturally preserves this exact action and branch order: ' + row['source_meaning']
            else:
                reason = CHOICE_FIND[key[:2]] + ' ' + row['source_meaning']
                if key[:2] == (311,1306):
                    english = ['Brush on the left', 'Brush on the right'][row['source_index']]
        else:
            key = (row['block'], row['source_reference']['record_index'])
            retention = RETAIN.get(key[0], {}).get(key[1])
            if retention:
                english = prior
                reason = retention
                used_retentions.add(key)
            else:
                reason = FIND[key[0]][key[1]]
                english = FINAL.get(key, english)
                used_findings.add(key)
        if english == prior and kind == 'actor-style-alternative' and not (physical in offsets):
            reason = 'The existing English exactly matches the independent source draft and naturally preserves this variant: ' + row['source_meaning']
        english.encode('ascii')
        assert english == english.strip() and not any(t in english for t in ['{LB', '{ALIGN', '{PAD}', '\n', '\r', '%'])
        assert all(english.count('{MACRO:'+m+'}') == row.get('source_macros', {}).get(m, 0) for m in ['FI', 'FA', 'FO'])
        decision = 'retention' if english == prior else 'revision'
        if any(ord(c) > 127 for c in prior) and english != prior:
            glyphs.append(dict(id=row['id'], current_reference=row['current_reference'], current_text=prior,
                               target_text=english, kind='scoped-ASCII-question-or-silence-consistency', fresh_display_checks_pending=True))
        row.update(english=english, logical_English=english, decision=decision, finding=reason,
                   retention_reason=reason if decision == 'retention' else None, localization_note=reason,
                   current_comparison_paragraph=old['current_comparison_paragraph'],
                   independent_clean_draft_reference=dict(path=str(DRAFTS), id=row['id'], sha256=digest(DRAFTS)),
                   current_English_conversation_comparison_pending=False, current_ROM_English_unconsulted=False,
                   current_English_now_exposed=True, earlier_English_unconsulted=False,
                   clean_first_draft_not_final_comparison_approval=False, source_only_not_final_English=False,
                   source_current_complete_exchange_comparison_complete=True, new_credit=0)
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        rows.append(row)
    assert used_findings == {(b, i) for b, values in FIND.items() for i in values}
    assert {(b, i) for b, values in RETAIN.items() for i in values} <= used_retentions
    assert {((b, command), offset) for (b, command), (offsets, _) in STYLE_RETAIN.items() for offset in offsets} <= used_retentions
    counts = dict(Counter(row['decision'] for row in rows))
    assert sum(counts.values()) == 400
    save(OUT, {**draft, 'records': rows, 'counts': counts, 'remaining_contextual_comparisons': 0,
               'all_four_individual_prose_gates_pass': True, 'all_formatting_gates_pending': True,
               'scoped_native_names_terms_anddisplay_still_pending': True, 'current_English_comparisons': 400,
               'current_binding': str(CURRENT), 'current_binding_sha256': digest(CURRENT),
               'current_objects': str(OBJECTS), 'current_objects_sha256': digest(OBJECTS),
               'current_ROM': current['current_ROM'], 'current_ROM_sha256': current['current_ROM_sha256'],
               'native_runtime': current['runtime'], 'findings_requiring_fresh_display_checks': glyphs,
               'native_substitutions_require_fresh_changed_body_checks': True,
               'no_new_font_artwork_orengine_changes': True, 'prose_only_no_new_ROM_orregistered_credit': True,
               'full_goal_complete': False, 'new_credit': 0,
               'evidence': {str(p): digest(p) for p in [DRAFTS, MEANINGS, CURRENT, OBJECTS,
                   ROOT / 'draft_name_reference_v1.json', ROOT / 'draft_item_reference_v1.json',
                   ROOT / 'linked_clean_recruitment_context_v1.json', Path(__file__)]}})
    print('Saved400 contextual decisions:', counts, '; glyph targets:', len(glyphs), '; all display checks remain.')

if __name__ == '__main__':
    main()
