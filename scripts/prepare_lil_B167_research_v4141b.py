"""Resume the interrupted tool derivation; verify already-created files without rewriting."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive
from scripts.verify_village_wrap_v608 import save
def checked_derive(a,b,changes):
    source=Path(a).read_text(encoding='utf-8');changes=dict(changes)
    # This shared path substitution is unused by the census/control scripts.
    if 'lil_B166_research_v4096' not in source:changes.pop('lil_B166_research_v4096',None)
    for old in changes:assert old in source,(a,old)
    expected=re.sub('|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    if Path(b).exists():
        assert Path(b).read_text(encoding='utf-8')==expected,b
        return dict(previous=a,previous_sha256=sha(Path(a).read_bytes()),successor=b,successor_sha256=sha(Path(b).read_bytes()),existing_partial_derivation_verified_without_rewrite=True)
    return original_derive(a,b,changes)
if __name__=='__main__':
    source=Path('scripts/prepare_lil_B167_research_v4141.py');text=source.read_text(encoding='utf-8')
    old='from scripts.prepare_lil_B156_layout_v3705 import derive';assert text.count(old)==1
    exec(compile(text.replace(old,'derive=checked_derive'),str(source)+'::verified-resume','exec'),dict(globals()))
    save(Path('work/analysis/lil_B167_research_tools_v4141/partial_derivation_recovery.json'),dict(original_failure='Unused common lil_B166_research_v4096 substitution absent from census script; first two generated scripts verified exact and preserved.',original_producer=str(source),original_producer_sha256=sha(source.read_bytes()),resume_producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_ledger_or_registry_changes=True))
