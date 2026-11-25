"""Keep the field address distinct from the dereferenced string's own offset."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retainer_source_consumer_repair_v7828b')
    assert not root.exists()
    result=derive('scripts/review_retainer_source_name_consumer_v7828.py','scripts/review_retainer_source_name_consumer_v7828b.py',
        {'dict(offset=field_offset,**value)':'dict(table_field_offset=field_offset,**value)'})
    root.mkdir(parents=True)
    save(root/'provenance.json',dict(derivation=result,failed_original_preserved=True,
        correction='Avoid duplicate offset keyword; retain both the table-field offset and pointed-string offset.',
        no_native_guard_orclaim_changed=True,no_shared_mutation=True,full_goal_complete=False))
