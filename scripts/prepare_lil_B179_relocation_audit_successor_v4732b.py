"""Preserve the stopped audit and bind every pending counter to B179, not B178."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/verify_editorial_handoff_v4732.py','scripts/verify_editorial_handoff_v4732b.py',{
    "len({historical_key(r) for r in fresh['record_keys']})==5898":
        "len({historical_key(r) for r in fresh['record_keys']})==5912",
    "ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==4045":
        "ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==4059",
    "scope=ledger['unfinished_editorial_scope_v4679']":"scope=ledger['unfinished_editorial_scope_v4727']",
    "scope['remaining_B179_B180_physical_speeches']==25":"scope['remaining_B180_physical_speeches']==11",
    "scope['incomplete_route_source_prose']==13":"scope['incomplete_route_source_prose']==14",
    "len(rows)==13 and Counter(r['editorial_decision'] for r in rows)=={'revise':2,'retain-wording':11}":
        "len(rows)==14 and Counter(r['editorial_decision'] for r in rows)=={'revise':8,'retain-wording':6}",
    "assert sha(Path(scope['path']).read_bytes())==scope['sha256']":
        "assert sha(Path(scope['path']).read_bytes())==scope['sha256']\n    assert read(scope['path'])['untranslated_Sao_Jorge_alias_lead']['id']=='ARM9-Sao-Jorge-alias-15E5D4-pointer122504'",
})
print('Prepared corrected B179 independent audit; original failure and metadata retained.')
