"""Explicit route andregistered predecessor metadata;all82 approved records stay exact."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_metadata_v8829')
OLD=Path('translations/hodram_B54_B60_editorial_manuscript_v3.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v4.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')
APPROVAL=Path('work/analysis/Hodram_B54_B60_format_v8826/formatting_approval.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,inp,approval=map(read,[OLD,INPUT,APPROVAL])
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v8778'
    assert ledger['current_integrated_candidate']['sha256']==old['current_ROM_sha256']==inp['current_ROM_sha256']
    assert approval['manuscript_sha256']==sha(OLD.read_bytes()) and approval['all82_five_gates_true']
    assert old['file_path']=='/data/SC1.DK4' and old['blocks']==list(range(54,61)) and len(old['records'])==82
    doc=deepcopy(old);doc.update(route=1,route_identity='Hodram',registered_predecessor_profile='all-routes-unified-v8778',
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        route_metadata_is_file_EV1_owncaptain1_bound_not_name_orblocknumber_guess=True)
    assert doc['records']==old['records'];validate_natural_dialogue_batch(doc);save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'explicit_route_binding.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),
        route=1,route_identity='Hodram',source_file='/data/SC1.DK4',registered_predecessor_profile='all-routes-unified-v8778',
        all82_complete_records_approved_words_bytes_refs_andfivegates_unchanged=True,new_credit=0,no_ROM_registry_orledger_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,INPUT,APPROVAL,Path(__file__)]}))
    print('Explicit SC1/Hodram/V8778 route binding added;all82 approved records exact;standardv2 passes.No credit.')
