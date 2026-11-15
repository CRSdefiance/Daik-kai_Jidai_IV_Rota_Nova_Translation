"""Publish315 sealed clean-first drafts and current bindings without completion credit."""
from pathlib import Path
from collections import Counter
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT=Path('work/Maria_B286_B302_clean_20261110')

def main():
    releasepath=Path('work/maria349_B275_B285_release_v1/registered_release_verification.json')
    pp,sp,sealpath=[ROOT/p for p in ['clean_source_packet.json','source_selection_v1.json','clean_draft_seal_v1.json']]
    packet,selection,seal,release=map(load,[pp,sp,sealpath,releasepath])
    drafts=load(seal['independent_drafts'])
    assert packet['selected_blocks']==list(range(286,303)) and selection['exact_disjoint_credited_keys']
    assert (seal['source_objects'],seal['complete_exchanges'])==(315,17)
    assert seal['no_current_story_English_read'] and seal['all_five_review_gates_pending']
    assert Counter(r['kind'] for r in drafts['records'])=={'ordinary-speech':196,'physical-style-alternative':113,'typed-menu-caption':6}
    assert all(not any(r['review'].values()) and r['current_English_not_consulted'] for r in drafts['records'])
    for p,h in seal['evidence'].items():assert digest(p)==h
    currentpath=ROOT/'current_v1/current_effective.json';objectpath=ROOT/'current_objects_v1/current_objects.json'
    namepath=ROOT/'scoped_names_macros_reference_v1.json';rolepath=ROOT/'dynamic_roles_current_v1.json'
    current,objects,names,roles=map(load,[currentpath,objectpath,namepath,rolepath])
    assert current['records']==196 and len(objects['style_records'])==113 and len(objects['choice_records'])==6
    assert len(objects['style_objects'])==17 and len(objects['native_style_getter_cases'])==136
    assert len(roles['source_records'])==119 and roles['source_selectors']==[207,208,211,214]
    assert all(d['runtime']==current['runtime'] for d in [objects,names,roles])
    paths=[pp,sp,sealpath,releasepath,currentpath,objectpath,namepath,rolepath,
        ROOT/'all315_clean_meanings_v1.json',ROOT/'all315_independent_drafts_v1.json',Path(__file__)]
    evidence={**seal['evidence'],**{str(p):digest(p) for p in paths}}
    summary=('The final315 unreviewed native Maria story objects are selected across17 complete groups B286–B302: '
        '196 ordinary bodies,113 physical personality alternatives and6 captions. All315 clean meanings and independent English drafts were sealed before current-English extraction. '
        'Current ordinary/style/menu text,13 scoped actors/26 getters,default macros and119 dynamic-role references are bound. '
        'Contextual comparisons,names/terms review andallfive individual gates remain pending. No new ROM orcredit;23,778 integrated,the registered fd825d4d candidate andmain areunchanged. No worker islive.')
    document='docs/editorial_Maria315_B286_B302_clean_bindings_20261110.md'
    text=f'''# Maria B286–B302 clean drafts and current bindings — November 10, 2026

{summary}

The previous goal turn was progress: Maria349 was registered and credited once, its cumulative testing package was prepared, and commit `c3bf64e6e2bb7717f781cef7fb6f8469b1989f32` was pushed to `codex/combined-routes-v89`. The GitHub head and local head matched and the working tree was clean at that handoff. This continuation adds new draft/checkpoint work; it does not change that testing ROM or promote main. The full editorial goal remains active.

This turn reused the exact SC3_v16 source inventory. Its315 remaining objects span17 groups, including B302's28 objects; B286–B301 alone has287 and was correctly rejected by the315-count guard before output. `source_selection_v1.json` proves exact clean positions and disjointness from prior credit. The two authored parts contain191 and124 meanings/drafts. Both complete clean exchanges and necessary source actor fields were read before drafting; the generic part saver wrote meanings before drafts, and `clean_draft_seal_v1.json` predates current-English extraction. All source/current references are preserved. No record receives a prose or formatting gate from an independent draft alone.

Source findings to carry into comparison:

- B286's celadon incense-burner lead is reported divination lore, followed by a pirate warning. Its reply controls use Rafael, actor0, despite SC3. Preserve the controls and the FI substitution independently; the current captain remains Maria.
- B287–B290 requests are five cargo holds of armor, five holds of guns and two holds of cannons, with deferred combined payment,77,000 coins and a slight Sao Jorge share increase. The subsequent Sahara hideout is rumor. Keep Maria's dry frustration at repeated trips.
- B291 distinguishes pushing through fog, searching for a detour and waiting a day. Keep both separate system pauses and the unnamed destination. B292 distinguishes a dangerous giant snake from apparently harmless bats, possible injury from fatigue, uncertain Indian-python identification and uncertain location near ruins. Seventeen whole personality objects contain113 physical variants and136 original getter cases; do not reduce these to one voice.
- B293's guide says the ruins appear to be off the current island, has a small boat, restricts knowledge of their location and continues overland after one day. Do not invent a named island, society, rank or burial site.
- B294/B302's missing monk story turns from hearsay and scientific excitement to grief. Preserve alchemy, mineral poison in drinking water, medicine given entirely to villagers and the monk's death, without inventing a toxin or medical training. B302's two book-recognition controls use Lil, actor2. Charles is actor18; keep the exact controls instead of silently assigning every line to Maria.
- B295 begins with a rumored ghost ship; B296 separately confirms its defeat,65,000 coins,Havana share and a nonrefundable5,000-coin advance toward an uncertain ruins search. The greatest-warrior account includes moral character and wisdom. Keep the permission-to-fail joke, map requirement and gate rendezvous.
- B297 retains the unfamiliar thanks as `Xie xie`, because Maria initially asks what was said. The gift is not named. B298 preserves the guardian's mistrust of Western conquerors, Maria's personal refusal of coercion, Xien's harder warning and the eventual voluntary trust. Do not change Maria's denial into a claim that clears Xien's warning of its coercive implication. Keep Escante's destruction and submission as separate alternatives and the unnamed friend's recommendation.
- B299/B300 preserve the source's sextant barter and unnamed reward. B301's offered object and long wait stay unspecified. Item titles,city spellings and source-number ambiguity remain subject to exact consumer binding.

Current bindings are saved in `current_v1/current_effective.json` and `current_objects_v1/current_objects.json`, after the sealed clean draft. The current13 scoped actors are0,2,3,10,18,22,43,135,147,161,179,204,206. Their26 original name getters and default FI=Maria,FA=Li,FO=Li Clan,FU=Maria Huamei Li are bound, not newly localized or display-approved. Source role metadata for135 does not authorize a biography or nationality;161/179 share Villager across different regional contexts. Spoken Charles/Escante names are bound. Names still need individual localized retentions/revisions; the fallback156 name pair will also need explicit scoped inclusion before final display approval.

`dynamic_roles_current_v1.json` binds119 references:113 physical style variants plus6 ordinary207/208 controls. Selectors207/208/211/214 use the original current dispatch:207 resolves to Maria/voice3, and208/211/214 are unassigned and use fallback156/voice4 in this startup only. No future roster,role or RNG result is assigned. The initial role-binding invocation's incomplete argument scope was rejected before output; the succeeding exact119-reference call preserves all original guards. Native getter/role checks are offline evidence, not new scene gameplay.

Next compare all315 records as complete current/source exchanges, with exact findings and individual justified retentions. Bind item/city terms and14 scoped names including156; then seal the first four prose gates and generate fresh formatting. Fresh every-page visual review, stored allocation/branches/lookups, representative initialized or natural gameplay and registered cumulative integration remain required. Reuse compatible technical proofs and do not repeat completed old batches.

Integrated23,778=14,181 revisions+9,597 retentions; historical source/prose/draft count23,781. Native story remainder2,120=Maria315+Lil1,805 includes this entire uncredited batch. Other shared/player-facing scope and the full207-name review remain separate inventories. Preserve all existing translations, retentions, ROMs, drafts, evidence and failed producers. All storylines and earlier unfinished contextual passes remain in scope, with early Rafael/tutorial priority, town/shop/random prose, names, wraps and glyph consistency. No guide photos. Deferred artwork and the later older-record technical re-audit remain separate. No worker is live.
'''
    checkpoint(mutation=ROOT/'clean_bindings_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria315 B286–B302 clean meanings/drafts sealed andcurrent bindings saved;allcomparisons andgates pending.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=0,justified_retentions=0,native_job_live=False,native_sessions=[],stored_job_live=False,stored_sessions=[],
            registered_build_live=False,registered_cumulative_build_live=False,current_batch_evidence=evidence,guide_photos=False,no_batch_worker_live=True,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',
            next_action='Compare all315 current/source records in whole exchanges;bind names andterms,then allfour prose gates andfresh formatting.'),
        new_entries={'Maria_SC3_B286_B302_clean_20261110':dict(new_credit=0,source_objects=315,complete_exchanges=17,
            source_speech_objects=196,physical_style_alternatives=113,typed_choice_labels=6,clean_source_selected=True,
            clean_meanings_andindependent_drafts_pending=False,clean_meanings=315,independent_drafts=315,
            clean_meanings_path=seal['source_meanings'],independent_drafts_path=seal['independent_drafts'],clean_source_draft_seal=str(sealpath),
            current_English_extracted_after_clean_seal=True,current_English_not_read=False,contextual_comparison_pending=True,names_terms_consumers_pending=True,
            current_name_getters_bound=26,current_scoped_actors_bound=13,current_dynamic_role_references_bound=119,
            all_five_review_gates_pending=True,all_fifth_gates_pending=True,registered_integration_pending=True,
            no_batch_worker_live=True,evidence=evidence,full_goal_complete=False)},
        summary=summary,document=document,document_text=text,completed=23778,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    save(ROOT/'clean_bindings_checkpoint.json',dict(document=document,evidence=evidence,new_credit=0,
        no_batch_worker_live=True,all315_contextual_comparisons_andfive_gates_pending=True,full_goal_complete=False))
    print('Published315 clean-first drafts andcurrent bindings;23778 integrated andtesting candidate unchanged.')

if __name__=='__main__':main()
