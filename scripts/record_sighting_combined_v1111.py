"""Record exact combined V1105 and both actual sighting families;leave open gates."""
from collections import Counter
from pathlib import Path
from shutil import copy2
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_combined_review_v1111')
RELEASE=Path('work/analysis/sighting_grammar_release_v1104')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1111 Sighting grammar combined and actual checkpoint')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1111 Sighting and incoming attack')
GENERATED=Path('E:/Rota Nova translations/Generated')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists() and not GUIDE.exists()
    release_path=RELEASE/'registered_release_verification.json';release=read(release_path)
    startup_path=RELEASE/'ordinary_startup_verification.json';startup=read(startup_path)
    assert release['candidate_sha256']=='64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and release['all471_batches114_accepted_layers_and_final_guards_pass']
    assert release['entire_renderer_selector_previous_runtime_and_all_native_name_labels_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    readiness_path=Path('work/analysis/sighting_grammar_actual_v1106b/actual_compass_and_covering_fire_verification.json')
    incoming_path=Path('work/analysis/sighting_incoming_actual_v1109/actual_compass_and_covering_fire_verification.json')
    readiness,incoming=read(readiness_path),read(incoming_path)
    for proof in (readiness,incoming):
        assert proof['candidate_sha256']==release['candidate_sha256'] and len(proof['complete_actual_holds'])==4
        assert proof['normal_sighting_A_dismissal_to_original_covering_fire_then_normal_A_to_sea']
        assert proof['original_pending_battle_setup_and_identity_bound_roles_verified']
        assert proof['source_and_disposable_saves_unchanged'] and proof['terminal_frame']==5710
    assert [r['message_ID'] for r in readiness['complete_actual_holds']]==[614,614,1917,1917]
    assert [r['message_ID'] for r in incoming['complete_actual_holds']]==[622,622,1917,1917]
    cap=Path(readiness['complete_actual_holds'][0]['capture']).parent
    old_cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sighting_v1094_1086_compassReady8')
    controls=[]
    for frame,suffix in ((3400,'cold_boot'),(4200,'navigation')):
        current,old=cap/f'frame_{frame:06d}_{suffix}.png',old_cap/f'frame_{frame:06d}_{suffix}.png'
        assert Image.open(current).convert('RGB').tobytes()==Image.open(old).convert('RGB').tobytes()
        controls.append({'frame':frame,'capture':str(current),'capture_sha256':sha(current.read_bytes()),
            'entire_town_or_forecast_frame_exact_to_V1086':True})
    failed=Path('work/analysis/sighting_grammar_gameplay_v1106_compassReady8');failed_plan=read(failed/'run_plan.json')
    assert not (Path(failed_plan['capture_folder'])/'capture_report.json').exists()
    for key in ('source_donor','disposable_donor'):
        assert sha(Path(failed_plan[key]).read_bytes())==failed_plan['source_donor_sha256']
    retention_path=Path('work/rom_retention/20261021T1340521652363Z.json')
    import json
    retention=json.loads(retention_path.read_text(encoding='utf-8-sig'))
    assert len(retention['roms'])==223 and all(Path(row['path']).is_file() for row in retention['roms'])
    actions=dict(Counter(row['action'] for row in retention['roms']))
    assert any(row['path'].endswith('all_routes_combined_v1105_candidate.nds') and row['action']=='keep' for row in retention['roms'])
    ROOT.mkdir(parents=True)
    visual=ROOT/'visual_and_control_review.json'
    save(visual,{'all8_startup_sheet_frames_visually_reviewed':startup['review_sheet'],
        'both614_readiness_and622_actual_attack_and1917_support_visually_reviewed':True,
        'entire_text_bitmap_blank_paper_complete_letters_uniform_margins_and_bounds_verified':True,
        'town_and_forecast_controls':controls,'normal_A_dismissals_and_sea_returns_visually_reviewed':True,
        'original_pending_battle_setup_not_complete_battle_playthrough':True,
        'failed_first_fixture_stopped_at_old_terrain_ROM_hash_guard_before_RAM_return':True,
        'failed_fixture_original_and_disposable_donors_unchanged':True,
        'corrected_fixture_uses_same_original_terrain_code_bound_to_exact_V1105':True,
        'retention_preview':str(retention_path),'retention_action_counts':actions,
        'default_preview_only_no_ApplyPlan_all223_ROMs_still_present':True,
        'targeted_headless_emulator_tests_not_full_routes_or_hardware':True})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1267
    assert ledger['current_integrated_candidate']['sha256']=='0093915adb53c7c1034b696d54bf897079908aa598ea39bdced849107983660d'
    ledger['previous_pending_registered_sighting_candidate_V1086']=ledger['pending_registered_sighting_candidate']
    candidate={'path':release['candidate'],'sha256':release['candidate_sha256'],'profile':release['profile'],
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'manifest':release['manifest'],'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'release_proof':str(release_path),'startup_proof':str(startup_path),'actual_readiness_proof':str(readiness_path),
        'actual_incoming_proof':str(incoming_path),'status':'experimental-grammar15-integrated-and-both-representative-families-actual-verified;close-name-and-inherited-shot-still-open',
        'full_goal_complete':False}
    ledger['pending_registered_sighting_candidate']=candidate
    ledger['newly_observed_sighting_followup'].update(status='V1105-current-grammar-integrated;614-readiness-and622-attack-actual-complete;close-range-actual-pending',
        registered_candidate=release['candidate'],actual_compass_proof=str(readiness_path),actual_incoming_proof=str(incoming_path),
        completed_entries_added=0)
    ledger['sighting_faction_grammar_v1098'].update(status='V1105-integrated;both-source-families-sampled-in-actual-game;close-range-label-UI-pending',
        candidate=release['candidate'],release_proof=str(release_path),actual_readiness_proof=str(readiness_path),actual_incoming_proof=str(incoming_path))
    ledger['newly_observed_armed_latina_followup'].update(candidate=release['candidate'],
        status='16-byte-label-and-original-constructor-proof-preserved-exactly-in-V1105;actual-UI-pending',actual_UI_complete=False)
    ledger['formatting_watchlist']['latest_registered_preservation']={'candidate':release['candidate'],
        'proof':str(release_path),'all_repaired676_677_strings_and_entire_renderer_exact_to_V1086':True,
        'fresh_V1105_shop_activation_claimed':False,'global_formatting_audit_still_open':True}
    ledger['sighting_v1111']={'candidate':candidate,'visual_review':str(visual),'eight_complete_actual_sighting_support_holds':True,
        'two_original_source_family_roles_and_all_other_state_preserved':True,'no_new_completed_entry_credit':True,
        'close_range_and_name_UI_successful_shot_duel_geometry_and_full_scope_still_pending':True}
    summary=('V1111 records registered combined V1105 for15 source-faithful faction-grammar sighting revisions. All471 batches114 accepted layers,2700 complete native fonts,7336 loader copies178 cache sequences,and exact clean-input patch pass. Only COMMON7/message metadata differ from V1086;entire renderer/runtime,labels,graphics,routes/fonts and123040 staged bytes remain exact. Eight no-save startup/New Game frames,town and forecast controls pass. Two terminal original encounter runs verify614 readiness and622 incoming attack with four holds each including1917 support,complete font/RGB/blank-paper masks,uniform margins,full letters and normal A sea returns.17/19-byte fixtures preserve original actors,ownership,RNG,seen flags and outcomes;original/disposable saves exact. The earlier stale terrain-ROM test guard is corrected without ROM changes. Duel33 drafts now bind the full DA28->53914->D5404 macro path and four corrected native voice-fallback metadata lists;prose unchanged.1196 complete,1267 source/prose;no new completion credit. Close-range/Armed Latina actual UI,successful-shot event,duel native geometry/fonts/integration,remaining shared/routes/raw source,global formatting and separate graphics audit remain open. Canonical and fully scene-verified V997 remain unchanged;goal active.')
    ledger['latest_checkpoint']=summary;save(ledger_path,ledger)
    doc=Path('docs/sighting_v1111_combined_checkpoint.md')
    doc.write_text('# V1111: combined sighting grammar and original scene evidence\n\n'+summary+
        '\n\n## Candidate identity and handoff\n\n- Candidate: `out/all_routes_combined_v1105_candidate.nds`\n- Candidate SHA-256: `'+release['candidate_sha256']+'`\n- Canonical base: `out/raphael_natural_v2_accepted_base.nds`\n- Canonical SHA-256: `'+release['canonical_sha256']+'`\n- Profile: `all-routes-unified-v1105` (experimental). All114 accepted layers and471 inherited batches remain;the15-entry grammar stage follows the complete V1086 stack. The neighboring manifest and current release registry enumerate the complete set and scoped changes.\n- Exact clean-input patch: `out/all_routes_combined_v1105_candidate.xdelta`\n- Patch SHA-256: `'+release['patch_sha256']+'`\n- Clean input SHA-256: `'+release['clean_input_sha256']+'`\n- Changed from V1086: COMMON7 and ARM9 native message metadata only. All code,previous runtime patches,name labels,sections/BSS/cache/arenas and entire123040-byte staged payload are exact.\n\n## Verified scope\n\nNative checks include2700 complete glyph/wrap cases,7336 original warm/cold copies,178 cache sequences,whole-byte patch reconstruction,and original actor/table/name selection. Eight ordinary no-save title/New Game frames are pixel-identical to V1086. The Syracuse town screen and sailing forecast controls are also whole-frame identical. Actual614 readiness and622 incoming attack each have two stable full-font/RGB holds and the original1917 covering-fire follow-up. Both normal A inputs return to Sea View with original pending battle context;this is not a full battle playthrough.\n\nThe readiness fixture owns17 bytes:16 player coordinate bytes and1 original-method relationship prerequisite. The attack fixture owns19,adding2 original-method enemy attack-order bytes. No message ID,renderer,actor identity,seen flag,RNG or battle result is injected. These are disclosed isolated tests rather than earned progression. The first run stopped at a stale terrain-helper ROM-hash guard before returning a RAM mutation;its source/disposable saves remain exact. The corrected successor changes only the helper test ROM binding.\n\nThe candidate remains experimental. Cold-boot test the title menu,New Game,ordinary town dialogue and fleet-sighting/attacking notices when reached. Remaining audit gates specifically include close-range vicinity and Armed Latina actual UI,successful Lookout shot,duel formatting and transitions,and full shared/route/raw-source editorial review. The canonical baseline is not promoted. All18 plaques and the separate graphics audit remain open.\n\n## Duel source clarification\n\nOriginalDA28 calls53914 before D5404,so one logical paragraph before macro expansion remains required. The distinct duel parent/bitmap geometry still needs calibration. ManuscriptV2 corrects the -1 voice fallback membership for1939/1945/1951/1973;all33 English paragraphs and source glosses are unchanged. Existing hardcoded cover him in main-captain escape notices is source-reviewed for neutral replacement but is not integrated in this ROM.\n',encoding='utf-8')
    for filename in ('docs/translation_progress.md','docs/todo.md','docs/known_issues.md'):
        with Path(filename).open('a',encoding='utf-8') as stream:stream.write('\n\n## V1111: sighting grammar combined and actual checkpoint\n\n'+summary+' See [V1111 evidence](sighting_v1111_combined_checkpoint.md).\n')
    GUIDE.mkdir(parents=True);guide=[]
    for filename,proof,index in (('01_Fleet_Sighting.png',readiness,0),('02_Incoming_Attack.png',incoming,0),('03_Manuel_Covering_Fire.png',incoming,2)):
        source=Path(proof['complete_actual_holds'][index]['capture']);target=GUIDE/filename;copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'path':str(target),'source':str(source),'sha256':sha(target.read_bytes())})
    save(GUIDE/'provenance.json',{'candidate_sha256':release['candidate_sha256'],'captures':guide,
        'source_proofs':[str(readiness_path),str(incoming_path)],'disclosed17_and19_byte_coordinate_and_native_prerequisite_fixtures':True,
        'not_earned_progression_complete_route_or_hardware_verification':True})
    save(ROOT/'checkpoint.json',{'summary':summary,'candidate':candidate,'visual_review':str(visual),
        'retention_plan':str(retention_path),'retention_action_counts':actions,'no_ROMs_deleted':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    ARCHIVE.mkdir(parents=True);sources=[Path(__file__),ledger_path,doc,ROOT/'checkpoint.json',visual,release_path,startup_path,
        readiness_path,incoming_path,Path(startup['review_sheet']),Path(release['manifest']),Path(release['patch']),retention_path,
        Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('translations/sighting_grammar_editorial_release_v1.json'),Path('translations/sighting_editorial_manuscript_v9.json'),
        Path('translations/duel_editorial_manuscript_v2.json'),Path('dk4tool/patch/sighting_grammar_editorial.py'),
        Path('scripts/build_integrated_release.py'),Path('docs/translation_progress.md'),Path('docs/todo.md'),Path('docs/known_issues.md')]
    for pattern in ('*v1104.py','*v1105.py','*v1106*.py','*v1107.py','*v1109.py','*v1110.py'):sources+=list(Path('scripts').glob(pattern))
    for folder in ('sighting_grammar_release_v1104','duel_consumer_v1107','duel_metadata_v1110'):
        sources+=list(Path('work/analysis',folder).rglob('*.json'))
    for proof in (readiness,incoming):
        sources += [Path(row['capture']) for row in proof['complete_actual_holds']]
        sources.append(Path(proof['terminal_report']))
    for row in controls:sources.append(Path(row['capture']))
    seen=set();files=[]
    for source in sources:
        if not source.is_file() or source.absolute() in seen:continue
        seen.add(source.absolute());relative=(source.absolute().relative_to(Path.cwd()) if source.absolute().is_relative_to(Path.cwd()) else
            Path('Generated')/source.absolute().relative_to(GENERATED))
        target=ARCHIVE/relative;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        files.append({'source':str(source),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':files,'all_hashes_verified':True,'no_canonical_promotion_or_new_completed_entry_credit':True,'full_goal_complete':False})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(files),'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print('V1111 combined V1105 and both original sighting families verified and archived;1196 complete/1267 source-prose. All remaining gates and full goal stay open.',flush=True)


if __name__=='__main__':main()
