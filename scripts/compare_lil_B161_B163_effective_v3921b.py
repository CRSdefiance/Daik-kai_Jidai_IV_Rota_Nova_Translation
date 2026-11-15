"""Preserve the comparison draft and bind the corrected scope successor."""
from pathlib import Path
if __name__=='__main__':
    PRESERVED=Path('scripts/compare_lil_B161_B163_effective_v3921.py');t=PRESERVED.read_text(encoding='utf-8');assert t.count('lil_B161_B163_scope_v3920/')==2;t=t.replace('lil_B161_B163_scope_v3920/','lil_B161_B163_scope_v3920b/');needle='draft_producer_sha256=sha(DRAFT.read_bytes())';assert needle in t;t=t.replace(needle,needle+",preserved_comparison_draft='scripts/compare_lil_B161_B163_effective_v3921.py',preserved_comparison_draft_sha256=sha(Path(\"scripts/compare_lil_B161_B163_effective_v3921.py\").read_bytes())");exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__))
