"""Archive verified covering fire; retain reinforcement and successful-shot gates."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1045')
ACTUAL=Path('work/analysis/reinforcement_sniping_v1042/actual_covering_fire_verification.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    actual=read(ACTUAL);assert sha(ROM.read_bytes())==actual['candidate_sha256']
    assert len(actual['complete_actual_holds'])==len(actual['exact_fixture_replays'])==2
    assert actual['normal_A_dismissal_enters_original_battle_without_blank_or_extra_page']
    assert actual['original_support_scan_loaded_existing_own_fleet57_as_player_support']
    for version,frame in ((1037,5100),(1039,5510),(1041,6310),(1044,6550)):
        p=Path(f'work/analysis/reinforcement_sniping_v{version}/terminal_preservation.json')
        terminal=read(p);assert terminal['source_and_disposable_donors_unchanged']
        report=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v{version}_1034_regional/capture_report.json')
        assert read(report)['frames']==frame
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    checkpoint=('V1045 verifies original covering-fire source1917 in registered V1034. A disposable cold reload of the original-UI-created Manuel regional fleet reaches normal declaration,opponent reply,and the original support scan;fleet57 remains player-owned and supplies its native compact commander name. Two complete actual228x64 font/RGB holds match every glyph and blank paper,with uniform margins,stable portrait/name and full leading/trailing letters. Two exact location-fixture replays own16 then32 coordinate bytes;all other RAM and all identities remain exact. Normal dismissal enters original battle/duel with groups1(player),8(opponent),57(player support),without an extra page. A separate ranged pilot confirms original-qualified Lookout actor16 with native Aim166 from one Luck byte64->100 through the original attribute method;level37 remains unchanged. That pilot produced a normal Latina capture and later normal withdrawal,no successful admiral-shot claim. All four runs terminate and original/disposable donors remain unchanged. Reinforcement and successful-shot actual events,original eligibility/RNG outcomes and normal transitions remain required for this20-entry batch. No new completion credit:1196 complete,1219 source/prose. Full editorial scope and separate graphics audit remain active;V997 stays the current fully scene-verified candidate,V1034 remains pending.')
    ledger['reinforcement_sniping_actual_v1045']={'status':'covering-fire-original-event-verified-other-two-families-pending',
        'candidate':'out/all_routes_combined_v1034_candidate.nds','actual_covering_fire_proof':str(ACTUAL),
        'actual_covering_fire_proof_sha256':sha(ACTUAL.read_bytes()),'representative_actual_message_ID':1917,
        'family_native_message_IDs':list(range(1917,1924)),
        'Lookout_fixture':'scripts/native_reinforcement_lookout_v1043.py',
        'Lookout_native_prerequisite_and_ranged_pilot':'work/analysis/reinforcement_sniping_v1044',
        'reinforcement_and_successful_shot_events_pending':True,'completed_entries_added':0}
    ledger['pending_registered_reinforcement_sniping_candidate']['verified_actual_families']=['covering_fire']
    ledger['pending_registered_reinforcement_sniping_candidate']['pending_actual_families']=['reinforcement','admiral_shot']
    ledger['formatting_watchlist']['covering_fire_actual_v1045']={'proof':str(ACTUAL),
        'checks':'Two complete actual font/RGB holds;native Manuel argument;uniform visible margins,complete first/last letters,blank paper and normal dismissal;whole-game formatting audit remains open.'}
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1045-covering-fire-actual-event','proof':str(ACTUAL),
        'completed_entries_added':0,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'progress:694 native font cases,registered V1034 exact patch,7336 copies178 sequences and8 ordinary cold-boot frames',
        'this_goal_turn_classification':'progress:original own-fleet support event verified with complete actual glyphs and exact fixture replays;native Lookout shot prerequisite established',
        'full_goal_complete':False})
    for key in ('current_integrated_candidate','source_pins','current_native_relocation_reference','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==before[key]
    save(lp,ledger)
    doc=Path('docs/reinforcement_sniping_v1045_actual_checkpoint.md');assert not doc.exists()
    doc.write_text('# V1045: original covering-fire event verified\n\n'+checkpoint+'\n\n## Next source-bound tests\n\n'
        'The first approach allowed normal sailing to separate the fleets;the successor places two existing own fleets near an unchanged opponent while the original target selector is paused. No fleet ownership,captain identity,policy,source selector,text or battle outcome was injected. Both fixture receipts replay every4MiB byte exactly. Actual First Mate/fallback actor18 selects1917 through source table021173C0;fleet57 commander23 supplies Manuel through its original compact-name getter.\n\n'
        'For the shot test,the original Lookout assignment is Gerhard16,with native qualification and Aim166. The original shot branch,RNG2000 and threshold remain unchanged. The failed ranged pilot exposed an inadequately protected new regional vessel and accidental withdrawal when A was pressed outside a dialog. Before the next pilot,map original crew capacities and use only valid pre-battle staffing or bounded recovery of still-live own ships;never revive a disabled ship or force a result. Use shorter pauses at battle entry and original course/attack controls.\n\n'
        'Reinforcement helpers774BC/7777C additionally require source faction association getter3C740 (field47),relation predicates and nearby-fleet selector773D8. Original method3CB00 owns the association write. These observations are mapping leads;confirm original caller semantics before creating a documented assistance context. No reinforcement scene has been claimed.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1045: original covering-fire actual event\n\n'+checkpoint+' See [V1045 checkpoint](reinforcement_sniping_v1045_actual_checkpoint.md).\n')
    guide=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1045 Covering fire');assert not guide.exists();guide.mkdir(parents=True)
    source=Path(actual['complete_actual_holds'][0]['capture']);target=guide/'01_Manuel_Covering_Fire.png'
    copy2(source,target);assert sha(target.read_bytes())==actual['complete_actual_holds'][0]['capture_sha256']
    save(guide/'provenance.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_capture':str(source),'unmodified_screenshot':str(target),'sha256':sha(target.read_bytes()),
        'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes()),
        'disclosed_fixture':'Original-UI-created own regional fleet;location-only placement of both own fleets near the unchanged opponent. No earned travel/progression claim.'})
    archive=Path('E:/Rota Nova translations/Editorial review/V1045 Covering fire gameplay');assert not archive.exists()
    files=[lp,doc,ACTUAL,Path(__file__),Path('scripts/verify_covering_fire_gameplay_v1042.py')]
    for version in (1037,1039,1041,1044):
        files += list(Path(f'work/analysis/reinforcement_sniping_v{version}').glob('*.json'))
        files += list(Path(f'work/analysis/reinforcement_sniping_v{version}').glob('*.jsonl'))
        files += [Path(f'scripts/run_reinforcement_regional_live_v{version}.py')]
        folder=Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v{version}_1034_regional')
        files += [folder/'capture_report.json']
    files += [Path('scripts/native_reinforcement_location_v1038.py'),Path('scripts/native_reinforcement_proximity_v1040.py'),
        Path('scripts/native_reinforcement_lookout_v1043.py'),Path('work/analysis/reinforcement_sniping_v1043/offline_exact_fixture_proof.json')]
    files += [Path(r['capture']) for r in actual['complete_actual_holds']]+[Path(actual['actual_duel_entry_screenshot'])]
    copied=[]
    for source in dict.fromkeys(files):
        target=archive/source.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True)
        assert not target.exists();copy2(source,target);assert source.read_bytes()==target.read_bytes()
        copied.append({'source':str(source),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'completed_entries_added':0,
        'actual_guide_screenshots':1,'full_goal_complete':False})
    save(ROOT/'final_goal_turn_check.json',{'actual_covering_fire_proof_sha256':sha(ACTUAL.read_bytes()),
        'four_terminal_cold_boot_runs_and_original_donors_preserved':True,
        'no_live_process_left_by_this_checkpoint':True,'completed_records':1196,'source_prose_records':1219,
        'remaining_actual_families':['reinforcement','admiral_shot'],'full_goal_active_and_incomplete':True})
    print('Original covering fire verified and guide screenshot saved. Reinforcement and successful-shot events remain;1196 complete unchanged;goal active.',flush=True)


if __name__=='__main__':main()
