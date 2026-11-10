"""Localize the first two complete exchanges in the still-open224-record batch."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B62_prose_v8886')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_partial_v1.json')
CURRENT=Path('work/analysis/Hodram_B61_B70_current_v8885/current_effective.json')
GLOSS=Path('work/analysis/Hodram_B61_B70_clean_gloss_v8877/224_complete_clean_first_meanings_all_ten_exchanges_before_current_English.json')
VIEW=Path('work/analysis/Hodram_B61_B70_source_review_v8884/source_context_names_display_review_before_current_English.json')
PATHS=Path('work/analysis/Hodram_B61_B70_source_paths_v8883/all224_source_memberships_original_branch_cases.json')
NAMES=Path('translations/hodram_B61_B70_speaker_name_review_v1.json')

# One logical paragraph per utterance. No fit-driven omissions or manual breaks.
LINES={
61:{
9:('This place...', 'Here loses her hesitant recognition of this place.', 'Let her first attempt to name the place remain unfinished. The next question invites the recognition she expresses in her following turn; do not anticipate her full explanation.'),
13:("What's wrong?", 'Bare What? is more abrupt than the source inquiry.', 'The captain notices her hesitation and asks what is the matter. Ordinary direct English preserves his attention without adding alarm or a pet name.'),
17:('I know this place.', 'Known place is a compressed label rather than respectful learner dialogue.', 'Use a simple complete sentence for her recognition. Her limited vocabulary does not require removing every pronoun or verb, and this turn does not say her homeland is nearby.'),
21:('What?! Then your homeland is nearby?', 'The surprised question about proximity already works.', 'Keep the captain\'s mistaken inference as a question. Her immediate No rejects it; neither this line nor her recognition establishes where her country lies.'),
24:('...No.', 'The hesitant correction already works.', 'Preserve her quiet refusal of his assumption. The pause belongs to her delivery and does not require a manual line break.'),
28:('I see... Did you pass through here when they brought you?', 'Away leaves the destination unclear and the acknowledgment was lost.', 'The captain accepts her correction and asks about the route by which others brought her. Here binds the present place; no captor, port, direction or completed escape is invented in his question.'),
32:('When I escaped... from the Ottomans.', 'The predecessor loses when and compresses the answer into a report label.', 'Her short answer identifies the occasion on which she passed through. Preserve the escape and the Ottomans, with a natural hesitation; do not claim that recognition itself proves any country was destroyed.'),
36:('The Ottoman Turks! Did the Ottoman Empire destroy your country?', 'Restore the recognition linking Ottoman and Turks; do not add army before the simpler follow-up.', 'The captain recognizes the name and asks the more difficult question about the fate of her country. It remains an unanswered question because her next turn shows she has not understood it.'),
40:('？', 'The isolated puzzled reaction already works.', 'Keep her uncomprehending reaction rather than supplying an answer. The original full-width question glyph remains subject to the later native English display checks.'),
44:('Was that hard to follow? I mean, Ottoman soldiers attacked your home, right?', 'Too hard? sounds dismissive; the full rephrasing should distinguish home from country.', 'The captain checks whether the question was difficult and restates it in simpler terms. Home refers to her hometown in this exchange. Her following yes confirms this attack, not the unanswered claim that the empire destroyed her country.'),
48:('...Yes.', 'Restore the pause before her confirmation.', 'This hesitant yes answers the immediately preceding simpler question about soldiers attacking her home. Preserve the scope of that answer and do not merge it with the earlier country-destruction question.'),
52:('I see...', 'So... leaves his acknowledgment incomplete in a different way.', 'The quiet acknowledgment closes the exchange. It registers what she has actually confirmed without adding a verdict on her country or a promise of revenge.'),
},
62:{
5:('…', 'Her opening silence already works.', 'The silence precedes the captain noticing her apart from the bustle. It establishes a reflective pause without an invented thought or a leading layout break.'),
9:('Sera? What brings you here?', 'The familiar name and conversational inquiry already work.', 'The captain notices her in this spot and asks naturally what brings her there. The short name is already source-bound; no new intimacy or relationship is implied.'),
12:('The city... so lively...', 'Busy city is an abrupt label and drops the source hesitation.', 'Use simple learner phrasing for her impression of a lively town. She is observing the activity, not yet saying that she dislikes it or is afraid of crowds.'),
16:("Yes. It's a hub for trade on the Indian Ocean. Is all the bustle too much for you?", 'The predecessor omits the Indian Ocean and removes the difficult vocabulary that prompts her question.', 'Restore the explicit regional trading-center fact. Bustle gives her a plausible unfamiliar word to ask about before he rephrases it as crowds; keep his question tentative rather than deciding her reaction for her.'),
20:('Bustle?', 'Crowds? wrongly anticipates the simpler word supplied in the next turn.', 'She repeats the unfamiliar word from the previous line. Preserve that teaching-and-rephrasing sequence, not just two isolated semantically similar questions.'),
24:('Do you dislike crowds?', 'Hate crowds? is unnecessarily blunt and telegraphic.', 'The captain now uses the more concrete word crowds. A short complete question preserves his simplification without talking to her as though she were a child.'),
28:("No. I don't mind. Just... surprised.", 'Not dislike is stiff; the response should remain simple without a caricatured accent.', 'She denies disliking the bustle and says it surprised her. Simple familiar words and the pause preserve effort and meaning without turning the surprise into fear or claiming she positively loves the crowds.'),
31:("I see. You're not used to it. ...It's quiet here.", 'The compressed predecessor loses his acknowledgment and sounds like a note.', 'The captain understands her lack of familiarity, then notices the quiet of their present spot. Keep the change of attention and natural contractions; do not identify an unproven building, district or sanctuary.'),
35:('…', 'Her pause before the homeland question already works.', 'Retain the quiet reaction as its own turn. Do not invent a reply or an internal monologue to fill the silence.'),
39:('Tell me... what is your homeland like?', 'The predecessor is understandable, but a gentle lead-in better carries his hesitant invitation.', 'He changes the subject to her homeland and asks what kind of place it is. Keep homeland as the word she has trouble with next; do not replace it with hometown before the source clarifies it.'),
42:('Homeland?', 'The vocabulary question already works.', 'The short echo asks about the word itself. It does not question that she has a home country or contradict her earlier account.'),
46:('The country where you were born.', 'Where you were born omits the explicit country in his explanation.', 'He defines homeland with simpler words. Preserve country without adding a nationality, political boundary or place name.'),
50:('…', 'The pause while she recalls home already works.', 'Give her the source\'s quiet turn before the landscape description. An invented spoken response would change the pace of the memory.'),
54:('Wide, wide grasslands... In spring... so many flowers.', 'Restore the repeated breadth and the abundance of flowers.', 'Simple phrases preserve her expanding recollection: broad grasslands, spring and many flowers. The repetition conveys her voice and the feeling of the landscape without inventing a poetic image or a specific flower.'),
57:('Rivers... springs... birds, goats, sheep... And...', 'The predecessor omits springs and compresses the hesitant enumeration.', 'Retain every natural feature and animal in the source, including springs. The final And carries her search for the next image; no new species, ownership or pastoral way of life is asserted.'),
61:('You can see... the sea, far away.', 'The predecessor loses the explicit act of seeing the distant sea.', 'A simple sentence and pause preserve the visible distant sea. You is generic English for the source description, not a promise that the captain is already visiting or can travel there.'),
65:('Ah... the sea.', 'The predecessor loses his interested acknowledgment and makes it a bare question.', 'The captain responds with quiet interest to the sea in her description. He does not doubt her, name the sea or interrupt with a new fact.'),
69:('Yes. A blue, blue sea.', 'Restore her assent and the repeated color as one simple learner response.', 'The repetition is meaningful in her memory and should not be polished away. The small complete phrase remains respectful and adds no claim about where that sea is.'),
73:("It sounds beautiful. I'd like to see it.", 'Someday, perhaps omits his actual wish and leaves an awkward fragment.', 'He finds the place beautiful and expresses a wish to see it. It is a wish, not a travel plan, promise to take her home or future guarantee.'),
76:('But... everything burned...', 'The recollection of destruction already works.', 'The context supplies what everything refers to: the remembered place. Do not expand the destruction into a claim that every resident died or that all people from her country are gone.'),
79:('！', 'His wordless startled reaction already works.', 'Keep the isolated reaction between her painful reminder and his apology. Do not add a new question, revelation or emotional speech.'),
83:("Oh... yes. I'm sorry.", 'Yes. Sorry is clipped and can sound like an agreement rather than rueful recollection.', 'He recalls the painful fact and apologizes. The soft acknowledgment and complete apology preserve his awkward remorse without explicitly inventing that he forgot or knew more than the source states.'),
86:("No. {MACRO:FI}, don't worry.", 'Her reassurance and given-name address already work.', 'The simple learner reply reassures the captain after his apology. Preserve the exact given-name substitution, without turning the reassurance into forgiveness of an unstated offense or a romantic declaration.'),
89:('...Our town... It must...', 'Surely sounds translated, but the unfinished thought must remain unfinished.', 'Keep her uncertain attempt to say something about their town and the sense of conviction in きっと. Do not supply a surviving town, rebuilt home, dead population, return plan or any other missing predicate.'),
92:('Hm? What about your town?', 'What about it? is understandable, but the explicit echo makes the exchange clearer.', 'He asks her to continue the unfinished thought about the town. This does not interpret it or introduce a new subject.'),
96:("I can't... say it right...", "Can't explain loses the difficulty expressing herself and can sound like refusal.", 'Her struggle is finding the words, in the ongoing learner-language context. Simple language conveys that frustration without treating the thought as secret, unintelligible nonsense or lack of intelligence.'),
100:('…', 'The captain\'s pause after her difficulty already works.', 'Keep his silence before the offer to stay. A new consoling statement would fill in emotional content absent from this turn.'),
104:("If you have nowhere to go back to, you're welcome to stay aboard.", 'No home? Stay aboard loses the condition and sounds like an abrupt command.', 'He makes an open-ended offer if she has nowhere to return to. Welcome conveys permission and reserved warmth; it is not an order, adoption, employment appointment or promise that she will never choose to leave.'),
107:("You said... women can't be on warships... I'd be in the way...", 'Restore the nuisance concern and frame the restriction as her callback to his earlier objection.', 'B142 supplies his previous objection to a civilian woman aboard a warship. She remembers that objection and worries about causing trouble. Explicit You said makes the contextual callback clear without inventing a universal historical naval rule. Preserve simple learner phrasing, not a comic accent.'),
110:('You remember what I said before you learned the language...', 'The predecessor omits the timing relative to her learning the language.', 'He realizes she remembers the earlier remark made before she learned these words. Preserve his unfinished reflection without naming the in-world language English or claiming that she previously had no language of her own.'),
114:("Don't worry about that. Your cooking's well liked. No one will object.", 'The predecessor drops the explicit assurance that no one will oppose her staying.', 'He dismisses her concern, praises the reputation of her cooking and assures her that no one will object. Keep all three parts without inventing a formal cook post, romantic motive, family bond or new naval policy.'),
118:('{MACRO:FI}…', 'The quiet name call already works.', 'Her closing given-name call leaves the emotion understated. Preserve the macro and the pause rather than adding gratitude, romance or an explicit decision absent from the source.'),
}}

CONTEXTS={
61:'Sera recognizes a place from her escape. The captain first asks about the fate of her country, which she does not understand, then simplifies the question to soldiers attacking her home. Only the simpler question receives her yes. Review all twelve turns together without converting that answer into confirmation of national destruction.',
62:'Away from the busy city, the captain simplifies unfamiliar vocabulary as Sera describes her homeland. Her landscape recollection gives way to the memory of destruction and an unfinished thought about the town. He offers her a place aboard; she recalls his earlier civilian-woman objection, and he reassures her. Preserve respectful learner speech, his reserved warmth, all concrete landscape details and the unfinished emotional progression without inventing romance or completing her thought.'
}

def normalize_old(text):
    return re.sub(r'\b(FI|FA|FO)\b',lambda m:'{MACRO:'+m[1]+'}',text)

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists()
    current,gloss,view,paths,names=map(read,[CURRENT,GLOSS,VIEW,PATHS,NAMES])
    ledger_path=Path('translations/editorial_review_current_v1.json');before=ledger_path.read_bytes();ledger=read(ledger_path)
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'] and ledger['records_editorially_completed']==7319
    assert current['all224_source_units_uncredited_in_current_ledger'] and current['source_first_glosses_andcomplete_native_page_view_precede_current_English']
    assert view['all23_source_sheets224_complete_native_pages_directly_viewed_before_current_English'] and len(names['records'])==16
    all_keys={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not all_keys&{historical_key(r) for r in current['records']}
    path_groups={g['block']:g for g in paths['groups']};rows=[];pending=[];macro_counts=dict(FI=0,FA=0,FO=0)
    for original in current['records']:
        if original['block'] not in LINES:
            pending.append({k:deepcopy(original[k]) for k in ['id','file_path','block','source_record_index','source_reference','source_hex','current_reference','current_hex']})
            continue
        row=deepcopy(original);text,finding,note=LINES[row['block']][row['source_record_index']]
        assert text==text.strip() and not any(v in text for v in ['\n','\r','{LB','{ALIGN','{PAD','  ','%'])
        text.encode('cp932');old=normalize_old(row['effective_predecessor_paragraph']);decision='retention' if text==old else 'revision'
        for macro in macro_counts:
            n=bytes.fromhex(row['source_hex'])[1:].count(macro.encode())
            assert text.count('{MACRO:'+macro+'}')==n;macro_counts[macro]+=n
        group=path_groups[row['block']];membership=next(r for r in group['utterance_membership'] if r['id']==row['id']);neighbors=[]
        for model in group['binary_models']:
            ids=model['source_speech_IDs']
            if row['id'] not in ids:continue
            at=ids.index(row['id']);pair=dict(previous=ids[at-1] if at else None,following=ids[at+1] if at+1<len(ids) else None)
            found=next((p for p in neighbors if all(p[k]==v for k,v in pair.items())),None)
            if found:found['structural_models'].append(model['model'])
            else:neighbors.append(dict(**pair,structural_models=[model['model']]))
        assert neighbors and row['source_meaning_gloss'] and row['whole_exchange_fidelity_note']
        row.update(english=text,logical_English=text,speaker={1:'Hodram',24:'Sera'}[row['source_selector']],
            source_meaning=row['source_meaning_gloss'],context=CONTEXTS[row['block']],
            localization_note=note,finding=finding,decision=decision,retention_reason=note if decision=='retention' else None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            exact_structural_neighbor_pairs=neighbors,structural_membership=membership,
            whole_clean_exchange_andcadence_emotional_progression_reviewed=True,
            structural_neighbors_not_actual_eligibility_orcontinuous_chronology=True,
            prior_raw_storage_preserved=row['current_raw_storage_English'],prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],
            prior_macro_normalized_comparison=old,planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+text,
            source_only_not_localized_dialogue_orreview_credit=False,
            no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
            formatting_native_stored_actual_policy_atomic_registered_integration_andcompletion_credit_pending=True,
            no_source_prose_counter_orcompletion_credit=True)
        rows.append(row)
    assert len(rows)==sum(map(len,LINES.values()))==44 and len(pending)==180 and macro_counts==dict(FI=2,FA=0,FO=0)
    revisions=sum(r['decision']=='revision' for r in rows);retentions=len(rows)-revisions
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,GLOSS,VIEW,PATHS,NAMES,Path(__file__)]}
    save(DOC,dict(format='dk4-whole-exchange-editorial-manuscript-partial-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],
        current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],file_path='/data/SC1.DK4',
        full_batch_blocks=list(range(61,71)),full_batch_physical_speeches=224,blocks=[61,62],records=rows,
        total_editorial_objects=44,physical_speech_objects=44,typed_choice_objects=0,typed_choice_records=[],
        revised=revisions,retained=retentions,source_macro_counts=macro_counts,source_FE_panels=0,
        remaining180_records_pending_individual_prose_decisions=pending,
        current_comparison_complete224_not_all224_individually_editorially_approved=True,
        all44_individual_source_context_localization_naturalness_gates_true_formatting_false=True,
        no_native_English_wrapping_stored_actual_orrelease_approval=True,
        all224_clean_first_meanings_names_native_source_andlinked_context_precede_English_comparison=True,
        names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),
        source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),
        source_native_view=str(VIEW),source_native_view_sha256=sha(VIEW.read_bytes()),
        ordinary_wrapping_owned_by_formatter=True,all_prior_full_scope_leads_names_graphics_andlater_technical_reaudit_preserved=True,
        no_new_ROM_registered_integration_orcompletion_credit=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    ROOT.mkdir(parents=True)
    save(ROOT/'44_contextual_decisions_180_still_pending.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=[{k:r[k] for k in ['id','source_reference','source_hex','source_Japanese','current_reference','current_hex','prior_effective_paragraph_preserved','english','decision','finding','localization_note','retention_reason','exact_structural_neighbor_pairs','review']} for r in rows],
        revised=revisions,retained=retentions,remaining_individual_prose_decisions=180,
        new_credit=0,new_emulator_runs=0,no_ROM_registry_orledger_change=True,full_goal_complete=False,evidence=evidence))
    assert ledger_path.read_bytes()==before
    print(f'44 individual contextual decisions: {revisions} revisions/{retentions} justified retentions. Other180 individual decisions andall English formatting/storage/actual/release gates pending; zero credit.')
