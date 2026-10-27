"""Credit26 reviews only after registered,native,actual,visual and exact-patch gates."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import illness_critical_editorial as owned
from dk4tool.patch.physical_wounds_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.illness_critical_layout_v974 import layout
from scripts.prepare_illness_critical_release_v975 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_illness_critical_gameplay_v976b import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/illness_critical_editorial_final_review_v1.json')
DOC=Path('docs/illness_critical_v976_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V976 Illness Critical completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V976 Illness Critical')


def reference(e):return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1092 and ledger['records_with_source_and_prose_pass']==1121
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==12 and {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1810,1811,1816,1822,1825,1832}
    assert len(gameplay['scoped_normal_return_controls'])==6 and all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==26 and all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['ASCII_I1810_three_row36cell1811_personal_captain1816_complete1822_retained1825_and_Sera1832_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V969']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256'] and sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all150_original_direct_main_battle_and_ordinary_condition4_5_selections'])==150 and len(context['all100_prior_condition0_1_2_3_discriminating_controls'])==100
    assert context['condition4_selects_critical_sounding1820_1832_not_illness1807_1819'] and context['condition5_selects_illness1807_1819']
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==26 and fonts['complete_native_font_cases']==52
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v975' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),'twelve_actual_holds_six_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'ASCII_I1810_three_row36cell1811_personal1816_independent1822_retained1825_Sera1832_reviewed':True,'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),'all26_fonts52_cases150_source100_controls7336_copies178_sequences_pass':True,
        'twelve_actual_holds_six_returns_seven_startup_controls_and_title_pass':True,'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])};assert not existing.intersection(owned.IDS)
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row) and all(v['text_hex']==entries[n].text.hex() for v in native[n]['ordinary_and_battle_font_controls'])
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],'before_text_hex':row['current_text_hex'],
            'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),'native_font_canvas_sha256_by_mode':{v['mode']:v['canvas_sha256'] for v in native[n]['ordinary_and_battle_font_controls']},
            'actual_display_holds':[h for h in gameplay['actual_complete_dialogue_holds'] if h['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert len(records)==26 and sum(r['editorial_decision']=='revise' for r in records)==22
    final={'format':'dk4-editorial-family-final-review-v1','status':'26-source-context-editorial-native-and-representative-actual-verified','candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'source_manuscript':str(MANUSCRIPT),'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_font_proof':doc['native_font_proof'],'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),'source_context_supplement':doc['source_context_supplement'],
        'actual_scope':gameplay['scope'],'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Illness5-Critical4-comments1807-1832','native_message_IDs':list(owned.IDS),'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1118,records_revised_and_integrated=839,retained_wordings_editorially_completed=279)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1117
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS];assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These are not the full remaining unreviewed shared/routes/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V969']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v975','MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),
        'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-illness-critical26-native-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate);ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_illness_critical_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),'parser':'dk4tool.patch.illness_critical_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['illness_critical_v976']={'status':final['status'],'completed_entries_added':26,'native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),'scope':'26 illness/near-death comments. Remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['illness_critical_actual_phase_v976']={'status':'complete-for26-entries-global-formatting-audit-open','proof':final['actual_gameplay_proof'],
        'checks':'26 full native-font previews in52 source controls,twelve full-word/actual-RGB holds,six normal returns and26 offline corruption controls. Complete ASCII I1810,repaired1821/1822,three-row1811/1816,full Camille1830 and first-person Sera1832 pass within stated native/actual scopes. No game-wide guarantee.'}
    previous_user=Path('work/analysis/physical_wounds_v970/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin']);assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V976 completes26 illness/near-death comments1807-1832 for source conditions5/4 in registered V975:22 revisions and4 retentions. All150 original direct/main battle/ordinary selections,100 prior-status controls,52 native font cases,7336 full copies and178 cache sequences pass. Twelve active-widget bitmap/RGB holds verify ASCII I1810,three-row1811 with36cell last row,personal captain1816,independent complete1822,retained1825 and Sera1832. Six normal returns preserve scoped state through first Back;original battle time resumes on exit. Disclosed room assignment follows observed combat0/1,and one condition4/5 byte is inserted after Deck opens. Seven startup/New Game captures and title match V969. Exact clean-input patch preserves471 batches,114 layers,3642 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes.1118 entries complete (839 revised/279 retained),1121 source/prose reviewed. Older750-752,mood1833,special1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw coverage,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V976-Illness-Critical26-complete','documentation':str(DOC),'proof':str(closure),'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':26,
        'previous_goal_turn_classification':'progress:13 wound messages completed in V969 with52 native fonts,four actual scenes/returns,exact patch and next26 physical-state source contexts',
        'this_goal_turn_classification':'progress:26 source/prose reviews,250 source/control selections,52 native fonts,registered V975/exact patch,six actual scenes/returns and26 completed entries','full_goal_complete':False})
    previous=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1118 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1121
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):assert ledger[key]==previous[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active';save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V976: illness and near-death editorial completion\n\n'+checkpoint+'\n\n## Source and English\n\nTwenty-two revisions and four justified retentions cover26 independent physical-state alternatives. Personal symptoms,reassurance,admiral responsibility,death fears,food regret,still-unfulfilled dream,strongest-fleet ambition,locked Camille,and Seras hesitant wish are preserved.1821 and1822 are separate native alternatives;the old split contraction is repaired without joining their source meanings. Full-width I1810/1824/1830 becomes ASCII. All26 clean sources contain no IC macro. Condition4 selects critical-sounding1820-1832 and5 selects illness1807-1819;source tables and actual native selection prove the order. Cure boasts and fears remain speech,without new outcomes. Exact source references and all five natural-dialogue-v2 gates are retained.\n\n## Formatting and actual scenes\n\nAll26 complete native-font previews match independent words in52 ordinary/battle controls. Three-row1811 keeps Well with the answer and ends in a full36cell row. Personal admiral1816 uses three rows. Appetite1813,retained1818 and dream1828 continuation fill36cells;Camille1830 is complete. All rows start at x0 without manual spacing or breaks. The general story audit rejects this COMMON format;the dedicated native audit has zero errors and unwaived warnings. Six bad-format and20 glyph-deletion controls reject offline.\n\n'+gameplay['scope']+'\n\n## Registered candidate\n\nExperimental profile all-routes-unified-v975 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 message selection metadata differ from V969. All other prose,graphics/routes/HELP/ARM7/overlays,native code,sections/BSS,cache arenas and123040 staged bytes are exact. The xdelta reconstructs every candidate byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Explicit user cold-boot acceptance is still required for canonical promotion.\n\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V976: illness and near-death editorial completion\n\n'+checkpoint+' See [V976 evidence](illness_critical_v976_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label in SPECS:
        source=CAP/f'illness_critical_v976_975_{label}'/'frame_016300_navigation.png';target=GUIDE/f'{label}_V975.png';copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),'provenance':'Actual V975 cold boot with declared coordinates,room assignment and late condition4/5 fixture;not earned illness,injury,recruitment,refit or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in range(971,977):paths.update(p for p in (Path('work/analysis')/f'illness_critical_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*illness_critical*v9*.py'))
    paths.update(Path(p) for p in (owned.CONFIG,str(MANUSCRIPT),'translations/illness_critical_editorial_manuscript_v1.json',str(REVIEW),str(LEDGER),'translations/release_stack.json',
        'dk4tool/patch/illness_critical_editorial.py','scripts/build_integrated_release.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),'work/analysis/illness_critical_v975/standard_story_audit.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'illness_critical_v976_975_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('26 reviews complete:1118 total (839 revised/279 retained),1121 source/prose;',len(copied),'archive files verified. Full goal active.',flush=True)


if __name__=='__main__':main()
