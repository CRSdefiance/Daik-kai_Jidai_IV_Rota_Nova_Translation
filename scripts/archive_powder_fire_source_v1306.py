"""Audit both terminal fixtures/inputs and archive source-only fire review on E."""
import re
import struct
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_town_fixture_v1290 import apply_fixture as first_mate
from scripts.native_town_gunnery_fixture_v1299 import apply_fixture as gunnery
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/powder_fire_evidence_v1306')
DEST = Path('E:/Rota Nova translations/Editorial review/V1306 Powder fire source checkpoint')
BASE = 0x02000000
DONOR = '2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1'


def main():
    assert not ROOT.exists() and not DEST.exists()
    repo = Path.cwd().absolute()
    release = read('work/analysis/battle_aftermath_release_v1265/registered_release_verification.json')
    for field in ['candidate','patch']:
        assert sha(Path(release[field]).read_bytes()) == release[field+'_sha256']
    arm = NdsImage.open(release['candidate']).read_file('/__arm9__.bin')
    cases = [
        ('town_hold_v1297','town_hold_v1297_1266',7110,first_mate,{'town_context':'SaoTomeFirstMate'},18,12),
        ('town_gunnery_v1300','town_gunnery_v1300_1266',7510,gunnery,{'town_context':'SaoTomeGunnery'},24,16)]
    audited = []
    reports = []
    for run_name,cap_name,terminal,fixture,request,owned_count,changed_count in cases:
        run = Path('work/analysis')/run_name
        cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193')/cap_name
        report_path = cap/'capture_report.json'
        report = read(report_path)
        assert report['frames'] == terminal and report['cold_boot'] and not report['savestate_loaded']
        assert report['ROM_sha256'] == release['candidate_sha256'] and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k != 'synthetic_battle_recovery_proximity_fixtures')
        plan = read(run/'run_plan.json')
        assert sha(Path(plan['source_donor']).read_bytes()) == sha(Path(plan['disposable_donor']).read_bytes()) == DONOR
        assert read(run/'terminal_preservation.json')['source_and_disposable_donors_unchanged']
        snapshots = {}
        for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
            value = Path(row['path']).read_bytes()
            assert len(value) == row['bytes'] == 0x400000 and sha(value) == row['sha256']
            if row['frame'] in snapshots:
                assert snapshots[row['frame']]['sha256'] == row['sha256']
            snapshots[row['frame']] = row
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        before = Path(snapshots[5000]['path']).read_bytes()
        after,receipt = fixture(arm,before,request)
        assert report['synthetic_battle_recovery_proximity_fixtures'] == [{**receipt,'frame':5000}]
        owned = set(receipt['owned_bytes'])
        changes = [BASE+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a != b]
        assert len(owned) == owned_count and len(changes) == changed_count
        assert all(address in owned for address in changes)
        cpu,get = get_machine(arm,before)
        for root,length in [(get(0xCB184),0x1A04),(get(0xCB178),4+114*108),(get(0xCB160),4+21*76)]:
            assert before[root-BASE:root-BASE+length] == after[root-BASE:root-BASE+length]
        for offset in [0xD9858,0x51A20]:
            address = struct.unpack_from('<I',arm,offset)[0]
            assert not owned.intersection(range(address,address+4))
            assert before[address-BASE:address-BASE+4] == after[address-BASE:address-BASE+4]
        schedule = read(run/'original_load_inputs.json')
        for item in read(cap/'navigation_command_journal.json')['commands_received']:
            assert item['validation_passed']
            command = item['command']
            if command.get('stop'):
                continue
            assert command['until'] in snapshots and command['until'] > item['frame']
            if item['frame'] > 5000:
                assert 'battle_fixture' not in command
            if command.get('buttons') or command.get('touch') is not None:
                event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
                if command.get('touch') is not None:
                    event['touch'] = command['touch']
                schedule.append(event)
        assert schedule == report['scripted_input_schedule']
        audited.append({'run':str(run),'report':str(report_path),'report_sha256':sha(report_path.read_bytes()),
            'terminal_frame':terminal,'fixture_frame':5000,'owned_bytes':owned_count,'actual_changed_bytes':changed_count,
            'entire4MiB_fixture_replay_all_actor_objects_towns_companies_RNG_and_inputs_exact':True,
            'no_fixture_after_battle_entry':True,'all_primary_E_RAM_PNG_references_verified':True,
            'source_and_disposable_saves_unchanged':True,'new_translation_completion_credit':0})
        reports.append((cap_name,report_path))
    context_path = Path('work/analysis/powder_fire_context_v1303c/source_and_actual_binding.json')
    context = read(context_path)
    assert len(context['actual_old_wording_holds']) == 1
    assert context['actual_old_wording_holds'][0]['source_selected_message_ID'] == 2053
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass']) == (1296,1379)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs']) == 83
    ROOT.mkdir(parents=True)
    proof_path = ROOT/'actual_old_fire_and_fixture_audits.json'
    save(proof_path,{'candidate_sha256':release['candidate_sha256'],'terminal_test_audits':audited,
        'old_fire_binding':str(context_path),'old_fire_binding_sha256':sha(context_path.read_bytes()),
        'new_six_translation_native_layout_release_and_revised_gameplay_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    files = {Path('translations/powder_fire_editorial_manuscript_v1.json'),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('docs/powder_fire_v1305_source_checkpoint.md'),Path('docs/translation_progress.md'),
        Path('docs/editorial_review_goal.md'),Path('docs/known_issues.md'),Path('docs/todo.md')}
    pattern = r'_v(?:129[6-9]|130[0-6])(?:[a-z])?'
    files.update(p for p in Path('scripts').glob('*.py') if re.search(pattern+r'\.py$',p.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(pattern+r'$',folder.name):
            files.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() != '.nds')
    retention = max(Path('work/rom_retention').glob('*.json'),key=lambda p:p.stat().st_mtime)
    plan = read(retention)
    assert all(Path(row['path']).is_file() for row in plan['roms'])
    pin = next(row for row in plan['roms'] if row['name'] == 'all_routes_combined_v1266_candidate.nds')
    assert pin['action'] == 'keep' and pin['reason'].startswith('pinned:')
    files.add(retention)
    DEST.mkdir(parents=True)
    archived = []
    for source in sorted(files,key=lambda p:str(p).lower()):
        target = DEST/'Workspace'/source.absolute().relative_to(repo)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        archived.append({'source':str(source),'archive':str(target.relative_to(DEST)),'sha256':digest})
    for name,source in reports:
        target = DEST/'Capture reports'/name/'capture_report.json'
        target.parent.mkdir(parents=True)
        copy2(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    for name,frame in [('old_powder_fire_2053',7210),('old_fire_extinguished_after_touch',7310)]:
        source = Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266')/f'frame_{frame:06d}_navigation.png'
        target = DEST/'Old wording source evidence - not finalized guide'/(name+'.png')
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    result = {'archive':str(DEST),'files':archived,'file_count':len(archived),'terminal_tests':audited,
        'source_reviewed_new_records':6,'completed_entries_added':0,'completed':1296,'source_prose_reviewed':1379,
        'all_copies_and_primary_E_RAM_PNG_files_hash_verified':True,
        'old_wording_images_separate_from_finalized_guide_screenshots':True,
        'all_originals_preserved_no_ROM_deleted_moved_or_rebuilt':True,'ROMs_in_preview_still_present':len(plan['roms']),
        'retention_preview':str(retention),'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',result)
    save(DEST/'archive_receipt.json',result)
    print(f'{len(archived)} checkpoint files archived;both terminal4MiB fixture/input audits and all capture references pass.',flush=True)


if __name__ == '__main__':
    main()
