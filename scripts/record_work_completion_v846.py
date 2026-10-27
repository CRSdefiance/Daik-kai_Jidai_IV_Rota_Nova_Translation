"""Close24 source-reviewed work comments after complete native and sampled actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import work_comments_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_work_release_v845 import MANUSCRIPT,OLD
from scripts.verify_work_gameplay_v846 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.work_comments_layout_v843 import layout
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/work_comments_editorial_final_review_v1.json')
DOC=Path('docs/work_comments_v846_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V846 Shipwright and Doctor completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V846 Shipwright and Doctor')
RELEASE_ROOT=Path('work/analysis/work_comments_v845')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==671 and ledger['records_with_source_and_prose_pass']==698
    validate_natural_dialogue_batch(doc)
    gameplay=read(ROOT/'actual_gameplay_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={1387,1395,1398,1405}
    assert len(gameplay['scoped_normal_return_state_controls'])==4
    assert all(r['all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal'] and r['actual_captain32_byte_object_equal'] for r in gameplay['scoped_normal_return_state_controls'])
    assert gameplay['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(gameplay['review_sheet']).read_bytes())==gameplay['review_sheet_sha256']
    gameplay.update(visual_review_pending=False,visual_review={
        'all8_actual_holds_in_sheet_opened_and_read':True,'four_normal_town_returns_opened':True,
        'complete_first_I_and_odd19_character_line_then_I_continuation_at_x16':True,
        'Manuel_full36_character_row_and_final_period_visible':True,
        'real_Hodram_work_comment_and_correct_portrait_visible':True,
        'fixtures_not_earned_refit_or_recruitment':True})
    save(ROOT/'actual_gameplay_verification.json',gameplay)
    startup=read(RELEASE_ROOT/'ordinary_startup_verification.json')
    assert startup['candidate_sha256']==gameplay['candidate_sha256'] and startup['all7_full_screen_pairs_exact']
    startup.update(visual_review_pending=False,visual_review='Seven whole native startup/New Game captures opened;character selection,confirmation and opening portrait/text remain intact. No ordinary full-route playthrough claim.')
    save(RELEASE_ROOT/'ordinary_startup_verification.json',startup)
    fonts=read('work/analysis/work_comments_v843/native_font_proof.json')
    visual=read('work/analysis/work_comments_v844/visual_review.json')
    assert len(fonts['cases'])==24 and not visual['visual_review_pending'] and visual['all24_previews_visually_reviewed']
    context=read('work/analysis/work_comments_v842/native_context.json')
    assert len(context['all42_NPC_voice_selections_cover_all_eight_classes'])==42 and len(context['all8_real_protagonist_group_selections'])==8
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']
    entries=owned.current_entries(c,a)
    copies=read(RELEASE_ROOT/'native_copy_proof.json')
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies'])==3668
    release=read(RELEASE_ROOT/'registered_release_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']==release['clean_input_sha256']
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471 and manifest['profile']=='all-routes-unified-v845'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE_ROOT/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'all24_complete_native_fonts_50_source_selections_7336_copies_7_startup_controls_pass':True,
        'eight_complete_actual_holds_four_normal_returns_and_fixtures_pass':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_accepted_layers_routes_graphics_and_fixed123040_staged_bytes_preserved':True,
        'fresh_stage_replay_matches_complete_target':True,'no_native_code_or_crop_change':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(owned.IDS)
    native={r['message_id']:r for r in fonts['cases']}
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row) and native[n]['text_hex']==entries[n].text.hex()
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),
            'before_reference':row['current_reference'],'before_text_hex':row['current_text_hex'],
            'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),'native_font_canvas_sha256':native[n]['canvas_sha256'],
            'actual_display_holds':[r for r in gameplay['actual_complete_dialogue_holds'] if r['message_id']==n],
            'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True,
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True})
    assert sum(r['editorial_decision']=='revise' for r in records)==21
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_font_proof':'work/analysis/work_comments_v843/native_font_proof.json',
        'native_visual_review':'work/analysis/work_comments_v844/visual_review.json','actual_scope':gameplay['scope'],
        'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Shipwright-and-Doctor-work-comments1386-1409','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=695,records_revised_and_integrated=506,retained_wordings_editorially_completed=189)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=694
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts',
        'note':'Work24 completes in V845 with V846 actual verification. These three reviewed drafts are not the full remaining scope;all unreviewed shared/route/player prose and raw-source coverage remain.'}
    ledger['previous_current_integrated_candidate_V838']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v845',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),
        'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-work24-editorially-native-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_work_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.work_comments_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True}
    ledger['work_comments_v846']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 work-comment bodies;other shared prose,routes,player-facing prose,raw-source coverage and graphics remain unfinished.'})
    ledger['coverage_units'][0]['next']='Continue untouched shared working/cooking and other dialogue;resolve older750-752 consumer context,then all route scenes and remaining player-facing prose with raw native-source inventory. Graphics audit stays separate.'
    ledger['formatting_watchlist']['work_comment_actual_phase_v846']={'status':'complete-for24-work-comments-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All24 native complete fonts;actual19-character first row with complete aligned I continuation;actual36-character row with trailing period;four normal returns. No game-wide formatting guarantee claimed.'}
    prior_user=Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    user_rows=read(prior_user)['candidates'][-1]['entries']
    for row in user_rows:assert entries[row['id']].text.hex()==row['template_hex']
    user_proof=ROOT/'user676_677_current_preservation.json'
    save(user_proof,{'candidate_sha256':release['candidate_sha256'],'reference_proof':str(prior_user),
        'reference_sha256':sha(prior_user.read_bytes()),'exact_repaired676_677_bytes_preserved':True,
        'native_renderer_code_unchanged_from_V838':True,'new_shop_scene_activation_not_claimed':True,
        'global_indents_gaps_fragments_complete_letters_bounds_and_pagination_watch_stays_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user_proof),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V846 completes24 Shipwright/Doctor work comments1386-1409 in registered V845:21 revisions and3 retentions. '
        'Fifty original role/voice/current-protagonist helper selections,all24 complete native font planes and7336 warm/cold message copies pass. '
        'Eight actual complete bitmap/RGB holds verify Gerhard1387,real Hodram1395,Janus1398 andManuel1405,including an odd19-character first row with full aligned I continuation and a complete36-cell row with final period. '
        'Each fresh disposable Copenhagen run uses only2/3 declared room-type/occupant bytes;Janus faction21 is preserved with no recruitment claim. Four normal cancels/town returns preserve scoped funds,calendar,31 roles,owned companions,actual captain and ship models. '
        'Seven ordinary cold-boot/New Game whole frames match V838. Registered combined V845 and exact clean-input patch retain471 batches,114 accepted layers,3644 other COMMON strings,all graphics/routes/scripts/HELP/ARM7/overlays,native code,existing216x36 crop and fixed123040 staged bytes. '
        '695 entries complete (506 revised/189 retained),698 source/prose reviewed;three older750-752 reviewed drafts and all unreviewed shared/route/player prose/raw-source work remain. '
        'Graphics/all18 plaques,Samwell middle-name glyph and later older-record re-audit stay open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V846-Shipwright-Doctor-comments-complete','documentation':str(DOC),
        'proof':str(closure),'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:source review and native formatting research',
        'this_goal_turn_classification':'progress:registered integrated release,exact patch,all24 native fonts,eight actual holds,four returns and24-entry completion',
        'full_goal_complete':False})
    old=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==695
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==698
    assert ledger['unresolved_graphics_work']==old['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==old['older_record_reaudit_after_full_editorial_goal']
    assert not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V846: Shipwright and Doctor editorial completion in V845\n\n'+checkpoint+'\n\n'
        '## Source and natural English\n\n'
        'The clean Japanese selects eight NPC voice classes and four actual protagonists per duty. Source context is50 original helper calls,not50 game visits. '
        'Revisions preserve preparation,ongoing work,quality,uncertainty,medicine and references to Claudio and Xien. Native actor10 first-name getter establishes Xien,correcting older Xian without renaming him. '
        'V2 uses source-comma punctuation in1405 without shortening its words. The formatter generates all breaks,retains technical phrases where possible,and adds only the proven invisible pre-LF parity space. '
        'V3 uses the required production review-gate list;the initial schema rejection is retained as a diagnostic. No validator or source lock was relaxed.\n\n'
        '## Actual verification scope\n\n'+gameplay['scope']+'\n\n'
        'The source body is CDeckCabinInfoView and parent CDeckPersonnelView,identified without matching expected text. Each sampled hold matches the independent full252x36 native word plane and whole216x36 visible ink/blank RGB region at x16,y112. '
        'The existing216x36 crop,paper frame,palette and other parent drawing commands remain exact. Room12 is an originally empty visible Cabin;fixtures change its type and assignment only. '
        'The old donor already contains a disclosed isolated five-ship Copenhagen fleet;this is not earned travel,refitting,recruitment or progression. '
        'Initial harness prelaunch failures from pruned dependencies and a closed stdin produced no display credit. Retained patches restore exact source dependencies;fresh recorded-input folders hold the successful runs.\n\n'
        '## Release\n\n'
        f'- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n'
        f'- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `{manifest["base_sha256"]}`.\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256 `{candidate["patch_sha256"]}`.\n'
        f'- Clean input SHA-256: `{release["clean_input_sha256"]}`.\n'
        f'- Final review: `{REVIEW}`;closure: `{closure}`.\n\n'
        'Only COMMON and native ARM9 message-selection metadata differ from V838. All other ROM components and allocations are exact. '
        'Human cold-boot acceptance is required before canonical promotion. Four raw native guide-candidate PNGs retain fixture provenance. '
        'Repaired shop676/677 is byte-exact;the earlier actual shop capture remains the display reference,and no fresh shop activation is claimed. '
        'The full editorial goal,global formatting watch,raw-source inventory,separate graphics/all18 plaques and older-record revisit remain unfinished.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V846: Shipwright and Doctor editorial completion\n\n'+checkpoint+' See [V846 evidence](work_comments_v846_completion.md).\n')
    GUIDE.mkdir(parents=True)
    guides=[]
    for label,number in CASES.items():
        source=CAP/f'work_comments_v846_845_{label}_scheduled/frame_004200_navigation.png';target=GUIDE/f'{label}_ID{number}_V845.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual cold-boot framebuffer with disclosed2/3-byte isolated room assignment;no earned refit or recruitment claim.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'guide_candidates':guides,'not_unqualified_ordinary_progression_screenshots':True})
    sources={p for v in (842,843,844,845,846) for p in Path(f'work/analysis/work_comments_v{v}').glob('*') if p.is_file() and p.suffix!='.nds'}
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,
        'translations/work_comments_editorial_manuscript_v1.json','translations/work_comments_editorial_manuscript_v2.json',
        'translations/release_stack.json','translations/rom_retention_pins.json','scripts/prepare_work_comments_v842.py',
        'scripts/record_work_source_v842.py','scripts/work_comments_layout_v843.py','scripts/probe_work_fonts_v843.py',
        'dk4tool/patch/work_comments_editorial.py','scripts/prepare_work_release_v845.py','scripts/verify_work_release_v845.py',
        'scripts/run_work_startup_v845.py','scripts/native_work_room_fixture_v846.py','scripts/run_work_room_adapter_v846.py',
        'scripts/run_work_comments_v846.py','scripts/verify_work_gameplay_v846.py','scripts/record_work_completion_v846.py',
        'scripts/build_integrated_release.py','docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    sources.update(map(Path,read(owned.CONFIG)['dependencies']));sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for label in CASES:
        folder=f'work_comments_v846_845_{label}_scheduled'
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name;target=ARCHIVE/'captures'/folder/name;target.parent.mkdir(parents=True,exist_ok=True)
            copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
            archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'all_ROMs_captures_and_generated_artifacts_on_E':True,'full_goal_complete':False})
    print('Work24 complete:695 total,506 revised,189 retained;698 source/prose reviewed. Full goal and separate graphics audit remain open.',flush=True)


if __name__=='__main__':main()
