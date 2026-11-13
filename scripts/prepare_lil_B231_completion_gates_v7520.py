"""Derive exact release/startup/native gates with the sole approved article warning."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    src=Path('scripts/lil_B230_completion_gates_v7472.py').read_text('utf8');old=next(s for s in src.splitlines() if 'assert not sum(' in s)
    new="""    assert sum(len(r['base_QA_report']['exact_reviewed_base_warnings']) for r in doc['records'])==1 and sum(bool(r['row_count_reason']) for r in doc['records'])==4
    special=next(r for r in doc['records'] if r['source_record_index']==35)
    assert special['exact_reviewed_base_warnings']==[dict(severity='warning',code='weak-line-ending',message="line 2 ends with weak wrap word 'the'")] and special['qa_waivers']==['weak-line-ending'] and special['qa_waiver_reason']"""
    derive('scripts/lil_B230_completion_gates_v7472.py','scripts/lil_B231_completion_gates_v7520.py',{old:new,'B230':'B231','release_v7467':'release_v7515','startup_v7470':'startup_v7518','registration_v7465':'registration_v7513','retention_v7468':'retention_v7516','all623_manifest_batches':'all624_manifest_batches','V7418':'V7466','v7466':'v7514',"len(manifest['batches'])==623":"len(manifest['batches'])==624","r['block']==230":"r['block']==231",'runs_v7469':'runs_v7517','current_V7466_native_v7471':'current_V7514_native_v7519','all17':'all16','==17':'==16','all17_objects17_pages_actual_complete':'all16_objects16_pages_actual_complete','(17,17,67,67)':'(16,16,63,63)'})
