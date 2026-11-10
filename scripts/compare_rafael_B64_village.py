"""Compare the complete village exchange after sealing its clean-source drafts."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.compare_rafael_B61_B63 import current_paragraph

ROOT = Path('work/analysis/Rafael_B61_B80_clean_20261104')
RETAIN = {
5: 'The natural surprised observation preserves discovering a village this far away.',
17: 'The short question naturally responds to the nearby commotion; the scene supplies its location.',
21: 'Looks like trouble is a natural inference from the commotion and leads into the intervention.',
25: 'The brief invitation naturally motivates going to investigate; the destination is already understood.',
31: 'The protest clearly recalls the earlier higher-price promise in natural spoken English.',
39: 'These are our very best naturally conveys her defense of the village goods without unnecessary expansion.',
55: 'The pain cry and angry question fit the abusive sailor and the immediate physical confrontation.',
58: 'The short cry accurately preserves her frightened reaction without inventing an action.',
62: 'The command and objection to a man striking a woman naturally preserve Rafael expressed moral stance.',
67: 'The short challenge sounds natural in Claudio rough protective voice.',
71: 'The annoyed tongue click is the correct terse reaction before the sailor leaves.',
75: 'The scornful observation accurately notes the retreat in Claudio voice.',
84: 'The silent ellipsis is the intended pause; no invented reply or ASCII-letter substitution is needed.',
98: 'Rich boy and Keep your pity naturally convey her offended assessment and refusal of condescension.',
102: 'The angry complaint preserves Claudio belief that their rescue deserved gratitude.',
106: 'The tentative question naturally begins Rafael self-examination of their attitude.',
111: 'The blunt protest fits Claudio indignation and correctly appeals to their having helped her.',
119: 'The slightly formal response fits Janus considering the account just told.',
123: 'The angry exclamations preserve Claudio outrage without needing a synonym-only rewrite.',
134: 'The gentle inclusive reassurance and name substitution already work in Arcadius voice.',
141: 'The supportive reference to helping people in need naturally praises Rafael habitual kindness.',
152: 'The interruption accurately protests that Rafael is not to blame and remains unfinished; retain wording and correct its one full-width I.',
155: 'The resigned dismissal and hopelessly softhearted crew preserve Claudio affectionate exasperation.',
166: 'The short puzzled response naturally answers the unexpected approach.',
171: 'The startled recognition and rude woman accusation preserve Claudio lingering anger.',
181: 'There is no pressure is an idiomatic hesitant assurance that they are free to refuse.',
184: 'The brusque agreement and question naturally defer the decision to Rafael with the correct substitution.',
202: 'The hesitant Um and well already communicate her difficulty getting the apology out.',
206: 'The direct apology naturally delivers the words she struggled to say; no added explanation is needed.',
210: 'The short surprised response accurately precedes her hasty farewell.',
215: 'The casual farewell sounds natural and preserves her intention to meet them later.',
219: 'The slightly formal conclusion suits Janus recognizing her underlying kindness.',
222: 'The rebuke correctly criticizes Clau for calling her rude and continues the companions gentle correction.',
225: 'The defensive echo of cruel and the rescue/parting insult complaint preserve Claudio argument.',
229: 'The paired refusal of pity and request to buy remain clear, with a natural blunt accusation in Claudio voice.',
232: 'The concise contrast correctly recasts her return as courage and sets up Janus explanation.',
239: 'The short observation naturally affirms her good character after hearing why she returned.',
244: 'The quiet realization appropriately marks Claudio change of mind.',
252: 'The natural warning correctly points out that Claudio is acting before any negotiation.',
260: 'The stammered familiar name preserves Rafael surprise at Claudio sudden enthusiasm.',
265: 'Janus balanced observation already conveys forcefulness tempered by admiration for Clau directness.',
269: 'The short affirmative naturally agrees with Janus assessment.',
274: 'The straightforward confirmation naturally concludes the transaction.',
283: 'The introduction and reciprocal name question are accurate and natural; retain wording and correct its two full-width I letters.',
290: 'The direct question naturally asks why the village occupies poor land and invites her account.',
301: 'The narrative transition accurately introduces an offer to settle in the New World without inventing its recruiter.',
305: 'They said clearly attributes the gold and fertile-land promises to others rather than endorsing them as facts.',
309: 'Pooling their scarce money and deciding to cross the sea remain clear and natural; no new amount is invented.',
313: 'Her parents, the wider group, initial hope and ownership of land/village are all preserved naturally.',
316: 'The short transition accurately turns hope into despair and leads into its explanation.',
326: 'The account preserves despair, mutual encouragement and the decision realized in building the village.',
343: 'The natural statement preserves widespread European prejudice as her experience of others looking at them.',
347: 'The silence preserves Rafael reaction to the account without inventing dialogue.',
363: 'The hesitant admission of genuine happiness at his help already works; retain wording and correct its one full-width I.',
370: 'The direct admission correctly links his first words to her hurt without inventing an additional incident.',
375: 'The natural acknowledgment of his good intentions and deserved thanks preserves her reciprocal apology.',
379: 'Here unambiguously means the village and the return request already sounds natural.',
383: 'The warm affirmative answers the return request naturally.',
388: 'The brief confirmation question preserves her hopeful surprise.',
401: 'The natural casual farewell answers her wish to see him again.',
406: 'The calling reminder of the promise works as a short farewell and adds no invented relationship.',
410: 'The pause and surprised discovery of Clau presence naturally lead into the eavesdroppers exchange.',
418: 'The sympathetic observation accurately links her hardships in Europe and the New World.',
451: 'The urgent appeal to Rafael preserves Claudio desire to help; retain wording and correct its one full-width I.',
455: 'The formal inclusive suggestion fits Arcadius and preserves helping village growth even if benefits come later.',
458: 'The enthusiastic agreement naturally commits them to thinking of a way to help.',
462: 'The quiet pause preserves the source emotional transition without invented speech.',
467: 'The softly spoken name preserves Rafael lingering reflection without declaring romance.',
472: 'The appreciative observation naturally describes her sincerity and good character.',
476: 'The brief affirmative agrees with the preceding assessment; a synonym change adds no value.',
480: 'The hesitant affirmative matches Rafael quiet reaction at the end of the conversation.',
}
FINDINGS = {
9: 'Replace the clipped Quiet village. No life with a natural observation of the village lack of vitality.',
12: 'Restore the present observation of foreign ships docked here, rather than a general claim that they sometimes stop.',
35: 'Replace the unidiomatic At today quality/not one coin fragment with a complete dismissive bargaining response.',
43: 'Make the sailor mocking repetition of village best sound like actual spoken English.',
47: 'Restore the taunting demonstration while damaging the goods; Beat it incorrectly turns the taunt into an order to leave.',
51: 'Make the threat grammatically natural and connect the villagers hard work to the goods he is breaking.',
79: 'Make Rafael concern after the blow a clear natural question rather than an isolated ambiguous Okay.',
88: 'Restore the question about picking a quarrel or making false complaints; Did he accuse you loses the intended inquiry.',
91: 'Restore Rafael hesitant personal offer and its unintended condescending shade, so Charlotte next offended echo has a real setup.',
95: 'Replace the disconnected Perhaps with an exact echo of the localized help me out offer she has just heard.',
114: 'Use the ordinary Getting angry makes you hungry phrasing while retaining the working familiar address and meal suggestion.',
126: 'Restore Rafael first-person responsibility, tentative self-criticism and the help you out echo connecting all three beats of the misunderstanding.',
130: 'Restore his admission that he did pity her and the personal concern about hurting her, rather than impersonal What can be done.',
138: 'Express the advice as gentle reassurance instead of a clipped maxim/order.',
144: 'Restore a natural supportive sentence recognizing his awkward approach while assuring him his good intentions were understood.',
147: 'Use a natural warm thank-you to the whole group rather than the stiff Thanks, all.',
158: 'Replace the unnatural All full with the ordinary post-meal expression I am stuffed.',
162: 'Use a hesitant attention-getting request rather than hello, matching her difficulty approaching after the quarrel.',
174: 'Restore the reluctant tentative request to buy after all, rather than making it an abrupt command.',
177: 'Replace turned us down so boldly with a natural accusation recalling her forceful earlier refusal.',
187: 'Correct collective We to Rafael personal decision and restore the polite request to bring the goods to the port office.',
191: 'Correct the subject of the promised arrival to Charlotte herself; remove the added demand for fair judgment.',
194: 'Restore Rafael warning that he may disappoint her expectations, rather than asserting that her goods may not meet their needs.',
198: 'Use the natural Nothing to lose by trying meaning of her reply instead of the abrupt No risk.',
235: 'Restore the omitted red face as well as trembling and pride, which explain the courage of her return for her family/village.',
248: 'Correct load her cargo to the source unloading preparation; do not reverse the cargo action or invent her cargo as its object.',
256: 'Restore the shared lack of concern about inspection and make the push to buy the whole lot a natural complete appeal.',
279: 'Restore her personal gratitude and ability to report back happily to the villagers in natural sentences.',
287: 'Replace Mine is Charlotte with the idiomatic I am Charlotte while preserving her thoughtful echo of his name.',
295: 'Preserve Romani cultural identity and former itinerant life without implying that settling ended their ethnicity.',
298: 'Restore her childhood memory of holding her mother hand and trying to keep up, rather than inventing endless walking.',
319: 'Replace compressed report fragments with Charlotte natural explanation that random digging did not reveal gold and only barren land remained.',
322: 'Restore Rafael specific condemnation of luring people with promises to take their money in a natural sentence.',
330: 'Make the connection between never having owned land and continuing difficulty growing crops sound like a personal account.',
333: 'Restore the explicit country question, which motivates Charlotte explanation that they have no country of their own.',
337: 'Keep the country question/answer coherent and frame the Romani lack of a country of their own in Charlotte personal voice.',
340: 'Make the theft/disease accusations explicitly things other people blamed on the Romani, preserving reported prejudice without endorsing it.',
352: 'Correct the unnatural our own village lived and retain both approximate timing and achieved self-sufficiency.',
355: 'Restore about a year rather than an exact date and express the arrival of goods through barter naturally.',
358: 'Correct most traders, which invents a claim about the proportion of people; the source says they are often forced to sell cheaply.',
367: 'Correct the invented never once had anyone helped history to her actual statement that she had never expected anyone to help.',
392: 'Make Rafael promise explicit as I promise, avoiding an ambiguous bare Promise that could sound like a request.',
397: 'Correct collective We to Charlotte own waiting and finish the broken sentence/punctuation.',
414: 'Restore Claudio being moved to tears, rather than only labeling the account heartbreaking.',
422: 'Make the surprised response a natural direct address to Arcadius, paralleling the preceding discovery of Clau.',
427: 'Replace the stilted passive Eavesdropping was not intended with a personal apologetic explanation.',
439: 'Restore Rafael personal feeling of losing his place when annexation threatened Portugal; preserve the threatened rather than completed event.',
444: 'Express the absence of a place to belong, rather than implying they literally never had anywhere to live while traveling.',
485: 'Replace the literal with our own hands question with a natural open-ended thought about how they can help; add no mission or optimistic assertion.',
}
OVERRIDES = {
114: "Easy, Clau. Getting angry makes you hungry. Let's eat and clear our heads.",
147: 'Thank you, everyone...',
295: "We're Romani. We used to travel from place to place all over Europe...",
355: 'About a year ago, a ship stopped here. We started getting new goods through barter.',
397: "You'd better! I'll be waiting!",
}

if __name__ == '__main__':
    output = ROOT/'B64_120_whole_exchange_comparison_v1.json'
    assert not output.exists()
    draft_path = ROOT/'B64_120_logical_English_drafts_v2.json'
    current_path = Path('work/analysis/Rafael_B61_B64_current_20261104/current_effective.json')
    draft, current = map(load, [draft_path, current_path])
    byid = {r['id']: r for g in current['groups'] for r in g['records']}
    indices = {r['source_reference']['record_index'] for r in draft['records']}
    assert not (set(RETAIN) & set(FINDINGS)) and set(RETAIN) | set(FINDINGS) == indices
    records, glyphs = [], []
    for original in draft['records']:
        row = deepcopy(original)
        now = byid[row['id']]
        index = row['source_reference']['record_index']
        keep = index in RETAIN
        english = current_paragraph(now) if keep else OVERRIDES.get(index, row['english'])
        assert all(english.count('{MACRO:'+key+'}') == count for key, count in row['source_macros'].items())
        assert '\n' not in english and not any(x in english for x in ['{LB', '{ALIGN', '{PAD}'])
        assert not any('Ａ' <= ch <= 'Ｚ' or 'ａ' <= ch <= 'ｚ' for ch in english)
        finding = RETAIN[index] if keep else FINDINGS[index]
        for key in ['current_hex', 'current_reference', 'current_record_index', 'current_stored_text',
                    'current_effective_hex', 'current_effective_text', 'current_comparison_paragraph',
                    'current_catalogue_selected', 'selected_native_pointer']:
            row[key] = now[key]
        changes = now['current_comparison_paragraph'].count('Ｉ')
        if changes:
            glyphs.append(dict(id=row['id'], fullwidth_I_replaced=changes, wording_retained=keep))
        row.update(english=english, logical_English=english, decision='retention' if keep else 'revision',
            finding=finding, retention_reason=finding if keep else None, localization_note=finding,
            source_first_draft_English=original['english'],
            source_first_draft_reference=dict(path=str(draft_path), sha256=sha(draft_path.read_bytes()), id=row['id']),
            source_first_draft=False, earlier_English_unconsulted=False,
            current_English_comparison_pending=False, current_ROM=current['current_ROM'],
            current_ROM_sha256=current['current_ROM_sha256'],
            complete_source_current_anddraft_considered_in_whole_exchange=True,
            four_prose_gates_pass_butformatting_pending=True,
            fullwidth_I_corrections=changes, glyph_only_correction_withwording_retention=bool(changes and keep),
            source_first_context_provenance=original['context'],
            context=original['context'].split(' Final proper-name/header/event bindings')[0])
        assert row['review'] == dict(source=True, context=True, localization=True, naturalness=True, formatting=False)
        if keep:
            assert english == current_paragraph(now)
        else:
            assert english != current_paragraph(now), row['id']
        records.append(row)
    revised = sum(r['decision'] == 'revision' for r in records)
    retained = len(records)-revised
    assert len(records) == 120 and sum(g['fullwidth_I_replaced'] for g in glyphs) == 5
    save(output, dict(format='dk4-whole-exchange-editorial-comparison-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', records=records, proposed_revisions=revised, justified_retentions=retained,
        fullwidth_I_corrections=glyphs, source_first_drafts=str(draft_path),
        source_first_drafts_sha256=sha(draft_path.read_bytes()), current_binding=str(current_path),
        current_binding_sha256=sha(current_path.read_bytes()),
        whole120_source_Japanese_current_andsealed_draft_exchange_read=True,
        charity_offer_offended_echo_andself_reflection_localized_together=True,
        Romani_identity_reported_prejudice_andapproximate_dates_preserved=True,
        Portugal_threatened_annexation_notlater_completed_event=True,
        all_first_four_individual_gates_pass=True, all_individual_fifth_gates_still_false=True,
        remaining342_older_English_not_selected_orconsulted=True,
        fresh_formatting_native_visual_stored_actual_andregistered_integration_pending=True,
        new_credit=0, guide_photos=False, producer_sha256=sha(Path(__file__).read_bytes())))
    print(f'Village120 comparisons: {revised} proposed revisions/{retained} justified retentions; five full-width I corrections. Formatting/credit pending.', flush=True)
