"""Use the verified successor audit; preserve the earlier unexecuted research producer."""
from scripts.prepare_lil_B160_research_v3890 import *
if __name__=='__main__':
    DRAFT=Path('scripts/prepare_lil_B160_research_v3890.py');t=DRAFT.read_text(encoding='utf-8');assert t.count('editorial_handoff_verification_v3886/')==1;t=t.replace('editorial_handoff_verification_v3886/','editorial_handoff_verification_v3886e/');t=t.replace('producer_sha256=sha(Path(__file__).read_bytes())','producer_sha256=sha(Path(__file__).read_bytes()),preserved_draft=str(DRAFT),preserved_draft_sha256=sha(DRAFT.read_bytes())');exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=DRAFT))
