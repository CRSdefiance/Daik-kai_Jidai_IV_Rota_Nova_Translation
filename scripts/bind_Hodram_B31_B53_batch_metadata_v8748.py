"""Bind the approved unchanged rows to explicit source-owned route metadata."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_metadata_v8748')
OLD=Path('translations/hodram_B31_B53_editorial_manuscript_v4.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v5.json')
APPROVAL=Path('work/analysis/Hodram_B31_B53_format_v8745b/formatting_approval.json')
REFERENCES=Path('work/analysis/Hodram_B31_B53_references_v8738/references.json')
INPUT=Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,approval,refs,inp=map(read,[OLD,APPROVAL,REFERENCES,INPUT])
    assert approval['manuscript_sha256']==sha(OLD.read_bytes()) and approval['all3_five_gates_true']
    assert inp['expected_original_captain_ID']==1 and inp['registered_profile']=='all-routes-unified-v8704'
    assert old['current_ROM_sha256']==inp['current_ROM_sha256']==refs['parent_sha256'] and refs['blocks']==old['blocks']==[31,53]
    assert old['file_path']=='/data/SC1.DK4' and all(r['file_path']==old['file_path'] for r in old['records'])
    doc=deepcopy(old);doc.update(route=1,route_identity='Hodram',registered_predecessor_profile=inp['registered_profile'],
        predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        metadata_binding_note='Explicit route1/Hodram/SC1/blocks31and53 metadata is bound to the unchanged original EV1 references and the exact registered captain1 current context. Every approved row,word,compiled/stored byte,source/current/final reference,name packet andfive gates remains unchanged. No new editorial/native/actual approval orcredit is added.')
    assert doc['records']==old['records'] and doc['names_packet_sha256']==old['names_packet_sha256']
    assert all(doc[k]==old[k] for k in old if k not in ['predecessor_manuscript','predecessor_manuscript_sha256'])
    validate_natural_dialogue_batch(doc);save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'explicit_route_binding.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),
        route=1,route_identity='Hodram',file_path='/data/SC1.DK4',blocks=[31,53],all3_approved_rows_andnames_native_actual_formatting_values_exact=True,
        standard_natural_dialogue_v2_validation_pass=True,no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,APPROVAL,REFERENCES,INPUT,Path(__file__)]}))
    print('Explicit source-owned route1/Hodram/SC1 metadata bound;all3approved rows/names/compiledbytes/refs/gates unchanged. No new reviewcredit.',flush=True)
