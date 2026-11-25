"""Archive completed source work and the terminal failed pilot; live run stays open."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_checkpoint_v1067')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1067 Sighting source and contact research')
GENERATED=Path('E:/Rota Nova translations/Generated')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==1196 and ledger['records_with_source_and_prose_pass']==1234
    rom_path=Path('out/all_routes_combined_v1034_candidate.nds')
    assert sha(rom_path.read_bytes())==ledger['pending_registered_reinforcement_sniping_candidate']['sha256']
    arm=NdsImage.open(rom_path).read_file('/__arm9__.bin')
    failed=Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1060_1034_regional/frame_006750_arm9_ram.bin')
    raw=failed.read_bytes();cpu,get=get_machine(arm,raw)
    assert get(0x7F244)==1 and get(0x7E19C,get(0x65EEC))==0
    log=Path('work/analysis/reinforcement_regional_live_v1060.log')
    assert 'native_contact_training_v1057c.py' in log.read_text(encoding='utf8') and 'AssertionError' in log.read_text(encoding='utf8')
    plan=read('work/analysis/reinforcement_sniping_v1060/run_plan.json')
    for path in (plan['source_donor'],plan['disposable_donor']):
        assert sha(Path(path).read_bytes())==plan['source_donor_sha256']
    ROOT.mkdir(parents=True)
    failure=ROOT/'terminal1060_guard_failure.json'
    save(failure,{'terminal_failure_log':str(log),'log_sha256':sha(log.read_bytes()),
        'last_saved_pause':str(failed),'last_saved_pause_sha256':sha(raw),'actual_player_captain_ID':1,
        'last_pause_native_captain_HP':0,'positive_HP_guard_correctly_refused_revival':True,
        'no_final_capture_report_or_successful_shot_credit':True,'original_and_disposable_donors_unchanged':True,
        'successor':'scripts/native_contact_live_geometry_v1062.py',
        'successor_changes':'Keep own captain at observed living144HP and opponent at positive10HP using original7E154;copy exact live opponent fixed point instead of stale cached point;both vessels must still be alive. Original RNG,selector,enemy result byte and outcome code are untouched.',
        'synthetic_health_and_provisions_not_earned_progression':True})
    checkpoint='V1067 archives15 source/prose-reviewed sighting drafts614-628 and exact native evidence for the still-Japanese close-range bearing provider.1196 entries complete,1234 source/prose reviewed;no new completed-entry credit. The previous contact pilot stopped at actual captainHP0;its positive-HP guard correctly refused revival and original/disposable saves remain unchanged. Source-guarded successor1062 uses healthy own captain,positive low-HP opponent,live fixed-point contact geometry and disclosed still-live vessel/provision recovery without RNG/message/outcome edits. Fresh cold-boot1063 remains a separate pending actual-shot test. Covering fire and reinforcements are verified;shot and normal outcome/dismissal remain open. V997 current fully scene-verified,V1034 pending;no ROM build or canonical change. Full editorial scope and separate unfinished graphics audit remain open.'
    ledger['latest_checkpoint']=checkpoint
    ledger['contact_research_v1067']={'terminal_failure_proof':str(failure),
        'offline_successor_proof':'work/analysis/reinforcement_sniping_v1062/offline_exact_fixture_proof.json',
        'current_run_plan':'work/analysis/reinforcement_sniping_v1063/run_plan.json',
        'current_capture_folder':'E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_sniping_v1063_1034_regional',
        'status':'separate-pending-targeted-event-test;not-completion-credit','no_new_ROM_built':True}
    save(ledger_path,ledger)
    doc=Path('docs/editorial_v1067_checkpoint.md')
    doc.write_text('# V1067: sighting review and contact-test checkpoint\n\n'+checkpoint+'\n\nThe15 drafts retain both native substitutions and independent voice classes. Preparing for battle never replaces already being attacked. The9-byte close-range source label至近距離 has a proposed equal-allocation vicinity replacement so in the vicinity remains natural alongside in the N/NW/etc. Provider-user classification,native wrapping/full-font proofs,registered integration and actual sighting scenes are still required. All15 formatting gates remain false.\n\nThe new contact context is explicitly synthetic. Both positive captain HP fields,still-live Hull/Crew,own provisions,staffing/Luck and coordinates are declared and bounded;actor IDs,ownership,RNG seed/initialization and enemy result byte remain untouched. Source eligibility/RNG/outcome code is unchanged. Original first-sighting,war choices and covering-fire scenes are reached from cold boot plus normal battery loading;no savestate is used. This is targeted headless emulator testing,not a full route or hardware playthrough.\n',encoding='utf8')
    for path in ('docs/translation_progress.md','docs/todo.md'):
        with Path(path).open('a',encoding='utf8') as f:f.write('\n\n## V1067: sighting/contact checkpoint\n\n'+checkpoint+'\n')
    paths=[Path(__file__),doc,Path('docs/sighting_v1066_source_review.md'),ledger_path,Path('translations/sighting_editorial_manuscript_v1.json'),
        Path('scripts/native_contact_live_geometry_v1062.py'),Path('scripts/run_reinforcement_regional_live_v1063.py'),
        Path('scripts/drive_contact_probe_v1064.py'),Path('scripts/research_sighting_context_v1065.py'),Path('scripts/prepare_sighting_prose_v1066.py'),
        Path('work/analysis/reinforcement_sniping_v1063/run_plan.json'),log,failed,failure]
    for folder in ('work/analysis/reinforcement_sniping_v1062','work/analysis/sighting_editorial_v1065','work/analysis/sighting_editorial_v1066'):
        paths.extend(Path(folder).rglob('*'))
    ARCHIVE.mkdir(parents=True);manifest=[];seen=set()
    for source in paths:
        if not source.is_file() or source.absolute() in seen:continue
        seen.add(source.absolute())
        if source.absolute().is_relative_to(Path.cwd()):relative=source.absolute().relative_to(Path.cwd())
        else:relative=Path('Generated')/source.absolute().relative_to(GENERATED)
        target=ARCHIVE/relative;target.parent.mkdir(parents=True,exist_ok=True);copy2(source,target)
        assert sha(source.read_bytes())==sha(target.read_bytes())
        manifest.append({'source':str(source),'archived':str(target),'sha256':sha(target.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':manifest,'completed_source_checkpoint_only_live_run_not_archived_as_terminal':True,
        'goal_complete':False,'no_new_ROM_or_patch':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(manifest),
        'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes()),'no_editorial_completion_credit':True})
    print('V1067:source checkpoint and terminal failed-pilot evidence archived;',len(manifest),'files. Actual-shot test remains pending.',flush=True)


if __name__=='__main__':main()
