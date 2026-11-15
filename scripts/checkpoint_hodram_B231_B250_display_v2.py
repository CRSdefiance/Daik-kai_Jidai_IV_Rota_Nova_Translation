"""Save approved offline display/storage work without granting gameplay or release credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.approve_hodram_B231_B250_display_v2 import ROOT,VIEW,OUT as INPUT
from scripts.build_registered_hodram_B211_B230_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import LEDGER,PACKAGE

PROSE=Path('translations/hodram_B231_B250_contextual_review_v2.json')
NAMES=Path('translations/hodram_B231_B250_scoped_names_review_v1.json')
STORED=ROOT/'stored_v1/stored_native_verification.json'
LOOKUP=ROOT/'stored_catalogue_all_v1/all223_stored_effective_body_bindings.json'
LOADERS=ROOT/'loaders_v1/verification.json'
REBUILT=ROOT/'research_rebuilt_v1/reconstruction.json'

def main():
    prose,names,view,stored,lookup,loaders,rebuilt,release,ledger,package=map(load,
        (PROSE,NAMES,VIEW,STORED,LOOKUP,LOADERS,REBUILT,RELEASE,LEDGER,PACKAGE))
    assert prose['records_count']==225 and prose['counts']=={'retention':110,'revision':115}
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert view['final_speech_pages_visually_approved'] and view['all17_new_native_pages_directly_viewed']
    assert view['final_pages']==228 and view['visual_layout_revisions']==13 and view['visual_candidate_retentions']==9
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['all_stored_planes_equal_directly_viewed_compiled_planes']
    assert (stored['complete_stored_pages'],stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'],stored['fresh_relocated_native_relative_cases'])==(228,108,120,170)
    assert lookup['all223_ordinary_and_style_bodies_checked'] and lookup['all_new_effective_bodies_byte_exact_before_original_macro_expansion']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(325,36,614)
    assert len(rebuilt['changed_blocks'])==18 and rebuilt['unchanged_control_only_blocks']==[235]
    assert rebuilt['command_count']==359 and rebuilt['relative_sites']==34
    assert rebuilt['all_other_files_components_exact'] and rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    assert ledger['records_editorially_completed']==17308 and not ledger['full_goal_complete']
    summary=('Hodram B231–B250 has 225 contextual decisions: 115 proposed revisions and 110 justified retentions. '
        'All 19 scoped names are retained with reasons. All 228 final body pages and the menu/name sheets pass offline native and visual checks. '
        'Thirteen wraps improve; nine layout trials retain the better original. Stored checks and all 223 native lookups pass. '
        'Representative scene gameplay, fifth-gate sealing and registered integration remain. Integrated coverage stays 17,308; main is unchanged.')
    doc=f'''# Hodram B231–B250: approved offline display and stored reconstruction

{summary}

The [current contextual review](../{PROSE.as_posix()}) keeps exact clean/current references and all 225 individual source, context, localization and naturalness decisions. Its fifth gates remain false. The earlier 116/109 manuscript is preserved; only B239 R33 becomes a justified retention after the scoped item check confirms that “spirit beast” fits the magical-statue conversation. The other 224 prose decisions are unchanged. Preserve the existing clean-first meanings, drafts, current bindings and the 18 excluded, already-credited B237 records. Refer to the [previous contextual checkpoint](editorial_Hodram_B231_B250_contextual_20261107.md) for the complete exchange findings; do not repeat it as new review.

The [19 scoped name and role decisions](../{NAMES.as_posix()}) retain the approved public forms with individual source/context reasons. Thirty-eight current original name getters pass; exact clean static fields/pointers reuse the qualified constructor proof, without a new clean getter-permutation claim. Sailor and Retainer remain distinct original consumers. Native name planes use 12 fresh and seven exact cached strings, qualified by identical complete ARM9/font/COMMON dependencies. Both name sheets were directly viewed. Regional metadata remains metadata; no new biography or surname is inferred. Global name review and complete catalogue UI remain open.

The scoped term receipt at `work/Hodram_B231_B250_clean_20261107/scoped_terms_v1.json` binds 11 item fields, two Sofala aliases and the approved Spirit/Mood distinction. It does not insert unspoken Magic Leather Gloves, Poseidon's Roar or King Figurehead names into dialogue. B243's actual figurehead item is King Figurehead, not the unrelated Demon Figurehead. Both native and ASCII targets preserve control bytes. B239 R39's full-width F in Fernando and B244 R14's isolated full-width question mark are corrected and freshly checked in the native body planes.

Initial formatting produced 223 bodies/230 pages, with zero errors or warnings. All 892 native alignments passed. Every initial page was directly viewed across ten readable sheets, together with the menu and name sheets. The first visual trial is rejected and preserved: forcing one-page plans produced three weak-article endings and one impossible plan. Nine original layouts are explicitly retained with reasons; some proposed phrase constraints made openings sparse, added a page or displaced a better question tag. Thirteen scoped refinements pass with unchanged prose and native geometry. They improve short questions, phrase continuity and page tails; two speeches lose an unnecessary page turn. No QA waiver is used.

All 17 newly rendered pages passed 52 fresh alignments and direct visual review. The [qualified final native join](../work/Hodram_B231_B250_clean_20261107/final_native_v2/compiled_native_pages.json) uses 210 exact initial body proofs and 13 changed body proofs, totaling 228 final pages. The two eight-slot style objects preserve all 14 physical bodies and 16 alias slots exactly across layout refinement; their existing native compiler/getter proofs are bridged only after byte equality. The two-caption menu retains Try it / Leave it and passes complete provider, return, glyph, centering and bounds checks. The [visual approval and individual layout dispositions](../{VIEW.as_posix()}) bind all source/current/prose and compiled references.

The [complete research reconstruction](../{REBUILT.as_posix()}) changes only 18 eligible SC1 blocks, preserves control-only B235 and excludes credited B237. All 359 commands, three compound objects, 34 relative sites, exact clean/current block/archive/serialized ROM inverses and all unowned files/components pass. Its SHA-256 is `{rebuilt['research_ROM_sha256']}`. The ROM is retained and pinned as research; it is not a registered testing candidate. The registered ASCII right-bound runtime, font and all earlier accepted layers remain exact to parent Hodram B211–B230.

The [stored check](../{STORED.as_posix()}) passes 228 pages: 108 parity-dependent pages freshly checked, 120 exact planes reused, and 170 relocated native branch cases. All [223 original pre-macro stored-body lookups](../{LOOKUP.as_posix()}) pass. [Archive checks](../{LOADERS.as_posix()}) pass 325 complete loads/cache hits, 36 fresh parent cases and 614 qualified exact reuses. All terminal jobs exited zero. No job remains live.

These are offline checks. No B231–B250 scene gameplay has yet been observed. The separate 4,001-frame own-parent startup proves the route context, not activation of these scenes. Next use a focused, disclosed native-command emulator sequence for complete representative exchanges, four distinct FE panels, runtime substitutions, the two voice objects, the menu and revised page transitions. Preserve normal initializers and controls; disclose copied sequencing versus original branch routing. Visually inspect all new observed pages, identify remaining unvisited content and seal individual fifth gates only after the necessary evidence passes. Then register the cumulative successor, produce the exact clean-input patch and its own startup, and grant 225 records once. Do not rerun completed offline checks wholesale.

Integrated coverage remains 17,308: 10,584 revisions and 6,724 retentions. The registered candidate remains `{release['candidate']}`, SHA-256 `{release['candidate_sha256']}`. Main, clean input, canonical base, registered patch and weekend ZIP remain unchanged. All remaining routes, earlier unfinished contextual passes, town/shop/shared/random dialogue, names and player-facing prose stay in scope, with Rafael/tutorial priority preserved. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos are collected. The full goal remains active.
'''
    paths=(PROSE,NAMES,VIEW,STORED,LOOKUP,LOADERS,REBUILT,ROOT/'scoped_terms_v1.json',
        ROOT/'native_initial_v1/compiled_native_pages.json',ROOT/'final_native_v2/compiled_native_pages.json',
        ROOT/'name_planes_v1/native_name_planes.json',Path(__file__))
    checkpoint(mutation=ROOT/'display_storage_checkpoint_v2',batch_key='Hodram_B231_B250_clean_next_20261107',
        batch_updates=dict(new_credit=0,current_English_comparisons=225,remaining_current_English_comparisons=0,
            proposed_revisions=115,justified_retentions=110,all_four_prose_gate_records=225,
            scoped_names_reviewed=19,scoped_name_revisions=0,scoped_name_retentions=19,scoped_names_andterms_pending=False,
            fresh_native_body_pages_pending=False,initial_native_body_objects=223,initial_native_pages=230,
            initial_body_pages_directly_viewed=230,initial_body_sheets_directly_viewed=10,name_sheets_directly_viewed=2,menu_sheets_directly_viewed=1,
            final_offline_native_pages=228,new_layout_pages_directly_viewed=17,visual_layout_revisions=13,visual_candidate_retentions=9,
            final_formatting_andvisual_approval_pending=False,stored_reconstruction_pending=False,stored_native_pages_passed=228,
            stored_original_catalogue_lookups_passed=223,current_story_gameplay_utterances=0,representative_gameplay_pending=True,
            all_five_review_gates_pending=True,all_formatting_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,guide_photos=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence={str(p):digest(p) for p in paths}),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B231–B250: prose/names and all offline native, visual and stored checks complete.',
            next_action='Run representative initialized emulator fixtures, seal individual fifth gates and register the cumulative successor.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B231_B250_display_20261107.md',document_text=doc,
        completed=17308,protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved approved offline display/storage checkpoint. Integrated credit 17,308 and registered release unchanged; full goal remains active.')

if __name__=='__main__':main()
