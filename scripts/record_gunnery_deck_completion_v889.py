"""Finish only24 gunnery/deck records after independent release and actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import gunnery_deck_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.gunnery_deck_layout_v887 import layout
from scripts.prepare_gunnery_deck_release_v888 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_gunnery_deck_gameplay_v889 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/gunnery_deck_editorial_final_review_v1.json')
DOC=Path('docs/gunnery_deck_v889_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V889 Gunnery and deck cleaning completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V889 Gunnery and deck cleaning')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==832 and ledger['records_with_source_and_prose_pass']==859
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert not any(p['visual_review_pending'] for p in (gameplay,startup,title))
    assert len(gameplay['actual_complete_dialogue_holds'])==8 and {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}==set(CASES.values())
    assert len(gameplay['scoped_normal_return_state_controls'])==4
    assert all(c['all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal'] and c['actual_captain32_byte_object_equal'] for c in gameplay['scoped_normal_return_state_controls'])
    assert gameplay['actual_ASCII_I1561_empty_stomach35_and_odd23_mentor_training_continuation_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V882']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all50_original_role_helper_selections'])==50
    terms=read(doc['native_pronoun_proof']);assert terms['source1561_IC_plus_plural_ra_means_our_ship']
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==24
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v888' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'all24_complete_fonts_50_source_selections_7336_copies_178_sequences_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_and_paired_title_menu_pass':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])};assert not existing.intersection(owned.IDS)
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row) and native[n]['text_hex']==entries[n].text.hex()
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],
            'before_text_hex':row['current_text_hex'],'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),'native_font_canvas_sha256':native[n]['canvas_sha256'],
            'actual_display_holds':[h for h in gameplay['actual_complete_dialogue_holds'] if h['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,
            'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert sum(r['editorial_decision']=='revise' for r in records)==15 and len(records)==24
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'native_pronoun_proof':doc['native_pronoun_proof'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Gunnery8-DeckCleaning2-comments1547-1570','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=856,records_revised_and_integrated=633,retained_wordings_editorially_completed=223)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=855
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These three reviewed drafts are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V882']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v888',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-gunnery-deck24-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_gunnery_deck_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.gunnery_deck_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['gunnery_deck_v889']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 Gunnery/Deck Cleaning comments. Other shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['gunnery_deck_actual_phase_v889']={'status':'complete-for24-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All24 complete fonts;actual ASCII initial I1561,full35-character empty-stomach1553 and complete training continuation after odd23-character1568 first row,four normal returns. No game-wide guarantee.'}
    user=Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    for row in read(user)['candidates'][-1]['entries']:assert entries[row['id']].text.hex()==row['template_hex']
    user_proof=ROOT/'user676_677_current_preservation.json'
    save(user_proof,{'candidate_sha256':candidate['sha256'],'reference_proof':str(user),'reference_sha256':sha(user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'native_dialogue_renderer_code_unchanged_from_V882':True,
        'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user_proof),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V889 completes24 Gunnery8/DeckCleaning2 comments1547-1570 in registered V888:15 revisions and9 retentions. All50 original role selections,50 current/clean IC pronoun expansions,native Emilio spelling,all24 complete fonts,7336 full native copies and178 cache sequences pass. Eight actual bitmap/RGB holds verify polite test-firing deferral,full35-character empty-stomach joke,complete ASCII initial I in our ship,and full training-under-mentor continuation after23-character first row. Four normal returns preserve scoped state. Seven startup/New Game frames and the title menu match V882. Exact clean-input patch preserves471 batches,114 layers,3644 unselected strings,all graphics/routes,native code,existing single8KiB cache,216x36 crop and123040 staged bytes. 856 entries complete (633 revised/223 retained),859 source/prose reviewed. Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain. Separate graphics/all18 plaques,Samwell name lead and later older-record re-audit stay open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V889-Gunnery-Deck24-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:Sails/Boarding24 completed inV882,next24 native contexts proved',
        'this_goal_turn_classification':'progress:24 source reviews,phrase-aware native audit,registered release/exact patch,actual samples and24 completed entries','full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==856 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==859
    assert ledger['unresolved_graphics_work']==prior['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==prior['older_record_reaudit_after_full_editorial_goal'] and not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V889: gunnery and deck cleaning editorial completion in V888\n\n'+checkpoint+'\n\n'
        '## Source and English\n\nFifteen revisions restore personal/polite gunnery speech,nervous anticipation,the empty-stomach sound joke,training readiness,the ships home/value comparison,offers to clean,occasional outdoor cleaning,and nostalgia for training under a mentor. Nine natural wordings are retained:1551,1552,1554,1556,1557,1565,1567,1569,1570. The mentor is left unnamed and no family relationship is invented. Current native actor14 is Emilio. SourceIC plus plural ra in1561 means our ship;50 current/clean native expansion cases prove this. Existing fluent wording is preserved there while the obsolete full-width I guard becomes ordinary ASCII with complete native and actual-display verification.\n\n'
        '## Layout and actual scope\n\nEvery252x96 native font plane matches independently placed complete words;all body ink fits216x36. Phrase hints preserve empty stomach,our ship,the home comparison,now and then,and training under my mentor. No prose shortening,manual breaks or authored alignment spaces. The standard story audit rejects this COMMON source-manuscript format;its failure log remains. The dedicated native-consumer audit has zero blocking errors and unwaived warnings.\n\n'+gameplay['scope']+'\n\n'
        '## Release\n\n'
        f'- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `{manifest["base_sha256"]}`\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256 `{candidate["patch_sha256"]}`\n- Clean input SHA-256: `{release["clean_input_sha256"]}`\n'
        f'- Final review: `{REVIEW}`\n- Closure: `{closure}`\n\n'
        'Only COMMON and ARM9 selection metadata differ from V882. Native code,existing cache policy and allocations,216x36 crop,sections/BSS,123040 staged bytes and all prior routes/art remain exact. Human cold-boot acceptance remains necessary before canonical promotion. Repaired shop676/677 bytes stay exact;no fresh shop activation is claimed. The full editorial goal and separate graphics audit remain unfinished.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V889: gunnery and deck cleaning editorial completion\n\n'+checkpoint+' See [V889 evidence](gunnery_deck_v889_completion.md).\n')
    GUIDE.mkdir(parents=True);guides=[]
    for label,number in CASES.items():
        source=CAP/f'gunnery_deck_v889_888_{label}/frame_004200_navigation.png';target=GUIDE/f'{label}_ID{number}_V888.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual cold-boot framebuffer with disclosed2/3-byte isolated room assignment;not earned refit/recruitment.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'guide_candidates':guides,'not_unqualified_ordinary_progression_screenshots':True})
    sources={p for v in range(884,890) for p in Path(f'work/analysis/gunnery_deck_v{v}').rglob('*') if p.is_file() and p.suffix not in ('.nds','.dsv')}
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,'translations/release_stack.json','translations/rom_retention_pins.json',
        'scripts/record_gunnery_deck_completion_v889.py','scripts/build_integrated_release.py','scripts/prepare_gunnery_deck_release_v888.py','scripts/verify_gunnery_deck_release_v888.py',
        'scripts/native_gunnery_deck_fixture_v889.py','scripts/run_gunnery_deck_adapter_v889.py','scripts/run_gunnery_deck_v889.py','scripts/verify_gunnery_deck_gameplay_v889.py',
        'scripts/check_gunnery_deck_title_v889.py','scripts/run_gunnery_deck_startup_v888.py','scripts/verify_gunnery_deck_startup_v888.py',
        'docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    sources.update(map(Path,config['dependencies']));sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for folder in [f'gunnery_deck_v889_888_{label}' for label in CASES]+['gunnery_deck_v888_newgame','sails_boarding_v883_title_882','gunnery_deck_v889_title_888']:
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name
            if not source.exists():continue
            target=ARCHIVE/'captures'/folder/name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes());archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'all_ROMs_captures_and_generated_artifacts_on_E':True,'full_goal_complete':False})
    print('Gunnery/Deck24 complete:856 total,633 revised,223 retained;859 source/prose. Full editorial/graphics goals remain unfinished.',flush=True)


if __name__=='__main__':main()
