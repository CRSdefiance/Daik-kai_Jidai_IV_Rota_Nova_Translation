"""Bind the scope successor after deriving the final code, preserving both comparison drafts."""
from pathlib import Path
import hashlib
if __name__=='__main__':
    drafts=[Path('scripts/compare_lil_B161_B163_effective_v3921.py'),Path('scripts/compare_lil_B161_B163_effective_v3921b.py')];s=drafts[0].read_text(encoding='utf-8');prefix,tail=s.rsplit(';exec(compile(t',1);assert tail;ns=dict(__name__='__main__',__file__=__file__);exec(compile(prefix,'comparison-transform-only','exec'),ns);t=ns['t'];assert t.count('lil_B161_B163_scope_v3920/')==2;t=t.replace('lil_B161_B163_scope_v3920/','lil_B161_B163_scope_v3920b/');needle='producer_sha256=sha(PRODUCER.read_bytes())';assert t.count(needle)==1;t=t.replace(needle,needle+',preserved_comparison_drafts='+repr({str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in drafts}));exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,PRODUCER=Path(__file__),DRAFT=Path('scripts/compare_lil_B159_effective_v3831.py')))
