"""Record exact combined build/startup evidence; keep actual events incomplete."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1036')
BUILD=Path('work/analysis/reinforcement_sniping_v1033')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')
RETENTION=Path('work/rom_retention/20261021T0612111839985Z.json')


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    release=read(BUILD/'registered_release_verification.json');startup=read(BUILD/'ordinary_startup_verification.json')
    assert sha(ROM.read_bytes())==release['candidate_sha256']==startup['candidate_sha256']
    assert sha(ROM.with_suffix('.xdelta').read_bytes())==release['patch_sha256']
    assert sha(Path(release['exact_clean_input_patch_reconstruction']).read_bytes())==release['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and len(startup['pairs'])==8
    assert startup['all8_complete_startup_title_NewGame_frames_exact']
    assert sha(Path(startup['review_sheet']).read_bytes())==startup['review_sheet_sha256']
    plan=read(RETENTION)
    assert len(plan['roms'])==219 and sum(r['action']=='keep' for r in plan['roms'])==191
    assert all(Path(r['path']).exists() for r in plan['roms'])
    assert not RETENTION.with_suffix('.result.json').exists() and not RETENTION.with_suffix('.journal.jsonl').exists()
    save(ROOT/'startup_visual_review.json',{'startup_proof':str(BUILD/'ordinary_startup_verification.json'),
        'startup_proof_sha256':sha((BUILD/'ordinary_startup_verification.json').read_bytes()),
        'review_sheet':startup['review_sheet'],'review_sheet_sha256':startup['review_sheet_sha256'],
        'all8_complete_startup_frames_visually_reviewed':True,
        'title_captain_selection_confirmation_and_Rafael_opening_match_V997':True,
        'new20_event_announcements_not_activated':True,'full_goal_complete':False})
    doc=Path('docs/reinforcement_sniping_v1036_integrated_checkpoint.md');assert not doc.exists()
    candidate={'path':str(ROM),'sha256':release['candidate_sha256'],'profile':'all-routes-unified-v1034',
        'MESFILE_sha256':release['COMMON_sha256'],'ARM9_sha256':release['ARM9_sha256'],
        'patch':str(ROM.with_suffix('.xdelta')),'patch_sha256':release['patch_sha256'],
        'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-native-copy-font-exact-patch-startup-verified-three-event-families-pending',
        'details':str(doc),'full_goal_complete':False}
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    assert ledger['current_integrated_candidate']['sha256']=='0093915adb53c7c1034b696d54bf897079908aa598ea39bdced849107983660d'
    ledger['pending_registered_reinforcement_sniping_candidate']=candidate
    ledger['reinforcement_sniping_v1036']={'candidate':candidate,'native_message_IDs':list(range(1911,1931)),
        'status':'registered-exact-patch-startup-verified-original-events-pending',
        'release_proof':str(BUILD/'registered_release_verification.json'),
        'startup_proof':str(BUILD/'ordinary_startup_verification.json'),
        'startup_visual_review':str(ROOT/'startup_visual_review.json'),
        'actual_preflight_plan':'work/analysis/reinforcement_sniping_v1035/actual_scene_preflight_plan.json',
        'completed_entries_added':0,'source_prose_reviews_added':0}
    checkpoint=('V1036 records experimental combined V1034 for20 reinforcement,covering-fire and Lookout-shot paragraphs1911-1930. All471 batches114 accepted layers and final guards pass. All3648 unselected messages,including user676/677 repair,and unrelated graphics/routes/names/fonts/ARM7/overlays are exact to V997.7336 native copies178 cache sequences and694 complete font cases pass;56696 source and56696 research selector cases preserve fixed212/128-byte runtime spans and entire123040 staged bytes. The exact clean-input patch reconstructs every ROM byte. Two fixture-free no-save cold boots provide eight title/New Game full-screen pairs exact to V997 and visually reviewed. Source-mapped physical ILNK record movement1916-1976 stays within repacked blocks20/21;stable message IDs,all unrelated text and complete native copies are preserved. Original reinforcement/own-fleet covering-fire/successful-shot eligibility,actual announcements,geometry,dismissal and transitions remain pending. V997 stays current fully scene-verified candidate;no completed-entry credit:1196 complete,1219 source/prose. Full shared/routes/player prose/raw-source inventory,separate graphics/all18 plaques,older750-752,Samwell header and later older-record re-audit remain open. Canonical unchanged;goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1036-reinforcement-sniping-combined-startup',
        'candidate':candidate,'proof':str(BUILD/'registered_release_verification.json'),
        'completed_entries_added':0,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'progress:current V997 shop repair font/wrapping preserved and formatting watch updated',
        'this_goal_turn_classification':'progress:20 native formatting approvals,694 font cases,registered combined ROM,exact patch,7336 copies178 cache sequences and8 complete ordinary cold-boot screens',
        'full_goal_complete':False})
    for key in ('current_integrated_candidate','source_pins','current_native_relocation_reference','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles','formatting_watchlist'):
        assert ledger[key]==before[key]
    save(lp,ledger)
    doc.write_text('# V1036: combined reinforcement and shot candidate\n\n'+checkpoint+'\n\n## Exact candidate\n\n'
        '- Experimental ROM: '+str(ROM)+'\n- ROM SHA-256: '+candidate['sha256']+'\n- Profile: '+candidate['profile']+
        '\n- Patch SHA-256: '+candidate['patch_sha256']+'\n- Clean input SHA-256: '+release['clean_input_sha256']+
        '\n- Canonical base: '+release['canonical_base']+'\n- Canonical SHA-256: '+release['canonical_sha256']+
        '\n- Applied stack: all471 registered batches and114 accepted layers;new optional reinforcement_sniping_editorial stage after the full V997 stack.'+
        '\n- Changed from V997: /COMMON/MESFILE.DK4 and source-guarded ARM9 text-directory metadata/three fixed runtime spans. Every other internal file is exact.'+
        '\n\n## Verification limits and next work\n\nThe eight ordinary cold-boot captures verify title,New Game selection/confirmation and Rafael opening. They do not activate these20 event alternatives. Next exercise original supporting-faction reinforcement,another own fleet for covering fire,and original Lookout successful-shot eligibility/RNG/resolution. Verify portrait/name,text bitmap/RGB,bounds,normal dismissal and transitions. No numeric-message injection or forged battle result. The original-UI-created Manuel fleet donor is hash-protected in the V1035 actual-scene preflight plan.\n\n'
        'The first release verifier incorrectly required unchanged physical record indices across an explicitly registered relocation. Its preserved successor proves each of61 moved physical indices belongs to the source-mapped blocks20/21,all3668 stable IDs survive,and every unselected string is exact. All7336 original loader copies and178 sequences use the rebuilt directory. No display or source-identity failure was waived.\n\n'
        'ROM retention was preview-only:219 files inventoried,191 designated keep and28 potential deletions. No ApplyPlan or deletion ran;all219 files remain. All new ROMs,captures and evidence reside on E.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1036: reinforcement and shot combined/startup checkpoint\n\n'+checkpoint+' See [V1036 checkpoint](reinforcement_sniping_v1036_integrated_checkpoint.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V1036 Reinforcement and shot combined build')
    assert not archive.exists()
    files=[lp,doc,Path(__file__),RETENTION,ROOT/'startup_visual_review.json',
        Path('translations/reinforcement_sniping_editorial_release_v1.json'),Path('translations/release_stack.json'),
        Path('dk4tool/patch/reinforcement_sniping_editorial.py'),Path('scripts/build_integrated_release.py'),
        Path('scripts/prepare_reinforcement_sniping_release_v1033.py'),Path('scripts/verify_reinforcement_sniping_release_v1034.py'),
        Path('scripts/verify_reinforcement_sniping_release_v1034b.py'),Path('scripts/run_reinforcement_sniping_startup_v1034.py'),
        ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta'),
        Path('work/analysis/reinforcement_sniping_v1035/actual_scene_preflight_plan.json')]
    files += [p for p in BUILD.glob('*.json')]+[BUILD/'native_audit/audit.json',BUILD/'builder_before.py',
        BUILD/'builder_added_optional_stage.bin',Path(startup['review_sheet'])]
    copied=[]
    for source in dict.fromkeys(files):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        assert not target.exists();copy2(source,target);assert source.read_bytes()==target.read_bytes()
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_ROM_or_donor_duplicate_added':True,
        'completed_entries_added':0,'full_goal_complete':False})
    save(ROOT/'final_goal_turn_check.json',{'candidate':candidate,
        'release_proof_sha256':sha((BUILD/'registered_release_verification.json').read_bytes()),
        'startup_proof_sha256':sha((BUILD/'ordinary_startup_verification.json').read_bytes()),
        'ledger_completed':1196,'ledger_source_prose':1219,'no_new_actual_event_credit':True,
        'current_fully_scene_verified_candidate_unchanged_V997':True,
        'canonical_and_clean_hashes_verified_in_release_and_retention':True,
        'all219_inventory_ROM_files_still_exist':True,'full_goal_active_and_incomplete':True})
    print('V1036:V1034 exact combined ROM/patch and8 ordinary boots archived.1196 complete;20 event scenes still pending. Goal active.',flush=True)


if __name__=='__main__':main()
