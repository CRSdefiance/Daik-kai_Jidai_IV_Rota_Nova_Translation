"""Record verified original reinforcement; retain the independent successful-shot gate."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.reinforcement_sniping_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/reinforcement_sniping_v1054')
ACTUAL=Path('work/analysis/reinforcement_sniping_v1052/actual_reinforcement_verification.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    actual=read(ACTUAL);assert sha(ROM.read_bytes())==actual['candidate_sha256']
    assert len(actual['complete_actual_holds'])==2 and len(actual['exact_fixture_replays'])==1
    assert actual['original_reinforcement_scan_loaded_existing_allied_fleet24_as_player_support']
    assert actual['normal_A_dismissal_enters_original_battle_without_blank_or_extra_page']
    for version,frame in ((1047,5610),(1049,5810)):
        folder=Path(f'work/analysis/reinforcement_sniping_v{version}')
        assert read(folder/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
        assert read(Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v{version}_1034_regional/capture_report.json'))['frames']==frame
    rom,clean=map(NdsImage.open,(ROM,'work/clean.nds'))
    current=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'))
    source=common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'),clean.read_file('/__arm9__.bin'))
    inventory=ROOT/'preceding_sighting614_621_followup_inventory.json'
    rows=[{'message_ID':n,'source_hex':source[n].text.hex(),'source_Japanese':source[n].text.decode('cp932'),
        'current_hex':current[n].text.hex(),'current_English':current[n].text.decode('cp932'),
        'source_block':source[n].block,'current_block':current[n].block} for n in range(614,622)]
    save(inventory,{'candidate_sha256':sha(ROM.read_bytes()),'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),
        'source_table':0x02118560,'native_message_IDs':list(range(614,622)),'entries':rows,
        'observed_actual_message614':'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1049_1034_regional/frame_005210_navigation.png',
        'finding':'The earlier source sighting notice uses At NW in its current English. Queue the complete eight-voice family for natural-English/context review;it is preserved unchanged by V1034.',
        'inventory_only_not_source_prose_or_completion_credit':True})
    lp=Path('translations/editorial_review_current_v1.json');ledger=read(lp);before=deepcopy(ledger)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1219
    checkpoint=('V1054 verifies original reinforcement1911 in registered V1034:two complete actual font/RGB holds,full Valdes faction bytes,stable portrait/name,uniform margins and all leading/trailing letters. One exact19-byte context replay combines16 own-position bytes and3 original-method faction bytes;source3C8F4 sets alliance/assistance and existing hostility. Applied before first sighting,it reaches the original614 notice,then1911,and normal dismissal loads existing allied fleet24 as player support with enemy8 in original battle. The later-context pilot remains a negative first-sighting control;no sighting flags were reset. Covering fire and reinforcement are now actual-display verified;successful Lookout shot and native outcome/dismissal remain pending. Native-clamped staffing124/24,qualified Gunnery role9/room8 and Lookout role7/Aim166 have source-bound fixture proof. The current ranged encounter remains a separate unfinished test;no shot or battle-result credit. The preceding614-621 family is queued as unreviewed inventory,not new prose credit.1196 complete,1219 source/prose;V997 current fully scene-verified,V1034 pending;full editorial scope and separate graphics audit active.')
    ledger['reinforcement_sniping_actual_v1054']={'status':'reinforcement-and-covering-fire-verified-successful-shot-pending',
        'candidate':str(ROM),'actual_reinforcement_proof':str(ACTUAL),'actual_reinforcement_proof_sha256':sha(ACTUAL.read_bytes()),
        'representative_actual_message_ID':1911,'family_native_message_IDs':list(range(1911,1917)),
        'successful_shot_actual_gate_pending':True,'completed_entries_added':0}
    ledger['pending_registered_reinforcement_sniping_candidate']['verified_actual_families']=['covering_fire','reinforcement']
    ledger['pending_registered_reinforcement_sniping_candidate']['pending_actual_families']=['admiral_shot']
    ledger['newly_observed_sighting_followup']={'inventory':str(inventory),'native_message_IDs':list(range(614,622)),
        'status':'inventory-only-natural-English-review-open','source_prose_reviews_added':0,'completed_entries_added':0}
    ledger['formatting_watchlist']['reinforcement_actual_v1054']={'proof':str(ACTUAL),
        'checks':'Two actual full font/RGB holds;complete native Valdes argument;uniform margins and normal battle entry. Global formatting audit remains open.'}
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V1054-reinforcement-original-event','proof':str(ACTUAL),
        'completed_entries_added':0,'source_prose_reviews_added':0,
        'previous_goal_turn_classification':'progress:covering-fire actual fonts,state and normal dismissal verified',
        'this_goal_turn_classification':'progress:original faction assistance and first-sighting gates mapped;reinforcement full actual fonts and battle transition verified;native ranged prerequisites established',
        'full_goal_complete':False})
    for key in ('current_integrated_candidate','source_pins','current_native_relocation_reference','unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal','raw_source_coverage_revisit','approved_name_roles'):
        assert ledger[key]==before[key]
    save(lp,ledger)
    doc=Path('docs/reinforcement_sniping_v1054_reinforcement_checkpoint.md');assert not doc.exists()
    doc.write_text('# V1054: original reinforcement event verified\n\n'+checkpoint+'\n\n'
        'The source sequence is614 first-sighting/battle preparation,then1911 reinforcement. Source faction7 supplies the complete native label Valdes (56616c646573),not Walds;an initial visual transcription was corrected against actual bytes before verification. The failed1052 transcription assertion is retained;1052b proves the correct original label and all text pixels. No ROM translation change was needed.\n\n'
        'At5410/5510 the original reinforcement body is complete and stable. A at5510 dismisses it;5610 shows original sea battle with allied fleet24 loaded under the player-support flag. Later pauses and a later A input are retained in the terminal5810 trace;verification of the required transition ends at5610. No victory or earned alliance/travel claim.\n\n'
        'The ranged test uses the existing player crew and ships. Native AddCrew AAF38 clamps main/regional crew to124/24;Charles18 qualifies for Gunnery room8 (source role9),Gerhard16 qualifies for Lookout room1 (source role7),and one original-method Luck adjustment gives Lookout Aim166 with level37 unchanged. Original enemy damage has been observed;only still-live own health/coordinates are recovered. Original shot RNG and all enemy statistics remain unchanged in the current unfinished attempt.\n',encoding='utf-8')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V1054: original reinforcement actual event\n\n'+checkpoint+' See [V1054 checkpoint](reinforcement_sniping_v1054_reinforcement_checkpoint.md).\n')
    guide=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V1054 Reinforcements');assert not guide.exists();guide.mkdir(parents=True)
    capture=Path(actual['complete_actual_holds'][0]['capture']);target=guide/'01_Valdes_Reinforcements.png';copy2(capture,target)
    assert sha(target.read_bytes())==actual['complete_actual_holds'][0]['capture_sha256']
    save(guide/'provenance.json',{'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),
        'source_capture':str(capture),'unmodified_screenshot':str(target),'sha256':sha(target.read_bytes()),
        'actual_proof':str(ACTUAL),'actual_proof_sha256':sha(ACTUAL.read_bytes()),
        'disclosed_fixture':'Original existing fleets;16 own coordinate bytes plus3 original-method faction alliance/assistance/hostility bytes before first sighting. No earned progression claim.'})
    archive=Path('E:/Rota Nova translations/Editorial review/V1054 Reinforcement gameplay');assert not archive.exists()
    files=[lp,doc,ACTUAL,inventory,Path(__file__),Path('scripts/verify_reinforcement_gameplay_v1052.py'),
        Path('scripts/verify_reinforcement_gameplay_v1052b.py'),Path('scripts/native_reinforcement_pact_v1046.py'),
        Path('scripts/native_reinforcement_pact_v1048.py'),Path('scripts/native_ranged_staffing_v1050.py'),
        Path('scripts/native_ranged_staffing_v1050b.py'),Path('work/analysis/reinforcement_sniping_v1050b/offline_exact_fixture_proof.json')]
    for version in (1047,1049):
        folder=Path(f'work/analysis/reinforcement_sniping_v{version}')
        files+=list(folder.glob('*.json'))+list(folder.glob('*.jsonl'))+[Path(f'scripts/run_reinforcement_regional_live_v{version}.py')]
        files.append(Path(f'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v{version}_1034_regional/capture_report.json'))
    files += [Path(r['capture']) for r in actual['complete_actual_holds']]+[Path(actual['actual_battle_entry_screenshot'])]
    copied=[];generated=Path('E:/Rota Nova translations/Generated')
    for source in dict.fromkeys(files):
        try:relative=source.absolute().relative_to(Path.cwd())
        except ValueError:relative=Path('Generated')/source.absolute().relative_to(generated)
        destination=archive/relative;destination.parent.mkdir(parents=True,exist_ok=True);assert not destination.exists()
        copy2(source,destination);assert source.read_bytes()==destination.read_bytes()
        copied.append({'source':str(source),'archive':str(destination),'sha256':sha(destination.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'guide_screenshots_added':1,
        'no_unfinished_live_ranged_capture_report_or_growing_journal_archived_as_final':True,
        'completed_entries_added':0,'full_goal_complete':False})
    print('Reinforcement actual event and guide archived;two of three event families verified. Successful shot remains;1196 complete unchanged.',flush=True)


if __name__=='__main__':main()
