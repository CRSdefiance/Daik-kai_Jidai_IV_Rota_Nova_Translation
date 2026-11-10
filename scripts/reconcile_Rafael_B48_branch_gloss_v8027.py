"""Bind91 source glosses to32 paths and optional Athens/Hayreddin callbacks before current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_branch_gloss_v8027')
GLOSS=Path('work/analysis/Rafael_B48_clean_gloss_v8022/91_fresh_clean_glosses_nine_source_identities_before_current_English.json')
PATHS=Path('work/analysis/Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json')
CONTEXT=Path('work/analysis/Rafael_B48_clean_context_v8026/complete_clean_SC0_B128_EV0_andcoverage_before_current_English.json')
B37=Path('work/analysis/Rafael_B47_clean_context_v7972/complete_clean_SC0_B37_EV0_andcoverage_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B48_names_v8023/nine_static_speakers18_getters_clean_fields36_synthetic_macro_alignments.json')
REFINEMENTS={
71:"When original event128 is not completed, Julio introduces the research as a good opportunity during the Athens visit. This is the first introduction of his errand on this path.",
75:"Only the event128-incomplete introduction contains Claudio sounding out the unfamiliar term. Preserve a puzzled response rather than knowledge.",
81:"Only if original event128 is complete does Rafael recall Julio's earlier errand and ask what it was. Clean B128R128-168 supplied the request to visit Athens without naming the object, so this is a callback, not a repeated question within B48.",
86:"Answer to the event128-complete callback: Julio finally names the object he wants to investigate. It is exclusive with R71's spontaneous introduction.",
92:"Common to both introductions: Rafael asks what the newly named object means. Do not duplicate both introductions before this question.",
97:"Julio gives the same mildly evasive joke after either introduction: finding that out is what he is going to research. Preserve the friendly comic timing without inventing ignorance of his acquaintance Hans.",
232:"Optional Janus aside. The same exact04FE0030 raw-result1 condition also enables Claudio's R236 andRafael's R239 responses, so read all three as one beat.",
236:"Optional response to Janus, under the same source predicate asR232. Claudio's 'you're one to talk' is directed to Janus;do not assign it to the assistant or invent a diagnosis.",
239:"Rafael's throat clearing completes the optional Janus/Claudio aside. With that predicate absent, do not imply that an unseen insulting exchange has occurred.",
324:"Julio identifies Hans only as an acquaintance and a long-standing researcher. Shared surname fields elsewhere do not establish family ties, and this sentence does not establish an additional rank or mentor relationship.",
379:"Only if original event37 is incomplete: Rafael resolves to find the treasures;he does not mention Hayreddin on this path.",
385:"Only if original event37 is complete: Rafael adds that someday he will also challenge Hayreddin. Previously read complete B37 supplies the daring bargain andpassage context;this is prospective ambition,not guaranteed victory.",
389:"Only the event37-complete path: the assistant reacts to Rafael naming Hayreddin,not to the general existence of the treasures.",
393:"Only the event37-complete path: Hans's comic astonishment answers the Hayreddin ambition. Do not attach this surprise to the simple R379 promise.",
396:"Only the event37-complete path: Julio chuckles about the fearless admiral/captain. Preserve source address/affection without claiming invulnerability or inventing kinship.",
427:"System announcement: the natural-history scholar/doctor ハンス・レッツェル has joined. Earlier English 'Retzel' in the intent gloss was a provisional rendering,not a settled spelling. Current original getters use Hans Letzel;the discrepancy with historical documentation remains to be resolved in the explicit name review.",
}
if __name__=='__main__':
    assert not ROOT.exists()
    gloss,paths,context,b37,names=map(read,[GLOSS,PATHS,CONTEXT,B37,NAMES])
    assert paths['source_gloss_sha256']==names['source_gloss_sha256']==sha(GLOSS.read_bytes())
    assert names['current_English_B48_bodies_still_unread'] and all(r['current_English_body_unread'] for r in gloss['records'])
    assert len(paths['representative_text_paths'])==32 and len(paths['source_result_compositions'])==500
    assert context['source_only_no_current_English_exposed_orused'] and not context['inventory_failures']
    c=context['groups'][0];assert c['block']==128 and len(c['records'])==45 and len(c['commands'])==68
    assert b37['source_ROM_sha256']==context['source_ROM_sha256'] and b37['clean_archive_sha256']==context['clean_archive_sha256']
    assert len(b37['groups'][0]['records'])==72
    event=c['source_event_records'][0];assert event['event_ID']==128 and event['must_be_completed']==[139] and event['must_not_be_completed']==[48]
    rows=[]
    for original in gloss['records']:
        row=deepcopy(original);i=row['source_record_index']
        membership=[n for n,p in enumerate(paths['representative_text_paths']) if row['id'] in p['source_speech_IDs']]
        assert membership
        row.update(source_composed_text_paths=membership,source_branch_context_proof=str(PATHS),source_branch_context_proof_sha256=sha(PATHS.read_bytes()),
            source_name_proof=str(NAMES),source_name_proof_sha256=sha(NAMES.read_bytes()),
            original_source_intent_gloss_before_branch_refinement=row['source_gloss'],
            source_branch_refined_gloss=REFINEMENTS.get(i,row['source_gloss']),
            all_original_control_paths_andoptional_callbacks_considered=True,
            source_gloss_not_current_English_derived=True)
        rows.append(row)
    ROOT.mkdir(parents=True)
    save(ROOT/'91_fresh_glosses32_paths_B128_B37_context_before_current_English.json',dict(
        records=rows,source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_paths=str(PATHS),source_paths_sha256=sha(PATHS.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        complete_B128_clean_context=str(CONTEXT),complete_B128_clean_context_sha256=sha(CONTEXT.read_bytes()),
        complete_B128_context_speeches45_read_without_new_credit=True,
        prior_complete_B37_clean_context=str(B37),prior_complete_B37_clean_context_sha256=sha(B37.read_bytes()),
        B37_reused_by_exact_clean_ROM_archive_EV_identity_not_repeated_native_oractual_tests=True,
        callback_context_summary="Clean B128's sailing lesson optionally ends by Julio asking for Athens,to investigate a future common goal. Event128 requires139/excludes48;B48queries completion128,not a mandatory B48trigger dependency. B37 supplies Hayreddin's bargain/passage context only for source query37's completed variant.",
        all91_source_glosses_complete_exchange_nine_identities_and32_paths_bound_before_current_English=True,
        source_Janus_group_andtwo_exclusive_introductions_andambition_alternatives_not_flattened=True,
        no_hidden_identity_explanation_health_diagnosis_kinship_orunsupported_national_biography_added=True,
        current_names_exposed_only_after_fresh_clean_glosses_body_English_still_unread=True,
        current_name_consistency_followups=dict(
            Hans='Current native Hans Letzel versus historical workflow Hans Retzel;not a settled spelling from either alone.',
            Arcadius='Current progressive Arcadius Eudoxios versus full Arcadius Eirene Eudoxios;source spoken introduction omits middle. Preserve consumer distinction andconcealed-characterization limits.',
            Cristina='Clean/current Cristina Erneco;existing Cristina/Christina counterpart leads remain open. Shared surname withJulio alone proves no kinship.',
            Cesare='Cleanチェザーレ/トーニ versuscurrent Cesare Tony;source-sound/English-readability/cross-consumer naming review remains required.',
            PortWorker='Clean出港所の兄貴 versuscurrent Port Worker;whole exchange supports occupational role,no family/rank from familiar兄貴. Wider seven counterpart consumers remain separate.'),
        all_English_B48_bodies_still_unread=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(Path(p).read_bytes()) for p in [GLOSS,PATHS,CONTEXT,B37,NAMES,Path(__file__)]},full_goal_complete=False))
    print('91 branch-refined glosses/32 source paths pluscomplete45-speech B128 andprior72-speech B37 context bound.Current English bodies unread;zero credit.')
