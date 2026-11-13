"""Preserve V3782 and correct one input-snapshot reference without changing reviewed prose."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B157_provenance_amendment_v3784')
OLD=Path('work/analysis/lil_B157_completion_v3782/completion_receipt.json')
OLD_FINAL=Path('translations/lil_B157_contextual_final_review_v1.json')
FINAL=Path('translations/lil_B157_contextual_final_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists();old=read(OLD);lp=Path('translations/editorial_review_current_v1.json');docs=[Path('docs')/n for n in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']]
    for p,d in old['updated_files'].items():assert sha(Path(p).read_bytes())==d,p
    wrong='docs\\known_issues.md';snapshot=Path('work/analysis/lil_B157_completion_v3782/known_issues.md.before');assert old['evidence'][wrong]==sha(snapshot.read_bytes());draft=Path('scripts/complete_lil_B157_v3782.py');wrapper=Path('scripts/complete_lil_B157_v3782b.py')
    ROOT.mkdir(parents=True)
    for p in [lp,*docs]:copy2(p,ROOT/(p.name+'.before'))
    def amend(value):
        if isinstance(value,dict):
            out={}
            for k,v in value.items():
                if k=='evidence' and isinstance(v,dict) and wrong in v:
                    assert v[wrong]==sha(snapshot.read_bytes());v={str(snapshot) if a==wrong else a:b for a,b in v.items()};v.update({str(draft):sha(draft.read_bytes()),str(wrapper):sha(wrapper.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())})
                out[k]=amend(v)
            return out
        if isinstance(value,list):return [amend(v) for v in value]
        if isinstance(value,str) and value in [str(OLD_FINAL),OLD_FINAL.as_posix()]:return str(FINAL)
        return value
    final=amend(read(OLD_FINAL));final['previous_final_review']=str(OLD_FINAL);final['previous_final_review_sha256']=sha(OLD_FINAL.read_bytes());final['provenance_amendment']='Bind the pre-completion known_issues input to its preserved .before snapshot and bind both completion producers explicitly. No source, English, native proof, ROM, patch, decision or coverage change.';assert final['records']==read(OLD_FINAL)['records'];save(FINAL,final)
    ledger=amend(read(lp));ledger['lil_B157_provenance_amendment_v3784']=dict(previous_completion_receipt=str(OLD),previous_completion_receipt_sha256=sha(OLD.read_bytes()),previous_final_review=str(OLD_FINAL),previous_final_review_sha256=sha(OLD_FINAL.read_bytes()),final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),input_snapshot=str(snapshot),input_snapshot_sha256=sha(snapshot.read_bytes()),cause='A wrapper variable named p was rebound by the completion backup loop; the intended producer entry captured the pre-write known_issues input. Its hash is exact for the preserved input snapshot.',source_English_decisions_ROM_patch_and_coverage_unchanged=True,full_goal_complete=False);save(lp,ledger)
    note='## V3784: B157 provenance reference clarified\n\nThe V3782 completion is retained. Its pre-completion known_issues input hash is now bound to the preserved .before snapshot, and both completion producers are explicitly hashed in final review v2. All75 records,31 revisions/44 retentions,5329 completed rereads,5332 source/prose reviews and the verified V3778 ROM/clean-input patch are unchanged. Full editorial goal remains active; continue the other82 B158-B160 objects and all wider scope.\n\n'
    for i,p in enumerate(docs):
        first,rest=p.read_text(encoding='utf-8').split('\n',1);p.write_text(('# Current editorial handoff - V3784' if i==0 else first)+'\n\n'+note+rest.replace(OLD_FINAL.as_posix(),FINAL.as_posix()),encoding='utf-8',newline='\n')
    receipt=amend(deepcopy(old));receipt['checkpoint']='V3784';receipt['evidence'].pop(str(OLD_FINAL),None);receipt['evidence'].update({str(FINAL):sha(FINAL.read_bytes()),str(OLD):sha(OLD.read_bytes()),str(OLD_FINAL):sha(OLD_FINAL.read_bytes())});receipt['updated_files']={str(p):sha(p.read_bytes()) for p in [lp,*docs]};receipt['provenance_amendment']=ledger['lil_B157_provenance_amendment_v3784'];receipt['original_completion_updated_files_verified_against_amendment_backups']=True;save(ROOT/'completion_receipt.json',receipt);print('Preserved V3782; corrected input snapshot/producers in final v2 and ledger. All75 prose/decisions/ROM/patch/counts unchanged.')
