"""Credit13 wound reviews only after exact registered,native,actual and visual evidence."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import physical_wounds_editorial as owned
from dk4tool.patch.physical_fatigue_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.physical_wounds_layout_v968b import layout
from scripts.prepare_physical_wounds_release_v969 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_physical_wounds_gameplay_v970b import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/physical_wounds_editorial_final_review_v1.json')
DOC=Path('docs/physical_wounds_v970_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V970 Physical Wounds completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V970 Physical Wounds')


def reference(e):return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1079 and ledger['records_with_source_and_prose_pass']==1095
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8 and {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1796,1799,1803,1806}
    assert len(gameplay['scoped_normal_return_controls'])==4 and all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==15 and all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['Camille_ASCII_I_Julio35cell_continuation_genuine_captain_and_Sera_special_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V962']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all150_original_direct_main_battle_and_ordinary_wound_selections'])==150 and len(context['all25_healthy_direct_helper_no_message_controls'])==25
    assert context['Sera24_special_ID']==1806 and context['job_role_and_mood_getters_not_called'] and len(context['all25_condition1_prior_fatigue_discriminating_controls'])==25
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==13 and fonts['complete_native_font_cases']==52
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v969' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete_ASCII_I1796_35cell_strength1799_retained1803_and_Sera1806_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),'all13_fonts52_cases150_source25_healthy25_fatigue7336_copies178_sequences_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_pass':True,'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])};assert not existing.intersection(owned.IDS)
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row)
        assert all(v['text_hex']==entries[n].text.hex() for v in native[n]['condition2_3_ordinary_and_battle_font_controls'])
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],'before_text_hex':row['current_text_hex'],
            'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),
            'native_font_canvas_sha256_by_mode':{v['mode']:v['canvas_sha256'] for v in native[n]['condition2_3_ordinary_and_battle_font_controls']},
            'actual_display_holds':[h for h in gameplay['actual_complete_dialogue_holds'] if h['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert len(records)==13 and sum(r['editorial_decision']=='revise' for r in records)==11
    final={'format':'dk4-editorial-family-final-review-v1','status':'13-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'registered_release_proof':str(closure),'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),'source_context_supplement':doc['source_context_supplement'],
        'actual_scope':gameplay['scope'],'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Physical-Conditions2-3-Wounds1794-1806','native_message_IDs':list(owned.IDS),'records':records,
        'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1092,records_revised_and_integrated=817,retained_wordings_editorially_completed=275)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1091
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS];assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts','note':'These are not the full remaining unreviewed shared/routes/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V962']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v969','MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),
        'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-physical-wounds13-native-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate);ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_physical_wounds_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.physical_wounds_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['physical_wounds_v970']={'status':final['status'],'completed_entries_added':13,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),
        'scope':'13 condition2/3 wound comments. Other physical states and remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['physical_wounds_actual_phase_v970']={'status':'complete-for13-entries-global-formatting-audit-open','proof':final['actual_gameplay_proof'],
        'checks':'13 full native fonts in52 condition2/3 ordinary/battle controls,eight full-word/actual-RGB holds,four normal returns and15 offline rejection controls. Complete initial I1796,35cell continuation1799,retained captain1803 and Sera1806 pass. No game-wide guarantee.'}
    previous_user=Path('work/analysis/physical_fatigue_v964/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin']);assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V970 completes13 wound comments1794-1806 for original conditions2/3 in registered V969:11 revisions and2 retentions. All150 original direct/main battle/ordinary selections,25 healthy and25 prior-fatigue controls,52 full native font cases,7336 copies and178 cache sequences pass. Eight active-widget bitmap/RGB holds verify complete initial I1796,Julios35cell continuation1799,genuine captain retained1803 and Sera24 special1806. Four normal returns preserve scoped state through first Back;original battle time resumes on exit. Explicit room assignments follow observed native combat0/1,and a one-byte condition2/3 fixture is applied after Deck opens. Seven ordinary startup/New Game captures and title match V962. Exact clean-input patch preserves471 batches,114 layers,3655 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes.1092 entries complete (817 revised/275 retained),1095 source/prose reviewed. Other physical states,older750-752,mood1833,special1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw coverage,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V970-Physical-Wounds13-complete','documentation':str(DOC),'proof':str(closure),'actual_proof':final['actual_gameplay_proof'],
        'completed_entries_added':13,'previous_goal_turn_classification':'progress:13 fatigue entries completed in V962 with26 native-font cases,four actual scenes/returns,exact patch and next13 wound source controls',
        'this_goal_turn_classification':'progress:13 source/prose reviews,200 original selectors,52 native fonts,registered V969/exact patch,four actual scenes/returns and13 completed entries','full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1092 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1095
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):assert ledger[key]==prior[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V970: physical wound editorial completion\n\n'+checkpoint+'\n\n## Source and English\n\nEleven revisions and two justified retentions cover13 independent wound responses. The clean Japanese restores personal reassurance,hesitant unfinished thoughts,Rafaels ongoing bleeding and But I,Lils pain and responsibility as admiral,and Seras natural brief reassurance. Conditions2/3 share the same dialogue alternatives,but their other effects are not asserted identical. The rough spit remedy remains character speech. All13 clean sources have no IC macro;literal Japanese first-person wording becomes natural English. Exact clean/canonical/current references and all five natural-dialogue-v2 gates are retained.\n\n## Formatting and actual scenes\n\nAll13 complete native-font previews match independent words at x0 in52 ordinary/battle condition2/3 controls. Maria1805 now breaks after Dont worry,and the continuation keeps about a little wound like this intact. The two prior soft-hint attempts are preserved;no prose or manual line breaks were changed. Source fonts and native bounds cover Rafael1802s full35cell first-person fragment and Lils personal admiral line1804. The general story audit rejects this COMMON format;the dedicated original-consumer audit passes with zero errors and unwaived warnings. Four bad-format and11 glyph-deletion controls reject offline.\n\n'+gameplay['scope']+'\n\n## Registered candidate\n\nExperimental profile all-routes-unified-v969 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V962. Native code,all other prose,graphics/routes/HELP/ARM7/overlays,sections/BSS,cache arenas and123040 staged bytes are exact. The xdelta reconstructs every candidate byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Explicit user cold-boot acceptance is still required for canonical promotion.\n\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V970: physical wound editorial completion\n\n'+checkpoint+' See [V970 evidence](physical_wounds_v970_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label in SPECS:
        source=CAP/f'physical_wounds_v970_969_{label}'/'frame_016300_navigation.png';target=GUIDE/f'{label}_V969.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V969 cold boot with declared coordinates,room assignment and late officer-condition2/3 fixture;not earned injury,recruitment,refit or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in (965,966,967,968,'968b',969,970):paths.update(p for p in (Path('work/analysis')/f'physical_wounds_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*physical_wounds*v9*.py'))
    paths.update(Path(p) for p in (owned.CONFIG,str(MANUSCRIPT),'translations/physical_wounds_editorial_manuscript_v1.json',str(REVIEW),str(LEDGER),'translations/release_stack.json',
        'dk4tool/patch/physical_wounds_editorial.py','scripts/build_integrated_release.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/physical_wounds_v969/standard_story_audit.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'physical_wounds_v970_969_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('13 reviews complete:1092 total (817 revised/275 retained),1095 source/prose;',len(copied),'archive files verified. Full goal active.',flush=True)


if __name__=='__main__':main()
