"""Save the complete mixed255-object storage pass and the authoritative failed679 terminal."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.save_editorial_progress_checkpoint_v5 import checkpoint
from dk4tool.patch.grand_race_menu_release import sha

DOC=Path('translations/rafael_B101_B120_contextual_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/Rafael255_layout_v1_20261105/automatic_plans.json')
INPUTS=Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105')
REBUILD=Path('work/analysis/Rafael255_rebuilt678_v2_20261105/reconstruction.json')
STORED=Path('work/analysis/Rafael255_stored_native_v3_20261105/stored_native_verification.json')
CAT=Path('work/analysis/Rafael255_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json')
LOADERS=Path('work/analysis/Rafael255_loaders_v1_20261105/verification.json')
FAILED=Path('work/analysis/Rafael261_registered_build_20261105/completion.json')
KEY='Rafael_SC0_B101_B120_clean_20261105'

if __name__=='__main__':
    doc,plan,rebuild,stored,catalogue,loaders,failed=map(load,[DOC,PLAN,REBUILD,STORED,CAT,LOADERS,FAILED])
    assert len(doc['records'])==255 and (doc['proposed_revisions'],doc['justified_retentions'])==(135,120)
    assert all(r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False) for r in doc['records'])
    assert len(plan['records'])==243 and sum(r['expected_native_pages'] for r in plan['records'])==248 and not plan['failures']
    assert (len(stored['records']),len(stored['style_records']),stored['typed_labels_checked'],stored['complete_stored_pages'])==(229,14,12,248)
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['fresh_relocated_native_relative_cases']==180 and len(stored['relative_cases'])==36
    assert (stored['fresh_parity_dependent_pages'],stored['exact_compiled_pages_reused'])==(110,138)
    assert len(stored['prior_completed_block_receipts_reused'])==2
    assert len(catalogue['records'])==243 and catalogue['all243_ordinary_andphysical_style_bodies_checked']
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases'])==(343,36,650)
    terminals=[Path('work/analysis')/name/'completion.json' for name in [
        'Rafael255_stored_gc_v3_20261105','Rafael255_catalogue_gc_v1_20261105','Rafael255_loaders_gc_v1_20261105']]
    for path in terminals:
        terminal=load(path);assert terminal['terminal'] and terminal['completed_without_exception'] and terminal['all_locked_sources_unchanged']
        assert not terminal['garbage_collection']['errors']
    assert failed['terminal'] and not failed['driver_completed_without_exception'] and failed['all_original_driver_andregistry_bytes_unchanged']
    assert failed['elapsed_seconds']==5195.8 and not Path(failed['out']).exists() and not Path(failed['out']).with_suffix('.manifest.json').exists()
    assert 'MemoryError' in FAILED.with_name('failure_traceback.txt').read_text()
    assert sha(Path('translations/release_stack.json').read_bytes())==failed['registry_sha256']
    for path,digest in failed['driver_andcanonical_bytes'].items():assert sha(Path(path).read_bytes())==digest
    assert sha(Path('dk4tool/rom/nds.py').read_bytes())==failed['original_locked_ROM_core_sha256']
    ledger=load('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==11845
    completed={(r['file_path'],r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    keys={(r['file_path'],r['id']) for r in doc['records']};assert len(keys)==255 and not keys&completed
    mutation=Path('work/analysis/Rafael255_storage_checkpoint_20261105');assert not mutation.exists()
    census=Path('work/analysis/Rafael255_completed_overlap_census_20261105.json');assert not census.exists()
    save(census,dict(source_objects=255,ordinary_speeches=229,style_physical_alternatives=14,choice_labels=12,
        completed_overlap=[],all255_unique_source_keys=True,earlier241_coverage_preserved=True,
        ledger_sha256=sha(Path('translations/editorial_review_current_v1.json').read_bytes()),ledger_completed=11845,new_credit=0))
    summary=('Rafael’s early storyline and all tutorials remain first. B101–B120 now covers 255 text objects: 135 proposed revisions and 120 justified retentions, with all four prose gates passed. '
        'The reconstruction preflight found two additional personality objects; all 14 variants are reviewed and checked, preserving the earlier 241 records exactly. '
        'All 243 speech variants/248 pages, 12 captions, two eight-slot tables, 180 branch cases, 243 catalogue lookups and 343 loads/cache hits pass offline. '
        'Research image b0eee86f preserves all unowned files and has an exact parent inverse. Representative gameplay, fifth gates and integration remain pending. '
        'Original registered679 build73098/PID105028 is terminal1 after a MemoryError at5195.8 seconds; no candidate or manifest, all locked sources unchanged. It has not been restarted. '
        '11845 integrated; verifiedcc71/main unchanged. Full scope, translations, ROMs and evidence preserved; no guide photos or main promotion.')
    text=f'''# Rafael255 storage checkpoint — November 5, 2026

Rafael’s early storyline and all tutorials remain first. The full editorial objective stays in scope, including other routes, unfinished contextual passes of earlier translations, town/shop exchanges, random scenes, names, glyphs and remaining prose. No guide photos, promotion, pruning or commit/push.

## Complete source inventory and prose decisions

`{DOC}` contains **255 individual contextual reviews: 135 proposed revisions and 120 justified retentions**. All four prose gates pass; all fifth formatting gates remain false until representative gameplay and the remaining release work are complete.

The plain reconstruction preflight correctly rejected the assumption that these blocks had no personality objects. Clean source contains two `4100` commands: B113 at10 and B119 at16. They hold fourteen distinct bodies across sixteen style slots. Those fourteen meanings and independent drafts were saved before decoding their current English; prior whole-command hex exposure is explicitly disclosed. Eleven existing versions already worked and were retained with individual reasons; three were revised. The earlier241 reviewed records remain exactly unchanged. All255 source keys are unique and absent from completed coverage; see `{census}`.

Source and current bindings for the added objects: `work/analysis/Rafael14_style_current678_20261105/current_objects.json`. Role proof: its sibling `roles0_1.json`. Native selector207 is role0, resolving to Rafael in this own startup; selector208 is role1, unassigned in the strict query and falling back to Sailor151/voice4 in the original speech resolver. Both stay dynamic. No static actor207/208 table access, role assignment, roster change or claim about original conditional scene participation.

The existing eighteen scoped name decisions, seven item references and all source-fidelity corrections are preserved. Reuse [the preceding prose/display checkpoint](editorial_Rafael241_native_checkpoint_20261105.md) for the original241 findings; do not repeat their history or reviews. In particular, retain the grandfather joke, source uncertainty, correct clan/descendant distinction, religious context, exact clues and unspoken relationships/ranks.

## Display and stored-script evidence

`{PLAN}` has243 speech variants and248 body pages, with zero errors or warnings. `{INPUTS/'native.json'}` joins fourteen fresh native/viewed pages with the exact229 prior body proofs. Both new readable sheets were viewed; every earlier approved page, caption and name plane is reused only where bytes and dependencies match. Native expansion coverage is972 composite alignment cases, not one run. All source-specific FE guard corrections, wrapping refinements and justified layout retentions remain intact.

The two complete personality objects pass all sixteen target slot/getter cases and eighteen semantic rejection checks. Source alias equivalence and header selector/flag bytes remain exact. The formatter’s virtual `D0` prefix is excluded from stored style bodies. The four three-choice menus retain twelve labels,24 provider alignments,96 bridged returns and48 caption/style planes; their exact earlier proofs are reused.

`{REBUILD}` reconstructs eighteen changed blocks:101–105 and108–120. B106/B107 remain byte-identical control-only blocks. It preserves406 native commands,36 relative sites, both personality tables and all four menus. Only owned SC0 data changes; all other files/components and the complete archive/serialized parent inverse pass. The research ROM is `{rebuild['research_ROM']}`, SHA-256 **`{rebuild['research_ROM_sha256']}`**. It is pinned and is not a registered playable candidate.

`{STORED}` passes all229 ordinary speeches,14 physical style bodies,12 captions and248 pages. It freshly checks110 parity-dependent pages and reuses138 exact native pages. All complete leading/internal/trailing glyphs, native row membership, pixels, bounds, canaries, allocation, consumption and pagination pass. Thirty-six relocated relative sites pass180 native branch cases. Two durable completed block receipts are reused, with exact input/runtime/hash qualification.

`{CAT}` proves all243 stored ordinary/style bodies survive the original pre-macro catalogue lookup byte-for-byte. Physical style bodies are checked without stripping a nonexistent stored prefix. `{LOADERS}` passes343 whole native loads/cache hits and686 parent handoffs:36 fresh changed-block modes and650 exact prior modes. The correctly matching prior is `Rafael330_loaders_v3_20261105`; earlier v1/v2 modes differ in B81 and were not reused.

These are offline checks. There is no new gameplay, original-location, natural event, earned chronology, complete route, hardware, item-card or global207/full-catalogue UI approval. The255 fifth gates and new completion credit remain pending.

## Preserved failures and memory handling

The first stored checker stopped on JSON string keys in the host dynamic-selector map; v2 restores integer keys without changing game inputs. V2 then stopped with a host `MemoryError` after saving completed B101/B102 receipts. V3 reuses those exact receipts and completes all remaining checks under `{terminals[0]}`. System allocation plus regular collection of unreachable Python/native callback cycles kept peak private memory near246MB. No native assertion, instruction guard, renderer, input state or ROM core was relaxed. The two failed runs and all partial evidence are preserved; they are not whole-run passes.

The catalogue and loader jobs are also terminal0 under the same wrapper, with locked sources unchanged and collector errors empty. There are no live jobs from this checkpoint.

The **original registered679 build73098/PID105028 is terminal1**, not a wait: `{FAILED}` records a `MemoryError` in `NdsImage.path_map/iter_files` during late-editorial extension verification at5195.8 seconds. There is no679 candidate or manifest. The registry, all nine original drivers/dependencies and locked core remained exact. Do not run final candidate verification or grant261 credit against that failed build. No retry was launched here.

The original core is still `27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963`; the archived payload-free lookup optimization remains unadopted because historical dependency guards require the original core. Do not bypass those guards or substitute a research image for a registered release. The observed memory failures do not establish a ROM/text defect or prove that a future cumulative retry will succeed. Before retrying, preserve the failure, use an isolated low-memory process and avoid overlapping heavy ROM/emulator jobs. All required registered checks and eight final stages remain mandatory.

## Continue from here

1. Run representative initialized gameplay for the full255-object batch: new public headers, dynamic207/208, both native personality objects, FE period/four-row riddle behavior, the four three-choice menus with all cursor states and normal acceptance, and meaningful multi-page transitions. Use complete exchanges where useful and explicitly list unvisited content. Existing offline checks need no repetition.
2. Extend `prepare_reviewed_dialogue_fixtures_v1.py` carefully for complete `4100` commands. It currently copies only ordinary speeches and menus; never turn a virtual style prefix into a stored speech preamble. The source-tested roles in `roles0_1.json` select voice4/Sailor fallback for208 here; other variants remain offline-only unless observed. The actual analyzer also needs explicit dynamic-header handling; source selectors207/208 are not ordinary actor IDs.
3. Once necessary checks pass, close the fifth gates and integrate through a registered cumulative release with an exact clean-input patch. The earlier261 already have complete research checks; their registered build failed before candidate emission. Consider combining ready261+255 batches in the next cumulative attempt to avoid two full rebuilds, while retaining the full registry prefix, all accepted layers, every check and clear provenance. This is a possible next workflow, not a prepared/registered build or permission to bypass a failed prefix.

The current255 research image uses verified678 (`cc71ec06…`) as parent and does **not** contain the pending261 revisions. To combine them, copy only the eighteen owned B101–B120 blocks onto the qualified261 target; never overwrite a newer whole SC0 archive with this older-parent research archive. Preserve every ROM, earlier translation and proof.

Integrated totals remain **11845 =6836 revisions +5009 retentions**; historical source/prose11848 is unchanged. Verified experimental parent: `out/all_routes_combined_help97_rafael330_20261105_candidate.nds`, SHA-256`cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448`. Main remains `out/raphael_natural_v2_accepted_base.nds`, SHA-256`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`. Registry `11021a16…`;114 accepted layers and all eight runtime/name/data stages, including ASCII right bounds and Fernan’s F, remain unchanged. Graphics artwork and the later older-record technical re-audit remain separate. Full goal active.
'''
    protected={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,REBUILD,STORED,CAT,LOADERS,FAILED,*terminals,
        INPUTS/'native.json',INPUTS/'menu.json',INPUTS/'styles.json',
        Path('translations/release_stack.json'),Path('dk4tool/rom/nds.py'),Path(rebuild['research_ROM']),
        Path('out/all_routes_combined_help97_rafael330_20261105_candidate.nds'),Path('out/raphael_natural_v2_accepted_base.nds')]}
    protected.update(failed['driver_andcanonical_bytes'])
    checkpoint(mutation=mutation,completed=11845,protected=protected,batch_key=KEY,summary=summary,
        document='docs/editorial_Rafael255_storage_checkpoint_20261105.md',document_text=text,
        batch_updates=dict(new_credit=0,source_speeches=229,source_style_physical_alternatives=14,source_style_command_objects=2,
            source_choice_captions=12,source_objects=255,contextual_comparisons=255,proposed_revisions=135,justified_retentions=120,
            all_previous241_reviews_preserved_exact=True,all255_four_prose_gates_pass=True,four_gate_passes=255,
            contextual_manuscript=str(DOC),contextual_manuscript_sha256=sha(DOC.read_bytes()),
            completed_overlap_census=str(census),completed_overlap_census_sha256=sha(census.read_bytes()),
            source_dynamic_selectors=[207,208],scoped_identity='work/analysis/Rafael255_extended_identity_20261105.json',pending_name_term_holds=0,
            offline_native=str(INPUTS/'native.json'),offline_native_sha256=sha((INPUTS/'native.json').read_bytes()),
            offline_complete_speeches=243,offline_body_pages=248,offline_style_objects=2,offline_choice_captions=12,offline_menus=4,
            reconstruction=str(REBUILD),reconstruction_sha256=sha(REBUILD.read_bytes()),research_ROM=rebuild['research_ROM'],research_ROM_sha256=rebuild['research_ROM_sha256'],
            stored_native=str(STORED),stored_native_sha256=sha(STORED.read_bytes()),stored_body_pages=248,native_relative_cases=180,
            stored_catalogue=str(CAT),stored_catalogue_sha256=sha(CAT.read_bytes()),all243_catalogue_lookups_pass=True,
            loader_proof=str(LOADERS),loader_proof_sha256=sha(LOADERS.read_bytes()),whole_native_loads=343,parent_handoffs=686,
            stored_script_catalogue_andloaders_complete=True,stored_script_catalogue_loaders_actual_gameplay_andintegration_pending=False,
            actual_gameplay_andregistered_integration_pending=True,all_fifth_formatting_gates_pending=True,actual_gameplay=False,new_captures=0,guide_photos=False),
        additional_updates={
            'Rafael261_registered_cumulative_20261105':dict(new_credit=0,build_live=False,build_terminal=True,build_failed=True,
                failed_session=73098,failed_PID=105028,terminal_proof=str(FAILED),terminal_proof_sha256=sha(FAILED.read_bytes()),
                failure_reason='Host MemoryError inlocked path_map/iter_files duringlate-editorial verification;no candidate ormanifest.',
                no_registered_candidate_emitted=True,registered_manifest_patch_RAM_binding_andonce_only_credit_pending=True),
            'Rafael_SC0_B85_B100_contextual_20261105':dict(new_credit=0,registered_build_live=False,registered_build_terminal=True,
                registered_build_failed=True,registered_integration_pending=True,all261_five_research_gates_pass=True),
            'Rafael_SC0_B81_B100_clean_20261105':dict(new_credit=0,next261_registered_build_live=False,next261_registered_build_terminal=True,
                next261_registered_build_failed=True,next261_registered_failure_proof=str(FAILED)),
            'editorial_execution_priority_20261104':dict(new_credit=0,current_batch=KEY,
                current255_four_gate_passes=255,current255_name_term_holds=0,current255_native_pages=248,current255_stored_catalogue_loaders_complete=True,
                current255_actual_gameplay_andfifth_gates_pending=True,registered_cumulative_build_live=False,registered_build_live=False,build_live=False,
                registered_build_terminal=True,registered_build_failed=True,registered_integration_pending=True,
                registered_build_session=73098,registered_build_PID=105028,build_session=73098,build_PID=105028,
                next_focus='Focused255 gameplay including dynamic207/208 andcomplete4100 commands;close necessary research gates,then prepare a full registered cumulative attempt. Original679 isterminal1;no restart orcredit yet.'),
        })
    print('Saved255 prose/native/stored/catalogue/loader progress andterminal679 failure;11845 integrated unchanged;full goalactive.')
