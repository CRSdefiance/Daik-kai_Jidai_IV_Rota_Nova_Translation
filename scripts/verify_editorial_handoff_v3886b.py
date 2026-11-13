"""Preserve the failed audit; correct its overlapping leaf-key/count substitution."""
from pathlib import Path
if __name__=='__main__':
    AUDIT_DRAFT=Path('scripts/verify_editorial_handoff_v3886.py');t=AUDIT_DRAFT.read_text(encoding='utf-8');needle=";t=t.replace('producer_sha256=sha(Path(__file__).read_bytes())'";assert t.count(needle)==1;t=t.replace(needle,";t=t.replace(\"len(effects['all12_nonrelative_source_current_control_leaves'])==23\",\"len(effects['all12_nonrelative_source_current_control_leaves'])==12\")"+needle);t=t.replace("draft_producer_sha256=sha(DRAFT.read_bytes())'","draft_producer_sha256=sha(DRAFT.read_bytes()),preserved_failed_audit=\"+repr(str(AUDIT_DRAFT))+\",preserved_failed_audit_sha256=\"+repr(__import__('hashlib').sha256(AUDIT_DRAFT.read_bytes()).hexdigest())+\"'")
    exec(compile(t,str(AUDIT_DRAFT)+'::leaf-count-successor','exec'),dict(__name__='__main__',__file__=__file__))
