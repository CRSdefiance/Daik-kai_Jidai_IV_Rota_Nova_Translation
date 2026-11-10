"""Save the complete Maria330 comparison intake without release changes or credit."""
from collections import Counter
from pathlib import Path
from scripts.meaning_maria330_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v9 import checkpoint


def main():
    meanings_path=ROOT/'all330_clean_meanings_v1.json';drafts_path=ROOT/'all330_independent_drafts_v1.json'
    proposals_path=ROOT/'all330_contextual_proposals_v1.json';current_path=ROOT/'current_v1/current_effective.json'
    objects_path=ROOT/'current_objects_v1/current_objects.json';names_path=ROOT/'scoped_names_macros_reference_v1.json'
    terms_path=ROOT/'scoped_item_stat_reference_v1.json';release_path=Path('work/maria328_release_v1/registered_release_verification.json')
    meanings,drafts,proposals,current,objects,names,terms,release=map(load,[meanings_path,drafts_path,proposals_path,current_path,objects_path,names_path,terms_path,release_path])
    assert len(meanings['records'])==len(drafts['records'])==proposals['records_count']==330
    assert meanings['source_meanings_sealed_before_independent_drafts'] and drafts['current_English_not_consulted']
    assert (proposals['revised'],proposals['retained'],proposals['complete_exchanges'])==(248,82,26)
    assert all(r['contextual_comparison_saved'] and r['finding'] and not any(r['review'].values()) for r in proposals['records'])
    assert all(r['retention_reason'] for r in proposals['records'] if r['decision']=='retention')
    assert Counter(r['kind'] for r in proposals['records'])==Counter({'ordinary-speech':293,'physical-style-alternative':35,'typed-menu-caption':2})
    assert current['original_current_catalogue_lookups']==293 and len(objects['style_objects'])==6
    assert objects['native_style_getter_cases']==48 and len(objects['choice_objects'])==1 and objects['choice_objects'][0]['count']==2
    assert names['scoped_actors']==26 and names['original_native_name_getters']==52 and len(names['default_macro_cases'])==4
    assert len(terms['items'])==13 and terms['UI'][0]['current']['text']=='Spirit'
    assert current['runtime']==objects['runtime']==proposals['runtime']==names['runtime']==terms['runtime']
    assert current['current_ROM_sha256']==release['candidate_sha256'] and digest('translations/release_stack.json')==release['registry_sha256']
    nonascii=[r for r in proposals['records'] if not r['current_comparison_paragraph'].isascii()]
    mixed=[r['id'] for r in nonascii if any(0xff21<=ord(c)<=0xff5a for c in r['current_comparison_paragraph'])]
    untranslated=[r['id'] for r in nonascii if any(0x3040<=ord(c)<=0x9fff for c in r['current_comparison_paragraph'])]
    assert len(nonascii)==30 and mixed==['DK4_MES_B105_R0023','DK4_MES_B110_R0011','DK4_MES_B121_R0019']
    assert untranslated==['DK4_MES_B118_R0008']
    paths=[meanings_path,drafts_path,proposals_path,current_path,objects_path,names_path,terms_path,
        ROOT/'source_selection_v1.json',ROOT/'clean_source_packet.json',ROOT/'current_inputs_v1/sealed_drafts.json',
        ROOT/'current_inputs_v1/projection.json',release_path,Path(__file__)]
    evidence={str(p):digest(p) for p in paths}
    summary=('Maria B96–B124 has 330 saved clean meanings, independent drafts and individual contextual comparisons across 26 complete exchanges: '
        '248 proposed revisions/82 justified retentions. Findings include one still-Japanese line, three mixed full-width Latin lines, '
        'an Indian Ocean geography error and missing personal/emotional distinctions. Thirteen items, Spirit, 26 scoped names/52 getters '
        'and four default macros are reference-bound. Final names/terms/roles, prose gates, fresh formatting/visual/gameplay and integration remain. '
        'No new ROM or credit; integrated20,689 and registered c20375bf/main/full scope are unchanged.')
    text='''# Maria330 comparison checkpoint — November 9, 2026

**330 clean-source meanings, independent drafts and individual comparisons are saved in 26 complete exchanges.** There are 248 proposed revisions and 82 justified retentions. This is progress, with zero completion credit. Every individual v2 gate remains false pending final reconciliation and display checks.

Continue under `work/Maria_B96_B124_clean_20261109`. `all330_contextual_proposals_v1.json` binds each exact source/current span and bytes, Japanese, meaning, scene context, independent draft, proposed paragraph, finding and retention reason. Clean meanings preceded independent drafts, which preceded this intake's current-English extraction. The historical unconsulted flags describe those saved stages, not a blanket claim of no prior exposure.

The complete blocks are 96/98/99/100/101/102/103/104/105/106/107/110/111/112/113/114/115/116/117/118/119/120/121/122/123/124. The completed native census is reused, with all selected clean positions rechecked and disjoint from credited keys. Numeric block order does not assert earned chronology. The batch contains 293 ordinary bodies, 35 physical alternatives in six eight-slot style objects, and two captions in one two-choice menu. Eight bodies use FE. Source selectors207/209 and styles208/209/214/220 require the established dynamic-role contract; do not assign invented fixed companions. FI/FA/FO substitutions remain live. No ordinary authored line breaks were introduced.

Findings include Maria's personal moral doubts changed to collective claims; families and companions whose suffering must not become invented deaths; a child proposing figurehead use reduced to a noun; lost past/present alternatives in her pirate epithet; a metaphorical demon vow made into a transformation; loss of the Chinese taught-phrase joke; Indian Ocean mistranslated as great southern ocean; a grant still in Japanese; and a child's This mistranslated as One. Preserve the execution account's explicit reward, desertion charge, death sentence, family pension, fear and sorrow. Do not soften it or add a military rank. Clifford is defeated, not explicitly dead. Diagram use involves dismantling the bamboo object. Maps and Proofs themselves remain distinct.

There are 30 non-ASCII current targets, including three mixed-width Latin defects: B105R23, B110R11 and B121R19. B118R8 remains Japanese. All have ASCII proposals; none is yet claimed visually repaired. These are text-display issues, separate from deferred artwork.

`current_v1/current_effective.json` binds 293 original current lookups on registered Maria328's own captain3 startup context. `current_objects_v1/current_objects.json` binds all six style objects/48 original getters and two caption spans; menu provider/return tests remain pending. `scoped_names_macros_reference_v1.json` binds 26 actors/52 short/full native getters and FI=Maria, FA=Li, FO=Li Clan, FU=Maria Huamei Li. These readbacks are not editorial or font approval. Keep approved names, including Hodram/Joakim/Maria/Cristina; do not globally rename Boy163 to Mao or infer family from familiar address.

`scoped_item_stat_reference_v1.json` binds 13 exact current registered item labels and Spirit. Reconcile provisional drafts to Guiding Staff, Evergreen Lotus Leaf, Tang Bamboo Craft, Bamboo Assembly Plan, Upper/Lower Stone Tablet, Red Dye and Lotion Jar, while preserving natural descriptive sentences and source facts. Retain Ancient Kingdom Coin, Kushan Platter, Patterned Cloth, Brass Lamp and Old Parchment. Nagalpur in draft/company prose differs from current actor38 Nagarpur and needs scoped reconciliation. The earlier source-qualified Soaring Scarlet Orca term is documented in `docs/name_source_review_v294.md` and integrated Maria301 B28; bind that exact unchanged anchor rather than repeat its dictionary investigation or conflate the separate Shachihoko item. Spirit is already bound to its exact stat pointer. Complete the individual name/role editorial choices and final whole-English reread before approving prose gates.

Next format selected logical paragraphs using validated consumer widths, inspect every new page and boundary, run stored/allocation/control/substitution/glyph checks, and use representative focused gameplay for distinct behavior and transitions. Reuse compatible proofs and preserve all source controls, menu order, style aliases and native relative commands. No new pages, gameplay observations or reachability coverage are claimed for this batch. Original conditions, locations, rewards and hardware remain unvisited. No guide photos are requested.

Registered cumulative candidate remains `work/maria328_release_v1/all_routes_maria328_candidate.nds`, SHA-256 `c20375bfc50a4d5973bfad203f3c45db9ae4b3dada0d328610c79fa19e908692`, with715 manifest entries/114 accepted layers/50 passing checks, exact clean-input patch and own startup. The user's old Rafael2952 Market Goods Info defect is fixed there, including both Local/Cargo pointers. Preserve the registered market allocation, six-section ARM9, ASCII right-bound fix, source25 v2 guard and all earlier corrections. No new ROM was built; main was not promoted. Integrated20,689 and remaining native story5,209 (Lil1,805/Maria3,404) are unchanged. Full unfinished storyline/shared/town/shop/random/name/player-prose scope, earlier contextual passes, separate artwork and later older-record technical re-audit remain active. All ROMs, translations and evidence are preserved. No worker is live.
'''
    checkpoint(mutation=ROOT/'comparison_progress_checkpoint_v1',batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0,current_batch='Maria330:330 clean meanings/drafts/comparisons;248 proposed revisions/82 retentions.',
            current_batch_not_yet_integrated=True,current_batch_registered_andcredited_once=False,all_current_batch_fifth_gates_pending=True,
            proposed_revisions=248,justified_retentions=82,native_job_live=False,registered_build_live=False,guide_photos=False,
            next_action='Reconcile exact names/items/epithet and dynamic roles; final whole-prose reread before prose gates and fresh formatting.',current_batch_evidence=evidence),
        new_entries={'Maria_SC3_B96_B124_clean_20261109':dict(new_credit=0,source_meanings_saved=330,independent_drafts_saved=330,
            contextual_comparisons_saved=330,proposed_revisions=248,justified_retentions=82,complete_exchanges=26,
            selected_contextual_proposals=str(proposals_path),selected_contextual_proposals_sha256=digest(proposals_path),
            source_meanings_anddrafts_preceded_current_comparison=True,all_five_individual_gates_pending=True,
            reference_bound_items=13,reference_bound_scoped_names=26,reference_native_name_getters=52,
            non_ASCII_current_targets=30,mixed_fullwidth_Latin_targets=mixed,untranslated_current_targets=untranslated,
            registered_integration_pending=True,current_batch_actual_gameplay_observations=0,progress_evidence=evidence)},
        summary=summary,document='docs/editorial_Maria330_comparisons_20261109.md',document_text=text,completed=20689,
        protected={'translations/release_stack.json':release['registry_sha256'],release['candidate']:release['candidate_sha256'],
            release['manifest']:release['manifest_sha256'],release['patch']:release['patch_sha256'],release['canonical_base']:release['canonical_sha256']})
    print('Saved Maria330 checkpoint:330 comparisons,248 proposed revisions/82 retentions;no new credit or release change.')

if __name__=='__main__':main()
