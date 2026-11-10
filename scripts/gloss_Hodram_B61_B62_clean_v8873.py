"""First meanings for two complete Sera/Hodram exchanges, before consulting current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B61_B62_clean_gloss_v8873')
SOURCE=Path('work/analysis/Hodram_next_clean_v8872/complete_clean_SC1_B61_B70_EV1_andcoverage_before_current_English.json')
CONTEXT=Path('work/analysis/Hodram_B54_B60_clean_context_v8795/complete_clean_linked_15_37_65_128_142_context_before_B54_B60_English.json')
# Meanings, not final localized/compiled lines. Keep each hesitation and question
# in the complete exchange; do not infer an answer to the captain's first theory.
GLOSSES={
61:[
 (9,'Sera hesitantly calls attention to this place.','The unfinished here introduces recognition; do not add a destination name.'),
 (13,'Hodram asks what is wrong or what has caught her attention.','A short response to her hesitation; not an accusation.'),
 (17,'Sera says she knows or recognizes this place.','Recognition alone does not mean it is her hometown.'),
 (21,'Hodram reacts with surprise and asks whether her homeland must therefore be nearby.','This is his hopeful inference framed as a question, not an established geographic fact.'),
 (24,'Sera says no.','She rejects the nearby-homeland inference.'),
 (28,'Hodram acknowledges that and asks whether she passed through while being brought here.','Keep the passive/involuntary context and the question; do not invent a particular ship, owner or route.'),
 (32,'Sera identifies the occasion as fleeing the Ottomans.','Japanese leaves the subject unspoken. Preserve her flight and do not invent companions, a successful homecoming or a specific battle.'),
 (36,'Hodram identifies Ottoman Turkey and asks whether the Ottoman Empire destroyed her country.','This remains his question. Her later yes answers a different, simpler question about soldiers attacking her home.'),
 (40,'Sera does not understand the question.','A puzzled reaction, not a denial and not confirmation of nationwide destruction.'),
 (44,'Hodram realizes his question was difficult and rephrases: Ottoman soldiers attacked her home, did they not?','Preserve the contrast between the difficult country/empire question and this simpler attack question. Do not mock her language learning.'),
 (48,'Sera confirms the attack described in the rephrased question.','Her yes confirms the attack on her home; do not promote the earlier uncomprehended question into fact.'),
 (52,'Hodram quietly acknowledges her answer.','A subdued close after learning about the attack, not a new vow, threat or revenge plan.'),
],
62:[
 (5,'Sera is silent.','Preserve the pause; no invented sigh or distress statement.'),
 (9,'Hodram addresses Sera and asks what she is doing in a place like this.','The question notices her presence; it supplies no new location name or relationship.'),
 (12,'Sera remarks that the town is bustling.','She is observing the liveliness rather than explicitly saying she fears crowds.'),
 (16,'Hodram explains that the town is a relay point for Indian Ocean trade and asks whether city bustle bothers her.','Preserve the Indian Ocean trading context. His question about her preference is not proof she dislikes crowds.'),
 (20,'Sera asks about the unfamiliar word for bustle or hubbub.','Retain the lexical misunderstanding so the following simpler rephrasing has a purpose; do not make her sound unintelligent.'),
 (24,'Hodram rephrases his question as whether she dislikes crowds.','This is a deliberate simpler restatement of his earlier bustle question.'),
 (28,'Sera says no, she does not dislike them, but she was surprised.','Do not reverse her answer into fear, hatred or dislike of crowded places.'),
 (31,'Hodram understands that she is not used to it and observes that it is quiet here.','Do not assign movement or other semantics to opaque scene commands, or invent a spoken instruction to find another place.'),
 (35,'Sera pauses without speaking.','A quiet transition into a more personal conversation.'),
 (39,'After a pause, Hodram asks what her homeland is like.','An open question about her home, not a demand for a national identity or an assertion about the current town.'),
 (42,'Sera asks what the word for homeland means.','Preserve the second vocabulary clarification and its relation to the following answer.'),
 (46,'Hodram explains that he means the country where she was born.','Do not replace the explicit country explanation with an invented village or province.'),
 (50,'Sera pauses before remembering her home.','The pause begins the recollection; no invented trauma diagnosis.'),
 (54,'Sera remembers very wide grasslands and many flowers in spring.','Preserve spring and the expansiveness/repetition as emotional recollection, without adding a named country.'),
 (57,'She recalls rivers, springs, birds, goats and sheep, then trails off before another detail.','Keep the complete concrete list and unfinished progression.'),
 (61,'She recalls being able to see the sea in the distance.','The distant sea belongs to the homeland recollection, not a newly identified current location.'),
 (65,'Hodram responds with interest to the mention of the sea.','A brief invitation to continue; no additional geographic deduction.'),
 (69,'Sera confirms it and describes a very blue sea.','Preserve the repeated blue as affectionate recollection rather than flattening the emotional detail.'),
 (73,'Hodram says it must be beautiful and that he would like to see it.','A wish to see the place, not a promise to take her home or a completed travel plan.'),
 (76,'Sera contrasts the beautiful memory with the loss: it all burned.','Do not turn this into an explicit statement that all her people or relatives died; the source does not say that here.'),
 (79,'Hodram reacts in shock.','Preserve the abrupt reaction without adding a curse or explanation.'),
 (83,'Hodram acknowledges that and apologizes.','He recognizes the painful implication after his question; no invented account of personal responsibility.'),
 (86,'Sera dismisses the need for an apology and tells FI not to worry.','FI is retained as a runtime macro. Its approved default given-name meaning is not a company, rank or surname; do not substitute a fixed name in encoded prose.'),
 (89,'After another pause, Sera starts to say that their town surely or probably is something, but cannot finish.','Preserve the plural our and the unfinished thought. Do not supply survival, rebuilding, destruction, hope or a return as its unstated completion.'),
 (92,'Hodram asks what she means about the town.','He seeks clarification, rather than supplying an answer to the unfinished thought.'),
 (96,'Sera says she cannot express it well.','This concerns her difficulty putting the thought into words. Do not diagnose memory loss or make her speech a joke.'),
 (100,'Hodram pauses.','Allow the silence before the offer, without an invented internal monologue.'),
 (104,'Hodram says that if she has nowhere to return to, she may keep staying aboard this ship.','Retain the conditional and open-ended permission; do not invent adoption, a romance, a military appointment or a lifelong contract.'),
 (107,'Sera recalls that women are not allowed on a warship and worries about being a burden.','Read with clean B142R139: this recalls Hodram\'s earlier objection about taking a civilian woman aboard. It is her recollection, not a narrator\'s claim about universal historical naval law.'),
 (110,'Hodram recognizes the remark he made before she had learned their language.','The trailing object is elliptical. The callback is supported by B142R139; direct address versus an aside still needs final contextual/voice review. Do not name the language English.'),
 (114,'Hodram tells her not to worry, says her cooking is well regarded and that nobody will object.','Preserve reassurance and the specific praise for her cooking; do not invent a chef rank, a family relationship or a formal rule change.'),
 (118,'Sera responds by speaking FI and trailing off.','Preserve the given-name macro and emotional pause. No explicit romantic declaration, promise or additional sentence is supplied.'),
],
}
if __name__=='__main__':
    assert not ROOT.exists();source,context=map(read,[SOURCE,CONTEXT]);groups=[]
    assert source['source_only_no_current_English_exposed_orused'] and not source['inventory_failures']
    prior142=next(g for g in context['groups'] if g['block']==142)
    callback=next(r for r in prior142['records'] if r['source_record_index']==139)
    assert callback['source_Japanese']=='軍艦に民間人の\nしかも女を乗せるわけにはいかん'
    protected=[Path('work/clean.nds'),Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json'),Path('translations/hodram_B54_B60_editorial_release_v1.json')]
    before={str(p):sha(p.read_bytes()) for p in protected}
    for number,meanings in GLOSSES.items():
        original=next(g for g in source['groups'] if g['block']==number)
        assert [r['source_record_index'] for r in original['records']]==[r[0] for r in meanings]
        rows=[]
        for source_row,(index,meaning,note) in zip(original['records'],meanings,strict=True):
            assert source_row['source_selector'] in [1,24] and source_row['current_English_body_unread'] and not source_row['already_contextually_completed']
            rows.append(dict(deepcopy(source_row),source_meaning_gloss=meaning,whole_exchange_fidelity_note=note,speaker_identity_reference='Approved Hodram/clean actor1 or Sera/clean actor24; new current native consumer binding still pending',
                current_English_dialogue_still_unconsulted=True,meaning_read_in_complete_clean_exchange=True,source_only_not_localized_dialogue_orreview_credit=True))
        groups.append(dict(block=number,source_block_sha256=original['clean_block_sha256'],source_event_records=original['source_event_records'],records=rows,
            entire_clean_exchange_andemotional_progression_read_before_English=True,opaque_commands_andnumeric_adjacency_not_plot_orchronology_proof=True))
    assert sum(len(g['records']) for g in groups)==44
    ROOT.mkdir(parents=True);save(ROOT/'44_first_meanings_with_country_question_vocabulary_andnaval_callback_context.json',dict(format='dk4-clean-source-meaning-only-v1',future_translation_policy='natural-dialogue-v2',target_locale='en-US',source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),groups=groups,
        linked_clean_context=str(CONTEXT),linked_clean_context_sha256=sha(CONTEXT.read_bytes()),B142_complete68_source_context_read_for_callback=True,exact_B142_R139_callback=callback,
        all44_meanings_andtwo_complete_clean_exchanges_read_before_current_English=True,
        B61_uncomprehended_country_destruction_question_not_treated_as_answered_fact=True,
        B62_vocabulary_rephrasing_unfinished_town_thought_conditional_permission_andspecific_cooking_praise_preserved=True,
        Sera_learning_respectful_no_mock_accent_universal_naval_rule_English_language_name_orinvented_relationship=True,
        native_preambles_names_macros_branches_glyphs_current_comparison_localization_formatting_actual_andregistered_release_pending=True,
        other180_candidate_speeches_not_glossed_here=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        protected_hashes=before,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,CONTEXT,Path(__file__)]}))
    assert {str(p):sha(p.read_bytes()) for p in protected}==before
    print('44 clean-first meanings/two whole exchanges;68-record clean callback context;country-question andcivilian-woman recollection distinguished.No current English,ROM orcredit.',flush=True)
