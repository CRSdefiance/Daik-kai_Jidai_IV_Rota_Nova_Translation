"""Close24 role17/18 comments after source,native,release and actual gates."""

from copy import deepcopy
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import livestock_prayer_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.livestock_prayer_layout_v854 import layout
from scripts.prepare_livestock_prayer_release_v855 import MANUSCRIPT,OLD
from scripts.verify_livestock_prayer_gameplay_v856 import ROOT,ROM,CAP,CASES
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read,save

LEDGER=Path('translations/editorial_review_current_v1.json')
REVIEW=Path('translations/livestock_prayer_editorial_final_review_v1.json')
DOC=Path('docs/livestock_prayer_v856_completion.md')
RELEASE_ROOT=Path('work/analysis/livestock_prayer_v855')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V856 Livestock and prayer completion')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V856 Livestock and prayer')


def reference(e):
    return {k:getattr(e,k) for k in ('message_id','block','table_offset','block_offset','copy_end','record_index','start','end')}


def main():
    assert not REVIEW.exists() and not DOC.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    ledger,doc=read(LEDGER),read(MANUSCRIPT)
    assert ledger['records_editorially_completed']==708 and ledger['records_with_source_and_prose_pass']==735
    validate_natural_dialogue_batch(doc)
    gameplay=read(ROOT/'actual_gameplay_verification.json')
    assert len(gameplay['actual_complete_dialogue_holds'])==8
    assert {r['message_id'] for r in gameplay['actual_complete_dialogue_holds']}=={1428,1435,1441,1444}
    assert gameplay['actual_three_row_invocation_with_odd15_middle_row_and_complete_third_row_pass']
    assert len(gameplay['scoped_normal_return_state_controls'])==4
    assert all(r['all_scoped_funds_calendar_assignments_owned_actor_ship_Hull_Crew_equal'] and r['actual_captain32_byte_object_equal'] for r in gameplay['scoped_normal_return_state_controls'])
    assert gameplay['candidate_sha256']==sha(ROM.read_bytes())
    assert sha(Path(gameplay['review_sheet']).read_bytes())==gameplay['review_sheet_sha256']
    assert sha(Path(gameplay['return_review_sheet']).read_bytes())==gameplay['return_review_sheet_sha256']
    gameplay.update(visual_review_pending=False,visual_review={'all8_actual_holds_opened_and_read':True,
        'four_normal_town_returns_opened':True,'full_invocation_Father_Son_Holy_Spirit_all_three_rows_read':True,
        'odd15_middle_row_then_complete_and_continuation_at_x16':True,
        'Bible_first_I_and_final_period_fleet_question_mark_and_livestock_attachment_read':True,
        'correct_portraits_and_declared_fixtures_no_earned_recruitment_claim':True})
    save(ROOT/'actual_gameplay_verification.json',gameplay)
    startup=read(RELEASE_ROOT/'ordinary_startup_verification.json')
    assert startup['candidate_sha256']==gameplay['candidate_sha256'] and startup['all7_full_screen_pairs_exact']
    startup.update(visual_review_pending=False,visual_review='Seven ordinary whole native startup/New Game controls opened;selection,confirmation and opening portrait/text intact. No full-route or hardware claim.')
    save(RELEASE_ROOT/'ordinary_startup_verification.json',startup)
    fonts=read('work/analysis/livestock_prayer_v854/native_font_proof.json')
    visual=read('work/analysis/livestock_prayer_v854/visual_review.json')
    context=read('work/analysis/livestock_prayer_v852/source_context_packet.json')
    assert len(fonts['cases'])==24 and fonts['full_invocation_has_three_automatically_generated_complete_rows']
    assert visual['all24_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert len(context['all50_original_role_helper_selections'])==50
    assert {r['selected_message_ID'] for r in context['all50_original_role_helper_selections']}==set(owned.IDS)
    before,after=map(files,map(NdsImage.open,(OLD,ROM)))
    assert before.keys()==after.keys() and {p for p in before if before[p]!=after[p]}=={'/COMMON/MESFILE.DK4','/__arm9__.bin'}
    c,a,stage=owned.apply_release(before['/COMMON/MESFILE.DK4'],before['/__arm9__.bin'],owned.CONFIG)
    assert c==after['/COMMON/MESFILE.DK4'] and a==after['/__arm9__.bin']
    entries=owned.current_entries(c,a)
    copies=read(RELEASE_ROOT/'native_copy_proof.json');release=read(RELEASE_ROOT/'registered_release_verification.json')
    assert len(copies['all3668_native_IDs_warm_and_cold7336_complete_copies'])==3668
    assert release['candidate_sha256']==sha(ROM.read_bytes())==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==doc['source_clean_ROM_sha256']==release['clean_input_sha256']
    registry,manifest=read('translations/release_stack.json'),read(ROM.with_suffix('.manifest.json'))
    assert len(registry['accepted_layers'])==114 and len(manifest['batches'])==471 and manifest['profile']=='all-routes-unified-v855'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256']==registry['canonical_baseline']['sha256']
    closure=ROOT/'registered_release_completion.json'
    save(closure,{'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],
        'registered_release_proof':str(RELEASE_ROOT/'registered_release_verification.json'),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'actual_gameplay_proof_sha256':sha((ROOT/'actual_gameplay_verification.json').read_bytes()),
        'all24_complete_native_fonts_50_source_selections_7336_copies_7_startup_controls_pass':True,
        'eight_actual_complete_holds_four_returns_and_fixture_replays_pass':True,
        'three_row_invocation_and_odd_middle_row_complete':True,'exact_clean_input_patch_reconstruction_fresh_hash_matches':True,
        'all471_batches114_layers_routes_graphics_and_fixed123040_staged_bytes_preserved':True,
        'fresh_late_stage_replay_exact_no_code_or_crop_change':True,'canonical_not_promoted':True,'full_goal_complete':False})
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
            'all_source_native_copy_font_and_visible_bounds_gates_pass':True,
            'individual_actual_visit_not_claimed_when_actual_holds_list_empty':True})
    assert sum(r['editorial_decision']=='revise' for r in records)==17
    final={'format':'dk4-editorial-family-final-review-v1','status':'24-source-context-editorial-native-and-representative-actual-verified',
        'candidate':str(ROM),'candidate_sha256':release['candidate_sha256'],'source_manuscript':str(MANUSCRIPT),
        'source_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),'registered_release_proof':str(closure),
        'actual_gameplay_proof':str(ROOT/'actual_gameplay_verification.json'),
        'native_font_proof':'work/analysis/livestock_prayer_v854/native_font_proof.json',
        'native_visual_review':'work/analysis/livestock_prayer_v854/visual_review.json','actual_scope':gameplay['scope'],
        'records':records,'full_editorial_goal_complete':False,'separate_graphics_goal_complete':False}
    save(REVIEW,final)
    family={'id':'Shared-Livestock17-Chapel18-comments1423-1446','native_message_IDs':list(owned.IDS),
        'records':records,'final_review':str(REVIEW),'documentation':str(DOC),'actual_verification_scope':gameplay['scope']}
    ledger['completed_editorial_families'].append(family)
    ledger.update(records_editorially_completed=732,records_revised_and_integrated=533,retained_wordings_editorially_completed=199)
    ledger['completed_editorial_record_counts_by_file']['/COMMON/MESFILE.DK4']=731
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in owned.IDS]
    assert ledger['reviewed_but_incomplete_COMMON_IDs']==[750,751,752]
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json'],'status':'three-older-context-unmapped-drafts',
        'note':'Livestock/Chapel24 completes in V855 with V856 actual verification. These three reviewed drafts are not the full remaining unreviewed shared/route/player prose or raw-source scope.'}
    ledger['previous_current_integrated_candidate_V850']=deepcopy(ledger['current_integrated_candidate'])
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v855',
        'MESFILE_sha256':sha(c),'ARM9_sha256':sha(a),'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'status':'experimental-livestock-prayer24-editorially-native-and-representative-gameplay-verified',
        'details':str(DOC),'full_goal_complete':False}
    ledger['current_integrated_candidate']=candidate;ledger['source_pins']['current']=deepcopy(candidate)
    ledger['next_integrated_profile_for_goal_continuation']=candidate['profile']
    ledger['native_relocation_reference_before_livestock_prayer_completion']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(ROM),'COMMON_sha256':sha(c),'ARM9_sha256':sha(a),
        'parser':'dk4tool.patch.livestock_prayer_editorial.current_entries','release_config':owned.CONFIG,
        'source_locked_directory_and_all_other_strings_preserved':True}
    ledger['livestock_prayer_v856']={'status':final['status'],'completed_entries_added':24,'native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'documentation':str(DOC),'proof':str(closure),'canonical_not_promoted':True}
    ledger['coverage_units'].append({'id':family['id'],'status':'completed','native_message_IDs':list(owned.IDS),
        'final_review':str(REVIEW),'scope':'24 role17/18 bodies. Other shared prose,all routes,player-facing prose,raw inventory and graphics stay unfinished.'})
    ledger['coverage_units'][0]['next']='Continue all untouched shared duty/town dialogue;resolve older750-752 context and review every route scene and remaining player-facing prose with raw native-source inventory. Graphics stays separate.'
    ledger['formatting_watchlist']['livestock_prayer_actual_phase_v856']={'status':'complete-for24-entries-global-formatting-audit-open',
        'proof':final['actual_gameplay_proof'],'checks':'All24 full native fonts;actual three-row invocation with15-character middle row,full third-row and/Holy Spirit text at x16,and four normal returns. No game-wide formatting guarantee.'}
    user_path=Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    for row in read(user_path)['candidates'][-1]['entries']:assert entries[row['id']].text.hex()==row['template_hex']
    user_proof=ROOT/'user676_677_current_preservation.json'
    save(user_proof,{'candidate_sha256':candidate['sha256'],'reference_proof':str(user_path),'reference_sha256':sha(user_path.read_bytes()),
        'exact_repaired676_677_bytes_preserved':True,'native_renderer_code_unchanged_from_V850':True,
        'new_shop_activation_not_claimed':True,'global_formatting_watch_still_open':True})
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={'proof':str(user_proof),'candidate':str(ROM),
        'exact_repaired676_677_bytes_preserved':True,'new_actual_shop_activation_claimed':False}
    checkpoint=('V856 completes24 Livestock17/Chapel18 comments1423-1446 in registered V855:17 revisions and7 retentions. '
        'Fifty original role selections,all24 complete native fonts and7336 warm/cold message copies pass. '
        'Eight actual complete bitmap/RGB holds verify Julio1428,Janus1435,Emilio1441 andreal Joakim1444. The full invocation uses three generated rows;its odd15-character middle row retains the complete third-row and/Holy Spirit text at x16. '
        'Four normal returns preserve scoped funds,calendar,31 assignments,owned actors,actual captain and ship models. Each fresh disposable Copenhagen run changes only2/3 room/occupant bytes;foreign faction21 is preserved,no earned recruitment/refit/qualification claim. '
        'Seven ordinary startup/New Game whole frames match V850. Registered V855 and exact clean-input patch preserve471 batches,114 layers,3644 other COMMON strings,all graphics/routes/scripts/HELP/ARM7/overlays,native code,216x36 crop and123040 staged bytes. '
        '732 entries complete (533 revised/199 retained),735 source/prose reviewed;older750-752 and all unreviewed shared/route/player prose/raw work remain. Graphics/all18 plaques,Samwell name lead and later older-record re-audit stay open;canonical not promoted;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V856-Livestock-Chapel24-complete','documentation':str(DOC),'proof':str(closure),
        'actual_proof':final['actual_gameplay_proof'],'completed_entries_added':24,
        'previous_goal_turn_classification':'progress:Cooking13 completed and next24 source selectors mapped',
        'this_goal_turn_classification':'progress:24 source reviews,new bounded word planner,registered release/exact patch,all24 full fonts,eight actual holds,four returns and24-entry completion',
        'full_goal_complete':False})
    prior=read(ROOT/'editorial_ledger_before_completion.json')
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==732
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==735
    assert ledger['unresolved_graphics_work']==prior['unresolved_graphics_work']
    assert ledger['older_record_reaudit_after_full_editorial_goal']==prior['older_record_reaudit_after_full_editorial_goal']
    assert not ledger['full_goal_complete']
    save(LEDGER,ledger);save('out/editorial_review_latest.json',candidate)
    DOC.write_text('# V856: livestock and prayer editorial completion in V855\n\n'+checkpoint+'\n\n'
        '## Source and layout\n\n'
        'Eight NPC voices and four actual protagonists per duty are independent alternatives. Revisions restore wiping-linked attachment,growth/inspection/reactions,the full Father/Son/Holy Spirit invocation,the Bible,the act of confession,Portugal recovery soon and the first-person strongest-fleet question. '
        'Retain1427,1431,1434,1436,1437,1445,1446 as faithful,natural wording. No animal growth,conversion,particular sin,new rank or route outcome is invented. '
        'The new36x3 planner scores readable clauses across all permitted row counts,keeps Holy Spirit/strongest fleet together,and reuses the frozen proven parity serializer. No manual breaks,padding or shortened invocation. Native code,crop and older compilers stay exact.\n\n'
        '## Actual verification scope\n\n'+gameplay['scope']+'\n\n'
        'Native RTTI/geometry identifies CDeckCabinInfoView/CDeckPersonnelView without text matching. Every hold matches the independent full252x36 native word plane and whole216x36 actual ink/blank RGB region at x16,y112. The full third-row ending and odd-middle-row transition are verified in actual playback. '
        'Other drawing commands,frame and palette remain unchanged. Fixtures alter only the empty visible Cabin type and original occupant fields. The donor already contains an isolated five-ship Copenhagen fleet;this is not earned travel,refitting or recruitment. Original source saves remain exact.\n\n'
        '## Release\n\n'
        f'- Candidate: `E:/Rota Nova translations/Generated/out/{ROM.name}`\n- SHA-256: `{candidate["sha256"]}`\n'
        f'- Profile: `{candidate["profile"]}`;experimental,canonical not promoted.\n'
        f'- Canonical base: `out/raphael_natural_v2_accepted_base.nds`;SHA-256 `{manifest["base_sha256"]}`.\n'
        f'- Exact clean-input patch: `{ROM.with_suffix(".xdelta").name}`;SHA-256 `{candidate["patch_sha256"]}`.\n'
        f'- Clean input SHA-256: `{release["clean_input_sha256"]}`.\n'
        f'- Final review: `{REVIEW}`;closure: `{closure}`.\n\n'
        'Only COMMON and ARM9 selection metadata differ from V850. Complete471-batch/114-layer inheritance,all other components,negative source/control cases and exact patch reconstruction pass. Earlier modules/scripts are frozen;new successors use exclusive creation with source hash checks. '
        'Human cold-boot acceptance is required before canonical promotion;test title/New Game and changed role17/18 scenes on the user\'s setup. Repaired shop676/677 remains exact;no fresh shop activation is claimed. '
        'Four native guide-candidate PNGs retain fixture provenance. The full editorial goal,global formatting watch,raw-source inventory,graphics/all18 plaques and later older-record re-audit remain unfinished.\n',encoding='utf-8')
    for path in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with path.open('a',encoding='utf-8') as f:f.write('\n\n## V856: livestock and prayer editorial completion\n\n'+checkpoint+' See [V856 evidence](livestock_prayer_v856_completion.md).\n')
    GUIDE.mkdir(parents=True);guides=[]
    for label,number in CASES.items():
        source=CAP/f'livestock_prayer_v856_855_{label}/frame_004200_navigation.png';target=GUIDE/f'{label}_ID{number}_V855.png'
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guides.append({'source':str(source),'guide_candidate':str(target),'sha256':sha(target.read_bytes()),
            'provenance':'Actual cold-boot framebuffer with disclosed2/3-byte isolated room assignment;not earned refit or recruitment.'})
    save(GUIDE/'provenance.json',{'candidate_sha256':candidate['sha256'],'guide_candidates':guides,'not_unqualified_ordinary_progression_screenshots':True})
    sources={p for v in (852,853,854,855,856) for p in Path(f'work/analysis/livestock_prayer_v{v}').glob('*') if p.is_file() and p.suffix!='.nds'}
    sources.update(map(Path,(str(LEDGER),str(REVIEW),str(DOC),str(MANUSCRIPT),owned.CONFIG,
        'translations/livestock_prayer_editorial_manuscript_v1.json','translations/release_stack.json','translations/rom_retention_pins.json',
        'scripts/prepare_livestock_prayer_context_v852.py','scripts/prepare_livestock_prayer_prose_v853.py','scripts/livestock_prayer_layout_v854.py',
        'scripts/probe_livestock_prayer_fonts_v854.py','dk4tool/patch/livestock_prayer_editorial.py',
        'scripts/prepare_livestock_prayer_release_v855.py','scripts/verify_livestock_prayer_release_v855.py',
        'scripts/run_livestock_prayer_startup_v855.py','scripts/verify_livestock_prayer_startup_v855.py',
        'scripts/native_livestock_prayer_fixture_v856.py','scripts/run_livestock_prayer_adapter_v856.py','scripts/run_livestock_prayer_v856.py',
        'scripts/verify_livestock_prayer_gameplay_v856.py','scripts/record_livestock_prayer_completion_v856.py','scripts/build_integrated_release.py',
        'docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')))
    sources.update(map(Path,read(owned.CONFIG)['dependencies']));sources.update((ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta')))
    archived=[]
    for source in sorted(sources):
        target=ARCHIVE/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    for label in CASES:
        folder=f'livestock_prayer_v856_855_{label}'
        for name in ('capture_report.json','navigation_command_journal.json'):
            source=CAP/folder/name;target=ARCHIVE/'captures'/folder/name;target.parent.mkdir(parents=True,exist_ok=True)
            copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
            archived.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'archive':str(ARCHIVE),'all_copies_hash_verified':True,'files':archived,
        'guide_candidates':str(GUIDE),'all_ROMs_captures_and_generated_artifacts_on_E':True,'full_goal_complete':False})
    print('Livestock/Chapel24 complete:732 total,533 revised,199 retained;735 source/prose reviewed. Full goal and separate graphics audit remain open.',flush=True)


if __name__=='__main__':main()
