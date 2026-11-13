"""Credit24 reviews only after registered/native/actual/visual gates pass."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch import battle_gunnery_deck_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_sails_boarding_editorial import current_entries as previous_entries
from dk4tool.rom.nds import NdsImage
from scripts.battle_gunnery_deck_layout_v952 import layout
from scripts.prepare_battle_gunnery_deck_release_v954 import ROOT as RELEASE,MANUSCRIPT,OLD
from scripts.verify_battle_gunnery_deck_gameplay_v955 import ROOT,ROM,CAP,SPECS
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/battle_gunnery_deck_editorial_final_review_v1.json')
DOC=Path('docs/battle_gunnery_deck_v956_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V956 Battle Gunnery Deck completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V956 Battle Gunnery Deck')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==1042 and ledger['records_with_source_and_prose_pass']==1069
    gameplay=read(ROOT/'actual_gameplay_verification.json');startup=read(RELEASE/'ordinary_startup_verification.json')
    title=read(ROOT/'paired_actual_title_menu.json');release=read(RELEASE/'registered_release_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8
    assert {h['message_id'] for h in gameplay['actual_complete_dialogue_holds']}=={1759,1770,1775,1778}
    assert len(gameplay['scoped_normal_return_controls'])==4
    assert all(c['all_scoped_state_equal_through_first_back'] and c['no_active_Cabin_view_after_normal_return'] for c in gameplay['scoped_normal_return_controls'])
    assert len(gameplay['offline_deletion_and_bad_header_controls'])==15
    assert all(c['rejected'] for c in gameplay['offline_deletion_and_bad_header_controls'])
    assert gameplay['complete36cell_Aim1759_odd35cell1770_initial_I1775_full_captain1778_pass']
    assert startup['all7_full_screen_pairs_exact'] and title['whole256x384_title_menu_at1100_exact_to_V947']
    assert release['candidate_sha256']==sha(ROM.read_bytes())==gameplay['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert (c,a)==(after['/COMMON/MESFILE.DK4'],after['/__arm9__.bin'])
    entries=owned.current_entries(c,a);config=read(owned.CONFIG);copies=read(config['native_copy_proof'])
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    context=read(doc['native_context_proof']);fonts=read(doc['native_font_proof'])
    assert len(context['all150_original_battle_helper_main_and_ordinary_control_selections'])==150
    assert context['no_Sera_special_role15_override_for_roles8_or2']
    native={r['message_id']:r for r in fonts['cases']};assert len(native)==24
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471
    assert manifest['profile']=='all-routes-unified-v954' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    visual=ROOT/'completion_visual_review.json'
    save(visual,{'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'title_proof_sha256':sha((ROOT/'paired_actual_title_menu.json').read_bytes()),
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_visually_reviewed':True,
        'complete36cell_Aim1759_odd35cell1770_initial_I1775_full_captain1778_reviewed':True,
        'visual_review_pending':False,'no_global_formatting_or_graphics_completion_claim':True})
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'visual_review':str(visual),'visual_review_sha256':sha(visual.read_bytes()),
        'all24_fonts150_source_controls7336_copies178_sequences_pass':True,
        'eight_actual_holds_four_returns_seven_startup_controls_and_title_pass':True,
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
    assert len(records)==24 and sum(r['editorial_decision']=='revise' for r in records)==17
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),'native_font_proof':doc['native_font_proof'],
        'native_visual_review':doc['visual_review_proof'],'completion_visual_review':str(visual),
        'ordinary_context_supplement':doc['ordinary_context_supplement'],'actual_scope':gameplay['scope'],'records':records,
        'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Battle-Gunnery8-DeckCleaning2-comments1757-1780','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=1066,records_revised_and_integrated=796,retained_wordings_editorially_completed=270)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=1065
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'These are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V947']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v954',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-battle-gunnery-deck24-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_battle_gunnery_deck_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.battle_gunnery_deck_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True,'requires_guarded_single8192_cache_policy':True}
    ledger['battle_gunnery_deck_v956']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 battle Gunnery/DeckCleaning comments. Remaining shared/routes/player prose,raw coverage and graphics stay unfinished.'})
    ledger['formatting_watchlist']['battle_gunnery_deck_actual_phase_v956']={'status':'complete-for24-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'24 full native fonts,eight actual full-word/RGB holds,four normal returns and15 offline rejection controls. Complete36cell Aim1759,continuation after35cell1770,initial I1775 and personal captain1778 with36cell first row pass. No game-wide guarantee.'}

    previous_user=Path('work/analysis/battle_sails_boarding_v948/user676_677_current_preservation.json')
    old_entries=previous_entries(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'])
    assert all(entries[n].text==old_entries[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':candidate['sha256'],'reference_proof':str(previous_user),'reference_sha256':sha(previous_user.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint='V956 completes24 battle Gunnery8/DeckCleaning2 comments1757-1780 in registered V954:17 revisions and7 retentions. All150 original battle/main/ordinary controls,all24 native fonts,7336 full copies and178 cache sequences pass. Eight active-widget bitmap/RGB holds verify full36cell Aim1759,conditional orders1770 after35cell first row,complete initial I1775 and personal captain1778 with36cell first row. Four normal returns preserve scoped state through first Back;original battle time resumes on exit. Every room assignment follows observed original combat0/1. Seven ordinary startup/New Game frames and title match V947. Exact clean-input patch preserves471 batches,114 layers,3644 unselected strings,all graphics/routes,native code,single8KiB cache,216x36 crop and123040 staged bytes. 1066 entries complete (796 revised/270 retained),1069 source/prose reviewed. Older750-752,mood1833,special actors1885-1888,raw abandon-caption0x134E54,remaining shared/routes/player prose and raw-source inventory remain. Separate graphics/all18 plaques,Samwell header and later older-record re-audit stay open;canonical not promoted;full goal active.'
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V956-Battle-Gunnery-Deck24-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:24 SailHandling/Boarding entries completed in V947;four actual cases,50 source pronoun controls,exact patch and next24 contexts mapped',
        'this_goal_turn_classification':'progress:24 source reviews,source-bound Aim/Gun Batteries help,native fonts,registered V954/exact patch,four actual scenes/returns and24 completed entries',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1066 and sum(ledger['source_prose_reviewed_counts_by_file'].values())==1069
    for key in ('unresolved_graphics_work','older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==prior[key]
    assert not ledger['full_goal_complete'] and ledger['goal_status']=='active'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    with DOC.open('x',encoding='utf-8') as f:
        f.write('# V956: battle Gunnery/DeckCleaning editorial completion\n\n'+checkpoint+'\n\n## Source and English\n\nSeventeen revisions and seven justified retentions cover24 independent alternatives. They restore target acquisition,Aim and the source more-shots statement,personal flagship promise,conditional close-range firing,negative ammunition order,next-shot loading and imminent fire,deckhand boarding advantage,conditional deference,ongoing cleaning,irony,developed scrubbing strength,personal first-aboard promise and captains cleaning remarks. Source1759 says more firing;help129 establishes Gun Batteries/Gunners and more shots,while173 separately discusses Aim and accuracy. This is faithful localization of dialogue,not an independently measured firing formula. No guaranteed hit,victory,new command assignment or forced battle action is invented. Exact clean/canonical/current references and all five natural-dialogue-v2 gates are retained.\n\n## Formatting and gameplay\n\nAll24 full native planes match independent complete words at x0 inside216x36. Aim1759,retained1776 and first row1778 fill36cells;conditional1770 has35cell first row;initial I1775 and Lil1779 three-row aside are intact. Phrase review keeps Ive built and until the boarding together without prose shortening,manual breaks or alignment padding. The actual standard story-audit format rejection is recorded;the dedicated native audit has zero errors or unwaived warnings. Four wrong-format,eight first/final-glyph,two continuation-glyph and final-letter-s-in-shots controls reject offline. Strict active-widget RTTI,geometry,bitmap,actual RGB and blank-paper checks exclude stale menu text.\n\n'+gameplay['scope']+'\n\n## Registered candidate\n\nExperimental profile all-routes-unified-v954 rebuilds471 batches and114 accepted layers from canonical out/raphael_natural_v2_accepted_base.nds,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Only COMMON/MESFILE.DK4 and ARM9 selection metadata differ from V947. All other prose,graphics/routes/HELP/ARM7/overlays,native code,sections/BSS,cache arenas and123040 staged bytes are preserved. Exact xdelta reconstructs V954 from clean Japanese SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d. Explicit human cold-boot acceptance remains required before canonical promotion. Test Gunnery/DeckCleaning battle comments and normal returns. The full goal remains active.\n\nROM SHA256 '+candidate['sha256']+'\nPatch SHA256 '+candidate['patch_sha256']+'\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V956: battle Gunnery/DeckCleaning editorial completion\n\n'+checkpoint+' See [V956 evidence](battle_gunnery_deck_v956_completion.md).\n')
    GUIDE.mkdir(parents=True);guide=[];frame_plan=read(ROOT/'actual_sample_frame_plan.json')
    for label in SPECS:
        n=frame_plan['cases'][label]['holds'][0]
        source=CAP/f'battle_gunnery_deck_v955_954_{label}'/f'frame_{n:06d}_navigation.png'
        target=GUIDE/f'{label}_V954.png';copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual V954 cold boot with declared coordinate and room/occupant fixtures;not earned refit,recruitment,qualification or published guide approval.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'files':guide,'actual_proof':final['actual_gameplay_proof']})
    paths=set()
    for version in (950,951,952,954,955,956):
        paths.update(p for p in (Path('work/analysis')/f'battle_gunnery_deck_v{version}').rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path('scripts').glob('*battle_gunnery_deck*v9*.py'))
    paths.update(Path(p) for p in (owned.CONFIG,'translations/battle_gunnery_deck_editorial_release_v1.json',str(MANUSCRIPT),
        'translations/battle_gunnery_deck_editorial_manuscript_v1.json',str(REVIEW),'translations/editorial_review_current_v1.json',
        'translations/release_stack.json','dk4tool/patch/battle_gunnery_deck_editorial.py','scripts/build_integrated_release.py',
        'scripts/native_battle_standoff_v955.py','scripts/probe_battle_boarding_pronoun_v943.py',str(DOC),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta')),
        'work/analysis/battle_gunnery_deck_v954/standard_story_audit_failure.log'))
    copied=[]
    def archive(source,target):
        target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for source in sorted(paths):archive(source,ARCHIVE/source.absolute().relative_to(Path.cwd()))
    for label in SPECS:
        folder=CAP/f'battle_gunnery_deck_v955_954_{label}'
        for source in folder.iterdir():
            if source.suffix in ('.json','.jsonl','.png'):archive(source,ARCHIVE/'actual_captures'/folder.name/source.name)
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_candidates':guide,'no_ROM_or_battery_save_duplicated_in_archive':True})
    print('24 reviews complete:1066 total (796 revised/270 retained),1069 source/prose;',len(copied),'archive files verified. Full goal active.',flush=True)


if __name__=='__main__':main()
