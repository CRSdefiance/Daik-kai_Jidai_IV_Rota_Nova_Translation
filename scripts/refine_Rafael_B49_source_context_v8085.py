"""Bind all clean exchange variants and27-speech event41 context before prior English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_branch_gloss_v8085')
GLOSS=Path('work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json')
CONTEXT=Path('work/analysis/Rafael_B49_event41_context_v8083/complete_clean_SC0_B41_EV0_andcoverage_before_current_English.json')
PATHS=Path('work/analysis/Rafael_B49_source_paths_v8082/156250_compositions_distinct_complete_text_paths_and61_source_memberships.json')
NAMES=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
MENTIONED=Path('work/analysis/Rafael_B49_mentioned_names_v8084/three_clean_mentioned_identities_six_native_getters_component_only_review.json')
PREREQUISITE=Path('work/analysis/Rafael_B49_prerequisite_gloss_v8077/complete22_clean_B39_glosses_explicit_B49_prerequisite_context_only.json')
CONTEXT_GLOSSES={
26:'Claudio asks Hans whether it is about time they found a clue to the Proof reportedly in Africa. He is impatient, not asserting a confirmed precise location.',
29:'Hans says there is no use becoming impatient.',
33:'Rafael asks how they should look for that clue.',
37:'Hans first urges them to acquire the strength appropriate to a ruler, personifying the Proof as refusing to look their way without it. Do not invent a literal deity or one specific mandatory stat.',
40:'Claudio asks whether strength means having a large fleet.',
43:'Rafael wonders whether it instead means becoming an accomplished navigator.',
55:'Janus suggests it might refer to financial resources.',
69:'Julio wonders whether it means possessing a large trading sphere.',
75:'Hans notes the different interpretations and says it might mean all of them. This is tentative, not a verified checklist or a declaration that only one interpretation is correct.',
79:'Rafael finds the prospect daunting or overwhelming.',
83:'Hans adds that merely having power is not enough.',
87:'Rafael is surprised that there is more to it.',
92:'Hans explicitly frames what follows as his own theory.',
95:'He thinks the mysteries of the Proofs are likely sealed within ruins around the world. Preserve both probability and theory, not an exact guaranteed location.',
98:'Rafael asks about ruins.',
103:'Hans confirms that this is what he means.',
107:'Rafael asks where the ruins are.',
112:'Hans supposes they lie in or near the major cities representing the different cultural regions. This is an inference, not a complete list of specific towns.',
116:'Claudio says that alone still leaves them no practical way of finding them.',
119:'Hans believes some local residents should know and advises first gaining the townspeople\'s trust. Do not turn this into a guarantee that every resident knows.',
122:'Rafael asks about gaining their trust.',
127:'Hans explains that ruins and old churches symbolize local religion and culture; residents will not readily reveal them to outsiders like Rafael\'s party. Preserve the cultural rationale respectfully.',
131:'He gives examples: listen to requests, help people in difficulty, and punish corrupt merchants or soldiers who are making them suffer. Do not invent an indiscriminate war against merchants or a whole culture.',
134:'Claudio dryly compares this to charity work.',
137:'Hans says a worthy ruler in any case needs the character or capacity to earn many people\'s trust.',
141:'Rafael sighs that becoming a ruler is difficult.',
146:'Hans laughs and says of course it is, because no one has achieved it before. Preserve his claim within the fictional conversation without extending it into real-world history.',
}
REFINEMENTS={
142:'Lil casually and imperfectly remembers Hodram\'s name as Hodram Ber... something and calls him a navy man; the current source-compatible surname is Bergstrom but the source deliberately does not finish it here. She qualifies his northern presence with for now. Do not supply the full surname or invent an uncle relationship or rank.',
158:'Lil describes Admiral Clifford as managing the area around イギリス. The source names the surname only; current James Clifford is identity context, not permission to add James to this line. Resolve the local geographical term in context without globally changing the wider recorded イギリス lead.',
175:'Lil casually describes Martin Speyer of the Hanseatic League as somehow keeping things running around Germany. Native current spelling matches the clean マルティン・シュパイヤー identity; do not add a personal rank or biography.',
238:'If original event41 completion query returns0, Lil suggests Africa or the western New World. This belongs to the version before the specific Hans-advice event41 is completed, not proof that Africa is unvisited or unconquered.',
244:'If original event41 completion query returns1, Lil suggests the western New World or mysteries of the far East. Event41 is Hans\'s theoretical advice about power, ruins and local trust; it does not certify that Africa has been cleared or that a Proof is already obtained.',
266:'Rafael gently identifies Lil\'s intent as seeking an agreement. Preserve 協定 without inventing a signed formal alliance or treating the blunt request as a guaranteed gameplay treaty. The full source exchange is required to choose natural pact/terms wording.',
336:'Lil invokes their common Spanish enemy to justify avoiding a fight here. This is her argument and does not itself establish a signed alliance.',
405:'Arcadius calls postponing this sea region wise if it is not the only region left. Preserve the spoken qualification independently of the unchanged native actor and raw-expression branch conditions.',
}
if __name__=='__main__':
    assert not ROOT.exists();old,context,paths,names,mentioned,prerequisite=map(read,[GLOSS,CONTEXT,PATHS,NAMES,MENTIONED,PREREQUISITE])
    assert len(context['groups'][0]['records'])==len(CONTEXT_GLOSSES)==27
    assert paths['structural_compositions_evaluated']==156250 and paths['distinct_text_path_count']==256
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes()) and names['current_English_B49_bodies_still_unread']
    ROOT.mkdir(parents=True);context_out=ROOT/'27_complete_clean_event41_context_glosses_no_new_credit.json'
    save(context_out,dict(source_packet=str(CONTEXT),source_packet_sha256=sha(CONTEXT.read_bytes()),records=[dict(**r,context_source_gloss=CONTEXT_GLOSSES[r['source_record_index']]) for r in context['groups'][0]['records']],
        event41_is_qualified_Hans_advice_not_Africa_clear_visited_orProof_obtained_flag=True,context_only_no_new_source_prose_orcompletion_credit=True,
        clean_context_not_current_English_comparison=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    doc=deepcopy(old)
    for r in doc['records']:
        r['refined_source_gloss']=REFINEMENTS.get(r['source_record_index'],r['first_clean_source_gloss'])
        r['source_path_membership']=next(m for m in paths['source_speech_memberships'] if m['id']==r['id'])
        r['current_English_body_andname_fields_still_unread']=False
        r['current_English_dialogue_body_still_unread']=True
        r['current_native_name_getters_now_verified_after_first_clean_gloss']=True
    doc.pop('current_English_never_exposed_for_this_batch')
    doc.update(source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_paths=str(PATHS),source_paths_sha256=sha(PATHS.read_bytes()),source_names=str(NAMES),source_names_sha256=sha(NAMES.read_bytes()),
        mentioned_name_components=str(MENTIONED),mentioned_name_components_sha256=sha(MENTIONED.read_bytes()),
        source_event39_context=str(PREREQUISITE),source_event39_context_sha256=sha(PREREQUISITE.read_bytes()),
        source_event41_context=str(context_out),source_event41_context_sha256=sha(context_out.read_bytes()),
        all61_source_glosses_complete_exchange_seven_identities_and256_paths_bound_before_current_English=True,
        original_event41_query_not_Africa_completion_orproof_ofnatural_B49_activation=True,
        original_raw_A0_operand_mechanic_meanings_not_invented_orconverted_to_character_IDs=True,
        current_B49_English_dialogue_bodies_still_unread=True,
        complete_scope_42_common19_conditional_source_objects_no_credit=True,
        source_control_C281_two_byte_structural_boundary_only_actual_transition_andopaque_effect_body_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CONTEXT,PATHS,NAMES,MENTIONED,PREREQUISITE,context_out,Path(__file__)]})
    save(ROOT/'61_refined_glosses256_paths_B39_B41_context_before_current_English.json',doc)
    print('61source glosses/256paths/seven speakers/three mentioned identities bound. B39all22 andB41all27 context read. Event41 doesnot mean Africa cleared. CurrentB49English dialogue unread;no credit.')
