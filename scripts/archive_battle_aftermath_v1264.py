"""Copy the source/native checkpoint to the approved E-drive archive."""
import re
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

DESTINATION = Path('E:/Rota Nova translations/Editorial review/V1264 Aftermath native checkpoint')


def main():
    assert not DESTINATION.exists()
    repo = Path.cwd().absolute()
    checkpoint = read('work/analysis/battle_aftermath_checkpoint_v1264/native_checkpoint.json')
    paths = {Path(checkpoint['manuscript']),Path('translations/editorial_review_current_v1.json'),
        Path('translations/release_stack.json'),Path('translations/rom_retention_pins.json'),
        Path('docs/battle_aftermath_v1264_native_checkpoint.md'),Path('docs/translation_progress.md'),
        Path('docs/known_issues.md'),Path('docs/todo.md')}
    for path in Path('scripts').glob('*.py'):
        if re.search(r'_v(?:124[7-9]|125\d|126[0-4])(?:[a-z])?\.py$',path.name):
            paths.add(path)
    paths.update(Path('translations').glob('battle_aftermath_editorial_manuscript_v*.json'))
    for folder in Path('work/analysis').iterdir():
        if folder.is_dir() and re.search(r'_v(?:124[7-9]|125\d|126[0-4])(?:[a-z])?$',folder.name):
            paths.update(p for p in folder.rglob('*') if p.is_file() and p.suffix.lower() != '.nds')
    for path in checkpoint['proofs'].values():
        assert sha(Path(path['path']).read_bytes()) == path['sha256']
    DESTINATION.mkdir(parents=True)
    files = []
    for path in sorted(paths,key=lambda p:str(p).lower()):
        assert path.is_file() and path.suffix.lower() != '.nds'
        # Keep lexical repo paths across junctions; never resolve to E then
        # attempt relative_to(repo). No original file is moved or changed.
        relative = path.absolute().relative_to(repo)
        target = DESTINATION/'Workspace'/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        copy2(path,target)
        digest = sha(path.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source':str(path),'archive':str(target.relative_to(DESTINATION)),
            'bytes':target.stat().st_size,'sha256':digest})
    context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')
    source = Path(context['snapshot'])
    assert sha(source.read_bytes()) == context['snapshot_sha256']
    target = DESTINATION/'External inputs'/'V1224_before_duel_frame005770_arm9_ram.bin'
    target.parent.mkdir(parents=True)
    copy2(source,target)
    assert sha(target.read_bytes()) == context['snapshot_sha256']
    files.append({'source':str(source),'archive':str(target.relative_to(DESTINATION)),
        'bytes':target.stat().st_size,'sha256':context['snapshot_sha256']})
    receipt = {'archive':str(DESTINATION),'files':files,'file_count':len(files),
        'all_archived_files_hash_checked':True,'all_originals_preserved_no_ROM_moved_deleted_or_created':True,
        'latest_registered_ROM':'E:/Rota Nova translations/Generated/out/all_routes_combined_v1224_candidate.nds',
        'latest_registered_ROM_sha256':'cdc860e53267dbef64ac9d40a1832b00fda6a4da6adbde2b61be830345d55dbd',
        'reviewed_records':75,'native_font_cases':783,'completed_entries_added':0,
        'registered_release_patch_and_actual_scene_verification_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(DESTINATION/'archive_receipt.json',receipt)
    save('work/analysis/battle_aftermath_checkpoint_v1264/archive_receipt.json',receipt)
    print(str(len(files))+' checkpoint files copied and SHA-256 verified at '+str(DESTINATION),flush=True)


if __name__ == '__main__':
    main()
