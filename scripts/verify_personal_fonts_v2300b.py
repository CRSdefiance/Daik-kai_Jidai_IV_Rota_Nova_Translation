"""Successor supplies the cloned projection helper's keyword-only mode default."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/verify_personal_fonts_v2300.py')
if __name__=='__main__':
 source=OLD.read_text().replace("personal_fonts_v2300'","personal_fonts_v2300b'");old="actor=row['actor_ID'],state=1)";new="actor=row['actor_ID'],state=1,forced_mode=None)";assert source.count(old)==1;source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/personal_fonts_v2300b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='FunctionType cloning does not copy keyword-only defaults;the supplied actor andstate still required an explicit forced_mode=None. The first complete font passed;no projection orformatting approval was recorded before rejection.',explicit_none_preserves_original_normal_mode=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
