"""Correct only the root gate-declaration schema; preserve all three approved records."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_gate_metadata_v8516')
OLD=Path('translations/hodram_B50_editorial_manuscript_v4.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old=read(OLD);doc=deepcopy(old)
    gates=['source','context','localization','naturalness','formatting']
    assert old['review_gates']==dict.fromkeys(gates,True) and all(all(r['review'].get(g) is True for g in gates) for r in old['records'])
    try:validate_natural_dialogue_batch(old)
    except ValueError as error:
        diagnostic=str(error);assert 'requires source, context, localization, naturalness, and formatting gates' in diagnostic
    else:raise AssertionError('Preserved dictionary declaration unexpectedly accepted')
    doc['review_gates']=gates
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()))
    assert doc['records']==old['records'] and doc['names_packet']==old['names_packet'] and doc['names_packet_sha256']==old['names_packet_sha256']
    assert {k for k in old if old[k]!=doc[k]}=={'review_gates','predecessor_manuscript','predecessor_manuscript_sha256'}
    validate_natural_dialogue_batch(doc);ROOT.mkdir(parents=True);save(DOC,doc)
    save(ROOT/'metadata_approval.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor=str(OLD),predecessor_sha256=sha(OLD.read_bytes()),preserved_standard_rejection=diagnostic,only_root_gate_declaration_andpredecessor_metadata_changed=True,all_source_current_final_records_names_prose_compiled_bytes_individual_gates_andactual_evidence_value_exact=True,standard_natural_dialogue_v2_passes_without_validator_change=True,new_credit=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('B50 root gate-declaration schema corrected;standardv2 passes;all three approved records/names/bytes/evidence unchanged;rejected predecessor preserved.')
