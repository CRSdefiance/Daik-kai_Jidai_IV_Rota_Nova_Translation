"""Credit39 reviews only after exact registered,native,actual and visual evidence."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import mood_comments_editorial_v981b as owned
from dk4tool.patch.illness_critical_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.mood_comments_layout_v980 import layout
from scripts.prepare_mood_comments_release_v981b import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_mood_comments_gameplay_v982b import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/mood_comments_editorial_final_review_v1.json')
DOC=Path('docs/mood_comments_v982_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V982 Mood comments completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V982 Mood comments')

def reference(e):return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}

def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1118 and ledger['records_with_source_and_prose_pass']==1160
    assert ledger['records_revised_and_integrated']==839 and ledger['retained_wordings_editorially_completed']==279
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==12
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1835,1845,1853,1855,1868,1871}
    assert len(gameplay['scoped_normal_return_controls'])==6
    assert all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==26 and all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['complete_I1835_ASCII_I1845_quoted19_and35cell1853_pure_silence1855_self_calming1868_comic1871_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V975']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all225_original_direct_main_battle_and_ordinary_mood_selections'])==225
    assert len(context['all75_physical_condition1_priority_controls'])==75 and len(context['all72_direct_NPC_hero_normal_mood1_2_3_no_message_controls'])==72
    assert context['source_mood_IDs']==[0,4,5] and context['source_physical_condition0_required_for_mood_selection']
    native={r['message_id']:r for r in fonts['cases']}
    assert len(native)==39 and fonts['complete_native_font_cases']==78
    assert fonts['preserved_byte_identical_native_font_cases']==76 and fonts['new_native_font_cases']==2 and fonts['only_changed_compiled_IDs']==[1853]
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v981' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(release['changed_native_message_IDs'])==25 and stage['all3629_other_message_strings_exact']
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'twelve_actual_holds_six_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete_I_self_talk_odd_row_silence_personal_panic_and_comic_symbols_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all39_fonts78_cases225_source75_priority72_normal_controls7336_copies178_sequences_pass':True,
        'font_case_reuse_disclosed_76_exact_original_plus2_fresh_for1853':True,
        'twelve_actual_holds_six_returns_seven_startup_controls_and_title_pass':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,
        'retained1854_and1865_entire_opaque_copy_spans_exact':True,'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for family in ledger['completed_editorial_families'] for n in family.get('native_message_IDs',[])}
    assert not existing.intersection(owned.IDS)
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row)
        assert all(v['text_hex']==entries[n].text.hex() for v in native[n]['ordinary_and_battle_font_controls'])
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],
            'before_text_hex':row['current_text_hex'],'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),
            'native_font_canvas_sha256_by_mode':{v['mode']:v['canvas_sha256'] for v in native[n]['ordinary_and_battle_font_controls']},
            'actual_display_holds':[h for h in gameplay['actual_complete_dialogue_holds'] if h['message_id']==n],
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert len(records)==39 and sum(r['editorial_decision']=='revise' for r in records)==25
    final={'format':'dk4-editorial-family-final-review-v1','status':'39-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),
        'source_context_supplement':doc['source_context_supplement'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Mood0-4-5-comments1833-1871','native_message_IDs':list(owned.IDS),'records':records,
        'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1157,records_revised_and_integrated=864,retained_wordings_editorially_completed=293)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1156
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts','note':'These are not the full remaining unreviewed shared/routes/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V975']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v981',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-mood39-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_mood_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.mood_comments_editorial_v981b.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['mood_comments_v982']={'status':final['status'],'completed_entries_added':39,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),'final_review':str(REVIEW),
        'scope':'39 independent mood comments. Remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['mood_actual_phase_v982']={'status':'complete-for39-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All39 complete fonts in78 controls (76 original byte-identical cases plus2 fresh for1853);twelve actual bitmap/RGB holds,six returns and26 negative controls. Complete I,19cell quotation with aligned35cell reply,pure silent ellipsis and six comic symbols pass. No game-wide guarantee.'}
    prior_user=Path('work/analysis/illness_critical_v976/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'])
    assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(prior_user),'reference_sha256':sha(prior_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V982 completes39 independent mood0/4/5 comments1833-1871 in registered V981:25 revisions and14 retentions. All225 original selections,75 physical-priority controls,72 defined normal-mood controls,78 complete font cases (76 exact originals plus2 fresh self-talk cases),7336 full copies and178 cache sequences pass. Twelve active-widget bitmap/RGB holds verify complete I1835/1845,19cell quoted self-talk and aligned35cell reply1853,pure silent1855,personal self-calming1868 and six comic symbols1871. Six normal returns and26 offline corruption controls pass. Disclosed room assignments follow observed combat0/1;only one mood byte7 changes after Deck opens,with physical health0 and identities preserved. Seven startup/New Game captures and title match V975. Exact clean-input patch preserves471 batches,114 layers,3629 unselected strings,all graphics/routes/native code,single8KiB cache,216x36 crop,opaque spans and123040 staged bytes.1157 entries complete (864 revised/293 retained),1160 source/prose reviewed. Older750-752,remaining activity/special comments1872-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose/raw inventory,separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V982-Mood39-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':39,
        'previous_goal_turn_classification':'progress:current shop676/677 bytes,native wrapping and independent glyph planes freshly reverified;formatting watch remains open',
        'this_goal_turn_classification':'progress:39 source/prose/font reviews integrated into registered V981 with exact patch,six actual scenes/returns and ledger completion credit',
        'full_goal_complete':False})
    previous=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1157
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==1160
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==previous[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V982: mood and panic editorial completion\n\n'+checkpoint+'\n\n## Source and English\n\nTwenty-five revisions and fourteen justified retentions cover39 independent alternatives. Mood0 is positive,4 dejected,5 panicked;physical health0 is required. Original health1 preempts mood. Full separate1843/1844 and1855/1856 restore words previously split across unrelated choices.1855 is source silence only;1871 remains nonverbal comic symbols without invented profanity.1868/1870 are personal self-calming. ASCII I1845/1846/1858 replaces obsolete full-width guards. Source/gloss/context,natural American English and five v2 editorial gates are recorded for every entry.\n\n## Formatting and actual evidence\n\nAll39 whole-font previews pass. Two fresh original-consumer font executions refine1853 to a19cell quote and35cell complete reply;76 byte-identical cases retain their hash-checked original evidence. All lines start at x0 without authored padding or manual breaks. Dedicated native QA has zero blocking errors and unwaived warnings;the general story audit rejects this distinct COMMON format and is not claimed as passing. Retained1854/1865 have opaque punctuation after their NULs;their entire copy spans remain exact. No repacker assertion was relaxed.\n\n'+gameplay['scope']+'\n\n## Registered release\n\nProfile all-routes-unified-v981 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only /COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V975. Every other ROM file,route,graphic,HELP,ARM7,overlay,native code/cache/section/BSS/arena and123040 staged bytes is exact. The xdelta reconstructs all bytes from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Canonical promotion awaits explicit user acceptance.\n\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V982: mood and panic editorial completion\n\n'+checkpoint+' See [V982 evidence](mood_comments_v982_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label in SPECS:
        source=CAP/f'mood_comments_v982_975_{label}'/'frame_016300_navigation.png';target=GUIDE/f'{label}_V981.png'
        copy2(source,target);assert source.read_bytes()==target.read_bytes()
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V981 cold boot with declared coordinates,room and late mood fixture. Health/identities preserved;not earned mood,recruitment,refit or publication approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in range(977,983):
        paths.update(p for p in (Path('work/analysis')/f'mood_comments_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*mood*v9*.py'))
    paths.update(Path('dk4tool/patch').glob('mood_comments_editorial*.py'))
    paths.update(Path('translations').glob('mood_comments*.json'))
    paths.update(Path(p) for p in (str(LEDGER),'translations/release_stack.json','scripts/build_integrated_release.py',str(DOC),
        str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/mood_comments_v981/builder_added_optional_stage.bin','work/analysis/mood_comments_v981/standard_story_audit.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'mood_comments_v982_975_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('39 reviews complete:1157 total (864 revised/293 retained),1160 source/prose;',len(copied),'archive files verified. Full goal active.')

if __name__=='__main__':main()
