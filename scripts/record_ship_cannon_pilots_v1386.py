"""Record verified cannon/anchor pilots with no premature editorial credit."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_cannon_checkpoint_v1386')
DEST = Path('E:/Rota Nova translations/Editorial review/V1386 Cannon and anchor pilots')
PILOTS = [Path('work/analysis/ship_loadout_pilot_verified_v1381/actual_loadout_pilot_verification.json'),
    Path('work/analysis/ship_anchor_verified_v1385/actual_anchor_pilot_verification.json')]


if __name__=='__main__':
    assert not ROOT.exists() and not DEST.exists()
    pilots = [read(p) for p in PILOTS]
    assert all(p['entire4MiB_sole_prebattle45_owned_byte_fixture_and_all_input_schedule_audited'] for p in pilots)
    assert pilots[0]['terminal_frame']==11830 and pilots[1]['terminal_frame']==13480
    assert pilots[0]['target_Hull_Crew_before_duel']==[10,12]
    assert pilots[1]['actual_target_Hull_Crew_after_original_anchored_gunfire']==[5,6]
    assert all(p['source_and_disposable_donor_unchanged'] for p in pilots)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before = deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1307,1395)
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==88
    assert set(range(2058,2074))<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    summary = ('V1385 verifies two original V1364 equipment pilots after the inconclusive V1373 gunnery test. '
        'A clean-source cannon census explains why light escort shots exhaust crews before sinking:original '
        'Saker/zero-battery broadside base Hull damage is0 while crew casualties use separate original RNG(6). '
        'The flagship originally uses Culverin,strength2;the declared prebattle loadout selects original Heavy '
        'Cannon4,strength5,and NoGun7 for four escorts. One45-owned-byte fixture at4800 contains the prior40 live '
        'position bytes plus five cannon-type model bytes. Full4MiB/input/PNG/RAM/save audits prove no direct '
        'enemy health,crew,actor/ID,RNG,result or later battle/duel mutation. '
        'V1379 naturally reduces the target to Hull10/Crew12 but a coast collision turns the flagship west and '
        'a proximity duel begins11830 without any touchscreen input. This corrects the earlier assumption that '
        'touch alone caused boarding. The harness stops at the intro without modifying the duel. '
        'V1383 replays exactly through10090 and ordinary B closes sails;all five positions stay fixed through13340. '
        'Original anchored fire reduces the target to Hull5/Crew6. A separate Charles work report is visibly held '
        'and dismissed normally;it is not sinking evidence. The target escapes Heavy Cannon range and remains '
        'afloat at13480. Original getter48144 proves Heavy Cannon range160 and Carronade5 range224,with equal '
        'strength5. Next use Carronade only in a fresh declared prebattle fixture and the established safe anchor '
        'position;do not lower enemy health or alter RNG/results. '
        'No sinking,withdrawal or new editorial completion credit. Counts remain1307 complete(975 revised332 '
        'retained),1395 source/prose,88 reviewed-incomplete COMMON(16 sinking34 aftermath38 older),plus broader '
        'shared/routes/raw prose. Registered V1364/exact patch,canonical,V997,all graphics/all18 plaques and the '
        'later older-record re-audit remain unchanged/open. Full goal active.')
    document = Path('docs/ship_cannon_pilots_v1386_checkpoint.md')
    assert not document.exists()
    document.write_text('# V1386 cannon/anchor pilots: sinking still pending\n\n'+summary+
        '\n\n## Evidence\n\n'+''.join('- `'+str(p)+'`\n' for p in PILOTS)+
        '- Clean-source cannon census: `work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json`.\n'
        '- Pilot capture folders: `E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_loadout_v1379_1364` '
        'and `E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_anchor_v1383_1364`.\n'
        '- Current experimental ROM SHA-256: `'+pilots[0]['candidate_sha256']+'`.\n\n'
        'No new ROM was built or handed off. No new finalized guide image is claimed. These are targeted '
        'headless tests,not earned travel,a whole-route playthrough,or hardware verification. '\
        'The photographed shop676/677 formatting repair stays preserved and remains a regression reference;'
        'uniform margins,complete first/final letters,wraps,pagination,bounds and following transitions stay '
        'part of the full editorial audit.\n',encoding='utf-8')
    for name in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md']:
        path = Path(name)
        text = path.read_text(encoding='utf-8')
        assert '## V1386 cannon/anchor pilots' not in text
        path.write_text(text+'\n\n## V1386 cannon/anchor pilots\n\n'+summary+
            '\n\nSee [checkpoint](ship_cannon_pilots_v1386_checkpoint.md).\n',encoding='utf-8')
    checkpoint = {'id':'V1386-cannon-and-anchor-pilots-no-sinking-credit',
        'proofs':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in PILOTS],
        'source_census':'work/analysis/ship_cannon_setup_v1377/source_cannon_setup.json',
        'completed_entries_added':0,'source_prose_entries_added':0,
        'finding':'Original target reaches5Hull6Crew;proximity can trigger a duel without touch. Carronade5 retains strength5 with range224 versus Heavy Cannon160.',
        'next_action':pilots[1]['next_source_bound_loadout_candidate']}
    assert not any(c['id']==checkpoint['id'] for c in ledger['research_checkpoints'])
    ledger['research_checkpoints'].append(checkpoint)
    assert {k:v for k,v in ledger.items() if k!='research_checkpoints'}=={k:v for k,v in before.items() if k!='research_checkpoints'}
    ROOT.mkdir(parents=True)
    save(ROOT/'ledger_before.json',before)
    save(ledger_path,ledger)
    save(ROOT/'checkpoint_receipt.json',{'completed_unchanged':1307,'source_prose_unchanged':1395,
        'reviewed_incomplete_unchanged':88,'all16_sinking_entries_still_open':True,
        'ledger_after_sha256':sha(ledger_path.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes())})
    DEST.mkdir(parents=True)
    paths = [document,Path(__file__),ledger_path]+PILOTS
    paths += [Path(p) for p in ['docs/known_issues.md','docs/todo.md','docs/translation_progress.md',
        'scripts/research_ship_cannon_setup_v1377.py','scripts/native_ship_cannon_fixture_v1378.py',
        'scripts/run_ship_sinking_loadout_v1379.py','scripts/inspect_ship_loadout_live_v1380.py',
        'scripts/verify_ship_loadout_pilot_v1381.py','scripts/run_ship_sinking_anchor_v1383.py',
        'scripts/inspect_ship_anchor_live_v1384.py','scripts/verify_ship_anchor_pilot_v1385.py']]
    for folder in ['work/analysis/ship_cannon_setup_v1377','work/analysis/ship_sinking_loadout_v1379',
        'work/analysis/ship_loadout_inspection_v1380','work/analysis/ship_loadout_pilot_verified_v1381',
        'work/analysis/ship_sinking_anchor_v1383','work/analysis/ship_anchor_inspection_v1384',
        'work/analysis/ship_anchor_verified_v1385',str(ROOT)]:
        paths += list(Path(folder).glob('*.json'))+list(Path(folder).glob('*.jsonl'))
    copied = []
    workspace = Path.cwd().absolute()
    for source in sorted(set(paths)):
        target = DEST/'workspace'/source.absolute().relative_to(workspace)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(source,target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes())==digest
        copied.append({'source':str(source),'archive':str(target),'sha256':digest})
    cohorts = []
    for proof in pilots:
        report_path = Path(proof['terminal_report'])
        assert sha(report_path.read_bytes())==proof['terminal_report_sha256']
        report = read(report_path)
        refs = []
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
            refs.append({'path':row['path'],'sha256':row['PNG_sha256'],'kind':'PNG'})
        for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
            assert sha(Path(row['path']).read_bytes())==row['sha256']
            refs.append({'path':row['path'],'sha256':row['sha256'],'kind':'read-only-RAM'})
        for name in ['capture_report.json','navigation_command_journal.json']:
            source = report_path.parent/name
            target = DEST/'terminal_records'/report_path.parent.name/name
            target.parent.mkdir(parents=True,exist_ok=True)
            copy2(source,target)
            assert sha(target.read_bytes())==sha(source.read_bytes())
        cohorts.append({'report':str(report_path),'sha256':proof['terminal_report_sha256'],
            'original_E_drive_captures_preserved_and_verified':refs})
    receipt = {'archive':str(DEST),'workspace_files':copied,'terminal_cohorts':cohorts,
        'all_originals_preserved_no_ROM_build_move_delete_or_change':True,
        'completion_counts_unchanged':1307,'source_prose_unchanged':1395,'reviewed_incomplete_unchanged':88,
        'no_sinking_completion_or_finalized_guide_image_claim':True,'full_goal_complete':False}
    save(ROOT/'archive_receipt.json',receipt)
    copy2(ROOT/'archive_receipt.json',DEST/'archive_receipt.json')
    print(f'Two terminal pilots/source-cannon evidence archived:{len(copied)} files;all16 sinking entries remain open.',flush=True)
