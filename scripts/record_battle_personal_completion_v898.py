"""Complete only25 source-reviewed battle comments after all native/actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.patch import battle_personal_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.battle_personal_layout_v892 import layout
from scripts.prepare_battle_personal_release_v893 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_battle_personal_gameplay_v898 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/battle_personal_editorial_final_review_v1.json')
DOC=Path('docs/battle_personal_v898_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V898 Battle personal completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V898 Battle personal comments')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==856 and ledger['records_with_source_and_prose_pass']==884
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==6
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1572,1577,1590}
    assert len(gameplay['scoped_normal_return_controls'])==3
    assert all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['Carlo_odd19_row_complete_leading_N_and_nodding_direction_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V888']
    assert read('work/analysis/duel_name_v896/name_policy_resolution.json')['duel_Hodram_label_is_consistent_with_recorded_user_name_decision']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all125_original_selector_and_discriminating_control_cases'])==125
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==25
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v893' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'six_actual_holds_three_normal_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete_odd_row_N_and_trailing_punctuation_reviewed':True,'visual_review_pending':False,
        'format_flags0E04_observed_from_actual_native_bitmap_and_unchanged_LDRB_format_contract':True,
        'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all25_complete_fonts125_source_controls7336_copies178_sequences_pass':True,
        'six_actual_holds_three_returns_ordinary_control_seven_startup_controls_and_title_pass':True,
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
    assert sum(r['editorial_decision']=='revise' for r in records)==18 and len(records)==25
    final={'format':'dk4-editorial-family-final-review-v1','status':'25-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),
        'hobby_and_terms_proof':doc['hobby_and_term_proof'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Battle-personal-hobby-comments1571-1595','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=881,records_revised_and_integrated=651,retained_wordings_editorially_completed=230)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=880
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These three reviewed drafts are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V888']=deepcopy(ledger['current_integrated_candidate'])
    ledger['previous_pending_integrated_candidate_V893']=ledger.pop('pending_registered_battle_personal_candidate')
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v893',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-battle-personal25-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_battle_personal_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.battle_personal_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['battle_personal_v898']={'status':final['status'],'completed_entries_added':25,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'25 battle-personal hobby comments. Other shared/routes/player prose,raw coverage,special actors and graphics stay unfinished.'})
    ledger['formatting_watchlist']['battle_personal_actual_phase_v898']={'status':'complete-for25-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All25 complete fonts;x0 alignment;actual Julio drink text,Carlo complete leading N after odd19-character row,and genuine captain1 retained comment. Six complete bitmap/RGB holds,three normal returns and ordinary1380 discrimination. No game-wide guarantee.'}
    user=ROOT/'user676_677_current_preservation.json';reference_user=Path('work/analysis/battle_personal_v894/user676_677_current_preservation.json')
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(reference_user),'reference_sha256':sha(reference_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V898 completes25 battle-personal hobby comments1571-1595 in registered V893:18 revisions and7 retentions. '
        'All125 original selector/control cases,all25 complete native fonts,7336 full copies and178 cache sequences pass. Six actual bitmap/RGB holds verify Julio generic drink,Carlo nodding-off continuation with complete N after odd19-character row,and genuine captain1 retained battle reaction. '
        'A separate actual ordinary Carlo1380 control distinguishes battle1590. Three normal returns preserve UI-open state through first Back;original battle time resumes after leaving. Seven ordinary startup/New Game frames and title menu match V888. '
        'Exact clean-input patch preserves471 batches,114 layers,3643 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes. '
        '881 entries complete (651 revised/230 retained),884 source/prose reviewed. The naming lead is resolved:Hodram is the documented first name and Joakim the middle name;no name edit. '
        'Older750-752,special actors1885-1888,and all unreviewed shared/routes/player prose/raw coverage remain. Separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V898-Battle-personal25-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':25,
        'previous_goal_turn_classification':'progress:V893 integrated25 source/native reviews and original battle initialization;actual bodies pending',
        'this_goal_turn_classification':'progress:three actual battle samples,ordinary control,returns,title,source name-policy correction and25 completed entries',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==881
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==884
    for k in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit'):
        assert ledger[k]==prior[k]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    save('out/editorial_review_pending_battle_personal.json',{**candidate,'pending':False,'superseded_by_current_completed_family_review':str(REVIEW)})
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V898: battle-personal editorial completion\n\n'+checkpoint+'\n\n'
            '## Source and English\n\nEighteen source-first revisions remove invented smoke/rum and restore the Naval Warfare Encyclopedia title,reading delay,fishing priority,sword/model care,food/grooming thoughts,training breaths,experiment,nodding-off gag,card-reading offer,duel move,sleepy refusal and sad flowers. Seven natural wordings remain. Each independent actor alternative has exact clean/canonical/current references,meaning gloss,localization note and all natural-dialogue-v2 gates. No combat/stat effect is invented. The original book-title romanization typo in the explanatory draft note is corrected in productionv2,without changing source or shipped prose.\n\n'
            '## Native formatting and actual verification\n\nAll25 original-font planes match independently placed complete words at x0;body ink fits216x36. The standard story audit does not support this COMMON manuscript format;its failure log remains. The dedicated source/native consumer audit passes with zero errors/unwaived warnings. Actual native0E04 texture flags retain the documented low-byte4 format;only this observed flag value is added in a scoped successor while preserving RTTI,geometry,pointer,complete bitmap and RGB guards.\n\n'+gameplay['scope']+'\n\n'
            'The actual first/final letters and all blank cells pass. Offline removal of Carlo continuation N and Julio final exclamation is rejected;three wrong-format-header controls are rejected. The six actual screenshots,three returns,seven startup frames and title were visually reviewed. The captain sample needed its own tutorial timing;the journal preserves those inputs. No battle mode or outcome was assigned.\n\n'
            '## Names and retained work\n\nThe observed duel Hodram label is correct under the documented full name Hodram Joakim Bergstrom. A fresh no-save control,original getter and complete6144-cell name bitmap resolve the earlier first/middle-name audit confusion. No name overwrite or ROM edit is warranted. The distinct Samwell header,graphics/all18 plaques,older750-752,special actor texts1885-1888,remaining shared/routes/player prose,raw source coverage and later older-record re-audit remain open.\n\n'
            '## Registered candidate\n\nExperimental profile all-routes-unified-v893. ROM SHA256 '+candidate['sha256']+'. Patch SHA256 '+candidate['patch_sha256']+'. Canonical base out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V888. All471 batches/114 accepted layers,art/routes/HELP/ARM7/overlays,native code,section/BSS/cache arenas and123040 staged bytes remain exact. Clean-input patch reconstruction is byte-exact. Human cold-boot acceptance remains required before canonical promotion.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V898: battle personal editorial completion\n\n'+checkpoint+' See [V898 evidence](battle_personal_v898_completion.md).\n')
    GUIDE.mkdir(parents=True);guide_rows=[]
    for label,spec in CASES.items():
        source=CAP/f'battle_personal_v897_893_{label}'/f'frame_{spec[2][0]:06d}_navigation.png'
        target=GUIDE/f'{label}_battle_personal_V893.png';copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        guide_rows.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V893 cold-boot naval battle with declared coordinate and Cabin-occupant fixture;not earned recruitment,travel,qualification or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide_rows,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for directory in ('battle_personal_v890','battle_personal_v891','battle_personal_v892','battle_personal_v893',
        'battle_personal_v894','battle_personal_v895','duel_name_v896','battle_personal_v897','battle_personal_v898'):
        paths.update(p for p in (Path('work/analysis')/directory).rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*battle_personal*v89*.py'));paths.update(Path('scripts').glob('*duel_name*v896.py'))
    paths.update(Path(p) for p in (owned.CONFIG,str(MANUSCRIPT),'translations/battle_personal_editorial_manuscript_v1.json',str(REVIEW),
        'translations/editorial_review_current_v1.json','translations/release_stack.json','translations/character_name_localization_policy_v1.json',
        'dk4tool/patch/battle_personal_editorial.py','scripts/build_integrated_release.py','scripts/native_battle_standoff_v897.py',
        'scripts/native_battle_proximity_v894.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/battle_personal_v893/standard_story_audit_console.log'))
    copied=[]
    for source in sorted(paths):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for label in CASES:
        folder=CAP/f'battle_personal_v897_893_{label}'
        for source in folder.iterdir():
            if source.suffix not in ('.json','.jsonl','.png'):continue
            target=ARCHIVE/'actual_captures'/folder.name/source.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
            assert sha(source.read_bytes())==sha(target.read_bytes());copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide_rows,
        'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('Battle personal25 completed:881 total (651 revised/230 retained),884 source/prose;',len(copied),'archive files verified. Full goal remains active.',flush=True)


if __name__=='__main__':main()
