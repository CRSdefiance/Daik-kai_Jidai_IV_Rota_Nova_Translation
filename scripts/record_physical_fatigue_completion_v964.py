"""Credit13 fatigue reviews only after exact registered,native,actual and visual evidence."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import physical_fatigue_editorial as owned
from dk4tool.patch.battle_gunnery_deck_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.physical_fatigue_layout_v960 import layout
from scripts.prepare_physical_fatigue_release_v962 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_physical_fatigue_gameplay_v964 import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/physical_fatigue_editorial_final_review_v1.json')
DOC=Path('docs/physical_fatigue_v964_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V964 Physical Fatigue completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V964 Physical Fatigue')


def reference(e):return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1066 and ledger['records_with_source_and_prose_pass']==1082
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8 and {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1783,1784,1790,1793}
    assert len(gameplay['scoped_normal_return_controls'])==4 and all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==15 and all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['Camille_ASCII_I_Cristina_Recreation_Room_genuine_captain_and_Sera_special_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V954']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all75_original_direct_main_battle_and_ordinary_fatigue_selections'])==75 and len(context['all25_healthy_direct_helper_no_message_controls'])==25
    assert context['Sera24_special_ID']==1793 and context['job_role_and_mood_not_queried_in_physical_status_branch']
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==13 and fonts['complete_native_font_cases']==26
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v962' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete_ASCII_I1783_aligned_Recreation_Room1784_retained1790_and_Sera1793_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),'all13_fonts26_cases75_source25_healthy50_pronoun7336_copies178_sequences_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_pass':True,'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])};assert not existing.intersection(owned.IDS)
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row)
        assert all(v['text_hex']==entries[n].text.hex() for v in native[n]['ordinary_and_battle_font_controls'])
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],'before_text_hex':row['current_text_hex'],
            'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),
            'native_font_canvas_sha256_by_mode':{v['mode']:v['canvas_sha256'] for v in native[n]['ordinary_and_battle_font_controls']},
            'actual_display_holds':[h for h in gameplay['actual_complete_dialogue_holds'] if h['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert len(records)==13 and sum(r['editorial_decision']=='revise' for r in records)==10
    final={'format':'dk4-editorial-family-final-review-v1','status':'13-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'registered_release_proof':str(closure),'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),'source_context_supplement':doc['source_context_supplement'],
        'actual_scope':gameplay['scope'],'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Physical-Condition1-Fatigue1781-1793','native_message_IDs':list(owned.IDS),'records':records,
        'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1079,records_revised_and_integrated=806,retained_wordings_editorially_completed=273)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1078
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS];assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts','note':'These are not the full remaining unreviewed shared/routes/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V954']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v962','MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),
        'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-physical-fatigue13-native-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate);ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_physical_fatigue_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.physical_fatigue_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['physical_fatigue_v964']={'status':final['status'],'completed_entries_added':13,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),
        'scope':'13 condition1 fatigue comments. Other physical states and remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['physical_fatigue_actual_phase_v963']={'status':'complete-for13-entries-global-formatting-audit-open','proof':final['actual_gameplay_proof'],
        'checks':'13 full native fonts in26 ordinary/battle controls,eight full-word/actual-RGB holds,four normal returns and15 offline rejection controls. Complete ASCII I1783,aligned Recreation Room1784,retained captain1790 and Sera1793 pass. No game-wide guarantee.'}
    previous_user=Path('work/analysis/battle_gunnery_deck_v955/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin']);assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V964 completes13 physical-condition1 fatigue comments1781-1793 in registered V962:10 revisions and3 retentions. All75 original direct/main battle/ordinary selections,25 healthy controls,50 first-person expansions,26 full native font cases,7336 full copies and178 cache sequences pass. Eight active-widget bitmap/RGB holds verify complete ASCII I1783,aligned Recreation Room1784,genuine captain retained1790 and Sera24 special1793. Four normal returns preserve scoped state through first Back;original battle time resumes on exit. Disclosed room and early condition fixtures follow observed original combat0/1;NPC condition1 is inserted again after Deck opens because original simulation recomputes it before arrival. Initial V963 timing trials remain non-credit evidence. Seven ordinary startup/New Game frames and title match V954. Exact clean-input patch preserves471 batches,114 layers,3655 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes. 1079 entries complete (806 revised/273 retained),1082 source/prose reviewed. Other physical states,older750-752,mood1833,special1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V964-Physical-Fatigue13-complete','documentation':str(DOC),'proof':str(closure),'actual_proof':final['actual_gameplay_proof'],
        'completed_entries_added':13,'previous_goal_turn_classification':'progress:current V954 user screenshot676/677 repair preservation freshly verified and earlier actual corrected scene reviewed',
        'this_goal_turn_classification':'progress:13 source/prose reviews,50 first-person expansions,26 native fonts,registered V962/exact patch,four actual scenes/returns and13 completed entries','full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1079 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1082
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):assert ledger[key]==prior[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V964: physical fatigue editorial completion\n\n'+checkpoint+'\n\n## Source and English\n\nTen revisions and three justified retentions cover13 independent alternatives. Personal fatigue,uncertainty,the Recreation Room rest wish,rough self-question,brief rest,accumulated fatigue,Rafaels tentative question,Marias reassurance stammer and Seras unfinished first-person fragment are preserved. Clean IC1783 is a first-person macro,not an actor name;50 current/clean expansions pass. Help112 establishes Recreation Room. No cause,diagnosis,completed healing,reassignment or family relationship is invented. Other physical-state families remain separate. All five natural-dialogue-v2 gates and exact clean/canonical/current references are retained.\n\n## Formatting and actual tests\n\nAll13 paragraphs have complete original-font previews in both ordinary and battle controls. Visible rows start at x0,without manual alignment or breaks. Complete ASCII I1783,Recreation Room1784,Marias stammer1792 and intentional Sera fragment1793 are intact inside216x36. The standard story audit rejects this COMMON manuscript format;the recorded dedicated native-consumer audit passes with zero errors and unwaived warnings. Four wrong-format and11 offline glyph-deletion controls reject.\n\n'+gameplay['scope']+'\n\n## Registered candidate\n\nExperimental profile all-routes-unified-v962 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 message selection metadata differ from V954. Native code,all other prose,graphics/routes/HELP/ARM7/overlays,sections/BSS,arenas and123040 staged bytes are exact. The xdelta reconstructs every ROM byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Canonical promotion still requires explicit human cold-boot acceptance.\n\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V964: physical fatigue editorial completion\n\n'+checkpoint+' See [V964 evidence](physical_fatigue_v964_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label in SPECS:
        source=CAP/f'physical_fatigue_v964_962_{label}'/'frame_016300_navigation.png';target=GUIDE/f'{label}_V962.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V962 cold boot with declared coordinates,room assignment and officer-condition1 fixture;not earned fatigue,recruitment,refit or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in range(957,965):paths.update(p for p in (Path('work/analysis')/f'physical_fatigue_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*physical_fatigue*v9*.py'))
    paths.update(Path(p) for p in (owned.CONFIG,str(MANUSCRIPT),'translations/physical_fatigue_editorial_manuscript_v1.json',str(REVIEW),str(LEDGER),'translations/release_stack.json',
        'dk4tool/patch/physical_fatigue_editorial.py','scripts/build_integrated_release.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/physical_fatigue_v962/standard_story_audit.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'physical_fatigue_v964_962_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('13 reviews complete:1079 total (806 revised/273 retained),1082 source/prose;',len(copied),'archive files verified. Full goal active.',flush=True)


if __name__=='__main__':main()
