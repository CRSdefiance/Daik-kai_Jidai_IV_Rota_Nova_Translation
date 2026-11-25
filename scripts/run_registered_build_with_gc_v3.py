"""Run original dependency-locked release code with tighter collection and the system allocator."""
import os
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load
from dk4tool.patch.grand_race_menu_release import sha

previous=Path('scripts/run_registered_build_with_gc_v1.py')
restoration_path=Path('work/analysis/ROM_path_lookup_memory_20261105/locked_core_restoration.json')
restoration=load(restoration_path)
assert os.environ.get('PYTHONMALLOC')=='malloc'
assert sha(Path('dk4tool/rom/nds.py').read_bytes())==restoration['restored_sha256']=='27ce07965815b1c71ce39ce166406507fab621631b2373a96733eccd75dc2963'
source=checked_text(previous.read_text(encoding='utf-8'),{
    'gc.set_threshold(100,5,5)':'gc.set_threshold(10,1,1)',
    'while not stop.wait(2):':'while not stop.wait(0.25):',
    'gc_thresholds=[100,5,5],collection_interval_seconds=2':'gc_thresholds=[10,1,1],collection_interval_seconds=0.25',
    'no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0)':
        "no_test_skip_rewrite_orrelaxed_release_contract=True,new_credit=0,\n        original_locked_ROM_core_sha256=restoration['restored_sha256'],PYTHONMALLOC='malloc',\n        core_restoration=str(restoration_path),core_restoration_sha256=sha(restoration_path.read_bytes()),\n        no_concurrent_editorial_native_orDeSmuME_jobs_at_launch=True)",
    'unchanged=registry.read_bytes()==registry_before and all(sha(Path(p).read_bytes())==value for p,value in pins.items())':
        "unchanged=registry.read_bytes()==registry_before and all(sha(Path(p).read_bytes())==value for p,value in pins.items()) and sha(Path('dk4tool/rom/nds.py').read_bytes())==restoration['restored_sha256']",
})
if __name__=='__main__':exec(compile(source,str(previous)+'::unchanged-locked-sources-tighter-collection-system-allocator','exec'),globals())
