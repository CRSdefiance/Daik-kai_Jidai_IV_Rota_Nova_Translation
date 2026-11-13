"""Normalize only equivalent local path separators in the preserved legacy proof reference."""
from pathlib import Path
from scripts.reconcile_remaining_story_sources_v2 import source
from scripts import reconcile_rafael_source_coverage_v1 as base
from scripts.qualify_lil_B294_legacy_source_binding_v1 import qualified_location,IDENT,OUT
from scripts.audit_story_glyph_consistency import load

def source_location(row):
    ordinary=base.source_location(row)
    if row.get('file_path')=='/data/SC2.DK4' and row['id']==IDENT and ordinary[1:]==(None,None):
        expected=load(OUT)['source_control_evidence']
        assert Path(row['source_control_evidence']).resolve()==Path(expected).resolve()
        return qualified_location({**row,'source_control_evidence':expected})
    return ordinary

exec(compile(source,__file__+'::same-exact-binding-semantic-local-path-normalization-only','exec'),globals())
