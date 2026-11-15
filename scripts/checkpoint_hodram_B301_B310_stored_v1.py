"""Save the finished offline pass without claiming gameplay or integration credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load
from scripts.prepare_hodram_B301_B310_formatting_v1 import ROOT,PROSE
from scripts.build_registered_hodram_B281_B300_v1 import RELEASE,REGISTRY
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v7 import checkpoint
from scripts.save_rafael3222_weekend_checkpoint_v1 import PACKAGE

def main():
    paths={
        'visual':ROOT/'final_visual_approval_v6.json',
        'reconstruction':ROOT/'reconstruction_v1/reconstruction.json',
        'stored':ROOT/'stored_v1/stored_native_verification.json',
        'loaders':ROOT/'loaders_v1/verification.json',
        'catalogue':ROOT/'stored_catalogue_all_v1/all225_stored_effective_body_bindings.json',
        'names':Path('translations/hodram_B301_B310_scoped_names_review_v1.json'),
        'terms':ROOT/'scoped_terms_v1.json',
        'styles':ROOT/'native_style_delta_v6/compiled_style_objects.json',
        'names_visual':ROOT/'scoped_names_visual_approval_v1.json',
        'fixtures':ROOT/'focused_fixtures_v1/fixtures.json',
    }
    data={k:load(p) for k,p in paths.items()}
    prose=load(PROSE);view=data['visual'];rebuilt=data['reconstruction'];stored=data['stored']
    assert len(prose['records'])==234 and prose['counts']==dict(revision=127,retention=107)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in prose['records'])
    assert view['final_speech_pages_visually_approved'] and view['final_pages']==228
    assert (view['visual_layout_revisions'],view['visual_candidate_retentions'],view['corrected_FE_split_words'],view['scoped_punctuation_glyph_fixes'])==(18,1,1,1)
    assert rebuilt['changed_blocks']==list(range(301,311)) and rebuilt['compound_objects']==27
    assert (rebuilt['command_count'],rebuilt['relative_sites'])==(264,38)
    assert (stored['complete_stored_pages'],stored['typed_labels_checked'],stored['fresh_relocated_native_relative_cases'])==(228,9,190)
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'])==(35,193)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert (data['loaders']['fresh_whole_archive_loads_andcache_hits'],data['loaders']['fresh_parent_cases'],data['loaders']['exact_reused_parent_cases'])==(325,20,630)
    assert data['catalogue']['all225_ordinary_and_style_bodies_checked'] and len(data['catalogue']['records'])==225
    assert data['names_visual']['all8_name_strings_directly_viewed']
    for key in ['stored','loaders']:assert data[key]['reconstruction_sha256']==digest(paths['reconstruction'])
    assert data['catalogue']['stored_sha256']==digest(paths['stored'])
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    fixture=data['fixtures']['fixtures'];assert len(fixture)==1
    assert (fixture[0]['utterances'],fixture[0]['pages'],fixture[0]['menus'],fixture[0]['frames'])==(96,97,4,29201)
    release,package=map(load,(RELEASE,PACKAGE))
    summary=('Hodram B301–B310 has234 contextual decisions:127 proposed revisions and107 justified retentions. '
        'All228 final pages, eight scoped names and four menus pass offline native/visual checks. '
        'Eighteen layouts improve; one better original is retained. One native FE split-word defect and one glyph target are corrected. '
        'Stored checks pass228 pages, nine captions,190 branch cases and225 catalogue lookups; archive loading passes. '
        'Representative gameplay and registered integration remain. Integrated coverage stays18,133; main is unchanged.')
    document=f'''# Hodram B301–B310: offline display and storage checkpoint

{summary}

The [contextual manuscript](../{PROSE.as_posix()}) preserves every exact clean/current reference and all234 prose decisions. Reuse the [contextual checkpoint](editorial_Hodram_B301_B310_contextual_20261107.md) for the source findings; no dialogue wording changed during this formatting pass. Scope remains73 ordinary speeches,152 physical voice alternatives/184 alias slots in23 objects, and nine captions in four menus. B308 is style-only, not control-only. All234 individual fifth gates remain false pending the remaining required proofs. These objects have no integrated credit yet.

The [scoped name review](../{paths['names'].as_posix()}) justifies all eight retentions. Sixteen fresh original progressive/full-name getters pass; all eight name strings were directly viewed. Hodram/Joakim, Gerhard, Senior Monk, Sailor/Retainer, Matilda, Safia, Mihwa and Sakura retain their source-bound identities and distinct consumers. 高僧 supports Senior Monk, without an invented abbot office. Regional metadata is not treated as a surname, biography or relationship. Global207/full-catalogue UI and future conditional role assignments remain unvisited.

The [term receipt](../{paths['terms'].as_posix()}) binds item45 Kublai's Greatsword and item171 Golden Temple Map from fresh own RAM, preserving20 nonname metadata bytes. The map's Japanese label is descriptive, not literally Kinkaku-ji; spoken Kinkaku-ji remains the monk's proper temple identifier. The failed initial label assumption remains preserved. Proof of Conquest reuses compatible reviewed HELP_TOPIC33 evidence. This establishes no map ownership, purchase, destination activation or new HELP UI coverage.

The [final visual approval](../{paths['visual'].as_posix()}) records all229 initial pages and21 changed pages directly viewed in readable sheets, plus every scoped name and menu sheet. Final output has225 bodies/228 pages. Eighteen layouts improve phrase continuity, question tags and page boundaries; one prompt/treatment layout retains the better balanced original because its trial added a row and another split. One Proof-map reminder now fits one page without shortening prose. Three other long passages retain necessary two-page layouts while keeping their final sentences intact. All19 candidates have individual dispositions. No ordinary manual breaks, QA waivers, font/engine changes or shortened prose are introduced.

At B309 R294 the first native trial split appear into appea and a lone r before the protected LF. This was a split-word defect, not a blank row or lost glyph. A source-bound FE36 planning budget fixes that record while preserving228-pixel native geometry and all prose/controls. The final layout also keeps Some appear together; do not count the same record twice as two unique repaired records. B307 R55 uses an ASCII ellipsis in place of the inconsistent punctuation glyph. All complete leading/internal/trailing characters, substitutions, controls, bounds, guards, consumption and pagination pass.

Only18 changed bodies were freshly rerendered after the initial pass:72 placement alignments. The207 unchanged bodies reuse byte-identical native proof, yielding900 final alignment cases. Five changed voice objects receive40 fresh original target-slot cases/45 negative cases;18 unchanged objects reuse exact proofs, covering all184 slots/207 negative cases. All four menus pass their complete native caption/highlight/provider checks. The eight FE notices include a captain FI injury substitution through the distinct null-actor ABI.

The [research reconstruction](../{paths['reconstruction'].as_posix()}) changes only ten reviewed SC1 blocks over registered B281–B300. Every other file/component, prior artwork/name/runtime layer and whole serialized parent inverse remains exact. Research ROM SHA-256: `{rebuilt['research_ROM_sha256']}`. This is not a registered handoff or main build. All generated ROMs remain preserved.

The [stored proof](../{paths['stored'].as_posix()}) checks228 pages:35 freshly rendered parity-dependent pages and193 exact compiled-plane reuses; all nine captions and190 relocated native branch cases pass. The [catalogue proof](../{paths['catalogue'].as_posix()}) verifies225 complete pre-macro native lookups with input guards and unowned RAM exact. The [archive proof](../{paths['loaders'].as_posix()}) checks325 complete loads/cache hits,20 fresh parent cases and630 compatible exact reuses. These are offline checks.

A [focused fixture](../{paths['fixtures'].as_posix()}) is prepared for96 utterances/97 pages and all four menus over29,201 frames. It copies all73 ordinary speech commands and23 whole style commands at original startup assignments in inventory order. It is not yet observed gameplay at this checkpoint. It does not activate original optional events, route branches, stat effects, rewards or chronology. Current own-parent4,001-frame startup evidence is not B301–B310 scene coverage. Other physical voice alternatives and catalogue UI remain unvisited. No test/build process remains live at this checkpoint.

Next run that representative emulator sequence, compare actual body/header/menu pixels and transitions, then seal all234 fifth gates and integrate a registered cumulative successor with an exact clean-input patch and its own startup. Reuse these completed proofs; do not restart the batch. Integrated totals remain18,133:11,009 revisions/7,124 retentions; historical source/prose/draft counters remain18,136. Main, current registered candidate, clean/canonical inputs, accepted layers, ASCII right-bound correction and weekend package are unchanged. The full goal stays active across every storyline, unfinished earlier contextual pass, shared town/shop/random exchange, names and remaining player-facing prose, with Rafael/tutorial priority. Deferred graphics artwork and the later older-record technical re-audit remain separate. No guide photos.
'''
    evidence={str(p):digest(p) for p in [PROSE,*paths.values(),Path(__file__)]}
    checkpoint(mutation=ROOT/'stored_checkpoint_v1',batch_key='Hodram_B301_B310_clean_next_20261107',
        batch_updates=dict(new_credit=0,scoped_names_pending=False,scoped_terms_pending=False,fresh_native_body_pages_pending=False,
            scoped_name_actors_reviewed=8,scoped_name_strings_checked=8,fresh_original_name_getters=16,
            stored_reconstruction_pending=False,final_native_pages=228,visual_layout_revisions=18,justified_layout_retentions=1,
            FE_split_word_wrap_fixes=1,glyph_targets_corrected=1,stored_pages_passed=228,typed_captions_checked=9,
            native_relative_cases_passed=190,stored_catalogue_lookups_passed=225,archive_loading_pass=True,
            current_story_gameplay_utterances=0,representative_gameplay_pending=True,registered_integration_pending=True,
            all_five_review_gates_pending=True,all_formatting_gates_pending=True,native_job_live=False,registered_build_live=False,
            contextual_manuscript=str(PROSE),contextual_manuscript_sha256=digest(PROSE),evidence=evidence),
        additional_updates={'editorial_execution_priority_20261104':dict(new_credit=0,
            current_batch='Hodram B301–B310:234 contextual decisions and228 offline display/stored pages pass.',
            next_action='Observe prepared96-utterance/97-page focused fixture, seal individual fifth gates and register cumulative integration with exact clean patch and own startup.',
            current_batch_not_yet_integrated=True,all_current_batch_fifth_gates_pending=True,registered_integration_pending=True,
            native_job_live=False,registered_build_live=False,registered_cumulative_build_live=False,guide_photos=False)},
        summary=summary,document='docs/editorial_Hodram_B301_B310_stored_20261107.md',document_text=document,completed=18133,
        protected={str(REGISTRY):release['registry_sha256'],release['canonical_base']:release['canonical_sha256'],
            release['candidate']:release['candidate_sha256'],release['patch']:release['patch_sha256'],package['zip']:package['zip_sha256']})
    print('Saved234 contextual decisions and228 offline pages; integrated18,133 unchanged. Full goal active.')

if __name__=='__main__':main()
