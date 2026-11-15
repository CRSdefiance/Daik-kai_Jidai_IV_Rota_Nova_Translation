"""Successor uses exact batch-count replacements and preserves V1492 guard."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_refit_spritsail_release_v2285.py')
if __name__=='__main__':
 source=OLD.read_text().replace('refit_spritsail_release_v2285','refit_spritsail_release_v2285b');old="('492','493')";new="('==492','==493'),('all492_manifest','all493_manifest'),('manifest_batches=492','manifest_batches=493')";assert source.count(old)==1;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/refit_spritsail_release_v2285b/failure_successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='An overly broad492-to493 test-source replacement also changed the V1492 promotion assertion to V1493. The release remained V1492;the incorrect assertion rejected before patch creation.',successor_uses_exact_batch_count_replacements=True,V1492_promotion_guard_retained=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
