"""Package the cumulative name checkpoint and immutable input audit without promotion."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.generic_speaker_labels_completion_text_v5897 import SUMMARY,NEXT
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('releases/all_routes_unified_v5891')

if __name__=='__main__':
    assert not ROOT.exists()
    vp=Path('work/analysis/editorial_handoff_verification_v5898/verified_handoff.json')
    rp=Path('work/analysis/generic_speaker_labels_release_v5895/registered_release_verification.json')
    v,r=map(read,[vp,rp]);ledger=Path('translations/editorial_review_current_v1.json')
    assert sha(ledger.read_bytes())==v['ledger_sha256'] and v['three_speaker_label_revisions_integrated']
    for key in ['candidate','patch']:assert sha(Path(r[key]).read_bytes())==r[key+'_sha256']==v[key+'_sha256']
    assert sha(Path(r['exact_patch_reconstruction']).read_bytes())==r['candidate_sha256']
    manifest=read(r['manifest']);assert len(manifest['batches'])==587 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    expected={
        'work/clean.nds':'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d',
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe',
        'out/all_routes_combined_v4701_candidate.nds':'dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e',
        'out/raphael_natural_v2_pre_lil_hodram_unified_v1_accepted_rollback.nds':'0c6e5a686b4fefb98a4d25ebb3c0e8c90ffa20e3f43240ca1629d8f6d40c85f2',
        'out/all_routes_combined_v5872_candidate.nds':'27f9d8565f2bfc1e2a97267ac06fa3940c538786da4ac843f3a63d3382a6f7bb'}
    for p,h in expected.items():assert sha(Path(p).read_bytes())==h,p
    scope=read(v['scope_inventory']['path'])
    assert scope['retrospective_name_review_current_v5897']['closed_source_context_label_leads']==[164,165,172]
    assert scope['next_Lil_B201_clean_review_pending']['reviewed_objects']==0
    text=f'''# Translation DS cumulative editorial checkpoint V5891

Experimental cumulative build for testing. Main V4701 stays promoted. The full editorial goal remains active.

- ROM: {r['candidate']}
- ROM SHA-256: {r['candidate_sha256']}
- Clean-input patch: {r['patch']}
- Patch SHA-256: {r['patch_sha256']}
- Required clean Japanese input SHA-256: {r['clean_input_sha256']}
- Registered profile: {r['profile']}
- Immutable construction baseline: {r['canonical_base']}
- Baseline SHA-256: {r['canonical_base_sha256']}
- Full manifest: {r['manifest']}
- Previous cumulative build: out/all_routes_combined_v5872_candidate.nds

The complete587 manifest batches preserve114 accepted layers and all previous experimental work. One new batch replaces Man in a Couple/Woman in a Couple/Collapsed Person with context-reviewed Man/Woman/Stranger. Only three owned primary ASCII name prefixes and their NULs change in /__arm9__.bin from V5872. All story prose,controls,other names,secondary/middle fields,pointers,code,fonts,graphics,other files/components and the123040-byte allocation remain exact. The clean-input patch reconstructs the entire approved reference byte for byte.71 semantic pre-mutation negatives,110 repository regressions and18 registered release checks pass.

Actual display evidence comprises two ordinary-input8001-frame initialized-Amsterdam B22 content fixtures,showing both complete existing tea/recovery exchanges,all28 speeches/all61 commands,25 complete nameplates and16 revised-label headers. Five full-context sheets were viewed. These do not establish natural event activation,original location,full-route completion or hardware. Catalogue UI was not visited;native getters and font bounds were tested offline. All621 original field getters and414 progressive/catalogue getters pass on both parent and target. Only three primary/six combined results change.64 substitution/literal alignment cases and three complete native font planes pass. Original full-name scratch writes are accounted for individually;all unowned4MiB remain exact.

Two fresh current New Game/town cold boots match V5872 across31 complete sampled screens/five actor controls;the six-frame review sheet was viewed. The town test uses an inherited five-ship battery,not earned progression. Source and disposable batteries remain unchanged. Representative title/New Game,Lil opening,town and changed-name displays are covered;no exhaustive natural playthrough or complete conditional-line visitation is claimed. Broader player testing remains welcome.

Coverage remains6282 completed contextual rereads/6285 source-prose/3941 revisions/2341 justified retentions. The labels add no duplicate dialogue or earlier name review credit. The207-entry retrospective name/alias review remains open;technical preservation of204 other actors does not newly approve their localizations. Approved Rafael,Hodram,Joakim,Maria and Camille remain exact.

{SUMMARY}

{NEXT}

Final label manuscript: translations/generic_speaker_labels_manuscript_v2.json

Verified handoff: {vp}

Current handoff: docs/editorial_handoff_current.md
'''
    ROOT.mkdir(parents=True);(ROOT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    evidence={str(p):sha(p.read_bytes()) for p in [vp,rp,Path('translations/generic_speaker_labels_manuscript_v2.json'),
        Path('scripts/generic_speaker_labels_completion_text_v5897.py'),Path(__file__)]}
    save(ROOT/'immutable_input_audit.json',dict(inputs=expected,all_clean_canonical_main_rollback_parent_inputs_unchanged=True,
        all_generated_ROMs_translations_history_proofs_and_failures_preserved=True,ROMs_deleted=0))
    save(ROOT/'verification.json',dict(profile=r['profile'],candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],patch=r['patch'],patch_sha256=r['patch_sha256'],
        clean_input_sha256=r['clean_input_sha256'],canonical_base=r['canonical_base'],canonical_base_sha256=r['canonical_base_sha256'],
        manifest=r['manifest'],manifest_sha256=r['manifest_sha256'],changed_internal_files=r['changed_internal_files'],
        changed_actor_primary_labels={'164':'Man','165':'Woman','172':'Stranger'},
        all587_batches114_accepted18_checks71_semantic_negatives110_regressions_pass=True,
        whole_clean_input_patch_and_approved_reference_reconstruct_exactly=True,
        completed=6282,source_prose=6285,revised=3941,retained=2341,no_duplicate_dialogue_or_name_credit=True,
        all207_name_scope_open_with_three_leads_closed_other204_not_newly_editorially_approved=True,
        actual_changed_name_headers=16,actual_complete_nameplates=25,actual_complete_existing_speeches=28,
        actual_name_scene_boots=2,actual_name_scene_frames=16002,actual_registered_startup_boots=2,actual_registered_startup_frames=21402,
        actual_catalogue_UI_not_visited_offline_native_consumers_and_font_bounds_checked=True,
        main_V4701_preserved=True,all_previous_artifacts_preserved=True,full_goal_active=True,full_goal_complete=False,evidence=evidence))
    print('Packaged V5891 cumulative ROM/clean patch/manifest/source-native-actual evidence. All protected inputs exact;full goal active.')
