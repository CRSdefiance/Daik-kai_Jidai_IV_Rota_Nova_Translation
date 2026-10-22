"""Archive five-message completion,terminal evidence and unreviewed route leads."""
import re
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/flagship_capture_archive_v1372')
LEAD = Path('work/analysis/route_encounter_leads_v1372')
DEST = Path('E:/Rota Nova translations/Editorial review/V1372 Flagship capture completion')
RETENTION = Path('work/rom_retention/20261022T0305409411395Z.json')


def main():
    assert not ROOT.exists() and not LEAD.exists() and not DEST.exists()
    release = read('work/analysis/flagship_precision_release_v1363/registered_release_verification.json')
    for field in ['candidate','patch']:
        assert sha(Path(release[field]).read_bytes())==release[field+'_sha256']
    completion = read('work/analysis/flagship_capture_completion_v1371/completion_receipt.json')
    assert (completion['completed'],completion['source_prose'],completion['newly_completed'])==(1307,1395,5)
    ledger = read('translations/editorial_review_current_v1.json')
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1307,1395)
    plan = read(RETENTION)
    assert len(plan['roms'])==239 and sum(r['action']=='keep' for r in plan['roms'])==211
    assert all(Path(r['path']).is_file() for r in plan['roms'])
    for version in [1266,1316,1344,1364]:
        pin = next(r for r in plan['roms'] if r['name']==f'all_routes_combined_v{version}_candidate.nds')
        assert pin['action']=='keep' and pin['reason'].startswith('pinned:')
    rom,clean = NdsImage.open(release['candidate']),NdsImage.open('work/clean.nds')
    current = IlnkContainer.parse(rom.read_file('/data/SC1.DK4')).blocks[29]
    source = IlnkContainer.parse(clean.read_file('/data/SC1.DK4')).blocks[29]
    assert current.find(b'Willful.')==528
    LEAD.mkdir(parents=True)
    (LEAD/'SC1_B29_clean.bin').write_bytes(source)
    (LEAD/'SC1_B29_current.bin').write_bytes(current)
    leads = []
    for frame,token in [(6500,b'Willful.'),(6600,b'They mean to sink us'),(7700,b'Guns fire alone'),
                        (8100,b'Useful battle posts:'),(6000,b'Your fleet may have')]:
        offsets = [i for i in range(len(current)) if current.startswith(token,i)]
        assert offsets
        capture = Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364')/f'frame_{frame:06d}_navigation.png'
        leads.append({'frame':frame,'capture':str(capture),'capture_sha256':sha(capture.read_bytes()),
            'current_asset':'/data/SC1.DK4','block':29,'current_block_token_offsets':offsets,'token':token.decode('ascii'),
            'status':'observed-editorial-lead-only;clean-record-mapping-controls-and-Japanese-review-pending'})
    save(LEAD/'lead_manifest.json',{'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],
        'clean_ROM_sha256':sha(Path('work/clean.nds').read_bytes()),'current_SC1_sha256':sha(rom.read_file('/data/SC1.DK4')),
        'clean_SC1_sha256':sha(clean.read_file('/data/SC1.DK4')),'block':29,
        'complete_clean_block_sha256':sha(source),'complete_current_block_sha256':sha(current),'leads':leads,
        'do_not_infer_clean_record_offsets_from_translated_offsets_or_strip_control_prefixes':True,
        'source_prose_or_translation_completion_credit_added':0,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    paths = {Path('dk4tool/patch/flagship_capture_precision.py'),Path('scripts/build_integrated_release.py'),
        Path('translations/flagship_capture_precision_release_v1.json'),
        Path('translations/flagship_capture_precision_manuscript_v1.json'),Path('translations/flagship_capture_precision_manuscript_v2.json'),
        Path('translations/battle_aftermath_flagship_capture_final_review_v1.json'),
        Path('translations/battle_aftermath_editorial_manuscript_v3.json'),
        Path('translations/editorial_review_current_v1.json'),Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('docs/flagship_capture_v1371_completion.md'),Path('docs/translation_progress.md'),Path('docs/editorial_review_goal.md'),
        Path('docs/known_issues.md'),Path('docs/todo.md'),Path(release['candidate']).with_suffix('.manifest.json'),Path(release['patch']),RETENTION}
    pattern = r'_v(?:135\d|136\d|137[0-2])(?:[a-z])?'
    paths.update(p for p in Path('scripts').glob('*.py') if re.search(pattern+r'\.py$',p.name))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(pattern+r'$',folder.name):
            paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower()!='.nds')
    repo = Path.cwd().absolute()
    DEST.mkdir(parents=True)
    archived = []
    for path in sorted(paths,key=lambda p:str(p).lower()):
        assert path.is_file() and path.suffix.lower()!='.nds'
        target = DEST/'Workspace'/path.absolute().relative_to(repo)
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(path,target)
        digest = sha(path.read_bytes())
        assert sha(target.read_bytes())==digest
        archived.append({'source':str(path),'archive':str(target.relative_to(DEST)),'sha256':digest})
    caproot = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
    reports = []
    for name,frames in [('ship_sinking_v1350_1344',5400),('ship_sinking_v1353_1344',13200),
                        ('flagship_capture_v1369_1364',13200),('flagship_precision_v1364_newgame',4000),
                        ('flagship_precision_v1364_title',1150)]:
        path = caproot/name/'capture_report.json'
        report = read(path)
        assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete']
        ram = report['read_only_capture_RAM_snapshots']+report.get('read_only_pause_RAM_snapshots',[])
        for row in ram:
            assert sha(Path(row['path']).read_bytes())==row['sha256']
        for row in report['frames_captured']:
            assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        target = DEST/'Capture reports'/name/path.name
        target.parent.mkdir(parents=True)
        copy2(path,target)
        assert target.read_bytes()==path.read_bytes()
        reports.append({'report':str(path),'sha256':sha(path.read_bytes()),'terminal_frame':frames,
            'RAM_references':len(ram),'PNG_references':len(report['frames_captured']),
            'all_primary_E_capture_files_hash_verified_and_retained':True})
    guides = []
    for name in ['V1344 Flagship capture','V1364 Flagship capture']:
        for path in (Path('E:/Rota Nova translations/Guide screenshots')/name).iterdir():
            assert path.is_file()
            target = DEST/'Guide screenshots'/name/path.name
            target.parent.mkdir(parents=True,exist_ok=True)
            copy2(path,target)
            assert path.read_bytes()==target.read_bytes()
            guides.append({'source':str(path),'sha256':sha(path.read_bytes())})
    receipt = {'archive':str(DEST),'files':archived,'file_count':len(archived),'capture_reports':reports,'guide_files':guides,
        'candidate':release['candidate'],'candidate_sha256':release['candidate_sha256'],'patch_sha256':release['patch_sha256'],
        'completed':1307,'source_prose_reviewed':1395,'completed_capture_alternatives_added':5,'reviewed_incomplete_COMMON':88,
        'sinking16_still_pending_no_sinking_credit':True,'new_SC1_B29_leads_not_reviewed_or_completed':str(LEAD/'lead_manifest.json'),
        'all239_ROMs_still_present_preview_only_no_ApplyPlan':True,
        'all_originals_preserved_no_ROM_deleted_moved_or_rebuilt':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    ROOT.mkdir(parents=True)
    save(ROOT/'archive_receipt.json',receipt)
    save(DEST/'archive_receipt.json',receipt)
    print(f'{len(archived)} completion/source/release files archived;five terminal reports and all RAM/PNGs checked;239 ROMs retained.',flush=True)


if __name__=='__main__':
    main()
