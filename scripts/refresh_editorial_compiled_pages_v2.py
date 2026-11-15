"""Reuse exact old proofs across immutable manuscript successors; recheck changed text."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/refresh_editorial_compiled_pages.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    "    assert plan['manuscript_sha256']==previous['manuscript_sha256']==sha(args.manuscript.read_bytes())":
    """    assert plan['manuscript_sha256']==sha(args.manuscript.read_bytes())
    old_doc_path=Path(previous['manuscript'])
    assert sha(old_doc_path.read_bytes())==previous['manuscript_sha256']
    old_doc=load(old_doc_path)
    assert doc['current_ROM_sha256']==old_doc['current_ROM_sha256']
    typed_ids=[r['id'] for r in doc['records'] if r['kind']=='typed-choice-label']
    doc['records']=[r for r in doc['records'] if r['kind'] in ['progressive','system-FE']]
    old_records={r['id']:r for r in old_doc['records'] if r['kind'] in ['progressive','system-FE']}
    assert len(doc['records'])==doc['physical_speech_objects'] and len(typed_ids)==doc['typed_choice_objects']
    for row in doc['records']:
        old=old_records[row['id']]
        for key in ['source_reference','current_reference','source_hex','current_hex','source_selector','kind']:
            assert row[key]==old[key],(row['id'],key)""",
    "    assert sha(old_plan_path.read_bytes())==previous['plan_sha256']":
    """    assert sha(old_plan_path.read_bytes())==previous['plan_sha256']
    assert load(old_plan_path)['manuscript_sha256']==previous['manuscript_sha256']""",
    "        revised=sum(r['decision']=='revision' for r in subset['records']),":
    """        physical_speech_objects=len(changed),typed_choice_objects=0,
        revised=sum(r['decision']=='revision' for r in subset['records']),""",
    "        '--manuscript',str(subset_path),'--plan',str(subplan_path),":
    "        '--manuscript',str(subset_path),'--plan',str(subplan_path),",
    "        manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),":
    """        manuscript=str(args.manuscript),manuscript_sha256=sha(args.manuscript.read_bytes()),
        excluded_typed_choice_IDs_separately_pending=typed_ids,
        unchanged_source_current_bindings_checked=True,immutable_prior_manuscript=str(old_doc_path),""",
})
exec(compile(source,__file__+'::immutable-manuscript-successor-reuse','exec'),globals())
