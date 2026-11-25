"""Close tutorial research gates from exact saved evidence; grant no release credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.rafael_early_tutorial_rebuild_v1 import rebuild_block
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_editorial_progress_checkpoint_v1 import checkpoint

ROOT = Path('work/analysis/Rafael_early_tutorial_B42_B43_checked_20261104')
FORMAT = Path('work/analysis/Rafael_early_tutorial_B42_B43_formatting_20261104')
DOC = FORMAT / 'formatting_input.json'
PLAN = FORMAT / 'speech_display_approved_v2/all40_compiled_plans.json'
NATIVE = FORMAT / 'speech_display_approved_v2/all40_native_pages.json'
VISUAL = FORMAT / 'speech_display_approved_v2/visual_approval.json'
REBUILT = Path('work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/reconstruction_v2/reconstruction.json')
STORED = Path('work/analysis/Rafael_early_tutorial_B42_B43_storage_20261104/stored_native_v1/stored_native_verification.json')
LOADERS = Path('work/analysis/Rafael_early_tutorial_B42_B43_loaders_20261104/verification.json')
NAMES = Path('work/analysis/Rafael_early_tutorial_B42_B43_current_name_planes_20261104/native_name_planes.json')
PIXELS = Path('work/analysis/Rafael_early_tutorial_B42_B43_actual_pixels_20261104/focused_actual_pixels.json')
FINAL = Path('translations/rafael_B42_B43_contextual_final_review_v1.json')
NAME_FINAL = Path('translations/rafael_B42_B43_scoped_names_final_v1.json')

if __name__ == '__main__':
    assert not ROOT.exists() and not FINAL.exists() and not NAME_FINAL.exists()
    doc, plan, native, visual, rebuilt, stored, loaders, names, pixels = map(load, [DOC, PLAN, NATIVE, VISUAL, REBUILT, STORED, LOADERS, NAMES, PIXELS])
    assert len(doc['records']) == 40 and (doc['proposed_revisions'],doc['wording_retentions']) == (19,21)
    assert native['all42_final_pages_directly_viewed'] and not native['direct_visual_review_pending']
    assert visual['pages'] == stored['complete_stored_pages'] == 42 and not visual['QA_waivers']
    assert stored['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert stored['fresh_relocated_native_relative_cases'] == rebuilt['relative_sites'] == 0
    assert (loaders['fresh_whole_archive_loads_andcache_hits'],loaders['fresh_parent_cases'],loaders['exact_reused_parent_cases']) == (343,4,682)
    assert native['runtime'] == stored['runtime'] == names['runtime']
    assert pixels['actual_frames'] == 25002 and len(pixels['runs']) == 2
    assert len(pixels['body_pages']) == 92 and len(pixels['observed_record_pages']) == 42 and len(pixels['name_headers']) == 5
    assert pixels['all_required_distinct_display_cases_match'] and len(pixels['review_sheets']) == 2
    for sheet in pixels['review_sheets'] + names['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    plans = {r['id']:r for r in plan['records']}
    source = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file(doc['file_path'])).blocks
    image = NdsImage.open(doc['current_ROM'])
    current = IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    inventory,_,_ = scoped_inventory()
    # The source/end-padding correction is now frozen. Bind the current producer
    # with an exact replay against the existing blocks, without generating a ROM.
    for group in rebuilt['groups']:
        number = group['block']
        target, proof = rebuild_block(image.read_file('/__arm9__.bin'),source[number],current[number],
            [r for r in doc['records'] if r['block']==number],plans,inventory)
        assert target == Path(group['target_block']).read_bytes() and sha(target) == group['target_sha256']
        assert all(value == group[key] for key,value in proof.items())
    ROOT.mkdir()
    save(ROOT/'current_rebuilder_exact_replay.json',dict(reconstruction=str(REBUILT),reconstruction_sha256=sha(REBUILT.read_bytes()),
        complete_source_current_block_inverses_andall47_commands_exact=True,relative_sites=0,new_ROM_generated=False,
        current_rebuilder='dk4tool/script/rafael_early_tutorial_rebuild_v1.py',
        current_rebuilder_sha256=sha(Path('dk4tool/script/rafael_early_tutorial_rebuild_v1.py').read_bytes()),new_credit=0))
    actual = dict(total_frames=25002,runs=pixels['runs'],all_review_sheets_directly_viewed=pixels['review_sheets'],
        all_target_sampled_paragraphs_andnormal_F_headers_complete=True,all42_target_pages_observed_in_order=True,
        observed_name_actor_IDs=[0,4,5,6],complete_body_planes=92,complete_name_headers=5,
        both_corrected_two_page_utterances_observed=True,source00_FI_FE_andfollowing_port_transitions_observed=True,
        no_natural_activation_original_location_earned_chronology_fullroute_orhardware_claim=True,
        following_resupply_sailing_text_outside_this_batch=True,read_only_pixel_proof=str(PIXELS),read_only_pixel_proof_sha256=sha(PIXELS.read_bytes()),
        actual_gameplay=True,disclosed_initialized_fixtures=True,guide_photos=False,new_credit=0)
    actual_path = ROOT/'actual_visual_approval.json'
    save(actual_path,actual)
    save(ROOT/'scoped_name_visual_approval.json',dict(native=str(NAMES),native_sha256=sha(NAMES.read_bytes()),
        four_complete_name_planes_directly_viewed=True,all_eight_current_Rafael_getters_pass=True,
        complete_actual_headers=pixels['name_headers'],full_catalogue_UI_unvisited=True,no_name_data_change=True,new_credit=0))
    old_names_path=Path(names['clean_name_binding'])
    old_names=load(old_names_path)
    reasons={0:'Retain the approved Rafael spelling and established Castor surname; the source identifies the same protagonist.',
        4:'Retain the established Janus Pasar name used throughout the opening; both source consumers identify the same recurring companion. No new title or relationship is implied.',
        5:'Retain Claudio Manaus, a natural established rendering of the source name. The familiar Clau in Janus\'s banter remains a nickname rather than a new identity.',
        6:'Retain Julio Erneco, including Spanish Julio for source フリオ. The name adds no kinship or rank; familiar old-man banter is reviewed separately in context.'}
    name_rows=[]
    for actor,reason in reasons.items():
        clean_rows=[r for r in old_names['clean_names']['rows'] if r['actor_ID']==actor]
        current_rows=[r for r in names['consumer_bindings'] if r['actor_ID']==actor]
        assert len(clean_rows)==len(current_rows)==2 and len({r['text'] for r in current_rows})==1
        text=current_rows[0]['text']
        name_rows.append(dict(id=f'RAFAEL_EARLY_TUTORIAL_ACTOR_{actor}',actor_ID=actor,english=text,speaker=text,
            source_meaning=clean_rows[0]['text'],context='Recurring companion identity in both complete Rafael B42/B43 tutorial exchanges.',
            localization_note=reason,decision='retention',retention_reason=reason,
            source_reference=dict(native_binding=str(old_names_path),native_binding_sha256=sha(old_names_path.read_bytes()),actor_ID=actor,consumers=clean_rows),
            current_reference=dict(native_binding=str(NAMES),native_binding_sha256=sha(NAMES.read_bytes()),actor_ID=actor,consumers=current_rows),
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True)))
    names_final=dict(format='dk4-scoped-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        review_gates=doc['review_gates'],records=name_rows,no_name_data_change=True,no_new_dialogue_credit=True,
        formatting_evidence=str(ROOT/'scoped_name_visual_approval.json'),global_207_name_review_still_open=True)
    validate_natural_dialogue_batch(names_final)
    save(NAME_FINAL,names_final)
    final=deepcopy(doc)
    stored_by={r['id']:r for r in stored['records']}
    for row in final['records']:
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        entry=stored_by[row['id']]
        row['review']['formatting']=True
        row['planned_English_markup']=plans[row['id']]['English']
        row['planned_integrated_reference']=dict(file_path=doc['file_path'],block=row['block'],offset=entry['new_offset'],
            header_offset=entry['new_offset']-5,record_index=entry['new_record_index'],exact_stored_hex=entry['stored_hex'],
            target_archive_sha256=rebuilt['target_archive_sha256'])
        for key in ['source_preamble_andname_consumer_approval_not_inferred','source_context_localization_formatting_gates_pending',
            'native_identity_terms_localization_andformatting_pending','fresh_formatting_native_visual_stored_andrepresentative_gameplay_pending']:
            row[key]=False
        row.update(registered_release_andcompletion_credit_pending=True,formatting_evidence=dict(native=str(NATIVE),stored=str(STORED),visual=str(VISUAL),actual=str(actual_path),
            scope='Complete native/offline pages and representative initialized gameplay; natural tutorial activation remains unvisited.'))
    final.update(format='dk4-editorial-final-review-v1',encoder='dialogue-relocatable-v1',all_five_individual_review_gates_passed=True,
        all_formatting_gates_false=False,source00_complete_preamble_andRafael_macro_fresh_display_binding_pending=False,
        source_preamble_andnames_approved_for_this_scope=True,scoped_name_review=str(NAME_FINAL),scoped_name_review_sha256=sha(NAME_FINAL.read_bytes()),
        registered_release_andcompletion_credit_pending=True,new_credit=0,
        formatting_evidence={str(p):sha(p.read_bytes()) for p in [PLAN,NATIVE,VISUAL,REBUILT,STORED,LOADERS,NAMES,PIXELS,actual_path,NAME_FINAL,ROOT/'current_rebuilder_exact_replay.json',Path(__file__)]})
    validate_natural_dialogue_batch(final)
    save(FINAL,final)
    save(ROOT/'release_plans.json',plan)
    proof_path=ROOT/'formatting_checkpoint.json'
    save(proof_path,dict(final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),scoped_names=str(NAME_FINAL),scoped_names_sha256=sha(NAME_FINAL.read_bytes()),
        prose_reviews=40,revised=19,retained=21,final_pages=42,layout_corrections=2,new_glyph_fixes=0,existing_Julio_ASCII_fix_preserved=True,
        whole_archive_loads=343,fresh_parent_modes=4,exact_reused_parent_modes=682,actual_runs=2,actual_frames=25002,
        actual_body_planes=92,observed_record_pages=42,actual_headers=5,actual_sheets=2,
        all_individual_five_gates_pass_in_research=True,registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False))
    summary=('Rafael early-game priority: B42/B43 now has 40 five-gate research reviews (19 revisions, 21 retentions), '
        '42 visually checked/stored pages and two page-boundary fixes. Both initialized coldboots pass: 25002 frames, '
        'all 42 ordered pages, 92 complete body planes and five headers. Four names/eight current getters and SC0 loaders pass. '
        'Production registration, rejection checks and cumulative integration remain. 10306 integrated completions; experimental 88e9984f and main unchanged. '
        'Earlier credit, later drafts, full scope, all ROMs/evidence preserved; no live jobs or guide photos.')
    document=Path('docs/editorial_rafael_early_tutorial_checked_20261104.md')
    text='''# Rafael early tutorials: checked research batch

Rafael's early game and all tutorials have priority. SC0 B42 (resupply and first-voyage planning) and B43 (crew duties) now have 40 complete contextual reviews: 19 revisions and 21 individually justified retentions. All five gates pass in research. No integration credit has been added.

The [final manuscript](../translations/rafael_B42_B43_contextual_final_review_v1.json) retains exact clean/current references, source meanings and individual decisions, and adds exact proposed stored references. Four source-bound speaker names are retained with individual reasons in [the scoped name review](../translations/rafael_B42_B43_scoped_names_final_v1.json). Approved Rafael and established Janus, Claudio and Julio identities are preserved.

All 42 final pages passed native glyph, bounds, macro, guard, row and pagination checks and direct visual review. Two page findings were fixed without shortening prose: B42 R19's complete closing sentence now starts page two; B43 R30 keeps the complete second First Mate benefit on page two. The captain clause and Rafael name fit the opening line. First uses the existing registered ASCII correction; this is preservation, not a new glyph-fix credit. The Deck View instruction uses three readable FE rows. Reuse unchanged proofs for 38 records; only the two changed layouts were rerendered.

Current context is the registered candidate's own ordinary Rafael captain0/route0 startup. All 40 source/current six-byte preambles, including five selector00 records and the separate FE path, are bound. Native FI/FA/FO defaults remain Rafael/Castor/Castor Co. Four complete name planes and eight fresh current getters pass. Their contact sheet was directly viewed; catalogue UI layout is unvisited.

Research reconstruction changes only SC0 B42/B43. All 47 commands, source/current/serialized inverses and all unowned files/components pass. B43 already contained the registered sparse Julio relocation; clean and current offsets are mapped separately. The frozen successor was replayed against every tested block without generating another ROM. Both failed partial reconstruction attempts and all successful outputs remain. There are zero relative branch sites; no branch-execution credit is invented. Stored verification covers 42 pages, with 22 fresh parity-dependent pages and 20 exact compiled-page reuses. SC0 has 343 native load/cache checks, four fresh changed-block parent modes and 682 exact unchanged reused modes, with current native instruction dependencies checked.

Two initialized English coldboots (25002 frames) preserve the entire original tutorial command sequences behind the original Rafael opening initializer. Their 29/13 ordered speech-page calls match the copied source sequence. All 42 target pages have complete framebuffer matches: 92 body-plane samples and five full speaker headers. Both corrected two-page transitions, normal F, actual FI/Rafael, source00 speakers, the FE instruction and following port/resupply transition are observed. Two focused gameplay sheets were directly viewed. These are disclosed entry fixtures; natural event activation, original scene location, earned progression, custom player names, full route and hardware remain unvisited. Following resupply/sailing dialogue is outside this batch and receives no extra credit.

Evidence: `work/analysis/Rafael_early_tutorial_B42_B43_checked_20261104/formatting_checkpoint.json`; final page/native/visual proofs under `...B42_B43_formatting_20261104/speech_display_approved_v2/`; stored reconstruction under `...B42_B43_storage_20261104/`; gameplay under `...B42_B43_actual_pixels_20261104/`. Refer to these receipts rather than repeating completed checks.

Next: create the source-locked SC0 production adapter and focused rejection tests, register a cumulative successor of experimental 88e9984f while preserving all 114 accepted layers and six runtime/name/static stages, then verify the manifest, exact clean-input patch and its own startup. Do not hand off research fixtures or promote main. Completion remains 10306 until once-only integrated credit is earned.

After integration, prioritize remaining shared beginner help/tutorial/menu prose and Rafael story progression. The First Mate/adjutant deck-tooltip mismatch is queued. Preserve the already completed B44 opening (117), B45 trade (12), B46 sea actions (26) and B47–B50 credit; revisit only concrete unfinished prose or wrap/glyph/label findings. Later Hodram B211–B230 work remains saved (277 meanings, 114 drafts). Every other storyline, earlier translation, town/shop/random scene and player-facing text stays in scope. Graphics artwork and the later older-record technical re-audit remain separate. No guide-photo collection, pruning, commit/push or main promotion.
'''
    protected={doc['current_ROM']:doc['current_ROM_sha256'],'translations/release_stack.json':sha(Path('translations/release_stack.json').read_bytes()),
        'out/raphael_natural_v2_accepted_base.nds':'3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'}
    checkpoint(mutation=ROOT/'progress_mutation_v1',batch_key='Rafael_SC0_B42_B43_early_tutorial_20261104',
        batch_updates=dict(new_credit=0,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
            checkpoint=str(proof_path),checkpoint_sha256=sha(proof_path.read_bytes()),all_fifth_formatting_gates_pending=False,
            all_five_individual_gates_pass_in_research=True,final_pages=42,layout_corrections=2,scoped_name_retentions=4,
            actual_runs=2,actual_frames=25002,actual_body_planes=92,actual_headers=5,actual_observed_pages=42,
            remaining=['Source-locked production adapter and rejection checks','Registered cumulative integration/clean patch/own startup'],
            full_goal_complete=False),summary=summary,document=document,document_text=text,completed=10306,protected=protected)
    print('40 five-gate tutorial research reviews saved; 10306 integrated completions preserved; registered integration next.')
