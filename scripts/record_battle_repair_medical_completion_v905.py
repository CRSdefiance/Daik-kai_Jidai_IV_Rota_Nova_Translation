"""Complete24 battle repair/medical reviews only after native and actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import battle_repair_medical_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_repair_medical_layout_v902 import layout
from scripts.prepare_battle_repair_medical_release_v904 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_battle_repair_medical_gameplay_v905 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/battle_repair_medical_editorial_final_review_v1.json')
DOC=Path('docs/battle_repair_medical_v905_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V905 Battle repair medical completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V905 Battle repair medical')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==881 and ledger['records_with_source_and_prose_pass']==908
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1600,1605,1610,1615}
    assert len(gameplay['scoped_normal_return_controls'])==4
    assert all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==9
    assert all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['complete36_cell1600_1615_lines_ASCII_I1610_and_odd25_emergency_repair_continuation_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V893']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof']);terms=read(doc['native_pronoun_proof'])
    assert len(context['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    assert terms['source1610_means_I_am_here_so_do_not_worry'] and len(terms['all25_current_and_clean_parser_control_cases'])==25
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==24
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v904' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'both36_cell_lines_complete_I_and_C_continuations_and_all_trailing_letters_reviewed':True,
        'observed_native0C04_flags_supported_by_original_LDRB_low_byte4_contract_and_full_pixel_proof':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all24_fonts150_source_controls50_pronoun_controls7336_copies178_sequences_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_pass':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and123040_staged_bytes_preserved':True,
        'only_COMMON_and_ARM9_selection_metadata_change_existing_cache_code_and_crop_exact':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
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
    assert sum(r['editorial_decision']=='revise' for r in records)==19 and len(records)==24
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),
        'native_pronoun_proof':doc['native_pronoun_proof'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Battle-Shipwright13-Medical14-comments1596-1619','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=905,records_revised_and_integrated=670,retained_wordings_editorially_completed=235)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=904
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These three reviewed drafts are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V893']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v904',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-battle-repair-medical24-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_battle_repair_medical_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.battle_repair_medical_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['battle_repair_medical_v905']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 battle Shipwright/Medical comments. Other shared/routes/player prose,raw coverage,special actors and graphics stay unfinished.'})
    ledger['formatting_watchlist']['battle_repair_medical_actual_phase_v905']={'status':'complete-for24-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All24 native fonts;two actual36-cell lines,complete initial ASCII I1610,I after odd25-cell1605 row,and Come1615 continuation. Eight complete bitmap/RGB holds,four normal returns and9 negative controls. No game-wide guarantee.'}
    user=ROOT/'user676_677_current_preservation.json';previous_user=Path('work/analysis/battle_personal_v898/user676_677_current_preservation.json')
    old_entries=__import__('dk4tool.patch.battle_personal_editorial',fromlist=['current_entries']).current_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'])
    assert all(entries[n].text==old_entries[n].text for n in (676,677))
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V905 completes24 battle Shipwright13/Medical14 comments1596-1619 in registered V904:19 revisions and5 retentions. '
        'All150 original battle/ordinary selector controls,50 current/clean first-person expansions,all24 complete fonts,7336 native copies and178 cache sequences pass. '
        'Eight actual bitmap/RGB holds verify full36-cell1600/1615 lines,genuine captain emergency repairs1605 with full33-cell continuation after odd25,complete initial ASCII I1610 and Come1615 continuation. '
        'Four normal returns preserve UI state through first Back;original battle time resumes on exit. Seven startup/New Game frames and title menu match V893. '
        'Exact clean-input patch preserves471 batches,114 layers,3644 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes. '
        '905 entries complete (670 revised/235 retained),908 source/prose reviewed. Older750-752,special actors1885-1888,and all unreviewed shared/routes/player prose/raw coverage remain. '
        'Separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V905-Battle-repair-medical24-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:25 battle-personal entries completed and next24 original contexts mapped',
        'this_goal_turn_classification':'progress:24 source reviews,50 pronoun controls,all native fonts,registered V904/exact patch,4 actual scenes/returns and24 completed entries',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==905 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==908
    for k in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[k]==prior[k]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V905: battle repair and medical editorial completion\n\n'+checkpoint+'\n\n'
            '## Source and English\n\nNineteen source-first revisions restore immediate personal reinforcement and repair offers,damage-location reporting,emergency repairs,medical reassurance,personal treatment and the understated life warning. Five natural wordings remain. Original IC is first person in all50 current/clean parser cases;the fluent1610 wording now uses complete ordinary ASCII I. Independent NPC voice alternatives and four genuine captains are distinguished from consecutive speech. Every record retains exact clean/canonical/current references and natural-dialogue-v2 gloss,context,note and gates. No repair,medical or statistic effect is invented.\n\n'
            '## Native formatting and actual scope\n\nAll24 original-font planes match independently placed complete words at x0 within216x36. The standard story audit rejects the COMMON manuscript format;its actual failure log remains. The dedicated native consumer audit passes with zero errors/unwaived warnings. Actual0C04 flags are additionally admitted in a scoped successor after verifying original clean/current01FF9344 is LDRB r0,[r6],which reads low-byte format4. All RTTI,geometry,pointer,complete bitmap/RGB and guard checks remain. The initial header rejection was a verifier admission limit,not a game display failure.\n\n'+gameplay['scope']+'\n\n'
            'Each actual first/final letter and blank cell passes. Four bad-format controls and five offline glyph-deletion controls reject missing initial I,continuation I/C and final periods at36-cell bounds. The eight actual screenshots,four returns,seven startup frames and title were visually reviewed. Individual input journals preserve the different tutorial and menu paths;stale upper-screen content behind a menu is not credited as an active body. No mode,outcome,resource,health or actor-identity injection was used.\n\n'
            '## Registered candidate and remaining work\n\nExperimental profile all-routes-unified-v904. ROM SHA256 '+candidate['sha256']+'. Patch SHA256 '+candidate['patch_sha256']+'. Canonical base out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V893. All471 batches/114 layers,graphics/routes/HELP/ARM7/overlays,native code,section/BSS/cache arenas and123040 staged bytes remain exact. Clean-input patch reconstruction is byte-exact. Human cold-boot acceptance is required before canonical promotion. Older750-752,special actors1885-1888,remaining shared/routes/player prose,raw inventory,separate graphics/all18 plaques,Samwell header and the later older-record re-audit remain open.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V905: battle repair and medical editorial completion\n\n'+checkpoint+' See [V905 evidence](battle_repair_medical_v905_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for label,spec in CASES.items():
        source=CAP/f'battle_repair_medical_v905_904_{label}'/f'frame_{spec[4][0]:06d}_navigation.png'
        target=GUIDE/f'{label}_V904.png';copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V904 cold-boot naval battle with declared ship-coordinate and room/occupant fixture;not earned refit,recruitment,qualification or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for directory in ('battle_repair_medical_v899','battle_medical_v900','battle_repair_medical_v901','battle_repair_medical_v902','battle_repair_medical_v904','battle_repair_medical_v905'):
        paths.update(p for p in (Path('work/analysis')/directory).rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*battle_repair_medical*v90*.py'));paths.update(Path('scripts').glob('*battle_medical*v900.py'))
    paths.update(Path(p) for p in (owned.CONFIG,str(MANUSCRIPT),'translations/battle_repair_medical_editorial_manuscript_v1.json',str(REVIEW),
        'translations/editorial_review_current_v1.json','translations/release_stack.json','dk4tool/patch/battle_repair_medical_editorial.py',
        'scripts/build_integrated_release.py','scripts/native_battle_standoff_v905.py',str(DOC),
        str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),'work/analysis/battle_repair_medical_v904/standard_story_audit_console.log'))
    copied=[]
    for source in sorted(paths):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for label in CASES:
        folder=CAP/f'battle_repair_medical_v905_904_{label}'
        for source in folder.iterdir():
            if source.suffix not in ('.json','.jsonl','.png'):continue
            target=ARCHIVE/'actual_captures'/folder.name/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,
        'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('Battle repair/medical24 completed:905 total (670 revised/235 retained),908 source/prose;',len(copied),'archive files verified. Full goal remains active.',flush=True)


if __name__=='__main__':main()
