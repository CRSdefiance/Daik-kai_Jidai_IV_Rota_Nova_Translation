"""Keep generated draft and create the actual-newline completion successor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/complete_lil_B131_B133_v3342b.py');new=Path('scripts/complete_lil_B131_B133_v3342e.py');assert not new.exists()
    t=old.read_text(encoding='utf-8');before=t
    t=t.replace('\\\\n','\\n');assert t!=before
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_completion_newlines_v3342d');root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),change='Use actual newlines in generated progress Markdown.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
