"""Require exact release, patch, own cold boots and native context before any credit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    src=Path('scripts/lil_B231_completion_gates_v7520.py').read_text('utf8');a=src.index("    assert sum(len(r['base_QA_report']");b=src.index("    actual=read(doc['actual_English_proof'])",a);old=src[a:b].rstrip()
    new="    assert sum(len(r['base_QA_report']['exact_reviewed_base_warnings']) for r in doc['records'])==0 and sum(bool(r['row_count_reason']) for r in doc['records'])==3 and not any(r['qa_waivers'] or r['qa_waiver_reason'] for r in doc['records'])"
    derive('scripts/lil_B231_completion_gates_v7520.py','scripts/lil_B233_completion_gates_v7569.py',{old:new,'B231':'B233','release_v7515':'release_v7564','startup_v7518':'startup_v7567','registration_v7513':'registration_v7562','retention_v7516':'retention_v7565','all624_manifest_batches':'all625_manifest_batches','V7466':'V7514','v7514':'v7563',"reg['negative_count']==253":"reg['negative_count']==240","len(manifest['batches'])==624":"len(manifest['batches'])==625","r['block']==231":"r['block']==233",'runs_v7517':'runs_v7566','current_V7514_native_v7519':'current_V7563_native_v7568','all16':'all11','==16':'==11','all16_objects16_pages_actual_complete':'all11_objects11_pages_actual_complete','(16,16,63,63)':'(11,11,43,43)'})
