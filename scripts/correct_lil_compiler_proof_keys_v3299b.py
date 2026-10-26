"""Preserve3299; correct two inherited batch-qualified representative keys."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('dk4tool/patch/lil_B122_B127_editorial.py');new=Path('dk4tool/patch/lil_B122_B127_editorial_v2.py')
    regold=Path('scripts/register_lil_B122_B127_v3299.py');regnew=Path('scripts/register_lil_B122_B127_v3299b.py');assert not new.exists() and not regnew.exists()
    text=old.read_text(encoding='utf-8');assert text.count('B111_B119')==2;text=text.replace('B111_B119','B122_B127');compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    text=regold.read_text(encoding='utf-8').replace('lil_B122_B127_registration_v3299','lil_B122_B127_registration_v3299b').replace('from dk4tool.patch import lil_B122_B127_editorial as owned','from dk4tool.patch import lil_B122_B127_editorial_v2 as owned').replace('from dk4tool.patch.lil_B122_B127_editorial import apply_release','from dk4tool.patch.lil_B122_B127_editorial_v2 import apply_release').replace('release_stack_v3299_pending.json','release_stack_v3299b_pending.json')
    compile(text,str(regnew),'exec');regnew.write_text(text,encoding='utf-8')
    root=Path('work/analysis/lil_B122_B127_compiler_repair_v3299b');root.mkdir(parents=True)
    save(root/'preserved_failure_and_successor_provenance.json',dict(previous={str(p):sha(p.read_bytes()) for p in [old,regold]},successors={str(p):sha(p.read_bytes()) for p in [new,regnew]},failure='Positive in-memory reconstruction rejected two inherited B111_B119-qualified representative metadata names. Correct successor requires the actual reviewed B122_B127 names; all source/native/hash guards remain. No ROM,builder or registry was changed by failed3299.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
