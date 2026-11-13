"""Independently audit the immutable original completion and its exact provenance amendment."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
if __name__=='__main__':
    original=Path('work/analysis/lil_B157_completion_v3782/completion_receipt.json');amendroot=Path('work/analysis/lil_B157_provenance_amendment_v3784');amended=amendroot/'completion_receipt.json';r=read(amended);old=read(original)
    assert r['provenance_amendment']['previous_completion_receipt_sha256']==sha(original.read_bytes())
    for p,d in old['updated_files'].items():assert sha((amendroot/(Path(p).name+'.before')).read_bytes())==d
    for p,d in old['evidence'].items():
        target=Path('work/analysis/lil_B157_completion_v3782/known_issues.md.before') if p=='docs\\known_issues.md' else Path(p);assert sha(target.read_bytes())==d,p
    final=read(r['provenance_amendment']['final_review']);prior=read(r['provenance_amendment']['previous_final_review']);assert final['records']==prior['records'] and (final['revised'],final['retained'],final['candidate_sha256'])==(prior['revised'],prior['retained'],prior['candidate_sha256'])
    p=Path('scripts/verify_editorial_handoff_v3783.py');t=p.read_text(encoding='utf-8');changes={
        "ROOT=Path('work/analysis/editorial_handoff_verification_v3783')":"ROOT=Path('work/analysis/editorial_handoff_verification_v3785')",
        "rp=CHECKPOINT/'completion_receipt.json';receipt=read(rp)":"rp=Path('work/analysis/lil_B157_provenance_amendment_v3784/completion_receipt.json');receipt=read(rp)",
        "assert jp[n][at:at+len(v)]==v and jp[n][at+len(v)]==0;ref=":"assert jp[n][at:at+len(v)]==v and jp[n][at+len(v)]==0 and jp[n][at-5:at+1].hex()==r['source_complete_preamble_hex'];ref=",
        "startswith('# Current editorial handoff - V3782')":"startswith('# Current editorial handoff - V3784')",
        "checkpoint='V3782'":"checkpoint='V3784'",
        'V3738/531batches/exactpatch;76new references andhonest76-panel fixture coverage.':'V3778/532 batches/exact patch;75 new references and disclosed75-panel/seven-actor/two-FE fixture coverage.',
    }
    for a,b in changes.items():assert t.count(a)==1,(a,t.count(a));t=t.replace(a,b)
    exec(compile(t,str(p)+'::verified-input-snapshot-amendment-and-complete-clean-preamble','exec'),dict(__name__='__main__',__file__=__file__))
