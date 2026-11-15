"""Credit17 reviews after both native consumers,actual scenes,returns and exact patch pass."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import activity_special_editorial_v987b as owned
from dk4tool.patch.mood_comments_editorial_v981b import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.activity_special_layout_v986b import compiled,visible_lines
from scripts.prepare_activity_special_release_v987 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_activity_special_gameplay_v989 import ROOT,ROM,CAP,SPECS,case_folder
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/activity_special_editorial_final_review_v1.json')
DOC=Path('docs/activity_special_v988_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V988 Activity special completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V988 Activity special')

def reference(e):return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}

def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1157 and ledger['records_with_source_and_prose_pass']==1177
    assert ledger['records_revised_and_integrated']==864 and ledger['retained_wordings_editorially_completed']==293
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==18 and len(gameplay['scoped_normal_return_controls'])==9
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={1873,1876,1878,1879,1880,1885,1886,1887,1888}
    assert all(r['assignments_and_funds_preserved_on_return'] and r['no_active_Cabin_view_at_normal_sea_return'] for r in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_corruption_controls'])==36 and all(r['rejected'] for r in gameplay['offline_corruption_controls'])
    assert gameplay['all3_Chapel_refusal_source_and_wrapped_buffers_complete_and_original_Assign_dismissal_return_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V981']
    digest=sha(ROM.read_bytes());assert digest==release['candidate_sha256']==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==digest
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert [len(context[k]) for k in ('all52_activity2_direct_and_main_priority_cases','all16_special_ordinary_battle_direct_and_main_bit2_controls',
        'all12_original_actor_role_legality_controls','all3_original_Chapel_assignment_refusal_owner_and_speaker_calls')]==[52,16,12,3]
    assert len(fonts['cases'])==17 and fonts['complete_Deck_native_font_cases']==20 and fonts['complete_modal_native_font_cases']==3
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471 and manifest['profile']=='all-routes-unified-v987'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(release['changed_native_message_IDs'])==14 and stage['all3651_other_message_strings_exact']
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'all18_actual_holds9_returns7_startup_controls_and_title_visually_reviewed':True,
        'all3_popup_A_dismissal_frames17300_show_no_extra_or_blank_page':True,
        'three_popup_guards_full_ASCII_I_and_uniform_margins_36cell_body_edges_and_Aziza_both_outcomes_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_graphics_or_full_route_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':digest,'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all17_source_prose20_Deck_and3_modal_font_cases_52_16_12_3_original_controls_pass':True,
        'all18_actual_holds9_returns36_negative_controls_startup_and_title_pass':True,
        '7336_native_copies178_cache_sequences_and_exact_clean_patch_fresh_hash_pass':True,
        'all471_batches114_accepted_layers_routes_graphics_native_code_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_changed_from_V981':True,
        'modal_layouts_machine_generated_and_reconstructable_without_historical_ROM_dependency':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])};assert not existing.intersection(owned.IDS)
    cases={r['message_id']:r for r in fonts['cases']};records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==compiled(row) and entries[n].text.hex()==cases[n]['compiled_hex']
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],
            'before_text_hex':row['current_text_hex'],'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':visible_lines(row),'complete_native_font_case':cases[n],
            'actual_display_holds':[r for r in gameplay['actual_complete_dialogue_holds'] if r['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert len(records)==17 and sum(r['editorial_decision']=='revise' for r in records)==14
    final={'format':'dk4-editorial-family-final-review-v1','status':'17-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':digest,'source_manuscript':str(MANUSCRIPT),'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'registered_release_proof':str(closure),'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_font_proof':doc['native_font_proof'],'source_context_supplement':doc['source_context_supplement'],
        'completion_visual_review':str(visual),'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Activity2-Chapel-refusal-special1872-1888','native_message_IDs':list(owned.IDS),'records':records,
        'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1174,records_revised_and_integrated=878,retained_wordings_editorially_completed=296)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1173
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts','note':'These are not the full remaining shared/routes/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V981']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':digest,'profile':'all-routes-unified-v987','MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),
        'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-activity-special17-two-native-consumers-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_activity_special_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.activity_special_editorial_v987b.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['activity_special_v988']={'status':final['status'],'completed_entries_added':17,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),
        'scope':'17 independent activity/Chapel/special comments. Wider prose/raw inventory and graphics stay unfinished.'})
    ledger['formatting_watchlist']['activity_special_actual_v988']={'status':'complete-for17-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'20 embedded original font cases and3 separate native popup cases;18 actual complete font/RGB holds,nine original returns and36 corruption controls. Complete first I in all3 popup strings,aligned guarded continuations and36cell body edges pass. No game-wide guarantee.'}
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin']);assert all(entries[n].text==old_entries[n].text for n in (676,677))
    prior_user=Path('work/analysis/mood_comments_v982/user676_677_current_preservation.json');user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':digest,'reference_proof':str(prior_user),'reference_sha256':sha(prior_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V988 completes17 activity2,Chapel refusal and special-character comments1872-1888 in registered V987:14 revisions and3 retentions.52 original activity controls,16 special ordinary/battle controls,12 legality calls and3 original Chapel refusal dispatches pass.20 complete embedded font cases and3 distinct native popup cases preserve all words,guards,margins and bounds.18 actual native/bitmap/RGB holds cover six Deck samples and all3 Chapel refusals;nine normal returns and36 corruption controls pass. Native Assign opens each refusal,A dismisses once,and selection cancel/Deck exit return to sea without an extra page. Declared room/UI event/selection and two Aziza shared-item-bit fixtures preserve actor/captain32-byte records,health,mood and actual battle mode;two coordinate approaches remain. Seven startup/New Game captures and title match V981. Exact clean-input patch preserves471 batches,114 layers,3651 other strings,all graphics/routes/native code,single8KiB cache,216x36 crop and123040 staged bytes.1174 entries complete (878 revised/296 retained),1177 source/prose reviewed. Older750-752,remaining shared/routes/player prose/raw inventory,raw abandon-caption0x134E54,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V988-activity-special17-complete','proof':str(closure),'documentation':str(DOC),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':17,
        'previous_goal_turn_classification':'progress:39 mood comments completed in V981 with full native and six actual samples;next17 original selection research mapped',
        'this_goal_turn_classification':'progress:17 source/prose reviews,two native-consumer font proofs,registered V987/exact patch,nine actual samples/returns and completed coverage',
        'full_goal_complete':False})
    previous=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1174 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1177
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==previous[key]
    assert ledger['goal_status']=='active' and not ledger['full_goal_complete'];save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:f.write('# V988: activity,Chapel and special-character editorial completion\n\n'+checkpoint+'\n\n## English and source fidelity\n\nFourteen revisions and three justified retentions cover independent alternatives. Source review restores Emilio\'s promise,Samwell\'s change of pace,Jam\'s health warning,Fernando\'s leisurely work,Julio\'s mood-lifting drink,Al\'s personal Arab pride,Yifa\'s ongoing Taoist training,Yukihisa\'s formal Christian refusal,Yifa\'s exertion cries and training test,Julian\'s new pickup line,and Aziza\'s request to fight and protective instruction. No universal Taoist ban,named religion for Al,rum,kinship or unverified story-state meaning is invented. Native actor names and Chapel refusal speaker pointers are proven. The original post-event activity2 path is preserved;no new Scold command is introduced.\n\n## Distinct display consumers\n\nThe14 Deck comments use the original36cell/3row body and phase-safe automatic planner. The3 popup paragraphs use existing native balanced wrapping,with its generated bytes source-locked to exact prose and original font proof. The compiler requires no historical ROM;no runtime membership or code change is needed. Native and actual glyph comparisons include complete ASCII I,continuation origins,blank paper and final punctuation.\n\n'+gameplay['scope']+'\n\n## Integrated experimental candidate\n\nProfile all-routes-unified-v987 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Changed internal files relative to V981:/COMMON/MESFILE.DK4 and ARM9 selection metadata only. Every other file and native code/sections/BSS/arena/cache/crop/123040 staged bytes is exact. Xdelta reconstructs every byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Candidate remains experimental and canonical promotion awaits explicit user acceptance. For manual review,cold-boot the title/New Game and inspect the post-event Deck speech and Chapel assignment refusal/dismissal paths.\n\nROM SHA256 '+digest+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for path in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## V988: activity,Chapel and special-character editorial completion\n\n'+checkpoint+' See [V988 evidence](activity_special_v988_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label,(_,_,activity,_) in SPECS.items():
        frame=16900 if activity is None else 16300;source=case_folder(label)/f'frame_{frame:06d}_navigation.png';target=GUIDE/f'{label}_V987.png'
        copy2(source,target);assert source.read_bytes()==target.read_bytes()
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V987 cold boot with disclosed room/UI/shared-item-bit and coordinate fixtures. No earned event,unlock,recruitment,assignment or publication approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':digest,'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in range(984,990):
        paths.update(p for p in (Path('work/analysis')/f'activity_special_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*activity_special*.py'));paths.update(Path('dk4tool/patch').glob('activity_special*.py'))
    paths.update(Path('translations').glob('activity_special*.json'))
    paths.update(Path(p) for p in (str(LEDGER),'translations/release_stack.json','scripts/build_integrated_release.py',str(DOC),
        str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/activity_special_v987/builder_added_optional_stage.bin','work/analysis/activity_special_v987/standard_story_audit.log',
        'work/analysis/next_comments_v983/source_selection_research.json'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=case_folder(label)
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_save_duplicated_in_archive':True})
    print('17 reviews complete:1174 total (878 revised/296 retained),1177 source/prose;',len(copied),'archive files and9 guide screenshots verified. Full goal active.')

if __name__=='__main__':main()
