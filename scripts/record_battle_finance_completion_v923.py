"""Credit12 reviews only after registered/native/actual/visual gates pass."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import battle_finance_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_chapel_planning_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from scripts.battle_finance_layout_v920 import layout
from scripts.prepare_battle_finance_release_v922 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_battle_finance_gameplay_v923 import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/battle_finance_editorial_final_review_v1.json')
DOC=Path('docs/battle_finance_v923_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V923 Battle Finance completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V923 Battle Finance')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==954 and ledger['records_with_source_and_prose_pass']==969
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==6
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1670,1675,1678}
    assert len(gameplay['scoped_normal_return_controls'])==3
    assert all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==11
    assert all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['complete_three_row_financial_report1670_initial_I1675_retained_captain1678_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V916']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all75_original_battle_helper_main_and_ordinary_control_selections'])==75
    assert context['no_Sera_special_role15_override_for_role20']
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==12
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v922' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'six_actual_holds_three_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete_three_row_financial_report_initial_I_and_retained_captain_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all12_fonts75_source_controls7336_copies178_sequences_pass':True,
        'six_actual_holds_three_returns_seven_startup_controls_and_title_pass':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])}
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
    assert len(records)==12 and sum(r['editorial_decision']=='revise' for r in records)==11
    final={'format':'dk4-editorial-family-final-review-v1','status':'12-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),
        'ordinary_context_supplement':doc['ordinary_context_supplement'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Battle-Finance20-comments1669-1680','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=966,records_revised_and_integrated=717,retained_wordings_editorially_completed=249)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=965
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V916']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v922',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-battle-finance12-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_battle_finance_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.battle_finance_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['battle_finance_v923']={'status':final['status'],'completed_entries_added':12,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'12 battle Finance comments. Remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['battle_finance_actual_phase_v923']={'status':'complete-for12-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'12 full native fonts,six actual complete words/RGB holds,three normal returns and11 offline rejection controls. Full three-row report1670,initial I1675 and retained captain1678 pass. No game-wide guarantee.'}
    previous_user=Path('work/analysis/battle_chapel_planning_v917/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'])
    assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V923 completes12 battle Finance20 comments1669-1680 in registered V922:11 revisions and1 retention. All75 original battle/main/ordinary controls,all12 native fonts,7336 full copies and178 cache sequences pass. Six active-widget bitmap/RGB holds verify the full three-row financial report1670,Emilios complete initial I1675,and genuine captain1 retained profit reaction1678. Captain assignment is guarded until actual original combat0/1 is observed. Three normal returns preserve UI state through first Back;original battle time resumes on exit. Seven startup/New Game frames and title match V916. Exact clean-input patch preserves471 batches,114 layers,3656 unselected strings,graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes. 966 entries complete (717 revised/249 retained),969 source/prose reviewed. Older750-752,mood1833,special actors1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose and raw inventory remain. Separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V923-Battle-Finance12-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':12,
        'previous_goal_turn_classification':'progress:24 Chapel/Planning entries completed in V916;next12 original Finance contexts mapped',
        'this_goal_turn_classification':'progress:12 source reviews,native fonts,registered V922/exact patch,3 actual scenes/returns and12 completed entries',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==966 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==969
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==prior[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V923: battle Finance editorial completion\n\n'+checkpoint+'\n\n'+"## Source and English\n\nEleven revisions restore the financial report and available time,the explicit month in1674,simultaneous haggling/fighting,first-person wishes,Lils Purser's Office reference and the crew receiving Marias orders. Naval combat is distinguished from all sailing. The already natural1678 wording remains unchanged. Every independent NPC alternative and genuine captain retains exact clean/canonical/current references and natural-dialogue-v2 gloss,context,note and all five review gates. Flavor dialogue does not calculate profits,issue orders or change assignment.\n\n## Formatting and gameplay evidence\n\nAll12 full native-font planes match independently placed complete words at x0 inside216x36. The full three-row financial report1670,initial I1675,explicit month1674 and full Purser's Office1679 are intact. The required standard story audit rejects the COMMON manuscript format;its actual failure log is preserved. The dedicated consumer audit has zero blocking errors/unwaived warnings. Three bad-format controls,six first/final glyph deletions and second/third-row w deletions all reject as intended. Unique native RTTI,geometry,252x36 full bitmap and216x36 actual RGB ink/blank-plane checks exclude stale text behind menus.\n\n"+gameplay['scope']+'\n\n'+"## Registered candidate\n\nExperimental profile all-routes-unified-v922. Canonical base out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. All471 batches/114 accepted layers plus the registered experimental profile are rebuilt by the integrated builder. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V916;all other strings,graphics/routes/HELP/ARM7/overlays,native code,sections/BSS,cache arenas and123040 staged bytes are exact. The patch reconstructs V922 byte-for-byte from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Human cold-boot acceptance remains required before canonical promotion;test Finance/Purser's Office battle comments and normal returns. The full editorial goal remains active.\n"+'\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V923: battle Finance editorial completion\n\n'+checkpoint+' See [V923 evidence](battle_finance_v923_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[];frame_plan=read(ROOT/'actual_sample_frame_plan.json')
    for label in SPECS:
        n=frame_plan['cases'][label]['holds'][0]
        source=CAP/f'battle_finance_v923_922_{label}'/f'frame_{n:06d}_navigation.png'
        target=GUIDE/f'{label}_V922.png';copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V922 cold boot with declared coordinate and room/occupant fixtures;not earned refit,recruitment,qualification or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in (918,919,920,922,923):
        paths.update(p for p in (Path('work/analysis')/f'battle_finance_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*battle_finance*v9*.py'))
    paths.update(Path(p) for p in (owned.CONFIG,'translations/battle_finance_editorial_release_v1.json',str(MANUSCRIPT),
        'translations/battle_finance_editorial_manuscript_v1.json',str(REVIEW),'translations/editorial_review_current_v1.json',
        'translations/release_stack.json','dk4tool/patch/battle_finance_editorial.py','scripts/build_integrated_release.py',
        'scripts/native_battle_standoff_v923.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/battle_finance_v922/standard_story_audit.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'battle_finance_v923_922_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('12 reviews complete:966 total (717 revised/249 retained),969 source/prose;',len(copied),'archive files verified. Full goal active.',flush=True)


if __name__=='__main__':main()
