"""Complete13 cooking entries only after native,release,startup and actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import cooking_comments_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_cooking_release_v850 import MANUSCRIPT,OLD
from scripts.verify_cooking_gameplay_v851 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.work_comments_layout_v843 import layout
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/cooking_comments_editorial_final_review_v1.json')
DOC=Path('docs/cooking_comments_v851_completion.md')
RELEASE_ROOT=Path('work/analysis/cooking_comments_v850')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V851 Cooking comments completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V851 Cooking comments')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==695 and ledger['records_with_source_and_prose_pass']==711
    validate_natural_dialogue_batch(doc)
    gameplay=read(ROOT/'actual_gameplay_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={1411,1416,1419,1422}
    assert len(gameplay['scoped_normal_return_state_controls'])==4
    assert all(r['all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal'] and r['actual_captain32_byte_object_equal'] for r in gameplay['scoped_normal_return_state_controls'])
    assert sha(ROM.read_bytes())==gameplay['candidate_sha256']
    assert sha(Path(gameplay['review_sheet']).read_bytes())==gameplay['review_sheet_sha256']
    assert sha(Path(gameplay['return_review_sheet']).read_bytes())==gameplay['return_review_sheet_sha256']
    gameplay.update(visual_review_pending=False,visual_review={
        'all8_actual_holds_in_sheet_opened_and_read':True,'four_normal_town_returns_opened':True,
        'Emilio_and_Joakim_odd19_character_rows_complete_Huh_and_this_continuations_at_x16':True,
        'Sera_special1422_and_distinct_correct_portrait_header_read':True,
        'all_sampled_leading_trailing_letters_punctuation_and_native_paper_bounds_read':True,
        'fixtures_not_earned_recruitment_refit_or_qualification':True})
    save(ROOT/'actual_gameplay_verification.json',gameplay)
    startup=read(RELEASE_ROOT/'ordinary_startup_verification.json')
    assert startup['candidate_sha256']==gameplay['candidate_sha256'] and startup['all7_full_screen_pairs_exact']
    startup.update(visual_review_pending=False,visual_review='Seven ordinary whole native startup/New Game captures opened;character selection,confirmation and opening portrait/text remain intact. No complete route or hardware claim.')
    save(RELEASE_ROOT/'ordinary_startup_verification.json',startup)
    fonts=read('work/analysis/cooking_comments_v849/native_font_proof.json')
    visual=read('work/analysis/cooking_comments_v849/visual_review.json')
    assert len(fonts['cases'])==13 and not visual['visual_review_pending'] and visual['all13_previews_visually_reviewed']
    context=read('work/analysis/cooking_comments_v847/source_context_packet.json')
    assert len(context['all25_original_role_helper_selections'])==25
    assert {r['selected_message_ID'] for r in context['all25_original_role_helper_selections']}==set(owned.IDS)
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']
    entries=owned.current_entries(c,a);copies=read(RELEASE_ROOT/'native_copy_proof.json')
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies'])==3668
    release=read(RELEASE_ROOT/'registered_release_verification.json')
    assert release['candidate_sha256']==sha(ROM.read_bytes())==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']==release['clean_input_sha256']
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471 and manifest['profile']=='all-routes-unified-v850'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE_ROOT/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'all13_complete_native_fonts_25_source_selectors_7336_copies_7_startup_controls_pass':True,
        'eight_complete_actual_holds_four_normal_returns_and_all_fixture_replays_pass':True,
        'Sera_extra_native_branch_included_not_lost_to_twelve_slot_inventory':True,
        'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_accepted_layers_routes_graphics_and_fixed123040_staged_bytes_preserved':True,
        'fresh_stage_replay_matches_complete_target_no_native_code_or_crop_change':True,
        'canonical_not_promoted':True,'full_goal_complete':False})
    save(ROOT/'editorial_ledger_before_completion.json',ledger)
    existing={n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])}
    assert not existing.intersection(owned.IDS)
    native={r['message_id']:r for r in fonts['cases']};records=[]
    for row in doc['records']:
        n=row['message_id'];assert entries[n].text==owned.compiled(row) and native[n]['text_hex']==entries[n].text.hex()
        records.append({**deepcopy(row),'completed_candidate_reference':str(ROM),'before_reference':row['current_reference'],
            'before_text_hex':row['current_text_hex'],'current_reference':reference(entries[n]),'current_text_hex':entries[n].text.hex(),
            'decision':'revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            'generated_native_lines':layout(row['english']),'native_font_canvas_sha256':native[n]['canvas_sha256'],
            'actual_display_holds':[r for r in gameplay['actual_complete_dialogue_holds'] if r['message_id']==n],
            'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True,
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True})
    assert sum(r['editorial_decision']=='revise' for r in records)==10
    final={'format':'dk4-editorial-family-final-review-v1','status':'13-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_font_proof':'work/analysis/cooking_comments_v849/native_font_proof.json',
        'native_visual_review':'work/analysis/cooking_comments_v849/visual_review.json',
        'actual_scope':gameplay['scope'],'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Cook15-comments1410-1422-including-Sera','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=708,records_revised_and_integrated=516,retained_wordings_editorially_completed=192)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=707
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],
        'status':'three-older-context-unmapped-drafts',
        'note':'Cooking13 completes in V850 with V851 actual verification. These three reviewed drafts are not the full remaining scope;all unreviewed shared/route/player prose and raw-source coverage remain.'}
    ledger['previous_current_integrated_candidate_V845']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v850',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),
        'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-cooking13-editorially-native-and-representative-gameplay-verified','details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_cooking_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.cooking_comments_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True}
    ledger['cooking_comments_v851']={'status':final['status'],'completed_entries_added':13,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'13 independent Cook15 bodies,including Sera. Other shared prose,routes,player-facing prose,raw-source coverage and graphics remain unfinished.'})
    ledger['coverage_units'][0]['next']='Review Livestock17 and Chapel18 comments,then all other untouched shared dialogue. Resolve older750-752 consumer context and cover all route scenes and remaining player-facing prose with raw native-source inventory. Graphics remains separate.'
    ledger['formatting_watchlist']['cooking_actual_phase_v851']={'status':'complete-for13-cooking-comments-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All13 complete native fonts;two actual19-character first rows with full aligned Huh/this continuations;four normal returns. Sera special branch included. No game-wide formatting guarantee.'}
    user_path=Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    for row in read(user_path)['candidates'][-1]['entries']:assert entries[row['id']].text.hex()==row['template_hex']
    user_proof=ROOT/'user676_677_current_preservation.json'
    save(user_proof,{'candidate_sha256':candidate['sha256'],'reference_proof':str(user_path),'reference_sha256':sha(user_path.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'native_renderer_code_unchanged_from_V845':True,
        'new_shop_scene_activation_not_claimed':True,'global_indents_gaps_fragments_complete_letters_bounds_and_pagination_watch_stays_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user_proof),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V851 completes13 Cook15 comments1410-1422 in registered V850:10 revisions and3 retentions. '
        'All25 original role-helper selections include the special Sera1422 branch and four actual captains;all13 full native font planes and7336 warm/cold message copies pass. '
        'Eight actual complete bitmap/RGB holds verify Gerhard1411,Emilio1416,real Joakim1419 andSera1422. Both19-character first rows retain complete Huh/this continuations at x16;four normal cancels/town returns preserve scoped funds,calendar,31 assignments,owned companions,actual captain and ship models. '
        'Each fresh disposable Copenhagen run uses only2/3 declared Cook15 room-type/occupant bytes;Emilio/Sera faction21 is preserved,no earned recruitment/refit/qualification claim. '
        'Seven ordinary cold-boot/New Game whole frames match V845. V850 and its exact clean-input patch preserve471 batches,114 accepted layers,3655 other COMMON strings,all routes/graphics/scripts/HELP/ARM7/overlays,native code,existing216x36 crop and123040 staged bytes. '
        '708 entries complete (516 revised/192 retained),711 source/prose reviewed;three older750-752 drafts and all unreviewed shared/route/player prose/raw-source coverage remain. '
        'Graphics/all18 plaques,Samwell name lead and later older-record re-audit stay open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V851-Cooking13-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':13,
        'previous_goal_turn_classification':'progress:Work24 completed and Cooking13 source selectors mapped',
        'this_goal_turn_classification':'progress:13 source reviews,registered integrated release,exact patch,13 complete fonts,eight actual holds,four returns and13-entry completion',
        'full_goal_complete':False})
    old=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==708
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==711
    assert ledger['unresolved_graphics_work']==old['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==old['older_record_reaudit_after_full_editorial_goal']
    assert not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V851: cooking editorial completion in V850\n\n'+checkpoint+'\n\n'
        '## Source and prose\n\n'
        'The clean source has eight ordinary NPC voices,four protagonist variants,and Sera\'s separate actor24 branch. Storage neighbors are alternatives,not a spoken conversation. '
        'Revisions restore choosing a dish,the salt/sugar realization,the tasting joke,the male-cooking self-challenge,Joakim\'s past cooking during his apprenticeship,Lil\'s complaint,Maria\'s tentative fried rice and Sera\'s simple general observation. '
        'No new dish,occupation,rank,recipient or inventory change is invented. The older-sounding description in1415\'s source gloss denotes the Japanese speech register;no actor age is established. '
        'Retain1410,1417,1418 as faithful,natural wording. Every line is authored as one paragraph;the established36-cell planner generates all breaks and invisible pre-LF parity spaces. '
        'The inherited native-probe console says All24,while its13 cases,13 PNGs,all13 proof key and review sheet correctly cover13 entries;the separate visual review records this count-label erratum.\n\n'
        '## Actual verification scope\n\n'+gameplay['scope']+'\n\n'
        'Original CDeckCabinInfoView and CDeckPersonnelView are identified by RTTI and geometry,without text matching. Independent full252x36 native word planes and whole216x36 visible ink/blank RGB regions match at x16,y112 for every sampled hold. '
        'The original parent projection preserves frame,palette and all other drawing commands. The room fixture re-purposes an empty visible Cabin to Cook15 with only its type and occupant fields changed. '
        'The donor already contains a disclosed isolated five-ship Copenhagen fleet;this does not prove earned travel,fleet acquisition,refitting or recruitment. All original and disposable source saves remain exact.\n\n'
        '## Registered release\n\n'
        f'- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n'
        f'- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `{manifest["base_sha256"]}`.\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256 `{candidate["patch_sha256"]}`.\n'
        f'- Clean input SHA-256: `{release["clean_input_sha256"]}`.\n'
        f'- Final review: `{REVIEW}`;closure: `{closure}`.\n\n'
        'Only COMMON and native ARM9 selection metadata differ from V845;no renderer,code,crop,section,BSS,arena or staged payload grows. '
        'Complete471-batch/114-layer inheritance,all other text/components,negative source/control guards and exact patch reconstruction pass. '
        'Automatic review rejected an earlier preparation command as a possible in-place edit of the completed work module;it did not execute. Explicit new cooking files resolved it,and the frozen work module hash is unchanged. '
        'Human cold-boot acceptance is required before canonical promotion;test title/New Game and the changed Cook15 scenes on the user\'s setup. '
        'Repaired shop676/677 remains exact;no fresh shop activation is claimed. Four actual native guide-candidate PNGs retain fixture provenance. '
        'The full editorial goal,global formatting watch,raw-source inventory,separate graphics/all18 plaques and later older-record revisit remain unfinished.\n',encoding='utf-8')
    for path in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## V851: cooking editorial completion\n\n'+checkpoint+' See [V851 evidence](cooking_comments_v851_completion.md).\n')
    GUIDE.mkdir(parents=True);guides=[]
    for label,number in CASES.items():
        source=CAP/f'cooking_comments_v851_850_{label}/frame_004200_navigation.png';target=GUIDE/f'{label}_ID{number}_V850.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual cold-boot framebuffer with disclosed2/3-byte isolated Cook15 assignment;not earned refit or recruitment.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'guide_candidates':guides,'not_unqualified_ordinary_progression_screenshots':True})
    sources={p for v in (847,848,849,850,851) for p in Path(f'work/analysis/cooking_comments_v{v}').glob('*') if p.is_file() and p.suffix!='.nds'}
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,
        'translations/cooking_comments_editorial_manuscript_v1.json','translations/release_stack.json','translations/rom_retention_pins.json',
        'scripts/prepare_cooking_context_v847.py','scripts/prepare_cooking_prose_v848.py','scripts/probe_cooking_fonts_v849.py',
        'dk4tool/patch/cooking_comments_editorial.py','scripts/prepare_cooking_release_v850.py','scripts/verify_cooking_release_v850.py',
        'scripts/run_cooking_startup_v850.py','scripts/verify_cooking_startup_v850.py',
        'scripts/native_cook_room_fixture_v851.py','scripts/run_cook_room_adapter_v851.py',
        'scripts/run_cooking_comments_v851.py','scripts/verify_cooking_gameplay_v851.py','scripts/record_cooking_completion_v851.py',
        'scripts/build_integrated_release.py','docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    sources.update(map(Path,read(owned.CONFIG)['dependencies']));sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for label in CASES:
        folder=f'cooking_comments_v851_850_{label}'
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name;target=ARCHIVE/'captures'/folder/name;target.parent.mkdir(parents=True,exist_ok=True)
            copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
            archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'all_ROMs_captures_and_generated_artifacts_on_E':True,'full_goal_complete':False})
    print('Cooking13 complete:708 total,516 revised,192 retained;711 source/prose reviewed. Full goal and separate graphics audit remain open.',flush=True)


if __name__=='__main__':main()
