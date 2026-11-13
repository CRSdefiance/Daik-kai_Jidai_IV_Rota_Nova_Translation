"""Close only the24 reviewed planning/finance records after release/actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch import planning_finance_editorial_v2 as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.planning_finance_layout_v860 import layout
from scripts.prepare_planning_finance_release_v863 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_planning_finance_gameplay_v865 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/planning_finance_editorial_final_review_v1.json')
DOC=Path('docs/planning_finance_v864_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V864 Planning and finance completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V864 Planning and finance')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==732 and ledger['records_with_source_and_prose_pass']==759
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    assert not gameplay['visual_review_pending'] and not startup['visual_review_pending']
    assert len(gameplay['actual_complete_dialogue_holds'])==8 and len(gameplay['scoped_normal_return_state_controls'])==4
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}==set(CASES.values())
    assert gameplay['actual_odd23_29_19_11_first_rows_and_complete_aligned_continuations_pass']
    assert all(c['all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal'] and c['actual_captain32_byte_object_equal'] for c in gameplay['scoped_normal_return_state_controls'])
    assert startup['all7_full_screen_pairs_exact']
    title=read(ROOT/'paired_actual_title_menu.json')
    assert title['whole256x384_title_menu_at1100_exact_to_V855'] and not title['visual_review_pending']
    release=read(RELEASE/'registered_release_verification.json')
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']
    entries=owned.current_entries(c,a)
    config=read(owned.CONFIG)
    native_proofs={k:read(v) for k,v in config['native_cache_proofs'].items()}
    assert sum(p['complete_native_copies'] for p in native_proofs.values())==14886
    assert sum(len(p['sequenced_cache_cases']) for p in native_proofs.values())==534
    fonts=read(doc['native_font_proof']);native={r['message_id']:r for r in fonts['cases']}
    manifest,registry=read(ROM.with_suffix('.manifest.json')),read('translations/release_stack.json')
    assert len(manifest['batches'])==471 and len(registry['accepted_layers'])==114
    assert manifest['profile']=='all-routes-unified-v863' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'all24_complete_fonts_50_source_selections_and_native_consumer_audit_pass':True,
        '14886_complete_native_copies_and534_sequence_cases_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_pass':True,
        'paired_actual_title_menu_after_START_exact':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_metadata_and8_cache_code_bytes_change_in_ARM9':True,
        'single8192_input_reuses_two4096_allocation_no_memory_growth':True,
        'single_cache_may_increase_file_reads':True,'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(owned.IDS)
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
    assert sum(r['editorial_decision']=='revise' for r in records)==17
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Planning19-Finance20-comments1447-1470','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=756,records_revised_and_integrated=550,retained_wordings_editorially_completed=206)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=755
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These three reviewed drafts are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V855']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v863',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-planning-finance24-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_planning_finance_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.planning_finance_editorial_v2.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['planning_finance_v864']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 role19/20 bodies. All other shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['planning_finance_actual_phase_v864']={'status':'complete-for24-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All24 full fonts;actual odd23/29/19/11 first rows,complete aligned continuations,35-character monthly profit continuation and four returns. No game-wide guarantee.'}
    user=Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    for row in read(user)['candidates'][-1]['entries']:assert entries[row['id']].text.hex()==row['template_hex']
    user_proof=ROOT/'user676_677_current_preservation.json'
    save(user_proof,{'candidate_sha256':candidate['sha256'],'reference_proof':str(user),'reference_sha256':sha(user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'native_dialogue_renderer_code_unchanged_from_V855':True,
        'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user_proof),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V864 completes24 Planning19/Finance20 comments1447-1470 in registered V863:17 revisions and7 retentions. '
        'Fifty original role selections,all24 full native glyph planes and the source-consumer audit pass. '
        'The original4KiB packing limit is resolved by replacing only8 private cache-helper bytes:one8KiB input occupies the same former two4KiB allocation,with512-byte output,sections/BSS,216x36 crop and123040-byte staged payload unchanged. '
        'All7336 code-only and7336 target native copies,214 exact8KiB boundary copies and534 cache-sequence cases pass;old two-slot overflow is reproduced. '
        'Eight actual full bitmap/RGB holds sample the planning/sleep joke,direct tactics plus schemes,selling goods and monthly profit;four normal returns preserve scoped state. Seven ordinary startup/New Game frames match V855. '
        'The exact clean-input patch preserves471 batches,114 layers,3644 unselected COMMON strings and all prior routes/art. '
        '756 entries complete (550 revised/206 retained),759 source/prose reviewed. Older750-752 and all unreviewed shared/routes/player prose/raw coverage remain. '
        'Separate graphics/all18 plaques,Samwell name lead and later older-record re-audit stay open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V864-Planning-Finance24-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:specific shop676/677 preservation freshly verified and earlier actual capture read',
        'this_goal_turn_classification':'progress:capacity and source/native verification,registered build/exact patch,actual samples and24 completed entries',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==756
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==759
    assert ledger['unresolved_graphics_work']==prior['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==prior['older_record_reaudit_after_full_editorial_goal'] and not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V864: planning and finance editorial completion in V863\n\n'+checkpoint+'\n\n'
        '## English and source\n\nThe Japanese planning/sleeping homophone is adapted with dream up a plan versus dreaming. '
        'Other revisions restore more study,direct methods alone being insufficient,each port,current tentative profitability,selling goods and this month. '
        'Retain1449,1452,1454,1457,1458,1462,1464. Market prices,clear picture,dream up and best shot stay together through a successor formatter;no authored alignment spaces or manual wrapping.\n\n'
        '## Storage and native verification\n\nThe old41-block4KiB next-fit packer cannot hold the full reviewed prose. '
        'Research preserves all previous strings instead of shortening prose or stripping unreviewed padding. Block18 grows from4084 to4464 bytes. '
        'A source/call-census-guarded8-byte helper returns input slot0,using the original8192-byte input allocation. All other ARM9 bytes outside declared directory/offset metadata remain exact. '
        'The generic native file reader and full copy routines remain original. Single-entry caching may increase file reads;the targeted actual runs and startup controls pass. '
        'Native tests bridge successful host open/read calls;they do not prove physical I/O or hardware behavior. The old loader rejects the larger block in a reproduced slot1 overflow case.\n\n'
        '## Actual scope\n\n'+gameplay['scope']+'\n\n'
        f'## Release\n\n- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n- Canonical base SHA-256: `{manifest["base_sha256"]}`\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256: `{candidate["patch_sha256"]}`\n'
        f'- Clean input SHA-256: `{release["clean_input_sha256"]}`\n- Final review: `{REVIEW}`\n- Closure: `{closure}`\n\n'
        'Only COMMON and ARM9 differ from V855. All prior release components,fonts,graphics and routes remain exact. '
        'Human cold-boot acceptance is still required before canonical promotion. Repaired shop676/677 bytes remain exact;no fresh activation of those shops is claimed. '
        'The complete editorial goal and separate graphics audit remain unfinished.\n',encoding='utf-8')
    for path in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## V864: planning and finance editorial completion\n\n'+checkpoint+' See [V864 evidence](planning_finance_v864_completion.md).\n')
    GUIDE.mkdir(parents=True);guides=[]
    for label,number in CASES.items():
        source=CAP/f'planning_finance_v864_863_{label}/frame_004200_navigation.png';target=GUIDE/f'{label}_ID{number}_V863.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual cold-boot framebuffer with disclosed2/3-byte isolated room assignment;not earned refit/recruitment.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'guide_candidates':guides,'not_unqualified_ordinary_progression_screenshots':True})
    sources={p for prefix,versions in (('planning_finance',(857,858,859,860,863,864)),('common_single_cache',(861,862)))
        for v in versions for p in Path(f'work/analysis/{prefix}_v{v}').rglob('*') if p.is_file() and p.suffix not in ('.nds','.dsv')}
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,'translations/release_stack.json',
        'translations/rom_retention_pins.json','scripts/record_planning_finance_completion_v864.py','scripts/build_integrated_release.py',
        'scripts/prepare_planning_finance_release_v863.py','scripts/verify_planning_finance_release_v863.py',
        'scripts/native_planning_finance_fixture_v864.py','scripts/run_planning_finance_adapter_v864.py','scripts/run_planning_finance_v864.py',
        'scripts/verify_planning_finance_gameplay_v864.py','scripts/verify_planning_finance_gameplay_v865.py',
        'scripts/check_planning_finance_title_v864.py','scripts/run_planning_finance_startup_v863.py','scripts/verify_planning_finance_startup_v863.py',
        'docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    sources.update(map(Path,config['dependencies']));sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for folder in [f'planning_finance_v864_863_{label}' for label in CASES]+['planning_finance_v863_newgame','planning_finance_v864_title_855','planning_finance_v864_title_863']:
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name
            if not source.exists():continue
            target=ARCHIVE/'captures'/folder/name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes())
            archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'all_ROMs_captures_and_generated_artifacts_on_E':True,'full_goal_complete':False})
    print('Planning/Finance24 complete:756 total,550 revised,206 retained;759 source/prose. Full goal and graphics remain open.',flush=True)


if __name__=='__main__':main()
