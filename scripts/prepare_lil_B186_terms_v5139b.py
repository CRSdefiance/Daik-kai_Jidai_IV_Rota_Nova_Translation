"""Preserve the untranslated alias finding; avoid claiming an unmade label fix."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_terms_preparation_v5139b')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/reconcile_lil_B186_terms_v5139.py','scripts/reconcile_lil_B186_terms_v5139b.py',{
        "terms_v5139')":"terms_v5139b')",
        "assert [r['text'] for r in live['rows']]==['Owner','Cook','Alexandria','Alexandria']":"assert [r['text'] for r in live['rows']]==['Owner','Cook','アレキサンドリア','Alexandria']",
        "    for city,current in zip(cities,live['rows'][2:],strict=True):city.update(current)":"    for city,current in zip(cities,live['rows'][2:],strict=True):\n        city.update(current);city['current_alias_already_English']=current['text']=='Alexandria'\n    save(ROOT/'untranslated_Alexandria_alias_unreviewed_caller_lead.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],pointer_field=0x1223E4,source_and_current_storage_offset=0x15E4D0,current_text='アレキサンドリア',approved_English='Alexandria',other_English_alias_field=0x1230B4,not_a_new_fix_or_name_widget_completion=True,caller_and_display_fidelity_unreviewed=True,new_review_credit=0,full_goal_complete=False))",
        "two_source_current_city_aliases=cities,city='Alexandria',":"two_source_current_city_aliases=cities,city='Alexandria',one_current_alias_still_Japanese_and_caller_unreviewed=True,",
        "print('Owner/Cook and two Alexandria aliases bound; twelve category calls distinguish broad Sweets from Treats4. Incidental old FE exposure disclosed; no credit.')":"print('Owner/Cook and two Alexandria identities bound:one Japanese alias remains an unreviewed caller lead. Twelve category calls distinguish Sweets from Treats4;old FE exposure disclosed;no credit.')",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_bound_alias_finding_successor.json',dict(derivation=row,original_stopped_producer_and_context_preserved=True,reason='The source alias at field1223E4/storage15E4D0 remains Japanese in the actual current snapshot. The separate1230B4 alias is Alexandria. Do not invent a completed translation or widget test.',new_review_credit=0,full_goal_complete=False))
    print('Prepared v5139b:retain both actual aliases and explicit unresolved Japanese label lead.')
