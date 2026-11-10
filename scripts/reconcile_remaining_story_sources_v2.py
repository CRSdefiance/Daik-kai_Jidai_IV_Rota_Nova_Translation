"""Retain the exact source census with one independently qualified legacy metadata binding."""
from pathlib import Path
from scripts import reconcile_rafael_source_coverage_v1 as base
from scripts.qualify_lil_B294_legacy_source_binding_v1 import qualified_location,IDENT
from scripts.source_locked_derivation_v5118 import checked_text

def source_location(row):
    ordinary=base.source_location(row)
    if row.get('file_path')=='/data/SC2.DK4' and row['id']==IDENT and ordinary[1:] == (None,None):
        return qualified_location(row)
    return ordinary

source=checked_text(Path('scripts/reconcile_remaining_story_sources_v1.py').read_text(encoding='utf-8'),{
    "_v1')":"_v2')",
    "env={**vars(previous),'ROOT':root":"env={**vars(previous),'source_location':source_location,'ROOT':root",
})
exec(compile(source,__file__+'::same-native-inventory-with-exact-preserved-record-binding','exec'),globals())
