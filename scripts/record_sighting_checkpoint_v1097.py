"""Record registered V1086 and scoped actual evidence;do not claim full completion."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_checkpoint_v1097')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1097 Sighting combined and gameplay checkpoint')
GUIDE=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1097 Sighting and support')
GENERATED=Path('E:/Rota Nova translations/Generated')


def main():
    assert not ARCHIVE.exists() and not GUIDE.exists() and not (ROOT/'checkpoint.json').exists()
    release_path=Path('work/analysis/sighting_release_v1085/registered_release_verification.json')
    release=read(release_path);rom=Path(release['candidate'])
    assert sha(rom.read_bytes())==release['candidate_sha256']=='df958b7289743e8eca79c9a6a216e134c9a2590321597f7bead15111ee8d748f'
    assert release['complete_reconstruction_byte_exact'] and release['all471_batches114_accepted_layers_and_final_guards_pass']
    assert release['all3653_unselected_message_strings_including_user676_677_and_inherited20_event_paragraphs_exact']
    assert sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    assert sha(Path(release['manifest']).read_bytes())==release['manifest_sha256']
    manifest=read(release['manifest']);assert manifest['candidate_sha256']==release['candidate_sha256']
    startup_path=release_path.parent/'ordinary_startup_verification.json';startup=read(startup_path)
    assert startup['all8_complete_startup_title_NewGame_frames_exact'] and startup['no_battery_save_savestate_or_fixtures']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    compass_path=Path('work/analysis/sighting_compass_v1094b/actual_compass_and_covering_fire_verification.json')
    compass=read(compass_path);assert len(compass['complete_actual_holds'])==4
    assert compass['original_pending_battle_setup_and_identity_bound_roles_verified']
    negative_path=Path('work/analysis/sighting_pilots_v1096/terminal_negative_pilot_verification.json')
    negative=read(negative_path);assert negative['all218_entire4MiB_fixtures_exact']
    labels_path=Path('work/analysis/sighting_labels_v1083b/native_label_proof.json');labels=read(labels_path)
    assert labels['all153_other_initialized_ship_records_exact'] and labels['complete_Armed_Latina_and_NUL_survive_original_initializer']
    shop_path=ROOT/'photographed_shop_formatting.json';shop=read(shop_path)
    assert len(shop['entries'])==2 and shop['global_formatting_audit_still_open']
    checkpoint=('V1097 records experimental combined V1086:15 sighting paragraphs614-628 and bounded vicinity/Armed Latina labels,with all471 batches114 accepted layers,7336 native copies178 cache sequences,unchanged123040 staged bytes,and an exact clean-input patch. Eight no-save startup/title/New Game frames match V1034 and are visually reviewed. Four complete actual native-font/RGB holds verify compass614 and inherited covering-fire1917;original fleet roles are bound by identity,not world-slot order. Normal A dismissal returns to sea with original pending battle context;this is not a complete battle playthrough. Two terminal pre-formation pilots have218 independently reconstructed entire4MiB fixtures;both reach the original city-ahead notice,not the requested close-range/incoming attack. Source and disposable saves remain unchanged. Shop676/677 again retain repaired native wrapping and complete font planes in V1086. Both source labels are integrated and constructor/getter verified;their new actual UI remains pending.1196 complete,1234 source/prose;no new completed credit,V997 stays fully scene-verified,canonical unchanged. Remaining close-range/incoming/name scenes,successful-shot gate,global formatting/shared/routes/raw-source coverage and separate unfinished graphics audit remain open.')
    visual=ROOT/'visual_review.json'
    save(visual,{'startup_sheet':startup['review_sheet'],'startup_sheet_sha256':startup['review_sheet_sha256'],
        'all8_startup_frames_visually_reviewed':True,'actual_compass_and_covering_fire_visually_reviewed':True,
        'terminal_sea_return_visually_reviewed':True,'negative_city_notice_captures_visually_reviewed':True,
        'old_V747_shop_capture_visually_reviewed_not_new_scene':True,
        'targeted_headless_tests_not_full_route_or_hardware_verification':True})
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    assert ledger['current_integrated_candidate']['sha256']=='0093915adb53c7c1034b696d54bf897079908aa598ea39bdced849107983660d'
    graphics=ledger['unresolved_graphics_work']
    ledger['pending_registered_sighting_candidate']={
        'path':str(rom),'sha256':release['candidate_sha256'],'profile':release['profile'],
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'patch':release['patch'],'patch_sha256':release['patch_sha256'],'manifest':release['manifest'],
        'status':'experimental-integrated-startup-and-compass-sample-verified;close-incoming-name-and-inherited-shot-pending',
        'release_verification':str(release_path),'actual_compass_verification':str(compass_path),'full_goal_complete':False}
    paths=ledger['active_source_prose_drafts']['manuscripts']
    old='translations\\sighting_editorial_manuscript_v6.json';assert paths.count(old)==1
    paths[paths.index(old)]='translations\\sighting_editorial_manuscript_v7.json'
    ledger['active_source_prose_drafts']['status']='three-older-context-pending;20-reinforcement-shot-pending;15-sighting-integrated-partial-actual-pending'
    ledger['newly_observed_sighting_followup'].update(manuscript='translations\\sighting_editorial_manuscript_v7.json',
        status='15-integrated;startup-and-compass614-actual-pass;incoming-close-and-transitions-pending',
        registered_candidate=str(rom),actual_compass_proof=str(compass_path),negative_close_pilots=str(negative_path),completed_entries_added=0)
    ledger['newly_observed_armed_latina_followup'].update(status='source-owned16-byte-label-integrated-in-V1086;154-initializers-and-native-font-pass;actual-UI-pending',
        constructor_proof=str(labels_path),candidate=str(rom),actual_UI_complete=False)
    ledger['formatting_watchlist']['latest_reference_proof']=str(shop_path)
    ledger['formatting_watchlist']['latest_user_screenshot_recheck']={
        'proof':str(shop_path),'candidate':str(rom),'exact_repaired676_677_bytes_preserved':True,
        'complete_native_wrapping_and_glyph_planes_rechecked':True,'new_actual_shop_activation_claimed':False,
        'result':'Aligned cooking pitch;no padding gap or stray Discover. Fashion pitch remains independently complete. Global audit open.'}
    ledger['sighting_v1097']={'release_proof':str(release_path),'startup_proof':str(startup_path),
        'visual_review':str(visual),'actual_compass_proof':str(compass_path),'negative_close_proof':str(negative_path),
        'completed_entries_added':0,'full_goal_complete':False}
    ledger['latest_checkpoint']=checkpoint
    assert ledger['unresolved_graphics_work']==graphics and not ledger['full_goal_complete']
    save(ledger_path,ledger)
    doc=Path('docs/sighting_v1097_integrated_checkpoint.md')
    doc.write_text('# V1097: registered sighting candidate and scoped gameplay evidence\n\n'+checkpoint+
        '\n\n## Verified scope\n\nThe compass capture contains the complete original faction label Centurione Co. and unchanged First Mate fallback Charles Rochefort. Both messages have two stable complete holds,all font pixels and blank paper match,and the A inputs dismiss normally. Original slot order is player1,support57,opponent8;source flags change support57 from5 to1. A prior verifier incorrectly assumed opponent8 must precede support57. Its failed script remains preserved;the successor binds roles to original fleet identities and ownership. The terminal image is Sea View,so the proof records pending battle setup and sea return rather than claiming a full visually observed battle.\n\nThe two close-range pilots use the protected pre-formation battery save,original faction prerequisites and only16 own-coordinate bytes for subsequent following. They stop when the original message changes;both stop at city-ahead,with target28 still unseen and absent from loaded groups. No sighting flag,actor identity,RNG or battle outcome is injected. They supply no target-scene credit.\n\n## Candidate identity\n\n- Candidate: `out/all_routes_combined_v1086_candidate.nds`\n- SHA-256: `'+release['candidate_sha256']+'`\n- Canonical base: `out/raphael_natural_v2_accepted_base.nds`\n- Canonical SHA-256: `'+release['canonical_sha256']+'`\n- Profile: `all-routes-unified-v1086` (experimental)\n- Exact patch SHA-256: `'+release['patch_sha256']+'`\n- Changed from V1034: COMMON block7 and native metadata,three existing bounded runtime spans,and two owned ARM9 label allocations. All other messages/routes/graphics/fonts/ARM7/overlays remain exact.\n\nThe canonical baseline and fully scene-verified V997 pin are unchanged. Remaining requirements include original incoming/close-range/name UI,dismissal and transitions,the inherited successful-shot scene,and the full shared/route/raw-source editorial inventory. Native uppercase weak-word matching remains an open general formatter issue. All18 plaques and the separate graphics audit remain unfinished.\n',encoding='utf-8')
    for filename in ('docs/translation_progress.md','docs/todo.md'):
        with Path(filename).open('a',encoding='utf-8') as stream:stream.write('\n\n## V1097: sighting combined and actual checkpoint\n\n'+checkpoint+'\n')
    with Path('docs/known_issues.md').open('a',encoding='utf-8') as stream:
        stream.write('\n\n## V1097: integrated labels and scoped encounter tests\n\nV1086 now integrates vicinity and Armed Latina in the original9/16-byte allocations;the V1082 research-only integration status is superseded. Original154 ship initializers preserve153 unrelated models. Actual compass614 and covering-fire1917 have four complete native-font/RGB holds and normal sea return. Close/incoming pilots reach a city-ahead notice and have no target credit. A failed fixed-slot-order verifier is superseded by identity-bound role checks;original groups retain player1/support57/opponent8. The terminal image is sea view with pending battle context,not a full battle playthrough. General uppercase weak-word matching,actual close/incoming/name display and inherited successful shot remain open. See sighting_v1097_integrated_checkpoint.md.\n')
    save(ROOT/'checkpoint.json',{'summary':checkpoint,'release_proof':str(release_path),'visual_review':str(visual),
        'actual_compass_proof':str(compass_path),'negative_pilot_proof':str(negative_path),
        'no_new_editorial_completion_credit':True,'full_goal_complete':False,'producer_sha256':sha(Path(__file__).read_bytes())})
    GUIDE.mkdir(parents=True);guide=[]
    for filename,frame in (('01_Compass_Fleet_Sighting.png',5310),('02_Manuel_Covering_Fire.png',5510)):
        source=Path(compass['complete_actual_holds'][0]['capture']).parent/f'frame_{frame:06d}_navigation.png'
        target=GUIDE/filename;copy2(source,target);assert sha(source.read_bytes())==sha(target.read_bytes())
        guide.append({'path':str(target),'sha256':sha(target.read_bytes()),'source':str(source),'frame':frame})
    save(GUIDE/'provenance.json',{'captures':guide,'candidate_sha256':release['candidate_sha256'],
        'targeted_cold_boot_test_with_disclosed17_byte_position_and_hostility_fixture':True,
        'not_earned_progression_or_full_route_verification':True,'actual_proof':str(compass_path)})
    ARCHIVE.mkdir(parents=True);files=[]
    sources=[ledger_path,doc,release_path,startup_path,labels_path,compass_path,negative_path,shop_path,visual,
        ROOT/'checkpoint.json',Path(startup['review_sheet']),Path(release['manifest']),Path(release['patch']),
        Path('translations/sighting_editorial_manuscript_v7.json'),Path('translations/sighting_editorial_release_v1.json'),
        Path('dk4tool/patch/sighting_editorial.py'),Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('docs/translation_progress.md'),Path('docs/todo.md'),Path('docs/known_issues.md')]
    sources+=list(Path('scripts').glob('*v109[4-7]*.py'))
    for row in compass['complete_actual_holds']:sources.append(Path(row['capture']))
    for case in ('closeReady28','closeAttack28'):
        run=Path('work/analysis/sighting_gameplay_v1095_'+case);plan=read(run/'run_plan.json');cap=Path(plan['capture_folder'])
        sources.extend([run/'run_plan.json',run/'terminal_preservation.json',run/'bounded_follow_observations.json',
            run/'navigation.jsonl',cap/'capture_report.json',cap/'frame_005619_navigation.png'])
    seen=set()
    for source in sources:
        if source.absolute() in seen:continue
        seen.add(source.absolute());assert source.is_file()
        relative=(source.absolute().relative_to(Path.cwd()) if source.absolute().is_relative_to(Path.cwd()) else
            Path('Generated')/source.absolute().relative_to(GENERATED))
        target=ARCHIVE/relative;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        files.append({'source':str(source),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':files,'no_ROM_duplicate_or_promotion':True,'no_new_completed_credit':True,'full_goal_complete':False})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(files),'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print('V1097 registered build,scoped gameplay and negative pilots archived;1196 complete/1234 source-prose;goal active.',flush=True)


if __name__=='__main__':main()
