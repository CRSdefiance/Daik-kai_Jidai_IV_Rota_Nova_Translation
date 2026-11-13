"""Resume after pre-write census-key assertions; reuse the two exact generated tools."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

def derive_resume(a,b,changes):
    a,b=Path(a),Path(b);text=a.read_text(encoding='utf-8')
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    compile(text,str(b),'exec')
    if b.exists():assert b.read_bytes()==text.encode('utf-8'),str(b)
    else:b.write_text(text,encoding='utf-8',newline='\n')
    return dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()))

if __name__=='__main__':
    source=Path(__file__).with_name('prepare_lil_B175_research_v4525.py');text=source.read_text(encoding='utf-8')
    fixes={
        'from scripts.prepare_lil_B156_layout_v3705 import derive':'derive=RESUME_DERIVE',
        "'all39_commands_four_relative_sites_and_shipped_entry_census':":"'all45_commands_four_relative_sites_and_shipped_entry_census':",
        "'all39_clean_current_target_commands_and_four_relative_sites_reexecuted':":"'all45_clean_current_target_commands_and_four_relative_sites_reexecuted':",
    }
    for old,new in fixes.items():assert old in text; text=text.replace(old,new)
    exec(compile(text,str(source)+'::corrected-census-keys','exec'),
         {'__name__':'__main__','__file__':str(source),'RESUME_DERIVE':derive_resume})
