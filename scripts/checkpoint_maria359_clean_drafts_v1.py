"""Publish the new359 clean-first drafts without altering credit or the testing candidate."""
from pathlib import Path
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B253_B274_clean_20261110')

def main():
    pp,sp,sealpath=[ROOT/p for p in ['clean_source_packet.json','source_selection_v1.json','clean_draft_seal_v1.json']]
    rp=Path('work/maria363_B216_B252_release_v1/registered_release_verification.json')
    packet,selection,seal,release=map(load,[pp,sp,sealpath,rp]);drafts=load(seal['independent_drafts'])
    assert packet['selected_blocks']==list(range(253,275)) and selection['exact_disjoint_credited_keys']
    assert (seal['source_objects'],seal['complete_exchanges'])==(359,22)
    assert seal['no_current_story_English_read'] and seal['all_five_review_gates_pending']
    assert Counter(r['kind'] for r in drafts['records'])=={'ordinary-speech':218,'physical-style-alternative':131,'typed-menu-caption':10}
    assert all(not any(r['review'].values()) and r['current_English_not_consulted'] for r in drafts['records'])
    for p,h in seal['evidence'].items():assert digest(p)==h
    evidence={**seal['evidence'],**{str(p):digest(p) for p in [pp,sp,sealpath,rp,Path(__file__)]}}
    summary=('The next Maria batch has359 clean meanings and independent American English drafts across22 complete groups B253–B274: '
        '218 ordinary bodies,131 physical style alternatives and10 captions. Every draft issealed before current-English extraction. '
        'Contextual comparison,names/terms andallfive gates remain pending. No new ROM orcredit. Integrated23,070,registered edf002f8, '
        'the GitHub testing candidate andfull scope remain unchanged;no worker islive.')
    document='docs/editorial_Maria359_B253_B274_clean_drafts_20261110.md'
    text=f'''# Maria B253–B274 clean-first drafts — November 10, 2026

{summary}

The previous goal turn was progress: Maria363 was registered and credited once, the cumulative candidate was packaged, and the complete project checkpoint was committed and pushed as `ec6108d4b243f0c8e3d182aefa37054d0d467c3d`. The testing candidate remains `{release['candidate_sha256']}`, with722 entries,114 accepted layers,57 release checks,exact clean-input reconstruction,own startup and24 protected getters. Main remains V4701 pending user acceptance. Preserve all completed checks andearlier artifacts.

This turn reuses the qualified SC3_v14 inventory andselects359 exact,unique source objects disjoint from prior credit. Complete Japanese reading covers London's one-month scurvy-remedy loan andrepayment,Malacca's shark-fin orother-delicacy alternatives,the Istanbul-Ceuta30-day demonstration against a normal40-day trip andcouriers taking overtwo months,armor research,Colosseum/mosque clues,andjungle/forest/desert exploration. Preserve these source-specific numbers,hearsay,Chinese palace cuisine,Islamic boarding tactics andthe game's own carronade description. Do not silently revise source claims tofit real-world history. The armor gift andalternative delicacy remain unnamed where the dialogue doesnot identify them.

Use `work/Maria_B253_B274_clean_20261110/clean_source_packet.json`, `source_selection_v1.json`, `all359_clean_meanings_v1.json`, `all359_independent_drafts_v1.json` and `clean_draft_seal_v1.json`. The two selected part directories `clean_part_B253_B264_v2` and `clean_part_B265_B274_v2` contain162 and197 records. Both original v1 parts remain preserved. Four clean-only refinements remove an isolated leading exclamation,avoid inventing friendship for fellow crew,replace an awkward double contraction andavoid adding profanity toan ordinary rough complaint. Each source meaning precedes its draft,andallparts precede first current-story-English exposure. All359 individual gates remain false;these areindependent drafts,not approved revisions orretentions.

Review the complete alternatives asconditional content. The jungle tiger's defeat isnot an explicit death;the forest snake isexplicitly not killed. The forest bog anddesert quicksand aredistinct hazards. Maria's fatigue andsailor fatigue notices have separate causes. Source B271R223 usesactor18 despite feminine Japanese phrasing;bind its actual native speaker instead of silently relabeling it Maria. Dynamic selectors,131 embedded physical personality variants andfive two-choice menus stillneed current/native bindings;static source actor fields donot grant native dispatch orname-UI approval. Names,role labels,item titles,catalogue components andruntime substitutions remain in scope.

Next bind the sealed drafts toexact current effective ordinary/style/menu text,then compare every complete exchange. Document individual findings andjustified retentions;bind names andterms before sealing the firstfour gates. Keep logical paragraphs anduse validated consumer-specific full-width wrapping,with fresh checks anddirect review ofevery generated page. Reuse compatible proofs andrepresentative gameplay;no guide photos orexhaustive natural playthroughs. Do not repeat completed candidate tests without a changed dependency orconcrete risk.

Integrated23,070 =13,778 revisions+9,292 retentions;historical source/prose/draft23,073. Remaining native story objects2,828 =Maria1,023+Lil1,805 includes this uncredited359. Shared/player-facing inventories remain separate. Keep allstorylines,earlier unfinished contextual passes,town/shop/random prose,speaker names,wrap/glyph consistency andearly Rafael/tutorial priority. Deferred artwork andlater older-record technical re-audit remain separate. No cleanup,new build,promotion,commit orpush occurs inthis turn. The full goal remains active.
'''
    checkpoint(mutation=ROOT/'clean_draft_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria359 B253–B274:clean meanings andindependent drafts sealed;current comparison/names/terms/allgates pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=0,justified_retentions=0,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],
            registered_build_live=False,registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Bind sealed359 drafts tocurrent effective text;compare whole exchanges andbind names/roles/terms before first-four-gate approval.'),
        new_entries={'Maria_SC3_B253_B274_clean_20261110':dict(new_credit=0,source_objects=359,complete_exchanges=22,
            source_speech_objects=218,physical_style_alternatives=131,typed_choice_labels=10,clean_source_selected=True,
            clean_meanings_andindependent_drafts_pending=False,clean_meanings=359,independent_drafts=359,
            clean_meanings_path=seal['source_meanings'],independent_drafts_path=seal['independent_drafts'],clean_source_draft_seal=str(sealpath),
            current_English_not_read=True,contextual_comparison_pending=True,names_terms_consumers_pending=True,
            all_five_review_gates_pending=True,all_fifth_gates_pending=True,registered_integration_pending=True,
            no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=23070,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'clean_draft_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,no_current_story_English_read=True,no_batch_worker_live=True,full_goal_complete=False))
    print('Published359 clean meanings/drafts;allgates pending;23070 integrated andtesting candidate unchanged.')

if __name__=='__main__':main()
